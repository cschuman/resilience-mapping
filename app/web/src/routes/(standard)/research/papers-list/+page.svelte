<script lang="ts">
	const papers = [
		{
			number: 5,
			title: 'Beyond the Hispanic Paradox: Immigrant Health Advantage, Structural Poverty, and the Aggregation Artifact',
			summary: 'The "Hispanic Paradox" is an aggregation artifact. Black immigrants show stronger health advantage than Hispanic immigrants.',
			abstract: 'The "Hispanic Paradox" is an aggregation artifact: South American (r=+0.147) vs Mexican (r=-0.029) cancel to r≈0. Black immigrants show STRONGER health advantage than Hispanic immigrants. Same ethnicity, same state: Austin (+1.53 SD) vs Border (-1.08 SD)—2.61 SD gap.',
			status: 'preprint',
			date: 'January 2026',
			topics: ['Hispanic Paradox', 'Immigrant Health', 'Texas Border'],
			href: '/research/papers/immigrant-health-advantage',
			featured: true
		},
		{
			number: 4,
			title: 'Structural Correlates of Community Health Resilience: A Cross-Sectional Analysis of 53,889 U.S. Census Tracts',
			summary: 'A 0.43 SD resilience gap exists between majority-white and majority-minority communities.',
			abstract: 'A 0.43 SD resilience gap exists between majority-white and majority-minority communities. But state variation from +1.87 SD (DC) to -0.42 SD (Washington) proves structural factors—not immutable characteristics—determine resilience. Education is the strongest correlate (r=+0.41).',
			status: 'preprint',
			date: 'January 2026',
			topics: ['Health Equity', 'Racial Disparities', 'State Variation'],
			href: '/research/papers/health-equity',
			featured: false
		},
		{
			number: 3,
			title: 'Structural Determinants of Community Health Resilience: A Tract-Level Analysis of 53,889 U.S. Communities',
			summary: 'State variation proves structural factors—not race—determine resilience.',
			abstract: 'A 0.38 SD resilience gap exists between majority-white and majority-minority communities. But state variation from +1.87 SD (DC) to -0.53 SD (Oregon) proves structural factors—not race—determine resilience. Education is the strongest correlate (r=+0.41).',
			status: 'preprint',
			date: 'December 2025',
			topics: ['Health Equity', 'Racial Disparities', 'Structural Determinants'],
			href: '/research/papers/structural-determinants',
			featured: false
		},
		{
			number: 2,
			title: 'Regression to the Mean in Small-Area Health Estimates: Why Trajectory Prediction Fails',
			summary: 'Extreme year-over-year changes regress to the mean, not genuine health dynamics.',
			abstract: 'We tried to predict which communities would get healthier or sicker—and failed completely (F1=0.26, chance performance). The "quintile gradient" reveals why: extreme year-over-year changes regress to the mean, not genuine health dynamics.',
			status: 'preprint',
			date: 'December 2025',
			topics: ['Regression to Mean', 'Measurement Error', 'Prediction'],
			href: '/research/papers/regression-to-mean',
			featured: false
		},
		{
			number: 1,
			title: 'Spatial Synchrony, Not Contagion: A Methodological Correction in Community Health Trajectory Prediction',
			summary: 'Communities change together, but neighbor trajectories do not predict future outcomes.',
			abstract: 'We demonstrate that apparent "spatial contagion" in community health trajectories was an artifact of temporal data leakage. Communities exhibit spatial synchrony—they change together—but prior neighbor trajectories do not predict future focal trajectories.',
			status: 'preprint',
			date: 'December 2025',
			topics: ['Spatial Epidemiology', 'Methodology', 'CDC PLACES'],
			href: '/research/papers/spatial-synchrony',
			featured: false
		}
	];

	let showFullAbstracts = $state(false);
</script>

<svelte:head>
	<title>Research Papers | odds.health</title>
	<meta
		name="description"
		content="Academic research papers on community health resilience, methodology, and health equity from the odds.health project."
	/>
</svelte:head>

