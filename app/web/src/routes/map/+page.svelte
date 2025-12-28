<script lang="ts">
	import { Map, Legend } from '$lib/components/map';
	import type { MapApi, TractProperties, GeocoderResult } from '$lib/components/map';
	import { AddressSearch } from '$lib/components/search';

	// State for map API and legend visibility
	let mapApi: MapApi | undefined = $state();
	let showLegend = $state(true);
	let selectedTract: TractProperties | null = $state(null);
	let hoveredTract: TractProperties | null = $state(null);

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
			mapApi.flyTo(result.lng, result.lat, 12);
			// Small delay to let the map fly, then select the tract
			setTimeout(() => {
				mapApi?.selectTract(result.tractFips);
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
	 * Navigate back to home.
	 */
	function goHome(): void {
		window.location.href = '/';
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
	<main class="map-container">
		<Map
			bind:api={mapApi}
			onTractClick={handleTractClick}
			onTractHover={handleTractHover}
		/>
		<Legend visible={showLegend} onClose={() => (showLegend = false)} />

		<!-- Hover info tooltip -->
		{#if hoveredTract && !selectedTract}
			<div class="hover-info" role="status" aria-live="polite">
				<span class="hover-fips">{hoveredTract.GEOID}</span>
				{#if hoveredTract.resilience_score !== null}
					<span class="hover-score">
						{hoveredTract.resilience_score >= 0 ? '+' : ''}{hoveredTract.resilience_score.toFixed(2)}
					</span>
				{/if}
			</div>
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
			padding: 0.5rem;
		}

		.title {
			font-size: 0.875rem;
		}

		.header-center {
			display: none;
		}
	}
</style>
