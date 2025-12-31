import { json } from '@sveltejs/kit';
import { sql } from '$lib/server/db';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
	// By default, only include residential tracts in stats
	// Set include_all=true to include non-residential tracts (for research purposes)
	const includeAll = url.searchParams.get('include_all') === 'true';

	let stats;
	let stateStats;
	let distribution;

	if (includeAll) {
		// Use direct queries for include_all (less common, research use)
		[stats] = await sql`
			SELECT
				COUNT(*) as total_tracts,
				AVG(resilience_score) as avg_resilience,
				MIN(resilience_score) as min_resilience,
				MAX(resilience_score) as max_resilience,
				SUM(total_pop) as total_population
			FROM tracts
			WHERE resilience_score IS NOT NULL
		`;

		stateStats = await sql`
			SELECT
				state_abbr,
				COUNT(*) as tract_count,
				AVG(resilience_score) as avg_resilience,
				SUM(total_pop) as population
			FROM tracts
			WHERE resilience_score IS NOT NULL
			GROUP BY state_abbr
			ORDER BY avg_resilience DESC
		`;

		distribution = await sql`
			SELECT
				width_bucket(resilience_score, -4, 4, 20) as bucket,
				COUNT(*) as count
			FROM tracts
			WHERE resilience_score IS NOT NULL
				AND resilience_score BETWEEN -4 AND 4
			GROUP BY bucket
			ORDER BY bucket
		`;
	} else {
		// Use materialized views for residential-only (common case, faster)
		[stats] = await sql`
			SELECT
				residential_tracts as total_tracts,
				avg_resilience,
				min_resilience,
				max_resilience,
				total_population
			FROM mv_overall_stats
			WHERE category = 'all'
		`;

		stateStats = await sql`
			SELECT
				state_abbr,
				residential_count as tract_count,
				avg_resilience,
				total_population as population
			FROM mv_state_stats
			ORDER BY avg_resilience DESC
		`;

		distribution = await sql`
			SELECT bucket, residential_count as count
			FROM mv_score_distribution
			ORDER BY bucket
		`;
	}

	// Convert to array with all buckets (fill in zeros)
	const buckets = Array(20).fill(0);
	distribution.forEach((d) => {
		const idx = parseInt(d.bucket) - 1;
		if (idx >= 0 && idx < 20) {
			buckets[idx] = parseInt(d.count);
		}
	});

	return json({
		overview: {
			totalTracts: parseInt(stats.total_tracts),
			avgResilience: parseFloat(stats.avg_resilience).toFixed(3),
			minResilience: parseFloat(stats.min_resilience).toFixed(3),
			maxResilience: parseFloat(stats.max_resilience).toFixed(3),
			totalPopulation: parseInt(stats.total_population)
		},
		distribution: {
			buckets,
			min: -4,
			max: 4,
			bucketWidth: 0.4
		},
		byState: stateStats.map((s) => ({
			state: s.state_abbr,
			tractCount: parseInt(s.tract_count),
			avgResilience: parseFloat(s.avg_resilience).toFixed(3),
			population: parseInt(s.population)
		})),
		filters: {
			includeAll,
			residentialOnly: !includeAll,
			note: includeAll
				? 'Includes all tracts (residential and non-residential)'
				: 'Excludes non-residential tracts (prisons, military bases, zero-population areas)'
		}
	});
};
