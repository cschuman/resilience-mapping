/**
 * Vector Tile Generation Pipeline
 *
 * Merges tract geometries with resilience scores and generates PMTiles.
 *
 * Prerequisites:
 *   brew install tippecanoe
 *   npm install -g pmtiles
 *
 * Usage: npx tsx scripts/generate-tiles.ts
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { parse } from 'csv-parse/sync';
import { execFileSync } from 'child_process';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = resolve(__dirname, '../../..');
const WEB_ROOT = resolve(__dirname, '..');

// File paths - Using 2023 boundaries for Connecticut Planning Regions compatibility
// Note: CDC PLACES 2024 uses CT Planning Region codes (09110-09190) which only exist in 2022+ boundaries
const RESILIENCE_CSV = resolve(PROJECT_ROOT, 'data/processed/2020_boundaries/model_table_2020.csv');
const TRACTS_GEOJSON = resolve(PROJECT_ROOT, 'data/input/tracts_2023.geojson');
const ENRICHED_GEOJSON = resolve(PROJECT_ROOT, 'data/processed/2020_boundaries/tracts_enriched_2023.geojson');
const MBTILES_OUTPUT = resolve(PROJECT_ROOT, 'data/processed/2020_boundaries/tracts_2023.mbtiles');
const PMTILES_OUTPUT = resolve(WEB_ROOT, 'static/tiles/tracts.pmtiles');

// Score category thresholds
type ScoreCategory = 'very-high' | 'high' | 'medium' | 'low' | 'very-low' | 'no-data';

function getScoreCategory(score: number | null): ScoreCategory {
	if (score === null || isNaN(score)) return 'no-data';
	if (score >= 2.0) return 'very-high';
	if (score >= 1.0) return 'high';
	if (score >= 0.0) return 'medium';
	if (score >= -1.0) return 'low';
	return 'very-low';
}

interface ResilienceRecord {
	TractFIPS: string;
	StateAbbr: string;
	burden: string;
	resilience_score: string;
}

interface GeoJSONFeature {
	type: 'Feature';
	properties: Record<string, unknown>;
	geometry: unknown;
}

interface GeoJSONCollection {
	type: 'FeatureCollection';
	features: GeoJSONFeature[];
}

/**
 * Safely execute a command using execFileSync (no shell injection risk)
 */
function safeExec(command: string, args: string[], options?: { stdio?: 'inherit' | 'pipe' }): string {
	try {
		const result = execFileSync(command, args, {
			stdio: options?.stdio ?? 'pipe',
			encoding: 'utf-8',
			maxBuffer: 50 * 1024 * 1024 // 50MB buffer for large outputs
		});
		return typeof result === 'string' ? result : '';
	} catch (error) {
		if (error instanceof Error && 'stdout' in error) {
			return (error as { stdout: string }).stdout || '';
		}
		throw error;
	}
}

/**
 * Check if a command exists in PATH
 */
function commandExists(command: string): boolean {
	try {
		execFileSync('which', [command], { stdio: 'pipe' });
		return true;
	} catch {
		return false;
	}
}

