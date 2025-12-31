/**
 * Special Population Analysis Script
 *
 * Identifies tracts that should be flagged as non-residential:
 * - Prisons (high gq_correctional_pct)
 * - Military bases (high gq_military_pct)
 * - College dorms (high gq_college_pct)
 * - Nursing homes (high gq_nursing_pct)
 * - Zero population tracts
 *
 * Run with: DATABASE_URL="..." npx tsx scripts/analyze-special-populations.ts
 */

import postgres from 'postgres';

const DATABASE_URL = process.env.DATABASE_URL;

if (!DATABASE_URL) {
	console.error('DATABASE_URL environment variable is required');
	console.error('Usage: DATABASE_URL="postgres://..." npx tsx scripts/analyze-special-populations.ts');
	process.exit(1);
}

const sql = postgres(DATABASE_URL, {
	ssl: false,
	connect_timeout: 30,
});

// Thresholds for flagging (percentage of population in group quarters)
const THRESHOLDS = {
	PRISON: 25,      // 25% or more in correctional facilities
	MILITARY: 25,    // 25% or more in military quarters
	COLLEGE: 50,     // 50% or more in college dorms (higher threshold - students are residents)
	NURSING: 50,     // 50% or more in nursing homes
	ZERO_POP: 0,     // Zero population
	SMALL_POP: 100,  // Very small population (unreliable estimates)
};

interface TractAnalysis {
	tract_fips: string;
	state_abbr: string;
	total_pop: number;
	resilience_score: number;
	burden: number;
	gq_college_pct: number;
	gq_military_pct: number;
	gq_correctional_pct: number;
	gq_nursing_pct: number;
	issue: string;
}

