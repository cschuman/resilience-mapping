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

export const load: PageServerLoad = async ({ url }) => {
	const page = parseInt(url.searchParams.get('page') || '1');
	const limit = 50;
	const offset = (page - 1) * limit;
	const sort = url.searchParams.get('sort') || 'resilience_score';
	const order = url.searchParams.get('order') || 'desc';
	const state = url.searchParams.get('state') || '';

	// Validate sort column
	const validSorts = ['resilience_score', 'total_pop', 'state_abbr', 'tract_fips'];
	const sortCol = validSorts.includes(sort) ? sort : 'resilience_score';
	const sortOrder = order === 'asc' ? 'ASC' : 'DESC';

	// Build query with optional state filter
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
				burden
			FROM tracts
			WHERE resilience_score IS NOT NULL
				AND state_abbr = ${state}
			ORDER BY ${sql.unsafe(sortCol)} ${sql.unsafe(sortOrder)} NULLS LAST
			LIMIT ${limit}
			OFFSET ${offset}
		`;

		const [count] = await sql`
			SELECT COUNT(*) as count
			FROM tracts
			WHERE resilience_score IS NOT NULL
				AND state_abbr = ${state}
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
				burden
			FROM tracts
			WHERE resilience_score IS NOT NULL
			ORDER BY ${sql.unsafe(sortCol)} ${sql.unsafe(sortOrder)} NULLS LAST
			LIMIT ${limit}
			OFFSET ${offset}
		`;

		const [count] = await sql`
			SELECT COUNT(*) as count
			FROM tracts
			WHERE resilience_score IS NOT NULL
		`;
		totalCount = parseInt(count.count);
	}

	// Get list of states for filter
	const states = await sql`
		SELECT DISTINCT state_abbr
		FROM tracts
		WHERE state_abbr IS NOT NULL
		ORDER BY state_abbr
	`;

	return {
		tracts: tracts.map((t) => {
			const stateName = STATE_NAMES[t.state_abbr] || t.state_abbr;
			const location = t.county ? `${t.county}, ${stateName}` : stateName;
			return {
				fips: t.tract_fips,
				location,
				state: t.state_abbr,
				score: t.resilience_score ? parseFloat(t.resilience_score).toFixed(2) : null,
				population: t.total_pop,
				burden: t.burden ? parseFloat(t.burden).toFixed(3) : null
			};
		}),
		pagination: {
			page,
			limit,
			total: totalCount,
			totalPages: Math.ceil(totalCount / limit)
		},
		filters: {
			sort: sortCol,
			order,
			state
		},
		states: states.map((s) => s.state_abbr)
	};
};
