<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	function formatScore(score: number): string {
		return score > 0 ? `+${score.toFixed(3)}` : score.toFixed(3);
	}
</script>

<svelte:head>
	<title>The 9-Point Chasm | Community Resilience Mapping</title>
	<meta
		name="description"
		content="Within single counties, resilience scores can vary by 9+ points between the best and worst neighborhoods. Explore the widest internal gaps in America."
	/>
</svelte:head>

<div class="finding-page">
	<div class="container">
		<!-- Breadcrumb -->
		<nav class="breadcrumb" aria-label="Breadcrumb">
			<a href="/research">Research</a>
			<span aria-hidden="true">/</span>
			<span>The 9-Point Chasm</span>
		</nav>

		<!-- Header -->
		<header class="header">
			<h1 class="header__title">The 9-Point Chasm</h1>
			<p class="header__subtitle">
				Same county. Same governance. 9+ point gaps between best and worst neighborhoods.
				Internal inequality may matter more than regional differences.
			</p>
		</header>

		<!-- Key Finding Banner -->
		<section class="key-finding" aria-labelledby="key-finding-heading">
			<h2 id="key-finding-heading" class="sr-only">Key Finding</h2>
			{#if data.widestGaps[0]}
				<div class="key-finding__highlight">
					<span class="key-finding__label">Widest Internal Gap</span>
					<span class="key-finding__value">{data.widestGaps[0].internalRange.toFixed(1)} points</span>
					<span class="key-finding__location">{data.widestGaps[0].county}, {data.widestGaps[0].state}</span>
				</div>
			{/if}
			<p class="key-finding__context">
				A 9-point gap represents approximately 9 standard deviations of difference—statistically
				speaking, these are entirely different worlds despite sharing the same county government,
				school district, and local services.
			</p>
		</section>

		<!-- Top 20 Widest Gaps -->
		<section class="gaps-section" aria-labelledby="gaps-heading">
			<h2 id="gaps-heading" class="section-title">Counties with Widest Internal Gaps</h2>
			<p class="section-intro">
				Counties with at least 10 census tracts, ranked by the difference between highest and lowest resilience scores.
			</p>

			<div class="gaps-table-wrapper">
				<table class="gaps-table">
					<thead>
						<tr>
							<th>Rank</th>
							<th>County</th>
							<th>Tracts</th>
							<th>Best Tract</th>
							<th>Worst Tract</th>
							<th>Gap</th>
						</tr>
					</thead>
					<tbody>
						{#each data.widestGaps as gap, i}
							<tr>
								<td class="rank">{i + 1}</td>
								<td class="county">{gap.county}, {gap.state}</td>
								<td class="count">{gap.tractCount}</td>
								<td class="score positive">{formatScore(gap.maxResilience)}</td>
								<td class="score negative">{formatScore(gap.minResilience)}</td>
								<td class="gap-value">{gap.internalRange.toFixed(1)} pts</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</section>

		<!-- Deep Dives -->
		{#each data.countyDetails as county}
			<section class="county-deep-dive" aria-labelledby="county-{county.state}-{county.county.replace(/\s/g, '-')}">
				<h2 id="county-{county.state}-{county.county.replace(/\s/g, '-')}" class="county-title">
					{county.county}, {county.state}
					<span class="county-gap">{county.internalRange.toFixed(1)} point gap</span>
				</h2>

				<div class="county-stats">
					<span>{county.tractCount} tracts</span>
					<span>{county.population.toLocaleString()} residents</span>
					<span>Avg: {formatScore(county.avgResilience)}</span>
				</div>

				<div class="tracts-comparison">
					<!-- Best Tracts -->
					<div class="tracts-column tracts-column--best">
						<h3 class="tracts-column__title">
							<span class="indicator positive"></span>
							Highest Resilience
						</h3>
						<ul class="tract-list">
							{#each county.bestTracts as tract}
								<li class="tract-item">
									<a href="/map?tract={tract.fips}" class="tract-link">{tract.fips}</a>
									<span class="tract-score positive">{formatScore(tract.resilience)}</span>
								</li>
							{/each}
						</ul>
					</div>

					<!-- Worst Tracts -->
					<div class="tracts-column tracts-column--worst">
						<h3 class="tracts-column__title">
							<span class="indicator negative"></span>
							Lowest Resilience
						</h3>
						<ul class="tract-list">
							{#each county.worstTracts as tract}
								<li class="tract-item">
									<a href="/map?tract={tract.fips}" class="tract-link">{tract.fips}</a>
									<span class="tract-score negative">{formatScore(tract.resilience)}</span>
								</li>
							{/each}
						</ul>
					</div>
				</div>
			</section>
		{/each}

		<!-- Research Implications -->
		<section class="implications" aria-labelledby="implications-heading">
			<h2 id="implications-heading" class="section-title">Why This Matters</h2>
			<div class="implications__grid">
				<div class="implication">
					<h3>Local Matters Most</h3>
					<p>
						Neighborhood-level factors create more variation than state or even city-level policies.
						Investment, infrastructure, and social cohesion at the hyperlocal level appear to
						drive outcomes.
					</p>
				</div>
				<div class="implication">
					<h3>Concentrated Advantage</h3>
					<p>
						High-resilience tracts often cluster together, creating islands of advantage.
						Resources, access, and opportunities compound within small geographic areas.
					</p>
				</div>
				<div class="implication">
					<h3>Policy Implications</h3>
					<p>
						County-wide or city-wide interventions may miss the mark. Precision targeting
						at the neighborhood level may be more effective than broad geographic policies.
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
		background: linear-gradient(135deg, var(--color-accent-primary-glow), var(--color-accent-secondary-glow));
		border: 1px solid var(--color-accent-primary);
		border-radius: var(--radius-xl);
		padding: var(--space-8);
		margin-bottom: var(--space-12);
		text-align: center;
	}

	.key-finding__highlight {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-bottom: var(--space-6);
	}

	.key-finding__label {
		font-size: var(--text-xs);
		font-weight: var(--font-weight-bold);
		color: var(--color-accent-primary);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		margin-bottom: var(--space-2);
	}

	.key-finding__value {
		font-family: var(--font-display);
		font-size: var(--text-4xl);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
	}

	.key-finding__location {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
		margin-top: var(--space-2);
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
	}

	.gaps-section {
		margin-bottom: var(--space-12);
	}

	/* Gaps Table */
	.gaps-table-wrapper {
		overflow-x: auto;
		border-radius: var(--radius-lg);
		border: 1px solid var(--color-border-subtle);
	}

	.gaps-table {
		width: 100%;
		border-collapse: collapse;
		font-size: var(--text-sm);
	}

	.gaps-table th {
		background: var(--color-foundation-surface);
		padding: var(--space-3) var(--space-4);
		text-align: left;
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.gaps-table td {
		padding: var(--space-3) var(--space-4);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.gaps-table tbody tr:hover {
		background: var(--color-foundation-surface);
	}

	.rank {
		font-weight: var(--font-weight-bold);
		color: var(--color-text-muted);
		width: 50px;
	}

	.county {
		color: var(--color-text-primary);
	}

	.count {
		color: var(--color-text-secondary);
		text-align: center;
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

	.gap-value {
		font-family: var(--font-mono);
		font-weight: var(--font-weight-bold);
		color: var(--color-warning);
		background: rgba(232, 165, 71, 0.15);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	/* County Deep Dive */
	.county-deep-dive {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
		margin-bottom: var(--space-6);
	}

	.county-title {
		display: flex;
		align-items: center;
		gap: var(--space-4);
		font-family: var(--font-display);
		font-size: var(--text-xl);
		color: var(--color-text-primary);
		margin-bottom: var(--space-3);
	}

	.county-gap {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-bold);
		color: var(--color-warning);
		background: rgba(232, 165, 71, 0.15);
		padding: var(--space-1) var(--space-3);
		border-radius: var(--radius-full);
	}

	.county-stats {
		display: flex;
		gap: var(--space-4);
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-6);
	}

	.tracts-comparison {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: var(--space-6);
	}

	.tracts-column {
		background: var(--color-foundation-surface);
		border-radius: var(--radius-lg);
		padding: var(--space-4);
	}

	.tracts-column__title {
		display: flex;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-3);
	}

	.indicator {
		width: 8px;
		height: 8px;
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

	.tract-link {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	.tract-link:hover {
		text-decoration: underline;
	}

	.tract-score {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
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

		.county-title {
			flex-direction: column;
			align-items: flex-start;
			gap: var(--space-2);
		}
	}
</style>
