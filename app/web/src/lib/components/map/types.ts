/**
 * Map Component Type Definitions
 *
 * Type-safe interfaces for map data, properties, and component APIs.
 */

/**
 * Score category for resilience classification.
 * Derived from z-score ranges in the statistical model.
 */
export type ScoreCategory = 'very-high' | 'high' | 'medium' | 'low' | 'very-low' | 'no-data';

/**
 * Properties attached to each tract feature in the vector tiles.
 * These are set during tile generation from CSV + GeoJSON merge.
 */
export interface TractProperties {
	/** 11-digit Census tract FIPS code (state + county + tract) */
	GEOID: string;
	/** State FIPS code (2 digits) */
	STATEFP: string;
	/** County FIPS code (3 digits) */
	COUNTYFP: string;
	/** Tract code (6 digits) */
	TRACTCE: string;
	/** Full tract name */
	NAME: string;
	/** Two-letter state abbreviation */
	state_abbr: string | null;
	/** Resilience score (z-score, typically -3 to +3) */
	resilience_score: number | null;
	/** Health burden index (0-1 scale) */
	burden: number | null;
	/** Categorical classification for styling */
	score_category: ScoreCategory;
}

/**
 * Result from the Census Geocoder API proxy.
 * Enriched with resilience data from our database.
 */
export interface GeocoderResult {
	/** Latitude of matched address */
	lat: number;
	/** Longitude of matched address */
	lng: number;
	/** 11-digit tract FIPS code */
	tractFips: string;
	/** Standardized address from Census */
	matchedAddress: string;
	/** State name */
	state: string;
	/** County name */
	county: string;
	/** Resilience score if available */
	resilienceScore: number | null;
	/** Percentile rank within dataset (0-100) */
	percentile: number | null;
	/** Score category for quick display */
	scoreCategory: ScoreCategory;
}

/**
 * Response shape from /api/geocode endpoint.
 */
export interface GeocoderResponse {
	success: boolean;
	results: GeocoderResult[];
	error?: string;
}

/**
 * Configuration options for the Map component.
 */
export interface MapOptions {
	/** Initial map center [lng, lat] */
	initialCenter?: [number, number];
	/** Initial zoom level (0-22) */
	initialZoom?: number;
	/** Whether to show navigation controls */
	showNavigation?: boolean;
	/** Whether to show fullscreen control */
	showFullscreen?: boolean;
	/** Whether to show the legend overlay */
	showLegend?: boolean;
}

/**
 * Feature state for interactive styling.
 * MapLibre uses feature state for hover/selection effects.
 */
export interface TractFeatureState {
	hover?: boolean;
	selected?: boolean;
}

/**
 * Map component public API exposed via bindable.
 * Allows parent components to control the map programmatically.
 */
export interface MapApi {
	/**
	 * Fly to a specific location with animation.
	 * @param lng - Longitude
	 * @param lat - Latitude
	 * @param zoom - Optional zoom level (default: 12)
	 */
	flyTo: (lng: number, lat: number, zoom?: number) => void;

	/**
	 * Select a tract by FIPS code.
	 * Highlights the tract and shows its popup.
	 * @param fips - 11-digit tract FIPS code
	 */
	selectTract: (fips: string) => void;

	/**
	 * Clear the current selection.
	 */
	clearSelection: () => void;

	/**
	 * Get the underlying MapLibre map instance.
	 * Use sparingly - prefer the typed API methods.
	 */
	getMap: () => maplibregl.Map | null;
}

/**
 * Color palette for score categories.
 * Matches Tailwind color values for consistency.
 */
export const SCORE_COLORS: Record<ScoreCategory, string> = {
	'very-high': '#059669', // emerald-600
	high: '#34d399', // emerald-400
	medium: '#fbbf24', // amber-400
	low: '#f97316', // orange-500
	'very-low': '#dc2626', // red-600
	'no-data': '#64748b' // slate-500
} as const;

/**
 * Labels for score categories in UI.
 */
export const SCORE_LABELS: Record<ScoreCategory, string> = {
	'very-high': 'Very High',
	high: 'High',
	medium: 'Medium',
	low: 'Low',
	'very-low': 'Very Low',
	'no-data': 'No Data'
} as const;

/**
 * Score range descriptions for legend.
 */
export const SCORE_RANGES: Record<ScoreCategory, string> = {
	'very-high': '\u2265 2.0',
	high: '1.0 to 2.0',
	medium: '0.0 to 1.0',
	low: '-1.0 to 0.0',
	'very-low': '< -1.0',
	'no-data': 'N/A'
} as const;

/**
 * Default map configuration.
 * Centers on continental US.
 */
export const DEFAULT_MAP_OPTIONS: Required<MapOptions> = {
	initialCenter: [-98.5795, 39.8283], // Geographic center of contiguous US
	initialZoom: 4,
	showNavigation: true,
	showFullscreen: true,
	showLegend: true
} as const;

/**
 * PMTiles source configuration.
 */
export const TILES_CONFIG = {
	/** URL path to PMTiles file (relative to static) */
	url: '/tiles/tracts.pmtiles',
	/** Layer name in the tileset */
	sourceLayer: 'tracts',
	/** Source ID for MapLibre */
	sourceId: 'tracts-source',
	/** Fill layer ID */
	fillLayerId: 'tracts-fill',
	/** Outline layer ID */
	outlineLayerId: 'tracts-outline',
	/** Highlight layer ID for hover/selection */
	highlightLayerId: 'tracts-highlight'
} as const;

/**
 * Basemap configuration.
 * Using CARTO light basemap for clean cartography.
 */
export const BASEMAP_STYLE =
	'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json';
