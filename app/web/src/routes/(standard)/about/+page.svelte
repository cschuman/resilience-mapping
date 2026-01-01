<script lang="ts">
	import { Accordion } from '$lib/components/ui';
	import { ScoreDistribution, MethodologyDiagram } from '$lib/components/viz';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>About & Methodology | Community Resilience Mapping</title>
	<meta
		name="description"
		content="Learn about the methodology behind community resilience scores and how to interpret the data."
	/>
</svelte:head>

<div class="about">
	<div class="container">
		<!-- Header -->
		<header class="header">
			<p class="header__eyebrow">Understanding the Data</p>
			<h1 class="header__title">Methodology</h1>
			<p class="header__subtitle">
				How we identify communities that thrive beyond what statistics predict.
			</p>
		</header>

		<!-- Quick Links -->
		<nav class="quick-links" aria-label="Quick navigation">
			<a href="#research">Research Question</a>
			<a href="#data-sources">Data Sources</a>
			<a href="#methodology">Methodology</a>
			<a href="#limitations">Limitations</a>
			<a href="#appropriate-use">Appropriate Uses</a>
			<a href="#api">API Access</a>
			<a href="#citation">Citation</a>
		</nav>

		<!-- Stats Overview -->
		<section class="stats" aria-labelledby="stats-heading">
			<h2 id="stats-heading" class="sr-only">Dataset Statistics</h2>
			<div class="stats__grid">
				<div class="stats__item">
					<span class="stats__value">{data.stats.totalTracts.toLocaleString()}</span>
					<span class="stats__label">Census Tracts</span>
				</div>
				<div class="stats__item">
					<span class="stats__value">{data.stats.stateCount}</span>
					<span class="stats__label">States + DC</span>
				</div>
				<div class="stats__item">
					<span class="stats__value">{Math.round(data.stats.totalPopulation / 1_000_000)}M+</span>
					<span class="stats__label">People</span>
				</div>
				<div class="stats__item">
					<span class="stats__value">2020</span>
					<span class="stats__label">Census Boundaries</span>
				</div>
			</div>
		</section>

		<!-- Score Legend -->
		<section class="legend" aria-labelledby="legend-heading">
			<h2 id="legend-heading" class="legend__title">Score Reference</h2>
			<div class="legend__grid">
				<div class="legend__table">
					<div class="legend__row">
						<span class="legend__swatch legend__swatch--very-high"></span>
						<span class="legend__label">Thriving (&ge;+2.0)</span>
						<span class="legend__desc">Exceptional resilience despite challenges</span>
					</div>
					<div class="legend__row">
						<span class="legend__swatch legend__swatch--high"></span>
						<span class="legend__label">Strong (+1.0 to +2.0)</span>
						<span class="legend__desc">Notable community strength</span>
					</div>
					<div class="legend__row">
						<span class="legend__swatch legend__swatch--medium"></span>
						<span class="legend__label">Steady (0 to +1.0)</span>
						<span class="legend__desc">Meeting expectations</span>
					</div>
					<div class="legend__row">
						<span class="legend__swatch legend__swatch--low"></span>
						<span class="legend__label">Challenged (-1.0 to 0)</span>
						<span class="legend__desc">Facing headwinds</span>
					</div>
					<div class="legend__row">
						<span class="legend__swatch legend__swatch--very-low"></span>
						<span class="legend__label">Struggling (&lt;-1.0)</span>
						<span class="legend__desc">Needs support</span>
					</div>
				</div>
				<div class="legend__chart">
					<h3 class="legend__chart-title">Score Distribution</h3>
					<ScoreDistribution buckets={data.distribution} />
				</div>
			</div>
		</section>

		<!-- Methodology Sections -->
		<section class="sections" aria-label="Detailed methodology">
			<h2 class="sections__title">Methodology</h2>

			<Accordion id="research" title="Research Question" defaultOpen>
				<div class="eli5">
					We're looking for neighborhoods that are healthier than they "should" be based on their
					income, education, and access to resources. What makes them special?
				</div>
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
			</Accordion>

			<Accordion id="data-sources" title="Data Sources" defaultOpen>
				<div class="eli5">
					We use publicly available government data on health conditions, food access, and demographics.
					All data is standardized to 2020 Census tract boundaries for consistency.
				</div>
				<ul>
					<li>
						<a href="https://www.cdc.gov/places/" target="_blank" rel="noopener"><strong>CDC PLACES 2024</strong></a> &mdash; Census tract-level health outcomes (BRFSS 2022)
						including obesity, diabetes, hypertension, heart disease, and physical inactivity.
						Kentucky and Pennsylvania use PLACES 2023 data (BRFSS 2021) as a fallback.
					</li>
					<li>
						<a href="https://www.ers.usda.gov/data-products/food-access-research-atlas/" target="_blank" rel="noopener"><strong>USDA Food Access Research Atlas 2019</strong></a> &mdash; Low-income, low-access
						(LILA) classification identifying food deserts (crosswalked to 2020 boundaries)
					</li>
					<li>
						<a href="https://www.census.gov/programs-surveys/acs" target="_blank" rel="noopener"><strong>Census Bureau ACS 5-Year Estimates</strong></a> &mdash; Socioeconomic indicators
						including poverty, education, and insurance coverage
					</li>
					<li>
						<a href="https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html" target="_blank" rel="noopener"><strong>Census Bureau 2020</strong></a> &mdash; Population data and tract boundary relationship
						files for geographic crosswalking
					</li>
				</ul>
			</Accordion>

			<Accordion id="methodology" title="Statistical Methodology" defaultOpen>
				<div class="eli5">
					We build a model that predicts how healthy a neighborhood "should" be based on income, education,
					and similar factors. Then we compare prediction to reality. Neighborhoods that are healthier than
					predicted get a positive score—the bigger the number, the more the community is beating the odds.
				</div>

				<MethodologyDiagram />

				<h3>Step 1: Measure Health Burden</h3>
				<p>
					We construct a composite health burden index (0-1 scale) from CDC PLACES data, combining:
				</p>
				<ul>
					<li>Chronic disease prevalence (diabetes, obesity, heart disease)</li>
					<li>Mental health indicators (depression, poor mental health days)</li>
					<li>Preventive care gaps (lack of health insurance, missed checkups)</li>
					<li>Behavioral risk factors (smoking, physical inactivity)</li>
				</ul>

				<h3>Step 2: Predict Expected Health</h3>
				<p>
					We use OLS regression with state fixed effects to predict health burden based on
					socioeconomic and access factors:
				</p>
				<pre><code>Health Burden ~ Poverty Rate + Education + Insurance
              + Food Access + Housing Cost Burden
              + State Fixed Effects</code></pre>

				<h3>Step 3: Calculate Resilience Score</h3>
				<p>
					The <strong>resilience score</strong> is the standardized residual from this model
					(z-score). A positive score means the community has better health outcomes than predicted;
					a negative score means worse outcomes than predicted.
				</p>
				<div class="example-box">
					<strong>Example:</strong> A tract with score +2.0 means the community is 2 standard deviations
					healthier than predicted &mdash; roughly in the top 2% of "positive outliers."
				</div>

				<h3>Note on Group Quarters</h3>
				<p>
					Tracts where more than 10% of the population lives in group quarters (college dorms,
					military barracks, correctional facilities, nursing homes) are <strong>excluded</strong> from
					the main analysis. These populations have health outcomes driven by institutional factors rather
					than community characteristics, leaving {data.stats.totalTracts.toLocaleString()} residential tracts
					in the final dataset. For research on these special populations, see our
					<a href="/research/special-populations">Special Populations Analysis</a>.
				</p>
			</Accordion>

			<Accordion id="limitations" title="Limitations" defaultOpen>
				<div class="eli5">
					This data has real limitations. It's an estimate, not a definitive answer. Use it as a
					starting point for asking questions, not as proof of anything.
				</div>
				<ul>
					<li>
						<strong>Kentucky &amp; Pennsylvania Data Vintage</strong> &mdash; These states use CDC PLACES 2023 data
						(BRFSS 2021) instead of 2024 data, as they couldn't collect enough BRFSS data in 2023.
						Their health outcomes are approximately one year older than other states.
					</li>
					<li>
						<strong>Temporal Gap</strong> &mdash; Health data (2024/BRFSS 2022), food access data (2019), and
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
			</Accordion>

			<Accordion id="appropriate-use" title="Appropriate Uses" defaultOpen>
				<div class="eli5">
					Use this data to ask interesting questions and find communities worth learning more about.
					Don't use it to make decisions that affect people's lives without doing more research first.
				</div>
				<div class="use-grid">
					<div class="use-card use-card--appropriate">
						<h4>Appropriate</h4>
						<ul>
							<li><a href="/research">Exploratory research</a> into community health patterns</li>
							<li>Identifying communities for qualitative follow-up research</li>
							<li><a href="/for-policy">Asset-based community development planning</a></li>
							<li><a href="/map">Understanding geographic variation</a> in health outcomes</li>
							<li>Educational purposes and data literacy</li>
						</ul>
					</div>
					<div class="use-card use-card--inappropriate">
						<h4>Inappropriate</h4>
						<ul>
							<li>Justifying disinvestment from "resilient" communities</li>
							<li>Making predictions about individual health</li>
							<li>Punitive comparisons between communities</li>
							<li>Replacing qualitative community input</li>
							<li>Definitive claims about community characteristics</li>
						</ul>
					</div>
				</div>
				<p class="use-audience-links">
					See detailed guidance for <a href="/for-researchers">researchers</a>,
					<a href="/for-journalists">journalists</a>, and
					<a href="/for-policy">policy analysts</a>.
				</p>
			</Accordion>

			<Accordion id="api" title="API Access" defaultOpen>
				<div class="eli5">
					Access the data programmatically through these endpoints, or visit the
					<a href="/data">Data page</a> to browse and download the full dataset.
				</div>
				<div class="api">
					<div class="api__endpoint">
						<code class="api__method">GET</code>
						<code class="api__path">/api/stats</code>
						<span class="api__desc">Aggregate statistics for the dataset</span>
					</div>
					<div class="api__endpoint">
						<code class="api__method">GET</code>
						<code class="api__path">/api/tracts?limit=100&offset=0</code>
						<span class="api__desc">Paginated list of tracts with resilience scores</span>
					</div>
					<div class="api__endpoint">
						<code class="api__method">GET</code>
						<code class="api__path">/api/tracts?format=csv</code>
						<span class="api__desc">Full dataset as CSV download</span>
					</div>
					<div class="api__endpoint">
						<code class="api__method">GET</code>
						<code class="api__path">/api/tracts/:fips</code>
						<span class="api__desc">Single tract by 11-digit FIPS code</span>
					</div>
					<div class="api__endpoint">
						<code class="api__method">GET</code>
						<code class="api__path">/api/geocode?address=...</code>
						<span class="api__desc">Geocode address and return tract with resilience data</span>
					</div>
				</div>
			</Accordion>

			<Accordion id="citation" title="Citation" defaultOpen>
				<div class="eli5">
					If you use this data, please cite it.
				</div>
				<pre><code>@misc&#123;resilience-mapping,
  title = &#123;Community Resilience Mapping&#125;,
  year = &#123;2026&#125;,
  url = &#123;https://odds.health&#125;,
  note = &#123;Census tract-level analysis of community
         health resilience using CDC PLACES 2024
         and USDA Food Access Research Atlas data,
         standardized to 2020 Census boundaries&#125;