async function generateTiles(): Promise<void> {
	console.log('='.repeat(60));
	console.log('Vector Tile Generation Pipeline');
	console.log('='.repeat(60));

	// Verify prerequisites
	console.log('\n1. Checking prerequisites...');

	if (!commandExists('tippecanoe')) {
		console.error('   ✗ tippecanoe not found. Install with: brew install tippecanoe');
		process.exit(1);
	}
	console.log('   ✓ tippecanoe found');

	if (!commandExists('pmtiles')) {
		console.error('   ✗ pmtiles CLI not found. Install with: npm install -g pmtiles');
		process.exit(1);
	}
	console.log('   ✓ pmtiles found');

	if (!existsSync(RESILIENCE_CSV)) {
		console.error(`   ✗ Resilience CSV not found: ${RESILIENCE_CSV}`);
		process.exit(1);
	}
	console.log('   ✓ Resilience CSV found');

	if (!existsSync(TRACTS_GEOJSON)) {
		console.error(`   ✗ Tracts GeoJSON not found: ${TRACTS_GEOJSON}`);
		process.exit(1);
	}
	console.log('   ✓ Tracts GeoJSON found');

	// Load resilience scores
	console.log('\n2. Loading resilience scores...');
	const csvContent = readFileSync(RESILIENCE_CSV, 'utf-8');
	const records: ResilienceRecord[] = parse(csvContent, {
		columns: true,
		skip_empty_lines: true
	});

	// Build lookup map with zero-padded FIPS codes
	const scoreMap = new Map<
		string,
		{
			score: number;
			burden: number;
			state: string;
			county: string;
			category: ScoreCategory;
		}
	>();

	for (const row of records) {
		// Ensure FIPS is 11 characters (zero-padded)
		const fips = row.TractFIPS.padStart(11, '0');
		const score = parseFloat(row.resilience_score);
		const burden = parseFloat(row.burden);

		scoreMap.set(fips, {
			score: isNaN(score) ? 0 : score,
			burden: isNaN(burden) ? 0 : burden,
			state: row.StateAbbr || '',
			county: row.CountyName || '',
			category: getScoreCategory(isNaN(score) ? null : score)
		});
	}
	console.log(`   Loaded ${scoreMap.size.toLocaleString()} resilience scores`);

	// Load and enrich GeoJSON
	console.log('\n3. Loading and enriching GeoJSON (this may take a moment)...');
	const startLoad = Date.now();

	const geojsonContent = readFileSync(TRACTS_GEOJSON, 'utf-8');
	const geojson: GeoJSONCollection = JSON.parse(geojsonContent);

	console.log(`   Loaded ${geojson.features.length.toLocaleString()} features in ${Date.now() - startLoad}ms`);

	let matched = 0;
	let unmatched = 0;
	const unmatchedStates = new Map<string, number>();

	for (const feature of geojson.features) {
		const geoid = feature.properties.GEOID as string;

		if (!geoid) {
			unmatched++;
			continue;
		}

		const data = scoreMap.get(geoid);

		if (data) {
			// Add resilience data to feature properties
			feature.properties.resilience_score = data.score;
			feature.properties.burden = data.burden;
			feature.properties.state_abbr = data.state;
			feature.properties.county_name = data.county;
			feature.properties.score_category = data.category;
			matched++;
		} else {
			// Mark as no data
			feature.properties.resilience_score = null;
			feature.properties.burden = null;
			feature.properties.state_abbr = feature.properties.STATEFP || null;
			feature.properties.county_name = null;
			feature.properties.score_category = 'no-data';
			unmatched++;

			// Track unmatched by state for debugging
			const state = (feature.properties.STATEFP as string) || 'unknown';
			unmatchedStates.set(state, (unmatchedStates.get(state) || 0) + 1);
		}

		// Remove unnecessary properties to reduce file size
		delete feature.properties.ALAND;
		delete feature.properties.AWATER;
		delete feature.properties.INTPTLAT;
		delete feature.properties.INTPTLON;
	}

	console.log(`   Matched: ${matched.toLocaleString()}`);
	console.log(`   Unmatched: ${unmatched.toLocaleString()}`);

	if (unmatched > 0) {
		console.log('   Top unmatched states:');
		const sortedStates = [...unmatchedStates.entries()]
			.sort((a, b) => b[1] - a[1])
			.slice(0, 5);
		for (const [state, count] of sortedStates) {
			console.log(`     STATEFP ${state}: ${count}`);
		}
	}

	// Write enriched GeoJSON
	console.log('\n4. Writing enriched GeoJSON...');
	const startWrite = Date.now();
	writeFileSync(ENRICHED_GEOJSON, JSON.stringify(geojson));
	console.log(`   Written to ${ENRICHED_GEOJSON}`);
	console.log(`   File size: ${(readFileSync(ENRICHED_GEOJSON).length / 1024 / 1024).toFixed(1)} MB`);
	console.log(`   Write time: ${Date.now() - startWrite}ms`);

	// Generate vector tiles with tippecanoe
	console.log('\n5. Generating vector tiles with tippecanoe...');
	console.log('   This may take several minutes for 70K+ features...');

	const tippecanoeArgs = [
		'-o', MBTILES_OUTPUT,
		'-z', '12', // Max zoom 12 (neighborhood level)
		'-Z', '3', // Min zoom 3 (continental view)
		'--drop-densest-as-needed', // Reduce features at low zoom
		'--extend-zooms-if-still-dropping', // Ensure all features at max zoom
		'--coalesce-smallest-as-needed', // Combine small features at low zoom
		'-l', 'tracts', // Layer name
		'--force', // Overwrite existing
		'--no-feature-limit', // Don't limit features per tile
		'--no-tile-size-limit', // Allow larger tiles if needed
		ENRICHED_GEOJSON
	];

	console.log(`   Command: tippecanoe ${tippecanoeArgs.join(' ')}`);
	const startTippecanoe = Date.now();

	try {
		execFileSync('tippecanoe', tippecanoeArgs, { stdio: 'inherit' });
		console.log(`   ✓ MBTiles generated in ${((Date.now() - startTippecanoe) / 1000).toFixed(1)}s`);
		console.log(`   File size: ${(readFileSync(MBTILES_OUTPUT).length / 1024 / 1024).toFixed(1)} MB`);
	} catch (error) {
		console.error('   ✗ tippecanoe failed:', error);
		process.exit(1);
	}

	// Convert to PMTiles
	console.log('\n6. Converting to PMTiles...');

	// Ensure output directory exists
	const tilesDir = dirname(PMTILES_OUTPUT);
	if (!existsSync(tilesDir)) {
		mkdirSync(tilesDir, { recursive: true });
	}

	const pmtilesArgs = ['convert', MBTILES_OUTPUT, PMTILES_OUTPUT];
	console.log(`   Command: pmtiles ${pmtilesArgs.join(' ')}`);

	try {
		execFileSync('pmtiles', pmtilesArgs, { stdio: 'inherit' });
		console.log('   ✓ PMTiles generated');
		console.log(`   File size: ${(readFileSync(PMTILES_OUTPUT).length / 1024 / 1024).toFixed(1)} MB`);
		console.log(`   Output: ${PMTILES_OUTPUT}`);
	} catch (error) {
		console.error('   ✗ PMTiles conversion failed:', error);
		process.exit(1);
	}

	// Summary
	console.log('\n' + '='.repeat(60));
	console.log('✓ Tile generation complete!');
	console.log('='.repeat(60));
	console.log(`\nOutput file: ${PMTILES_OUTPUT}`);
	console.log('\nScore category distribution:');

	const categoryCount = new Map<ScoreCategory, number>();
	for (const feature of geojson.features) {
		const cat = feature.properties.score_category as ScoreCategory;
		categoryCount.set(cat, (categoryCount.get(cat) || 0) + 1);
	}

	for (const [category, count] of categoryCount) {
		const pct = ((count / geojson.features.length) * 100).toFixed(1);
		console.log(`  ${category.padEnd(10)}: ${count.toLocaleString().padStart(8)} (${pct}%)`);
	}
}

generateTiles().catch((error) => {
	console.error('\nFatal error:', error);
	process.exit(1);
});
