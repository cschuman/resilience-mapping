import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { sql } from '$lib/server/db';
import { logger } from '$lib/server/logger';
import { PercentileDbSchema, type ScoreCategory } from '$lib/server/schemas';
import type { GeocoderResponse, GeocoderResult } from '$lib/components/map/types';
import { dev } from '$app/environment';
import { z } from 'zod';

/**
 * Input validation schema for coordinates.
 */
const CoordinatesSchema = z.object({
	lat: z.coerce.number().min(-90).max(90),
	lng: z.coerce.number().min(-180).max(180)
});

/**
 * Rate limiting configuration.
 */
const RATE_LIMIT = {
	maxRequests: 10,
	windowMs: 60_000,
	maxMapSize: 50_000
};

const INPUT_LIMITS = {
	fetchTimeoutMs: 10_000
};

// In-memory rate limit storage
const rateLimitMap = new Map<string, number[]>();

/**
 * Get client IP from request.
 */
function getSecureClientIp(request: Request, getClientAddress: () => string): string {
	if (dev) return getClientAddress();
	return request.headers.get('fly-client-ip') ||
		request.headers.get('x-real-ip') ||
		getClientAddress();
}

/**
 * Check if request is rate limited.
 */
function isRateLimited(ip: string): { limited: boolean; remaining: number; resetMs: number } {
	const now = Date.now();
	const windowStart = now - RATE_LIMIT.windowMs;
	const timestamps = rateLimitMap.get(ip) || [];
	const recentRequests = timestamps.filter((t) => t > windowStart);

	if (rateLimitMap.size >= RATE_LIMIT.maxMapSize && !rateLimitMap.has(ip)) {
		const keysToDelete = Array.from(rateLimitMap.keys()).slice(0, Math.floor(RATE_LIMIT.maxMapSize * 0.1));
		for (const key of keysToDelete) {
			rateLimitMap.delete(key);
		}
	}

	if (recentRequests.length >= RATE_LIMIT.maxRequests) {
		const oldestRequest = Math.min(...recentRequests);
		return {
			limited: true,
			remaining: 0,
			resetMs: Math.max(0, oldestRequest + RATE_LIMIT.windowMs - now)
		};
	}

	recentRequests.push(now);
	rateLimitMap.set(ip, recentRequests);

	return {
		limited: false,
		remaining: RATE_LIMIT.maxRequests - recentRequests.length,
		resetMs: RATE_LIMIT.windowMs
	};
}

/**
 * Derive score category from resilience score.
 */
