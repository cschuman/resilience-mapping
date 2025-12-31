/**
 * Migration: Add performance indexes
 *
 * This migration adds indexes to improve query performance:
 * 1. State + resilience_score composite index (for filtered rankings)
 * 2. Burden index (for sorting by burden)
 * 3. Population index (for sorting and filtering)
 * 4. Composite indexes for common API query patterns
 *
 * Run with: DATABASE_URL="..." npx tsx scripts/migrate-add-indexes.ts
 */

import postgres from 'postgres';

const DATABASE_URL = process.env.DATABASE_URL;

if (!DATABASE_URL) {
	console.error('DATABASE_URL environment variable is required');
	console.error('Usage: DATABASE_URL="postgres://..." npx tsx scripts/migrate-add-indexes.ts');
	process.exit(1);
}

const sql = postgres(DATABASE_URL, {
	ssl: false,
	connect_timeout: 30
});

interface IndexDefinition {
	name: string;
	definition: string;
	description: string;
}

const INDEXES: IndexDefinition[] = [
	{
		name: 'idx_tracts_state_score',
		definition: `CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tracts_state_score
			ON tracts(state_abbr, resilience_score DESC)
			WHERE is_residential = TRUE`,
		description: 'State + score for filtered state rankings'
	},
	{
		name: 'idx_tracts_burden',
		definition: `CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tracts_burden
			ON tracts(burden DESC)
			WHERE is_residential = TRUE`,
		description: 'Burden sorting for residential tracts'
	},
	{
		name: 'idx_tracts_population',
		definition: `CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tracts_population
			ON tracts(total_pop DESC)
			WHERE is_residential = TRUE`,
		description: 'Population sorting for residential tracts'
	},
	{
		name: 'idx_tracts_score_range',
		definition: `CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tracts_score_range
			ON tracts(resilience_score)
			WHERE is_residential = TRUE`,
		description: 'Score range queries for residential tracts'
	},
	{
		name: 'idx_tracts_state',
		definition: `CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tracts_state
			ON tracts(state_abbr)`,
		description: 'State filtering'
	},
	{
		name: 'idx_tracts_fips',
		definition: `CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tracts_fips
			ON tracts(tract_fips)`,
		description: 'FIPS lookup (may already exist as primary key)'
	},
	{
		name: 'idx_tracts_tract_type',
		definition: `CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tracts_tract_type
			ON tracts(tract_type)`,
		description: 'Tract type filtering'
	}
];

async function migrate() {
	console.log('╔══════════════════════════════════════════════════════════════════╗');
	console.log('║         MIGRATION: Add Performance Indexes                       ║');
	console.log('║         Task 1.1: Infrastructure Foundation                      ║');
	console.log('╚══════════════════════════════════════════════════════════════════╝\n');

	// First, check existing indexes
	console.log('Checking existing indexes...\n');
	const existingIndexes = await sql`
		SELECT indexname, indexdef
		FROM pg_indexes
		WHERE tablename = 'tracts'
		ORDER BY indexname
	`;

	console.log('Current indexes on tracts table:');
	console.log('─'.repeat(60));
	existingIndexes.forEach((idx) => {
		console.log(`  ${idx.indexname}`);
	});
	console.log('─'.repeat(60));
	console.log();

	// Create each index
	let created = 0;
	let skipped = 0;

	for (const index of INDEXES) {
		console.log(`Creating ${index.name}...`);
		console.log(`  Description: ${index.description}`);

		const exists = existingIndexes.some((idx) => idx.indexname === index.name);
		if (exists) {
			console.log('  ℹ Index already exists, skipping');
			skipped++;
			continue;
		}

		try {
			// Note: CONCURRENTLY can't be used in a transaction, so we run each separately
			await sql.unsafe(index.definition);
			console.log('  ✓ Created successfully');
			created++;
		} catch (e) {
			const error = e as Error;
			if (error.message.includes('already exists')) {
				console.log('  ℹ Index already exists');
				skipped++;
			} else {
				console.error(`  ✗ Failed: ${error.message}`);
			}
		}
		console.log();
	}

	// Record migration
	console.log('Recording migration...');
	await sql`INSERT INTO migrations (name) VALUES ('003_add_indexes') ON CONFLICT DO NOTHING`;

	// Analyze table to update statistics
	console.log('\nAnalyzing table to update query planner statistics...');
	await sql`ANALYZE tracts`;
	console.log('  ✓ ANALYZE complete');

	// Final summary
	console.log('\n╔══════════════════════════════════════════════════════════════════╗');
	console.log('║                     MIGRATION SUMMARY                            ║');
	console.log('╚══════════════════════════════════════════════════════════════════╝\n');

	console.log(`Indexes created: ${created}`);
	console.log(`Indexes skipped (already exist): ${skipped}`);

	// Show final index list
	const finalIndexes = await sql`
		SELECT indexname, pg_size_pretty(pg_relation_size(quote_ident(indexname)::text)) as size
		FROM pg_indexes
		WHERE tablename = 'tracts'
		ORDER BY indexname
	`;

	console.log('\nFinal index list:');
	console.log('─'.repeat(60));
	finalIndexes.forEach((idx) => {
		console.log(`  ${idx.indexname.padEnd(40)} ${idx.size}`);
	});
	console.log('─'.repeat(60));

	// Test query performance
	console.log('\nTesting query performance...');

	const start1 = Date.now();
	await sql`
		SELECT COUNT(*) FROM tracts
		WHERE state_abbr = 'CA' AND is_residential = TRUE
	`;
	const time1 = Date.now() - start1;
	console.log(`  State filter query: ${time1}ms`);

	const start2 = Date.now();
	await sql`
		SELECT COUNT(*) FROM tracts
		WHERE resilience_score BETWEEN -1 AND 1 AND is_residential = TRUE
	`;
	const time2 = Date.now() - start2;
	console.log(`  Score range query: ${time2}ms`);

	const start3 = Date.now();
	await sql`
		SELECT tract_fips, resilience_score FROM tracts
		WHERE is_residential = TRUE
		ORDER BY resilience_score DESC
		LIMIT 100
	`;
	const time3 = Date.now() - start3;
	console.log(`  Top 100 query: ${time3}ms`);

	await sql.end();
	console.log('\n✅ Migration complete!');
}

migrate().catch((e) => {
	console.error('Migration failed:', e);
	process.exit(1);
});
