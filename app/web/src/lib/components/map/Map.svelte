<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import maplibregl from 'maplibre-gl';
	import { Protocol } from 'pmtiles';
	import type { MapApi, MapOptions, TractProperties, ScoreCategory } from './types';
	import {
		BASEMAP_STYLE,
		DEFAULT_MAP_OPTIONS,
		SCORE_COLORS,
		TILES_CONFIG
	} from './types';
	import 'maplibre-gl/dist/maplibre-gl.css';

	interface Props {
		/** Map configuration options */
		options?: MapOptions;
		/** Callback when a tract is clicked */
		onTractClick?: (properties: TractProperties) => void;
		/** Callback when a tract is hovered */
		onTractHover?: (properties: TractProperties | null) => void;
		/** Bindable API for external control */
		api?: MapApi;
		/** Callback when map encounters an error */
		onError?: (error: Error) => void;
	}

	let {
		options = {},
		onTractClick,
		onTractHover,
		api = $bindable(),
		onError
	}: Props = $props();

	// Merge options with defaults
	const config = $derived({ ...DEFAULT_MAP_OPTIONS, ...options });

	// Component state
	let mapContainer: HTMLDivElement;
	let map: maplibregl.Map | null = $state(null);
	let popup: maplibregl.Popup | null = $state(null);
	let hoveredTractId: string | null = $state(null);
	let selectedTractId: string | null = $state(null);
	let isLoaded = $state(false);
	let mapError: string | null = $state(null);

	// PMTiles protocol singleton - prevents multiple registrations
	let protocolRegistered = false;
	const protocol = new Protocol();

	// Keyboard navigation settings
	const KEYBOARD_PAN_STEP = 100; // pixels
	const KEYBOARD_ZOOM_STEP = 1;

	/**
	 * Escape HTML special characters to prevent XSS.
	 */
	function escapeHtml(str: string | null | undefined): string {
		if (!str) return '';
		return str
			.replace(/&/g, '&amp;')
			.replace(/</g, '&lt;')
			.replace(/>/g, '&gt;')
			.replace(/"/g, '&quot;')
			.replace(/'/g, '&#039;');
	}

	/**
	 * Format resilience score for display.
	 */
	function formatScore(score: number | null | undefined): string {
		if (score == null || isNaN(score)) return 'N/A';
		return score >= 0 ? `+${score.toFixed(2)}` : score.toFixed(2);
	}

	/**
	 * Get human-readable category label.
	 */
	function getCategoryLabel(category: ScoreCategory): string {
		const labels: Record<ScoreCategory, string> = {
			'very-high': 'Very High Resilience',
			high: 'High Resilience',
			medium: 'Moderate Resilience',
			low: 'Low Resilience',
			'very-low': 'Very Low Resilience',
			'no-data': 'No Data Available'
		};
		return labels[category] || 'Unknown';
	}

	/**
	 * Create popup HTML content for a tract.
	 * All dynamic values are HTML-escaped to prevent XSS.
	 */
	function createPopupContent(props: TractProperties): string {
		const score = formatScore(props.resilience_score);
		const burden = props.burden != null ? props.burden.toFixed(2) : 'N/A';
		const category = props.score_category || 'no-data';
		const color = SCORE_COLORS[category];

		// Escape all user-controllable strings
		const geoid = escapeHtml(props.GEOID);
		const state = escapeHtml(props.state_abbr || props.STATEFP);
		const county = escapeHtml(props.COUNTYFP);
		const categoryLabel = escapeHtml(getCategoryLabel(category));

		return `
			<div class="tract-popup">
				<div class="popup-header">
					<span class="popup-fips">${geoid}</span>
					<span class="popup-state">${state}</span>
				</div>
				<div class="popup-score" style="border-left: 4px solid ${color}">
					<div class="score-value">${score}</div>
					<div class="score-label">${categoryLabel}</div>
				</div>
				<div class="popup-details">
					<div class="detail-row">
						<span class="detail-label">Health Burden:</span>
						<span class="detail-value">${burden}</span>
					</div>
					<div class="detail-row">
						<span class="detail-label">County:</span>
						<span class="detail-value">${county}</span>
					</div>
				</div>
			</div>
		`;
	}

	/**
	 * Build the match expression for fill colors based on score_category.
	 */
	function buildColorExpression(): maplibregl.ExpressionSpecification {
		return [
			'match',
			['get', 'score_category'],
			'very-high', SCORE_COLORS['very-high'],
			'high', SCORE_COLORS.high,
			'medium', SCORE_COLORS.medium,
			'low', SCORE_COLORS.low,
			'very-low', SCORE_COLORS['very-low'],
			SCORE_COLORS['no-data'] // default
		];
	}

	/**
	 * Initialize the map and layers.
	 */
	function initializeMap(): void {
		if (!mapContainer) return;

		// Register PMTiles protocol (singleton pattern - only once globally)
		if (!protocolRegistered) {
			try {
				maplibregl.addProtocol('pmtiles', protocol.tile);
				protocolRegistered = true;
			} catch (err) {
				// Protocol might already be registered from a previous mount
				console.warn('PMTiles protocol already registered');
			}
		}

		// Create map instance
		map = new maplibregl.Map({
			container: mapContainer,
			style: BASEMAP_STYLE,
			center: config.initialCenter,
			zoom: config.initialZoom,
			maxZoom: 14,
			minZoom: 3
		});

		// Add navigation controls
		if (config.showNavigation) {
			map.addControl(new maplibregl.NavigationControl(), 'top-right');
		}

		// Add fullscreen control
		if (config.showFullscreen) {
			map.addControl(new maplibregl.FullscreenControl(), 'top-right');
		}

		// Add scale control
		map.addControl(
			new maplibregl.ScaleControl({ maxWidth: 100, unit: 'imperial' }),
			'bottom-right'
		);

		// Handle map errors (including PMTiles loading failures)
		map.on('error', handleMapError);

		// Wait for style to load before adding sources/layers
		map.on('load', handleMapLoad);
	}

	/**
	 * Handle map errors including tile loading failures.
	 */
	function handleMapError(e: maplibregl.ErrorEvent): void {
		const errorMessage = e.error?.message || 'Unknown map error';
		console.error('Map error:', errorMessage, e);

		// Check if it's a critical error that should be shown to user
		if (errorMessage.includes('Failed to fetch') ||
			errorMessage.includes('pmtiles') ||
			errorMessage.includes('source')) {
			mapError = 'Failed to load map data. Please refresh the page.';
			isLoaded = false;
			// Ensure we pass a proper Error object
			const err = e.error instanceof Error ? e.error : new Error(errorMessage);
			onError?.(err);
		}
	}

	/**
	 * Handle map load event - add sources and layers.
	 */
	function handleMapLoad(): void {
		if (!map) return;

		// Add PMTiles source
		map.addSource(TILES_CONFIG.sourceId, {
			type: 'vector',
			url: `pmtiles://${TILES_CONFIG.url}`
		});

		// Add fill layer for tract polygons
		map.addLayer({
			id: TILES_CONFIG.fillLayerId,
			type: 'fill',
			source: TILES_CONFIG.sourceId,
			'source-layer': TILES_CONFIG.sourceLayer,
			paint: {
				'fill-color': buildColorExpression(),
				'fill-opacity': [
					'case',
					['boolean', ['feature-state', 'hover'], false],
					0.85,
					['boolean', ['feature-state', 'selected'], false],
					0.9,
					0.7
				]
			}
		});

		// Add outline layer
		map.addLayer({
			id: TILES_CONFIG.outlineLayerId,
			type: 'line',
			source: TILES_CONFIG.sourceId,
			'source-layer': TILES_CONFIG.sourceLayer,
			paint: {
				'line-color': [
					'case',
					['boolean', ['feature-state', 'selected'], false],
					'#1e293b', // slate-800 for selected
					['boolean', ['feature-state', 'hover'], false],
					'#475569', // slate-600 for hover
					'#94a3b8' // slate-400 default
				],
				'line-width': [
					'case',
					['boolean', ['feature-state', 'selected'], false],
					2.5,
					['boolean', ['feature-state', 'hover'], false],
					1.5,
					0.5
				],
				'line-opacity': 0.8
			}
		});

		// Set up event handlers
		setupEventHandlers();

		isLoaded = true;
	}

	// Named event handler functions for proper cleanup
	function handleMouseEnter(): void {
		if (map) map.getCanvas().style.cursor = 'pointer';
	}

	function handleCursorReset(): void {
		if (map) map.getCanvas().style.cursor = '';
	}

	/**
	 * Set up mouse and touch event handlers.
	 */
	function setupEventHandlers(): void {
		if (!map) return;

		// Mouse move for hover effects
		map.on('mousemove', TILES_CONFIG.fillLayerId, handleMouseMove);
		map.on('mouseleave', TILES_CONFIG.fillLayerId, handleMouseLeave);

		// Click for selection
		map.on('click', TILES_CONFIG.fillLayerId, handleClick);

		// Cursor styling - using named functions for cleanup
		map.on('mouseenter', TILES_CONFIG.fillLayerId, handleMouseEnter);
		map.on('mouseleave', TILES_CONFIG.fillLayerId, handleCursorReset);
	}

	/**
	 * Remove all event handlers for cleanup.
	 */
	function removeEventHandlers(): void {
		if (!map) return;

		map.off('mousemove', TILES_CONFIG.fillLayerId, handleMouseMove);
		map.off('mouseleave', TILES_CONFIG.fillLayerId, handleMouseLeave);
		map.off('click', TILES_CONFIG.fillLayerId, handleClick);
		map.off('mouseenter', TILES_CONFIG.fillLayerId, handleMouseEnter);
		map.off('mouseleave', TILES_CONFIG.fillLayerId, handleCursorReset);
		map.off('error', handleMapError);
	}

	/**
	 * Handle mouse move for hover effects.
	 */
	function handleMouseMove(e: maplibregl.MapLayerMouseEvent): void {
		if (!map || !e.features || e.features.length === 0) return;

		const feature = e.features[0];
		const props = feature.properties as TractProperties;
		const featureId = props.GEOID;

		// Clear previous hover state
		if (hoveredTractId && hoveredTractId !== featureId) {
			map.setFeatureState(
				{ source: TILES_CONFIG.sourceId, sourceLayer: TILES_CONFIG.sourceLayer, id: hoveredTractId },
				{ hover: false }
			);
		}

		// Set new hover state
		if (featureId) {
			hoveredTractId = featureId;
			map.setFeatureState(
				{ source: TILES_CONFIG.sourceId, sourceLayer: TILES_CONFIG.sourceLayer, id: featureId },
				{ hover: true }
			);
		}

		// Notify parent
		onTractHover?.(props);
	}

	/**
	 * Handle mouse leave to clear hover state.
	 */
	function handleMouseLeave(): void {
		if (!map) return;

		if (hoveredTractId) {
			map.setFeatureState(
				{ source: TILES_CONFIG.sourceId, sourceLayer: TILES_CONFIG.sourceLayer, id: hoveredTractId },
				{ hover: false }
			);
			hoveredTractId = null;
		}

		onTractHover?.(null);
	}

	/**
	 * Handle click for tract selection.
	 */
	function handleClick(e: maplibregl.MapLayerMouseEvent): void {
		if (!map || !e.features || e.features.length === 0) return;

		const feature = e.features[0];
		const props = feature.properties as TractProperties;
		const featureId = props.GEOID;

		// Clear previous selection
		if (selectedTractId) {
			map.setFeatureState(
				{ source: TILES_CONFIG.sourceId, sourceLayer: TILES_CONFIG.sourceLayer, id: selectedTractId },
				{ selected: false }
			);
		}

		// Set new selection
		if (featureId) {
			selectedTractId = featureId;
			map.setFeatureState(
				{ source: TILES_CONFIG.sourceId, sourceLayer: TILES_CONFIG.sourceLayer, id: featureId },
				{ selected: true }
			);
		}

		// Show popup
		showPopup(e.lngLat, props);

		// Notify parent
		onTractClick?.(props);
	}

	// Store popup close handler reference for cleanup
	let popupCloseHandler: (() => void) | null = null;

	/**
	 * Show popup at location with tract details.
	 */
	function showPopup(lngLat: maplibregl.LngLat, props: TractProperties): void {
		if (!map) return;

		// Remove existing popup and its handler
		if (popup) {
			if (popupCloseHandler) {
				popup.off('close', popupCloseHandler);
				popupCloseHandler = null;
			}
			popup.remove();
		}

		// Capture current selected tract ID for the closure
		const currentSelectedId = selectedTractId;

		// Create new popup
		popup = new maplibregl.Popup({
			closeButton: true,
			closeOnClick: false,
			maxWidth: '300px',
			className: 'tract-popup-container'
		})
			.setLngLat(lngLat)
			.setHTML(createPopupContent(props))
			.addTo(map);

		// Handle popup close - use captured ID to avoid stale closure
		popupCloseHandler = () => {
			// Use the component's current selectedTractId, not the captured one
			if (selectedTractId && map) {
				map.setFeatureState(
					{ source: TILES_CONFIG.sourceId, sourceLayer: TILES_CONFIG.sourceLayer, id: selectedTractId },
					{ selected: false }
				);
				selectedTractId = null;
			}
			popupCloseHandler = null;
		};

		popup.on('close', popupCloseHandler);
	}

	/**
	 * Fly to a specific location.
	 */
	function flyTo(lng: number, lat: number, zoom: number = 12): void {
		if (!map) return;
		map.flyTo({
			center: [lng, lat],
			zoom,
			duration: 1500,
			essential: true
		});
	}

	/**
	 * Select a tract by FIPS code.
	 */
	function selectTract(fips: string): void {
		if (!map || !isLoaded) return;

		// Query features with matching GEOID
		const features = map.querySourceFeatures(TILES_CONFIG.sourceId, {
			sourceLayer: TILES_CONFIG.sourceLayer,
			filter: ['==', ['get', 'GEOID'], fips]
		});

		if (features.length > 0) {
			const feature = features[0];
			const props = feature.properties as TractProperties;

			// Clear previous selection
			if (selectedTractId) {
				map.setFeatureState(
					{ source: TILES_CONFIG.sourceId, sourceLayer: TILES_CONFIG.sourceLayer, id: selectedTractId },
					{ selected: false }
				);
			}

			// Set new selection
			selectedTractId = fips;
			map.setFeatureState(
				{ source: TILES_CONFIG.sourceId, sourceLayer: TILES_CONFIG.sourceLayer, id: fips },
				{ selected: true }
			);

			// Get center of geometry for popup
			if (feature.geometry.type === 'Polygon' || feature.geometry.type === 'MultiPolygon') {
				const bounds = new maplibregl.LngLatBounds();
				const coords =
					feature.geometry.type === 'Polygon'
						? [feature.geometry.coordinates]
						: feature.geometry.coordinates;

				for (const polygon of coords) {
					for (const ring of polygon) {
						for (const coord of ring as [number, number][]) {
							bounds.extend(coord);
						}
					}
				}

				const center = bounds.getCenter();
				showPopup(center, props);

				// Fly to the tract
				map.flyTo({
					center,
					zoom: Math.max(map.getZoom(), 10),
					duration: 1000
				});
			}
		}
	}

	/**
	 * Clear the current selection.
	 */
	function clearSelection(): void {
		if (!map) return;

		if (popup) {
			popup.remove();
			popup = null;
		}

		if (selectedTractId) {
			map.setFeatureState(
				{ source: TILES_CONFIG.sourceId, sourceLayer: TILES_CONFIG.sourceLayer, id: selectedTractId },
				{ selected: false }
			);
			selectedTractId = null;
		}
	}

	/**
	 * Get the underlying map instance.
	 */
	function getMap(): maplibregl.Map | null {
		return map;
	}

	/**
	 * Handle keyboard navigation for the map.
	 */
	function handleKeydown(e: KeyboardEvent): void {
		if (!map || !isLoaded) return;

		// Only handle when map container is focused
		if (document.activeElement !== mapContainer) return;

		switch (e.key) {
			case 'ArrowUp':
				e.preventDefault();
				map.panBy([0, -KEYBOARD_PAN_STEP], { duration: 100 });
				break;
			case 'ArrowDown':
				e.preventDefault();
				map.panBy([0, KEYBOARD_PAN_STEP], { duration: 100 });
				break;
			case 'ArrowLeft':
				e.preventDefault();
				map.panBy([-KEYBOARD_PAN_STEP, 0], { duration: 100 });
				break;
			case 'ArrowRight':
				e.preventDefault();
				map.panBy([KEYBOARD_PAN_STEP, 0], { duration: 100 });
				break;
			case '+':
			case '=':
				e.preventDefault();
				map.zoomIn({ duration: 200 });
				break;
			case '-':
			case '_':
				e.preventDefault();
				map.zoomOut({ duration: 200 });
				break;
			case 'Escape':
				// Clear selection on Escape
				if (selectedTractId) {
					e.preventDefault();
					clearSelection();
				}
				break;
		}
	}

	// Initialize map on mount and expose API
	onMount(() => {
		initializeMap();

		// Expose API immediately after initialization
		api = {
			flyTo,
			selectTract,
			clearSelection,
			getMap
		};
	});

	// Cleanup on destroy - proper event handler removal
	onDestroy(() => {
		// Remove popup close handler
		if (popup && popupCloseHandler) {
			popup.off('close', popupCloseHandler);
			popupCloseHandler = null;
		}

		// Remove popup
		if (popup) {
			popup.remove();
			popup = null;
		}

		// Remove all event handlers before destroying map
		removeEventHandlers();

		// Remove map
		if (map) {
			map.remove();
			map = null;
		}

		// Note: We intentionally don't remove the PMTiles protocol
		// as it's a singleton that may be used by other map instances
	});
</script>

<div
	class="map-container"
	bind:this={mapContainer}
	role="application"
	aria-label="Interactive resilience map showing census tracts across the United States"
	aria-describedby="map-instructions"
	tabindex="0"
	onkeydown={handleKeydown}
>
	<div id="map-instructions" class="sr-only">
		Interactive map. Use arrow keys to pan, plus and minus to zoom.
		Click on census tracts to view details. Press Escape to close popups.
		Use the search bar above to find specific addresses.
	</div>

	{#if mapError}
		<div class="error-overlay" role="alert">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 24 24"
				fill="currentColor"
				class="error-icon"
				aria-hidden="true"
			>
				<path
					fill-rule="evenodd"
					d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003zM12 8.25a.75.75 0 01.75.75v3.75a.75.75 0 01-1.5 0V9a.75.75 0 01.75-.75zm0 8.25a1 1 0 100-1.5.75.75 0 000 1.5z"
					clip-rule="evenodd"
				/>
			</svg>
			<span>{mapError}</span>
			<button type="button" onclick={() => window.location.reload()}>Retry</button>
		</div>
	{:else if !isLoaded}
		<div class="loading-overlay">
			<div class="loading-spinner"></div>
			<span>Loading map...</span>
		</div>
	{/if}
</div>

<style>
	.map-container {
		width: 100%;
		height: 100%;
		position: relative;
	}

	.map-container:focus {
		outline: 2px solid #10b981;
		outline-offset: -2px;
	}

	.map-container:focus:not(:focus-visible) {
		outline: none;
	}

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

	.loading-overlay,
	.error-overlay {
		position: absolute;
		inset: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: rgba(15, 23, 42, 0.9);
		color: white;
		gap: 1rem;
		z-index: 10;
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

	.loading-spinner {
		width: 40px;
		height: 40px;
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

	/* Popup styles - using :global because MapLibre injects the popup into the DOM */
	:global(.tract-popup-container) {
		font-family: inherit;
	}

	:global(.tract-popup-container .maplibregl-popup-content) {
		padding: 0;
		border-radius: 8px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		overflow: hidden;
	}

	:global(.tract-popup) {
		min-width: 200px;
	}

	:global(.popup-header) {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem 1rem;
		background: #1e293b;
		color: white;
	}

	:global(.popup-fips) {
		font-family: ui-monospace, monospace;
		font-size: 0.875rem;
		font-weight: 600;
	}

	:global(.popup-state) {
		font-size: 0.75rem;
		color: #94a3b8;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	:global(.popup-score) {
		padding: 0.75rem 1rem;
		background: #f8fafc;
	}

	:global(.score-value) {
		font-size: 1.5rem;
		font-weight: 700;
		color: #0f172a;
	}

	:global(.score-label) {
		font-size: 0.75rem;
		color: #64748b;
		margin-top: 0.25rem;
	}

	:global(.popup-details) {
		padding: 0.75rem 1rem;
		background: white;
		border-top: 1px solid #e2e8f0;
	}

	:global(.detail-row) {
		display: flex;
		justify-content: space-between;
		font-size: 0.875rem;
		padding: 0.25rem 0;
	}

	:global(.detail-label) {
		color: #64748b;
	}

	:global(.detail-value) {
		color: #0f172a;
		font-weight: 500;
	}

	:global(.maplibregl-popup-close-button) {
		font-size: 1.25rem;
		padding: 0.25rem 0.5rem;
		color: #94a3b8;
	}

	:global(.maplibregl-popup-close-button:hover) {
		color: white;
		background: transparent;
	}
</style>
