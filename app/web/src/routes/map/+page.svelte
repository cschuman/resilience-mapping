<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
	import type { MapApi, TractProperties, GeocoderResult } from '$lib/components/map';
	import type { Component } from 'svelte';
	import { AddressSearch } from '$lib/components/search';

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

	// Cleanup on destroy
	onDestroy(() => {
		// Clear any pending timeout to prevent memory leaks
		if (selectTractTimeout) {
			clearTimeout(selectTractTimeout);
			selectTractTimeout = null;
		}
	});

	/**
	 * Handle tract click - update selected tract info.
	 */
	function handleTractClick(properties: TractProperties): void {
		selectedTract = properties;
	}

	/**
	 * Handle tract hover - update hovered tract info.
	 */
	function handleTractHover(properties: TractProperties | null): void {
		hoveredTract = properties;
	}

	/**
	 * Handle search result selection - fly to location and select tract.
	 */
	function handleSearchSelect(result: GeocoderResult): void {
		if (mapApi) {
			// Clear any previous timeout
			if (selectTractTimeout) {
				clearTimeout(selectTractTimeout);
			}

			mapApi.flyTo(result.lng, result.lat, 12);
			// Small delay to let the map fly, then select the tract
			selectTractTimeout = setTimeout(() => {
				mapApi?.selectTract(result.tractFips);
				selectTractTimeout = null;
			}, 1600);
		}
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
	<!-- Header -->
	<header class="header">
		<div class="header-left">
			<button type="button" class="back-button" onclick={goHome} aria-label="Go to home page">
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
			</button>
			<h1 class="title">Community Resilience Map</h1>
		</div>

		<div class="header-center">
			<AddressSearch
				placeholder="Search by address..."
				onSelect={handleSearchSelect}
			/>
		</div>

		<div class="header-right">
			<button
				type="button"
				class="icon-button"
				onclick={toggleLegend}
				aria-label={showLegend ? 'Hide legend' : 'Show legend'}
				aria-pressed={showLegend}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
					class="w-5 h-5"
					aria-hidden="true"
				>
					<path
						fill-rule="evenodd"
						d="M6 4.75A.75.75 0 016.75 4h10.5a.75.75 0 010 1.5H6.75A.75.75 0 016 4.75zM6 10a.75.75 0 01.75-.75h10.5a.75.75 0 010 1.5H6.75A.75.75 0 016 10zm0 5.25a.75.75 0 01.75-.75h10.5a.75.75 0 010 1.5H6.75a.75.75 0 01-.75-.75zM1.99 4.75a1 1 0 011-1H3a1 1 0 011 1v.01a1 1 0 01-1 1h-.01a1 1 0 01-1-1v-.01zM1.99 15.25a1 1 0 011-1H3a1 1 0 011 1v.01a1 1 0 01-1 1h-.01a1 1 0 01-1-1v-.01zM1.99 10a1 1 0 011-1H3a1 1 0 011 1v.01a1 1 0 01-1 1h-.01a1 1 0 01-1-1V10z"
						clip-rule="evenodd"
					/>
				</svg>
			</button>
			<a href="/about" class="nav-link">About</a>
		</div>
	</header>

	<!-- Map Container -->
	<main id="main-content" class="map-container">
		{#if isLoading}
			<div class="loading-overlay">
				<div class="loading-spinner"></div>
				<span>Loading map...</span>
			</div>
		{:else if loadError}
			<div class="error-overlay">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					fill="currentColor"
					class="error-icon"
					aria-hidden="true"
				>
					<path
						fill-rule="evenodd"
						d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003zM12 8.25a.75.75 0 01.75.75v3.75a.75.75 0 01-1.5 0V9a.75.75 0 01.75-.75zm0 8.25a.75.75 0 100-1.5.75.75 0 000 1.5z"
						clip-rule="evenodd"
					/>
				</svg>
				<span>{loadError}</span>
				<button type="button" onclick={() => window.location.reload()}>Retry</button>
			</div>
		{:else if MapComponent && LegendComponent}
			<MapComponent
				bind:api={mapApi}
				onTractClick={handleTractClick}
				onTractHover={handleTractHover}
			/>
			<LegendComponent visible={showLegend} onClose={() => (showLegend = false)} />

			<!-- Hover info tooltip -->
			{#if hoveredTract && !selectedTract}
				<div class="hover-info" role="status" aria-live="polite">
					<span class="hover-fips">{hoveredTract.GEOID}</span>
					{#if hoveredTract.resilience_score != null}
						<span class="hover-score">
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
		height: 100vh;
		width: 100vw;
		overflow: hidden;
		background: #0f172a;
	}

	.header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0.75rem 1rem;
		background: #1e293b;
		border-bottom: 1px solid #334155;
		flex-shrink: 0;
		gap: 1rem;
	}

	.header-left {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.header-center {
		flex: 1;
		max-width: 400px;
	}

	.header-right {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.back-button {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 36px;
		height: 36px;
		border: none;
		background: #334155;
		color: #e2e8f0;
		border-radius: 8px;
		cursor: pointer;
		transition: all 0.15s ease;
	}

	.back-button:hover {
		background: #475569;
	}

	.back-button:focus-visible {
		outline: 2px solid #10b981;
		outline-offset: 2px;
	}

	.title {
		font-size: 1.125rem;
		font-weight: 600;
		color: white;
		margin: 0;
		white-space: nowrap;
	}

	.icon-button {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 36px;
		height: 36px;
		border: none;
		background: transparent;
		color: #94a3b8;
		border-radius: 8px;
		cursor: pointer;
		transition: all 0.15s ease;
	}

	.icon-button:hover {
		background: #334155;
		color: white;
	}

	.icon-button:focus-visible {
		outline: 2px solid #10b981;
		outline-offset: 2px;
	}

	.icon-button[aria-pressed='true'] {
		background: #334155;
		color: #10b981;
	}

	.nav-link {
		font-size: 0.875rem;
		font-weight: 500;
		color: #94a3b8;
		text-decoration: none;
		padding: 0.5rem 0.75rem;
		border-radius: 6px;
		transition: all 0.15s ease;
	}

	.nav-link:hover {
		color: white;
		background: #334155;
	}

	.nav-link:focus-visible {
		outline: 2px solid #10b981;
		outline-offset: 2px;
	}

	.map-container {
		flex: 1;
		position: relative;
		overflow: hidden;
	}

	.loading-overlay,
	.error-overlay {
		position: absolute;
		inset: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: rgba(15, 23, 42, 0.95);
		color: white;
		gap: 1rem;
		z-index: 20;
	}

	.loading-spinner {
		width: 48px;
		height: 48px;
		border: 3px solid rgba(255, 255, 255, 0.2);
		border-top-color: #10b981;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	.error-overlay {
		color: #f87171;
	}

	.error-icon {
		width: 48px;
		height: 48px;
	}

	.error-overlay button {
		margin-top: 0.5rem;
		padding: 0.5rem 1rem;
		background: #334155;
		border: none;
		border-radius: 6px;
		color: white;
		cursor: pointer;
		transition: background 0.15s ease;
	}

	.error-overlay button:hover {
		background: #475569;
	}

	.hover-info {
		position: absolute;
		top: 1rem;
		left: 50%;
		transform: translateX(-50%);
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.5rem 1rem;
		background: rgba(15, 23, 42, 0.9);
		backdrop-filter: blur(8px);
		border-radius: 8px;
		color: white;
		font-size: 0.875rem;
		pointer-events: none;
		z-index: 10;
	}

	.hover-fips {
		font-family: ui-monospace, monospace;
		color: #e2e8f0;
	}

	.hover-score {
		font-weight: 600;
		color: #10b981;
	}

	/* Responsive adjustments */
	@media (max-width: 640px) {
		.header {
			flex-wrap: wrap;
			padding: 0.5rem 0.75rem;
			gap: 0.5rem;
		}

		.header-left {
			flex: 1;
			min-width: 0;
		}

		.title {
			font-size: 0.875rem;
			overflow: hidden;
			text-overflow: ellipsis;
		}

		.header-center {
			order: 3;
			width: 100%;
			max-width: 100%;
			flex: none;
		}

		.header-right {
			gap: 0.5rem;
		}

		/* Increase touch targets to 44px minimum for accessibility */
		.back-button,
		.icon-button {
			width: 44px;
			height: 44px;
		}

		.nav-link {
			padding: 0.625rem 0.875rem;
			min-height: 44px;
			display: flex;
			align-items: center;
		}
	}

	/* Tablet adjustments */
	@media (min-width: 641px) and (max-width: 768px) {
		.header-center {
			max-width: 280px;
		}
	}
</style>
