import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { sql } from '$lib/server/db';
import type { GeocoderResponse, GeocoderResult, ScoreCategory } from '$lib/components/map/types';

/**
 * Rate limiting configuration.
 * Uses in-memory storage - resets on server restart.
 */
const RATE_LIMIT = {
	maxRequests: 10,
	windowMs: 60_000 // 1 minute
};

// In-memory rate limit storage (IP -> timestamps)
const rateLimitMap = new Map<string, number[]>();

/**
 * Check if request is rate limited.
 */
function isRateLimited(ip: string): boolean {
	const now = Date.now();
	const windowStart = now - RATE_LIMIT.windowMs;

	// Get existing timestamps for this IP
	const timestamps = rateLimitMap.get(ip) || [];

	// Filter to only recent requests
	const recentRequests = timestamps.filter((t) => t > windowStart);

	// Update map
	rateLimitMap.set(ip, recentRequests);

	// Check if over limit
	if (recentRequests.length >= RATE_LIMIT.maxRequests) {
		return true;
	}

	// Add this request
	recentRequests.push(now);
	rateLimitMap.set(ip, recentRequests);

	return false;
}

/**
 * Clean up old rate limit entries periodically.
 */
function cleanupRateLimits(): void {
	const now = Date.now();
	const windowStart = now - RATE_LIMIT.windowMs;

	for (const [ip, timestamps] of rateLimitMap.entries()) {
		const recent = timestamps.filter((t) => t > windowStart);
		if (recent.length === 0) {
			rateLimitMap.delete(ip);
		} else {
			rateLimitMap.set(ip, recent);
		}
	}
}

// Cleanup every 5 minutes
setInterval(cleanupRateLimits, 5 * 60_000);

/**
 * Census Geocoder API response structure.
 */
interface CensusGeocoderResponse {
	result: {
		addressMatches: Array<{
			matchedAddress: string;
			coordinates: {
				x: number; // longitude
				y: number; // latitude
			};
			geographies: {
				'Census Tracts': Array<{
					GEOID: string;
					STATE: string;
					COUNTY: string;
					TRACT: string;
					NAME: string;
				}>;
			};
		}>;
	};
}

/**
 * Derive score category from resilience score.
 */
function getScoreCategory(score: number | null): ScoreCategory {
	if (score === null || isNaN(score)) return 'no-data';
	if (score >= 2.0) return 'very-high';
	if (score >= 1.0) return 'high';
	if (score >= 0.0) return 'medium';
	if (score >= -1.0) return 'low';
	return 'very-low';
}

/**
 * Get tract data from database.
 */
async function getTractData(
	tractFips: string
): Promise<{ resilienceScore: number | null; percentile: number | null }> {
	try {
		const result = await sql`
			WITH ranked AS (
				SELECT
					tract_fips,
					resilience_score,
					PERCENT_RANK() OVER (ORDER BY resilience_score) * 100 as percentile
				FROM tracts
				WHERE resilience_score IS NOT NULL
			)
			SELECT resilience_score, percentile
			FROM ranked
			WHERE tract_fips = ${tractFips}
			LIMIT 1
		`;

		if (result.length === 0) {
			return { resilienceScore: null, percentile: null };
		}

		return {
			resilienceScore: parseFloat(result[0].resilience_score),
			percentile: Math.round(parseFloat(result[0].percentile))
		};
	} catch {
		return { resilienceScore: null, percentile: null };
	}
}

/**
 * State FIPS to abbreviation mapping.
 */
const STATE_ABBR: Record<string, string> = {
	'01': 'AL', '02': 'AK', '04': 'AZ', '05': 'AR', '06': 'CA',
	'08': 'CO', '09': 'CT', '10': 'DE', '11': 'DC', '12': 'FL',
	'13': 'GA', '15': 'HI', '16': 'ID', '17': 'IL', '18': 'IN',
	'19': 'IA', '20': 'KS', '21': 'KY', '22': 'LA', '23': 'ME',
	'24': 'MD', '25': 'MA', '26': 'MI', '27': 'MN', '28': 'MS',
	'29': 'MO', '30': 'MT', '31': 'NE', '32': 'NV', '33': 'NH',
	'34': 'NJ', '35': 'NM', '36': 'NY', '37': 'NC', '38': 'ND',
	'39': 'OH', '40': 'OK', '41': 'OR', '42': 'PA', '44': 'RI',
	'45': 'SC', '46': 'SD', '47': 'TN', '48': 'TX', '49': 'UT',
	'50': 'VT', '51': 'VA', '53': 'WA', '54': 'WV', '55': 'WI',
	'56': 'WY', '72': 'PR'
};

/**
 * GET /api/geocode?address={query}
 *
 * Geocodes an address using the Census Geocoder API and enriches
 * the result with resilience data from our database.
 */
export const GET: RequestHandler = async ({ url, getClientAddress }) => {
	// Get and validate address parameter
	const address = url.searchParams.get('address');

	if (!address || address.trim().length < 3) {
		return json(
			{
				success: false,
				results: [],
				error: 'Address must be at least 3 characters'
			} satisfies GeocoderResponse,
			{ status: 400 }
		);
	}

	// Rate limiting
	const clientIp = getClientAddress();
	if (isRateLimited(clientIp)) {
		return json(
			{
				success: false,
				results: [],
				error: 'Rate limit exceeded. Please wait before trying again.'
			} satisfies GeocoderResponse,
			{ status: 429 }
		);
	}

	try {
		// Build Census Geocoder URL
		const geocoderUrl = new URL(
			'https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress'
		);
		geocoderUrl.searchParams.set('address', address.trim());
		geocoderUrl.searchParams.set('benchmark', 'Public_AR_Current');
		geocoderUrl.searchParams.set('vintage', 'Current_Current');
		geocoderUrl.searchParams.set('layers', 'Census Tracts');
		geocoderUrl.searchParams.set('format', 'json');

		// Fetch from Census Geocoder
		const response = await fetch(geocoderUrl.toString(), {
			headers: {
				Accept: 'application/json'
			}
		});

		if (!response.ok) {
			throw error(502, 'Census Geocoder service unavailable');
		}

		const data: CensusGeocoderResponse = await response.json();

		// Process results
		const results: GeocoderResult[] = [];

		for (const match of data.result.addressMatches) {
			const tract = match.geographies?.['Census Tracts']?.[0];

			if (!tract) continue;

			const tractFips = tract.GEOID.padStart(11, '0');
			const { resilienceScore, percentile } = await getTractData(tractFips);

			results.push({
				lat: match.coordinates.y,
				lng: match.coordinates.x,
				tractFips,
				matchedAddress: match.matchedAddress,
				state: STATE_ABBR[tract.STATE] || tract.STATE,
				county: tract.COUNTY,
				resilienceScore,
				percentile,
				scoreCategory: getScoreCategory(resilienceScore)
			});
		}

		return json({
			success: true,
			results
		} satisfies GeocoderResponse);
	} catch (err) {
		console.error('Geocoder error:', err);

		// Re-throw SvelteKit errors
		if (err && typeof err === 'object' && 'status' in err) {
			throw err;
		}

		return json(
			{
				success: false,
				results: [],
				error: 'Failed to geocode address. Please try again.'
			} satisfies GeocoderResponse,
			{ status: 500 }
		);
	}
};
