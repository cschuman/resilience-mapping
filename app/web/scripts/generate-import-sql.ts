/**
 * Generate SQL import statements for production database
 *
 * This script generates SQL that can be piped to `fly postgres connect`
 *
 * Run with: npx tsx scripts/generate-import-sql.ts > /tmp/import.sql
 * Then: cat /tmp/import.sql | fly postgres connect -a resilience-mapping-db -d resilience_mapping
 *
 * Output Format:
 * - String values: PostgreSQL-escaped with proper quote handling
 * - Numeric values: Validated to prevent NaN/Infinity in SQL output
 * - Population: Integer from PLACES data (first occurrence per tract)
 * - Resilience/Burden scores: 6 decimal precision
 */

import { createReadStream, statSync } from 'fs';
import { parse } from 'csv-parse';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
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
	const popMap = new Map<string, number>();
	let mismatchCount = 0;

	return new Promise((resolve, reject) => {
		createReadStream(PLACES_DATA)
			.pipe(parse({ columns: true, skip_empty_lines: true }))
			.on('data', (row: Record<string, string>) => {
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
			})
			.on('end', () => {
				if (mismatchCount > 0) {
					console.error(`-- Warning: ${mismatchCount} tracts had population mismatches (kept first value)`);
				}
				resolve(popMap);
			})
			.on('error', reject);
	});
}

/**
 * Escape a string for PostgreSQL literal value
 * Handles: single quotes, backslashes, and null/empty values
 */
function escapeString(str: string): string {
	if (!str) return 'NULL';
	// PostgreSQL standard: escape backslashes and single quotes
	return `'${str.replace(/\\/g, '\\\\').replace(/'/g, "''")}'`;
}

/**
 * Validate and return a numeric value for SQL insertion
 * Throws if value is NaN or Infinity to prevent malformed SQL
 */
function validateNumber(val: string, fieldName: string, tractId: string): number {
	const num = parseFloat(val);
	if (isNaN(num) || !isFinite(num)) {
		throw new Error(`Invalid ${fieldName} value for tract ${tractId}: "${val}"`);
	}
	return num;
}

async function generateSQL() {
	// Validate input files exist and have content
	for (const [name, path] of [['MODEL_DATA', MODEL_DATA], ['PLACES_DATA', PLACES_DATA]]) {
		try {
			const stat = statSync(path);
			if (stat.size === 0) {
				throw new Error(`${name} file is empty: ${path}`);
			}
			console.error(`-- ${name}: ${(stat.size / 1024 / 1024).toFixed(1)}MB`);
		} catch (e) {
			if ((e as NodeJS.ErrnoException).code === 'ENOENT') {
				throw new Error(`${name} file not found: ${path}`);
			}
			throw e;
		}
	}

	// Load data
	const modelData = await loadCSV<ModelRow>(MODEL_DATA);
	const popMap = await loadPopulationFromPlaces();

	console.error(`-- Loaded ${modelData.length} model rows, ${popMap.size} population entries`);

	// Output SQL
	console.log('-- =============================================================================');
	console.log('-- Import script for resilience data (2020 Census boundaries)');
	console.log('-- Generated: ' + new Date().toISOString());
	console.log('-- Total tracts: ' + modelData.length);
	console.log('-- =============================================================================');
	console.log('--');
	console.log('-- IMPORTANT: This script runs in a transaction. If any error occurs:');
	console.log('--   1. The entire import will be rolled back automatically');
	console.log('--   2. No data will be modified');
	console.log('--   3. Fix the issue and re-run the script');
	console.log('--');
	console.log('-- To manually rollback if the connection drops mid-import:');
	console.log('--   ROLLBACK;');
	console.log('--');
	console.log('');
	console.log('BEGIN;');
	console.log('');
	console.log('-- Step 1: Clear existing data');
	console.log('DELETE FROM communities;');
	console.log('DELETE FROM tracts;');
	console.log('');
	console.log('-- Step 2: Insert tracts (in batches for visibility)');

	const BATCH_SIZE = 500;
	let batchNum = 0;
	for (let i = 0; i < modelData.length; i += BATCH_SIZE) {
		batchNum++;
		const batch = modelData.slice(i, i + BATCH_SIZE);

		console.log(`-- Batch ${batchNum} (rows ${i + 1}-${Math.min(i + BATCH_SIZE, modelData.length)})`);
		console.log(`INSERT INTO tracts (tract_fips, state_abbr, county, total_pop, resilience_score, burden, gq_college_pct, gq_military_pct, gq_correctional_pct, gq_nursing_pct) VALUES`);

		const values = batch.map((row, idx) => {
			const tractFips = row.TractFIPS.padStart(11, '0');
			const pop = popMap.get(tractFips) || 0;
			const comma = idx < batch.length - 1 ? ',' : ';';

			// Validate numeric values to prevent malformed SQL
			const resilience = validateNumber(row.resilience_score, 'resilience_score', tractFips);
			const burden = validateNumber(row.burden, 'burden', tractFips);

			return `  (${escapeString(tractFips)}, ${escapeString(row.StateAbbr)}, ${escapeString(row.CountyName)}, ${pop}, ${resilience}, ${burden}, 0, 0, 0, 0)${comma}`;
		});

		values.forEach((v) => console.log(v));
		console.log('');
	}

	console.log('-- Step 3: Verify import before committing');
	console.log("SELECT 'Pre-commit verification:' as status;");
	console.log("SELECT COUNT(*) as total_tracts, COUNT(CASE WHEN state_abbr = 'FL' THEN 1 END) as florida_tracts FROM tracts;");
	console.log('');
	console.log('COMMIT;');
	console.log('');
	console.log('-- Import complete! Final verification:');
	console.log("SELECT COUNT(*) as total_tracts, COUNT(CASE WHEN state_abbr = 'FL' THEN 1 END) as florida_tracts FROM tracts;");
}

generateSQL().catch((e) => {
	console.error('Error:', e);
	process.exit(1);
});
