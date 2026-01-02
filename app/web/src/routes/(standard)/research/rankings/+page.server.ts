import { sql } from '$lib/server/db';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	// Get all state rankings
	const allStates = await sql`
		SELECT state_abbr, avg_resilience, residential_count, total_population
		FROM mv_state_stats
		ORDER BY avg_resilience DESC
	`;

	// Get county count
	const [countyCount] = await sql`
		SELECT COUNT(*) as count FROM mv_county_stats WHERE residential_count >= 10
	`;

	// Get all counties with at least 10 tracts
	const topCounties = await sql`
		SELECT county_fips, county, state_abbr, avg_resilience, residential_count, total_population, resilience_range
		FROM mv_county_stats
		WHERE residential_count >= 10
		ORDER BY avg_resilience DESC
		LIMIT 50
	`;

	const bottomCounties = await sql`
		SELECT county_fips, county, state_abbr, avg_resilience, residential_count, total_population, resilience_range
		FROM mv_county_stats
		WHERE residential_count >= 10
		ORDER BY avg_resilience ASC
		LIMIT 50
	`;

	// Counties with highest internal inequality
	const mostUnequalCounties = await sql`
		SELECT county_fips, county, state_abbr, avg_resilience, resilience_range, max_resilience, min_resilience, residential_count, total_population
		FROM mv_county_stats
		WHERE residential_count >= 20
		ORDER BY resilience_range DESC
		LIMIT 25
	`;

	return {
		stateCount: allStates.length,
		countyCount: parseInt(countyCount.count),
		allStates: allStates.map((s) => ({
			state: s.state_abbr,
			avgResilience: parseFloat(s.avg_resilience),
			tractCount: parseInt(s.residential_count),
			population: parseInt(s.total_population)
		})),
		topCounties: topCounties.map((c) => ({
			fips: c.county_fips,
			county: c.county,
			state: c.state_abbr,
			avgResilience: parseFloat(c.avg_resilience),
			tractCount: parseInt(c.residential_count),
			population: parseInt(c.total_population),
			range: parseFloat(c.resilience_range)
		})),
		bottomCounties: bottomCounties.map((c) => ({
			fips: c.county_fips,
			county: c.county,
			state: c.state_abbr,
			avgResilience: parseFloat(c.avg_resilience),
			tractCount: parseInt(c.residential_count),
			population: parseInt(c.total_population),
			range: parseFloat(c.resilience_range)
		})),
		mostUnequalCounties: mostUnequalCounties.map((c) => ({
			fips: c.county_fips,
			county: c.county,
			state: c.state_abbr,
			avgResilience: parseFloat(c.avg_resilience),
			range: parseFloat(c.resilience_range),
			maxScore: parseFloat(c.max_resilience),
			minScore: parseFloat(c.min_resilience),
			tractCount: parseInt(c.residential_count),
			population: parseInt(c.total_population)
		}))
	};
};
