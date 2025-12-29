import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { sql } from '$lib/server/db';
import { logger } from '$lib/server/logger';
import {
	CensusGeocoderResponseSchema,
	PercentileDbSchema,
	type ScoreCategory
} from '$lib/server/schemas';
import type { GeocoderResponse, GeocoderResult } from '$lib/components/map/types';
import { dev } from '$app/environment';

/**
 * Rate limiting configuration.
 */
const RATE_LIMIT = {
	maxRequests: 10,
	windowMs: 60_000, // 1 minute
	maxMapSize: 50_000 // Maximum IPs to track
};

/**
 * Input validation limits.
 */
const INPUT_LIMITS = {
	minAddressLength: 3,
	maxAddressLength: 200,
	fetchTimeoutMs: 10_000 // 10 seconds
};

// In-memory rate limit storage (IP -> timestamps)
const rateLimitMap = new Map<string, number[]>();

/**
 * Get client IP from request, preferring Fly.io headers.
 */
function getSecureClientIp(request: Request, getClientAddress: () => string): string {
	if (dev) {
		return getClientAddress();
	}

	// Fly.io sets this header
	const flyClientIp = request.headers.get('fly-client-ip');
	if (flyClientIp) {
		return flyClientIp;
	}

	// Fallback to x-real-ip (set by some proxies)
	const realIp = request.headers.get('x-real-ip');
	if (realIp) {
		return realIp;
	}

	return getClientAddress();
}

/**
 * Check if request is rate limited.
 */
function isRateLimited(ip: string): { limited: boolean; remaining: number; resetMs: number } {
	const now = Date.now();
	const windowStart = now - RATE_LIMIT.windowMs;

	// Get existing timestamps for this IP
	const timestamps = rateLimitMap.get(ip) || [];

	// Filter to only recent requests
	const recentRequests = timestamps.filter((t) => t > windowStart);

	// Enforce max map size (LRU eviction)
	if (rateLimitMap.size >= RATE_LIMIT.maxMapSize && !rateLimitMap.has(ip)) {
		// Evict oldest 10% of entries
		const keysToDelete = Array.from(rateLimitMap.keys()).slice(
			0,
			Math.floor(RATE_LIMIT.maxMapSize * 0.1)
		);
		for (const key of keysToDelete) {
			rateLimitMap.delete(key);
		}
	}

	// Check if over limit
	if (recentRequests.length >= RATE_LIMIT.maxRequests) {
		const oldestRequest = Math.min(...recentRequests);
		const resetMs = oldestRequest + RATE_LIMIT.windowMs - now;
		return {
			limited: true,
			remaining: 0,
			resetMs: Math.max(0, resetMs)
		};
	}

	// Add this request
	recentRequests.push(now);
	rateLimitMap.set(ip, recentRequests);

	return {
		limited: false,
		remaining: RATE_LIMIT.maxRequests - recentRequests.length,
		resetMs: RATE_LIMIT.windowMs
	};
}

/**
 * Clean up old rate limit entries periodically.
 */
function cleanupRateLimits(): void {
	const now = Date.now();
	const windowStart = now - RATE_LIMIT.windowMs;
	const ipsToDelete: string[] = [];

	// First pass: identify what to delete/update
	for (const [ip, timestamps] of rateLimitMap.entries()) {
		const recent = timestamps.filter((t) => t > windowStart);
		if (recent.length === 0) {
			ipsToDelete.push(ip);
		} else if (recent.length !== timestamps.length) {
			rateLimitMap.set(ip, recent);
		}
	}

	// Second pass: delete
	for (const ip of ipsToDelete) {
		rateLimitMap.delete(ip);
	}
}

// Cleanup every 5 minutes
setInterval(cleanupRateLimits, 5 * 60_000);

// CensusGeocoderResponse type is now imported from schemas

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
 * Get tract data from database with proper validation and logging.
 * Uses optimized query that leverages the new indexes.
 */
