/**
 * Database Migration Script
 *
 * Run with: npx tsx scripts/migrate.ts
 *
 * Requires DATABASE_URL environment variable
 */

import postgres from 'postgres';

const DATABASE_URL = process.env.DATABASE_URL;

if (!DATABASE_URL) {
	console.error('DATABASE_URL environment variable is required');
	process.exit(1);
}

const sql = postgres(DATABASE_URL, {
	ssl: false, // Disable SSL for local proxy connections
	connect_timeout: 30,
});

async function migrate() {
	console.log('Running migrations...\n');

	// 1. Enable PostGIS
	console.log('1. Enabling PostGIS extension...');
	try {
		await sql`CREATE EXTENSION IF NOT EXISTS postgis`;
		const [version] = await sql`SELECT PostGIS_Version() as version`;
		console.log(`   PostGIS version: ${version.version}`);
	} catch (e) {
		console.log(`   PostGIS may not be available: ${(e as Error).message}`);
	}

	// 2. Create tracts table
	console.log('\n2. Creating tracts table...');
	await sql`
		CREATE TABLE IF NOT EXISTS tracts (
			id SERIAL PRIMARY KEY,
			tract_fips VARCHAR(11) UNIQUE NOT NULL,
			state_abbr VARCHAR(2),
			county VARCHAR(100),
			total_pop INTEGER,
			resilience_score DECIMAL(10, 6),
			burden DECIMAL(10, 6),
			gq_college_pct DECIMAL(5, 2) DEFAULT 0,
			gq_military_pct DECIMAL(5, 2) DEFAULT 0,
			gq_correctional_pct DECIMAL(5, 2) DEFAULT 0,
			gq_nursing_pct DECIMAL(5, 2) DEFAULT 0,
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	`;
	console.log('   Done');

	// 3. Create indexes
	console.log('\n3. Creating indexes...');
	await sql`CREATE INDEX IF NOT EXISTS idx_tracts_state ON tracts(state_abbr)`;
	await sql`CREATE INDEX IF NOT EXISTS idx_tracts_resilience ON tracts(resilience_score DESC)`;
	await sql`CREATE INDEX IF NOT EXISTS idx_tracts_fips ON tracts(tract_fips)`;
	console.log('   Done');

	// 4. Create communities table (for stories with consent)
	console.log('\n4. Creating communities table...');
	await sql`
		CREATE TABLE IF NOT EXISTS communities (
			id SERIAL PRIMARY KEY,
			tract_fips VARCHAR(11) REFERENCES tracts(tract_fips),
			name VARCHAR(255),
			description TEXT,
			story TEXT,
			consent_given BOOLEAN DEFAULT FALSE,
			consent_date TIMESTAMP,
			contact_email VARCHAR(255),
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	`;
	console.log('   Done');

	// 5. Create migrations tracking table
	console.log('\n5. Creating migrations table...');
	await sql`
		CREATE TABLE IF NOT EXISTS migrations (
			id SERIAL PRIMARY KEY,
			name VARCHAR(255) UNIQUE NOT NULL,
			applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	`;
	await sql`INSERT INTO migrations (name) VALUES ('001_initial') ON CONFLICT DO NOTHING`;
	console.log('   Done');

	// Summary
	const [tractCount] = await sql`SELECT COUNT(*) as count FROM tracts`;
	const [communityCount] = await sql`SELECT COUNT(*) as count FROM communities`;

	console.log('\n========================================');
	console.log('Migration complete!');
	console.log('========================================');
	console.log(`Tracts: ${tractCount.count}`);
	console.log(`Communities: ${communityCount.count}`);

	await sql.end();
}

migrate().catch((e) => {
	console.error('Migration failed:', e);
	process.exit(1);
});