<div class="papers-page">
	<div class="container">
		<nav class="breadcrumb" aria-label="Breadcrumb">
			<a href="/research">Research</a>
			<span class="separator">/</span>
			<span class="current">Papers</span>
		</nav>

		<header class="header">
			<h1 class="header__title">Research Papers</h1>
			<p class="header__subtitle">
				Peer-reviewed and pre-print publications from the Community Health Resilience project.
				All papers are open access.
			</p>
		</header>

		<div class="controls">
			<label class="toggle">
				<input type="checkbox" bind:checked={showFullAbstracts} />
				<span class="toggle__label">Show full abstracts</span>
			</label>
		</div>

		<div class="papers">
			{#each papers as paper}
				<article class="paper" class:paper--featured={paper.featured}>
					<div class="paper__header">
						<span class="paper__number">Paper {paper.number}</span>
						{#if paper.featured}
							<span class="paper__badge">Latest</span>
						{/if}
					</div>

					<h2 class="paper__title">
						<a href={paper.href}>{paper.title}</a>
					</h2>

					<p class="paper__abstract">
						{showFullAbstracts ? paper.abstract : paper.summary}
					</p>

					<div class="paper__meta">
						<span class="paper__status">{paper.status}</span>
						<span class="paper__date">{paper.date}</span>
					</div>

					<div class="paper__topics">
						{#each paper.topics as topic}
							<span class="topic">{topic}</span>
						{/each}
					</div>

					<a href={paper.href} class="paper__link">
						Read full paper
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
							<path fill-rule="evenodd" d="M3 10a.75.75 0 01.75-.75h10.638L10.23 5.29a.75.75 0 111.04-1.08l5.5 5.25a.75.75 0 010 1.08l-5.5 5.25a.75.75 0 11-1.04-1.08l4.158-3.96H3.75A.75.75 0 013 10z" clip-rule="evenodd" />
						</svg>
					</a>
				</article>
			{/each}
		</div>

		<section class="citation">
			<h2>How to Cite</h2>
			<div class="citation__block">
				<code>Community Resilience Mapping Project (2026). Census tract-level health resilience scores for the United States. https://odds.health</code>
			</div>
		</section>
	</div>
</div>

<style>
	.papers-page {
		color: var(--color-text-primary);
	}

	.container {
		max-width: var(--container-md);
		margin: 0 auto;
		padding: var(--space-8) var(--space-6) var(--space-16);
	}

	.breadcrumb {
		display: flex;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-sm);
		margin-bottom: var(--space-6);
	}

	.breadcrumb a {
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	.breadcrumb a:hover {
		text-decoration: underline;
	}

	.breadcrumb .separator {
		color: var(--color-text-muted);
	}

	.breadcrumb .current {
		color: var(--color-text-secondary);
	}

	.header {
		margin-bottom: var(--space-8);
	}

	.header__title {
		font-family: var(--font-display);
		font-size: var(--text-3xl);
		font-weight: var(--font-weight-normal);
		margin-bottom: var(--space-3);
	}

	.header__subtitle {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		max-width: 600px;
	}

	.controls {
		margin-bottom: var(--space-8);
		padding: var(--space-4);
		background: var(--color-foundation-mid);
		border-radius: var(--radius-lg);
	}

	.toggle {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		cursor: pointer;
	}

	.toggle input {
		width: 18px;
		height: 18px;
		accent-color: var(--color-accent-primary);
	}

	.toggle__label {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	.papers {
		display: flex;
		flex-direction: column;
		gap: var(--space-6);
		margin-bottom: var(--space-12);
	}

	.paper {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
	}

	.paper--featured {
		border-color: var(--color-accent-primary);
		background: linear-gradient(135deg, var(--color-foundation-mid), var(--color-accent-primary-glow));
	}

	.paper__header {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		margin-bottom: var(--space-3);
	}

	.paper__number {
		font-size: var(--text-xs);
		font-weight: var(--font-weight-bold);
		color: var(--color-accent-primary);
		background: var(--color-accent-primary-glow);
		padding: var(--space-1) var(--space-3);
		border-radius: var(--radius-full);
	}

	.paper__badge {
		font-size: var(--text-xs);
		font-weight: var(--font-weight-bold);
		color: var(--color-score-high);
		background: var(--color-score-high-bg);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.paper__title {
		font-size: var(--text-xl);
		font-weight: var(--font-weight-semibold);
		line-height: var(--leading-tight);
		margin-bottom: var(--space-3);
	}

	.paper__title a {
		color: var(--color-text-primary);
		text-decoration: none;
	}

	.paper__title a:hover {
		color: var(--color-accent-primary);
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
		color: var(--color-accent-secondary);
		background: var(--color-accent-secondary-glow);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
		text-transform: capitalize;
	}

	.paper__date {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		display: flex;
		align-items: center;
	}

	.paper__topics {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-2);
		margin-bottom: var(--space-4);
	}

	.topic {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		background: var(--color-foundation-surface);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
		border: 1px solid var(--color-border-subtle);
	}

	.paper__link {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	.paper__link:hover {
		text-decoration: underline;
	}

	.paper__link svg {
		width: 16px;
		height: 16px;
	}

	.citation {
		padding-top: var(--space-8);
		border-top: 1px solid var(--color-border-subtle);
	}

	.citation h2 {
		font-size: var(--text-lg);
		font-weight: var(--font-weight-semibold);
		margin-bottom: var(--space-4);
	}

	.citation__block {
		background: var(--color-foundation-surface);
		border: 1px solid var(--color-border-default);
		border-radius: var(--radius-lg);
		padding: var(--space-4);
	}

	.citation__block code {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		word-break: break-word;
	}

	@media (max-width: 640px) {
		.container {
			padding: var(--space-6) var(--space-4) var(--space-12);
		}
	}
</style>
