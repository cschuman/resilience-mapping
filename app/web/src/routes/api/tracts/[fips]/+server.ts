import { json, error } from '@sveltejs/kit';
import { sql } from '$lib/server/db';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ params }) => {
	const { fips } = params;

	const [tract] = await sql`
		SELECT tract_fips, state_abbr, total_pop, resilience_score, burden,
			   gq_college_pct, gq_military_pct, gq_correctional_pct, gq_nursing_pct,
			   created_at
		FROM tracts
		WHERE tract_fips = ${fips}
	`;

	if (!tract) {
		throw error(404, 'Tract not found');
	}

	// Get percentile ranking
	const [ranking] = await sql`
		SELECT
			(SELECT COUNT(*) FROM tracts WHERE resilience_score < ${tract.resilience_score}) * 100.0 /
			(SELECT COUNT(*) FROM tracts) as percentile
	`;

	return json({
		tractFips: tract.tract_fips,
		state: tract.state_abbr,
		population: tract.total_pop,
		resilienceScore: parseFloat(tract.resilience_score),
		burden: parseFloat(tract.burden),
		percentile: parseFloat(ranking.percentile).toFixed(1),
		groupQuarters: {
			college: parseFloat(tract.gq_college_pct),
			military: parseFloat(tract.gq_military_pct),
			correctional: parseFloat(tract.gq_correctional_pct),
			nursing: parseFloat(tract.gq_nursing_pct)
		}
	});
};
