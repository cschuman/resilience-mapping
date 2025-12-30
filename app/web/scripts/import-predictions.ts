/**
 * Import Trajectory Predictions
 *
 * Run with: npx tsx scripts/import-predictions.ts
 *
 * Requires DATABASE_URL environment variable
 */

import postgres from 'postgres';
import { createReadStream } from 'fs';
import { parse } from 'csv-parse';
import { resolve } from 'path';

const DATABASE_URL = process.env.DATABASE_URL;

if (!DATABASE_URL) {
	console.error('DATABASE_URL environment variable is required');
	process.exit(1);
}

const sql = postgres(DATABASE_URL, {
	ssl: false,
	connect_timeout: 30
});

interface PredictionRow {
	tract_fips: string;
	state_abbr: string;
	predicted_trajectory: string;
	prob_decline: string;
	prob_improve: string;
	prob_stable: string;
	confidence: string;
	prediction_date: string;
	model_version: string;
}

async function importPredictions() {
	console.log('Importing trajectory predictions...\n');

	const csvPath = resolve(__dirname, '../../../data/processed/tract_predictions.csv');
	console.log(`Reading from: ${csvPath}`);

	const records: PredictionRow[] = [];

	// Parse CSV
	const parser = createReadStream(csvPath).pipe(
		parse({
			columns: true,
			skip_empty_lines: true
		})
	);

	for await (const record of parser) {
		records.push(record as PredictionRow);
	}

	console.log(`Parsed ${records.length} predictions\n`);

	// Clear existing predictions
	console.log('Clearing existing predictions...');
	await sql`TRUNCATE tract_predictions`;

	// Insert in batches
	const batchSize = 1000;
	let inserted = 0;

	for (let i = 0; i < records.length; i += batchSize) {
		const batch = records.slice(i, i + batchSize);

		await sql`
			INSERT INTO tract_predictions (
				tract_fips, state_abbr, predicted_trajectory,
				prob_decline, prob_improve, prob_stable,
				confidence, prediction_date, model_version
			)
			SELECT * FROM json_to_recordset(${JSON.stringify(
				batch.map((r) => ({
					tract_fips: r.tract_fips,
					state_abbr: r.state_abbr,
					predicted_trajectory: r.predicted_trajectory,
					prob_decline: parseFloat(r.prob_decline),
					prob_improve: parseFloat(r.prob_improve),
					prob_stable: parseFloat(r.prob_stable),
					confidence: parseFloat(r.confidence),
					prediction_date: r.prediction_date,
					model_version: r.model_version
				}))
			)}) AS x(
				tract_fips VARCHAR(11),
				state_abbr VARCHAR(2),
				predicted_trajectory VARCHAR(10),
				prob_decline DECIMAL,
				prob_improve DECIMAL,
				prob_stable DECIMAL,
				confidence DECIMAL,
				prediction_date DATE,
				model_version VARCHAR(50)
			)
		`;

		inserted += batch.length;
		console.log(`  Inserted ${inserted} / ${records.length}`);
	}

	// Summary
	const [count] = await sql`SELECT COUNT(*) as count FROM tract_predictions`;
	const trajectories = await sql`
		SELECT predicted_trajectory, COUNT(*) as count
		FROM tract_predictions
		GROUP BY predicted_trajectory
		ORDER BY count DESC
	`;

	console.log('\n========================================');
	console.log('Import complete!');
	console.log('========================================');
	console.log(`Total predictions: ${count.count}`);
	console.log('\nTrajectory distribution:');
	for (const t of trajectories) {
		console.log(`  ${t.predicted_trajectory}: ${t.count}`);
	}

	await sql.end();
}

importPredictions().catch((e) => {
	console.error('Import failed:', e);
	process.exit(1);
});
