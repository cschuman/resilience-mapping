<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	function formatScore(score: number): string {
		return score > 0 ? `+${score.toFixed(3)}` : score.toFixed(3);
	}
</script>

<svelte:head>
	<title>Ohio's Health Divide: Columbus vs Cleveland | odds.health</title>
	<meta
		name="description"
		content="Columbus has 4 of America's top 10 healthiest tracts. Cleveland has 3 of the bottom 10. Same state, 140 miles apart, 10+ standard deviations different."
	/>

	<!-- Open Graph -->
	<meta property="og:type" content="article" />
	<meta property="og:title" content="Ohio's Health Divide: 140 Miles, 10+ Standard Deviations" />
	<meta
		property="og:description"
		content="Columbus has 4 of the top 10 healthiest tracts nationally. Cleveland has 3 of the bottom 10. Same state, opposite outcomes."
	/>
	<meta property="og:image" content="https://odds.health/og-ohio.svg" />
</svelte:head>

<div class="finding-page">
	<div class="container">
		<!-- Breadcrumb -->
		<nav class="breadcrumb" aria-label="Breadcrumb">
			<a href="/research">Research</a>
			<span aria-hidden="true">/</span>
			<span>Ohio's Bifurcation</span>
		</nav>

		<!-- Header -->
		<header class="header">
			<h1 class="header__title">Ohio's Bifurcation</h1>
			<p class="header__subtitle">
				Two cities. 140 miles apart. 10+ standard deviations difference in community health resilience.
			</p>
		</header>

		<!-- Key Finding Banner -->
		<section class="key-finding" aria-labelledby="key-finding-heading">
			<h2 id="key-finding-heading" class="sr-only">Key Finding</h2>
			<div class="key-finding__stat-row">
				<div class="key-finding__stat key-finding__stat--positive">
					<span class="key-finding__city">Columbus</span>
					<span class="key-finding__value">{formatScore(data.columbus.stats?.avgResilience ?? 0)}</span>
					<span class="key-finding__label">Avg Resilience</span>
				</div>
				<div class="key-finding__vs">VS</div>
				<div class="key-finding__stat key-finding__stat--negative">
					<span class="key-finding__city">Cleveland</span>
					<span class="key-finding__value">{formatScore(data.cleveland.stats?.avgResilience ?? 0)}</span>
					<span class="key-finding__label">Avg Resilience</span>
				</div>
			</div>
			<p class="key-finding__context">
				Columbus (Franklin County) has some of the nation's top-performing tracts,
				while Cleveland (Cuyahoga County) contains several of the nation's most struggling communities.
				Same state. Same policies. Dramatically different outcomes.
			</p>
		</section>

		<!-- Columbus Section -->
		<section class="city-section" aria-labelledby="columbus-heading">
			<div class="city-section__header">
				<h2 id="columbus-heading" class="city-section__title">
					<span class="city-section__icon city-section__icon--positive">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
							<path fill-rule="evenodd" d="M10 17a.75.75 0 01-.75-.75V5.612L5.29 9.77a.75.75 0 01-1.08-1.04l5.25-5.5a.75.75 0 011.08 0l5.25 5.5a.75.75 0 11-1.08 1.04l-3.96-4.158V16.25A.75.75 0 0110 17z" clip-rule="evenodd" />
						</svg>
					</span>
					Columbus (Franklin County)
				</h2>
				{#if data.columbus.stats}
					<div class="city-section__summary">
						<span>{data.columbus.stats.tractCount} tracts</span>
						<span>{data.columbus.stats.population.toLocaleString()} residents</span>
						<span class="positive">Avg: {formatScore(data.columbus.stats.avgResilience)}</span>
					</div>
				{/if}
			</div>

			<p class="city-section__description">
				Ohio's capital city showcases what's possible. Home to Ohio State University, a diversified economy,
				and significant investment in community health infrastructure, Columbus tracts consistently
				outperform predictions.
			</p>

			<h3 class="subsection-title">Top 10 Highest-Resilience Tracts</h3>
			<div class="tract-table-wrapper">
				<table class="tract-table">
					<thead>
						<tr>
							<th>Tract</th>
							<th>Population</th>
							<th>Resilience</th>
							<th>Burden</th>
						</tr>
					</thead>
					<tbody>
						{#each data.columbus.topTracts as tract}
							<tr>
								<td>
									<a href="/map?tract={tract.fips}" class="tract-link">{tract.fips}</a>
								</td>
								<td>{tract.population.toLocaleString()}</td>
								<td class="score positive">{formatScore(tract.resilience)}</td>
								<td class="score" class:negative={tract.burden > 0}>{formatScore(tract.burden)}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</section>

		<!-- Cleveland Section -->
		<section class="city-section" aria-labelledby="cleveland-heading">
			<div class="city-section__header">
				<h2 id="cleveland-heading" class="city-section__title">
					<span class="city-section__icon city-section__icon--negative">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
							<path fill-rule="evenodd" d="M10 3a.75.75 0 01.75.75v10.638l3.96-4.158a.75.75 0 111.08 1.04l-5.25 5.5a.75.75 0 01-1.08 0l-5.25-5.5a.75.75 0 111.08-1.04l3.96 4.158V3.75A.75.75 0 0110 3z" clip-rule="evenodd" />
						</svg>
					</span>
					Cleveland (Cuyahoga County)
				</h2>
				{#if data.cleveland.stats}
					<div class="city-section__summary">
						<span>{data.cleveland.stats.tractCount} tracts</span>
						<span>{data.cleveland.stats.population.toLocaleString()} residents</span>
						<span class="negative">Avg: {formatScore(data.cleveland.stats.avgResilience)}</span>
					</div>
				{/if}
			</div>

			<p class="city-section__description">
				Cleveland's deindustrialization, population decline, and concentrated poverty create
				compounding challenges. Several census tracts show resilience scores among the lowest in the nation,
				with internal inequality creating a 9+ point chasm between best and worst neighborhoods.
			</p>

			<h3 class="subsection-title">10 Most Struggling Tracts</h3>
			<div class="tract-table-wrapper">
				<table class="tract-table">
					<thead>
						<tr>
							<th>Tract</th>
							<th>Population</th>
							<th>Resilience</th>
							<th>Burden</th>
						</tr>
					</thead>
					<tbody>
						{#each data.cleveland.bottomTracts as tract}
							<tr>
								<td>
									<a href="/map?tract={tract.fips}" class="tract-link">{tract.fips}</a>
								</td>
								<td>{tract.population.toLocaleString()}</td>
								<td class="score negative">{formatScore(tract.resilience)}</td>
								<td class="score" class:negative={tract.burden > 0}>{formatScore(tract.burden)}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</section>

		<!-- Research Implications -->
		<section class="implications" aria-labelledby="implications-heading">
			<h2 id="implications-heading" class="section-title">Why This Matters</h2>
			<div class="implications__grid">
				<div class="implication">
					<h3>Same State, Different Worlds</h3>
					<p>
						Both cities operate under the same state policies, yet produce dramatically different
						health outcomes. This suggests local factors—investment, infrastructure, economic
						diversification—may matter more than state-level policy.
					</p>
				</div>
				<div class="implication">
					<h3>Deindustrialization Legacy</h3>
					<p>
						Cleveland's decline tracks manufacturing job losses from the 1970s-2000s.
						Communities built around single industries face compounding challenges
						when those industries disappear.
					</p>
				</div>
				<div class="implication">
					<h3>University Effect</h3>
					<p>
						Columbus benefits from Ohio State University's economic engine, healthcare
						infrastructure, and stable employment base—factors that appear to create
						resilience even in surrounding neighborhoods.
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

	/* Breadcrumb */
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

	/* Header */
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
		align-items: center;
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

	.key-finding__stat--positive {
		background: var(--color-score-high-bg);
		border: 2px solid var(--color-score-high);
	}

	.key-finding__stat--negative {
		background: var(--color-score-low-bg);
		border: 2px solid var(--color-score-low);
	}

	.key-finding__city {
		font-size: var(--text-sm);
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
	}

	.key-finding__stat--positive .key-finding__value {
		color: var(--color-score-high);
	}

	.key-finding__stat--negative .key-finding__value {
		color: var(--color-score-low);
	}

	.key-finding__label {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.key-finding__vs {
		font-size: var(--text-lg);
		font-weight: var(--font-weight-bold);
		color: var(--color-text-muted);
	}

	.key-finding__context {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		max-width: 600px;
		margin: 0 auto;
		line-height: var(--leading-relaxed);
	}

	/* City Sections */
	.city-section {
		margin-bottom: var(--space-12);
	}

	.city-section__header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: var(--space-4);
		margin-bottom: var(--space-4);
		flex-wrap: wrap;
	}

	.city-section__title {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		font-family: var(--font-display);
		font-size: var(--text-xl);
		color: var(--color-text-primary);
	}

	.city-section__icon {
		width: 32px;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: var(--radius-full);
	}

	.city-section__icon svg {
		width: 20px;
		height: 20px;
	}

	.city-section__icon--positive {
		background: var(--color-score-high-bg);
		color: var(--color-score-high);
	}

	.city-section__icon--negative {
		background: var(--color-score-low-bg);
		color: var(--color-score-low);
	}

	.city-section__summary {
		display: flex;
		gap: var(--space-4);
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	.city-section__description {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-6);
		max-width: 800px;
	}

	.subsection-title {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-4);
	}

	/* Tables */
	.tract-table-wrapper {
		overflow-x: auto;
		border-radius: var(--radius-lg);
		border: 1px solid var(--color-border-subtle);
	}

	.tract-table {
		width: 100%;
		border-collapse: collapse;
		font-size: var(--text-sm);
	}

	.tract-table th {
		background: var(--color-foundation-surface);
		padding: var(--space-3) var(--space-4);
		text-align: left;
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.tract-table td {
		padding: var(--space-3) var(--space-4);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.tract-table tbody tr:last-child td {
		border-bottom: none;
	}

	.tract-table tbody tr:hover {
		background: var(--color-foundation-surface);
	}

	.tract-link {
		font-family: var(--font-mono);
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	.tract-link:hover {
		text-decoration: underline;
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

	.positive {
		color: var(--color-score-high);
	}

	.negative {
		color: var(--color-score-low);
	}

	/* Implications */
	.section-title {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		color: var(--color-text-primary);
		margin-bottom: var(--space-6);
		padding-bottom: var(--space-3);
		border-bottom: 1px solid var(--color-border-subtle);
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

		.city-section__header {
			flex-direction: column;
		}
	}
</style>
