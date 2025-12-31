import { json, error } from '@sveltejs/kit';
import { sql } from '$lib/server/db';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ params }) => {
	const { fips } = params;

	const [tract] = await sql`
		SELECT tract_fips, state_abbr, total_pop, resilience_score, burden,
			   gq_college_pct, gq_military_pct, gq_correctional_pct, gq_nursing_pct,
			   is_residential, tract_type, created_at
		FROM tracts
		WHERE tract_fips = ${fips}
	`;

	if (!tract) {
		throw error(404, 'Tract not found');
	}

	// Get percentile ranking (among residential tracts only for fair comparison)
	const [ranking] = await sql`
		SELECT
			(SELECT COUNT(*) FROM tracts WHERE resilience_score < ${tract.resilience_score} AND is_residential = TRUE) * 100.0 /
			NULLIF((SELECT COUNT(*) FROM tracts WHERE is_residential = TRUE), 0) as percentile
	`;

	// Get state ranking
	const [stateRanking] = await sql`
		SELECT
			(SELECT COUNT(*) FROM tracts
			 WHERE state_abbr = ${tract.state_abbr}
			   AND resilience_score > ${tract.resilience_score}
			   AND is_residential = TRUE) + 1 as rank,
			(SELECT COUNT(*) FROM tracts
			 WHERE state_abbr = ${tract.state_abbr}
			   AND is_residential = TRUE) as total
	`;

	return json({
		tractFips: tract.tract_fips,
		state: tract.state_abbr,
		population: tract.total_pop,
		resilienceScore: parseFloat(tract.resilience_score),
		burden: parseFloat(tract.burden),
		percentile: ranking.percentile ? parseFloat(ranking.percentile).toFixed(1) : null,
		stateRank: {
			rank: parseInt(stateRanking.rank),
			total: parseInt(stateRanking.total)
		},
		groupQuarters: {
			college: parseFloat(tract.gq_college_pct),
			military: parseFloat(tract.gq_military_pct),
			correctional: parseFloat(tract.gq_correctional_pct),
			nursing: parseFloat(tract.gq_nursing_pct)
		},
		isResidential: tract.is_residential,
		tractType: tract.tract_type,
		dataQuality: {
			isResidential: tract.is_residential,
			tractType: tract.tract_type,
			warning: !tract.is_residential
				? `This tract is classified as "${tract.tract_type}" and is excluded from default rankings.`
				: null
		}
	});
};
