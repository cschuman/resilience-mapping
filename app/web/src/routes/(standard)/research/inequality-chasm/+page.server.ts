import { sql } from '$lib/server/db';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	// Get counties with widest internal gaps (at least 10 tracts for reliability)
	const widestGaps = await sql`
		SELECT
			county, state_abbr,
			COUNT(*) as tract_count,
			ROUND(AVG(resilience_score)::numeric, 3) as avg_resilience,
			ROUND(MIN(resilience_score)::numeric, 3) as min_resilience,
			ROUND(MAX(resilience_score)::numeric, 3) as max_resilience,
			ROUND((MAX(resilience_score) - MIN(resilience_score))::numeric, 2) as internal_range,
			SUM(total_pop) as total_pop
		FROM tracts
		WHERE tract_type = 'residential'
		GROUP BY county, state_abbr
		HAVING COUNT(*) >= 10
		ORDER BY (MAX(resilience_score) - MIN(resilience_score)) DESC
		LIMIT 20
	`;

	// Get detailed tract data for top 3 counties with widest gaps
	const topCounties = widestGaps.slice(0, 5);
	const countyDetails = [];

	for (const county of topCounties) {
		const best = await sql`
			SELECT
				tract_fips, total_pop,
				ROUND(resilience_score::numeric, 3) as resilience_score,
				ROUND(burden::numeric, 3) as burden
			FROM tracts
			WHERE county = ${county.county} AND state_abbr = ${county.state_abbr}
			ORDER BY resilience_score DESC
			LIMIT 5
		`;

		const worst = await sql`
			SELECT
				tract_fips, total_pop,
				ROUND(resilience_score::numeric, 3) as resilience_score,
				ROUND(burden::numeric, 3) as burden
			FROM tracts
			WHERE county = ${county.county} AND state_abbr = ${county.state_abbr}
			ORDER BY resilience_score ASC
			LIMIT 5
		`;

		countyDetails.push({
			county: county.county,
			state: county.state_abbr,
			tractCount: parseInt(county.tract_count),
			avgResilience: parseFloat(county.avg_resilience),
			minResilience: parseFloat(county.min_resilience),
			maxResilience: parseFloat(county.max_resilience),
			internalRange: parseFloat(county.internal_range),
			population: parseInt(county.total_pop),
			bestTracts: best.map(t => ({
				fips: t.tract_fips,
				population: parseInt(t.total_pop),
				resilience: parseFloat(t.resilience_score),
				burden: parseFloat(t.burden)
			})),
			worstTracts: worst.map(t => ({
				fips: t.tract_fips,
				population: parseInt(t.total_pop),
				resilience: parseFloat(t.resilience_score),
				burden: parseFloat(t.burden)
			}))
		});
	}

	return {
		widestGaps: widestGaps.map(c => ({
			county: c.county,
			state: c.state_abbr,
			tractCount: parseInt(c.tract_count),
			avgResilience: parseFloat(c.avg_resilience),
			minResilience: parseFloat(c.min_resilience),
			maxResilience: parseFloat(c.max_resilience),
			internalRange: parseFloat(c.internal_range),
			population: parseInt(c.total_pop)
		})),
		countyDetails
	};
};
