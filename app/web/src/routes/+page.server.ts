import { sql } from '$lib/server/db';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	const [stats] = await sql`
		SELECT
			COUNT(*) as total_tracts,
			AVG(resilience_score) as avg_resilience,
			MAX(resilience_score) as max_resilience,
			SUM(total_pop) as total_population
		FROM tracts
		WHERE resilience_score > 0
	`;

	const topTracts = await sql`
		SELECT tract_fips, state_abbr, resilience_score, total_pop
		FROM tracts
		WHERE resilience_score > 0
		ORDER BY resilience_score DESC
		LIMIT 10
	`;

	const stateCount = await sql`
		SELECT COUNT(DISTINCT state_abbr) as count FROM tracts
	`;

	return {
		stats: {
			totalTracts: parseInt(stats.total_tracts),
			avgResilience: parseFloat(stats.avg_resilience).toFixed(3),
			maxResilience: parseFloat(stats.max_resilience).toFixed(3),
			totalPopulation: parseInt(stats.total_population),
			stateCount: parseInt(stateCount[0].count)
		},
		topTracts: topTracts.map((t) => ({
			fips: t.tract_fips,
			state: t.state_abbr,
			score: parseFloat(t.resilience_score).toFixed(3),
			population: t.total_pop
		}))
	};
};
