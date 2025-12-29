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
	<title>Community Resilience Mapping</title>
	<meta
		name="description"
		content="Discover which communities demonstrate better health outcomes than predicted. Explore 64,000+ census tracts with interactive maps and data."
	/>
</svelte:head>

<div class="home" class:home--mounted={mounted}>
	<!-- Hero Section -->
	<section class="hero">
		<div class="hero__content">
			<p class="hero__eyebrow">Open Research Dataset</p>
			<h1 class="hero__title">
				Community Health
				<em>Resilience</em>
				Atlas
			</h1>
			<p class="hero__subtitle">
				Tract-level analysis identifying US communities with better health outcomes
				than socioeconomic factors would predict. Free data for researchers.
			</p>

			<!-- Actions -->
			<div class="hero__actions">
				<a href="/api/tracts?format=csv" class="btn btn--primary" download>
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

	<!-- Citation & Data Access -->
	<section class="citation" aria-labelledby="citation-heading">
		<div class="citation__content">
			<p class="citation__eyebrow">For Researchers</p>
			<h2 id="citation-heading" class="citation__title">
				Use this data
			</h2>
			<p class="citation__description">
				This dataset is free for research, journalism, and policy analysis.
				Please cite when using.
			</p>
			<div class="citation__block">
				<code>Community Resilience Mapping (2024). Census tract-level health resilience scores. https://resilience-mapping.fly.dev</code>
			</div>
			<div class="citation__actions">
				<a href="/api/tracts?format=csv" class="btn btn--secondary" download>
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
						<path d="M10.75 2.75a.75.75 0 00-1.5 0v8.614L6.295 8.235a.75.75 0 10-1.09 1.03l4.25 4.5a.75.75 0 001.09 0l4.25-4.5a.75.75 0 00-1.09-1.03l-2.955 3.129V2.75z" />
						<path d="M3.5 12.75a.75.75 0 00-1.5 0v2.5A2.75 2.75 0 004.75 18h10.5A2.75 2.75 0 0018 15.25v-2.5a.75.75 0 00-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5z" />
					</svg>
					<span>Download CSV</span>
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
		line-height: var(--leading-tight);
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