function getScoreCategory(score: number | null): ScoreCategory {
	if (score === null || typeof score !== 'number' || isNaN(score)) return 'no-data';
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
	tractFips: string,
	correlationId: string
): Promise<{ resilienceScore: number | null; percentile: number | null; countyName: string | null }> {
	try {
		const result = await sql`
			SELECT
				t.resilience_score,
				t.county,
				(
					SELECT COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM tracts WHERE resilience_score IS NOT NULL), 0)
					FROM tracts
					WHERE resilience_score < t.resilience_score
				) as percentile
			FROM tracts t
			WHERE t.tract_fips = ${tractFips}
			LIMIT 1
		`;

		if (result.length === 0) {
			return { resilienceScore: null, percentile: null, countyName: null };
		}

		const parsed = PercentileDbSchema.safeParse(result[0]);
		if (!parsed.success) {
			logger.warn('Invalid tract data from database', { correlationId, tractFips });
			return { resilienceScore: null, percentile: null, countyName: null };
		}

		return {
			resilienceScore: parsed.data.resilience_score,
			percentile: parsed.data.percentile !== null ? Math.round(parsed.data.percentile) : null,
			countyName: (result[0] as { county?: string }).county || null
		};
	} catch (err) {
		logger.error('Database error fetching tract data', {
			correlationId,
			tractFips,
			error: err instanceof Error ? err.message : 'Unknown error'
		});
		return { resilienceScore: null, percentile: null, countyName: null };
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
 * Fetch with timeout.
 */
async function fetchWithTimeout(url: string, timeoutMs: number): Promise<Response> {
	const controller = new AbortController();
	const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

	try {
		const response = await fetch(url, {
			signal: controller.signal,
			headers: { Accept: 'application/json' }
		});
		clearTimeout(timeoutId);
		return response;
	} catch (err) {
		clearTimeout(timeoutId);
		if (err instanceof Error && err.name === 'AbortError') {
			throw error(504, 'External geocoder service timeout');
		}
		throw err;
	}
}

/**
 * GET /api/geocode/reverse?lat={lat}&lng={lng}
 *
 * Reverse geocodes coordinates to get tract information.
 */
export const GET: RequestHandler = async ({ url, request, getClientAddress }) => {
	const log = logger.withCorrelationId();
	const correlationId = log.correlationId;

	// Validate coordinates
	const latParam = url.searchParams.get('lat');
	const lngParam = url.searchParams.get('lng');

	const parseResult = CoordinatesSchema.safeParse({ lat: latParam, lng: lngParam });
	if (!parseResult.success) {
		log.info('Invalid coordinates', { errors: parseResult.error.issues });
		return json(
			{
				success: false,
				results: [],
				error: 'Invalid coordinates. Lat must be -90 to 90, lng must be -180 to 180.'
			} satisfies GeocoderResponse,
			{ status: 400 }
		);
	}

	const { lat, lng } = parseResult.data;

	// Rate limiting
	const clientIp = getSecureClientIp(request, getClientAddress);
	const rateLimit = isRateLimited(clientIp);

	if (rateLimit.limited) {
		log.info('Rate limit exceeded', { clientIp });
		const response = json(
			{
				success: false,
				results: [],
				error: 'Rate limit exceeded. Please wait before trying again.'
			} satisfies GeocoderResponse,
			{ status: 429 }
		);
		response.headers.set('X-RateLimit-Limit', String(RATE_LIMIT.maxRequests));
		response.headers.set('X-RateLimit-Remaining', '0');
		response.headers.set('Retry-After', String(Math.ceil(rateLimit.resetMs / 1000)));
		return response;
	}

	try {
		// Build Census Geocoder reverse geocoding URL
		const geocoderUrl = new URL(
			'https://geocoding.geo.census.gov/geocoder/geographies/coordinates'
		);
		geocoderUrl.searchParams.set('x', lng.toString());
		geocoderUrl.searchParams.set('y', lat.toString());
		geocoderUrl.searchParams.set('benchmark', 'Public_AR_Current');
		geocoderUrl.searchParams.set('vintage', 'Current_Current');
		geocoderUrl.searchParams.set('layers', 'Census Tracts');
		geocoderUrl.searchParams.set('format', 'json');

		const response = await fetchWithTimeout(
			geocoderUrl.toString(),
			INPUT_LIMITS.fetchTimeoutMs
		);

		if (!response.ok) {
			throw error(502, 'Census Geocoder service unavailable');
		}

		const data = await response.json();

		// Extract tract info from response
		const geographies = data?.result?.geographies;
		const tracts = geographies?.['Census Tracts'];
		const tract = tracts?.[0];

		if (!tract) {
			return json({
				success: true,
				results: [],
				error: 'No census tract found at this location'
			} satisfies GeocoderResponse);
		}

		const tractFips = tract.GEOID.padStart(11, '0');
		const { resilienceScore, percentile, countyName } = await getTractData(tractFips, correlationId);
		const stateAbbr = STATE_ABBR[tract.STATE] || tract.STATE;

		const result: GeocoderResult = {
			lat,
			lng,
			tractFips,
			matchedAddress: countyName
				? `${countyName}, ${stateAbbr}`
				: `Tract ${tract.TRACT}, ${stateAbbr}`,
			state: stateAbbr,
			county: countyName || tract.COUNTY,
			resilienceScore,
			percentile,
			scoreCategory: getScoreCategory(resilienceScore)
		};

		log.info('Reverse geocode successful', { lat, lng, tractFips });

		const jsonResponse = json({
			success: true,
			results: [result]
		} satisfies GeocoderResponse);

		jsonResponse.headers.set('X-RateLimit-Remaining', String(rateLimit.remaining));
		jsonResponse.headers.set('X-Correlation-ID', correlationId);

		return jsonResponse;
	} catch (err) {
		log.error('Reverse geocoder request failed', {
			error: err instanceof Error ? err.message : 'Unknown error',
			lat,
			lng
		});

		if (err && typeof err === 'object' && 'status' in err) {
			throw err;
		}

		return json(
			{
				success: false,
				results: [],
				error: 'Failed to reverse geocode location. Please try again.'
			} satisfies GeocoderResponse,
			{ status: 500 }
		);
	}
};