async function analyze() {
	console.log('╔══════════════════════════════════════════════════════════════════╗');
	console.log('║         SPECIAL POPULATION TRACT ANALYSIS                        ║');
	console.log('║         Task 0.1: Data Quality Sprint                            ║');
	console.log('╚══════════════════════════════════════════════════════════════════╝\n');

	// Get total tract count
	const [totalCount] = await sql`SELECT COUNT(*) as count FROM tracts`;
	console.log(`Total tracts in database: ${parseInt(totalCount.count).toLocaleString()}\n`);

	// 1. PRISON TRACTS (high correctional population)
	console.log('═══════════════════════════════════════════════════════════════════');
	console.log('1. PRISON/CORRECTIONAL TRACTS (≥25% in correctional facilities)');
	console.log('═══════════════════════════════════════════════════════════════════');

	const prisonTracts = await sql`
		SELECT tract_fips, state_abbr, total_pop, resilience_score, burden,
			   gq_correctional_pct, gq_college_pct, gq_military_pct, gq_nursing_pct
		FROM tracts
		WHERE gq_correctional_pct >= ${THRESHOLDS.PRISON}
		ORDER BY resilience_score DESC
		LIMIT 50
	`;

	console.log(`Found: ${prisonTracts.length} tracts with ≥${THRESHOLDS.PRISON}% correctional population\n`);

	if (prisonTracts.length > 0) {
		console.log('Top 10 by resilience score (THESE SHOULD NOT APPEAR AS "RESILIENT"):');
		console.log('─'.repeat(100));
		console.log('FIPS        | State | Pop    | Score  | Correctional%');
		console.log('─'.repeat(100));
		prisonTracts.slice(0, 10).forEach((t) => {
			console.log(
				`${t.tract_fips} | ${t.state_abbr}    | ${String(t.total_pop).padStart(6)} | ${parseFloat(t.resilience_score).toFixed(2).padStart(6)} | ${parseFloat(t.gq_correctional_pct).toFixed(1)}%`
			);
		});
	}

	// Count how many are in top 100 resilient
	const [prisonInTop100] = await sql`
		SELECT COUNT(*) as count FROM (
			SELECT tract_fips FROM tracts ORDER BY resilience_score DESC LIMIT 100
		) top100
		JOIN tracts t ON t.tract_fips = top100.tract_fips
		WHERE t.gq_correctional_pct >= ${THRESHOLDS.PRISON}
	`;
	console.log(`\n⚠️  Prison tracts in TOP 100 resilient: ${prisonInTop100.count}`);

	// 2. MILITARY TRACTS
	console.log('\n═══════════════════════════════════════════════════════════════════');
	console.log('2. MILITARY TRACTS (≥25% in military quarters)');
	console.log('═══════════════════════════════════════════════════════════════════');

	const militaryTracts = await sql`
		SELECT tract_fips, state_abbr, total_pop, resilience_score, burden,
			   gq_military_pct
		FROM tracts
		WHERE gq_military_pct >= ${THRESHOLDS.MILITARY}
		ORDER BY resilience_score DESC
		LIMIT 50
	`;

	console.log(`Found: ${militaryTracts.length} tracts with ≥${THRESHOLDS.MILITARY}% military population\n`);

	if (militaryTracts.length > 0) {
		console.log('Top 10 by resilience score:');
		console.log('─'.repeat(80));
		console.log('FIPS        | State | Pop    | Score  | Military%');
		console.log('─'.repeat(80));
		militaryTracts.slice(0, 10).forEach((t) => {
			console.log(
				`${t.tract_fips} | ${t.state_abbr}    | ${String(t.total_pop).padStart(6)} | ${parseFloat(t.resilience_score).toFixed(2).padStart(6)} | ${parseFloat(t.gq_military_pct).toFixed(1)}%`
			);
		});
	}

	const [militaryInTop100] = await sql`
		SELECT COUNT(*) as count FROM (
			SELECT tract_fips FROM tracts ORDER BY resilience_score DESC LIMIT 100
		) top100
		JOIN tracts t ON t.tract_fips = top100.tract_fips
		WHERE t.gq_military_pct >= ${THRESHOLDS.MILITARY}
	`;
	console.log(`\n⚠️  Military tracts in TOP 100 resilient: ${militaryInTop100.count}`);

	// 3. COLLEGE TRACTS
	console.log('\n═══════════════════════════════════════════════════════════════════');
	console.log('3. COLLEGE/UNIVERSITY TRACTS (≥50% in college dorms)');
	console.log('═══════════════════════════════════════════════════════════════════');

	const collegeTracts = await sql`
		SELECT tract_fips, state_abbr, total_pop, resilience_score, burden,
			   gq_college_pct
		FROM tracts
		WHERE gq_college_pct >= ${THRESHOLDS.COLLEGE}
		ORDER BY resilience_score DESC
		LIMIT 50
	`;

	console.log(`Found: ${collegeTracts.length} tracts with ≥${THRESHOLDS.COLLEGE}% college population\n`);

	if (collegeTracts.length > 0) {
		console.log('Top 10 by resilience score:');
		console.log('─'.repeat(80));
		console.log('FIPS        | State | Pop    | Score  | College%');
		console.log('─'.repeat(80));
		collegeTracts.slice(0, 10).forEach((t) => {
			console.log(
				`${t.tract_fips} | ${t.state_abbr}    | ${String(t.total_pop).padStart(6)} | ${parseFloat(t.resilience_score).toFixed(2).padStart(6)} | ${parseFloat(t.gq_college_pct).toFixed(1)}%`
			);
		});
	}

	const [collegeInTop100] = await sql`
		SELECT COUNT(*) as count FROM (
			SELECT tract_fips FROM tracts ORDER BY resilience_score DESC LIMIT 100
		) top100
		JOIN tracts t ON t.tract_fips = top100.tract_fips
		WHERE t.gq_college_pct >= ${THRESHOLDS.COLLEGE}
	`;
	console.log(`\n⚠️  College tracts in TOP 100 resilient: ${collegeInTop100.count}`);

	// 4. NURSING HOME TRACTS
	console.log('\n═══════════════════════════════════════════════════════════════════');
	console.log('4. NURSING HOME TRACTS (≥50% in nursing facilities)');
	console.log('═══════════════════════════════════════════════════════════════════');

	const nursingTracts = await sql`
		SELECT tract_fips, state_abbr, total_pop, resilience_score, burden,
			   gq_nursing_pct
		FROM tracts
		WHERE gq_nursing_pct >= ${THRESHOLDS.NURSING}
		ORDER BY resilience_score DESC
		LIMIT 50
	`;

	console.log(`Found: ${nursingTracts.length} tracts with ≥${THRESHOLDS.NURSING}% nursing home population\n`);

	if (nursingTracts.length > 0) {
		console.log('Top 10 by resilience score:');
		console.log('─'.repeat(80));
		console.log('FIPS        | State | Pop    | Score  | Nursing%');
		console.log('─'.repeat(80));
		nursingTracts.slice(0, 10).forEach((t) => {
			console.log(
				`${t.tract_fips} | ${t.state_abbr}    | ${String(t.total_pop).padStart(6)} | ${parseFloat(t.resilience_score).toFixed(2).padStart(6)} | ${parseFloat(t.gq_nursing_pct).toFixed(1)}%`
			);
		});
	}

	// 5. ZERO POPULATION TRACTS
	console.log('\n═══════════════════════════════════════════════════════════════════');
	console.log('5. ZERO POPULATION TRACTS');
	console.log('═══════════════════════════════════════════════════════════════════');

	const zeroPopTracts = await sql`
		SELECT tract_fips, state_abbr, total_pop, resilience_score, burden
		FROM tracts
		WHERE total_pop = 0 OR total_pop IS NULL
		ORDER BY resilience_score DESC
		LIMIT 50
	`;

	const [zeroPopTotal] = await sql`
		SELECT COUNT(*) as count FROM tracts WHERE total_pop = 0 OR total_pop IS NULL
	`;

	console.log(`Found: ${zeroPopTotal.count} tracts with zero population\n`);

	if (zeroPopTracts.length > 0) {
		console.log('Top 10 by resilience score (THESE SHOULD DEFINITELY BE FILTERED):');
		console.log('─'.repeat(60));
		console.log('FIPS        | State | Pop | Score');
		console.log('─'.repeat(60));
		zeroPopTracts.slice(0, 10).forEach((t) => {
			console.log(
				`${t.tract_fips} | ${t.state_abbr}    | ${t.total_pop ?? 0} | ${parseFloat(t.resilience_score).toFixed(2)}`
			);
		});
	}

	const [zeroPopInTop100] = await sql`
		SELECT COUNT(*) as count FROM (
			SELECT tract_fips FROM tracts ORDER BY resilience_score DESC LIMIT 100
		) top100
		JOIN tracts t ON t.tract_fips = top100.tract_fips
		WHERE t.total_pop = 0 OR t.total_pop IS NULL
	`;
	console.log(`\n⚠️  Zero-pop tracts in TOP 100 resilient: ${zeroPopInTop100.count}`);

	// 6. SMALL POPULATION TRACTS
	console.log('\n═══════════════════════════════════════════════════════════════════');
	console.log('6. VERY SMALL POPULATION TRACTS (<100 residents)');
	console.log('═══════════════════════════════════════════════════════════════════');

	const [smallPopTotal] = await sql`
		SELECT COUNT(*) as count FROM tracts
		WHERE total_pop > 0 AND total_pop < ${THRESHOLDS.SMALL_POP}
	`;

	const [smallPopInTop100] = await sql`
		SELECT COUNT(*) as count FROM (
			SELECT tract_fips FROM tracts ORDER BY resilience_score DESC LIMIT 100
		) top100
		JOIN tracts t ON t.tract_fips = top100.tract_fips
		WHERE t.total_pop > 0 AND t.total_pop < ${THRESHOLDS.SMALL_POP}
	`;

	console.log(`Found: ${smallPopTotal.count} tracts with 1-99 residents`);
	console.log(`⚠️  Small-pop tracts in TOP 100 resilient: ${smallPopInTop100.count}`);

	// 7. SUMMARY: TOP 100 ANALYSIS
	console.log('\n╔══════════════════════════════════════════════════════════════════╗');
	console.log('║                    TOP 100 RESILIENT ANALYSIS                    ║');
	console.log('╚══════════════════════════════════════════════════════════════════╝\n');

	const top100 = await sql`
		SELECT tract_fips, state_abbr, total_pop, resilience_score, burden,
			   gq_college_pct, gq_military_pct, gq_correctional_pct, gq_nursing_pct
		FROM tracts
		ORDER BY resilience_score DESC
		LIMIT 100
	`;

	let problemCount = 0;
	const issues: TractAnalysis[] = [];

	top100.forEach((t) => {
		const tractIssues: string[] = [];

		if (t.total_pop === 0 || t.total_pop === null) {
			tractIssues.push('ZERO_POP');
		} else if (t.total_pop < THRESHOLDS.SMALL_POP) {
			tractIssues.push('SMALL_POP');
		}

		if (parseFloat(t.gq_correctional_pct) >= THRESHOLDS.PRISON) {
			tractIssues.push('PRISON');
		}
		if (parseFloat(t.gq_military_pct) >= THRESHOLDS.MILITARY) {
			tractIssues.push('MILITARY');
		}
		if (parseFloat(t.gq_college_pct) >= THRESHOLDS.COLLEGE) {
			tractIssues.push('COLLEGE');
		}
		if (parseFloat(t.gq_nursing_pct) >= THRESHOLDS.NURSING) {
			tractIssues.push('NURSING');
		}

		if (tractIssues.length > 0) {
			problemCount++;
			issues.push({
				...t,
				issue: tractIssues.join(', '),
			});
		}
	});

	console.log(`PROBLEMATIC TRACTS IN TOP 100: ${problemCount}/100\n`);

	if (issues.length > 0) {
		console.log('Tracts that should be filtered from "Most Resilient" display:');
		console.log('─'.repeat(110));
		console.log('Rank | FIPS        | State | Pop    | Score  | Issue');
		console.log('─'.repeat(110));

		issues.forEach((t, idx) => {
			const rank = top100.findIndex((x) => x.tract_fips === t.tract_fips) + 1;
			console.log(
				`${String(rank).padStart(4)} | ${t.tract_fips} | ${t.state_abbr}    | ${String(t.total_pop ?? 0).padStart(6)} | ${parseFloat(t.resilience_score as unknown as string).toFixed(2).padStart(6)} | ${t.issue}`
			);
		});
	}

	// 8. RECOMMENDED FILTER
	console.log('\n╔══════════════════════════════════════════════════════════════════╗');
	console.log('║                 RECOMMENDED FILTERING CRITERIA                   ║');
	console.log('╚══════════════════════════════════════════════════════════════════╝\n');

	const [wouldFilter] = await sql`
		SELECT COUNT(*) as count FROM tracts
		WHERE total_pop < ${THRESHOLDS.SMALL_POP}
		   OR gq_correctional_pct >= ${THRESHOLDS.PRISON}
		   OR gq_military_pct >= ${THRESHOLDS.MILITARY}
	`;

	const [residential] = await sql`
		SELECT COUNT(*) as count FROM tracts
		WHERE total_pop >= ${THRESHOLDS.SMALL_POP}
		  AND gq_correctional_pct < ${THRESHOLDS.PRISON}
		  AND gq_military_pct < ${THRESHOLDS.MILITARY}
	`;

	console.log('Proposed is_residential = FALSE criteria:');
	console.log(`  - Population < ${THRESHOLDS.SMALL_POP}`);
	console.log(`  - OR gq_correctional_pct >= ${THRESHOLDS.PRISON}%`);
	console.log(`  - OR gq_military_pct >= ${THRESHOLDS.MILITARY}%`);
	console.log('');
	console.log(`Tracts to EXCLUDE: ${parseInt(wouldFilter.count).toLocaleString()}`);
	console.log(`Tracts to KEEP (is_residential = TRUE): ${parseInt(residential.count).toLocaleString()}`);
	console.log(`Percentage kept: ${((parseInt(residential.count) / parseInt(totalCount.count)) * 100).toFixed(1)}%`);

	// 9. SQL FOR MIGRATION
	console.log('\n╔══════════════════════════════════════════════════════════════════╗');
	console.log('║              SQL FOR MIGRATION (copy this to migrate script)    ║');
	console.log('╚══════════════════════════════════════════════════════════════════╝\n');

	console.log(`-- Add is_residential column
ALTER TABLE tracts ADD COLUMN IF NOT EXISTS is_residential BOOLEAN DEFAULT TRUE;

-- Add tract_type column for categorization
ALTER TABLE tracts ADD COLUMN IF NOT EXISTS tract_type VARCHAR(20) DEFAULT 'residential';

-- Update non-residential tracts
UPDATE tracts SET
  is_residential = FALSE,
  tract_type = CASE
    WHEN total_pop < ${THRESHOLDS.SMALL_POP} THEN 'small_pop'
    WHEN gq_correctional_pct >= ${THRESHOLDS.PRISON} THEN 'correctional'
    WHEN gq_military_pct >= ${THRESHOLDS.MILITARY} THEN 'military'
    ELSE 'other'
  END
WHERE total_pop < ${THRESHOLDS.SMALL_POP}
   OR gq_correctional_pct >= ${THRESHOLDS.PRISON}
   OR gq_military_pct >= ${THRESHOLDS.MILITARY};

-- Create index for efficient filtering
CREATE INDEX IF NOT EXISTS idx_tracts_residential ON tracts(is_residential) WHERE is_residential = TRUE;
`);

	await sql.end();
	console.log('\nAnalysis complete.');
}

analyze().catch((e) => {
	console.error('Analysis failed:', e);
	process.exit(1);
});
