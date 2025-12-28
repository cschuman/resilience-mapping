import { json } from '@sveltejs/kit';
import { sql } from '$lib/server/db';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
	const state = url.searchParams.get('state');
	const minScore = parseFloat(url.searchParams.get('min_score') || '0');
	const maxScore = parseFloat(url.searchParams.get('max_score') || '10');
	const limit = Math.min(parseInt(url.searchParams.get('limit') || '100'), 1000);
	const offset = parseInt(url.searchParams.get('offset') || '0');
	const sortBy = url.searchParams.get('sort') || 'resilience_score';
	const order = url.searchParams.get('order') === 'asc' ? 'ASC' : 'DESC';

	// Build query based on filters
	let tracts;
	let total;

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
