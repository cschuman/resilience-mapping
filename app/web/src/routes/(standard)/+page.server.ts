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

export const load: PageServerLoad = async () => {
	// Use materialized views for faster stats
	const [stats] = await sql`
		SELECT
			residential_tracts as total_tracts,
			avg_resilience,
			max_resilience,
			total_population
		FROM mv_overall_stats
		WHERE category = 'all'
	`;

	const total = parseInt(stats.total_tracts);

	// Get top residential tracts with their rank
	const topTracts = await sql`
		SELECT
			tract_fips,
			state_abbr,
			resilience_score,
			total_pop,
			RANK() OVER (ORDER BY resilience_score DESC) as rank
		FROM tracts
		WHERE is_residential = TRUE
		ORDER BY resilience_score DESC
		LIMIT 6
	`;

	// Get state count from materialized view
	const [stateCount] = await sql`
		SELECT COUNT(*) as count FROM mv_state_stats
	`;

	return {
		stats: {
			totalTracts: total,
			avgResilience: parseFloat(stats.avg_resilience).toFixed(3),
			maxResilience: parseFloat(stats.max_resilience).toFixed(3),
			totalPopulation: parseInt(stats.total_population),
			stateCount: parseInt(stateCount.count)
		},
		topTracts: topTracts.map((t) => {
			const rank = parseInt(t.rank);
			// Calculate "Top X%" - what percentage of tracts this one outperforms
			const topPercent = Math.max(1, Math.ceil((rank / total) * 100));
			const stateName = STATE_NAMES[t.state_abbr] || t.state_abbr;
			return {
				fips: t.tract_fips,
				state: stateName,
				score: parseFloat(t.resilience_score).toFixed(2),
				topPercent: topPercent,
				population: t.total_pop
			};
		})
	};
};
