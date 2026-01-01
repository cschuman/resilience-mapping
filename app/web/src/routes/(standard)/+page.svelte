<script lang="ts">
	import type { PageData } from './$types';
	import { AddressSearch } from '$lib/components/search';
	import { MiniMap } from '$lib/components/viz';
	import { goto } from '$app/navigation';
	import type { GeocoderResult } from '$lib/components/map';
	import { onMount } from 'svelte';

	let { data }: { data: PageData } = $props();

	// Animation states
	let mounted = $state(false);

	onMount(() => {
		// Trigger entrance animations after mount
		mounted = true;
	});

	/**
	 * Handle search result - navigate to map with the selected tract
	 */
	function handleSearchSelect(result: GeocoderResult): void {
		goto(`/map?tract=${result.tractFips}&lat=${result.lat.toFixed(4)}&lng=${result.lng.toFixed(4)}&zoom=12`);
	}
</script>

<svelte:head>
	<title>Where You Live Explains 28% of Your Health | odds.health</title>
	<meta
		name="description"
		content="Geography explains more health variance than income or education. Explore 54,000+ census tracts to find communities that defy prediction."
	/>
</svelte:head>

<div class="home" class:home--mounted={mounted}>
	<!-- Hero Section -->
	<section class="hero">
		<div class="hero__content">
			<p class="hero__eyebrow">Research Finding</p>
			<h1 class="hero__title">
				<em>Where</em> You Live Explains
				28% of Your Health
			</h1>
			<p class="hero__subtitle">
				Our analysis of 54,000+ census tracts reveals geography alone explains more
				health variance than income, education, or access combined. But some communities
				defy prediction—with outcomes far better than their circumstances suggest.
			</p>

			<!-- Actions -->
			<div class="hero__actions">
				<a href="/data" class="btn btn--primary">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
						<path d="M10.75 2.75a.75.75 0 00-1.5 0v8.614L6.295 8.235a.75.75 0 10-1.09 1.03l4.25 4.5a.75.75 0 001.09 0l4.25-4.5a.75.75 0 00-1.09-1.03l-2.955 3.129V2.75z" />
						<path d="M3.5 12.75a.75.75 0 00-1.5 0v2.5A2.75 2.75 0 004.75 18h10.5A2.75 2.75 0 0018 15.25v-2.5a.75.75 0 00-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5z" />
					</svg>
					<span>Download Dataset</span>
				</a>
				<a href="/map" class="btn btn--ghost">
					<span>Explore Map</span>
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
						<path fill-rule="evenodd" d="M3 10a.75.75 0 01.75-.75h10.638L10.23 5.29a.75.75 0 111.04-1.08l5.5 5.25a.75.75 0 010 1.08l-5.5 5.25a.75.75 0 11-1.04-1.08l4.158-3.96H3.75A.75.75 0 013 10z" clip-rule="evenodd" />
					</svg>
				</a>
				<a href="/about" class="btn btn--ghost">
					Methodology
				</a>
			</div>
		</div>

		<!-- Stats -->
		<div class="hero__stats">
			<div class="stat">
				<span class="stat__value">{data.stats.totalTracts.toLocaleString()}</span>
				<span class="stat__label">Census Tracts</span>
			</div>
			<div class="stat">
				<span class="stat__value">{data.stats.stateCount}</span>
				<span class="stat__label">States + DC</span>
			</div>
			<div class="stat">
				<span class="stat__value">{(data.stats.totalPopulation / 1_000_000).toFixed(0)}M+</span>
				<span class="stat__label">People</span>
			</div>
		</div>
	</section>

	<!-- Map Preview -->
	<section class="map-preview">
		<MiniMap />
	</section>

	<!-- Latest Research - Prominent CTA -->
	<section class="latest-research" aria-labelledby="research-heading">
		<div class="latest-research__content">
			<p class="latest-research__eyebrow">Key Finding</p>
			<h2 id="research-heading" class="latest-research__title">
				College Towns vs Prison Towns: A 4 SD Health Divide
			</h2>
			<p class="latest-research__description">
				Communities built around education show <strong class="positive">+2.95</strong> resilience.
				Communities built around incarceration show <strong class="negative">-0.98</strong>.
				Same country, same healthcare system—4 standard deviations apart.
			</p>
			<a href="/research/special-populations" class="latest-research__cta">
				<span>Explore the Data</span>
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
					<path fill-rule="evenodd" d="M3 10a.75.75 0 01.75-.75h10.638L10.23 5.29a.75.75 0 111.04-1.08l5.5 5.25a.75.75 0 010 1.08l-5.5 5.25a.75.75 0 11-1.04-1.08l4.158-3.96H3.75A.75.75 0 013 10z" clip-rule="evenodd" />
				</svg>
			</a>
		</div>
	</section>

	<!-- Top Performing Tracts -->
	<section class="featured" aria-labelledby="featured-heading">
		<header class="featured__header">
			<p class="featured__eyebrow">Positive Outliers</p>
			<h2 id="featured-heading" class="featured__title">
				Highest resilience scores
			</h2>
			<p class="featured__description">
				Tracts with health outcomes significantly better than predicted by socioeconomic factors.
			</p>
		</header>

		<div class="tracts">
			{#each data.topTracts.slice(0, 6) as tract, i}
				<a
					href="/map?tract={tract.fips}"
					class="tract"
					style="--delay: {i * 0.05}s"
				>
					<div class="tract__header">
						<span class="tract__percentile">Top {tract.topPercent}%</span>
					</div>
					<div class="tract__location">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="tract__icon" aria-hidden="true">
							<path fill-rule="evenodd" d="M9.69 18.933l.003.001C9.89 19.02 10 19 10 19s.11.02.308-.066l.002-.001.006-.003.018-.008a5.741 5.741 0 00.281-.14c.186-.096.446-.24.757-.433.62-.384 1.445-.966 2.274-1.765C15.302 14.988 17 12.493 17 9A7 7 0 103 9c0 3.492 1.698 5.988 3.355 7.584a13.731 13.731 0 002.273 1.765 11.842 11.842 0 00.976.544l.062.029.018.008.006.003zM10 11.25a2.25 2.25 0 100-4.5 2.25 2.25 0 000 4.5z" clip-rule="evenodd" />
						</svg>
						<span>{tract.state}</span>
					</div>
					<div class="tract__pop">{tract.population.toLocaleString()} residents</div>
					<div class="tract__cta">
						<span>View on map</span>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
							<path fill-rule="evenodd" d="M3 10a.75.75 0 01.75-.75h10.638L10.23 5.29a.75.75 0 111.04-1.08l5.5 5.25a.75.75 0 010 1.08l-5.5 5.25a.75.75 0 11-1.04-1.08l4.158-3.96H3.75A.75.75 0 013 10z" clip-rule="evenodd" />
						</svg>
					</div>
				</a>
			{/each}
		</div>

		<div class="featured__cta">
			<a href="/map" class="btn btn--outline">
				Explore Full Dataset
			</a>
		</div>
	</section>

	<!-- Research Findings -->
	<section class="findings" aria-labelledby="findings-heading">
		<header class="findings__header">
			<p class="findings__eyebrow">Research Insights</p>
			<h2 id="findings-heading" class="findings__title">What We've Learned</h2>
		</header>
		<div class="findings__grid">
			<div class="finding">
				<span class="finding__number">99.7%</span>
				<h3 class="finding__title">Stable Health Levels</h3>
				<p class="finding__description">
					Community health levels are remarkably consistent year-to-year.
					The factors that make communities resilient are deeply structural.
				</p>
			</div>
			<div class="finding">
				<span class="finding__number">28%</span>
				<h3 class="finding__title">Geographic Variation</h3>
				<p class="finding__description">
					Geography alone explains over a quarter of health outcome variance.
					Where you live matters as much as how you live.
				</p>
			</div>
			<div class="finding">
				<span class="finding__number">r = -0.72</span>
				<h3 class="finding__title">Burden Correlation</h3>
				<p class="finding__description">
					Strong inverse relationship between community burden and resilience.
					Communities facing the most challenges often show the least resilience.
				</p>
			</div>
		</div>
		<div class="findings__cta">
			<a href="/research" class="btn btn--outline-teal">
				Read Full Research
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
					<path fill-rule="evenodd" d="M3 10a.75.75 0 01.75-.75h10.638L10.23 5.29a.75.75 0 111.04-1.08l5.5 5.25a.75.75 0 010 1.08l-5.5 5.25a.75.75 0 11-1.04-1.08l4.158-3.96H3.75A.75.75 0 013 10z" clip-rule="evenodd" />
				</svg>
			</a>
		</div>
	</section>

	<!-- Audience Segments -->
	<section class="audiences" aria-labelledby="audiences-heading">
		<h2 id="audiences-heading" class="sr-only">Who uses this data</h2>
		<div class="audiences__grid">
			<a href="/for-researchers" class="audience">
				<div class="audience__icon">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
						<path d="M11.7 2.805a.75.75 0 01.6 0A60.65 60.65 0 0122.83 8.72a.75.75 0 01-.231 1.337 49.949 49.949 0 00-9.902 3.912l-.003.002-.34.18a.75.75 0 01-.707 0A50.009 50.009 0 007.5 12.174v-.224c0-.131.067-.248.172-.311a54.614 54.614 0 014.653-2.52.75.75 0 00-.65-1.352 56.129 56.129 0 00-4.78 2.589 1.858 1.858 0 00-.859 1.228 49.803 49.803 0 00-4.634-1.527.75.75 0 01-.231-1.337A60.653 60.653 0 0111.7 2.805z" />
						<path d="M13.06 15.473a48.45 48.45 0 017.666-3.282c.134 1.414.22 2.843.255 4.285a.75.75 0 01-.46.71 47.878 47.878 0 00-8.105 4.342.75.75 0 01-.832 0 47.877 47.877 0 00-8.104-4.342.75.75 0 01-.461-.71c.035-1.442.121-2.87.255-4.286A48.4 48.4 0 016 13.18v1.27a1.5 1.5 0 00-.14 2.508c-.09.38-.222.753-.397 1.11.452.213.901.434 1.346.661a6.729 6.729 0 00.551-1.608 1.5 1.5 0 00.14-2.67v-.645a48.549 48.549 0 013.44 1.668 2.25 2.25 0 002.12 0z" />
						<path d="M4.462 19.462c.42-.419.753-.89 1-1.394.453.213.902.434 1.347.661a6.743 6.743 0 01-1.286 1.794.75.75 0 11-1.06-1.06z" />
					</svg>
				</div>
				<h3 class="audience__title">Researchers</h3>
				<p class="audience__description">
					Validated tract-level resilience scores with full methodology documentation
					and API access for large-scale analysis.
				</p>
			</a>
			<a href="/for-journalists" class="audience">
				<div class="audience__icon">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
						<path fill-rule="evenodd" d="M4.125 3C3.089 3 2.25 3.84 2.25 4.875V18a3 3 0 003 3h15a3 3 0 01-3-3V4.875C17.25 3.839 16.41 3 15.375 3H4.125zM12 9.75a.75.75 0 000 1.5h1.5a.75.75 0 000-1.5H12zm-.75-2.25a.75.75 0 01.75-.75h1.5a.75.75 0 010 1.5H12a.75.75 0 01-.75-.75zM6 12.75a.75.75 0 000 1.5h7.5a.75.75 0 000-1.5H6zm-.75 3.75a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5H6a.75.75 0 01-.75-.75zM6 6.75a.75.75 0 00-.75.75v3c0 .414.336.75.75.75h3a.75.75 0 00.75-.75v-3A.75.75 0 009 6.75H6z" clip-rule="evenodd" />
						<path d="M18.75 6.75h1.875c.621 0 1.125.504 1.125 1.125V18a1.5 1.5 0 01-3 0V6.75z" />
					</svg>
				</div>
				<h3 class="audience__title">Journalists</h3>
				<p class="audience__description">
					Story-ready data with state and county comparisons. Find the
					resilience outliers in your coverage area.
				</p>
			</a>
			<a href="/for-policy" class="audience">
				<div class="audience__icon">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
						<path fill-rule="evenodd" d="M8.25 6.75a3.75 3.75 0 117.5 0 3.75 3.75 0 01-7.5 0zM15.75 9.75a3 3 0 116 0 3 3 0 01-6 0zM2.25 9.75a3 3 0 116 0 3 3 0 01-6 0zM6.31 15.117A6.745 6.745 0 0112 12a6.745 6.745 0 016.709 7.498.75.75 0 01-.372.568A12.696 12.696 0 0112 21.75c-2.305 0-4.47-.612-6.337-1.684a.75.75 0 01-.372-.568 6.787 6.787 0 011.019-4.38z" clip-rule="evenodd" />
						<path d="M5.082 14.254a8.287 8.287 0 00-1.308 5.135 9.687 9.687 0 01-1.764-.44l-.115-.04a.563.563 0 01-.373-.487l-.01-.121a3.75 3.75 0 013.57-4.047zM20.226 19.389a8.287 8.287 0 00-1.308-5.135 3.75 3.75 0 013.57 4.047l-.01.121a.563.563 0 01-.373.486l-.115.04c-.567.2-1.156.349-1.764.441z" />
					</svg>
				</div>
				<h3 class="audience__title">Policy Analysts</h3>
				<p class="audience__description">
					Evidence for place-based interventions. Identify communities
					with successful health outcomes despite economic challenges.
				</p>
			</a>
		</div>
	</section>

	<!-- Citation & Data Access -->
	<section class="citation" aria-labelledby="citation-heading">
		<div class="citation__content">
			<p class="citation__eyebrow">Open Access</p>
			<h2 id="citation-heading" class="citation__title">
				Use This Data in Your Work
			</h2>
			<p class="citation__description">
				This dataset is free for academic research, journalism, and policy analysis.
				No registration required. Please cite when publishing.
			</p>
			<div class="citation__block">
				<code>Community Resilience Mapping Project (2025). Census tract-level health resilience scores for the United States. https://odds.health</code>
			</div>
			<div class="citation__actions">
				<a href="/data" class="btn btn--secondary">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
						<path d="M10.75 2.75a.75.75 0 00-1.5 0v8.614L6.295 8.235a.75.75 0 10-1.09 1.03l4.25 4.5a.75.75 0 001.09 0l4.25-4.5a.75.75 0 00-1.09-1.03l-2.955 3.129V2.75z" />
						<path d="M3.5 12.75a.75.75 0 00-1.5 0v2.5A2.75 2.75 0 004.75 18h10.5A2.75 2.75 0 0018 15.25v-2.5a.75.75 0 00-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5z" />
					</svg>
					<span>Browse & Download</span>
				</a>
				<a href="/about#api" class="btn btn--ghost">
					API Documentation
				</a>
			</div>
		</div>
	</section>
</div>

<style>
	/* ==========================================
	 * HOME PAGE
	 * ========================================== */

	.home {
		color: var(--color-text-primary);
	}

	/* ==========================================
	 * HERO SECTION
	 * ========================================== */

	.hero {
		padding: var(--space-16) var(--space-6) var(--space-12);
		max-width: var(--container-content);
		margin: 0 auto;
		text-align: center;
	}

	.hero__content {
		margin-bottom: var(--space-12);
	}

	.hero__eyebrow {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-accent-primary);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		margin-bottom: var(--space-4);
		opacity: 0;
		transform: translateY(16px);
		animation: fadeUp var(--duration-entrance) var(--ease-cinematic) forwards;
		animation-delay: 0.1s;
	}

	.home--mounted .hero__eyebrow {
		animation-play-state: running;
	}

	.hero__title {
		font-family: var(--font-display);
		font-size: clamp(var(--text-3xl), 5vw, var(--text-5xl));
		font-weight: var(--font-weight-normal);
		line-height: var(--leading-snug);
		letter-spacing: var(--tracking-display);
		color: var(--color-text-primary);
		margin-bottom: var(--space-6);
		opacity: 0;
		transform: translateY(20px);
		animation: fadeUp var(--duration-entrance) var(--ease-cinematic) forwards;
		animation-delay: 0.2s;
	}

	.hero__title em {
		font-style: italic;
		color: var(--color-accent-primary);
	}

	.hero__subtitle {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		max-width: 560px;
		margin: 0 auto var(--space-10);
		opacity: 0;
		transform: translateY(20px);
		animation: fadeUp var(--duration-entrance) var(--ease-cinematic) forwards;
		animation-delay: 0.3s;
	}

	.hero__actions {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: var(--space-4);
		opacity: 0;
		transform: translateY(20px);
		animation: fadeUp var(--duration-entrance) var(--ease-cinematic) forwards;
		animation-delay: 0.5s;
	}

	.hero__stats {
		display: flex;
		justify-content: center;
		gap: var(--space-8);
		padding-top: var(--space-8);
		border-top: 1px solid var(--color-border-subtle);
		opacity: 0;
		animation: fadeIn var(--duration-slow) var(--ease-out) forwards;
		animation-delay: 0.7s;
	}

	@media (max-width: 480px) {
		.hero__stats {
			gap: var(--space-4);
		}
	}

	/* ==========================================
	 * STAT COMPONENT
	 * ========================================== */

	.stat {
		text-align: center;
	}

	.stat__value {
		display: block;
		font-family: var(--font-display);
		font-size: var(--text-2xl);
		color: var(--color-text-primary);
		line-height: 1;
		margin-bottom: var(--space-1);
	}

	.stat__label {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wider);
	}

	/* ==========================================
	 * MAP PREVIEW
	 * ========================================== */

	.map-preview {
		padding: 0 var(--space-6) var(--space-12);
		max-width: var(--container-md);
		margin: 0 auto;
	}

	/* ==========================================
	 * LATEST RESEARCH SECTION
	 * ========================================== */

	.latest-research {
		padding: var(--space-12) var(--space-6);
		max-width: var(--container-lg);
		margin: 0 auto;
	}

	.latest-research__content {
		background: linear-gradient(135deg, var(--color-foundation-mid), var(--color-accent-primary-glow));
		border: 2px solid var(--color-accent-primary);
		border-radius: var(--radius-2xl);
		padding: var(--space-10);
		text-align: center;
	}

	.latest-research__eyebrow {
		font-size: var(--text-xs);
		font-weight: var(--font-weight-bold);
		color: var(--color-accent-primary);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		margin-bottom: var(--space-4);
	}

	.latest-research__title {
		font-family: var(--font-display);
		font-size: clamp(var(--text-2xl), 4vw, var(--text-3xl));
		font-weight: var(--font-weight-normal);
		line-height: var(--leading-snug);
		letter-spacing: var(--tracking-display);
		color: var(--color-text-primary);
		margin-bottom: var(--space-4);
	}

	.latest-research__description {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		max-width: 600px;
		margin: 0 auto var(--space-8);
	}

	.latest-research__description em {
		font-style: italic;
		color: var(--color-text-primary);
	}

	.latest-research__cta {
		display: inline-flex;
		align-items: center;
		gap: var(--space-3);
		padding: var(--space-4) var(--space-8);
		font-size: var(--text-lg);
		font-weight: var(--font-weight-bold);
		color: white;
		background: var(--color-accent-primary);
		border-radius: var(--radius-xl);
		text-decoration: none;
		transition: all var(--duration-normal) var(--ease-out);
		box-shadow: var(--shadow-lg), var(--shadow-glow-accent);
	}

	.latest-research__cta:hover {
		background: var(--color-accent-primary-hover);
		transform: translateY(-2px);
		box-shadow: var(--shadow-xl), 0 0 32px rgba(209, 104, 71, 0.4);
	}

	.latest-research__cta svg {
		width: 20px;
		height: 20px;
		transition: transform var(--duration-fast) var(--ease-spring);
	}

	.latest-research__cta:hover svg {
		transform: translateX(4px);
	}

	/* ==========================================
	 * FEATURED SECTION
	 * ========================================== */

	.featured {
		padding: var(--space-12) var(--space-6);
		max-width: var(--container-lg);
		margin: 0 auto;
	}

	.featured__header {
		text-align: center;
		margin-bottom: var(--space-10);
	}

	.featured__eyebrow {
		font-size: var(--text-xs);
		font-weight: var(--font-weight-semibold);
		color: var(--color-score-very-high);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		margin-bottom: var(--space-3);
	}

	.featured__title {
		font-family: var(--font-display);
		font-size: var(--text-3xl);
		color: var(--color-text-primary);
		margin-bottom: var(--space-4);
	}

	.featured__description {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		max-width: 480px;
		margin: 0 auto;
	}

	.tracts {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
		gap: var(--space-4);
		margin-bottom: var(--space-10);
	}

	.tract {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-5);
		text-decoration: none;
		color: inherit;
		transition: all var(--duration-normal) var(--ease-out);
		opacity: 0;
		animation: fadeUp var(--duration-slow) var(--ease-out) forwards;
		animation-delay: var(--delay);
	}

	.home--mounted .tract {
		animation-play-state: running;
	}

	.tract:hover {
		border-color: var(--color-score-very-high);
		background: var(--color-foundation-surface);
		box-shadow: var(--shadow-lg), 0 0 0 1px var(--color-score-very-high);
	}

	.tract__header {
		display: flex;
		justify-content: flex-end;
		align-items: center;
		margin-bottom: var(--space-3);
	}

	.tract__percentile {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-bold);
		color: var(--color-score-very-high);
		background: var(--color-score-very-high-bg);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.tract__location {
		display: flex;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-xl);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-1);
	}

	.tract__icon {
		width: 20px;
		height: 20px;
		color: var(--color-score-very-high);
		flex-shrink: 0;
	}

	.tract__pop {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		margin-bottom: var(--space-4);
	}

	.tract__cta {
		display: flex;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-score-very-high);
	}

	.tract__cta svg {
		width: 16px;
		height: 16px;
		transition: transform var(--duration-fast) var(--ease-spring);
	}

	.tract:hover .tract__cta svg {
		transform: translateX(4px);
	}

	.featured__cta {
		text-align: center;
	}

	/* ==========================================
	 * RESEARCH FINDINGS
	 * ========================================== */

	.findings {
		padding: var(--space-12) var(--space-6);
		max-width: var(--container-lg);
		margin: 0 auto;
		border-top: 1px solid var(--color-border-subtle);
	}

	.findings__header {
		text-align: center;
		margin-bottom: var(--space-10);
	}

	.findings__eyebrow {
		font-size: var(--text-xs);
		font-weight: var(--font-weight-semibold);
		color: var(--color-accent-secondary);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		margin-bottom: var(--space-3);
	}

	.findings__title {
		font-family: var(--font-display);
		font-size: var(--text-3xl);
		color: var(--color-text-primary);
	}

	.findings__grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: var(--space-6);
		margin-bottom: var(--space-10);
	}

	.finding {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
		text-align: center;
		transition: all var(--duration-normal) var(--ease-out);
	}

	.finding:hover {
		border-color: var(--color-accent-secondary);
		background: var(--color-foundation-surface);
	}

	.finding__number {
		display: block;
		font-family: var(--font-display);
		font-size: var(--text-4xl);
		color: var(--color-accent-secondary);
		line-height: 1;
		margin-bottom: var(--space-3);
	}

	.finding__title {
		font-family: var(--font-body);
		font-size: var(--text-lg);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.finding__description {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	.findings__cta {
		text-align: center;
	}

	.btn--outline-teal {
		background: transparent;
		color: var(--color-accent-secondary);
		border: 1px solid var(--color-accent-secondary);
	}

	.btn--outline-teal:hover {
		background: var(--color-accent-secondary);
		color: var(--color-foundation-deep);
	}

	/* ==========================================
	 * AUDIENCE SEGMENTS
	 * ========================================== */

	.audiences {
		padding: var(--space-12) var(--space-6);
		max-width: var(--container-lg);
		margin: 0 auto;
		border-top: 1px solid var(--color-border-subtle);
	}

	.audiences__grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: var(--space-6);
	}

	.audience {
		display: block;
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
		text-decoration: none;
		color: inherit;
		cursor: pointer;
		transition: all var(--duration-normal) var(--ease-out);
	}

	.audience:hover {
		border-color: var(--color-accent-primary);
		background: var(--color-foundation-surface);
		box-shadow: var(--shadow-lg);
		transform: translateY(-2px);
	}

	.audience__icon {
		width: 48px;
		height: 48px;
		background: var(--color-accent-primary-glow);
		border-radius: var(--radius-lg);
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: var(--space-4);
	}

	.audience__icon svg {
		width: 24px;
		height: 24px;
		color: var(--color-accent-primary);
	}

	.audience__title {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.audience__description {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	/* ==========================================
	 * CITATION SECTION
	 * ========================================== */

	.citation {
		background: linear-gradient(
			135deg,
			var(--color-accent-secondary-glow),
			var(--color-accent-primary-glow)
		);
		border-top: 1px solid var(--color-border-subtle);
		padding: var(--space-16) var(--space-6);
	}

	.citation__content {
		max-width: var(--container-md);
		margin: 0 auto;
		text-align: center;
	}

	.citation__eyebrow {
		font-size: var(--text-xs);
		font-weight: var(--font-weight-semibold);
		color: var(--color-accent-secondary);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		margin-bottom: var(--space-3);
	}

	.citation__title {
		font-family: var(--font-display);
		font-size: var(--text-3xl);
		color: var(--color-text-primary);
		margin-bottom: var(--space-4);
	}

	.citation__description {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		max-width: 480px;
		margin: 0 auto var(--space-6);
		line-height: var(--leading-relaxed);
	}

	.citation__block {
		background: var(--color-foundation-surface);
		border: 1px solid var(--color-border-default);
		border-radius: var(--radius-lg);
		padding: var(--space-4) var(--space-5);
		margin-bottom: var(--space-8);
		text-align: left;
	}

	.citation__block code {
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		word-break: break-word;
	}

	.citation__actions {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: var(--space-4);
	}

	/* ==========================================
	 * BUTTONS
	 * ========================================== */

	.btn {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		gap: var(--space-2);
		padding: var(--space-3) var(--space-6);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		border-radius: var(--radius-lg);
		text-decoration: none;
		transition: all var(--duration-fast) var(--ease-out);
		cursor: pointer;
		border: none;
	}

	.btn svg {
		width: 18px;
		height: 18px;
		transition: transform var(--duration-fast) var(--ease-spring);
	}

	.btn:hover svg {
		transform: translateX(3px);
	}

	.btn--primary {
		background: var(--color-accent-primary);
		color: white;
	}

	.btn--primary:hover {
		background: var(--color-accent-primary-hover);
		box-shadow: var(--shadow-glow-accent);
	}

	.btn--secondary {
		background: var(--color-accent-secondary);
		color: var(--color-foundation-deepest);
	}

	.btn--secondary:hover {
		filter: brightness(1.1);
	}

	.btn--ghost {
		background: transparent;
		color: var(--color-text-secondary);
		border: 1px solid var(--color-border-default);
	}

	.btn--ghost:hover {
		background: var(--color-foundation-surface);
		color: var(--color-text-primary);
		border-color: var(--color-border-strong);
	}

	.btn--outline {
		background: transparent;
		color: var(--color-score-very-high);
		border: 1px solid var(--color-score-very-high);
	}

	.btn--outline:hover {
		background: var(--color-score-very-high);
		color: white;
	}

	/* ==========================================
	 * ANIMATIONS
	 * ========================================== */

	@keyframes fadeUp {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}

	/* ==========================================
	 * RESPONSIVE
	 * ========================================== */

	@media (max-width: 640px) {
		.hero {
			padding: var(--space-10) var(--space-4) var(--space-8);
		}

		.hero__title {
			font-size: var(--text-3xl);
		}

		.hero__subtitle {
			font-size: var(--text-base);
		}

		.featured {
			padding: var(--space-10) var(--space-4);
		}

		.featured__title,
		.citation__title {
			font-size: var(--text-2xl);
		}

		.tracts {
			grid-template-columns: 1fr;
		}

		.citation {
			padding: var(--space-12) var(--space-4);
		}
	}

	/* Reduced motion */
	@media (prefers-reduced-motion: reduce) {
		.hero__eyebrow,
		.hero__title,
		.hero__subtitle,
		.hero__actions,
		.hero__stats,
		.tract {
			opacity: 1;
			transform: none;
			animation: none;
		}
	}
</style>
