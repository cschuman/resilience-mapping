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
	<title>Research | odds.health</title>
	<meta
		name="description"
		content="Community health resilience research: papers, findings, and state/county rankings from the odds.health project."
	/>
</svelte:head>

<div class="research">
	<div class="container">
		<!-- Header -->
		<header class="header">
			<h1 class="header__title">Research</h1>
			<p class="header__subtitle">
				Findings, papers, and rankings from the Community Health Resilience project.
			</p>
		</header>

		<!-- Quick Navigation -->
		<nav class="nav-cards" aria-label="Research sections">
			<a href="#findings" class="nav-card">
				<div class="nav-card__icon">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
						<path fill-rule="evenodd" d="M9 4.5a.75.75 0 01.721.544l.813 2.846a3.75 3.75 0 002.576 2.576l2.846.813a.75.75 0 010 1.442l-2.846.813a3.75 3.75 0 00-2.576 2.576l-.813 2.846a.75.75 0 01-1.442 0l-.813-2.846a3.75 3.75 0 00-2.576-2.576l-2.846-.813a.75.75 0 010-1.442l2.846-.813A3.75 3.75 0 007.466 7.89l.813-2.846A.75.75 0 019 4.5z" clip-rule="evenodd" />
					</svg>
				</div>
				<div class="nav-card__content">
					<h2>Key Findings</h2>
					<p>Surprising discoveries that challenge assumptions</p>
				</div>
			</a>

			<a href="/research/papers-list" class="nav-card">
				<div class="nav-card__icon">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
						<path d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0016.5 9h-1.875a1.875 1.875 0 01-1.875-1.875V5.25A3.75 3.75 0 009 1.5H5.625z" />
						<path d="M12.971 1.816A5.23 5.23 0 0114.25 5.25v1.875c0 .207.168.375.375.375H16.5a5.23 5.23 0 013.434 1.279 9.768 9.768 0 00-6.963-6.963z" />
					</svg>
				</div>
				<div class="nav-card__content">
					<h2>Research Papers</h2>
					<p>5 pre-print publications</p>
				</div>
			</a>

			<a href="/research/rankings" class="nav-card">
				<div class="nav-card__icon">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
						<path fill-rule="evenodd" d="M3 6a3 3 0 013-3h12a3 3 0 013 3v12a3 3 0 01-3 3H6a3 3 0 01-3-3V6zm4.5 7.5a.75.75 0 01.75.75v2.25a.75.75 0 01-1.5 0v-2.25a.75.75 0 01.75-.75zm3.75-1.5a.75.75 0 00-1.5 0v4.5a.75.75 0 001.5 0V12zm2.25-3a.75.75 0 01.75.75v6.75a.75.75 0 01-1.5 0V9.75a.75.75 0 01.75-.75zm3.75-1.5a.75.75 0 00-1.5 0v9a.75.75 0 001.5 0v-9z" clip-rule="evenodd" />
					</svg>
				</div>
				<div class="nav-card__content">
					<h2>Rankings</h2>
					<p>All {data.stats.stateCount} states and {data.stats.countyCount}+ counties</p>
				</div>
			</a>
		</nav>

		<!-- Featured Finding -->
		<section class="featured" aria-labelledby="featured-heading">
			<div class="featured__badge">Featured Discovery</div>
			<h2 id="featured-heading" class="featured__title">
				College Towns vs Prison Towns: A 4 SD Health Divide
			</h2>
			<p class="featured__text">
				College communities average <strong class="positive">+2.95</strong> resilience.
				Prison communities average <strong class="negative">-0.98</strong>.
				Same country, same healthcare system—4 standard deviations apart.
			</p>
			<a href="/research/special-populations" class="featured__link">
				Explore Special Populations →
			</a>
		</section>

		<!-- Key Findings Preview -->
		<section id="findings" class="section">
			<div class="section__header">
				<h2 class="section__title">Key Findings</h2>
			</div>

			<div class="findings-grid">
				<a href="/research/special-populations" class="finding-card finding-card--featured">
					<h3>The 4 Standard Deviation Gap</h3>
					<p>
						College communities average <strong class="positive">+2.95</strong> resilience
						while prison communities average <strong class="negative">-0.98</strong>.
					</p>
					<span class="finding-card__link">Explore →</span>
				</a>

				<a href="/research/ohio-bifurcation" class="finding-card">
					<h3>Ohio's Bifurcation</h3>
					<p>
						Columbus has 4 of the nation's top 10 tracts.
						Cleveland has 3 of the bottom 10. Same state, 10+ SD apart.
					</p>
					<span class="finding-card__link">Explore →</span>
				</a>

				<a href="/research/inequality-chasm" class="finding-card">
					<h3>The 9-Point Chasm</h3>
					<p>
						Cleveland and New Orleans each have 9+ point gaps between their
						best and worst neighborhoods.
					</p>
					<span class="finding-card__link">Explore →</span>
				</a>

				<a href="/research/west-virginia-paradox" class="finding-card">
					<h3>West Virginia Paradox</h3>
					<p>
						Highest health burden in America, yet resilience near average.
						Something is protecting these communities.
					</p>
					<span class="finding-card__link">Explore →</span>
				</a>
			</div>
		</section>

		<!-- Papers Preview -->
		<section class="section">
			<div class="section__header">
				<h2 class="section__title">Latest Papers</h2>
				<a href="/research/papers-list" class="section__link">View all 5 papers →</a>
			</div>

			<div class="papers-preview">
				<a href="/research/papers/immigrant-health-advantage" class="paper-card paper-card--featured">
					<span class="paper-card__badge">New</span>
					<h3>Beyond the Hispanic Paradox</h3>
					<p>The "Hispanic Paradox" is an aggregation artifact. Black immigrants show stronger health advantage than Hispanic immigrants.</p>
				</a>

				<a href="/research/papers/health-equity" class="paper-card">
					<h3>Structural Correlates of Resilience</h3>
					<p>A 0.43 SD gap exists, but state variation proves structural factors—not race—determine resilience.</p>
				</a>

				<a href="/research/papers/spatial-synchrony" class="paper-card">
					<h3>Spatial Synchrony, Not Contagion</h3>
					<p>Communities change together, but neighbor trajectories don't predict future outcomes.</p>
				</a>
			</div>
		</section>

		<!-- Rankings Preview -->
		<section class="section">
			<div class="section__header">
				<h2 class="section__title">State Rankings</h2>
				<a href="/research/rankings" class="section__link">View all {data.stats.stateCount} states →</a>
			</div>

			<div class="rankings-preview">
				<div class="ranking-list ranking-list--top">
					<h3>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
							<path fill-rule="evenodd" d="M10 17a.75.75 0 01-.75-.75V5.612L5.29 9.77a.75.75 0 01-1.08-1.04l5.25-5.5a.75.75 0 011.08 0l5.25 5.5a.75.75 0 11-1.08 1.04l-3.96-4.158V16.25A.75.75 0 0110 17z" clip-rule="evenodd" />
						</svg>
						Top States
					</h3>
					<ol>
						{#each data.topStates.slice(0, 3) as state, i}
							<li>
								<span class="rank">{i + 1}</span>
								<span class="name">{STATE_NAMES[state.state]}</span>
								<span class="score positive">+{state.avgResilience.toFixed(3)}</span>
							</li>
						{/each}
					</ol>
				</div>

				<div class="ranking-list ranking-list--bottom">
					<h3>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
							<path fill-rule="evenodd" d="M10 3a.75.75 0 01.75.75v10.638l3.96-4.158a.75.75 0 111.08 1.04l-5.25 5.5a.75.75 0 01-1.08 0l-5.25-5.5a.75.75 0 111.08-1.04l3.96 4.158V3.75A.75.75 0 0110 3z" clip-rule="evenodd" />
						</svg>
						Bottom States
					</h3>
					<ol>
						{#each data.bottomStates.slice(0, 3) as state, i}
							<li>
								<span class="rank">{data.stats.stateCount - i}</span>
								<span class="name">{STATE_NAMES[state.state]}</span>
								<span class="score negative">{state.avgResilience.toFixed(3)}</span>
							</li>
						{/each}
					</ol>
				</div>
			</div>
		</section>

		<!-- Data Access -->
		<section class="section">
			<div class="section__header">
				<h2 class="section__title">Access the Data</h2>
			</div>

			<div class="access-options">
				<a href="/data" class="access-card">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
						<path fill-rule="evenodd" d="M1.5 5.625c0-1.036.84-1.875 1.875-1.875h17.25c1.035 0 1.875.84 1.875 1.875v12.75c0 1.035-.84 1.875-1.875 1.875H3.375A1.875 1.875 0 011.5 18.375V5.625z" clip-rule="evenodd" />
					</svg>
					<div>
						<h3>Browse & Download</h3>
						<p>Interactive data browser with CSV export</p>
					</div>
				</a>

				<a href="/map" class="access-card">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
						<path fill-rule="evenodd" d="M8.161 2.58a1.875 1.875 0 011.678 0l4.993 2.498c.106.052.23.052.336 0l3.869-1.935A1.875 1.875 0 0121.75 4.82v12.485c0 .71-.401 1.36-1.037 1.677l-4.875 2.437a1.875 1.875 0 01-1.676 0l-4.994-2.497a.375.375 0 00-.336 0l-3.868 1.935A1.875 1.875 0 012.25 19.18V6.695c0-.71.401-1.36 1.036-1.677l4.875-2.437z" clip-rule="evenodd" />
					</svg>
					<div>
						<h3>Interactive Map</h3>
						<p>Explore all 54,000+ census tracts</p>
					</div>
				</a>

				<a href="/about#api" class="access-card">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
						<path fill-rule="evenodd" d="M14.447 3.027a.75.75 0 01.527.92l-4.5 16.5a.75.75 0 01-1.448-.394l4.5-16.5a.75.75 0 01.921-.526z" clip-rule="evenodd" />
					</svg>
					<div>
						<h3>REST API</h3>
						<p>Programmatic access</p>
					</div>
				</a>
			</div>
		</section>

		<!-- Citation -->
		<section class="citation">
			<h2>How to Cite</h2>
			<div class="citation__block">
				<code>Community Resilience Mapping Project (2026). Census tract-level health resilience scores for the United States. https://odds.health</code>
			</div>
		</section>
	</div>
</div>

<style>
	.research {
		color: var(--color-text-primary);
	}

	.container {
		max-width: var(--container-lg);
		margin: 0 auto;
		padding: var(--space-8) var(--space-6) var(--space-16);
	}

	/* Header */
	.header {
		text-align: center;
		margin-bottom: var(--space-8);
		padding-top: var(--space-4);
	}

	.header__title {
		font-family: var(--font-display);
		font-size: var(--text-4xl);
		font-weight: var(--font-weight-normal);
		margin-bottom: var(--space-2);
	}

	.header__subtitle {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
	}

	/* Navigation Cards */
	.nav-cards {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: var(--space-4);
		margin-bottom: var(--space-10);
	}

	.nav-card {
		display: flex;
		align-items: center;
		gap: var(--space-4);
		padding: var(--space-5);
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		text-decoration: none;
		color: inherit;
		transition: all var(--duration-normal) var(--ease-out);
	}

	.nav-card:hover {
		border-color: var(--color-accent-primary);
		transform: translateY(-2px);
		box-shadow: var(--shadow-lg);
	}

	.nav-card__icon {
		width: 48px;
		height: 48px;
		background: var(--color-accent-primary-glow);
		border-radius: var(--radius-lg);
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}

	.nav-card__icon svg {
		width: 24px;
		height: 24px;
		color: var(--color-accent-primary);
	}

	.nav-card__content h2 {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		margin-bottom: var(--space-1);
	}

	.nav-card__content p {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	/* Featured */
	.featured {
		background: linear-gradient(135deg, var(--color-foundation-mid), var(--color-accent-primary-glow));
		border: 1px solid var(--color-accent-primary);
		border-radius: var(--radius-xl);
		padding: var(--space-8);
		margin-bottom: var(--space-12);
		text-align: center;
	}

	.featured__badge {
		display: inline-block;
		font-size: var(--text-xs);
		font-weight: var(--font-weight-bold);
		color: var(--color-accent-primary);
		background: var(--color-accent-primary-glow);
		padding: var(--space-1) var(--space-3);
		border-radius: var(--radius-full);
		margin-bottom: var(--space-4);
	}

	.featured__title {
		font-family: var(--font-display);
		font-size: var(--text-2xl);
		font-weight: var(--font-weight-normal);
		margin-bottom: var(--space-3);
	}

	.featured__text {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		max-width: 600px;
		margin: 0 auto var(--space-4);
	}

	.featured__text strong.positive {
		color: var(--color-score-high);
		font-weight: var(--font-weight-bold);
	}

	.featured__text strong.negative {
		color: var(--color-score-low);
		font-weight: var(--font-weight-bold);
	}

	.featured__link {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	.featured__link:hover {
		text-decoration: underline;
	}

	/* Section */
	.section {
		margin-bottom: var(--space-12);
	}

	.section__header {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		margin-bottom: var(--space-6);
		padding-bottom: var(--space-4);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.section__title {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		font-weight: var(--font-weight-normal);
	}

	.section__link {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	.section__link:hover {
		text-decoration: underline;
	}

	/* Findings Grid */
	.findings-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: var(--space-4);
	}

	.finding-card {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-lg);
		padding: var(--space-5);
		text-decoration: none;
		color: inherit;
		transition: all var(--duration-normal) var(--ease-out);
	}

	.finding-card:hover {
		border-color: var(--color-accent-primary);
		transform: translateY(-2px);
	}

	.finding-card--featured {
		grid-column: span 2;
		background: linear-gradient(135deg, var(--color-foundation-mid), var(--color-accent-primary-glow));
		border-color: var(--color-accent-primary);
	}

	.finding-card h3 {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		margin-bottom: var(--space-2);
	}

	.finding-card p {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-3);
	}

	.finding-card p strong.positive {
		color: var(--color-score-high);
	}

	.finding-card p strong.negative {
		color: var(--color-score-low);
	}

	.finding-card__link {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-accent-primary);
	}

	/* Papers Preview */
	.papers-preview {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: var(--space-4);
	}

	.paper-card {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-lg);
		padding: var(--space-5);
		text-decoration: none;
		color: inherit;
		transition: all var(--duration-normal) var(--ease-out);
	}

	.paper-card:hover {
		border-color: var(--color-accent-primary);
		transform: translateY(-2px);
	}

	.paper-card--featured {
		border-color: var(--color-accent-primary);
	}

	.paper-card__badge {
		display: inline-block;
		font-size: var(--text-xs);
		font-weight: var(--font-weight-bold);
		color: var(--color-score-high);
		background: var(--color-score-high-bg);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
		margin-bottom: var(--space-2);
	}

	.paper-card h3 {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		margin-bottom: var(--space-2);
		line-height: var(--leading-tight);
	}

	.paper-card p {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	/* Rankings Preview */
	.rankings-preview {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: var(--space-6);
	}

	.ranking-list {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-lg);
		padding: var(--space-5);
	}

	.ranking-list h3 {
		display: flex;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		margin-bottom: var(--space-4);
	}

	.ranking-list h3 svg {
		width: 18px;
		height: 18px;
	}

	.ranking-list--top h3 svg {
		color: var(--color-score-high);
	}

	.ranking-list--bottom h3 svg {
		color: var(--color-score-low);
	}

	.ranking-list ol {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	.ranking-list li {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		padding: var(--space-2) 0;
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.ranking-list li:last-child {
		border-bottom: none;
	}

	.ranking-list .rank {
		width: 24px;
		height: 24px;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: var(--text-xs);
		font-weight: var(--font-weight-bold);
		color: var(--color-text-muted);
		background: var(--color-foundation-surface);
		border-radius: var(--radius-full);
	}

	.ranking-list .name {
		flex: 1;
		font-size: var(--text-sm);
	}

	.ranking-list .score {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
	}

	.positive {
		color: var(--color-score-high);
	}

	.negative {
		color: var(--color-score-low);
	}

	/* Access */
	.access-options {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: var(--space-4);
	}

	.access-card {
		display: flex;
		align-items: center;
		gap: var(--space-4);
		padding: var(--space-4);
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-lg);
		text-decoration: none;
		color: inherit;
		transition: all var(--duration-normal) var(--ease-out);
	}

	.access-card:hover {
		border-color: var(--color-accent-primary);
	}

	.access-card svg {
		width: 24px;
		height: 24px;
		color: var(--color-accent-primary);
		flex-shrink: 0;
	}

	.access-card h3 {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		margin-bottom: var(--space-1);
	}

	.access-card p {
		font-size: var(--text-xs);
		color: var(--color-text-secondary);
	}

	/* Citation */
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

	/* Responsive */
	@media (max-width: 900px) {
		.nav-cards {
			grid-template-columns: 1fr;
		}

		.papers-preview {
			grid-template-columns: 1fr;
		}

		.access-options {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 640px) {
		.container {
			padding: var(--space-6) var(--space-4) var(--space-12);
		}

		.findings-grid {
			grid-template-columns: 1fr;
		}

		.finding-card--featured {
			grid-column: span 1;
		}

		.rankings-preview {
			grid-template-columns: 1fr;
		}
	}
</style>
