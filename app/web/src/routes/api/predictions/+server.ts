import { json } from '@sveltejs/kit';
import { sql } from '$lib/server/db';
import type { RequestHandler } from './$types';

/**
 * GET /api/predictions
 *
 * Returns summary statistics for trajectory predictions.
 * Optionally filter by state using ?state=XX query param.
 */
export const GET: RequestHandler = async ({ url }) => {
	const state = url.searchParams.get('state');

	// Get overall distribution
	const distribution = state
		? await sql`
				SELECT predicted_trajectory, COUNT(*) as count
				FROM tract_predictions
				WHERE state_abbr = ${state}
				GROUP BY predicted_trajectory
				ORDER BY count DESC
			`
		: await sql`
				SELECT predicted_trajectory, COUNT(*) as count
				FROM tract_predictions
				GROUP BY predicted_trajectory
				ORDER BY count DESC
			`;

	// Get total count
	const [totalResult] = state
		? await sql`SELECT COUNT(*) as count FROM tract_predictions WHERE state_abbr = ${state}`
		: await sql`SELECT COUNT(*) as count FROM tract_predictions`;

	const total = parseInt(totalResult.count);

	// Get high confidence predictions
	const [highConfResult] = state
		? await sql`
				SELECT COUNT(*) as count
				FROM tract_predictions
				WHERE confidence >= 0.6 AND state_abbr = ${state}
			`
		: await sql`
				SELECT COUNT(*) as count
				FROM tract_predictions
				WHERE confidence >= 0.6
			`;

	// Get top declining tracts
	const topDeclining = state
		? await sql`
				SELECT tract_fips, state_abbr, confidence
				FROM tract_predictions
				WHERE predicted_trajectory = 'DECLINE'
				  AND state_abbr = ${state}
				ORDER BY confidence DESC
				LIMIT 10
			`
		: await sql`
				SELECT tract_fips, state_abbr, confidence
				FROM tract_predictions
				WHERE predicted_trajectory = 'DECLINE'
				ORDER BY confidence DESC
				LIMIT 10
			`;

	// Get top improving tracts
	const topImproving = state
		? await sql`
				SELECT tract_fips, state_abbr, confidence
				FROM tract_predictions
				WHERE predicted_trajectory = 'IMPROVE'
				  AND state_abbr = ${state}
				ORDER BY confidence DESC
				LIMIT 10
			`
		: await sql`
				SELECT tract_fips, state_abbr, confidence
				FROM tract_predictions
				WHERE predicted_trajectory = 'IMPROVE'
				ORDER BY confidence DESC
				LIMIT 10
			`;

	// Format distribution
	const trajectoryDistribution: Record<string, { count: number; percentage: number }> = {};
	for (const row of distribution) {
		trajectoryDistribution[row.predicted_trajectory] = {
			count: parseInt(row.count),
			percentage: total > 0 ? (parseInt(row.count) / total) * 100 : 0
		};
	}

	return json({
		total,
		filter: state ? { state } : null,
		distribution: trajectoryDistribution,
		highConfidenceCount: parseInt(highConfResult.count),
		highConfidencePercentage: total > 0 ? (parseInt(highConfResult.count) / total) * 100 : 0,
		topDeclining: topDeclining.map((t) => ({
			tractFips: t.tract_fips,
			state: t.state_abbr,
			confidence: parseFloat(t.confidence)
		})),
		topImproving: topImproving.map((t) => ({
			tractFips: t.tract_fips,
			state: t.state_abbr,
			confidence: parseFloat(t.confidence)
		}))
	});
};
