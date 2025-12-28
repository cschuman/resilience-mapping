import { json } from '@sveltejs/kit';
import { sql } from '$lib/server/db';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async () => {
	const [stats] = await sql`
		SELECT
			COUNT(*) as total_tracts,
			AVG(resilience_score) as avg_resilience,
			MIN(resilience_score) as min_resilience,
			MAX(resilience_score) as max_resilience,
			SUM(total_pop) as total_population
		FROM tracts
		WHERE resilience_score > 0
	`;

	const stateStats = await sql`
		SELECT
			state_abbr,
			COUNT(*) as tract_count,
			AVG(resilience_score) as avg_resilience,
			SUM(total_pop) as population
		FROM tracts
		WHERE resilience_score > 0
		GROUP BY state_abbr
		ORDER BY avg_resilience DESC
	`;

	return json({
		overview: {
			totalTracts: parseInt(stats.total_tracts),
			avgResilience: parseFloat(stats.avg_resilience).toFixed(3),
			minResilience: parseFloat(stats.min_resilience).toFixed(3),
			maxResilience: parseFloat(stats.max_resilience).toFixed(3),
			totalPopulation: parseInt(stats.total_population)
		},
		byState: stateStats.map((s) => ({
			state: s.state_abbr,
			tractCount: parseInt(s.tract_count),
			avgResilience: parseFloat(s.avg_resilience).toFixed(3),
			population: parseInt(s.population)
		}))
	});
};
