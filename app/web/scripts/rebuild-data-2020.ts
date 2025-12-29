/**
 * Rebuild Resilience Data with 2020 Census Boundaries
 *
 * This script properly aligns all data sources to 2020 Census tract boundaries:
 * - CDC PLACES 2024 (already uses 2020 boundaries) - for 48 states + DC
 * - CDC PLACES 2023 (for Kentucky and Pennsylvania, which are missing from 2024)
 * - FARA 2019 food access data (crosswalked from 2010 to 2020 using Census relationship file)
 *
 * Note: Kentucky and Pennsylvania are missing from PLACES 2024/2025 because they
 * couldn't collect enough BRFSS data in 2023. PLACES 2023 (using BRFSS 2021) has
 * complete data for these states.
 *
 * Run with: npx tsx scripts/rebuild-data-2020.ts
 *
 * Output Format Precision:
 * - Health outcomes (obesity, diabetes, etc.): 1 decimal place (matches CDC PLACES precision)
 * - LILA/Low-income flags: binary (0 or 1)
 * - Burden score: 6 decimals (full precision for statistical analysis)
 * - Resilience score: 6 decimals (full precision for statistical analysis)
 *
 * Data Quality:
 * - All tracts must have all 5 health outcomes to be included
 * - Zero standard deviation is handled by treating z-score as 0
 * - SHA256 checksum is written for data integrity verification
 */

import { createReadStream, existsSync, writeFileSync, mkdirSync, statSync } from 'fs';
import { createHash } from 'crypto';
import { parse } from 'csv-parse';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = resolve(__dirname, '../../..');

// File paths
const PATHS = {
	// Input files
	placesRaw: resolve(PROJECT_ROOT, 'data/raw/places_2024/places_tract_2024.csv'),
	places2023KyPa: resolve(PROJECT_ROOT, 'data/raw/places_2023/places_tract_2023_ky_pa.csv'),
	faraRaw: resolve(PROJECT_ROOT, 'data/input/fara_2019.csv'),
	crosswalk: resolve(PROJECT_ROOT, 'data/raw/crosswalks/tab20_tract20_tract10_natl.txt'),

	// Output files
	outputDir: resolve(PROJECT_ROOT, 'data/processed/2020_boundaries'),
	placesWide: resolve(PROJECT_ROOT, 'data/processed/2020_boundaries/places_wide_2024.csv'),
	faraCrosswalked: resolve(PROJECT_ROOT, 'data/processed/2020_boundaries/fara_2020_boundaries.csv'),
	modelOutput: resolve(PROJECT_ROOT, 'data/processed/2020_boundaries/model_table_2020.csv'),
};

// States that need PLACES 2023 data (missing from 2024/2025)
const PLACES_2023_STATES = ['KY', 'PA'];

// Health outcomes to extract from PLACES (MeasureId values)
// Note: LPA = Lack of Physical Activity (formerly PHYSINACT)
const HEALTH_OUTCOMES = ['OBESITY', 'DIABETES', 'BPHIGH', 'CHD', 'LPA'];

// FARA columns to crosswalk (weighted by population or land area)
const FARA_POP_COLS = ['Pop2010', 'OHU2010'];
const FARA_BINARY_COLS = ['LILATracts_1And10', 'LILATracts_halfAnd10', 'LILATracts_1And20', 'LILATracts_Vehicle', 'LowIncomeTracts'];
const FARA_PCT_COLS = ['PovertyRate'];

interface CrosswalkRow {
	geoid2020: string;
	geoid2010: string;
	areaLand2020: number;
	areaLand2010: number;
	areaLandPart: number;
	weight: number; // Proportion of 2010 tract going to this 2020 tract
}

interface FaraRow {
	tractFips: string;
	state: string;
	county: string;
	pop2010: number;
	lilaTracts_1And10: number;
	lilaTracts_halfAnd10: number;
	lilaTracts_1And20: number;
	lilaTracts_Vehicle: number;
	lowIncomeTracts: number;
	povertyRate: number;
	[key: string]: string | number;
}

interface PlacesRow {
	tractFips: string;
	stateAbbr: string;
	countyName: string;
	obesity?: number;
	diabetes?: number;
	hypertension?: number;
	chd?: number;
	lpa?: number; // Lack of Physical Activity
}

