<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
	import type { MapApi, TractProperties } from '$lib/components/map';
	import type { Component } from 'svelte';
	import { updateUrlParams } from '$lib/utils';
	import type { PageData } from './$types';

	// Page data from +page.ts
	let { data }: { data: PageData } = $props();

	// Lazy-loaded components - using `any` props type for dynamic imports
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	let MapComponent: Component<any> | null = $state(null);
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	let LegendComponent: Component<any> | null = $state(null);
	let isLoading = $state(true);
	let loadError = $state<string | null>(null);

	// State for map API and legend visibility
	let mapApi: MapApi | undefined = $state();
	let showLegend = $state(true);
	let selectedTract: TractProperties | null = $state(null);
	let hoveredTract: TractProperties | null = $state(null);

	// Track timeouts for cleanup
	let selectTractTimeout: ReturnType<typeof setTimeout> | null = null;
	let initialParamsApplied = false;

	// Lazy load heavy map components on mount
	onMount(async () => {
		try {
			const [mapModule, legendModule] = await Promise.all([
				import('$lib/components/map/Map.svelte'),
				import('$lib/components/map/Legend.svelte')
			]);
			MapComponent = mapModule.default;
			LegendComponent = legendModule.default;
		} catch (err) {
			console.error('Failed to load map components:', err);
			loadError = 'Failed to load map. Please refresh the page.';
		} finally {
			isLoading = false;
		}
	});

	// Apply initial URL params when map API becomes available
	$effect(() => {
		if (mapApi && !initialParamsApplied) {
			initialParamsApplied = true;
			applyInitialParams();
		}
	});

	/**
	 * Apply initial URL parameters to the map.
	 */
	function applyInitialParams(): void {
		if (!mapApi) return;

		// If we have initial coordinates, fly there
		if (data.initialCenter && data.initialZoom) {
			mapApi.flyTo(data.initialCenter[0], data.initialCenter[1], data.initialZoom);
		} else if (data.initialCenter) {
			mapApi.flyTo(data.initialCenter[0], data.initialCenter[1], 10);
		}

		// If we have an initial tract, select it after a delay
		if (data.initialTract) {
			selectTractTimeout = setTimeout(() => {
				mapApi?.selectTract(data.initialTract!);
				selectTractTimeout = null;
			}, data.initialCenter ? 1600 : 500);
		}
	}

	// Cleanup on destroy
	onDestroy(() => {
		// Clear any pending timeout to prevent memory leaks
		if (selectTractTimeout) {
			clearTimeout(selectTractTimeout);
			selectTractTimeout = null;
		}
	});

	/**
	 * Handle tract click - update selected tract info and URL.
	 */
	function handleTractClick(properties: TractProperties): void {
		selectedTract = properties;
		// Update URL with selected tract
		updateUrlParams({ tract: properties.GEOID });
	}

	/**
	 * Handle tract hover - update hovered tract info.
	 */
	function handleTractHover(properties: TractProperties | null): void {
		hoveredTract = properties;
	}

	/**
	 * Toggle legend visibility.
	 */
	function toggleLegend(): void {
		showLegend = !showLegend;
	}

	/**
	 * Navigate back to home using SvelteKit navigation (no full page reload).
	 */
	function goHome(): void {
		goto('/');
	}
</script>

<svelte:head>
	<title>Interactive Map | Community Resilience Mapping</title>
	<meta
		name="description"
		content="Explore community resilience scores across 64,000+ census tracts in the United States."
	/>
</svelte:head>

