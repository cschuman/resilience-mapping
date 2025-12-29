import { json, error } from '@sveltejs/kit';
import { sql } from '$lib/server/db';
import type { RequestHandler } from './$types';

/**
 * Allowed sort fields - whitelist to prevent SQL injection.
 */
const ALLOWED_SORT_FIELDS = [
	'resilience_score',
	'total_pop',
	'burden',
	'tract_fips',
	'state_abbr',
	'gq_college_pct',
	'gq_military_pct',
	'gq_correctional_pct',
	'gq_nursing_pct'
] as const;

type SortField = (typeof ALLOWED_SORT_FIELDS)[number];

/**
 * Validate and parse a float parameter with bounds.
 */
function parseFloatParam(
	value: string | null,
	defaultValue: number,
	min: number,
	max: number
): number {
	if (!value) return defaultValue;
	const parsed = parseFloat(value);
	if (isNaN(parsed) || !isFinite(parsed)) return defaultValue;
	return Math.max(min, Math.min(max, parsed));
}

/**
 * Validate and parse an integer parameter with bounds.
 */
function parseIntParam(
	value: string | null,
	defaultValue: number,
	min: number,
	max: number
): number {
	if (!value) return defaultValue;
	const parsed = parseInt(value, 10);
	if (isNaN(parsed)) return defaultValue;
	return Math.max(min, Math.min(max, parsed));
}

/**
 * Validate state abbreviation format.
 */
const STATE_PATTERN = /^[A-Z]{2}$/;

function validateState(state: string | null): string | null {
	if (!state) return null;
	const upper = state.toUpperCase();
	return STATE_PATTERN.test(upper) ? upper : null;
}

/**
 * Validate sort field against whitelist.
 */
function validateSortField(field: string | null): SortField {
	if (!field) return 'resilience_score';
	return ALLOWED_SORT_FIELDS.includes(field as SortField)
		? (field as SortField)
		: 'resilience_score';
}

export const GET: RequestHandler = async ({ url }) => {
	// Validate all parameters
	const state = validateState(url.searchParams.get('state'));
	const minScore = parseFloatParam(url.searchParams.get('min_score'), -10, -10, 10);
	const maxScore = parseFloatParam(url.searchParams.get('max_score'), 10, -10, 10);
	const limit = parseIntParam(url.searchParams.get('limit'), 100, 1, 1000);
	const offset = parseIntParam(url.searchParams.get('offset'), 0, 0, 1000000);
	const sortBy = validateSortField(url.searchParams.get('sort'));
	const order = url.searchParams.get('order') === 'asc' ? 'ASC' : 'DESC';

	// Validate logical consistency
	if (minScore > maxScore) {
		throw error(400, 'min_score cannot be greater than max_score');
	}

	// Build query based on filters
	let tracts;
	let total;

	try {
		if (state) {
			tracts = await sql`
				SELECT tract_fips, state_abbr, total_pop, resilience_score, burden,
					   gq_college_pct, gq_military_pct, gq_correctional_pct, gq_nursing_pct
				FROM tracts
				WHERE state_abbr = ${state}
				  AND resilience_score >= ${minScore}
				  AND resilience_score <= ${maxScore}
				ORDER BY ${sql(sortBy)} ${sql.unsafe(order)}
				LIMIT ${limit} OFFSET ${offset}
			`;
			[total] = await sql`
				SELECT COUNT(*) as count FROM tracts
				WHERE state_abbr = ${state}
				  AND resilience_score >= ${minScore}
				  AND resilience_score <= ${maxScore}
			`;
		} else {
			tracts = await sql`
				SELECT tract_fips, state_abbr, total_pop, resilience_score, burden,
					   gq_college_pct, gq_military_pct, gq_correctional_pct, gq_nursing_pct
				FROM tracts
				WHERE resilience_score >= ${minScore}
				  AND resilience_score <= ${maxScore}
				ORDER BY ${sql(sortBy)} ${sql.unsafe(order)}
				LIMIT ${limit} OFFSET ${offset}
			`;
			[total] = await sql`
				SELECT COUNT(*) as count FROM tracts
				WHERE resilience_score >= ${minScore}
				  AND resilience_score <= ${maxScore}
			`;
		}
	} catch (err) {
		console.error('Database query error:', err);
		throw error(500, 'Database query failed');
	}

	return json({
		tracts: tracts.map((t) => ({
			tractFips: t.tract_fips,
			state: t.state_abbr,
			population: t.total_pop,
			resilienceScore: parseFloat(t.resilience_score),
			burden: parseFloat(t.burden),
			gqCollege: parseFloat(t.gq_college_pct),
			gqMilitary: parseFloat(t.gq_military_pct),
			gqCorrectional: parseFloat(t.gq_correctional_pct),
			gqNursing: parseFloat(t.gq_nursing_pct)
		})),
		pagination: {
			total: parseInt(total.count),
			limit,
			offset,
			hasMore: offset + tracts.length < parseInt(total.count)
		}
	});
};
