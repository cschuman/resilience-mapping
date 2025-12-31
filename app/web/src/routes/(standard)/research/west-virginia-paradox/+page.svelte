<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

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

	function formatScore(score: number): string {
		return score > 0 ? `+${score.toFixed(3)}` : score.toFixed(3);
	}
</script>

<svelte:head>
	<title>West Virginia Paradox | Community Resilience Mapping</title>
	<meta
		name="description"
		content="West Virginia has the highest health burden in America, yet near-average resilience. What protective factors are at play?"
	/>
</svelte:head>

<div class="finding-page">
	<div class="container">
		<!-- Breadcrumb -->
		<nav class="breadcrumb" aria-label="Breadcrumb">
			<a href="/research">Research</a>
			<span aria-hidden="true">/</span>
			<span>West Virginia Paradox</span>
		</nav>

		<!-- Header -->
		<header class="header">
			<h1 class="header__title">The West Virginia Paradox</h1>
			<p class="header__subtitle">
				America's highest health burden. Near-average resilience.
				Something is protecting these communities beyond what the numbers predict.
			</p>
		</header>

		<!-- Key Finding Banner -->
		<section class="key-finding" aria-labelledby="key-finding-heading">
			<h2 id="key-finding-heading" class="sr-only">Key Finding</h2>
			{#if data.westVirginia}
				<div class="key-finding__stat-row">
					<div class="key-finding__stat key-finding__stat--burden">
						<span class="key-finding__label">Avg Health Burden</span>
						<span class="key-finding__value">{formatScore(data.westVirginia.avgBurden)}</span>
						<span class="key-finding__rank">#1 in America</span>
					</div>
					<div class="key-finding__stat key-finding__stat--resilience">
						<span class="key-finding__label">Avg Resilience</span>
						<span class="key-finding__value">{formatScore(data.westVirginia.avgResilience)}</span>
						<span class="key-finding__rank">Near average</span>
					</div>
				</div>
			{/if}
			<p class="key-finding__context">
				If resilience were purely determined by health burden, West Virginia should be at the bottom.
				Instead, tight-knit communities, multi-generational networks, and cultural factors
				appear to provide unmeasured protective effects.
			</p>
		</section>

		<!-- State Comparison -->
		<section class="comparison" aria-labelledby="comparison-heading">
			<h2 id="comparison-heading" class="section-title">Highest Burden States Compared</h2>
			<p class="section-intro">
				States ranked by average health burden. Note how resilience doesn't track linearly with burden.
			</p>

			<div class="comparison-table-wrapper">
				<table class="comparison-table">
					<thead>
						<tr>
							<th>Rank</th>
							<th>State</th>
							<th>Avg Burden</th>
							<th>Avg Resilience</th>
							<th>Population</th>
						</tr>
					</thead>
					<tbody>
						{#each data.stateComparison as state, i}
							<tr class:highlighted={state.state === 'WV'}>
								<td class="rank">{i + 1}</td>
								<td class="state">{STATE_NAMES[state.state] || state.state}</td>
								<td class="score negative">{formatScore(state.avgBurden)}</td>
								<td class="score" class:positive={state.avgResilience > 0} class:negative={state.avgResilience < 0}>
									{formatScore(state.avgResilience)}
								</td>
								<td class="population">{(state.population / 1_000_000).toFixed(1)}M</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</section>

		<!-- WV Counties -->
		<section class="counties" aria-labelledby="counties-heading">
			<h2 id="counties-heading" class="section-title">West Virginia Counties</h2>
			<p class="section-intro">
				County-level breakdown reveals significant variation within the state.
				University towns like Monongalia (WVU) show particularly high resilience.
			</p>

			<div class="counties-grid">
				{#each data.counties.slice(0, 12) as county}
					<div class="county-card" class:positive={county.avgResilience > 0}>
						<div class="county-card__header">
							<span class="county-card__name">{county.county}</span>
							<span class="county-card__score" class:positive={county.avgResilience > 0} class:negative={county.avgResilience < 0}>
								{formatScore(county.avgResilience)}
							</span>
						</div>
						<div class="county-card__stats">
							<span>{county.tractCount} tracts</span>
							<span>Burden: {formatScore(county.avgBurden)}</span>
						</div>
					</div>
				{/each}
			</div>
		</section>

		<!-- Tract Details -->
		<section class="tracts-section" aria-labelledby="tracts-heading">
			<h2 id="tracts-heading" class="section-title">Most and Least Resilient Tracts</h2>

			<div class="tracts-grid">
				<!-- Top Tracts -->
				<div class="tracts-panel">
					<h3 class="tracts-panel__title">
						<span class="indicator positive"></span>
						Highest Resilience
					</h3>
					<ul class="tract-list">
						{#each data.topTracts as tract}
							<li class="tract-item">
								<div class="tract-item__info">
									<a href="/map?tract={tract.fips}" class="tract-link">{tract.fips}</a>
									<span class="tract-county">{tract.county}</span>
								</div>
								<span class="tract-score positive">{formatScore(tract.resilience)}</span>
							</li>
						{/each}
					</ul>
				</div>

				<!-- Bottom Tracts -->
				<div class="tracts-panel">
					<h3 class="tracts-panel__title">
						<span class="indicator negative"></span>
						Lowest Resilience
					</h3>
					<ul class="tract-list">
						{#each data.bottomTracts as tract}
							<li class="tract-item">
								<div class="tract-item__info">
									<a href="/map?tract={tract.fips}" class="tract-link">{tract.fips}</a>
									<span class="tract-county">{tract.county}</span>
								</div>
								<span class="tract-score negative">{formatScore(tract.resilience)}</span>
							</li>
						{/each}
					</ul>
				</div>
			</div>
		</section>

		<!-- Research Implications -->
		<section class="implications" aria-labelledby="implications-heading">
			<h2 id="implications-heading" class="section-title">Possible Explanations</h2>
			<div class="implications__grid">
				<div class="implication">
					<h3>Social Cohesion</h3>
					<p>
						West Virginia's population has lower mobility than most states.
						Multi-generational families and tight-knit communities may provide
						informal support systems that buffer against health challenges.
					</p>
				</div>
				<div class="implication">
					<h3>Adapted Expectations</h3>
					<p>
						Communities may have developed coping mechanisms over generations
						of economic challenge. Cultural resilience and community identity
						could provide psychological protective factors.
					</p>
				</div>
				<div class="implication">
					<h3>University Effect</h3>
					<p>
						Monongalia County (home to WVU) shows dramatically higher resilience.
						Educational infrastructure creates spillover benefits that
						extend beyond the campus.
					</p>
				</div>
				<div class="implication">
					<h3>Measurement Limitations</h3>
					<p>
						Our burden index may not capture all relevant factors.
						The paradox could also reflect unmeasured protective factors
						or limitations in how we measure health outcomes.
					</p>
				</div>
			</div>
		</section>

		<!-- Back Link -->
		<nav class="back-nav" aria-label="Back navigation">
			<a href="/research" class="back-link">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
					<path fill-rule="evenodd" d="M17 10a.75.75 0 01-.75.75H5.612l4.158 3.96a.75.75 0 11-1.04 1.08l-5.5-5.25a.75.75 0 010-1.08l5.5-5.25a.75.75 0 111.04 1.08L5.612 9.25H16.25A.75.75 0 0117 10z" clip-rule="evenodd" />
				</svg>
				Back to Research
			</a>
		</nav>
	</div>
</div>

<style>
	.finding-page {
		color: var(--color-text-primary);
	}

	.container {
		max-width: var(--container-lg);
		margin: 0 auto;
		padding: var(--space-8) var(--space-6) var(--space-16);
	}

	.breadcrumb {
		display: flex;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		margin-bottom: var(--space-4);
	}

	.breadcrumb a {
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	.breadcrumb a:hover {
		text-decoration: underline;
	}

	.header {
		margin-bottom: var(--space-8);
	}

	.header__title {
		font-family: var(--font-display);
		font-size: clamp(var(--text-2xl), 4vw, var(--text-3xl));
		color: var(--color-text-primary);
		margin-bottom: var(--space-3);
	}

	.header__subtitle {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
		max-width: 700px;
	}

	/* Key Finding */
	.key-finding {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-8);
		margin-bottom: var(--space-12);
		text-align: center;
	}

	.key-finding__stat-row {
		display: flex;
		justify-content: center;
		gap: var(--space-6);
		margin-bottom: var(--space-6);
		flex-wrap: wrap;
	}

	.key-finding__stat {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: var(--space-4) var(--space-6);
		border-radius: var(--radius-lg);
		min-width: 180px;
	}

	.key-finding__stat--burden {
		background: var(--color-score-low-bg);
		border: 2px solid var(--color-score-low);
	}

	.key-finding__stat--resilience {
		background: var(--color-foundation-surface);
		border: 2px solid var(--color-border-default);
	}

	.key-finding__label {
		font-size: var(--text-xs);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-secondary);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wider);
		margin-bottom: var(--space-2);
	}

	.key-finding__value {
		font-family: var(--font-mono);
		font-size: var(--text-3xl);
		font-weight: var(--font-weight-bold);
		color: var(--color-text-primary);
	}

	.key-finding__stat--burden .key-finding__value {
		color: var(--color-score-low);
	}

	.key-finding__rank {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		margin-top: var(--space-1);
	}

	.key-finding__context {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		max-width: 600px;
		margin: 0 auto;
		line-height: var(--leading-relaxed);
	}

	/* Sections */
	.section-title {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		color: var(--color-text-primary);
		margin-bottom: var(--space-3);
		padding-bottom: var(--space-3);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.section-intro {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-6);
		max-width: 700px;
	}

	.comparison, .counties, .tracts-section {
		margin-bottom: var(--space-12);
	}

	/* Comparison Table */
	.comparison-table-wrapper {
		overflow-x: auto;
		border-radius: var(--radius-lg);
		border: 1px solid var(--color-border-subtle);
	}

	.comparison-table {
		width: 100%;
		border-collapse: collapse;
		font-size: var(--text-sm);
	}

	.comparison-table th {
		background: var(--color-foundation-surface);
		padding: var(--space-3) var(--space-4);
		text-align: left;
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.comparison-table td {
		padding: var(--space-3) var(--space-4);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.comparison-table tr.highlighted {
		background: var(--color-accent-primary-glow);
	}

	.comparison-table tr.highlighted td {
		font-weight: var(--font-weight-semibold);
	}

	.rank {
		font-weight: var(--font-weight-bold);
		color: var(--color-text-muted);
		width: 50px;
	}

	.state {
		color: var(--color-text-primary);
	}

	.score {
		font-family: var(--font-mono);
		font-weight: var(--font-weight-medium);
	}

	.score.positive {
		color: var(--color-score-high);
	}

	.score.negative {
		color: var(--color-score-low);
	}

	.population {
		color: var(--color-text-secondary);
	}

	/* Counties Grid */
	.counties-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
		gap: var(--space-4);
	}

	.county-card {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-lg);
		padding: var(--space-4);
		transition: all var(--duration-fast) var(--ease-out);
	}

	.county-card:hover {
		border-color: var(--color-accent-primary);
	}

	.county-card.positive {
		border-left: 3px solid var(--color-score-high);
	}

	.county-card__header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--space-2);
	}

	.county-card__name {
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
	}

	.county-card__score {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-bold);
	}

	.county-card__score.positive {
		color: var(--color-score-high);
	}

	.county-card__score.negative {
		color: var(--color-score-low);
	}

	.county-card__stats {
		display: flex;
		gap: var(--space-3);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	/* Tracts Grid */
	.tracts-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
		gap: var(--space-6);
	}

	.tracts-panel {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-5);
	}

	.tracts-panel__title {
		display: flex;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-4);
		padding-bottom: var(--space-3);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.indicator {
		width: 10px;
		height: 10px;
		border-radius: var(--radius-full);
	}

	.indicator.positive {
		background: var(--color-score-high);
	}

	.indicator.negative {
		background: var(--color-score-low);
	}

	.tract-list {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	.tract-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: var(--space-2) 0;
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.tract-item:last-child {
		border-bottom: none;
	}

	.tract-item__info {
		display: flex;
		flex-direction: column;
		gap: var(--space-1);
	}

	.tract-link {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	.tract-link:hover {
		text-decoration: underline;
	}

	.tract-county {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.tract-score {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-bold);
	}

	.tract-score.positive {
		color: var(--color-score-high);
	}

	.tract-score.negative {
		color: var(--color-score-low);
	}

	.positive {
		color: var(--color-score-high);
	}

	.negative {
		color: var(--color-score-low);
	}

	/* Implications */
	.implications {
		margin-top: var(--space-12);
	}

	.implications__grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: var(--space-6);
	}

	.implication {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
	}

	.implication h3 {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.implication p {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	/* Back Navigation */
	.back-nav {
		margin-top: var(--space-8);
		padding-top: var(--space-6);
		border-top: 1px solid var(--color-border-subtle);
	}

	.back-link {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		color: var(--color-accent-primary);
		text-decoration: none;
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
	}

	.back-link:hover {
		text-decoration: underline;
	}

	.back-link svg {
		width: 18px;
		height: 18px;
	}

	.sr-only {
		position: absolute;
		width: 1px;
		height: 1px;
		padding: 0;
		margin: -1px;
		overflow: hidden;
		clip: rect(0, 0, 0, 0);
		white-space: nowrap;
		border: 0;
	}

	@media (max-width: 640px) {
		.container {
			padding: var(--space-6) var(--space-4) var(--space-12);
		}

		.key-finding__stat-row {
			flex-direction: column;
		}
	}
</style>
