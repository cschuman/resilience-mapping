import { sql } from '$lib/server/db';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	// Get Columbus (Franklin County) top tracts
	const columbusTop = await sql`
		SELECT
			tract_fips, county, total_pop,
			ROUND(resilience_score::numeric, 3) as resilience_score,
			ROUND(burden::numeric, 3) as burden
		FROM tracts
		WHERE county = 'Franklin' AND state_abbr = 'OH'
		ORDER BY resilience_score DESC
		LIMIT 10
	`;

	// Get Cleveland (Cuyahoga County) bottom tracts
	const clevelandBottom = await sql`
		SELECT
			tract_fips, county, total_pop,
			ROUND(resilience_score::numeric, 3) as resilience_score,
			ROUND(burden::numeric, 3) as burden
		FROM tracts
		WHERE county = 'Cuyahoga' AND state_abbr = 'OH'
		ORDER BY resilience_score ASC
		LIMIT 10
	`;

	// Get county averages for comparison
	const countyStats = await sql`
		SELECT
			county,
			COUNT(*) as tract_count,
			ROUND(AVG(resilience_score)::numeric, 3) as avg_resilience,
			ROUND(AVG(burden)::numeric, 3) as avg_burden,
			ROUND(MIN(resilience_score)::numeric, 3) as min_resilience,
			ROUND(MAX(resilience_score)::numeric, 3) as max_resilience,
			SUM(total_pop) as total_pop
		FROM tracts
		WHERE state_abbr = 'OH' AND county IN ('Franklin', 'Cuyahoga')
		GROUP BY county
	`;

	// Get Ohio overall stats
	const ohioStats = await sql`
		SELECT
			COUNT(*) as tract_count,
			ROUND(AVG(resilience_score)::numeric, 3) as avg_resilience,
			ROUND(AVG(burden)::numeric, 3) as avg_burden,
			SUM(total_pop) as total_pop
		FROM tracts
		WHERE state_abbr = 'OH'
	`;

	const franklin = countyStats.find(c => c.county === 'Franklin');
	const cuyahoga = countyStats.find(c => c.county === 'Cuyahoga');

	return {
		columbus: {
			topTracts: columbusTop.map(t => ({
				fips: t.tract_fips,
				population: parseInt(t.total_pop),
				resilience: parseFloat(t.resilience_score),
				burden: parseFloat(t.burden)
			})),
			stats: franklin ? {
				tractCount: parseInt(franklin.tract_count),
				avgResilience: parseFloat(franklin.avg_resilience),
				avgBurden: parseFloat(franklin.avg_burden),
				minResilience: parseFloat(franklin.min_resilience),
				maxResilience: parseFloat(franklin.max_resilience),
				population: parseInt(franklin.total_pop)
			} : null
		},
		cleveland: {
			bottomTracts: clevelandBottom.map(t => ({
				fips: t.tract_fips,
				population: parseInt(t.total_pop),
				resilience: parseFloat(t.resilience_score),
				burden: parseFloat(t.burden)
			})),
			stats: cuyahoga ? {
				tractCount: parseInt(cuyahoga.tract_count),
				avgResilience: parseFloat(cuyahoga.avg_resilience),
				avgBurden: parseFloat(cuyahoga.avg_burden),
				minResilience: parseFloat(cuyahoga.min_resilience),
				maxResilience: parseFloat(cuyahoga.max_resilience),
				population: parseInt(cuyahoga.total_pop)
			} : null
		},
		ohio: ohioStats[0] ? {
			tractCount: parseInt(ohioStats[0].tract_count),
			avgResilience: parseFloat(ohioStats[0].avg_resilience),
			avgBurden: parseFloat(ohioStats[0].avg_burden),
			population: parseInt(ohioStats[0].total_pop)
		} : null
	};
};
