<script lang="ts">
	// Static page - no dynamic data needed
</script>

<svelte:head>
	<title>About & Methodology | Community Resilience Mapping</title>
	<meta
		name="description"
		content="Learn about the methodology behind community resilience scores and how to interpret the data."
	/>
</svelte:head>

<main class="about-page">
	<div class="container">
		<!-- Header -->
		<header class="page-header">
			<a href="/" class="back-link" aria-label="Back to home">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
					class="w-5 h-5"
					aria-hidden="true"
				>
					<path
						fill-rule="evenodd"
						d="M17 10a.75.75 0 01-.75.75H5.612l4.158 3.96a.75.75 0 11-1.04 1.08l-5.5-5.25a.75.75 0 010-1.08l5.5-5.25a.75.75 0 111.04 1.08L5.612 9.25H16.25A.75.75 0 0117 10z"
						clip-rule="evenodd"
					/>
				</svg>
				<span>Back</span>
			</a>
			<h1>About & Methodology</h1>
			<p class="subtitle">
				Understanding how community resilience scores are calculated and what they mean.
			</p>
		</header>

		<!-- Key Stats -->
		<section class="stats-section" aria-labelledby="stats-heading">
			<h2 id="stats-heading" class="sr-only">Dataset Statistics</h2>
			<div class="stats-grid">
				<div class="stat-card">
					<div class="stat-value">64,419</div>
					<div class="stat-label">Census Tracts</div>
				</div>
				<div class="stat-card">
					<div class="stat-value">50</div>
					<div class="stat-label">States + DC</div>
				</div>
				<div class="stat-card">
					<div class="stat-value">330M+</div>
					<div class="stat-label">Population Covered</div>
				</div>
				<div class="stat-card">
					<div class="stat-value">1,059</div>
					<div class="stat-label">Resilient LILA Tracts</div>
				</div>
			</div>
		</section>

		<!-- Research Question -->
		<section class="content-section" aria-labelledby="question-heading">
			<h2 id="question-heading">Research Question</h2>
			<p class="lead">
				<strong>Which communities demonstrate better health outcomes than predicted by their
				material circumstances?</strong>
			</p>
			<p>
				Traditional metrics like income, education, and access to healthcare explain much of the
				variation in community health. But some communities do significantly better than these
				factors would predict. We call this "community resilience" &mdash; the capacity for a
				community to thrive despite challenging conditions.
			</p>
			<p>
				This project identifies these communities by looking at the gap between predicted and
				actual health outcomes, potentially revealing communities with strong social ties,
				cultural assets, or other protective factors that aren't captured by standard demographic
				measures.
			</p>
		</section>

		<!-- Methodology -->
		<section class="content-section" aria-labelledby="methodology-heading">
			<h2 id="methodology-heading">Methodology</h2>

			<h3>Data Sources</h3>
			<ul class="data-sources">
				<li>
					<strong>CDC PLACES 2023</strong> &mdash; Census tract-level health outcomes including
					diabetes, obesity, mental health, and preventive care measures
				</li>
				<li>
					<strong>USDA Food Access Research Atlas 2019</strong> &mdash; Low-income, low-access
					(LILA) classification identifying food deserts
				</li>
				<li>
					<strong>Census ACS 2020</strong> &mdash; Demographic and socioeconomic characteristics
					including group quarters population
				</li>
			</ul>

			<h3>Health Burden Index</h3>
			<p>
				We construct a composite health burden index (0-1 scale) from CDC PLACES data, combining:
			</p>
			<ul>
				<li>Chronic disease prevalence (diabetes, obesity, heart disease)</li>
				<li>Mental health indicators (depression, poor mental health days)</li>
				<li>Preventive care gaps (lack of health insurance, missed checkups)</li>
				<li>Behavioral risk factors (smoking, physical inactivity)</li>
			</ul>

			<h3>Statistical Model</h3>
			<p>
				We use OLS regression with state fixed effects to predict health burden based on
				socioeconomic and access factors:
			</p>
			<pre class="code-block"><code>Health Burden ~ Poverty Rate + Education + Insurance
              + Food Access + Housing Cost Burden
              + State Fixed Effects</code></pre>
			<p>
				The <strong>resilience score</strong> is the standardized residual from this model
				(z-score). A positive score means the community has better health outcomes than predicted;
				a negative score means worse outcomes than predicted.
			</p>

			<h3>Exclusion Criteria</h3>
			<p>
				Tracts where more than 10% of the population lives in group quarters (college dorms,
				military barracks, correctional facilities, nursing homes) are flagged but not excluded.
				These populations may have health outcomes driven by institutional factors rather than
				community characteristics.
			</p>
		</section>

		<!-- Score Categories -->
		<section class="content-section" aria-labelledby="categories-heading">
			<h2 id="categories-heading">Score Categories</h2>
			<div class="categories-table">
				<div class="category-row">
					<span class="category-swatch very-high"></span>
					<span class="category-name">Very High</span>
					<span class="category-range">&ge; 2.0</span>
					<span class="category-desc">Exceptionally better than predicted</span>
				</div>
				<div class="category-row">
					<span class="category-swatch high"></span>
					<span class="category-name">High</span>
					<span class="category-range">1.0 to 2.0</span>
					<span class="category-desc">Notably better than predicted</span>
				</div>
				<div class="category-row">
					<span class="category-swatch medium"></span>
					<span class="category-name">Medium</span>
					<span class="category-range">0.0 to 1.0</span>
					<span class="category-desc">Slightly better than predicted</span>
				</div>
				<div class="category-row">
					<span class="category-swatch low"></span>
					<span class="category-name">Low</span>
					<span class="category-range">-1.0 to 0.0</span>
					<span class="category-desc">Slightly worse than predicted</span>
				</div>
				<div class="category-row">
					<span class="category-swatch very-low"></span>
					<span class="category-name">Very Low</span>
					<span class="category-range">&lt; -1.0</span>
					<span class="category-desc">Notably worse than predicted</span>
				</div>
			</div>
		</section>

		<!-- Limitations -->
		<section class="content-section" aria-labelledby="limitations-heading">
			<h2 id="limitations-heading">Limitations</h2>
			<ul class="limitations-list">
				<li>
					<strong>Temporal Gap</strong> &mdash; Health data (2023), food access data (2019), and
					Census data (2020) come from different time periods.
				</li>
				<li>
					<strong>Model-Based Estimates</strong> &mdash; CDC PLACES uses small area estimation,
					not direct measurement. Some tract-level estimates have high uncertainty.
				</li>
				<li>
					<strong>Ecological Fallacy</strong> &mdash; Tract-level patterns do not describe
					individual outcomes. A "resilient" tract may still contain individuals with poor health.
				</li>
				<li>
					<strong>Unmeasured Confounders</strong> &mdash; The model cannot capture all factors
					affecting health. Positive residuals may reflect unmeasured socioeconomic advantages
					rather than community resilience.
				</li>
				<li>
					<strong>Static Snapshot</strong> &mdash; This is a cross-sectional analysis and cannot
					show trends or causation.
				</li>
			</ul>
		</section>

		<!-- Appropriate Use -->
		<section class="content-section" aria-labelledby="use-heading">
			<h2 id="use-heading">Appropriate Uses</h2>
			<div class="use-grid">
				<div class="use-card appropriate">
					<h3>Appropriate</h3>
					<ul>
						<li>Exploratory research into community health patterns</li>
						<li>Identifying communities for qualitative follow-up research</li>
						<li>Asset-based community development planning</li>
						<li>Understanding geographic variation in health outcomes</li>
						<li>Educational purposes and data literacy</li>
					</ul>
				</div>
				<div class="use-card inappropriate">
					<h3>Inappropriate</h3>
					<ul>
						<li>Justifying disinvestment from "resilient" communities</li>
						<li>Making predictions about individual health</li>
						<li>Punitive comparisons between communities</li>
						<li>Replacing qualitative community input</li>
						<li>Definitive claims about community characteristics</li>
					</ul>
				</div>
			</div>
		</section>

		<!-- API Documentation -->
		<section class="content-section" aria-labelledby="api-heading">
			<h2 id="api-heading">API Access</h2>
			<p>
				Access the underlying data through our REST API. All endpoints return JSON.
			</p>
			<div class="api-endpoints">
				<div class="endpoint">
					<code class="endpoint-method">GET</code>
					<code class="endpoint-path">/api/stats</code>
					<span class="endpoint-desc">Aggregate statistics for the dataset</span>
				</div>
				<div class="endpoint">
					<code class="endpoint-method">GET</code>
					<code class="endpoint-path">/api/tracts?limit=100&offset=0</code>
					<span class="endpoint-desc">Paginated list of tracts with resilience scores</span>
				</div>
				<div class="endpoint">
					<code class="endpoint-method">GET</code>
					<code class="endpoint-path">/api/tracts/:fips</code>
					<span class="endpoint-desc">Single tract by 11-digit FIPS code</span>
				</div>
				<div class="endpoint">
					<code class="endpoint-method">GET</code>
					<code class="endpoint-path">/api/geocode?address=...</code>
					<span class="endpoint-desc">Geocode address and return tract with resilience data</span>
				</div>
			</div>
		</section>

		<!-- Citation -->
		<section class="content-section" aria-labelledby="citation-heading">
			<h2 id="citation-heading">Citation</h2>
			<pre class="citation-block"><code>@misc&#123;resilience-mapping,
  title = &#123;Community Resilience Mapping&#125;,
  year = &#123;2024&#125;,
  url = &#123;https://resilience-mapping.fly.dev&#125;,
  note = &#123;Census tract-level analysis of community
         health resilience using CDC PLACES and
         USDA Food Access Research Atlas data&#125;
