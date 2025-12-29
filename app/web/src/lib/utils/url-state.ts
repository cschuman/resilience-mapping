import { goto } from '$app/navigation';

/**
 * Update URL search parameters without a full page reload.
 * Uses SvelteKit's goto with replaceState to update the URL.
 */
export function updateUrlParams(params: Record<string, string | null | undefined>): void {
	if (typeof window === 'undefined') return;

	const url = new URL(window.location.href);

	Object.entries(params).forEach(([key, value]) => {
		if (value === null || value === undefined) {
			url.searchParams.delete(key);
		} else {
			url.searchParams.set(key, value);
		}
	});

	goto(url.pathname + url.search, {
		replaceState: true,
		keepFocus: true,
		noScroll: true
	});
}

/**
 * Get a URL parameter from the current location.
 */
export function getUrlParam(key: string): string | null {
	if (typeof window === 'undefined') return null;
	return new URL(window.location.href).searchParams.get(key);
}

/**
 * Parse map-specific URL parameters.
 */
export interface MapUrlParams {
	tract?: string;
	lat?: number;
	lng?: number;
	zoom?: number;
}

export function parseMapParams(searchParams: URLSearchParams): MapUrlParams {
	const tract = searchParams.get('tract') || undefined;
	const latStr = searchParams.get('lat');
	const lngStr = searchParams.get('lng');
	const zoomStr = searchParams.get('zoom');

	return {
		tract,
		lat: latStr ? parseFloat(latStr) : undefined,
		lng: lngStr ? parseFloat(lngStr) : undefined,
		zoom: zoomStr ? parseFloat(zoomStr) : undefined
	};
}
