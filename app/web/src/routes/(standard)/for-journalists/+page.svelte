<script lang="ts">
</script>

<svelte:head>
	<title>For Journalists | Community Resilience Mapping</title>
	<meta
		name="description"
		content="Story-ready findings on community health resilience. Find your local data, explore surprising patterns, and access downloadable datasets."
	/>
</svelte:head>

<div class="persona-page">
	<div class="container">
		<!-- Header -->
		<header class="header">
			<p class="header__eyebrow">For Data Journalists</p>
			<h1 class="header__title">Story-Ready Findings</h1>
			<p class="header__subtitle">
				Counterintuitive patterns in community health resilience.
				Find your local data and uncover stories that matter.
			</p>
		</header>

		<!-- Story Starters -->
		<section class="stories" aria-labelledby="stories-heading">
			<h2 id="stories-heading" class="section-title">Story Starters</h2>
			<div class="stories-grid">
				<a href="/research/special-populations" class="story-card story-card--featured">
					<span class="story-card__badge">Headline</span>
					<h3 class="story-card__title">The 4 Standard Deviation Gap</h3>
					<p class="story-card__description">
						College communities average +2.95 resilience. Prison communities average -0.98.
						Education vs. incarceration: a 4 SD divide in community health.
					</p>
					<span class="story-card__link">Read the Story →</span>
				</a>

				<a href="/research/ohio-bifurcation" class="story-card">
					<h3 class="story-card__title">Ohio's Bifurcation</h3>
					<p class="story-card__description">
						Columbus has some of America's healthiest tracts. Cleveland has some of the worst.
						Same state, 140 miles apart, 10+ SD difference.
					</p>
					<span class="story-card__link">Explore →</span>
				</a>

				<a href="/research/inequality-chasm" class="story-card">
					<h3 class="story-card__title">The 9-Point Chasm</h3>
					<p class="story-card__description">
						Within single counties, resilience varies by 9+ points. Same governance,
						vastly different outcomes. The hyperlocal matters.
					</p>
					<span class="story-card__link">Explore →</span>
				</a>

				<a href="/research/west-virginia-paradox" class="story-card">
					<h3 class="story-card__title">The West Virginia Paradox</h3>
					<p class="story-card__description">
						Highest health burden in America, yet near-average resilience.
						What protective factors are communities providing?
					</p>
					<span class="story-card__link">Explore →</span>
				</a>

				<a href="/research/papers/immigrant-health-advantage" class="story-card story-card--new">
					<span class="story-card__badge story-card__badge--new">New</span>
					<h3 class="story-card__title">The Hispanic Paradox Is an Artifact</h3>
					<p class="story-card__description">
						South American communities: +0.147 correlation. Mexican communities: -0.029.
						The aggregate statistic masks a 2.6 SD gap within Texas alone.
					</p>
					<span class="story-card__link">Read the Paper →</span>
				</a>

				<a href="/research/papers/health-equity" class="story-card story-card--new">
					<span class="story-card__badge story-card__badge--new">New</span>
					<h3 class="story-card__title">0.43 SD Health Equity Gap</h3>
					<p class="story-card__description">
						Majority-minority communities show lower resilience on average—but DC shows
						+1.87 SD advantage while Mississippi shows -0.89 SD disadvantage. Equity is achievable.
					</p>
					<span class="story-card__link">Read the Paper →</span>
				</a>
			</div>
		</section>

		<!-- Find Your Story -->
		<section class="local" aria-labelledby="local-heading">
			<h2 id="local-heading" class="section-title">Find Your Local Story</h2>
			<div class="local-content">
				<p>
					Every region has a story. Use our tools to find the resilience outliers
					in your coverage area—communities thriving against the odds, or struggling
					despite advantages.
				</p>
				<div class="local-actions">
					<a href="/map" class="btn btn--primary">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
							<path fill-rule="evenodd" d="M8.161 2.58a1.875 1.875 0 011.678 0l4.993 2.498c.106.052.23.052.336 0l3.869-1.935A1.875 1.875 0 0121.75 4.82v12.485c0 .71-.401 1.36-1.037 1.677l-4.875 2.437a1.875 1.875 0 01-1.676 0l-4.994-2.497a.375.375 0 00-.336 0l-3.868 1.935A1.875 1.875 0 012.25 19.18V6.695c0-.71.401-1.36 1.036-1.677l4.875-2.437z" clip-rule="evenodd" />
						</svg>
						Explore Map
					</a>
					<a href="/data" class="btn btn--secondary">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
							<path fill-rule="evenodd" d="M4.5 2A1.5 1.5 0 003 3.5v13A1.5 1.5 0 004.5 18h11a1.5 1.5 0 001.5-1.5V7.621a1.5 1.5 0 00-.44-1.06l-4.12-4.122A1.5 1.5 0 0011.378 2H4.5z" clip-rule="evenodd" />
						</svg>
						Download Data
					</a>
				</div>
			</div>
		</section>

		<!-- Key Metrics -->
		<section class="metrics" aria-labelledby="metrics-heading">
			<h2 id="metrics-heading" class="section-title">Key Metrics Explained</h2>
			<div class="metrics-grid">
				<div class="metric-card">
					<h3>Resilience Score</h3>
					<p>
						How much better or worse a community's health outcomes are than predicted
						by its socioeconomic conditions. Positive = healthier than expected.
						Scale ranges roughly -5 to +5.
					</p>
				</div>
				<div class="metric-card">
					<h3>Health Burden</h3>
					<p>
						Composite measure of chronic disease, mental health, preventive care gaps,
						and behavioral risk factors. Higher = more health challenges.
						Standardized with mean 0.
					</p>
				</div>
				<div class="metric-card">
					<h3>Census Tract</h3>
					<p>
						Geographic unit averaging ~4,000 people. Small enough to show neighborhood
						variation, large enough for statistical reliability. There are 54,560
						residential tracts in our dataset.
					</p>
				</div>
			</div>
		</section>

		<!-- Press Materials -->
		<section class="press-kit" aria-labelledby="press-heading">
			<h2 id="press-heading" class="section-title">Press Materials</h2>
			<div class="press-grid">
				<a href="https://github.com/cschuman/resilience-mapping/blob/main/docs/press/PRESS-RELEASE-COLLEGE-VS-PRISON.md" class="press-card press-card--featured" target="_blank" rel="noopener">
					<span class="press-badge">Featured</span>
					<h3>Press Release: College vs Prison</h3>
					<p>The 4 standard deviation health gap between education and incarceration communities.</p>
				</a>
				<a href="https://github.com/cschuman/resilience-mapping/blob/main/docs/press/PRESS-RELEASE-HISPANIC-PARADOX.md" class="press-card" target="_blank" rel="noopener">
					<h3>Press Release: Hispanic Paradox</h3>
					<p>Why aggregate Hispanic health data masks dramatic heterogeneity.</p>
				</a>
				<a href="https://github.com/cschuman/resilience-mapping/blob/main/docs/press/PRESS-RELEASE-OHIO-BIFURCATION.md" class="press-card" target="_blank" rel="noopener">
					<h3>Press Release: Ohio's Health Divide</h3>
					<p>Columbus vs Cleveland: 140 miles apart, 10+ standard deviations different.</p>
				</a>
				<a href="https://github.com/cschuman/resilience-mapping/blob/main/docs/press/FACT-SHEET-JOURNALISTS.md" class="press-card" target="_blank" rel="noopener">
					<h3>Journalist Fact Sheet</h3>
					<p>Quick-reference guide to all major findings with interpretation guidelines.</p>
				</a>
			</div>
		</section>

		<!-- Contact -->
		<section class="contact" aria-labelledby="contact-heading">
			<h2 id="contact-heading" class="section-title">Need Help with Your Story?</h2>
			<p class="contact-text">
				We're happy to help journalists understand the data, identify local patterns,
				or provide context for stories. The data is open access—no restrictions on use.
			</p>
			<p class="contact-text">
				<strong>Citation:</strong> Community Resilience Mapping Project (2025). https://odds.health
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
		color: var(--color-accent-secondary);
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

	/* Stories */
	.stories {
		margin-bottom: var(--space-12);
	}

	.stories-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: var(--space-5);
	}

	.story-card {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-5);
		text-decoration: none;
		color: inherit;
		transition: all var(--duration-normal) var(--ease-out);
	}

	.story-card:hover {
		border-color: var(--color-accent-secondary);
		box-shadow: var(--shadow-lg);
		transform: translateY(-2px);
	}

	.story-card--featured {
		grid-column: span 2;
		background: linear-gradient(135deg, var(--color-foundation-mid), var(--color-accent-secondary-glow));
		border-color: var(--color-accent-secondary);
	}

	.story-card__badge {
		display: inline-block;
		font-size: var(--text-xs);
		font-weight: var(--font-weight-bold);
		color: var(--color-accent-secondary);
		background: rgba(232, 165, 71, 0.2);
		padding: var(--space-1) var(--space-3);
		border-radius: var(--radius-full);
		margin-bottom: var(--space-3);
	}

	.story-card__badge--new {
		color: var(--color-score-high);
		background: rgba(34, 197, 94, 0.2);
	}

	.story-card--new {
		border-color: var(--color-score-high);
	}

	.story-card__title {
		font-size: var(--text-lg);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.story-card__description {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-3);
	}

	.story-card__link {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-accent-secondary);
	}

	/* Local */
	.local {
		margin-bottom: var(--space-12);
	}

	.local-content {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
	}

	.local-content > p {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-6);
	}

	.local-actions {
		display: flex;
		gap: var(--space-4);
		flex-wrap: wrap;
	}

	/* Metrics */
	.metrics {
		margin-bottom: var(--space-12);
	}

	.metrics-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: var(--space-5);
	}

	.metric-card {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-5);
	}

	.metric-card h3 {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.metric-card p {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	/* Press Kit */
	.press-kit {
		margin-bottom: var(--space-12);
	}

	.press-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: var(--space-4);
	}

	.press-card {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-5);
		text-decoration: none;
		color: inherit;
		transition: all var(--duration-normal) var(--ease-out);
		position: relative;
	}

	.press-card:hover {
		border-color: var(--color-accent-secondary);
		box-shadow: var(--shadow-lg);
		transform: translateY(-2px);
	}

	.press-card--featured {
		border-color: var(--color-accent-secondary);
		background: linear-gradient(135deg, var(--color-foundation-mid), var(--color-accent-secondary-glow));
	}

	.press-badge {
		position: absolute;
		top: var(--space-3);
		right: var(--space-3);
		font-size: var(--text-xs);
		font-weight: var(--font-weight-bold);
		color: var(--color-accent-secondary);
		background: rgba(232, 165, 71, 0.2);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-full);
	}

	.press-card h3 {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.press-card p {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	/* Contact */
	.contact-text {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-4);
	}

	.contact-text strong {
		color: var(--color-text-primary);
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

	.btn svg {
		width: 18px;
		height: 18px;
	}

	.btn--primary {
		background: var(--color-accent-secondary);
		color: var(--color-foundation-deepest);
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

	@media (max-width: 700px) {
		.story-card--featured {
			grid-column: span 1;
		}
	}

	@media (max-width: 640px) {
		.container {
			padding: var(--space-6) var(--space-4) var(--space-12);
		}

		.local-actions {
			flex-direction: column;
		}

		.btn {
			width: 100%;
			justify-content: center;
		}
	}
</style>
