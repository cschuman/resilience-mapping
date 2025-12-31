/**
 * Migration: Create materialized views for common aggregations
 *
 * This migration creates materialized views for:
 * 1. State-level aggregates (avg score, tract count, population)
 * 2. Score distribution histogram
 * 3. Overall statistics
 *
 * These views can be refreshed periodically to avoid expensive aggregations on every request.
 *
 * Run with: DATABASE_URL="..." npx tsx scripts/migrate-materialized-views.ts
 */

import postgres from 'postgres';

const DATABASE_URL = process.env.DATABASE_URL;

if (!DATABASE_URL) {
	console.error('DATABASE_URL environment variable is required');
	console.error('Usage: DATABASE_URL="postgres://..." npx tsx scripts/migrate-materialized-views.ts');
	process.exit(1);
}

const sql = postgres(DATABASE_URL, {
	ssl: false,
	connect_timeout: 30
});

async function migrate() {
	console.log('╔══════════════════════════════════════════════════════════════════╗');
	console.log('║         MIGRATION: Create Materialized Views                     ║');
	console.log('║         Task 1.2: Infrastructure Foundation                      ║');
	console.log('╚══════════════════════════════════════════════════════════════════╝\n');

	// View 1: State aggregates
	console.log('Creating mv_state_stats materialized view...');
	await sql`DROP MATERIALIZED VIEW IF EXISTS mv_state_stats CASCADE`;
	await sql`
		CREATE MATERIALIZED VIEW mv_state_stats AS
		SELECT
			state_abbr,
			COUNT(*) as tract_count,
			COUNT(*) FILTER (WHERE is_residential = TRUE) as residential_count,
			AVG(resilience_score) FILTER (WHERE is_residential = TRUE) as avg_resilience,
			MIN(resilience_score) FILTER (WHERE is_residential = TRUE) as min_resilience,
			MAX(resilience_score) FILTER (WHERE is_residential = TRUE) as max_resilience,
			SUM(total_pop) FILTER (WHERE is_residential = TRUE) as total_population,
			PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY resilience_score)
				FILTER (WHERE is_residential = TRUE) as median_resilience
		FROM tracts
		WHERE resilience_score IS NOT NULL
		GROUP BY state_abbr
	`;
	await sql`CREATE UNIQUE INDEX ON mv_state_stats(state_abbr)`;
	console.log('  ✓ Created mv_state_stats');

	// View 2: Score distribution (20 buckets from -4 to +4)
	console.log('\nCreating mv_score_distribution materialized view...');
	await sql`DROP MATERIALIZED VIEW IF EXISTS mv_score_distribution CASCADE`;
	await sql`
		CREATE MATERIALIZED VIEW mv_score_distribution AS
		SELECT
			width_bucket(resilience_score, -4, 4, 20) as bucket,
			COUNT(*) as count,
			COUNT(*) FILTER (WHERE is_residential = TRUE) as residential_count
		FROM tracts
		WHERE resilience_score IS NOT NULL
			AND resilience_score BETWEEN -4 AND 4
		GROUP BY bucket
		ORDER BY bucket
	`;
	await sql`CREATE UNIQUE INDEX ON mv_score_distribution(bucket)`;
	console.log('  ✓ Created mv_score_distribution');

	// View 3: Overall statistics
	console.log('\nCreating mv_overall_stats materialized view...');
	await sql`DROP MATERIALIZED VIEW IF EXISTS mv_overall_stats CASCADE`;
	await sql`
		CREATE MATERIALIZED VIEW mv_overall_stats AS
		SELECT
			'all' as category,
			COUNT(*) as total_tracts,
			COUNT(*) FILTER (WHERE is_residential = TRUE) as residential_tracts,
			AVG(resilience_score) FILTER (WHERE is_residential = TRUE) as avg_resilience,
			MIN(resilience_score) FILTER (WHERE is_residential = TRUE) as min_resilience,
			MAX(resilience_score) FILTER (WHERE is_residential = TRUE) as max_resilience,
			SUM(total_pop) FILTER (WHERE is_residential = TRUE) as total_population,
			PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY resilience_score)
				FILTER (WHERE is_residential = TRUE) as median_resilience,
			PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY resilience_score)
				FILTER (WHERE is_residential = TRUE) as p25_resilience,
			PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY resilience_score)
				FILTER (WHERE is_residential = TRUE) as p75_resilience
		FROM tracts
		WHERE resilience_score IS NOT NULL
	`;
	await sql`CREATE UNIQUE INDEX ON mv_overall_stats(category)`;
	console.log('  ✓ Created mv_overall_stats');

	// View 4: Tract type breakdown
	console.log('\nCreating mv_tract_type_stats materialized view...');
	await sql`DROP MATERIALIZED VIEW IF EXISTS mv_tract_type_stats CASCADE`;
	await sql`
		CREATE MATERIALIZED VIEW mv_tract_type_stats AS
		SELECT
			tract_type,
			is_residential,
			COUNT(*) as tract_count,
			AVG(resilience_score) as avg_resilience,
			SUM(total_pop) as total_population
		FROM tracts
		WHERE resilience_score IS NOT NULL
		GROUP BY tract_type, is_residential
		ORDER BY tract_count DESC
	`;
	await sql`CREATE INDEX ON mv_tract_type_stats(tract_type)`;
	console.log('  ✓ Created mv_tract_type_stats');

	// Create refresh function
	console.log('\nCreating refresh function...');
	await sql`
		CREATE OR REPLACE FUNCTION refresh_all_materialized_views()
		RETURNS void AS $$
		BEGIN
			REFRESH MATERIALIZED VIEW CONCURRENTLY mv_state_stats;
			REFRESH MATERIALIZED VIEW CONCURRENTLY mv_score_distribution;
			REFRESH MATERIALIZED VIEW CONCURRENTLY mv_overall_stats;
			REFRESH MATERIALIZED VIEW mv_tract_type_stats;
		END;
		$$ LANGUAGE plpgsql
	`;
	console.log('  ✓ Created refresh_all_materialized_views() function');

	// Record migration
	console.log('\nRecording migration...');
	await sql`INSERT INTO migrations (name) VALUES ('004_materialized_views') ON CONFLICT DO NOTHING`;

	// Summary
	console.log('\n╔══════════════════════════════════════════════════════════════════╗');
	console.log('║                     MIGRATION SUMMARY                            ║');
	console.log('╚══════════════════════════════════════════════════════════════════╝\n');

	// Show view data
	console.log('State Statistics (top 10 by avg resilience):');
	console.log('─'.repeat(70));
	const stateStats = await sql`
		SELECT state_abbr, residential_count,
			   ROUND(avg_resilience::numeric, 3) as avg_score,
			   total_population
		FROM mv_state_stats
		ORDER BY avg_resilience DESC
		LIMIT 10
	`;
	console.log('State | Tracts  | Avg Score | Population');
	stateStats.forEach((s) => {
		console.log(
			`  ${s.state_abbr}  | ${String(s.residential_count).padStart(7)} | ${String(s.avg_score).padStart(9)} | ${parseInt(s.total_population).toLocaleString()}`
		);
	});

	console.log('\nOverall Statistics:');
	console.log('─'.repeat(70));
	const [overall] = await sql`SELECT * FROM mv_overall_stats`;
	console.log(`  Total tracts: ${parseInt(overall.total_tracts).toLocaleString()}`);
	console.log(`  Residential tracts: ${parseInt(overall.residential_tracts).toLocaleString()}`);
	console.log(`  Avg resilience: ${parseFloat(overall.avg_resilience).toFixed(3)}`);
	console.log(`  Median resilience: ${parseFloat(overall.median_resilience).toFixed(3)}`);
	console.log(`  25th percentile: ${parseFloat(overall.p25_resilience).toFixed(3)}`);
	console.log(`  75th percentile: ${parseFloat(overall.p75_resilience).toFixed(3)}`);
	console.log(`  Total population: ${parseInt(overall.total_population).toLocaleString()}`);

	console.log('\nTract Type Breakdown:');
	console.log('─'.repeat(70));
	const typeStats = await sql`SELECT * FROM mv_tract_type_stats`;
	typeStats.forEach((t) => {
		console.log(
			`  ${t.tract_type.padEnd(15)} (${t.is_residential ? 'residential' : 'excluded'}): ${parseInt(t.tract_count).toLocaleString()} tracts`
		);
	});

	// Performance comparison
	console.log('\nPerformance comparison:');
	console.log('─'.repeat(70));

	const start1 = Date.now();
	await sql`
		SELECT state_abbr, COUNT(*), AVG(resilience_score)
		FROM tracts
		WHERE is_residential = TRUE
		GROUP BY state_abbr
	`;
	const time1 = Date.now() - start1;

	const start2 = Date.now();
	await sql`SELECT * FROM mv_state_stats`;
	const time2 = Date.now() - start2;

	console.log(`  Direct query (state aggregates): ${time1}ms`);
	console.log(`  Materialized view query: ${time2}ms`);
	console.log(`  Speedup: ${(time1 / time2).toFixed(1)}x faster`);

	console.log('\nTo refresh views, run:');
	console.log('  SELECT refresh_all_materialized_views();');
	console.log('\nOr refresh individually:');
	console.log('  REFRESH MATERIALIZED VIEW CONCURRENTLY mv_state_stats;');

	await sql.end();
	console.log('\n✅ Migration complete!');
}

migrate().catch((e) => {
	console.error('Migration failed:', e);
	process.exit(1);
});
