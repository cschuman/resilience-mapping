import { sql } from '$lib/server/db';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	// Get key statistics from materialized views
	const [stats] = await sql`
		SELECT
			residential_tracts,
			avg_resilience,
			median_resilience,
			p25_resilience,
			p75_resilience,
			total_population
		FROM mv_overall_stats
		WHERE category = 'all'
	`;

	// Get state count
	const [stateCount] = await sql`
		SELECT COUNT(*) as count FROM mv_state_stats
	`;

	// Get top and bottom states by average resilience
	const topStates = await sql`
		SELECT state_abbr, avg_resilience, residential_count, total_population
		FROM mv_state_stats
		ORDER BY avg_resilience DESC
		LIMIT 5
	`;

	const bottomStates = await sql`
		SELECT state_abbr, avg_resilience, residential_count, total_population
		FROM mv_state_stats
		ORDER BY avg_resilience ASC
		LIMIT 5
	`;

	return {
		stats: {
			totalTracts: parseInt(stats.residential_tracts),
			avgResilience: parseFloat(stats.avg_resilience),
			medianResilience: parseFloat(stats.median_resilience),
			p25: parseFloat(stats.p25_resilience),
			p75: parseFloat(stats.p75_resilience),
			totalPopulation: parseInt(stats.total_population),
			stateCount: parseInt(stateCount.count)
		},
		topStates: topStates.map((s) => ({
			state: s.state_abbr,
			avgResilience: parseFloat(s.avg_resilience),
			tractCount: parseInt(s.residential_count),
			population: parseInt(s.total_population)
		})),
		bottomStates: bottomStates.map((s) => ({
			state: s.state_abbr,
			avgResilience: parseFloat(s.avg_resilience),
			tractCount: parseInt(s.residential_count),
			population: parseInt(s.total_population)
		}))
	};
};