&#125;</code></pre>
		</section>

		<!-- Footer -->
		<footer class="page-footer">
			<nav class="footer-nav">
				<a href="/">Home</a>
				<a href="/map">Interactive Map</a>
				<a href="/api/stats">API</a>
			</nav>
		</footer>
	</div>
</main>

<style>
	.about-page {
		min-height: 100vh;
		background: linear-gradient(to bottom, #0f172a, #1e293b);
		color: #e2e8f0;
	}

	.container {
		max-width: 800px;
		margin: 0 auto;
		padding: 2rem 1.5rem 4rem;
	}

	/* Header */
	.page-header {
		margin-bottom: 3rem;
	}

	.back-link {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		color: #94a3b8;
		text-decoration: none;
		font-size: 0.875rem;
		margin-bottom: 1.5rem;
		transition: color 0.15s ease;
	}

	.back-link:hover {
		color: #10b981;
	}

	h1 {
		font-size: 2.5rem;
		font-weight: 700;
		color: white;
		margin: 0 0 0.75rem;
	}

	.subtitle {
		font-size: 1.125rem;
		color: #94a3b8;
		margin: 0;
		line-height: 1.6;
	}

	/* Stats Grid */
	.stats-section {
		margin-bottom: 3rem;
	}

	.stats-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1rem;
	}

	@media (min-width: 640px) {
		.stats-grid {
			grid-template-columns: repeat(4, 1fr);
		}
	}

	.stat-card {
		background: rgba(51, 65, 85, 0.5);
		border-radius: 12px;
		padding: 1.25rem;
		text-align: center;
	}

	.stat-value {
		font-size: 1.75rem;
		font-weight: 700;
		color: #10b981;
	}

	.stat-label {
		font-size: 0.8125rem;
		color: #94a3b8;
		margin-top: 0.25rem;
	}

	/* Content Sections */
	.content-section {
		margin-bottom: 3rem;
	}

	h2 {
		font-size: 1.5rem;
		font-weight: 600;
		color: white;
		margin: 0 0 1.25rem;
		padding-bottom: 0.75rem;
		border-bottom: 1px solid #334155;
	}

	h3 {
		font-size: 1.125rem;
		font-weight: 600;
		color: #e2e8f0;
		margin: 1.5rem 0 0.75rem;
	}

	p {
		line-height: 1.7;
		margin: 0 0 1rem;
		color: #cbd5e1;
	}

	.lead {
		font-size: 1.125rem;
		color: #e2e8f0;
	}

	ul {
		margin: 0 0 1rem;
		padding-left: 1.5rem;
		color: #cbd5e1;
	}

	li {
		margin-bottom: 0.5rem;
		line-height: 1.6;
	}

	.data-sources li {
		margin-bottom: 0.75rem;
	}

	/* Code Block */
	.code-block {
		background: #0f172a;
		border: 1px solid #334155;
		border-radius: 8px;
		padding: 1rem 1.25rem;
		overflow-x: auto;
		margin: 1rem 0;
	}

	.code-block code {
		font-family: ui-monospace, 'SF Mono', monospace;
		font-size: 0.875rem;
		color: #94a3b8;
		white-space: pre;
	}

	/* Categories Table */
	.categories-table {
		background: rgba(51, 65, 85, 0.3);
		border-radius: 12px;
		overflow: hidden;
	}

	.category-row {
		display: grid;
		grid-template-columns: 20px 80px 80px 1fr;
		gap: 1rem;
		align-items: center;
		padding: 0.875rem 1.25rem;
		border-bottom: 1px solid #334155;
	}

	.category-row:last-child {
		border-bottom: none;
	}

	.category-swatch {
		width: 16px;
		height: 16px;
		border-radius: 4px;
	}

	.category-swatch.very-high {
		background: #059669;
	}
	.category-swatch.high {
		background: #34d399;
	}
	.category-swatch.medium {
		background: #fbbf24;
	}
	.category-swatch.low {
		background: #f97316;
	}
	.category-swatch.very-low {
		background: #dc2626;
	}

	.category-name {
		font-weight: 500;
		color: #e2e8f0;
	}

	.category-range {
		font-family: ui-monospace, monospace;
		font-size: 0.8125rem;
		color: #94a3b8;
	}

	.category-desc {
		font-size: 0.875rem;
		color: #94a3b8;
	}

	/* Limitations */
	.limitations-list li {
		margin-bottom: 0.875rem;
	}

	/* Use Grid */
	.use-grid {
		display: grid;
		gap: 1.5rem;
	}

	@media (min-width: 640px) {
		.use-grid {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	.use-card {
		background: rgba(51, 65, 85, 0.3);
		border-radius: 12px;
		padding: 1.25rem 1.5rem;
	}

	.use-card h3 {
		margin: 0 0 0.75rem;
		font-size: 1rem;
	}

	.use-card.appropriate h3 {
		color: #10b981;
	}

	.use-card.inappropriate h3 {
		color: #f87171;
	}

	.use-card ul {
		margin: 0;
		padding-left: 1.25rem;
	}

	.use-card li {
		font-size: 0.875rem;
		margin-bottom: 0.5rem;
	}

	/* API Endpoints */
	.api-endpoints {
		background: rgba(51, 65, 85, 0.3);
		border-radius: 12px;
		overflow: hidden;
	}

	.endpoint {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.875rem 1.25rem;
		border-bottom: 1px solid #334155;
		flex-wrap: wrap;
	}

	.endpoint:last-child {
		border-bottom: none;
	}

	.endpoint-method {
		background: #10b981;
		color: #0f172a;
		font-size: 0.6875rem;
		font-weight: 600;
		padding: 0.25rem 0.5rem;
		border-radius: 4px;
	}

	.endpoint-path {
		font-family: ui-monospace, monospace;
		font-size: 0.875rem;
		color: #e2e8f0;
	}

	.endpoint-desc {
		font-size: 0.8125rem;
		color: #94a3b8;
		width: 100%;
		margin-top: 0.25rem;
	}

	@media (min-width: 640px) {
		.endpoint-desc {
			width: auto;
			margin-top: 0;
			margin-left: auto;
		}
	}

	/* Citation */
	.citation-block {
		background: #0f172a;
		border: 1px solid #334155;
		border-radius: 8px;
		padding: 1rem 1.25rem;
		overflow-x: auto;
	}

	.citation-block code {
		font-family: ui-monospace, 'SF Mono', monospace;
		font-size: 0.8125rem;
		color: #94a3b8;
		white-space: pre;
	}

	/* Footer */
	.page-footer {
		margin-top: 4rem;
		padding-top: 2rem;
		border-top: 1px solid #334155;
	}

	.footer-nav {
		display: flex;
		justify-content: center;
		gap: 2rem;
	}

	.footer-nav a {
		color: #94a3b8;
		text-decoration: none;
		font-size: 0.875rem;
		transition: color 0.15s ease;
	}

	.footer-nav a:hover {
		color: #10b981;
	}

	/* Utilities */
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
</style>
