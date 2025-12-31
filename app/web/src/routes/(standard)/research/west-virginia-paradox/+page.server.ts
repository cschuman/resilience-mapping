import { sql } from '$lib/server/db';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	// Get West Virginia overall stats
	const wvStats = await sql`
		SELECT
			COUNT(*) as tract_count,
			ROUND(AVG(resilience_score)::numeric, 3) as avg_resilience,
			ROUND(AVG(burden)::numeric, 3) as avg_burden,
			ROUND(STDDEV(resilience_score)::numeric, 3) as std_resilience,
			SUM(total_pop) as total_pop
		FROM tracts
		WHERE state_abbr = 'WV'
	`;

	// Get state-level comparison (burden vs resilience)
	const stateComparison = await sql`
		SELECT
			state_abbr,
			ROUND(AVG(resilience_score)::numeric, 3) as avg_resilience,
			ROUND(AVG(burden)::numeric, 3) as avg_burden,
			SUM(total_pop) as total_pop
		FROM tracts
		GROUP BY state_abbr
		ORDER BY avg_burden DESC
		LIMIT 15
	`;

	// Get WV county breakdown
	const wvCounties = await sql`
		SELECT
			county,
			COUNT(*) as tract_count,
			ROUND(AVG(resilience_score)::numeric, 3) as avg_resilience,
			ROUND(AVG(burden)::numeric, 3) as avg_burden,
			SUM(total_pop) as total_pop
		FROM tracts
		WHERE state_abbr = 'WV'
		GROUP BY county
		ORDER BY avg_resilience DESC
	`;

	// Get WV's most resilient tracts
	const wvTopTracts = await sql`
		SELECT
			tract_fips, county, total_pop,
			ROUND(resilience_score::numeric, 3) as resilience_score,
			ROUND(burden::numeric, 3) as burden
		FROM tracts
		WHERE state_abbr = 'WV'
		ORDER BY resilience_score DESC
		LIMIT 10
	`;

	// Get WV's least resilient tracts
	const wvBottomTracts = await sql`
		SELECT
			tract_fips, county, total_pop,
			ROUND(resilience_score::numeric, 3) as resilience_score,
			ROUND(burden::numeric, 3) as burden
		FROM tracts
		WHERE state_abbr = 'WV'
		ORDER BY resilience_score ASC
		LIMIT 10
	`;

	return {
		westVirginia: wvStats[0] ? {
			tractCount: parseInt(wvStats[0].tract_count),
			avgResilience: parseFloat(wvStats[0].avg_resilience),
			avgBurden: parseFloat(wvStats[0].avg_burden),
			stdResilience: parseFloat(wvStats[0].std_resilience),
			population: parseInt(wvStats[0].total_pop)
		} : null,
		stateComparison: stateComparison.map(s => ({
			state: s.state_abbr,
			avgResilience: parseFloat(s.avg_resilience),
			avgBurden: parseFloat(s.avg_burden),
			population: parseInt(s.total_pop)
		})),
		counties: wvCounties.map(c => ({
			county: c.county,
			tractCount: parseInt(c.tract_count),
			avgResilience: parseFloat(c.avg_resilience),
			avgBurden: parseFloat(c.avg_burden),
			population: parseInt(c.total_pop)
		})),
		topTracts: wvTopTracts.map(t => ({
			fips: t.tract_fips,
			county: t.county,
			population: parseInt(t.total_pop),
			resilience: parseFloat(t.resilience_score),
			burden: parseFloat(t.burden)
		})),
		bottomTracts: wvBottomTracts.map(t => ({
			fips: t.tract_fips,
			county: t.county,
			population: parseInt(t.total_pop),
			resilience: parseFloat(t.resilience_score),
			burden: parseFloat(t.burden)
		}))
	};
};
