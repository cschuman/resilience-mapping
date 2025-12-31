import { sql } from '$lib/server/db';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	// Get special population summary stats
	const specialStats = await sql`
		SELECT
			tract_type,
			COUNT(*) as tract_count,
			ROUND(AVG(resilience_score)::numeric, 3) as avg_resilience,
			ROUND(AVG(burden)::numeric, 3) as avg_burden,
			SUM(total_pop) as total_pop
		FROM tracts
		WHERE tract_type IN ('college', 'military', 'correctional')
		GROUP BY tract_type
		ORDER BY avg_resilience DESC
	`;

	// Get college tract details
	const collegeTracts = await sql`
		SELECT
			tract_fips, state_abbr, county, total_pop,
			ROUND(resilience_score::numeric, 3) as resilience_score,
			ROUND(burden::numeric, 3) as burden,
			ROUND(gq_college_pct::numeric, 1) as college_pct
		FROM tracts
		WHERE tract_type = 'college'
		ORDER BY resilience_score DESC
	`;

	// Get military tract details
	const militaryTracts = await sql`
		SELECT
			tract_fips, state_abbr, county, total_pop,
			ROUND(resilience_score::numeric, 3) as resilience_score,
			ROUND(burden::numeric, 3) as burden,
			ROUND(gq_military_pct::numeric, 1) as military_pct
		FROM tracts
		WHERE tract_type = 'military'
		ORDER BY resilience_score DESC
	`;

	// Get correctional tract details
	const correctionalTracts = await sql`
		SELECT
			tract_fips, state_abbr, county, total_pop,
			ROUND(resilience_score::numeric, 3) as resilience_score,
			ROUND(burden::numeric, 3) as burden,
			ROUND(gq_correctional_pct::numeric, 1) as correctional_pct
		FROM tracts
		WHERE tract_type = 'correctional'
		ORDER BY resilience_score DESC
	`;

	// Calculate the gap between college and correctional
	const collegeAvg = specialStats.find(s => s.tract_type === 'college');
	const correctionalAvg = specialStats.find(s => s.tract_type === 'correctional');
	const resilienceGap = collegeAvg && correctionalAvg
		? parseFloat(collegeAvg.avg_resilience) - parseFloat(correctionalAvg.avg_resilience)
		: 0;

	return {
		summary: {
			college: collegeAvg ? {
				count: parseInt(collegeAvg.tract_count),
				avgResilience: parseFloat(collegeAvg.avg_resilience),
				avgBurden: parseFloat(collegeAvg.avg_burden),
				population: parseInt(collegeAvg.total_pop)
			} : null,
			military: specialStats.find(s => s.tract_type === 'military') ? {
				count: parseInt(specialStats.find(s => s.tract_type === 'military')!.tract_count),
				avgResilience: parseFloat(specialStats.find(s => s.tract_type === 'military')!.avg_resilience),
				avgBurden: parseFloat(specialStats.find(s => s.tract_type === 'military')!.avg_burden),
				population: parseInt(specialStats.find(s => s.tract_type === 'military')!.total_pop)
			} : null,
			correctional: correctionalAvg ? {
				count: parseInt(correctionalAvg.tract_count),
				avgResilience: parseFloat(correctionalAvg.avg_resilience),
				avgBurden: parseFloat(correctionalAvg.avg_burden),
				population: parseInt(correctionalAvg.total_pop)
			} : null,
			resilienceGap: Math.round(resilienceGap * 100) / 100
		},
		collegeTracts: collegeTracts.map(t => ({
			fips: t.tract_fips,
			state: t.state_abbr,
			county: t.county,
			population: parseInt(t.total_pop),
			resilience: parseFloat(t.resilience_score),
			burden: parseFloat(t.burden),
			collegePct: parseFloat(t.college_pct)
		})),
		militaryTracts: militaryTracts.map(t => ({
			fips: t.tract_fips,
			state: t.state_abbr,
			county: t.county,
			population: parseInt(t.total_pop),
			resilience: parseFloat(t.resilience_score),
			burden: parseFloat(t.burden),
			militaryPct: parseFloat(t.military_pct)
		})),
		correctionalTracts: correctionalTracts.map(t => ({
			fips: t.tract_fips,
			state: t.state_abbr,
			county: t.county,
			population: parseInt(t.total_pop),
			resilience: parseFloat(t.resilience_score),
			burden: parseFloat(t.burden),
			correctionalPct: parseFloat(t.correctional_pct)
		}))
	};
};
