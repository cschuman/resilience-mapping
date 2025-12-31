import { sql } from '$lib/server/db';
import type { PageServerLoad } from './$types';

// State abbreviation to full name lookup
const STATE_NAMES: Record<string, string> = {
	AL: 'Alabama', AK: 'Alaska', AZ: 'Arizona', AR: 'Arkansas', CA: 'California',
	CO: 'Colorado', CT: 'Connecticut', DE: 'Delaware', DC: 'Washington DC', FL: 'Florida',
	GA: 'Georgia', HI: 'Hawaii', ID: 'Idaho', IL: 'Illinois', IN: 'Indiana',
	IA: 'Iowa', KS: 'Kansas', KY: 'Kentucky', LA: 'Louisiana', ME: 'Maine',
	MD: 'Maryland', MA: 'Massachusetts', MI: 'Michigan', MN: 'Minnesota', MS: 'Mississippi',
	MO: 'Missouri', MT: 'Montana', NE: 'Nebraska', NV: 'Nevada', NH: 'New Hampshire',
	NJ: 'New Jersey', NM: 'New Mexico', NY: 'New York', NC: 'North Carolina', ND: 'North Dakota',
	OH: 'Ohio', OK: 'Oklahoma', OR: 'Oregon', PA: 'Pennsylvania', RI: 'Rhode Island',
	SC: 'South Carolina', SD: 'South Dakota', TN: 'Tennessee', TX: 'Texas', UT: 'Utah',
	VT: 'Vermont', VA: 'Virginia', WA: 'Washington', WV: 'West Virginia', WI: 'Wisconsin',
	WY: 'Wyoming', PR: 'Puerto Rico', VI: 'Virgin Islands', GU: 'Guam', AS: 'American Samoa'
};

// Parse and validate numeric parameter
function parseNumber(value: string | null, defaultValue: number, min: number, max: number): number {
	if (!value) return defaultValue;
	const num = parseFloat(value);
	if (isNaN(num)) return defaultValue;
	return Math.max(min, Math.min(max, num));
}

export const load: PageServerLoad = async ({ url }) => {
	// Pagination
	const page = Math.max(1, parseInt(url.searchParams.get('page') || '1') || 1);
	const limit = 50;
	const offset = (page - 1) * limit;

	// Sorting
	const sort = url.searchParams.get('sort') || 'resilience_score';
	const order = url.searchParams.get('order') || 'desc';
	const validSorts = ['resilience_score', 'total_pop', 'state_abbr', 'tract_fips', 'burden'];
	const sortCol = validSorts.includes(sort) ? sort : 'resilience_score';
	const sortOrder = order === 'asc' ? 'ASC' : 'DESC';

	// Filters
	const state = url.searchParams.get('state') || '';
	const minScore = parseNumber(url.searchParams.get('min_score'), -10, -10, 10);
	const maxScore = parseNumber(url.searchParams.get('max_score'), 10, -10, 10);
	const minPop = parseNumber(url.searchParams.get('min_pop'), 0, 0, 1000000);

	// Build dynamic query
	let tracts;
	let totalCount;

	if (state) {
		tracts = await sql`
			SELECT
				tract_fips,
				state_abbr,
				county,
				resilience_score,
				total_pop,
				burden,
				is_residential,
				tract_type
			FROM tracts
			WHERE resilience_score IS NOT NULL
				AND is_residential = TRUE
				AND state_abbr = ${state}
				AND resilience_score >= ${minScore}
				AND resilience_score <= ${maxScore}
				AND (total_pop >= ${minPop} OR total_pop IS NULL)
			ORDER BY ${sql.unsafe(sortCol)} ${sql.unsafe(sortOrder)} NULLS LAST
			LIMIT ${limit}
			OFFSET ${offset}
		`;

		const [count] = await sql`
			SELECT COUNT(*) as count
			FROM tracts
			WHERE resilience_score IS NOT NULL
				AND is_residential = TRUE
				AND state_abbr = ${state}
				AND resilience_score >= ${minScore}
				AND resilience_score <= ${maxScore}
				AND (total_pop >= ${minPop} OR total_pop IS NULL)
		`;
		totalCount = parseInt(count.count);
	} else {
		tracts = await sql`
			SELECT
				tract_fips,
				state_abbr,
				county,
				resilience_score,
				total_pop,
				burden,
				is_residential,
				tract_type
			FROM tracts
			WHERE resilience_score IS NOT NULL
				AND is_residential = TRUE
				AND resilience_score >= ${minScore}
				AND resilience_score <= ${maxScore}
				AND (total_pop >= ${minPop} OR total_pop IS NULL)
			ORDER BY ${sql.unsafe(sortCol)} ${sql.unsafe(sortOrder)} NULLS LAST
			LIMIT ${limit}
			OFFSET ${offset}
		`;

		const [count] = await sql`
			SELECT COUNT(*) as count
			FROM tracts
			WHERE resilience_score IS NOT NULL
				AND is_residential = TRUE
				AND resilience_score >= ${minScore}
				AND resilience_score <= ${maxScore}
				AND (total_pop >= ${minPop} OR total_pop IS NULL)
		`;
		totalCount = parseInt(count.count);
	}

	// Get list of states for filter (from materialized view for speed)
	const states = await sql`
		SELECT state_abbr
		FROM mv_state_stats
		ORDER BY state_abbr
	`;

	// Build CSV export URL with current filters
	const csvParams = new URLSearchParams();
	if (state) csvParams.set('state', state);
	if (minScore > -10) csvParams.set('min_score', minScore.toString());
	if (maxScore < 10) csvParams.set('max_score', maxScore.toString());
	if (minPop > 0) csvParams.set('min_pop', minPop.toString());
	csvParams.set('sort', sortCol);
	csvParams.set('order', order);
	csvParams.set('limit', '10000'); // Max export limit
	const csvUrl = `/api/tracts?${csvParams.toString()}`;

	return {
		tracts: tracts.map((t) => {
			const stateName = STATE_NAMES[t.state_abbr] || t.state_abbr;
			const location = t.county ? `${t.county}, ${stateName}` : stateName;
			return {
				fips: t.tract_fips,
				location,
				state: t.state_abbr,
				stateName,
				county: t.county,
				score: t.resilience_score ? parseFloat(t.resilience_score).toFixed(2) : null,
				population: t.total_pop,
				burden: t.burden ? parseFloat(t.burden).toFixed(3) : null,
				tractType: t.tract_type
			};
		}),
		pagination: {
			page,
			limit,
			total: totalCount,
			totalPages: Math.ceil(totalCount / limit),
			hasNext: page < Math.ceil(totalCount / limit),
			hasPrev: page > 1
		},
		filters: {
			sort: sortCol,
			order,
			state,
			minScore,
			maxScore,
			minPop
		},
		states: states.map((s) => s.state_abbr),
		csvUrl
	};
};
