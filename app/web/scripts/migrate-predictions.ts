/**
 * Database Migration for Trajectory Predictions
 *
 * Run with: npx tsx scripts/migrate-predictions.ts
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
	ssl: false,
	connect_timeout: 30
});

async function migrate() {
	console.log('Running predictions migration...\n');

	// 1. Create predictions table
	console.log('1. Creating tract_predictions table...');
	await sql`
		CREATE TABLE IF NOT EXISTS tract_predictions (
			id SERIAL PRIMARY KEY,
			tract_fips VARCHAR(11) UNIQUE NOT NULL,
			state_abbr VARCHAR(2),
			predicted_trajectory VARCHAR(10) NOT NULL,
			prob_decline DECIMAL(5, 4),
			prob_improve DECIMAL(5, 4),
			prob_stable DECIMAL(5, 4),
			confidence DECIMAL(5, 4),
			prediction_date DATE,
			model_version VARCHAR(50),
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	`;
	console.log('   Done');

	// 2. Create indexes
	console.log('\n2. Creating indexes...');
	await sql`CREATE INDEX IF NOT EXISTS idx_predictions_fips ON tract_predictions(tract_fips)`;
	await sql`CREATE INDEX IF NOT EXISTS idx_predictions_trajectory ON tract_predictions(predicted_trajectory)`;
	await sql`CREATE INDEX IF NOT EXISTS idx_predictions_confidence ON tract_predictions(confidence DESC)`;
	await sql`CREATE INDEX IF NOT EXISTS idx_predictions_state ON tract_predictions(state_abbr)`;
	console.log('   Done');

	// 3. Track migration
	console.log('\n3. Recording migration...');
	await sql`INSERT INTO migrations (name) VALUES ('002_predictions') ON CONFLICT DO NOTHING`;
	console.log('   Done');

	// Summary
	const [count] = await sql`SELECT COUNT(*) as count FROM tract_predictions`;

	console.log('\n========================================');
	console.log('Predictions migration complete!');
	console.log('========================================');
	console.log(`Predictions: ${count.count}`);

	await sql.end();
}

migrate().catch((e) => {
	console.error('Migration failed:', e);
	process.exit(1);
});
