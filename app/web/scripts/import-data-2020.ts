/**
 * Import Resilience Data (2020 Census Boundaries) to Postgres
 *
 * This script imports the rebuilt data that uses consistent 2020 Census boundaries.
 *
 * Run with: DATABASE_URL="..." npx tsx scripts/import-data-2020.ts
 *
 * Error Handling:
 * - Transient errors (network timeouts) are retried with individual inserts
 * - Fatal errors (constraint violations, malformed data) abort the import
 * - Population mismatches between duplicate tract entries are logged
 */

import postgres from 'postgres';
import { createReadStream, statSync, existsSync } from 'fs';
import { parse } from 'csv-parse';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const DATABASE_URL = process.env.DATABASE_URL;

if (!DATABASE_URL) {
	console.error('DATABASE_URL environment variable is required');
	process.exit(1);
}

const sql = postgres(DATABASE_URL, {
	ssl: DATABASE_URL.includes('fly') ? 'require' : false,
	connect_timeout: 30,
});

// Path to the data files (relative to project root)
const PROJECT_ROOT = resolve(__dirname, '../../..');
const MODEL_DATA = resolve(PROJECT_ROOT, 'data/processed/2020_boundaries/model_table_2020.csv');
const PLACES_DATA = resolve(PROJECT_ROOT, 'data/raw/places_2024/places_tract_2024.csv');

interface ModelRow {
	TractFIPS: string;
	StateAbbr: string;
	CountyName: string;
	burden: string;
	resilience_score: string;
}

interface PlacesPopRow {
	LocationID: string;
	TotalPopulation: string;
}

async function loadCSV<T>(filePath: string): Promise<T[]> {
	return new Promise((resolve, reject) => {
		const records: T[] = [];
		createReadStream(filePath)
			.pipe(parse({ columns: true, skip_empty_lines: true }))
			.on('data', (row: T) => records.push(row))
			.on('end', () => resolve(records))
			.on('error', reject);
	});
}

async function loadPopulationFromPlaces(): Promise<Map<string, number>> {
	console.log('   Loading population from PLACES 2024...');
	const popMap = new Map<string, number>();
	let mismatchCount = 0;

	return new Promise((resolve, reject) => {
		let count = 0;
		createReadStream(PLACES_DATA)
			.pipe(parse({ columns: true, skip_empty_lines: true }))
			.on('data', (row: Record<string, string>) => {
				count++;
				const tractFips = row['LocationID']?.padStart(11, '0');
				const pop = parseInt(row['TotalPopulation']) || 0;
				if (tractFips && pop > 0) {
					const existing = popMap.get(tractFips);
					if (!existing) {
						popMap.set(tractFips, pop);
					} else if (existing !== pop) {
						mismatchCount++;
						// Keep first value for consistency
					}
				}
				if (count % 500000 === 0) {
					process.stdout.write(`\r   Processed ${(count / 1000000).toFixed(1)}M PLACES rows...`);
				}
			})
			.on('end', () => {
				console.log(`\r   Loaded population for ${popMap.size.toLocaleString()} tracts from PLACES`);
				if (mismatchCount > 0) {
					console.log(`   Warning: ${mismatchCount} tracts had population mismatches (kept first value)`);
				}
				resolve(popMap);
			})
			.on('error', reject);
	});
}