// ============================================================================
// Step 0: Validate Input Files
// ============================================================================
async function validateInputFiles(): Promise<void> {
	console.log('\n0. Validating input files...');

	const requiredFiles: [string, string][] = [
		['crosswalk', PATHS.crosswalk],
		['faraRaw', PATHS.faraRaw],
		['placesRaw (2024)', PATHS.placesRaw],
		['places2023KyPa', PATHS.places2023KyPa],
	];

	for (const [name, path] of requiredFiles) {
		if (!existsSync(path)) {
			throw new Error(`Required file not found: ${name} at ${path}`);
		}
		const stat = statSync(path);
		if (stat.size === 0) {
			throw new Error(`Required file is empty: ${name} at ${path}`);
		}
		console.log(`   ${name}: ${(stat.size / 1024 / 1024).toFixed(1)}MB`);
	}

	console.log('   All input files validated');
}

// ============================================================================
// Step 1: Build Crosswalk Weights
// ============================================================================
async function buildCrosswalk(): Promise<Map<string, CrosswalkRow[]>> {
	console.log('\n1. Building 2010 to 2020 tract crosswalk...');

	const crosswalk = new Map<string, CrosswalkRow[]>();

	return new Promise((resolve, reject) => {
		const rows: CrosswalkRow[] = [];

		createReadStream(PATHS.crosswalk)
			.pipe(
				parse({
					columns: true,
					skip_empty_lines: true,
					delimiter: '|',
					bom: true,
				})
			)
			.on('data', (row: Record<string, string>) => {
				const geoid2020 = row['GEOID_TRACT_20'];
				const geoid2010 = row['GEOID_TRACT_10'];
				const areaLand2020 = parseInt(row['AREALAND_TRACT_20']) || 0;
				const areaLand2010 = parseInt(row['AREALAND_TRACT_10']) || 0;
				const areaLandPart = parseInt(row['AREALAND_PART']) || 0;

				// Weight is proportion of 2010 tract's land area in this 2020 tract
				const weight = areaLand2010 > 0 ? areaLandPart / areaLand2010 : 0;

				if (geoid2010 && geoid2020) {
					rows.push({
						geoid2020,
						geoid2010,
						areaLand2020,
						areaLand2010,
						areaLandPart,
						weight,
					});
				}
			})
			.on('end', () => {
				// Group by 2010 tract to see how it maps to 2020 tracts
				for (const row of rows) {
					if (!crosswalk.has(row.geoid2010)) {
						crosswalk.set(row.geoid2010, []);
					}
					crosswalk.get(row.geoid2010)!.push(row);
				}

				console.log(`   Loaded ${rows.length} crosswalk relationships`);
				console.log(`   Covering ${crosswalk.size} unique 2010 tracts`);

				// Validate weights sum to ~1 for each 2010 tract
				let invalidWeights = 0;
				for (const [tractId, mappings] of crosswalk) {
					const totalWeight = mappings.reduce((sum, m) => sum + m.weight, 0);
					if (Math.abs(totalWeight - 1.0) > 0.01) {
						invalidWeights++;
					}
				}
				console.log(`   Tracts with weight sum != 1.0: ${invalidWeights}`);

				resolve(crosswalk);
			})
			.on('error', reject);
	});
}

