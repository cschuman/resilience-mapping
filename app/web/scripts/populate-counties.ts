/**
 * Populate County Names in Database
 *
 * Downloads county FIPS data from Census Bureau and updates the tracts table.
 * Run with: DATABASE_URL="..." npx tsx scripts/populate-counties.ts
 */

import postgres from 'postgres';

const DATABASE_URL = process.env.DATABASE_URL;

if (!DATABASE_URL) {
	console.error('DATABASE_URL environment variable is required');
	process.exit(1);
}

const sql = postgres(DATABASE_URL, {
	ssl: false,
	connect_timeout: 30,
});

// Fetch county data from Census Bureau API
async function fetchCountyData(): Promise<Map<string, string>> {
	console.log('Fetching county data from Census Bureau...');

	const url = 'https://api.census.gov/data/2020/dec/pl?get=NAME&for=county:*';
	const response = await fetch(url);

	if (!response.ok) {
		throw new Error(`Census API error: ${response.status}`);
	}

	const data = await response.json() as string[][];

	// First row is headers: ["NAME", "state", "county"]
	// Data rows: ["Autauga County, Alabama", "01", "001"]
	const countyMap = new Map<string, string>();

	for (let i = 1; i < data.length; i++) {
		const [fullName, stateFips, countyFips] = data[i];
		const fips5 = stateFips + countyFips; // e.g., "01001"

		// Extract just county name (remove ", State" suffix)
		const countyName = fullName.split(',')[0].trim();
		countyMap.set(fips5, countyName);
	}

	console.log(`  Loaded ${countyMap.size} counties`);
	return countyMap;
}

async function updateCountyNames(countyMap: Map<string, string>) {
	console.log('\nUpdating tract county names...');

	// Get all unique state+county combinations from tracts
	const tracts = await sql`
		SELECT DISTINCT LEFT(tract_fips, 5) as county_fips
		FROM tracts
		WHERE tract_fips IS NOT NULL
	`;

	console.log(`  Found ${tracts.length} unique counties in tracts table`);

	let updated = 0;
	let notFound = 0;

	// Update in batches by county
	for (const tract of tracts) {
		const countyFips = tract.county_fips;
		const countyName = countyMap.get(countyFips);

		if (countyName) {
			await sql`
				UPDATE tracts
				SET county = ${countyName}
				WHERE LEFT(tract_fips, 5) = ${countyFips}
			`;
			updated++;
		} else {
			notFound++;
			console.log(`  Warning: No county name found for FIPS ${countyFips}`);
		}

		// Progress indicator
		if (updated % 100 === 0) {
			process.stdout.write(`\r  Updated ${updated} counties...`);
		}
	}

	console.log(`\n  Updated: ${updated} counties`);
	if (notFound > 0) {
		console.log(`  Not found: ${notFound} counties`);
	}
}

async function verifyUpdate() {
	console.log('\nVerifying update...');

	const [sample] = await sql`
		SELECT tract_fips, state_abbr, county, resilience_score
		FROM tracts
		WHERE county IS NOT NULL
		ORDER BY resilience_score DESC
		LIMIT 1
	`;

	if (sample) {
		console.log(`  Top tract: ${sample.tract_fips}`);
		console.log(`  Location: ${sample.county}, ${sample.state_abbr}`);
		console.log(`  Score: ${parseFloat(sample.resilience_score).toFixed(2)}`);
	}

	const [stats] = await sql`
		SELECT
			COUNT(*) as total,
			COUNT(county) as with_county,
			COUNT(*) - COUNT(county) as without_county
		FROM tracts
	`;

	console.log(`\n  Total tracts: ${stats.total}`);
	console.log(`  With county name: ${stats.with_county}`);
	console.log(`  Without county name: ${stats.without_county}`);
}

async function main() {
	console.log('='.repeat(50));
	console.log('Populating County Names');
	console.log('='.repeat(50));

	try {
		const countyMap = await fetchCountyData();
		await updateCountyNames(countyMap);
		await verifyUpdate();

		console.log('\n' + '='.repeat(50));
		console.log('Done!');
		console.log('='.repeat(50));
	} catch (error) {
		console.error('Error:', error);
		process.exit(1);
	} finally {
		await sql.end();
	}
}

main();
