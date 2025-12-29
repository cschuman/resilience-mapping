import { sql } from '$lib/server/db';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
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

	return {
		distribution: buckets
	};
};