// ============================================================================
// Step 2: Crosswalk FARA Data to 2020 Boundaries
// ============================================================================
async function crosswalkFara(crosswalk: Map<string, CrosswalkRow[]>): Promise<Map<string, FaraRow>> {
	console.log('\n2. Crosswalking FARA data to 2020 boundaries...');

	if (!existsSync(PATHS.faraRaw)) {
		throw new Error(`FARA file not found: ${PATHS.faraRaw}`);
	}

	// First, load all 2010 FARA data
	const fara2010 = new Map<string, Record<string, string>>();

	await new Promise<void>((resolve, reject) => {
		createReadStream(PATHS.faraRaw)
			.pipe(
				parse({
					columns: true,
					skip_empty_lines: true,
				})
			)
			.on('data', (row: Record<string, string>) => {
				const tractFips = row['CensusTract']?.padStart(11, '0');
				if (tractFips) {
					fara2010.set(tractFips, row);
				}
			})
			.on('end', () => {
				console.log(`   Loaded ${fara2010.size} FARA 2010 tracts`);
				resolve();
			})
			.on('error', reject);
	});

	// Now crosswalk to 2020 boundaries
	const fara2020 = new Map<string, FaraRow>();

	// First, initialize all 2020 tracts from the crosswalk
	const tracts2020 = new Set<string>();
	for (const mappings of crosswalk.values()) {
		for (const m of mappings) {
			tracts2020.add(m.geoid2020);
		}
	}

	for (const tractId of tracts2020) {
		fara2020.set(tractId, {
			tractFips: tractId,
			state: '',
			county: '',
			pop2010: 0,
			lilaTracts_1And10: 0,
			lilaTracts_halfAnd10: 0,
			lilaTracts_1And20: 0,
			lilaTracts_Vehicle: 0,
			lowIncomeTracts: 0,
			povertyRate: 0,
		});
	}

	// Crosswalk each 2010 tract to its 2020 counterpart(s)
	let matched = 0;
	let unmatched = 0;

	for (const [tract2010, faraData] of fara2010) {
		const mappings = crosswalk.get(tract2010);

		if (!mappings || mappings.length === 0) {
			unmatched++;
			continue;
		}

		matched++;
		const pop2010 = parseFloat(faraData['Pop2010']) || 0;

		for (const mapping of mappings) {
			const target = fara2020.get(mapping.geoid2020);
			if (!target) continue;

			// Copy state/county from first matching tract
			if (!target.state) {
				target.state = faraData['State'] || '';
				target.county = faraData['County'] || '';
			}

			// Population-weighted values
			target.pop2010 += pop2010 * mapping.weight;

			// For binary indicators (LILA flags), if any source tract is flagged AND
			// its weight is > 50%, mark the target tract
			if (mapping.weight > 0.5) {
				if (faraData['LILATracts_1And10'] === '1') target.lilaTracts_1And10 = 1;
				if (faraData['LILATracts_halfAnd10'] === '1') target.lilaTracts_halfAnd10 = 1;
				if (faraData['LILATracts_1And20'] === '1') target.lilaTracts_1And20 = 1;
				if (faraData['LILATracts_Vehicle'] === '1') target.lilaTracts_Vehicle = 1;
				if (faraData['LowIncomeTracts'] === '1') target.lowIncomeTracts = 1;
			}

			// Weighted average for rates
			const povertyRate = parseFloat(faraData['PovertyRate']) || 0;
			target.povertyRate += povertyRate * mapping.weight;
		}
	}

	console.log(`   Matched: ${matched} tracts`);
	console.log(`   Unmatched (no crosswalk): ${unmatched} tracts`);
	console.log(`   Output: ${fara2020.size} 2020-boundary tracts`);

	return fara2020;
}

// ============================================================================
// Step 3: Pivot PLACES Data to Wide Format
// ============================================================================

// Helper function to process a PLACES CSV file
function processPlacesFile(
	filePath: string,
	placesWide: Map<string, PlacesRow>,
	skipStates: string[] = []
): Promise<{ totalRows: number; relevantRows: number; skippedStates: number }> {
	return new Promise((resolve, reject) => {
		let totalRows = 0;
		let relevantRows = 0;
		let skippedStates = 0;

		createReadStream(filePath)
			.pipe(
				parse({
					columns: true,
					skip_empty_lines: true,
				})
			)
			.on('data', (row: Record<string, string>) => {
				totalRows++;

				const stateAbbr = row['StateAbbr'];
				if (skipStates.includes(stateAbbr)) {
					skippedStates++;
					return;
				}

				const measureId = row['MeasureId'];
				if (!HEALTH_OUTCOMES.includes(measureId)) return;

				relevantRows++;
				const tractFips = row['LocationID']?.padStart(11, '0');
				if (!tractFips) return;

				if (!placesWide.has(tractFips)) {
					placesWide.set(tractFips, {
						tractFips,
						stateAbbr,
						countyName: row['CountyName'],
					});
				}

				const value = parseFloat(row['Data_Value']);
				if (isNaN(value)) return;

				const target = placesWide.get(tractFips)!;

				switch (measureId) {
					case 'OBESITY':
						target.obesity = value;
						break;
					case 'DIABETES':
						target.diabetes = value;
						break;
					case 'BPHIGH':
						target.hypertension = value;
						break;
					case 'CHD':
						target.chd = value;
						break;
					case 'LPA':
						target.lpa = value;
						break;
				}

				// Progress indicator
				if (totalRows % 500000 === 0) {
					process.stdout.write(`\r   Processed ${(totalRows / 1000000).toFixed(1)}M rows...`);
				}
			})
			.on('end', () => {
				resolve({ totalRows, relevantRows, skippedStates });
			})
			.on('error', reject);
	});
}

