/**
 * Import Resilience Data to Postgres
 *
 * Run with: npx tsx scripts/import-data.ts
 *
 * Requires DATABASE_URL environment variable
 */

import postgres from 'postgres';
import { createReadStream } from 'fs';
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
});

// Path to the data files (relative to project root)
const PROJECT_ROOT = resolve(__dirname, '../../..');
const MODEL_DATA = resolve(PROJECT_ROOT, 'data/processed/model_table_corrected.csv');
const GQ_DATA = resolve(PROJECT_ROOT, 'data/input/census_gq_by_type_2020.csv');

interface ModelRow {
	TractFIPS: string;
	StateAbbr: string;
	burden: string;
	resilience_score: string;
}

interface GQRow {
	TractFIPS: string;
	total_pop: string;
	pct_gq_college: string;
	pct_gq_military: string;
	pct_gq_correctional: string;
	pct_gq_nursing: string;
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

async function importData() {
	console.log('Importing resilience data...\n');

	// Load CSV files
	console.log('1. Loading CSV files...');
	console.log(`   Model data: ${MODEL_DATA}`);
	const modelData = await loadCSV<ModelRow>(MODEL_DATA);
	console.log(`   Loaded ${modelData.length.toLocaleString()} model records`);

	console.log(`   GQ data: ${GQ_DATA}`);
	const gqData = await loadCSV<GQRow>(GQ_DATA);
	console.log(`   Loaded ${gqData.length.toLocaleString()} GQ records`);

	// Create lookup map for GQ data
	const gqMap = new Map<string, GQRow>();
	for (const row of gqData) {
		gqMap.set(row.TractFIPS.padStart(11, '0'), row);
	}

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

	for (let i = 0; i < modelData.length; i += BATCH_SIZE) {
		const batch = modelData.slice(i, i + BATCH_SIZE);
		const values = batch.map((row) => {
			const tractFips = row.TractFIPS.padStart(11, '0');
			const gq = gqMap.get(tractFips);

			return {
				tract_fips: tractFips,
				state_abbr: row.StateAbbr || null,
				county: null, // Would need to join from another source
				total_pop: gq ? parseInt(gq.total_pop) || 0 : 0,
				resilience_score: parseFloat(row.resilience_score) || 0,
				burden: parseFloat(row.burden) || 0,
				gq_college_pct: gq ? parseFloat(gq.pct_gq_college) || 0 : 0,
				gq_military_pct: gq ? parseFloat(gq.pct_gq_military) || 0 : 0,
				gq_correctional_pct: gq ? parseFloat(gq.pct_gq_correctional) || 0 : 0,
				gq_nursing_pct: gq ? parseFloat(gq.pct_gq_nursing) || 0 : 0,
			};
		});

		try {
			await sql`
				INSERT INTO tracts ${sql(values, 'tract_fips', 'state_abbr', 'county', 'total_pop', 'resilience_score', 'burden', 'gq_college_pct', 'gq_military_pct', 'gq_correctional_pct', 'gq_nursing_pct')}
				ON CONFLICT (tract_fips) DO UPDATE SET
					resilience_score = EXCLUDED.resilience_score,
					burden = EXCLUDED.burden,
					total_pop = EXCLUDED.total_pop
			`;
			inserted += batch.length;
		} catch (e) {
			console.error(`   Error in batch starting at ${i}:`, (e as Error).message);
			skipped += batch.length;
		}

		// Progress
		if ((i + BATCH_SIZE) % 10000 === 0 || i + BATCH_SIZE >= modelData.length) {
			process.stdout.write(`\r   Progress: ${Math.min(i + BATCH_SIZE, modelData.length).toLocaleString()}/${modelData.length.toLocaleString()}`);
		}
	}
	console.log(`\n   Inserted: ${inserted.toLocaleString()}, Skipped: ${skipped.toLocaleString()}`);

	// Verify
	console.log('\n4. Verifying import...');
	const [count] = await sql`SELECT COUNT(*) as count FROM tracts`;
	const [topTract] = await sql`SELECT tract_fips, state_abbr, resilience_score FROM tracts ORDER BY resilience_score DESC LIMIT 1`;

	console.log(`   Total tracts: ${parseInt(count.count).toLocaleString()}`);
	console.log(`   Top tract: ${topTract.tract_fips} (${topTract.state_abbr}) - score: ${parseFloat(topTract.resilience_score).toFixed(3)}`);

	// Stats by state
	console.log('\n5. Top 10 states by average resilience:');
	const stateStats = await sql`
		SELECT state_abbr, COUNT(*) as tract_count, AVG(resilience_score) as avg_score
		FROM tracts
		WHERE resilience_score > 0
		GROUP BY state_abbr
		ORDER BY avg_score DESC
		LIMIT 10
	`;
	for (const state of stateStats) {
		console.log(`   ${state.state_abbr}: ${parseInt(state.tract_count).toLocaleString()} tracts, avg ${parseFloat(state.avg_score).toFixed(3)}`);
	}

	console.log('\n========================================');
	console.log('Import complete!');
	console.log('========================================');

	await sql.end();
}

importData().catch((e) => {
	console.error('Import failed:', e);
	process.exit(1);
});
