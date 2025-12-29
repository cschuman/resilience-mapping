/**
 * Database Performance Index Migration
 *
 * Run with: DATABASE_URL="..." npx tsx scripts/migrate-indexes.ts
 *
 * This migration adds critical performance indexes identified by the database audit:
 * - Removes redundant idx_tracts_fips (UNIQUE constraint provides index)
 * - Replaces DESC index with ASC for better range query performance
 * - Adds composite indexes for common query patterns
 * - Adds data integrity constraints
 *
 * Expected performance improvements:
 * - PERCENT_RANK query: 80-150ms → 2-5ms (97% improvement)
 * - Tracts list: 25-40ms → 8-12ms (70% improvement)
 * - Stats aggregation: 60-90ms → 8-15ms (80% improvement)
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

async function migrateIndexes() {
	console.log('Starting performance index migration...\n');

	try {
		// Check if migration was already applied
		const [existingMigration] = await sql`
			SELECT name FROM migrations WHERE name = '002_performance_indexes'
		`;

		if (existingMigration) {
			console.log('Migration 002_performance_indexes already applied. Skipping.');
			await sql.end();
			return;
		}

		// ===================================================================
		// Step 1: Remove redundant index (UNIQUE constraint provides index)
		// ===================================================================
		console.log('1. Removing redundant idx_tracts_fips...');
		try {
			await sql`DROP INDEX IF EXISTS idx_tracts_fips`;
			console.log('   ✓ Removed idx_tracts_fips');
		} catch (e) {
			console.log(`   ⚠ Could not remove idx_tracts_fips: ${(e as Error).message}`);
		}

		// ===================================================================
		// Step 2: Replace DESC index with ASC (better for range queries)
		// ===================================================================
		console.log('\n2. Replacing resilience score index with ASC version...');
		try {
			await sql`DROP INDEX IF EXISTS idx_tracts_resilience`;
			console.log('   ✓ Dropped old idx_tracts_resilience DESC');
		} catch (e) {
			console.log(`   ⚠ Could not drop old index: ${(e as Error).message}`);
		}

		await sql`
			CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tracts_resilience_asc
			ON tracts(resilience_score ASC NULLS LAST)
			WHERE resilience_score IS NOT NULL
		`;
		console.log('   ✓ Created idx_tracts_resilience_asc');

		// ===================================================================
		// Step 3: Add composite index for state + score range queries
		// ===================================================================
		console.log('\n3. Creating composite index for state + resilience queries...');
		await sql`
			CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tracts_state_resilience
			ON tracts(state_abbr, resilience_score)
			WHERE resilience_score IS NOT NULL
		`;
		console.log('   ✓ Created idx_tracts_state_resilience');

		// ===================================================================
		// Step 4: Add covering index for state aggregation queries
		// ===================================================================
		console.log('\n4. Creating covering index for state aggregation...');
		await sql`
			CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tracts_state_score_pop
			ON tracts(state_abbr, resilience_score, total_pop)
			WHERE resilience_score > 0
		`;
		console.log('   ✓ Created idx_tracts_state_score_pop');

		// ===================================================================
		// Step 5: Add FIPS format validation constraint
		// ===================================================================
		console.log('\n5. Adding FIPS format constraint...');
		try {
			await sql`
				ALTER TABLE tracts
				ADD CONSTRAINT tract_fips_format
				CHECK (tract_fips ~ '^\\d{11}$')
			`;
			console.log('   ✓ Added tract_fips_format constraint');
		} catch (e) {
			const msg = (e as Error).message;
			if (msg.includes('already exists')) {
				console.log('   ⚠ Constraint already exists, skipping');
			} else {
				console.log(`   ⚠ Could not add constraint: ${msg}`);
			}
		}

		// ===================================================================
		// Step 6: Add range constraints for data integrity
		// ===================================================================
		console.log('\n6. Adding data integrity constraints...');
		const constraints = [
			{
				name: 'gq_college_pct_range',
				check: 'gq_college_pct IS NULL OR (gq_college_pct >= 0.00 AND gq_college_pct <= 100.00)'
			},
			{
				name: 'gq_military_pct_range',
				check: 'gq_military_pct IS NULL OR (gq_military_pct >= 0.00 AND gq_military_pct <= 100.00)'
			},
			{
				name: 'gq_correctional_pct_range',
				check: 'gq_correctional_pct IS NULL OR (gq_correctional_pct >= 0.00 AND gq_correctional_pct <= 100.00)'
			},
			{
				name: 'gq_nursing_pct_range',
				check: 'gq_nursing_pct IS NULL OR (gq_nursing_pct >= 0.00 AND gq_nursing_pct <= 100.00)'
			}
		];

		for (const { name, check } of constraints) {
			try {
				await sql.unsafe(`
					ALTER TABLE tracts
					ADD CONSTRAINT ${name}
					CHECK (${check})
				`);
				console.log(`   ✓ Added ${name}`);
			} catch (e) {
				const msg = (e as Error).message;
				if (msg.includes('already exists')) {
					console.log(`   ⚠ ${name} already exists, skipping`);
				} else {
					console.log(`   ⚠ Could not add ${name}: ${msg}`);
				}
			}
		}

		// ===================================================================
		// Step 7: Add index for communities table
		// ===================================================================
		console.log('\n7. Creating index for communities table...');
		await sql`
			CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_communities_tract_fips
			ON communities(tract_fips)
		`;
		console.log('   ✓ Created idx_communities_tract_fips');

		// ===================================================================
		// Record migration
		// ===================================================================
		console.log('\n8. Recording migration...');
		await sql`
			INSERT INTO migrations (name)
			VALUES ('002_performance_indexes')
			ON CONFLICT DO NOTHING
		`;
		console.log('   ✓ Migration recorded');

		// ===================================================================
		// Verify indexes
		// ===================================================================
		console.log('\n========================================');
		console.log('Verifying indexes...');
		console.log('========================================\n');

		const indexes = await sql`
			SELECT indexname, indexdef
			FROM pg_indexes
			WHERE tablename = 'tracts'
			ORDER BY indexname
		`;

		for (const idx of indexes) {
			console.log(`${idx.indexname}:`);
			console.log(`  ${idx.indexdef}\n`);
		}

		// Analyze table to update statistics
		console.log('Running ANALYZE to update statistics...');
		await sql`ANALYZE tracts`;
		console.log('✓ ANALYZE complete');

		console.log('\n========================================');
		console.log('Migration complete!');
		console.log('========================================');
		console.log('\nExpected performance improvements:');
		console.log('- PERCENT_RANK: 80-150ms → 2-5ms');
		console.log('- Tracts list:  25-40ms  → 8-12ms');
		console.log('- Stats query:  60-90ms  → 8-15ms');

	} catch (e) {
		console.error('Migration failed:', e);
		process.exit(1);
	} finally {
		await sql.end();
	}
}

migrateIndexes();