async function pivotPlaces(): Promise<Map<string, PlacesRow>> {
	console.log('\n3. Pivoting PLACES data to wide format...');
	console.log(`   Using PLACES 2024 for 48 states + DC`);
	console.log(`   Using PLACES 2023 for KY and PA (missing from 2024)`);

	const placesWide = new Map<string, PlacesRow>();

	// Step 3a: Load PLACES 2024 (skip KY and PA)
	console.log('\n   3a. Loading PLACES 2024 (excluding KY, PA)...');
	const result2024 = await processPlacesFile(PATHS.placesRaw, placesWide, PLACES_2023_STATES);
	console.log(`\r   PLACES 2024: ${(result2024.totalRows / 1000000).toFixed(1)}M rows processed`);
	console.log(`   Relevant health outcome rows: ${result2024.relevantRows}`);
	console.log(`   Skipped KY/PA rows: ${result2024.skippedStates}`);
	console.log(`   Tracts loaded: ${placesWide.size}`);

	// Step 3b: Load PLACES 2023 for KY and PA
	console.log('\n   3b. Loading PLACES 2023 (KY and PA only)...');
	const result2023 = await processPlacesFile(PATHS.places2023KyPa, placesWide, []);
	console.log(`   PLACES 2023: ${result2023.totalRows} rows processed`);
	console.log(`   Relevant health outcome rows: ${result2023.relevantRows}`);
	console.log(`   Total tracts after merge: ${placesWide.size}`);

	// Count tracts with complete data
	let complete = 0;
	const stateComplete = new Map<string, number>();
	for (const tract of placesWide.values()) {
		if (
			tract.obesity !== undefined &&
			tract.diabetes !== undefined &&
			tract.hypertension !== undefined &&
			tract.chd !== undefined &&
			tract.lpa !== undefined
		) {
			complete++;
			const count = stateComplete.get(tract.stateAbbr) || 0;
			stateComplete.set(tract.stateAbbr, count + 1);
		}
	}
	console.log(`\n   Tracts with all 5 outcomes: ${complete}`);

	// Report KY and PA counts
	const kyCount = stateComplete.get('KY') || 0;
	const paCount = stateComplete.get('PA') || 0;
	console.log(`   Kentucky tracts (from 2023): ${kyCount}`);
	console.log(`   Pennsylvania tracts (from 2023): ${paCount}`);

	return placesWide;
}

// ============================================================================
// Step 4: Calculate Burden and Resilience Scores
// ============================================================================
interface ModelRow {
	tractFips: string;
	stateAbbr: string;
	countyName: string;
	obesity: number;
	diabetes: number;
	hypertension: number;
	chd: number;
	lpa: number; // Lack of Physical Activity
	lilaFlag: number;
	lowIncomeFlag: number;
	burden: number;
	residual: number;
	resilienceScore: number;
}