async function importData() {
	console.log('='.repeat(60));
	console.log('Importing Resilience Data (2020 Census Boundaries)');
	console.log('='.repeat(60));

	// Validate input files
	console.log('\n0. Validating input files...');
	for (const [name, path] of [['MODEL_DATA', MODEL_DATA], ['PLACES_DATA', PLACES_DATA]]) {
		if (!existsSync(path)) {
			throw new Error(`Required file not found: ${name} at ${path}`);
		}
		const stat = statSync(path);
		if (stat.size === 0) {
			throw new Error(`Required file is empty: ${name} at ${path}`);
		}
		console.log(`   ${name}: ${(stat.size / 1024 / 1024).toFixed(1)}MB`);
	}

	// Load CSV files
	console.log('\n1. Loading data files...');
	console.log(`   Model data: ${MODEL_DATA}`);
	const modelData = await loadCSV<ModelRow>(MODEL_DATA);
	console.log(`   Loaded ${modelData.length.toLocaleString()} model records`);

	const popMap = await loadPopulationFromPlaces();

	// Clear existing data
	console.log('\n2. Clearing existing tract data...');
	await sql`DELETE FROM communities`;
	await sql`DELETE FROM tracts`;
	console.log('   Done');

	// Insert in batches
	console.log('\n3. Inserting tract data...');
	const BATCH_SIZE = 1000;
	let inserted = 0;
	let skipped = 0;
	let noPopCount = 0;

	for (let i = 0; i < modelData.length; i += BATCH_SIZE) {
		const batch = modelData.slice(i, i + BATCH_SIZE);
		const values = batch.map((row) => {
			const tractFips = row.TractFIPS.padStart(11, '0');
			const pop = popMap.get(tractFips) || 0;
			if (pop === 0) noPopCount++;

			return {
				tract_fips: tractFips,
				state_abbr: row.StateAbbr || null,
				county: row.CountyName || null,
				total_pop: pop,
				resilience_score: parseFloat(row.resilience_score) || 0,
				burden: parseFloat(row.burden) || 0,
				gq_college_pct: 0, // Not using GQ data in this version
				gq_military_pct: 0,
				gq_correctional_pct: 0,
				gq_nursing_pct: 0,
			};
		});

		try {
			await sql`
				INSERT INTO tracts ${sql(values, 'tract_fips', 'state_abbr', 'county', 'total_pop', 'resilience_score', 'burden', 'gq_college_pct', 'gq_military_pct', 'gq_correctional_pct', 'gq_nursing_pct')}
				ON CONFLICT (tract_fips) DO UPDATE SET
					resilience_score = EXCLUDED.resilience_score,
					burden = EXCLUDED.burden,
					total_pop = EXCLUDED.total_pop,
					county = EXCLUDED.county
			`;
			inserted += batch.length;
		} catch (e) {
			const error = e as Error;
			const errorMsg = error.message || '';

			// Check for fatal errors that should abort the import
			if (
				errorMsg.includes('violates check constraint') ||
				errorMsg.includes('invalid input syntax') ||
				errorMsg.includes('column') && errorMsg.includes('does not exist')
			) {
				console.error(`\n   FATAL: Database constraint error in batch ${i}:`, errorMsg);
				throw error;
			}

			// For transient errors, retry with individual inserts
			console.warn(`\n   Warning: Batch ${i} failed, retrying individual inserts...`);
			console.warn(`   Error was: ${errorMsg.slice(0, 100)}`);

			for (const row of values) {
				try {
					await sql`
						INSERT INTO tracts ${sql([row], 'tract_fips', 'state_abbr', 'county', 'total_pop', 'resilience_score', 'burden', 'gq_college_pct', 'gq_military_pct', 'gq_correctional_pct', 'gq_nursing_pct')}
						ON CONFLICT (tract_fips) DO UPDATE SET
							resilience_score = EXCLUDED.resilience_score,
							burden = EXCLUDED.burden,
							total_pop = EXCLUDED.total_pop,
							county = EXCLUDED.county
					`;
					inserted++;
				} catch (rowError) {
					console.error(`   Failed to insert tract ${row.tract_fips}:`, (rowError as Error).message);
					skipped++;
				}
			}
		}

		// Progress
		if ((i + BATCH_SIZE) % 10000 === 0 || i + BATCH_SIZE >= modelData.length) {
			process.stdout.write(`\r   Progress: ${Math.min(i + BATCH_SIZE, modelData.length).toLocaleString()}/${modelData.length.toLocaleString()}`);
		}
	}
	console.log(`\n   Inserted: ${inserted.toLocaleString()}, Skipped: ${skipped.toLocaleString()}`);
	console.log(`   Tracts without population data: ${noPopCount.toLocaleString()}`);

	// Verify
	console.log('\n4. Verifying import...');
	const [count] = await sql`SELECT COUNT(*) as count FROM tracts`;
	const [popStats] = await sql`SELECT COUNT(*) as with_pop FROM tracts WHERE total_pop > 0`;
	const [topTract] = await sql`
		SELECT tract_fips, state_abbr, county, resilience_score, total_pop
		FROM tracts
		WHERE total_pop > 100
		ORDER BY resilience_score DESC
		LIMIT 1
	`;

	console.log(`   Total tracts: ${parseInt(count.count).toLocaleString()}`);
	console.log(`   Tracts with population: ${parseInt(popStats.with_pop).toLocaleString()}`);
	console.log(`   Top tract: ${topTract.tract_fips} (${topTract.county}, ${topTract.state_abbr})`);
	console.log(`     Score: ${parseFloat(topTract.resilience_score).toFixed(3)}, Pop: ${topTract.total_pop.toLocaleString()}`);

	// State coverage
	console.log('\n5. State coverage:');
	const stateStats = await sql`
		SELECT state_abbr, COUNT(*) as tract_count, AVG(resilience_score) as avg_score
		FROM tracts
		GROUP BY state_abbr
		ORDER BY state_abbr
	`;
	for (const state of stateStats) {
		console.log(`   ${state.state_abbr}: ${parseInt(state.tract_count).toLocaleString()} tracts, avg ${parseFloat(state.avg_score).toFixed(3)}`);
	}

	// Check for Florida specifically
	const [fl] = await sql`SELECT COUNT(*) as count FROM tracts WHERE state_abbr = 'FL'`;
	console.log(`\n   Florida tracts: ${parseInt(fl.count).toLocaleString()}`);

	console.log('\n' + '='.repeat(60));
	console.log('Import complete!');
	console.log('='.repeat(60));

	await sql.end();
}

importData().catch((e) => {
	console.error('Import failed:', e);
	process.exit(1);
});
