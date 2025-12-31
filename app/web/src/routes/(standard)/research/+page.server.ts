import { sql } from '$lib/server/db';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	// Get key statistics from materialized views
	const [stats] = await sql`
		SELECT
			residential_tracts,
			avg_resilience,
			median_resilience,
			p25_resilience,
			p75_resilience,
			total_population
		FROM mv_overall_stats
		WHERE category = 'all'
	`;

	// Get state count
	const [stateCount] = await sql`
		SELECT COUNT(*) as count FROM mv_state_stats
	`;

	// Get county count
	const [countyCount] = await sql`
		SELECT COUNT(*) as count FROM mv_county_stats
	`;

	// Get top and bottom states by average resilience
	const topStates = await sql`
		SELECT state_abbr, avg_resilience, residential_count, total_population
		FROM mv_state_stats
		ORDER BY avg_resilience DESC
		LIMIT 5
	`;

	const bottomStates = await sql`
		SELECT state_abbr, avg_resilience, residential_count, total_population
		FROM mv_state_stats
		ORDER BY avg_resilience ASC
		LIMIT 5
	`;

	// Get top and bottom counties (with at least 10 tracts for statistical significance)
	const topCounties = await sql`
		SELECT county_fips, county, state_abbr, avg_resilience, residential_count, total_population, resilience_range
		FROM mv_county_stats
		WHERE residential_count >= 10
		ORDER BY avg_resilience DESC
		LIMIT 15
	`;

	const bottomCounties = await sql`
		SELECT county_fips, county, state_abbr, avg_resilience, residential_count, total_population, resilience_range
		FROM mv_county_stats
		WHERE residential_count >= 10
		ORDER BY avg_resilience ASC
		LIMIT 15
	`;

	// Counties with highest internal inequality (widest range between best/worst tracts)
	const mostUnequalCounties = await sql`
		SELECT county_fips, county, state_abbr, avg_resilience, resilience_range, max_resilience, min_resilience, residential_count, total_population
		FROM mv_county_stats
		WHERE residential_count >= 20
		ORDER BY resilience_range DESC
		LIMIT 10
	`;

	return {
		stats: {
			totalTracts: parseInt(stats.residential_tracts),
			avgResilience: parseFloat(stats.avg_resilience),
			medianResilience: parseFloat(stats.median_resilience),
			p25: parseFloat(stats.p25_resilience),
			p75: parseFloat(stats.p75_resilience),
			totalPopulation: parseInt(stats.total_population),
			stateCount: parseInt(stateCount.count),
			countyCount: parseInt(countyCount.count)
		},
		topStates: topStates.map((s) => ({
			state: s.state_abbr,
			avgResilience: parseFloat(s.avg_resilience),
			tractCount: parseInt(s.residential_count),
			population: parseInt(s.total_population)
		})),
		bottomStates: bottomStates.map((s) => ({
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
