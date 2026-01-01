<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	// State name lookup
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
		WY: 'Wyoming'
	};
</script>

<svelte:head>
	<title>College vs Prison: A 4 Standard Deviation Health Divide | odds.health Research</title>
	<meta
		name="description"
		content="College communities average +2.95 resilience. Prison communities average -0.98. Same country, same healthcare system, 4 SD apart. What's protecting students that's failing inmates?"
	/>
</svelte:head>

<div class="research">
	<div class="container">
		<!-- Header - LEAD WITH A FINDING -->
		<header class="header">
			<p class="header__eyebrow">Key Discovery</p>
			<h1 class="header__title">College Towns vs Prison Towns: A 4 SD Health Divide</h1>
			<p class="header__subtitle">
				College communities average <strong class="positive">+2.95</strong> resilience.
				Prison communities average <strong class="negative">-0.98</strong>.
				Same country, same healthcare system, 4 standard deviations apart.
			</p>
		</header>

		<!-- Headline Findings - NOW FIRST -->
		<section class="headlines" aria-labelledby="headlines-heading">
			<h2 id="headlines-heading" class="section-title">What We Found</h2>
			<p class="headlines__intro">
				Counterintuitive patterns and surprising discoveries that challenge assumptions.
			</p>

			<div class="headlines__grid">
				<a href="/research/special-populations" class="headline-card headline-card--featured">
					<div class="headline-card__badge">Featured</div>
					<h3 class="headline-card__title">The 4 Standard Deviation Gap</h3>
					<p class="headline-card__text">
						College communities average <strong class="positive">+2.95</strong> resilience
						while prison communities average <strong class="negative">-0.98</strong>.
						Education vs. incarceration: the starkest divide in American health.
					</p>
					<span class="headline-card__link">Explore Special Populations &rarr;</span>
				</a>

				<a href="/research/ohio-bifurcation" class="headline-card headline-card--link">
					<h3 class="headline-card__title">Ohio's Bifurcation</h3>
					<p class="headline-card__text">
						Columbus has 4 of the nation's top 10 tracts.
						Cleveland has 3 of the bottom 10.
						Same state, 60 miles apart, 10+ standard deviations difference.
					</p>
					<span class="headline-card__link">Explore Ohio →</span>
				</a>

				<a href="/research/inequality-chasm" class="headline-card headline-card--link">
					<h3 class="headline-card__title">The 9-Point Chasm</h3>
					<p class="headline-card__text">
						Cleveland and New Orleans each have 9+ point gaps between their
						best and worst neighborhoods. Same county, vastly different outcomes.
					</p>
					<span class="headline-card__link">Explore Inequality →</span>
				</a>

				<a href="/research/west-virginia-paradox" class="headline-card headline-card--link">
					<h3 class="headline-card__title">West Virginia Paradox</h3>
					<p class="headline-card__text">
						Highest health burden in America (+1.0), yet resilience near average (-0.04).
						Something is protecting these communities despite terrible metrics.
					</p>
					<span class="headline-card__link">Explore WV Paradox →</span>
				</a>
			</div>
		</section>

		<!-- Papers Section -->
		<section class="papers" aria-labelledby="papers-heading">
			<h2 id="papers-heading" class="section-title">Research Papers</h2>

			<div class="papers__grid">
				<article class="paper paper--primary">
					<div class="paper__badge">Paper 1</div>
					<h3 class="paper__title">
						Spatial Synchrony, Not Contagion: A Methodological Correction in Community Health Trajectory Prediction
					</h3>
					<p class="paper__abstract">
						We demonstrate that apparent "spatial contagion" in community health trajectories
						was an artifact of temporal data leakage. Communities exhibit spatial synchrony—they
						change together—but prior neighbor trajectories do not predict future focal trajectories.
						This finding has important implications for spatial health modeling.
					</p>
					<div class="paper__meta">
						<span class="paper__status paper__status--review">Pre-print</span>
						<span class="paper__date">December 2024</span>
					</div>
					<div class="paper__topics">
						<span class="topic">Spatial Epidemiology</span>
						<span class="topic">Methodology</span>
						<span class="topic">CDC PLACES</span>
					</div>
					<div class="paper__actions">
						<a href="/research/papers/spatial-synchrony" class="btn btn--primary">
							Read Paper
						</a>
					</div>
				</article>

				<article class="paper paper--secondary">
					<div class="paper__badge">Paper 2</div>
					<h3 class="paper__title">
						Regression to the Mean in Small-Area Health Estimates: Why Trajectory Prediction Fails
					</h3>
					<p class="paper__abstract">
						We tried to predict which communities would get healthier or sicker—and failed
						completely (F1=0.26, chance performance). The "quintile gradient" reveals why:
						extreme year-over-year changes regress to the mean, not genuine health dynamics.
					</p>
					<div class="paper__meta">
						<span class="paper__status paper__status--review">Pre-print</span>
						<span class="paper__date">December 2024</span>
					</div>
					<div class="paper__topics">
						<span class="topic">Regression to Mean</span>
						<span class="topic">Measurement Error</span>
						<span class="topic">Prediction</span>
					</div>
					<div class="paper__actions">
						<a href="/research/papers/regression-to-mean" class="btn btn--primary">
							Read Paper
						</a>
					</div>
				</article>

				<article class="paper paper--secondary">
					<div class="paper__badge">Paper 3</div>
					<h3 class="paper__title">
						Structural Determinants of Community Health Resilience: A Tract-Level Analysis of 53,889 U.S. Communities
					</h3>
					<p class="paper__abstract">
						A 0.38 SD resilience gap exists between majority-white and majority-minority communities.
						But state variation from +1.87 SD (DC) to -0.53 SD (Oregon) proves structural factors—not
						race—determine resilience. Education is the strongest correlate (r=+0.41).
					</p>
					<div class="paper__meta">
						<span class="paper__status paper__status--review">Pre-print</span>
						<span class="paper__date">December 2024</span>
					</div>
					<div class="paper__topics">
						<span class="topic">Health Equity</span>
						<span class="topic">Racial Disparities</span>
						<span class="topic">Structural Determinants</span>
					</div>
					<div class="paper__actions">
						<a href="/research/papers/structural-determinants" class="btn btn--primary">
							Read Paper
						</a>
					</div>
				</article>

				<article class="paper paper--secondary">
					<div class="paper__badge">Paper 4</div>
					<h3 class="paper__title">
						Structural Correlates of Community Health Resilience: A Cross-Sectional Analysis of 53,889 U.S. Census Tracts
					</h3>
					<p class="paper__abstract">
						A 0.43 SD resilience gap exists between majority-white and majority-minority communities.
						But state variation from +1.87 SD (DC) to -0.42 SD (Washington) proves structural factors—not
						immutable characteristics—determine resilience. Education is the strongest correlate (r=+0.41).
					</p>
					<div class="paper__meta">
						<span class="paper__status paper__status--review">Pre-print</span>
						<span class="paper__date">January 2025</span>
					</div>
					<div class="paper__topics">
						<span class="topic">Health Equity</span>
						<span class="topic">Racial Disparities</span>
						<span class="topic">State Variation</span>
					</div>
					<div class="paper__actions">
						<a href="/research/papers/health-equity" class="btn btn--primary">
							Read Paper
						</a>
					</div>
				</article>

				<article class="paper paper--featured">
					<div class="paper__badge">Paper 5</div>
					<div class="paper__new">NEW</div>
					<h3 class="paper__title">
						Beyond the Hispanic Paradox: Immigrant Health Advantage, Structural Poverty, and the Aggregation Artifact
					</h3>
					<p class="paper__abstract">
						The "Hispanic Paradox" is an aggregation artifact: South American (r=+0.147) vs Mexican (r=-0.029)
						cancel to r≈0. Black immigrants show STRONGER health advantage than Hispanic immigrants.
						Same ethnicity, same state: Austin (+1.53 SD) vs Border (-1.08 SD)—2.61 SD gap.
					</p>
					<div class="paper__meta">
						<span class="paper__status paper__status--review">Pre-print</span>
						<span class="paper__date">January 2025</span>
					</div>
					<div class="paper__topics">
						<span class="topic">Hispanic Paradox</span>
						<span class="topic">Immigrant Health</span>
						<span class="topic">Texas Border</span>
					</div>
					<div class="paper__actions">
						<a href="/research/papers/immigrant-health-advantage" class="btn btn--primary">
							Read Paper
						</a>
					</div>
				</article>
			</div>
		</section>

		<!-- Key Findings -->
		<section class="findings" aria-labelledby="findings-heading">
			<h2 id="findings-heading" class="section-title">Key Findings</h2>

			<div class="findings__grid">
				<div class="finding">
					<div class="finding__icon">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
							<path fill-rule="evenodd" d="M2.25 13.5a8.25 8.25 0 018.25-8.25.75.75 0 01.75.75v6.75H18a.75.75 0 01.75.75 8.25 8.25 0 01-16.5 0z" clip-rule="evenodd" />
							<path fill-rule="evenodd" d="M12.75 3a.75.75 0 01.75-.75 8.25 8.25 0 018.25 8.25.75.75 0 01-.75.75h-7.5a.75.75 0 01-.75-.75V3z" clip-rule="evenodd" />
						</svg>
					</div>
					<h3 class="finding__title">Normal Distribution</h3>
					<p class="finding__text">
						Resilience scores follow an approximately normal distribution with mean near zero.
						The median score is <strong>{data.stats.medianResilience.toFixed(3)}</strong>,
						with an interquartile range of {data.stats.p25.toFixed(2)} to {data.stats.p75.toFixed(2)}.
					</p>
				</div>

				<div class="finding">
					<div class="finding__icon">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
							<path fill-rule="evenodd" d="M8.161 2.58a1.875 1.875 0 011.678 0l4.993 2.498c.106.052.23.052.336 0l3.869-1.935A1.875 1.875 0 0121.75 4.82v12.485c0 .71-.401 1.36-1.037 1.677l-4.875 2.437a1.875 1.875 0 01-1.676 0l-4.994-2.497a.375.375 0 00-.336 0l-3.868 1.935A1.875 1.875 0 012.25 19.18V6.695c0-.71.401-1.36 1.036-1.677l4.875-2.437zM9 6a.75.75 0 01.75.75V15a.75.75 0 01-1.5 0V6.75A.75.75 0 019 6zm6.75 3a.75.75 0 00-1.5 0v8.25a.75.75 0 001.5 0V9z" clip-rule="evenodd" />
						</svg>
					</div>
					<h3 class="finding__title">Regional Variation</h3>
					<p class="finding__text">
						Significant variation exists across states. Top performers include
						<strong>{STATE_NAMES[data.topStates[0]?.state] || data.topStates[0]?.state}</strong> and
						<strong>{STATE_NAMES[data.topStates[1]?.state] || data.topStates[1]?.state}</strong>,
						while states like
						<strong>{STATE_NAMES[data.bottomStates[0]?.state] || data.bottomStates[0]?.state}</strong>
						show room for improvement.
					</p>
				</div>

				<div class="finding">
					<div class="finding__icon">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
							<path d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0112 5.052 5.5 5.5 0 0116.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 01-4.244 3.17 15.247 15.247 0 01-.383.219l-.022.012-.007.004-.003.001a.752.752 0 01-.704 0l-.003-.001z" />
						</svg>
					</div>
					<h3 class="finding__title">Positive Outliers Exist</h3>
					<p class="finding__text">
						Across all {data.stats.stateCount} states, we find communities that significantly
						outperform expectations. These "positive outliers" offer insights into what
						factors may promote health resilience beyond socioeconomic status.
					</p>
				</div>

				<div class="finding">
					<div class="finding__icon">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
							<path fill-rule="evenodd" d="M7.5 6a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM3.751 20.105a8.25 8.25 0 0116.498 0 .75.75 0 01-.437.695A18.683 18.683 0 0112 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 01-.437-.695z" clip-rule="evenodd" />
						</svg>
					</div>
					<h3 class="finding__title">Population Coverage</h3>
					<p class="finding__text">
						Our analysis covers <strong>{(data.stats.totalPopulation / 1_000_000).toFixed(0)}+ million</strong> people
						across <strong>{data.stats.totalTracts.toLocaleString()}</strong> residential census tracts,
						providing comprehensive national coverage.
					</p>
				</div>
			</div>
		</section>

		<!-- State Rankings -->
		<section class="rankings" aria-labelledby="rankings-heading">
			<h2 id="rankings-heading" class="section-title">State-Level Patterns</h2>

			<div class="rankings__grid">
				<div class="ranking ranking--top">
					<h3 class="ranking__title">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
							<path fill-rule="evenodd" d="M10 17a.75.75 0 01-.75-.75V5.612L5.29 9.77a.75.75 0 01-1.08-1.04l5.25-5.5a.75.75 0 011.08 0l5.25 5.5a.75.75 0 11-1.08 1.04l-3.96-4.158V16.25A.75.75 0 0110 17z" clip-rule="evenodd" />
						</svg>
						Highest Average Resilience
					</h3>
					<ol class="ranking__list">
						{#each data.topStates as state, i}
							<li class="ranking__item">
								<span class="ranking__rank">{i + 1}</span>
								<span class="ranking__state">{STATE_NAMES[state.state] || state.state}</span>
								<span class="ranking__score" class:positive={state.avgResilience > 0}>
									{state.avgResilience > 0 ? '+' : ''}{state.avgResilience.toFixed(3)}
								</span>
							</li>
						{/each}
					</ol>
				</div>

				<div class="ranking ranking--bottom">
					<h3 class="ranking__title">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
							<path fill-rule="evenodd" d="M10 3a.75.75 0 01.75.75v10.638l3.96-4.158a.75.75 0 111.08 1.04l-5.25 5.5a.75.75 0 01-1.08 0l-5.25-5.5a.75.75 0 111.08-1.04l3.96 4.158V3.75A.75.75 0 0110 3z" clip-rule="evenodd" />
						</svg>
						Lowest Average Resilience
					</h3>
					<ol class="ranking__list">
						{#each data.bottomStates as state, i}
							<li class="ranking__item">
								<span class="ranking__rank">{data.stats.stateCount - i}</span>
								<span class="ranking__state">{STATE_NAMES[state.state] || state.state}</span>
								<span class="ranking__score" class:negative={state.avgResilience < 0}>
									{state.avgResilience > 0 ? '+' : ''}{state.avgResilience.toFixed(3)}
								</span>
							</li>
						{/each}
					</ol>
				</div>
			</div>
		</section>

		<!-- County Rankings -->
		<section class="rankings" aria-labelledby="county-rankings-heading">
			<h2 id="county-rankings-heading" class="section-title">County Rankings</h2>
			<p class="rankings__intro">
				Rankings based on {data.stats.countyCount.toLocaleString()} counties with at least 10 census tracts for statistical reliability.
			</p>

			<div class="rankings__grid rankings__grid--three">
				<!-- Top Counties -->
				<div class="ranking">
					<h3 class="ranking__title">Most Resilient Counties</h3>
					<ol class="ranking__list ranking__list--compact">
						{#each data.topCounties.slice(0, 10) as county, i}
							<li class="ranking__item">
								<span class="ranking__rank">{i + 1}</span>
								<span class="ranking__county">{county.county}, {county.state}</span>
								<span class="ranking__score" class:positive={county.avgResilience > 0}>
									{county.avgResilience > 0 ? '+' : ''}{county.avgResilience.toFixed(3)}
								</span>
							</li>
						{/each}
					</ol>
				</div>

				<!-- Bottom Counties -->
				<div class="ranking">
					<h3 class="ranking__title">Struggling Counties</h3>
					<ol class="ranking__list ranking__list--compact">
						{#each data.bottomCounties.slice(0, 10) as county, i}
							<li class="ranking__item">
								<span class="ranking__rank ranking__rank--bottom">{data.stats.countyCount - i}</span>
								<span class="ranking__county">{county.county}, {county.state}</span>
								<span class="ranking__score negative">
									{county.avgResilience > 0 ? '+' : ''}{county.avgResilience.toFixed(3)}
								</span>
							</li>
						{/each}
					</ol>
				</div>

				<!-- Most Unequal Counties -->
				<div class="ranking">
					<h3 class="ranking__title">Widest Internal Gaps</h3>
					<p class="ranking__subtitle">Largest difference between best and worst tracts</p>
					<ol class="ranking__list ranking__list--compact">
						{#each data.mostUnequalCounties as county, i}
							<li class="ranking__item ranking__item--gap">
								<span class="ranking__rank">{i + 1}</span>
								<span class="ranking__county">{county.county}, {county.state}</span>
								<span class="ranking__gap">{county.range.toFixed(1)} pts</span>
							</li>
						{/each}
					</ol>
				</div>
			</div>
		</section>

		<!-- Data Access -->
		<section class="access" aria-labelledby="access-heading">
			<h2 id="access-heading" class="section-title">Access the Data</h2>

			<div class="access__content">
				<p class="access__description">
					All data from this research is freely available for academic, journalistic,
					and policy research. No registration required.
				</p>

				<div class="access__options">
					<a href="/data" class="access__option">
						<div class="access__option-icon">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
								<path fill-rule="evenodd" d="M1.5 5.625c0-1.036.84-1.875 1.875-1.875h17.25c1.035 0 1.875.84 1.875 1.875v12.75c0 1.035-.84 1.875-1.875 1.875H3.375A1.875 1.875 0 011.5 18.375V5.625zM21 9.375A.375.375 0 0020.625 9h-7.5a.375.375 0 00-.375.375v1.5c0 .207.168.375.375.375h7.5a.375.375 0 00.375-.375v-1.5zm0 3.75a.375.375 0 00-.375-.375h-7.5a.375.375 0 00-.375.375v1.5c0 .207.168.375.375.375h7.5a.375.375 0 00.375-.375v-1.5zm0 3.75a.375.375 0 00-.375-.375h-7.5a.375.375 0 00-.375.375v1.5c0 .207.168.375.375.375h7.5a.375.375 0 00.375-.375v-1.5zM10.875 18.75a.375.375 0 00.375-.375v-1.5a.375.375 0 00-.375-.375h-7.5a.375.375 0 00-.375.375v1.5c0 .207.168.375.375.375h7.5zM3.375 15h7.5a.375.375 0 00.375-.375v-1.5a.375.375 0 00-.375-.375h-7.5a.375.375 0 00-.375.375v1.5c0 .207.168.375.375.375zm0-3.75h7.5a.375.375 0 00.375-.375v-1.5A.375.375 0 0010.875 9h-7.5A.375.375 0 003 9.375v1.5c0 .207.168.375.375.375z" clip-rule="evenodd" />
							</svg>
						</div>
						<div class="access__option-content">
							<h3>Browse & Download</h3>
							<p>Interactive data browser with CSV export</p>
						</div>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="access__arrow" aria-hidden="true">
							<path fill-rule="evenodd" d="M3 10a.75.75 0 01.75-.75h10.638L10.23 5.29a.75.75 0 111.04-1.08l5.5 5.25a.75.75 0 010 1.08l-5.5 5.25a.75.75 0 11-1.04-1.08l4.158-3.96H3.75A.75.75 0 013 10z" clip-rule="evenodd" />
						</svg>
					</a>

					<a href="/map" class="access__option">
						<div class="access__option-icon">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
								<path fill-rule="evenodd" d="M8.161 2.58a1.875 1.875 0 011.678 0l4.993 2.498c.106.052.23.052.336 0l3.869-1.935A1.875 1.875 0 0121.75 4.82v12.485c0 .71-.401 1.36-1.037 1.677l-4.875 2.437a1.875 1.875 0 01-1.676 0l-4.994-2.497a.375.375 0 00-.336 0l-3.868 1.935A1.875 1.875 0 012.25 19.18V6.695c0-.71.401-1.36 1.036-1.677l4.875-2.437zM9 6a.75.75 0 01.75.75V15a.75.75 0 01-1.5 0V6.75A.75.75 0 019 6zm6.75 3a.75.75 0 00-1.5 0v8.25a.75.75 0 001.5 0V9z" clip-rule="evenodd" />
							</svg>
						</div>
						<div class="access__option-content">
							<h3>Interactive Map</h3>
							<p>Explore all 54,000+ census tracts visually</p>
						</div>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="access__arrow" aria-hidden="true">
							<path fill-rule="evenodd" d="M3 10a.75.75 0 01.75-.75h10.638L10.23 5.29a.75.75 0 111.04-1.08l5.5 5.25a.75.75 0 010 1.08l-5.5 5.25a.75.75 0 11-1.04-1.08l4.158-3.96H3.75A.75.75 0 013 10z" clip-rule="evenodd" />
						</svg>
					</a>

					<a href="/about#api" class="access__option">
						<div class="access__option-icon">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
								<path fill-rule="evenodd" d="M14.447 3.027a.75.75 0 01.527.92l-4.5 16.5a.75.75 0 01-1.448-.394l4.5-16.5a.75.75 0 01.921-.526zM16.72 6.22a.75.75 0 011.06 0l5.25 5.25a.75.75 0 010 1.06l-5.25 5.25a.75.75 0 11-1.06-1.06L21.44 12l-4.72-4.72a.75.75 0 010-1.06zm-9.44 0a.75.75 0 010 1.06L2.56 12l4.72 4.72a.75.75 0 11-1.06 1.06L.97 12.53a.75.75 0 010-1.06l5.25-5.25a.75.75 0 011.06 0z" clip-rule="evenodd" />
							</svg>
						</div>
						<div class="access__option-content">
							<h3>REST API</h3>
							<p>Programmatic access for applications</p>
						</div>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="access__arrow" aria-hidden="true">
							<path fill-rule="evenodd" d="M3 10a.75.75 0 01.75-.75h10.638L10.23 5.29a.75.75 0 111.04-1.08l5.5 5.25a.75.75 0 010 1.08l-5.5 5.25a.75.75 0 11-1.04-1.08l4.158-3.96H3.75A.75.75 0 013 10z" clip-rule="evenodd" />
						</svg>
					</a>
				</div>
			</div>
		</section>

		<!-- Citation -->
		<section class="citation" aria-labelledby="citation-heading">
			<h2 id="citation-heading" class="section-title">How to Cite</h2>
			<div class="citation__block">
				<code>Community Resilience Mapping Project (2025). Census tract-level health resilience scores for the United States. https://odds.health</code>
			</div>
			<p class="citation__note">
				This dataset is provided under open access terms. Please cite when using in publications.
			</p>
		</section>
	</div>
</div>

<style>
	/* ==========================================
	 * RESEARCH PAGE
	 * ========================================== */

	.research {
		color: var(--color-text-primary);
	}

	.container {
		max-width: var(--container-lg);
		margin: 0 auto;
		padding: var(--space-8) var(--space-6) var(--space-16);
	}

	/* ==========================================
	 * HEADER
	 * ========================================== */

	.header {
		text-align: center;
		margin-bottom: var(--space-12);
		padding-top: var(--space-8);
	}

	.header__eyebrow {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-accent-primary);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		margin-bottom: var(--space-4);
	}

	.header__title {
		font-family: var(--font-display);
		font-size: clamp(var(--text-3xl), 5vw, var(--text-4xl));
		font-weight: var(--font-weight-normal);
		line-height: var(--leading-snug);
		letter-spacing: var(--tracking-display);
		color: var(--color-text-primary);
		margin-bottom: var(--space-4);
	}

	.header__subtitle {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
		max-width: 600px;
		margin: 0 auto;
	}

	.header__subtitle strong.positive {
		color: var(--color-score-high);
		font-weight: var(--font-weight-bold);
	}

	.header__subtitle strong.negative {
		color: var(--color-score-low);
		font-weight: var(--font-weight-bold);
	}

	/* ==========================================
	 * SECTION TITLE
	 * ========================================== */

	.section-title {
		font-family: var(--font-display);
		font-size: var(--text-2xl);
		color: var(--color-text-primary);
		margin-bottom: var(--space-8);
		padding-bottom: var(--space-4);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	/* ==========================================
	 * PAPERS
	 * ========================================== */

	.papers {
		margin-bottom: var(--space-16);
	}

	.papers__grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
		gap: var(--space-6);
	}

	.paper {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
		transition: all var(--duration-normal) var(--ease-out);
	}

	.paper:hover {
		border-color: var(--color-accent-primary);
		box-shadow: var(--shadow-lg);
	}

	.paper__badge {
		display: inline-block;
		font-size: var(--text-xs);
		font-weight: var(--font-weight-bold);
		color: var(--color-accent-primary);
		background: var(--color-accent-primary-glow);
		padding: var(--space-1) var(--space-3);
		border-radius: var(--radius-full);
		margin-bottom: var(--space-4);
	}

	.paper__title {
		font-size: var(--text-xl);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-3);
		line-height: var(--leading-tight);
	}

	.paper__abstract {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-4);
	}

	.paper__meta {
		display: flex;
		gap: var(--space-3);
		margin-bottom: var(--space-4);
	}

	.paper__status {
		font-size: var(--text-xs);
		font-weight: var(--font-weight-medium);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.paper__status--draft {
		background: rgba(148, 163, 184, 0.15);
		color: var(--color-text-secondary);
	}

	.paper__status--published {
		background: var(--color-score-high-bg);
		color: var(--color-score-high);
	}

	.paper__status--review {
		background: var(--color-accent-secondary-glow);
		color: var(--color-accent-secondary);
	}

	.paper__date {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.paper__topics {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-2);
		margin-bottom: var(--space-6);
	}

	.topic {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		background: var(--color-foundation-surface);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
		border: 1px solid var(--color-border-subtle);
	}

	.paper__actions {
		margin-top: auto;
	}

	/* ==========================================
	 * FINDINGS
	 * ========================================== */

	.findings {
		margin-bottom: var(--space-16);
	}

	.findings__grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: var(--space-6);
	}

	.finding {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
	}

	.finding__icon {
		width: 48px;
		height: 48px;
		background: var(--color-accent-primary-glow);
		border-radius: var(--radius-lg);
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: var(--space-4);
	}

	.finding__icon svg {
		width: 24px;
		height: 24px;
		color: var(--color-accent-primary);
	}

	.finding__title {
		font-size: var(--text-lg);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.finding__text {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	/* ==========================================
	 * HEADLINES
	 * ========================================== */

	.headlines {
		margin-bottom: var(--space-16);
	}

	.headlines__intro {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-6);
	}

	.headlines__grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: var(--space-5);
	}

	.headline-card {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-5);
		transition: all var(--duration-normal) var(--ease-out);
	}

	.headline-card--featured {
		grid-column: span 2;
		background: linear-gradient(135deg, var(--color-foundation-mid), var(--color-accent-primary-glow));
		border-color: var(--color-accent-primary);
		text-decoration: none;
		color: inherit;
	}

	.headline-card--featured:hover {
		border-color: var(--color-accent-primary);
		box-shadow: var(--shadow-lg);
		transform: translateY(-2px);
	}

	.headline-card__badge {
		display: inline-block;
		font-size: var(--text-xs);
		font-weight: var(--font-weight-bold);
		color: var(--color-accent-primary);
		background: var(--color-accent-primary-glow);
		padding: var(--space-1) var(--space-3);
		border-radius: var(--radius-full);
		margin-bottom: var(--space-3);
	}

	.headline-card__title {
		font-size: var(--text-lg);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.headline-card__text {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	.headline-card__text strong.positive {
		color: var(--color-score-high);
	}

	.headline-card__text strong.negative {
		color: var(--color-score-low);
	}

	.headline-card--link {
		text-decoration: none;
		color: inherit;
		cursor: pointer;
	}

	.headline-card--link:hover {
		border-color: var(--color-accent-primary);
		box-shadow: var(--shadow-lg);
		transform: translateY(-2px);
	}

	.headline-card__link {
		display: inline-block;
		margin-top: var(--space-3);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-accent-primary);
	}

	@media (max-width: 700px) {
		.headline-card--featured {
			grid-column: span 1;
		}
	}

	.finding__text strong {
		color: var(--color-text-primary);
	}

	/* ==========================================
	 * RANKINGS
	 * ========================================== */

	.rankings {
		margin-bottom: var(--space-16);
	}

	.rankings__grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: var(--space-6);
	}

	.ranking {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
	}

	.ranking__title {
		display: flex;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-4);
	}

	.ranking__title svg {
		width: 20px;
		height: 20px;
	}

	.ranking--top .ranking__title svg {
		color: var(--color-score-high);
	}

	.ranking--bottom .ranking__title svg {
		color: var(--color-score-low);
	}

	.ranking__list {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	.ranking__item {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		padding: var(--space-3) 0;
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.ranking__item:last-child {
		border-bottom: none;
	}

	.ranking__rank {
		width: 28px;
		height: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: var(--text-sm);
		font-weight: var(--font-weight-bold);
		color: var(--color-text-muted);
		background: var(--color-foundation-surface);
		border-radius: var(--radius-full);
	}

	.ranking__state {
		flex: 1;
		font-size: var(--text-sm);
		color: var(--color-text-primary);
	}

	.ranking__score {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
	}

	.ranking__score.positive {
		color: var(--color-score-high);
	}

	.ranking__score.negative {
		color: var(--color-score-low);
	}

	.rankings__intro {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-6);
	}

	.rankings__grid--three {
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
	}

	.ranking__subtitle {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		margin-top: calc(var(--space-2) * -1);
		margin-bottom: var(--space-4);
	}

	.ranking__list--compact .ranking__item {
		padding: var(--space-2) 0;
	}

	.ranking__list--compact .ranking__rank {
		width: 24px;
		height: 24px;
		font-size: var(--text-xs);
	}

	.ranking__rank--bottom {
		background: var(--color-score-low);
		background: rgba(209, 104, 71, 0.15);
		color: var(--color-score-low);
	}

	.ranking__county {
		flex: 1;
		font-size: var(--text-sm);
		color: var(--color-text-primary);
	}

	.ranking__gap {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		font-weight: var(--font-weight-semibold);
		color: var(--color-warning);
		background: rgba(232, 165, 71, 0.15);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.ranking__item--gap {
		gap: var(--space-2);
	}

	/* ==========================================
	 * ACCESS
	 * ========================================== */

	.access {
		margin-bottom: var(--space-16);
	}

	.access__description {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-6);
	}

	.access__options {
		display: flex;
		flex-direction: column;
		gap: var(--space-4);
	}

	.access__option {
		display: flex;
		align-items: center;
		gap: var(--space-4);
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-4) var(--space-5);
		text-decoration: none;
		color: inherit;
		transition: all var(--duration-normal) var(--ease-out);
	}

	.access__option:hover {
		border-color: var(--color-accent-primary);
		background: var(--color-foundation-surface);
	}

	.access__option-icon {
		width: 48px;
		height: 48px;
		background: var(--color-accent-primary-glow);
		border-radius: var(--radius-lg);
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}

	.access__option-icon svg {
		width: 24px;
		height: 24px;
		color: var(--color-accent-primary);
	}

	.access__option-content {
		flex: 1;
	}

	.access__option-content h3 {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-1);
	}

	.access__option-content p {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	.access__arrow {
		width: 20px;
		height: 20px;
		color: var(--color-text-muted);
		transition: transform var(--duration-fast) var(--ease-spring);
	}

	.access__option:hover .access__arrow {
		transform: translateX(4px);
		color: var(--color-accent-primary);
	}

	/* ==========================================
	 * CITATION
	 * ========================================== */

	.citation__block {
		background: var(--color-foundation-surface);
		border: 1px solid var(--color-border-default);
		border-radius: var(--radius-lg);
		padding: var(--space-4) var(--space-5);
		margin-bottom: var(--space-4);
	}

	.citation__block code {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		word-break: break-word;
	}

	.citation__note {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	/* ==========================================
	 * BUTTONS
	 * ========================================== */

	.btn {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		gap: var(--space-2);
		padding: var(--space-3) var(--space-5);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		border-radius: var(--radius-lg);
		text-decoration: none;
		transition: all var(--duration-fast) var(--ease-out);
		cursor: pointer;
	}

	.btn--outline {
		background: transparent;
		color: var(--color-accent-primary);
		border: 1px solid var(--color-accent-primary);
	}

	.btn--outline:hover {
		background: var(--color-accent-primary);
		color: white;
	}

	.btn--primary {
		background: var(--color-accent-primary);
		color: white;
		border: none;
	}

	.btn--primary:hover {
		background: var(--color-accent-primary-hover, #6B8AFF);
		transform: translateY(-1px);
	}

	/* ==========================================
	 * RESPONSIVE
	 * ========================================== */

	@media (max-width: 640px) {
		.container {
			padding: var(--space-6) var(--space-4) var(--space-12);
		}

		.header {
			padding-top: var(--space-4);
		}

		.papers__grid,
		.findings__grid,
		.rankings__grid {
			grid-template-columns: 1fr;
		}

		.section-title {
			font-size: var(--text-xl);
		}
	}
</style>
