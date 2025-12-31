/**
 * Migration: Add is_residential filter
 *
 * This migration adds:
 * 1. is_residential BOOLEAN column (defaults to TRUE)
 * 2. tract_type VARCHAR column for categorization
 * 3. Updates non-residential tracts based on analysis criteria
 * 4. Creates index for efficient filtering
 *
 * Run with: DATABASE_URL="..." npx tsx scripts/migrate-residential-filter.ts
 */

import postgres from 'postgres';

const DATABASE_URL = process.env.DATABASE_URL;

if (!DATABASE_URL) {
	console.error('DATABASE_URL environment variable is required');
	console.error('Usage: DATABASE_URL="postgres://..." npx tsx scripts/migrate-residential-filter.ts');
	process.exit(1);
}

const sql = postgres(DATABASE_URL, {
	ssl: false,
	connect_timeout: 30,
});

// Thresholds (from analysis)
const THRESHOLDS = {
	MIN_POP: 100,         // Minimum population to be considered residential
	PRISON: 25,           // 25% or more in correctional facilities
	MILITARY: 25,         // 25% or more in military quarters
	COLLEGE: 50,          // 50% or more in college dorms (flag but don't exclude by default)
};

async function migrate() {
	console.log('╔══════════════════════════════════════════════════════════════════╗');
	console.log('║         MIGRATION: Add is_residential Filter                     ║');
	console.log('║         Task 0.2: Data Quality Sprint                            ║');
	console.log('╚══════════════════════════════════════════════════════════════════╝\n');

	// Step 1: Add columns if they don't exist
	console.log('Step 1: Adding columns...');

	try {
		await sql`ALTER TABLE tracts ADD COLUMN IF NOT EXISTS is_residential BOOLEAN DEFAULT TRUE`;
		console.log('  ✓ Added is_residential column');
	} catch (e) {
		console.log(`  ℹ is_residential column may already exist: ${(e as Error).message}`);
	}

	try {
		await sql`ALTER TABLE tracts ADD COLUMN IF NOT EXISTS tract_type VARCHAR(20) DEFAULT 'residential'`;
		console.log('  ✓ Added tract_type column');
	} catch (e) {
		console.log(`  ℹ tract_type column may already exist: ${(e as Error).message}`);
	}

	// Step 2: Reset all tracts to residential (in case of re-run)
	console.log('\nStep 2: Resetting all tracts to residential...');
	const resetResult = await sql`
		UPDATE tracts
		SET is_residential = TRUE, tract_type = 'residential'
		WHERE is_residential = FALSE OR tract_type != 'residential'
	`;
	console.log(`  ✓ Reset ${resetResult.count} tracts`);

	// Step 3: Flag zero/small population tracts
	console.log('\nStep 3: Flagging zero/small population tracts...');
	const smallPopResult = await sql`
		UPDATE tracts
		SET is_residential = FALSE, tract_type = 'small_pop'
		WHERE total_pop IS NULL OR total_pop < ${THRESHOLDS.MIN_POP}
	`;
	console.log(`  ✓ Flagged ${smallPopResult.count} tracts as small_pop (pop < ${THRESHOLDS.MIN_POP})`);

	// Step 4: Flag correctional tracts
	console.log('\nStep 4: Flagging correctional facility tracts...');
	const prisonResult = await sql`
		UPDATE tracts
		SET is_residential = FALSE, tract_type = 'correctional'
		WHERE gq_correctional_pct >= ${THRESHOLDS.PRISON}
		  AND is_residential = TRUE
	`;
	console.log(`  ✓ Flagged ${prisonResult.count} tracts as correctional (≥${THRESHOLDS.PRISON}%)`);

	// Step 5: Flag military tracts
	console.log('\nStep 5: Flagging military base tracts...');
	const militaryResult = await sql`
		UPDATE tracts
		SET is_residential = FALSE, tract_type = 'military'
		WHERE gq_military_pct >= ${THRESHOLDS.MILITARY}
		  AND is_residential = TRUE
	`;
	console.log(`  ✓ Flagged ${militaryResult.count} tracts as military (≥${THRESHOLDS.MILITARY}%)`);

	// Step 6: Flag college tracts (but keep is_residential = TRUE for now)
	console.log('\nStep 6: Flagging college campus tracts (marked but not excluded)...');
	const collegeResult = await sql`
		UPDATE tracts
		SET tract_type = 'college'
		WHERE gq_college_pct >= ${THRESHOLDS.COLLEGE}
		  AND is_residential = TRUE
		  AND tract_type = 'residential'
	`;
	console.log(`  ✓ Flagged ${collegeResult.count} tracts as college (≥${THRESHOLDS.COLLEGE}%)`);
	console.log(`    (Note: College tracts remain is_residential = TRUE for now)`);

	// Step 7: Create index
	console.log('\nStep 7: Creating index for efficient filtering...');
	try {
		await sql`
			CREATE INDEX IF NOT EXISTS idx_tracts_residential
			ON tracts(is_residential)
			WHERE is_residential = TRUE
		`;
		console.log('  ✓ Created partial index idx_tracts_residential');
	} catch (e) {
		console.log(`  ℹ Index may already exist: ${(e as Error).message}`);
	}

	// Step 8: Create composite index for sorted residential queries
	console.log('\nStep 8: Creating composite index for sorted queries...');
	try {
		await sql`
			CREATE INDEX IF NOT EXISTS idx_tracts_residential_score
			ON tracts(resilience_score DESC)
			WHERE is_residential = TRUE
		`;
		console.log('  ✓ Created partial index idx_tracts_residential_score');
	} catch (e) {
		console.log(`  ℹ Index may already exist: ${(e as Error).message}`);
	}

	// Step 9: Record migration
	console.log('\nStep 9: Recording migration...');
	await sql`INSERT INTO migrations (name) VALUES ('002_residential_filter') ON CONFLICT DO NOTHING`;

	// Summary
	console.log('\n╔══════════════════════════════════════════════════════════════════╗');
	console.log('║                     MIGRATION SUMMARY                            ║');
	console.log('╚══════════════════════════════════════════════════════════════════╝\n');

	const [totalCount] = await sql`SELECT COUNT(*) as count FROM tracts`;
	const [residentialCount] = await sql`SELECT COUNT(*) as count FROM tracts WHERE is_residential = TRUE`;
	const [nonResidentialCount] = await sql`SELECT COUNT(*) as count FROM tracts WHERE is_residential = FALSE`;

	const breakdown = await sql`
		SELECT tract_type, COUNT(*) as count
		FROM tracts
		GROUP BY tract_type
		ORDER BY count DESC
	`;

	console.log('Tract Classification:');
	console.log('─'.repeat(40));
	breakdown.forEach((row) => {
		console.log(`  ${row.tract_type.padEnd(15)}: ${parseInt(row.count).toLocaleString().padStart(8)}`);
	});
	console.log('─'.repeat(40));
	console.log(`  TOTAL         : ${parseInt(totalCount.count).toLocaleString().padStart(8)}`);

	console.log('\nFiltering Summary:');
	console.log(`  Residential (included)    : ${parseInt(residentialCount.count).toLocaleString()} (${((parseInt(residentialCount.count) / parseInt(totalCount.count)) * 100).toFixed(1)}%)`);
	console.log(`  Non-residential (excluded): ${parseInt(nonResidentialCount.count).toLocaleString()} (${((parseInt(nonResidentialCount.count) / parseInt(totalCount.count)) * 100).toFixed(1)}%)`);

	// Verify top 100 is now clean
	console.log('\nVerifying top 100 residential tracts:');
	const [problemsInTop100] = await sql`
		SELECT COUNT(*) as count FROM (
			SELECT tract_fips FROM tracts
			WHERE is_residential = TRUE
			ORDER BY resilience_score DESC
			LIMIT 100
		) top100
		JOIN tracts t ON t.tract_fips = top100.tract_fips
		WHERE t.total_pop < ${THRESHOLDS.MIN_POP}
		   OR t.gq_correctional_pct >= ${THRESHOLDS.PRISON}
		   OR t.gq_military_pct >= ${THRESHOLDS.MILITARY}
	`;
	console.log(`  Problematic tracts in top 100: ${problemsInTop100.count}`);

	if (parseInt(problemsInTop100.count) === 0) {
		console.log('  ✅ TOP 100 IS NOW CLEAN!');
	} else {
		console.log('  ⚠️  Some issues remain - review needed');
	}

	// Show new top 10
	console.log('\nNew Top 10 Most Resilient Communities (residential only):');
	console.log('─'.repeat(80));
	console.log('Rank | FIPS        | State | Population | Score');
	console.log('─'.repeat(80));

	const newTop10 = await sql`
		SELECT tract_fips, state_abbr, total_pop, resilience_score
		FROM tracts
		WHERE is_residential = TRUE
		ORDER BY resilience_score DESC
		LIMIT 10
	`;

	newTop10.forEach((t, idx) => {
		console.log(
			`${String(idx + 1).padStart(4)} | ${t.tract_fips} | ${t.state_abbr}    | ${String(t.total_pop).padStart(10)} | ${parseFloat(t.resilience_score).toFixed(3)}`
		);
	});

	await sql.end();
	console.log('\n✅ Migration complete!');
}

migrate().catch((e) => {
	console.error('Migration failed:', e);
	process.exit(1);
});
