import { json, error } from '@sveltejs/kit';
import { sql } from '$lib/server/db';
import type { RequestHandler } from './$types';

/**
 * GET /api/predictions/[fips]
 *
 * Returns the trajectory prediction for a specific tract.
 *
 * Response:
 * - tractFips: Census tract FIPS code
 * - predictedTrajectory: "DECLINE" | "STABLE" | "IMPROVE"
 * - probabilities: { decline, stable, improve }
 * - confidence: 0-1 (highest probability)
 * - interpretation: Human-readable description
 */
export const GET: RequestHandler = async ({ params }) => {
	const { fips } = params;

	const [prediction] = await sql`
		SELECT
			tract_fips,
			state_abbr,
			predicted_trajectory,
			prob_decline,
			prob_improve,
			prob_stable,
			confidence,
			prediction_date,
			model_version
		FROM tract_predictions
		WHERE tract_fips = ${fips}
	`;

	if (!prediction) {
		throw error(404, 'Prediction not found for this tract');
	}

	// Generate interpretation
	const trajectory = prediction.predicted_trajectory;
	const confidence = parseFloat(prediction.confidence);
	const confidenceLevel = confidence >= 0.7 ? 'high' : confidence >= 0.5 ? 'moderate' : 'low';

	let interpretation: string;
	switch (trajectory) {
		case 'DECLINE':
			interpretation = `This community is predicted to experience declining health outcomes over the next 12-24 months (${confidenceLevel} confidence). Preventive interventions may help reverse this trend.`;
			break;
		case 'IMPROVE':
			interpretation = `This community is predicted to see improving health outcomes over the next 12-24 months (${confidenceLevel} confidence). Current positive trends should be supported and sustained.`;
			break;
		case 'STABLE':
		default:
			interpretation = `This community is predicted to maintain stable health outcomes over the next 12-24 months (${confidenceLevel} confidence).`;
	}

	return json({
		tractFips: prediction.tract_fips,
		state: prediction.state_abbr,
		predictedTrajectory: trajectory,
		probabilities: {
			decline: parseFloat(prediction.prob_decline),
			improve: parseFloat(prediction.prob_improve),
			stable: parseFloat(prediction.prob_stable)
		},
		confidence,
		confidenceLevel,
		interpretation,
		predictionDate: prediction.prediction_date,
		modelVersion: prediction.model_version
	});
};
