<script lang="ts">
</script>

<svelte:head>
	<title>For Researchers | Community Resilience Mapping</title>
	<meta
		name="description"
		content="Academic resources for community health resilience research. Access validated tract-level data, methodology documentation, and API access."
	/>
</svelte:head>

<div class="persona-page">
	<div class="container">
		<!-- Header -->
		<header class="header">
			<p class="header__eyebrow">For Academic Research</p>
			<h1 class="header__title">Research Resources</h1>
			<p class="header__subtitle">
				Validated tract-level resilience scores for 54,000+ census tracts,
				complete methodology documentation, and programmatic API access.
			</p>
		</header>

		<!-- Quick Stats -->
		<section class="quick-stats" aria-labelledby="stats-heading">
			<h2 id="stats-heading" class="sr-only">Dataset Overview</h2>
			<div class="stats-grid">
				<div class="stat-card">
					<span class="stat-card__value">54,560</span>
					<span class="stat-card__label">Census Tracts</span>
				</div>
				<div class="stat-card">
					<span class="stat-card__value">51</span>
					<span class="stat-card__label">States + DC</span>
				</div>
				<div class="stat-card">
					<span class="stat-card__value">220M+</span>
					<span class="stat-card__label">Population Coverage</span>
				</div>
				<div class="stat-card">
					<span class="stat-card__value">2020</span>
					<span class="stat-card__label">Census Boundaries</span>
				</div>
			</div>
		</section>

		<!-- Recent Papers -->
		<section class="papers" aria-labelledby="papers-heading">
			<h2 id="papers-heading" class="section-title">Recent Papers</h2>
			<div class="papers-grid">
				<a href="/research/papers/immigrant-health-advantage" class="paper-card paper-card--new">
					<span class="paper-badge">New</span>
					<h3>Immigrant Health Advantage Analysis</h3>
					<p>
						Testing whether the "Hispanic Paradox" reflects genuine community resilience or aggregation
						artifacts. Finds dramatic heterogeneity across origin groups and a 2.6 SD gap within Texas.
					</p>
					<span class="paper-link">Read Paper →</span>
				</a>
				<a href="/research/papers/health-equity" class="paper-card paper-card--new">
					<span class="paper-badge">New</span>
					<h3>Structural Correlates of Resilience</h3>
					<p>
						Examines the 0.43 SD resilience gap between majority-white and majority-minority communities.
						State-level variation from +1.87 to -0.89 SD proves structural factors are modifiable.
					</p>
					<span class="paper-link">Read Paper →</span>
				</a>
				<a href="/research/papers/structural-determinants" class="paper-card">
					<h3>Structural Determinants Paper</h3>
					<p>
						Core methodology paper establishing the resilience framework and analyzing structural
						predictors across 53,889 census tracts.
					</p>
					<span class="paper-link">Read Paper →</span>
				</a>
				<a href="/research" class="paper-card paper-card--all">
					<h3>View All Research</h3>
					<p>
						Browse all published papers, working papers, and research findings from the
						Community Resilience Mapping Project.
					</p>
					<span class="paper-link">Browse All →</span>
				</a>
			</div>
		</section>

		<!-- Data Access -->
		<section class="data-access" aria-labelledby="access-heading">
			<h2 id="access-heading" class="section-title">Data Access</h2>
			<div class="access-grid">
				<a href="/data" class="access-card">
					<div class="access-card__icon">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
							<path fill-rule="evenodd" d="M1.5 5.625c0-1.036.84-1.875 1.875-1.875h17.25c1.035 0 1.875.84 1.875 1.875v12.75c0 1.035-.84 1.875-1.875 1.875H3.375A1.875 1.875 0 011.5 18.375V5.625zM21 9.375A.375.375 0 0020.625 9h-7.5a.375.375 0 00-.375.375v1.5c0 .207.168.375.375.375h7.5a.375.375 0 00.375-.375v-1.5z" clip-rule="evenodd" />
						</svg>
					</div>
					<h3 class="access-card__title">Full Dataset (CSV)</h3>
					<p class="access-card__description">
						Download the complete dataset with all variables including resilience scores,
						health burden, socioeconomic indicators, and geographic identifiers.
					</p>
					<span class="access-card__link">Browse & Download →</span>
				</a>

				<a href="/about#api" class="access-card">
					<div class="access-card__icon">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
							<path fill-rule="evenodd" d="M14.447 3.027a.75.75 0 01.527.92l-4.5 16.5a.75.75 0 01-1.448-.394l4.5-16.5a.75.75 0 01.921-.526zM16.72 6.22a.75.75 0 011.06 0l5.25 5.25a.75.75 0 010 1.06l-5.25 5.25a.75.75 0 11-1.06-1.06L21.44 12l-4.72-4.72a.75.75 0 010-1.06z" clip-rule="evenodd" />
						</svg>
					</div>
					<h3 class="access-card__title">REST API</h3>
					<p class="access-card__description">
						Programmatic access for applications. Query tracts by FIPS code, geocode addresses,
						and integrate resilience data into your research workflows.
					</p>
					<span class="access-card__link">API Documentation →</span>
				</a>

				<a href="/map" class="access-card">
					<div class="access-card__icon">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
							<path fill-rule="evenodd" d="M8.161 2.58a1.875 1.875 0 011.678 0l4.993 2.498c.106.052.23.052.336 0l3.869-1.935A1.875 1.875 0 0121.75 4.82v12.485c0 .71-.401 1.36-1.037 1.677l-4.875 2.437a1.875 1.875 0 01-1.676 0l-4.994-2.497a.375.375 0 00-.336 0l-3.868 1.935A1.875 1.875 0 012.25 19.18V6.695c0-.71.401-1.36 1.036-1.677l4.875-2.437z" clip-rule="evenodd" />
						</svg>
					</div>
					<h3 class="access-card__title">Interactive Map</h3>
					<p class="access-card__description">
						Visual exploration of all census tracts. Useful for identifying geographic patterns,
						outliers, and regions of interest for deeper analysis.
					</p>
					<span class="access-card__link">Explore Map →</span>
				</a>
			</div>
		</section>

		<!-- Methodology -->
		<section class="methodology" aria-labelledby="method-heading">
			<h2 id="method-heading" class="section-title">Methodology</h2>
			<div class="method-content">
				<p>
					Resilience scores are standardized residuals from an OLS regression predicting
					health burden from socioeconomic and access factors with state fixed effects.
					A positive score indicates better health outcomes than predicted; negative indicates worse.
				</p>

				<div class="method-steps">
					<div class="method-step">
						<span class="method-step__number">1</span>
						<h3>Health Burden Index</h3>
						<p>
							Composite 0-1 scale from CDC PLACES data: chronic disease prevalence,
							mental health indicators, preventive care gaps, and behavioral risk factors.
						</p>
					</div>
					<div class="method-step">
						<span class="method-step__number">2</span>
						<h3>Regression Model</h3>
						<p>
							OLS with state fixed effects predicting health burden from poverty rate,
							education levels, insurance coverage, food access, and housing cost burden.
						</p>
					</div>
					<div class="method-step">
						<span class="method-step__number">3</span>
						<h3>Resilience Score</h3>
						<p>
							Standardized residual (z-score). Score of +2.0 means community is ~2 SD healthier
							than predicted—roughly top 2% of positive outliers.
						</p>
					</div>
				</div>

				<a href="/about" class="btn btn--outline">Full Methodology Documentation →</a>
			</div>
		</section>

		<!-- Data Sources -->
		<section class="sources" aria-labelledby="sources-heading">
			<h2 id="sources-heading" class="section-title">Data Sources</h2>
			<ul class="sources-list">
				<li>
					<strong>CDC PLACES 2024</strong> — Census tract-level health outcomes (BRFSS 2022)
				</li>
				<li>
					<strong>USDA Food Access Research Atlas 2019</strong> — Food desert classification
				</li>
				<li>
					<strong>Census Bureau 2020</strong> — Population and boundary data
				</li>
				<li>
					<strong>ACS 5-Year Estimates</strong> — Socioeconomic indicators
				</li>
			</ul>
		</section>

		<!-- Citation -->
		<section class="citation" aria-labelledby="citation-heading">
			<h2 id="citation-heading" class="section-title">How to Cite</h2>
			<div class="citation-block">
				<code>Community Resilience Mapping Project (2025). Census tract-level health resilience scores for the United States. https://odds.health</code>
			</div>
			<p class="citation-note">
				This dataset is provided under open access terms for academic research. Please cite when publishing.
			</p>
		</section>
	</div>
