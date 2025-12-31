/**
 * Update county names in the tracts table using Census Bureau FIPS codes.
 *
 * Usage: DATABASE_URL="..." npx tsx scripts/update-county-names.ts
 */

import { db } from '../src/lib/server/db';
import { sql } from 'drizzle-orm';

const COUNTY_DATA_URL = 'https://www2.census.gov/geo/docs/reference/codes2020/national_county2020.txt';

interface CountyRecord {
	stateAbbr: string;
	stateFips: string;
	countyFips: string;
	countyName: string;
}

async function fetchCountyData(): Promise<CountyRecord[]> {
	console.log('Fetching county data from Census Bureau...');
	const response = await fetch(COUNTY_DATA_URL);
	const text = await response.text();

	const lines = text.trim().split('\n');
	const records: CountyRecord[] = [];

	// Skip header line
	for (let i = 1; i < lines.length; i++) {
		const parts = lines[i].split('|');
		if (parts.length >= 5) {
			records.push({
				stateAbbr: parts[0],
				stateFips: parts[1],
				countyFips: parts[2],
				countyName: parts[4].replace(' County', '').replace(' Parish', '').replace(' Borough', '').replace(' Census Area', '').replace(' Municipality', '').trim()
			});
		}
	}

	console.log(`Parsed ${records.length} county records`);
	return records;
}

async function updateCountyNames(counties: CountyRecord[]): Promise<void> {
	console.log('Updating county names in database...');

	let updated = 0;
	let errors = 0;

	// Build a map of county FIPS (5 digits) to county name
	const countyMap = new Map<string, string>();
	for (const county of counties) {
		const fips5 = county.stateFips + county.countyFips;
		countyMap.set(fips5, county.countyName);
	}

	console.log(`Built map with ${countyMap.size} county FIPS codes`);

	// Update in batches using CASE WHEN
	const batchSize = 500;
	const entries = Array.from(countyMap.entries());

	for (let i = 0; i < entries.length; i += batchSize) {
		const batch = entries.slice(i, i + batchSize);

		// Build CASE statement
		const whenClauses = batch
			.map(([fips, name]) => `WHEN LEFT(tract_fips, 5) = '${fips}' THEN '${name.replace(/'/g, "''")}'`)
			.join('\n            ');

		const fipsList = batch.map(([fips]) => `'${fips}'`).join(', ');

		const query = `
			UPDATE tracts
			SET county = CASE
				${whenClauses}
				ELSE county
			END
			WHERE LEFT(tract_fips, 5) IN (${fipsList})
		`;

		try {
			const result = await db.execute(sql.raw(query));
			updated += batch.length;
			console.log(`Updated batch ${Math.floor(i / batchSize) + 1}/${Math.ceil(entries.length / batchSize)}`);
		} catch (err) {
			console.error(`Error in batch ${i}:`, err);
			errors++;
		}
	}

	console.log(`\nDone! Updated ${updated} county mappings, ${errors} errors`);
}

async function verifyUpdate(): Promise<void> {
	console.log('\nVerifying update...');

	const result = await db.execute(sql`
		SELECT
			COUNT(*) as total,
			COUNT(county) as with_county,
			COUNT(DISTINCT county) as unique_counties
		FROM tracts
		WHERE is_residential = true
	`);

	console.log('Results:', result.rows[0]);

	// Sample some data
	const sample = await db.execute(sql`
		SELECT tract_fips, state_abbr, county, resilience_score
		FROM tracts
		WHERE county IS NOT NULL
		ORDER BY RANDOM()
		LIMIT 10
	`);

	console.log('\nSample tracts with county names:');
	console.table(sample.rows);
}

async function main() {
	try {
		const counties = await fetchCountyData();
		await updateCountyNames(counties);
		await verifyUpdate();
		process.exit(0);
	} catch (err) {
		console.error('Error:', err);
		process.exit(1);
	}
}

main();
