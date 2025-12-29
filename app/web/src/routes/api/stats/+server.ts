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
		WHERE resilience_score IS NOT NULL
	`;

	const stateStats = await sql`
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

	// Score distribution histogram (20 buckets from -4 to +4)
	const distribution = await sql`
		SELECT
			width_bucket(resilience_score, -4, 4, 20) as bucket,
			COUNT(*) as count
		FROM tracts
		WHERE resilience_score IS NOT NULL
			AND resilience_score BETWEEN -4 AND 4
		GROUP BY bucket
		ORDER BY bucket
	`;

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
		}))
	});
};