function calculateBurdenAndResilience(
	places: Map<string, PlacesRow>,
	fara: Map<string, FaraRow>
): ModelRow[] {
	console.log('\n4. Calculating burden and resilience scores...');

	// Merge PLACES and FARA data
	const merged: ModelRow[] = [];

	for (const [tractFips, place] of places) {
		// Skip tracts missing any health outcome
		if (
			place.obesity === undefined ||
			place.diabetes === undefined ||
			place.hypertension === undefined ||
			place.chd === undefined ||
			place.lpa === undefined
		) {
			continue;
		}

		const faraData = fara.get(tractFips);
		const lilaFlag = faraData?.lilaTracts_1And10 || 0;
		const lowIncomeFlag = faraData?.lowIncomeTracts || 0;

		merged.push({
			tractFips,
			stateAbbr: place.stateAbbr,
			countyName: place.countyName || '',
			obesity: place.obesity,
			diabetes: place.diabetes,
			hypertension: place.hypertension,
			chd: place.chd,
			lpa: place.lpa,
			lilaFlag,
			lowIncomeFlag,
			burden: 0,
			residual: 0,
			resilienceScore: 0,
		});
	}

	console.log(`   Merged ${merged.length} tracts with complete health data`);

	// Calculate means and standard deviations for z-score normalization
	const outcomes = ['obesity', 'diabetes', 'hypertension', 'chd', 'lpa'] as const;
	const stats: Record<string, { mean: number; sd: number }> = {};

	for (const outcome of outcomes) {
		const values = merged.map((r) => r[outcome]);
		const mean = values.reduce((sum, v) => sum + v, 0) / values.length;
		const variance = values.reduce((sum, v) => sum + Math.pow(v - mean, 2), 0) / values.length;
		const sd = Math.sqrt(variance);
		stats[outcome] = { mean, sd };
	}

	// Check for zero standard deviation (all values identical)
	for (const outcome of outcomes) {
		if (stats[outcome].sd === 0) {
			console.warn(`   Warning: ${outcome} has zero standard deviation (all values identical)`);
		}
	}

	// Calculate burden (mean of z-scores)
	// Handle zero SD by treating z-score as 0 (tract is at mean)
	for (const row of merged) {
		let zSum = 0;
		for (const outcome of outcomes) {
			const sd = stats[outcome].sd;
			// If no variance, z-score is 0 (tract is at population mean)
			const z = sd > 0 ? (row[outcome] - stats[outcome].mean) / sd : 0;
			zSum += z;
		}
		row.burden = zSum / outcomes.length;
	}

	// Validate burden scores don't contain invalid values
	const invalidBurdens = merged.filter((r) => !isFinite(r.burden));
	if (invalidBurdens.length > 0) {
		console.error(`   ERROR: ${invalidBurdens.length} tracts have invalid burden scores (NaN or Infinity)`);
		invalidBurdens.slice(0, 5).forEach((r) => {
			console.error(`     Tract ${r.tractFips}: burden = ${r.burden}`);
		});
		throw new Error('Data quality error: invalid burden scores detected');
	}

	console.log('   Calculated burden scores (all values valid)');

	// Calculate expected burden based on LILA status (simple regression)
	// burden = beta0 + beta1 * lila_flag
	const lilaTracts = merged.filter((r) => r.lilaFlag === 1);
	const nonLilaTracts = merged.filter((r) => r.lilaFlag === 0);

	const meanBurdenLila = lilaTracts.length > 0
		? lilaTracts.reduce((sum, r) => sum + r.burden, 0) / lilaTracts.length
		: 0;
	const meanBurdenNonLila = nonLilaTracts.length > 0
		? nonLilaTracts.reduce((sum, r) => sum + r.burden, 0) / nonLilaTracts.length
		: 0;

	console.log(`   Mean burden (LILA): ${meanBurdenLila.toFixed(3)}`);
	console.log(`   Mean burden (non-LILA): ${meanBurdenNonLila.toFixed(3)}`);

	// Simple model: expected_burden = meanBurdenNonLila + (meanBurdenLila - meanBurdenNonLila) * lila_flag
	const beta0 = meanBurdenNonLila;
	const beta1 = meanBurdenLila - meanBurdenNonLila;

	// Calculate residuals and resilience scores
	for (const row of merged) {
		const expectedBurden = beta0 + beta1 * row.lilaFlag;
		row.residual = row.burden - expectedBurden;
		// Resilience = negative residual (doing better than expected = positive resilience)
		row.resilienceScore = -row.residual;
	}

	// Validate scores
	const resilienceScores = merged.map((r) => r.resilienceScore);
	const minScore = Math.min(...resilienceScores);
	const maxScore = Math.max(...resilienceScores);
	const meanScore = resilienceScores.reduce((sum, s) => sum + s, 0) / resilienceScores.length;

	console.log(`   Resilience score range: ${minScore.toFixed(3)} to ${maxScore.toFixed(3)}`);
	console.log(`   Mean resilience score: ${meanScore.toFixed(6)}`);

	return merged;
}

