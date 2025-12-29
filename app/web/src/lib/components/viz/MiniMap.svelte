<script lang="ts">
	/**
	 * Mini Map Preview
	 *
	 * A small, non-interactive map preview showing real tract data.
	 * Links to the full interactive map.
	 */
	import { onMount, onDestroy } from 'svelte';
	import maplibregl from 'maplibre-gl';
	import { Protocol } from 'pmtiles';
	import { SCORE_COLORS, TILES_CONFIG } from '$lib/components/map/types';
	import 'maplibre-gl/dist/maplibre-gl.css';

	let mapContainer: HTMLDivElement;
	let map: maplibregl.Map | null = null;
	let isLoaded = $state(false);

	// PMTiles protocol
	let protocolRegistered = false;
	const protocol = new Protocol();

	// Dark basemap style for the mini preview
	const DARK_BASEMAP = 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';

	onMount(() => {
		if (!protocolRegistered) {
			maplibregl.addProtocol('pmtiles', protocol.tile);
			protocolRegistered = true;
		}

		map = new maplibregl.Map({
			container: mapContainer,
			style: DARK_BASEMAP,
			center: [-98.5795, 39.8283], // Center of US
			zoom: 3.2,
			interactive: false, // No panning/zooming
			attributionControl: false
		});

		map.on('load', () => {
			if (!map) return;

			// Add PMTiles source
			map.addSource(TILES_CONFIG.sourceId, {
				type: 'vector',
				url: `pmtiles://${TILES_CONFIG.url}`
			});

			// Add fill layer with score colors
			map.addLayer({
				id: TILES_CONFIG.fillLayerId,
				type: 'fill',
				source: TILES_CONFIG.sourceId,
				'source-layer': TILES_CONFIG.sourceLayer,
				paint: {
					'fill-color': [
						'match',
						['get', 'score_category'],
						'very-high', SCORE_COLORS['very-high'],
						'high', SCORE_COLORS['high'],
						'medium', SCORE_COLORS['medium'],
						'low', SCORE_COLORS['low'],
						'very-low', SCORE_COLORS['very-low'],
						SCORE_COLORS['no-data']
					],
					'fill-opacity': 0.7
				}
			});

			isLoaded = true;
		});
	});

	onDestroy(() => {
		if (map) {
			map.remove();
			map = null;
		}
	});
</script>

<a href="/map" class="minimap" aria-label="Explore interactive map">
	<div class="minimap__container" bind:this={mapContainer}>
		{#if !isLoaded}
			<div class="minimap__loading">
				<span class="minimap__spinner"></span>
			</div>
		{/if}
	</div>
	<div class="minimap__overlay">
		<span class="minimap__cta">
			<svg viewBox="0 0 20 20" fill="currentColor" class="minimap__icon">
				<path fill-rule="evenodd" d="M9.69 18.933l.003.001C9.89 19.02 10 19 10 19s.11.02.308-.066l.002-.001.006-.003.018-.008a5.741 5.741 0 00.281-.14c.186-.096.446-.24.757-.433.62-.384 1.445-.966 2.274-1.765C15.302 14.988 17 12.493 17 9A7 7 0 103 9c0 3.492 1.698 5.988 3.355 7.584a13.731 13.731 0 002.273 1.765 11.842 11.842 0 00.976.544l.062.029.018.008.006.003zM10 11.25a2.25 2.25 0 100-4.5 2.25 2.25 0 000 4.5z" clip-rule="evenodd" />
			</svg>
			Explore Interactive Map
		</span>
	</div>
</a>

<style>
	.minimap {
		display: block;
		position: relative;
		text-decoration: none;
		border-radius: var(--radius-xl);
		overflow: hidden;
		border: 1px solid var(--color-border-subtle);
		transition: all var(--duration-normal) var(--ease-out);
	}

	.minimap:hover {
		border-color: var(--color-accent-primary);
		box-shadow: var(--shadow-lg), 0 0 0 1px var(--color-accent-primary);
	}

	.minimap__container {
		width: 100%;
		aspect-ratio: 16 / 9;
		background: var(--color-foundation-deep);
	}

	/* Override MapLibre styles for clean look */
	.minimap__container :global(.maplibregl-canvas) {
		border-radius: var(--radius-xl);
	}

	.minimap__loading {
		position: absolute;
		inset: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		background: var(--color-foundation-deep);
	}

	.minimap__spinner {
		width: 24px;
		height: 24px;
		border: 2px solid var(--color-border-subtle);
		border-top-color: var(--color-accent-primary);
		border-radius: 50%;
		animation: spin 0.8s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	.minimap__overlay {
		position: absolute;
		bottom: var(--space-3);
		right: var(--space-3);
		z-index: 1;
	}

	.minimap__cta {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		padding: var(--space-2) var(--space-3);
		background: var(--color-foundation-deepest);
		border-radius: var(--radius-md);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-text-secondary);
		transition: all var(--duration-fast) var(--ease-out);
		backdrop-filter: blur(8px);
	}

	.minimap:hover .minimap__cta {
		background: var(--color-accent-primary);
		color: white;
	}

	.minimap__icon {
		width: 16px;
		height: 16px;
	}
</style>
