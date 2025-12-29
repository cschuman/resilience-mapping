/**
 * Download PLACES 2023 Data for Kentucky and Pennsylvania
 *
 * These states are missing health outcome data in PLACES 2024/2025 due to
 * BRFSS data collection issues in 2023. PLACES 2023 (using BRFSS 2021) has
 * complete data for these states.
 *
 * Run with: npx tsx scripts/download-places-2023-ky-pa.ts
 */

import { writeFileSync, existsSync, mkdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = resolve(__dirname, '../../..');

const OUTPUT_DIR = resolve(PROJECT_ROOT, 'data/raw/places_2023');
const OUTPUT_FILE = resolve(OUTPUT_DIR, 'places_tract_2023_ky_pa.csv');

// Health outcomes we need
const MEASURES = ['OBESITY', 'DIABETES', 'BPHIGH', 'CHD', 'LPA'];

// PLACES 2023 Census Tract API endpoint
const API_BASE = 'https://data.cdc.gov/resource/em5e-5hvn.json';

interface PlacesRecord {
	year: string;
	stateabbr: string;
	statedesc: string;
	locationname: string;
	datasource: string;
	category: string;
	measure: string;
	data_value_type: string;
	data_value: string;
	data_value_unit: string;
	low_confidence_limit: string;
	high_confidence_limit: string;
	totalpopulation: string;
	locationid: string;
	categoryid: string;
	measureid: string;
	datavaluetypeid: string;
	short_question_text: string;
	geolocation?: { latitude: string; longitude: string };
}

async function fetchPlacesData(state: string): Promise<PlacesRecord[]> {
	console.log(`Fetching PLACES 2023 data for ${state}...`);

	const allRecords: PlacesRecord[] = [];
	const limit = 50000;
	let offset = 0;

	while (true) {
		// Build query for health outcomes in this state
		const measureFilter = MEASURES.map((m) => `measureid='${m}'`).join(' OR ');
		const query = `$where=stateabbr='${state}' AND (${measureFilter}) AND data_value_type='Crude prevalence'&$limit=${limit}&$offset=${offset}`;

		const url = `${API_BASE}?${query}`;
		console.log(`   Fetching offset ${offset}...`);

		const response = await fetch(url);
		if (!response.ok) {
			throw new Error(`API error: ${response.status} ${response.statusText}`);
		}

		const records = (await response.json()) as PlacesRecord[];
		if (records.length === 0) break;

		allRecords.push(...records);
		offset += limit;

		// If we got fewer than the limit, we're done
		if (records.length < limit) break;
	}

	console.log(`   Retrieved ${allRecords.length} records for ${state}`);
	return allRecords;
}

function convertToCsv(records: PlacesRecord[]): string {
	// Match the format of our existing PLACES 2024 file
	const headers = [
		'Year',
		'StateAbbr',
		'StateDesc',
		'LocationName',
		'DataSource',
		'Category',
		'Measure',
		'Data_Value_Type',
		'Data_Value',
		'Data_Value_Unit',
		'Low_Confidence_Limit',
		'High_Confidence_Limit',
		'TotalPopulation',
		'LocationID',
		'CategoryID',
		'MeasureId',
		'DataValueTypeID',
		'Short_Question_Text',
		'Geolocation',
	];

	const rows = records.map((r) => {
		const geo = r.geolocation ? `POINT (${r.geolocation.longitude} ${r.geolocation.latitude})` : '';
		return [
			r.year || '2023',
			r.stateabbr || '',
			r.statedesc || '',
			r.locationname || '',
			r.datasource || '',
			r.category || '',
			r.measure || '',
			r.data_value_type || '',
			r.data_value || '',
			r.data_value_unit || '',
			r.low_confidence_limit || '',
			r.high_confidence_limit || '',
			r.totalpopulation || '',
			r.locationid || '',
			r.categoryid || '',
			r.measureid || '',
			r.datavaluetypeid || '',
			r.short_question_text || '',
			geo,
		]
			.map((v) => {
				// Escape values with commas or quotes
				if (v.includes(',') || v.includes('"') || v.includes('\n')) {
					return `"${v.replace(/"/g, '""')}"`;
				}
				return v;
			})
			.join(',');
	});

	return [headers.join(','), ...rows].join('\n');
}

async function main(): Promise<void> {
	console.log('='.repeat(60));
	console.log('Downloading PLACES 2023 Data for Kentucky and Pennsylvania');
	console.log('='.repeat(60));
	console.log('\nThese states are missing health outcome data in PLACES 2024/2025');
	console.log('due to BRFSS data collection issues. Using PLACES 2023 (BRFSS 2021).');
	console.log('');

	// Create output directory
	mkdirSync(OUTPUT_DIR, { recursive: true });

	// Fetch data for both states
	const kyRecords = await fetchPlacesData('KY');
	const paRecords = await fetchPlacesData('PA');

	const allRecords = [...kyRecords, ...paRecords];
	console.log(`\nTotal records: ${allRecords.length}`);

	// Count unique tracts
	const tracts = new Set(allRecords.map((r) => r.locationid));
	console.log(`Unique tracts: ${tracts.size}`);

	// Count by measure
	const measureCounts = new Map<string, number>();
	for (const r of allRecords) {
		const count = measureCounts.get(r.measureid) || 0;
		measureCounts.set(r.measureid, count + 1);
	}
	console.log('\nRecords by measure:');
	for (const [measure, count] of measureCounts) {
		console.log(`   ${measure}: ${count}`);
	}

	// Convert to CSV and save
	const csv = convertToCsv(allRecords);
	writeFileSync(OUTPUT_FILE, csv);
	console.log(`\nSaved to: ${OUTPUT_FILE}`);
	console.log(`File size: ${(csv.length / 1024 / 1024).toFixed(2)} MB`);

	console.log('\n' + '='.repeat(60));
	console.log('Download complete!');
	console.log('='.repeat(60));
	console.log('\nNext step: Run the merge script to combine with PLACES 2024 data');
}

main().catch((error) => {
	console.error('Error:', error);
	process.exit(1);
});