// ============================================================================
// Step 5: Save Output Files
// ============================================================================
async function saveOutput(model: ModelRow[]): Promise<void> {
	console.log('\n5. Saving output files...');

	// Create output directory
	mkdirSync(PATHS.outputDir, { recursive: true });

	// Build CSV content manually
	const header = 'TractFIPS,StateAbbr,CountyName,obesity,diabetes,hypertension,chd,lpa,lila_flag,low_income_flag,burden,resid,resilience_score';

	const rows = model.map((row) => {
		// Escape county name if it contains commas
		const countyName = row.countyName.includes(',') ? `"${row.countyName}"` : row.countyName;
		return [
			row.tractFips,
			row.stateAbbr,
			countyName,
			row.obesity.toFixed(1),
			row.diabetes.toFixed(1),
			row.hypertension.toFixed(1),
			row.chd.toFixed(1),
			row.lpa.toFixed(1),
			row.lilaFlag,
			row.lowIncomeFlag,
			row.burden.toFixed(6),
			row.residual.toFixed(6),
			row.resilienceScore.toFixed(6),
		].join(',');
	});

	const csv = [header, ...rows].join('\n');
	writeFileSync(PATHS.modelOutput, csv);

	// Write SHA256 checksum for data integrity verification
	const hash = createHash('sha256').update(csv).digest('hex');
	const checksumPath = PATHS.modelOutput + '.sha256';
	writeFileSync(checksumPath, `${hash}  model_table_2020.csv\n`);

	console.log(`   Saved model table: ${PATHS.modelOutput}`);
	console.log(`   SHA256 checksum: ${hash}`);
	console.log(`   Checksum file: ${checksumPath}`);
	console.log(`   Total tracts: ${model.length.toLocaleString()}`);
	console.log(`   File size: ${(csv.length / 1024 / 1024).toFixed(2)}MB`);
}

// ============================================================================
// Step 6: Validate State Coverage
// ============================================================================
function validateStateCoverage(model: ModelRow[]): void {
	console.log('\n6. Validating state coverage...');

	const stateCounts = new Map<string, number>();
	for (const row of model) {
		const count = stateCounts.get(row.stateAbbr) || 0;
		stateCounts.set(row.stateAbbr, count + 1);
	}

	// Sort by state abbreviation
	const sorted = [...stateCounts.entries()].sort((a, b) => a[0].localeCompare(b[0]));

	console.log('\n   State tract counts:');
	for (const [state, count] of sorted) {
		console.log(`   ${state}: ${count.toLocaleString()}`);
	}

	console.log(`\n   Total states: ${stateCounts.size}`);
	console.log(`   Total tracts: ${model.length.toLocaleString()}`);

	// Check for Florida specifically
	const flCount = stateCounts.get('FL') || 0;
	if (flCount > 0) {
		console.log(`\n   Florida included: ${flCount.toLocaleString()} tracts`);
	} else {
		console.warn('\n   WARNING: Florida is still missing!');
	}
}

// ============================================================================
// Main
// ============================================================================
async function main(): Promise<void> {
	console.log('='.repeat(60));
	console.log('Rebuilding Resilience Data with 2020 Census Boundaries');
	console.log('='.repeat(60));

	try {
		await validateInputFiles();
		const crosswalk = await buildCrosswalk();
		const fara = await crosswalkFara(crosswalk);
		const places = await pivotPlaces();
		const model = calculateBurdenAndResilience(places, fara);
		await saveOutput(model);
		validateStateCoverage(model);

		console.log('\n' + '='.repeat(60));
		console.log('Rebuild complete!');
		console.log('='.repeat(60));
		console.log(`\nOutput file: ${PATHS.modelOutput}`);
		console.log('\nNext steps:');
		console.log('1. Review state coverage and tract counts');
		console.log('2. Run import script to load data into database');
		console.log('3. Regenerate map tiles');
	} catch (error) {
		console.error('\nError:', error);
		process.exit(1);
	}
}

main();