async function getTractData(
	tractFips: string,
	correlationId: string
): Promise<{ resilienceScore: number | null; percentile: number | null }> {
	try {
		// Optimized query: avoids full table scan for PERCENT_RANK
		// Uses the new idx_tracts_resilience_asc index
		const result = await sql`
			SELECT
				t.resilience_score,
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
			return { resilienceScore: null, percentile: null };
		}

		// Validate database result with Zod
		const parsed = PercentileDbSchema.safeParse(result[0]);
		if (!parsed.success) {
			logger.warn('Invalid tract data from database', {
				correlationId,
				tractFips,
				errors: parsed.error.issues
			});
			return { resilienceScore: null, percentile: null };
		}

		return {
			resilienceScore: parsed.data.resilience_score,
			percentile: parsed.data.percentile !== null ? Math.round(parsed.data.percentile) : null
		};
	} catch (err) {
		logger.error('Database error fetching tract data', {
			correlationId,
			tractFips,
			error: err instanceof Error ? err.message : 'Unknown error'
		});
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
 * Validate and sanitize address input.
 */
function validateAddress(address: string | null): { valid: boolean; sanitized: string; error?: string } {
	if (!address) {
		return { valid: false, sanitized: '', error: 'Address is required' };
	}

	const trimmed = address.trim();

	if (trimmed.length < INPUT_LIMITS.minAddressLength) {
		return { valid: false, sanitized: '', error: 'Address must be at least 3 characters' };
	}

	if (trimmed.length > INPUT_LIMITS.maxAddressLength) {
		return { valid: false, sanitized: '', error: 'Address too long (max 200 characters)' };
	}

	// Remove potential injection characters
	const sanitized = trimmed.replace(/[\r\n\t]/g, ' ');

	// Check for suspicious patterns
	if (sanitized.includes('://') || sanitized.includes('@')) {
		return { valid: false, sanitized: '', error: 'Invalid address format' };
	}

	return { valid: true, sanitized };
}

/**
 * Fetch with timeout using AbortController.
 */
async function fetchWithTimeout(url: string, timeoutMs: number): Promise<Response> {
	const controller = new AbortController();
	const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

	try {
		const response = await fetch(url, {
			signal: controller.signal,
			headers: {
				Accept: 'application/json'
			}
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
 * GET /api/geocode?address={query}
 *
 * Geocodes an address using the Census Geocoder API and enriches
 * the result with resilience data from our database.
 */
export const GET: RequestHandler = async ({ url, request, getClientAddress }) => {
	// Create correlation ID for request tracing
	const log = logger.withCorrelationId();
	const correlationId = log.correlationId;

	// Validate address parameter
	const addressValidation = validateAddress(url.searchParams.get('address'));

	if (!addressValidation.valid) {
		log.info('Invalid address input', { error: addressValidation.error });
		return json(
			{
				success: false,
				results: [],
				error: addressValidation.error
			} satisfies GeocoderResponse,
			{ status: 400 }
		);
	}

	const address = addressValidation.sanitized;

	// Rate limiting with secure IP detection
	const clientIp = getSecureClientIp(request, getClientAddress);
	const rateLimit = isRateLimited(clientIp);

	if (rateLimit.limited) {
		log.info('Rate limit exceeded', { clientIp, resetMs: rateLimit.resetMs });

		const response = json(
			{
				success: false,
				results: [],
				error: 'Rate limit exceeded. Please wait before trying again.'
			} satisfies GeocoderResponse,
			{ status: 429 }
		);

		// Add rate limit headers
		response.headers.set('X-RateLimit-Limit', String(RATE_LIMIT.maxRequests));
		response.headers.set('X-RateLimit-Remaining', '0');
		response.headers.set('X-RateLimit-Reset', String(Math.ceil(rateLimit.resetMs / 1000)));
		response.headers.set('Retry-After', String(Math.ceil(rateLimit.resetMs / 1000)));
		response.headers.set('X-Correlation-ID', correlationId);

		return response;
	}

	try {
		// Build Census Geocoder URL
		const geocoderUrl = new URL(
			'https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress'
		);
		geocoderUrl.searchParams.set('address', address);
		geocoderUrl.searchParams.set('benchmark', 'Public_AR_Current');
		geocoderUrl.searchParams.set('vintage', 'Current_Current');
		geocoderUrl.searchParams.set('layers', 'Census Tracts');
		geocoderUrl.searchParams.set('format', 'json');

		// Fetch with timeout
		const response = await fetchWithTimeout(
			geocoderUrl.toString(),
			INPUT_LIMITS.fetchTimeoutMs
		);

		if (!response.ok) {
			throw error(502, 'Census Geocoder service unavailable');
		}

		// Validate response didn't redirect unexpectedly
		if (!response.url.startsWith('https://geocoding.geo.census.gov/')) {
			throw error(502, 'Unexpected redirect from geocoder service');
		}

		// Validate Census API response with Zod
		const rawData = await response.json();
		const parseResult = CensusGeocoderResponseSchema.safeParse(rawData);

		if (!parseResult.success) {
			log.error('Census API returned invalid response structure', {
				errors: parseResult.error.issues,
				address: address.slice(0, 50)
			});
			throw error(502, 'Census Geocoder returned invalid data');
		}

		const data = parseResult.data;

		// Process results
		const results: GeocoderResult[] = [];

		for (const match of data.result.addressMatches) {
			const tracts = match.geographies?.['Census Tracts'];
			const tract = tracts?.[0];

			if (!tract) continue;

			const tractFips = tract.GEOID.padStart(11, '0');
			const { resilienceScore, percentile } = await getTractData(tractFips, correlationId);

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

		log.info('Geocode request successful', {
			address: address.slice(0, 50),
			resultCount: results.length
		});

		const jsonResponse = json({
			success: true,
			results
		} satisfies GeocoderResponse);

		// Add rate limit and tracing headers
		jsonResponse.headers.set('X-RateLimit-Limit', String(RATE_LIMIT.maxRequests));
		jsonResponse.headers.set('X-RateLimit-Remaining', String(rateLimit.remaining));
		jsonResponse.headers.set('X-RateLimit-Reset', String(Math.ceil(rateLimit.resetMs / 1000)));
		jsonResponse.headers.set('X-Correlation-ID', correlationId);

		return jsonResponse;
	} catch (err) {
		// Log error details with correlation ID
		log.error('Geocoder request failed', {
			error: err instanceof Error ? err.message : 'Unknown error',
			address: address.slice(0, 50)
		});

		// Re-throw SvelteKit errors
		if (err && typeof err === 'object' && 'status' in err) {
			throw err;
		}

		const errorResponse = json(
			{
				success: false,
				results: [],
				error: 'Failed to geocode address. Please try again.'
			} satisfies GeocoderResponse,
			{ status: 500 }
		);

		errorResponse.headers.set('X-Correlation-ID', correlationId);
		return errorResponse;
	}
};
