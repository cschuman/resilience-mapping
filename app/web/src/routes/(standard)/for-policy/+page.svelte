<script lang="ts">
</script>

<svelte:head>
	<title>For Policy Analysts | Community Resilience Mapping</title>
	<meta
		name="description"
		content="Evidence for place-based interventions. Identify communities with protective factors, target resources effectively, and evaluate geographic health equity."
	/>
</svelte:head>

<div class="persona-page">
	<div class="container">
		<!-- Header -->
		<header class="header">
			<p class="header__eyebrow">For Policy & Planning</p>
			<h1 class="header__title">Evidence for Action</h1>
			<p class="header__subtitle">
				Identify communities that succeed against the odds. Target resources where they're
				needed most. Evaluate geographic health equity at scale.
			</p>
		</header>

		<!-- Key Insights -->
		<section class="insights" aria-labelledby="insights-heading">
			<h2 id="insights-heading" class="section-title">Policy-Relevant Insights</h2>
			<div class="insights-grid">
				<div class="insight-card">
					<div class="insight-card__number">4 SD</div>
					<h3 class="insight-card__title">Education vs. Incarceration Gap</h3>
					<p class="insight-card__description">
						College communities average +2.95 resilience; prison communities average -0.98.
						This 4 standard deviation gap raises questions about resource allocation and
						the health impacts of different institutional investments.
					</p>
					<a href="/research/special-populations" class="insight-card__link">Explore Data →</a>
				</div>

				<div class="insight-card">
					<div class="insight-card__number">9+ pts</div>
					<h3 class="insight-card__title">Intra-County Inequality</h3>
					<p class="insight-card__description">
						Within single counties, resilience scores vary by 9+ points. County-wide policies
						may miss hyperlocal variation. Neighborhood-level targeting may be more effective.
					</p>
					<a href="/research/inequality-chasm" class="insight-card__link">Explore Data →</a>
				</div>

				<div class="insight-card">
					<div class="insight-card__number">WV</div>
					<h3 class="insight-card__title">Protective Factors in High-Burden Areas</h3>
					<p class="insight-card__description">
						West Virginia has America's highest health burden but near-average resilience.
						Understanding what works in challenging conditions can inform interventions elsewhere.
					</p>
					<a href="/research/west-virginia-paradox" class="insight-card__link">Explore Data →</a>
				</div>

				<div class="insight-card insight-card--new">
					<span class="insight-badge">New Research</span>
					<div class="insight-card__number">0.43</div>
					<h3 class="insight-card__title">Health Equity Gap (Modifiable)</h3>
					<p class="insight-card__description">
						Majority-minority communities average 0.43 SD lower resilience—but state variation
						from +1.87 SD (DC) to -0.89 SD (Mississippi) proves structural factors determine outcomes.
					</p>
					<a href="/research/papers/health-equity" class="insight-card__link">Read Paper →</a>
				</div>

				<div class="insight-card insight-card--new">
					<span class="insight-badge">New Research</span>
					<div class="insight-card__number">2.6</div>
					<h3 class="insight-card__title">Hispanic Paradox Is an Artifact</h3>
					<p class="insight-card__description">
						Aggregate Hispanic data masks 2.6 SD gap within Texas. South American communities thrive
						(+0.147) while Mexican-American border communities struggle (-1.08 SD). Policy implications differ.
					</p>
					<a href="/research/papers/immigrant-health-advantage" class="insight-card__link">Read Paper →</a>
				</div>
			</div>
		</section>

		<!-- Use Cases -->
		<section class="use-cases" aria-labelledby="use-heading">
			<h2 id="use-heading" class="section-title">Policy Applications</h2>
			<div class="use-grid">
				<div class="use-card use-card--appropriate">
					<h3>Appropriate Uses</h3>
					<ul>
						<li>Identifying communities for qualitative follow-up research</li>
						<li>Asset-based community development planning</li>
						<li>Geographic targeting of health interventions</li>
						<li>Evaluating community health equity across regions</li>
						<li>Understanding variation within counties/states</li>
					</ul>
				</div>
				<div class="use-card use-card--caution">
					<h3>Use with Caution</h3>
					<ul>
						<li>Justifying disinvestment from "resilient" communities</li>
						<li>Making predictions about individual health</li>
						<li>Punitive comparisons between communities</li>
						<li>Replacing qualitative community input</li>
						<li>Definitive claims about causation</li>
					</ul>
				</div>
			</div>
		</section>

		<!-- Priority Interventions -->
		<section class="interventions" aria-labelledby="interventions-heading">
			<h2 id="interventions-heading" class="section-title">Suggested Priority Areas</h2>
			<p class="interventions-intro">
				Based on our analysis, these intervention categories show the highest potential impact:
			</p>
			<div class="interventions-list">
				<div class="intervention">
					<span class="intervention__number">1</span>
					<div class="intervention__content">
						<h3>Education-Based Resilience</h3>
						<p>
							College towns demonstrate that educational infrastructure creates health spillovers.
							Community college expansion, workforce training, and early childhood education
							may produce long-term community health benefits.
						</p>
					</div>
				</div>
				<div class="intervention">
					<span class="intervention__number">2</span>
					<div class="intervention__content">
						<h3>Reentry Support Networks</h3>
						<p>
							Prison communities show dramatic resilience deficits. Investing in reentry
							support, community integration, and alternatives to incarceration could address
							the widest gaps in our data.
						</p>
					</div>
				</div>
				<div class="intervention">
					<span class="intervention__number">3</span>
					<div class="intervention__content">
						<h3>Hyperlocal Targeting</h3>
						<p>
							The 9+ point gaps within counties suggest that neighborhood-level interventions
							may be more effective than county-wide programs. Precision targeting of resources
							could improve outcomes.
						</p>
					</div>
				</div>
				<div class="intervention">
					<span class="intervention__number">4</span>
					<div class="intervention__content">
						<h3>Learning from High-Burden Successes</h3>
						<p>
							Communities like those in West Virginia that maintain resilience despite high
							burden may offer lessons. Qualitative research to understand protective factors
							could inform interventions.
						</p>
					</div>
				</div>
			</div>
		</section>

		<!-- Data Access -->
		<section class="data-access" aria-labelledby="access-heading">
			<h2 id="access-heading" class="section-title">Access the Data</h2>
			<div class="access-content">
				<p>
					All data is freely available for policy research. No registration or approval required.
					Download the full dataset or use our API for programmatic access.
				</p>
				<div class="access-actions">
					<a href="/data" class="btn btn--primary">Download Dataset</a>
					<a href="/map" class="btn btn--secondary">Explore Map</a>
					<a href="/about#api" class="btn btn--secondary">API Access</a>
				</div>
			</div>
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
		color: var(--color-score-high);
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

	.section-title {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		color: var(--color-text-primary);
		margin-bottom: var(--space-6);
		padding-bottom: var(--space-3);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	/* Insights */
	.insights {
		margin-bottom: var(--space-12);
	}

	.insights-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: var(--space-5);
	}

	.insight-card {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
	}

	.insight-card__number {
		font-family: var(--font-display);
		font-size: var(--text-3xl);
		color: var(--color-score-high);
		margin-bottom: var(--space-3);
	}

	.insight-card__title {
		font-size: var(--text-lg);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.insight-card__description {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-4);
	}

	.insight-card__link {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	.insight-card__link:hover {
		text-decoration: underline;
	}

	.insight-card--new {
		border-color: var(--color-score-high);
		position: relative;
	}

	.insight-badge {
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

	/* Use Cases */
	.use-cases {
		margin-bottom: var(--space-12);
	}

	.use-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: var(--space-5);
	}

	.use-card {
		background: var(--color-foundation-mid);
		border-radius: var(--radius-xl);
		padding: var(--space-5);
	}

	.use-card h3 {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		margin-bottom: var(--space-3);
	}

	.use-card--appropriate {
		border: 1px solid var(--color-score-high);
	}

	.use-card--appropriate h3 {
		color: var(--color-score-high);
	}

	.use-card--caution {
		border: 1px solid var(--color-warning);
	}

	.use-card--caution h3 {
		color: var(--color-warning);
	}

	.use-card ul {
		margin: 0;
		padding-left: var(--space-6);
		list-style-type: disc;
		list-style-position: outside;
	}

	.use-card li {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-2);
		line-height: var(--leading-relaxed);
		padding-left: var(--space-2);
	}

	.use-card li::marker {
		color: var(--color-text-muted);
	}

	/* Interventions */
	.interventions {
		margin-bottom: var(--space-12);
	}

	.interventions-intro {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-6);
	}

	.interventions-list {
		display: flex;
		flex-direction: column;
		gap: var(--space-4);
	}

	.intervention {
		display: flex;
		gap: var(--space-4);
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-5);
	}

	.intervention__number {
		width: 36px;
		height: 36px;
		background: var(--color-score-high);
		color: white;
		border-radius: var(--radius-full);
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: var(--font-weight-bold);
		flex-shrink: 0;
	}

	.intervention__content h3 {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.intervention__content p {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	/* Data Access */
	.data-access {
		margin-bottom: var(--space-12);
	}

	.access-content {
		background: linear-gradient(135deg, var(--color-score-high-bg), var(--color-accent-primary-glow));
		border: 1px solid var(--color-score-high);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
		text-align: center;
	}

	.access-content > p {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-6);
		max-width: 600px;
		margin-left: auto;
		margin-right: auto;
	}

	.access-actions {
		display: flex;
		gap: var(--space-4);
		justify-content: center;
		flex-wrap: wrap;
	}

	/* Buttons */
	.btn {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		padding: var(--space-3) var(--space-5);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		border-radius: var(--radius-lg);
		text-decoration: none;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.btn--primary {
		background: var(--color-score-high);
		color: white;
	}

	.btn--primary:hover {
		filter: brightness(1.1);
	}

	.btn--secondary {
		background: transparent;
		color: var(--color-text-secondary);
		border: 1px solid var(--color-border-default);
	}

	.btn--secondary:hover {
		background: var(--color-foundation-surface);
		border-color: var(--color-border-strong);
	}

	@media (max-width: 640px) {
		.container {
			padding: var(--space-6) var(--space-4) var(--space-12);
		}

		.intervention {
			flex-direction: column;
			gap: var(--space-2);
		}

		.access-actions {
			flex-direction: column;
		}

		.btn {
			width: 100%;
			justify-content: center;
		}
	}
</style>