<div class="map-page">
	<!-- Skip link to bypass the interactive map -->
	<a href="#map-controls" class="skip-map-link">
		Skip to map controls
	</a>

	<!-- Header -->
	<header class="header" id="map-controls">
		<div class="header__left">
			<button type="button" class="header__back" onclick={goHome} aria-label="Go to home page">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
					aria-hidden="true"
				>
					<path
						fill-rule="evenodd"
						d="M17 10a.75.75 0 01-.75.75H5.612l4.158 3.96a.75.75 0 11-1.04 1.08l-5.5-5.25a.75.75 0 010-1.08l5.5-5.25a.75.75 0 111.04 1.08L5.612 9.25H16.25A.75.75 0 0117 10z"
						clip-rule="evenodd"
					/>
				</svg>
			</button>
			<div class="header__brand">
				<span class="header__mark">R</span>
				<h1 class="header__title">Resilience Map</h1>
			</div>
		</div>

		<div class="header__right">
			<button
				type="button"
				class="header__action"
				onclick={toggleLegend}
				aria-label={showLegend ? 'Hide legend' : 'Show legend'}
				aria-pressed={showLegend}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
					aria-hidden="true"
				>
					<path
						fill-rule="evenodd"
						d="M6 4.75A.75.75 0 016.75 4h10.5a.75.75 0 010 1.5H6.75A.75.75 0 016 4.75zM6 10a.75.75 0 01.75-.75h10.5a.75.75 0 010 1.5H6.75A.75.75 0 016 10zm0 5.25a.75.75 0 01.75-.75h10.5a.75.75 0 010 1.5H6.75a.75.75 0 01-.75-.75zM1.99 4.75a1 1 0 011-1H3a1 1 0 011 1v.01a1 1 0 01-1 1h-.01a1 1 0 01-1-1v-.01zM1.99 15.25a1 1 0 011-1H3a1 1 0 011 1v.01a1 1 0 01-1 1h-.01a1 1 0 01-1-1v-.01zM1.99 10a1 1 0 011-1H3a1 1 0 011 1v.01a1 1 0 01-1 1h-.01a1 1 0 01-1-1V10z"
						clip-rule="evenodd"
					/>
				</svg>
			</button>
			<a href="/about" class="header__link">About</a>
		</div>
	</header>

	<!-- Map Container -->
	<main id="main-content" class="map-container">
		{#if isLoading}
			<div class="loading">
				<div class="loading__spinner"></div>
				<span class="loading__text">Loading map...</span>
			</div>
		{:else if loadError}
			<div class="error">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					fill="currentColor"
					class="error__icon"
					aria-hidden="true"
				>
					<path
						fill-rule="evenodd"
						d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003zM12 8.25a.75.75 0 01.75.75v3.75a.75.75 0 01-1.5 0V9a.75.75 0 01.75-.75zm0 8.25a.75.75 0 100-1.5.75.75 0 000 1.5z"
						clip-rule="evenodd"
					/>
				</svg>
				<span class="error__message">{loadError}</span>
				<button type="button" class="error__retry" onclick={() => window.location.reload()}>
					Retry
				</button>
			</div>
		{:else if MapComponent && LegendComponent}
			<MapComponent
				bind:api={mapApi}
				onTractClick={handleTractClick}
				onTractHover={handleTractHover}
			/>
			<!-- Skip link after map to reach legend -->
			<a href="#map-legend" class="skip-to-legend">Skip to legend</a>
			<div id="map-legend">
				<LegendComponent visible={showLegend} onClose={() => (showLegend = false)} />
			</div>

			<!-- Hover info tooltip -->
			{#if hoveredTract && !selectedTract}
				<div class="hover-info" role="status" aria-live="polite">
					<span class="hover-info__fips">{hoveredTract.GEOID}</span>
					{#if hoveredTract.resilience_score != null}
						<span class="hover-info__score">
							{hoveredTract.resilience_score >= 0 ? '+' : ''}{hoveredTract.resilience_score.toFixed(2)}
						</span>
					{/if}
				</div>
			{/if}
		{/if}
	</main>
</div>

<style>
	.map-page {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
		overflow: hidden;
		background: var(--color-foundation-deepest);
	}

	/* Header */
	.header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: var(--space-3) var(--space-4);
		background: var(--color-foundation-mid);
		border-bottom: 1px solid var(--color-border-subtle);
		flex-shrink: 0;
		gap: var(--space-4);
	}

	.header__left {
		display: flex;
		align-items: center;
		gap: var(--space-3);
	}

	.header__brand {
		display: flex;
		align-items: center;
		gap: var(--space-2);
	}

	.header__mark {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 28px;
		height: 28px;
		background: var(--color-accent-primary);
		border-radius: var(--radius-md);
		color: white;
		font-family: var(--font-display);
		font-size: var(--text-base);
		font-weight: var(--font-weight-medium);
	}

	.header__right {
		display: flex;
		align-items: center;
		gap: var(--space-3);
	}

	.header__back {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 36px;
		height: 36px;
		border: none;
		background: var(--color-foundation-surface);
		color: var(--color-text-secondary);
		border-radius: var(--radius-lg);
		cursor: pointer;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.header__back svg {
		width: 20px;
		height: 20px;
	}

	.header__back:hover {
		background: var(--color-foundation-elevated);
		color: var(--color-text-primary);
	}

	.header__back:focus-visible {
		outline: 2px solid var(--color-accent-primary);
		outline-offset: 2px;
	}

	.header__title {
		font-family: var(--font-display);
		font-size: var(--text-lg);
		font-weight: var(--font-weight-normal);
		color: var(--color-text-primary);
		margin: 0;
		white-space: nowrap;
	}

	.header__action {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 36px;
		height: 36px;
		border: none;
		background: transparent;
		color: var(--color-text-muted);
		border-radius: var(--radius-lg);
		cursor: pointer;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.header__action svg {
		width: 20px;
		height: 20px;
	}

	.header__action:hover {
		background: var(--color-foundation-surface);
		color: var(--color-text-primary);
	}

	.header__action:focus-visible {
		outline: 2px solid var(--color-accent-primary);
		outline-offset: 2px;
	}

	.header__action[aria-pressed='true'] {
		background: var(--color-foundation-surface);
		color: var(--color-accent-primary);
	}

	.header__link {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-text-muted);
		text-decoration: none;
		padding: var(--space-2) var(--space-3);
		border-radius: var(--radius-md);
		transition: all var(--duration-fast) var(--ease-out);
	}

	.header__link:hover {
		color: var(--color-text-primary);
		background: var(--color-foundation-surface);
	}

	.header__link:focus-visible {
		outline: 2px solid var(--color-accent-primary);
		outline-offset: 2px;
	}

	/* Map Container */
	.map-container {
		flex: 1;
		position: relative;
		overflow: hidden;
	}

	/* Loading State */
	.loading {
		position: absolute;
		inset: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: var(--color-foundation-deepest);
		color: var(--color-text-primary);
		gap: var(--space-4);
		z-index: var(--z-modal);
	}

	.loading__spinner {
		width: 48px;
		height: 48px;
		border: 3px solid var(--color-border-subtle);
		border-top-color: var(--color-accent-primary);
		border-radius: var(--radius-full);
		animation: spin 1s linear infinite;
	}

	.loading__text {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	/* Error State */
	.error {
		position: absolute;
		inset: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: var(--color-foundation-deepest);
		gap: var(--space-4);
		z-index: var(--z-modal);
	}

	.error__icon {
		width: 48px;
		height: 48px;
		color: var(--color-error);
	}

	.error__message {
		color: var(--color-error);
		font-size: var(--text-sm);
	}

	.error__retry {
		margin-top: var(--space-2);
		padding: var(--space-2) var(--space-4);
		background: var(--color-foundation-surface);
		border: 1px solid var(--color-border-default);
		border-radius: var(--radius-lg);
		color: var(--color-text-primary);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		cursor: pointer;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.error__retry:hover {
		background: var(--color-foundation-elevated);
		border-color: var(--color-border-strong);
	}

	/* Hover Info Tooltip */
	.hover-info {
		position: absolute;
		top: var(--space-4);
		left: 50%;
		transform: translateX(-50%);
		display: flex;
		align-items: center;
		gap: var(--space-3);
		padding: var(--space-2) var(--space-4);
		background: rgba(10, 14, 26, 0.92);
		backdrop-filter: blur(12px);
		-webkit-backdrop-filter: blur(12px);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-lg);
		color: var(--color-text-primary);
		font-size: var(--text-sm);
		pointer-events: none;
		z-index: var(--z-tooltip);
	}

	.hover-info__fips {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-secondary);
	}

	.hover-info__score {
		font-weight: var(--font-weight-semibold);
		color: var(--color-score-very-high);  /* Deep Teal for positive scores */
	}

	/* Skip Links */
	.skip-map-link,
	.skip-to-legend {
		position: absolute;
		left: -9999px;
		z-index: 9999;
		padding: 0.75rem 1.5rem;
		background: var(--color-accent-primary);
		color: white;
		font-weight: 600;
		font-size: var(--text-sm);
		text-decoration: none;
		border-radius: 0 0 var(--radius-lg) var(--radius-lg);
		transition: left 0.2s ease;
	}

	.skip-map-link:focus,
	.skip-to-legend:focus {
		left: 50%;
		transform: translateX(-50%);
		outline: 2px solid white;
		outline-offset: 2px;
	}

	.skip-to-legend {
		top: auto;
		bottom: 0;
		border-radius: var(--radius-lg) var(--radius-lg) 0 0;
	}

	.skip-to-legend:focus {
		bottom: 0;
	}

	/* Legend wrapper for focus target */
	#map-legend {
		display: contents;
	}

	#map-legend:target {
		scroll-margin-top: 1rem;
	}

	/* Responsive */
	@media (max-width: 640px) {
		.header {
			flex-wrap: wrap;
			padding: var(--space-2) var(--space-3);
			gap: var(--space-2);
		}

		.header__left {
			flex: 1;
			min-width: 0;
		}

		.header__brand {
			gap: var(--space-2);
		}

		.header__mark {
			width: 24px;
			height: 24px;
			font-size: var(--text-sm);
		}

		.header__title {
			font-size: var(--text-base);
			overflow: hidden;
			text-overflow: ellipsis;
		}

		.header__right {
			gap: var(--space-2);
		}

		/* Touch-friendly targets */
		.header__back,
		.header__action {
			width: 44px;
			height: 44px;
		}

		.header__link {
			padding: var(--space-3) var(--space-3);
			min-height: 44px;
			display: flex;
			align-items: center;
		}
	}

</style>