&#125;</code></pre>
			</Accordion>
		</section>
	</div>
</div>

<style>
	.about {
		color: var(--color-text-secondary);
	}

	.container {
		max-width: var(--container-content);
		margin: 0 auto;
		padding: var(--space-8) var(--space-6) var(--space-16);
	}

	/* Header */
	.header {
		text-align: center;
		margin-bottom: var(--space-10);
	}

	.header__eyebrow {
		font-size: var(--text-xs);
		font-weight: var(--font-weight-semibold);
		color: var(--color-accent-primary);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		margin-bottom: var(--space-3);
	}

	.header__title {
		font-family: var(--font-display);
		font-size: var(--text-4xl);
		color: var(--color-text-primary);
		margin-bottom: var(--space-4);
	}

	.header__subtitle {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
		max-width: 480px;
		margin: 0 auto;
	}

	/* Quick Links */
	.quick-links {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: var(--space-2) var(--space-4);
		margin-bottom: var(--space-10);
		padding: var(--space-4);
		background: var(--color-foundation-mid);
		border-radius: var(--radius-xl);
		border: 1px solid var(--color-border-subtle);
	}

	.quick-links a {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-text-secondary);
		text-decoration: none;
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-md);
		transition: all var(--duration-fast) var(--ease-out);
	}

	.quick-links a:hover {
		color: var(--color-accent-primary);
		background: var(--color-accent-primary-glow);
	}

	/* Stats */
	.stats {
		margin-bottom: var(--space-10);
	}

	.stats__grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: var(--space-3);
	}

	@media (min-width: 640px) {
		.stats__grid {
			grid-template-columns: repeat(4, 1fr);
		}
	}

	.stats__item {
		background: var(--color-foundation-mid);
		border-radius: var(--radius-xl);
		padding: var(--space-5);
		text-align: center;
	}

	.stats__value {
		display: block;
		font-family: var(--font-display);
		font-size: var(--text-2xl);
		color: var(--color-accent-primary);
		line-height: 1;
		margin-bottom: var(--space-1);
	}

	.stats__label {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wide);
	}

	/* Legend */
	.legend {
		margin-bottom: var(--space-12);
	}

	.legend__title {
		font-family: var(--font-body);
		font-size: var(--text-xs);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		margin-bottom: var(--space-3);
	}

	.legend__grid {
		display: grid;
		grid-template-columns: 1fr;
		gap: var(--space-6);
	}

	@media (min-width: 768px) {
		.legend__grid {
			grid-template-columns: 1fr 1fr;
			align-items: start;
		}
	}

	.legend__chart {
		background: var(--color-foundation-mid);
		border-radius: var(--radius-xl);
		padding: var(--space-4);
		border: 1px solid var(--color-border-subtle);
	}

	.legend__chart-title {
		font-family: var(--font-body);
		font-size: var(--text-xs);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		margin: 0 0 var(--space-3);
		text-align: center;
	}

	.legend__table {
		background: var(--color-foundation-mid);
		border-radius: var(--radius-xl);
		overflow: hidden;
		border: 1px solid var(--color-border-subtle);
	}

	.legend__row {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		padding: var(--space-3) var(--space-4);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.legend__row:last-child {
		border-bottom: none;
	}

	.legend__swatch {
		width: 14px;
		height: 14px;
		border-radius: var(--radius-sm);
		flex-shrink: 0;
	}

	.legend__swatch--very-high { background: var(--color-score-very-high); }
	.legend__swatch--high { background: var(--color-score-high); }
	.legend__swatch--medium { background: var(--color-score-medium); }
	.legend__swatch--low { background: var(--color-score-low); }
	.legend__swatch--very-low { background: var(--color-score-very-low); }

	.legend__label {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-text-primary);
		min-width: 140px;
	}

	.legend__desc {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	@media (max-width: 480px) {
		.legend__desc {
			display: none;
		}
	}

	/* Sections */
	.sections {
		margin-bottom: var(--space-8);
	}

	.sections__title {
		font-family: var(--font-body);
		font-size: var(--text-xs);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		margin-bottom: var(--space-4);
	}

	/* Accordion Content */
	.lead {
		font-size: var(--text-base);
		color: var(--color-text-primary);
	}

	/* Summary callouts */
	.eli5 {
		background: var(--color-accent-primary-glow);
		border-left: 3px solid var(--color-accent-primary);
		padding: var(--space-3) var(--space-4);
		border-radius: 0 var(--radius-md) var(--radius-md) 0;
		margin-bottom: var(--space-4);
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	.eli5 strong {
		color: var(--color-accent-primary);
	}

	.eli5 a {
		color: var(--color-accent-primary);
	}

	/* Example boxes */
	.example-box {
		background: var(--color-foundation-deep);
		border: 1px solid var(--color-border-subtle);
		padding: var(--space-3) var(--space-4);
		border-radius: var(--radius-md);
		margin: var(--space-4) 0;
		font-size: var(--text-sm);
	}

	.example-box strong {
		color: var(--color-accent-secondary);
	}

	:global(.about h3) {
		font-family: var(--font-body);
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin: var(--space-5) 0 var(--space-2);
	}

	:global(.about h3:first-child) {
		margin-top: 0;
	}

	/* Links in lists */
	:global(.about ul a),
	:global(.about p a) {
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	:global(.about ul a:hover),
	:global(.about p a:hover) {
		text-decoration: underline;
	}

	:global(.about h4) {
		font-family: var(--font-body);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		margin: 0 0 var(--space-2);
	}

	/* Use Grid */
	.use-grid {
		display: grid;
		gap: var(--space-4);
	}

	@media (min-width: 500px) {
		.use-grid {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	.use-card {
		background: var(--color-foundation-deep);
		border-radius: var(--radius-lg);
		padding: var(--space-4);
	}

	.use-card--appropriate h4 {
		color: var(--color-success);
	}

	.use-card--inappropriate h4 {
		color: var(--color-error);
	}

	.use-card ul {
		margin: 0;
		padding-left: var(--space-5);
	}

	.use-card li {
		font-size: var(--text-sm);
		margin-bottom: var(--space-1);
	}

	.use-card li a {
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	.use-card li a:hover {
		text-decoration: underline;
	}

	.use-audience-links {
		margin-top: var(--space-4);
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	.use-audience-links a {
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	.use-audience-links a:hover {
		text-decoration: underline;
	}

	/* API Endpoints */
	.api {
		background: var(--color-foundation-deep);
		border-radius: var(--radius-lg);
		overflow: hidden;
	}

	.api__endpoint {
		display: flex;
		align-items: center;
		gap: var(--space-2);
		padding: var(--space-3) var(--space-4);
		border-bottom: 1px solid var(--color-border-subtle);
		flex-wrap: wrap;
	}

	.api__endpoint:last-child {
		border-bottom: none;
	}

	.api__method {
		background: var(--color-accent-primary);
		color: white;
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		font-weight: var(--font-weight-semibold);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.api__path {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-primary);
	}

	.api__desc {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		width: 100%;
		margin-top: var(--space-1);
	}

	@media (min-width: 500px) {
		.api__desc {
			width: auto;
			margin-top: 0;
			margin-left: auto;
		}
	}

	/* Code */
	:global(.about pre) {
		background: var(--color-foundation-deep);
		border-radius: var(--radius-lg);
		padding: var(--space-4);
		overflow-x: auto;
	}

	:global(.about code) {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
	}

	/* Screen reader */
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