</div>

<style>
	.persona-page {
		color: var(--color-text-primary);
	}

	.container {
		max-width: var(--container-lg);
		margin: 0 auto;
		padding: var(--space-8) var(--space-6) var(--space-16);
	}

	.header {
		text-align: center;
		margin-bottom: var(--space-12);
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
		color: var(--color-text-primary);
		margin-bottom: var(--space-4);
	}

	.header__subtitle {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
		max-width: 600px;
		margin: 0 auto;
	}

	/* Stats */
	.quick-stats {
		margin-bottom: var(--space-12);
	}

	.stats-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
		gap: var(--space-4);
	}

	.stat-card {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-5);
		text-align: center;
	}

	.stat-card__value {
		display: block;
		font-family: var(--font-display);
		font-size: var(--text-2xl);
		color: var(--color-accent-primary);
		margin-bottom: var(--space-1);
	}

	.stat-card__label {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wider);
	}

	/* Section Title */
	.section-title {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		color: var(--color-text-primary);
		margin-bottom: var(--space-6);
		padding-bottom: var(--space-3);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	/* Papers */
	.papers {
		margin-bottom: var(--space-12);
	}

	.papers-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: var(--space-4);
	}

	.paper-card {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-5);
		text-decoration: none;
		color: inherit;
		transition: all var(--duration-normal) var(--ease-out);
		position: relative;
	}

	.paper-card:hover {
		border-color: var(--color-accent-primary);
		box-shadow: var(--shadow-lg);
		transform: translateY(-2px);
	}

	.paper-card--new {
		border-color: var(--color-score-high);
	}

	.paper-card--all {
		border-style: dashed;
	}

	.paper-badge {
		position: absolute;
		top: var(--space-3);
		right: var(--space-3);
		font-size: var(--text-xs);
		font-weight: var(--font-weight-bold);
		color: var(--color-score-high);
		background: rgba(34, 197, 94, 0.2);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-full);
	}

	.paper-card h3 {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
		padding-right: var(--space-10);
	}

	.paper-card p {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-3);
	}

	.paper-link {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-accent-primary);
	}

	/* Data Access */
	.data-access {
		margin-bottom: var(--space-12);
	}

	.access-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: var(--space-5);
	}

	.access-card {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
		text-decoration: none;
		color: inherit;
		transition: all var(--duration-normal) var(--ease-out);
	}

	.access-card:hover {
		border-color: var(--color-accent-primary);
		box-shadow: var(--shadow-lg);
		transform: translateY(-2px);
	}

	.access-card__icon {
		width: 48px;
		height: 48px;
		background: var(--color-accent-primary-glow);
		border-radius: var(--radius-lg);
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: var(--space-4);
	}

	.access-card__icon svg {
		width: 24px;
		height: 24px;
		color: var(--color-accent-primary);
	}

	.access-card__title {
		font-size: var(--text-lg);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.access-card__description {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-4);
	}

	.access-card__link {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-accent-primary);
	}

	/* Methodology */
	.methodology {
		margin-bottom: var(--space-12);
	}

	.method-content > p {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-6);
	}

	.method-steps {
		display: grid;
		gap: var(--space-4);
		margin-bottom: var(--space-6);
	}

	.method-step {
		display: flex;
		gap: var(--space-4);
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-lg);
		padding: var(--space-4);
	}

	.method-step__number {
		width: 32px;
		height: 32px;
		background: var(--color-accent-primary);
		color: white;
		border-radius: var(--radius-full);
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: var(--font-weight-bold);
		font-size: var(--text-sm);
		flex-shrink: 0;
	}

	.method-step h3 {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-1);
	}

	.method-step p {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	/* Sources */
	.sources {
		margin-bottom: var(--space-12);
	}

	.sources-list {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	.sources-list li {
		padding: var(--space-3) 0;
		border-bottom: 1px solid var(--color-border-subtle);
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	.sources-list li:last-child {
		border-bottom: none;
	}

	.sources-list strong {
		color: var(--color-text-primary);
	}

	/* Citation */
	.citation-block {
		background: var(--color-foundation-surface);
		border: 1px solid var(--color-border-default);
		border-radius: var(--radius-lg);
		padding: var(--space-4) var(--space-5);
		margin-bottom: var(--space-4);
	}

	.citation-block code {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		word-break: break-word;
	}

	.citation-note {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	/* Buttons */
	.btn {
		display: inline-flex;
		align-items: center;
		padding: var(--space-3) var(--space-5);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		border-radius: var(--radius-lg);
		text-decoration: none;
		transition: all var(--duration-fast) var(--ease-out);
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

		.method-step {
			flex-direction: column;
			gap: var(--space-2);
		}
	}
</style>
