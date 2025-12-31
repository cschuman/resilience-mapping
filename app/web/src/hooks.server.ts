import type { Handle } from '@sveltejs/kit';
import { sql } from '$lib/server/db';
import { logger } from '$lib/server/logger';

/**
 * Simple in-memory rate limiter.
 * Uses a sliding window approach with cleanup.
 * For production, consider Redis-based rate limiting at the edge.
 */
class RateLimiter {
	private requests: Map<string, number[]> = new Map();
	private readonly windowMs: number;
	private readonly maxRequests: number;
	private lastCleanup: number = Date.now();
	private readonly cleanupInterval: number = 60000; // 1 minute

	constructor(windowMs: number = 60000, maxRequests: number = 100) {
		this.windowMs = windowMs;
		this.maxRequests = maxRequests;
	}

	isAllowed(ip: string): { allowed: boolean; remaining: number; resetMs: number } {
		const now = Date.now();

		// Periodic cleanup of old entries
		if (now - this.lastCleanup > this.cleanupInterval) {
			this.cleanup(now);
			this.lastCleanup = now;
		}

		// Get existing requests for this IP
		const requests = this.requests.get(ip) || [];

		// Filter to requests within the window
		const windowStart = now - this.windowMs;
		const validRequests = requests.filter((time) => time > windowStart);

		// Check if limit exceeded
		if (validRequests.length >= this.maxRequests) {
			const oldestRequest = Math.min(...validRequests);
			const resetMs = oldestRequest + this.windowMs - now;
			return {
				allowed: false,
				remaining: 0,
				resetMs: Math.max(0, resetMs)
			};
		}

		// Add current request
		validRequests.push(now);
		this.requests.set(ip, validRequests);

		return {
			allowed: true,
			remaining: this.maxRequests - validRequests.length,
			resetMs: this.windowMs
		};
	}

	private cleanup(now: number): void {
		const windowStart = now - this.windowMs;
		for (const [ip, requests] of this.requests.entries()) {
			const validRequests = requests.filter((time) => time > windowStart);
			if (validRequests.length === 0) {
				this.requests.delete(ip);
			} else {
				this.requests.set(ip, validRequests);
			}
		}
	}
}

// Rate limiter: 100 requests per minute per IP
const rateLimiter = new RateLimiter(60000, 100);

/**
 * Graceful shutdown handling.
 * Properly close database connections when receiving SIGTERM.
 */
let isShuttingDown = false;

if (typeof process !== 'undefined') {
	process.on('SIGTERM', async () => {
		logger.info('SIGTERM received, initiating graceful shutdown');
		isShuttingDown = true;

		try {
			// Close database connections
			await sql.end({ timeout: 5 });
			logger.info('Database connections closed');
		} catch (err) {
			logger.error('Error during shutdown', {
				error: err instanceof Error ? err.message : 'Unknown error'
			});
		}

		// Force exit after 10 seconds if still running
		setTimeout(() => {
			logger.warn('Forcing exit after timeout');
			process.exit(0);
		}, 10000);
	});

	process.on('SIGINT', async () => {
		logger.info('SIGINT received, initiating graceful shutdown');
		isShuttingDown = true;

		try {
			await sql.end({ timeout: 5 });
			logger.info('Database connections closed');
		} catch (err) {
			logger.error('Error during shutdown', {
				error: err instanceof Error ? err.message : 'Unknown error'
			});
		}

		process.exit(0);
	});
}

/**
 * Security headers for all responses.
 * Following OWASP recommendations.
 * Note: CSP is handled by SvelteKit in svelte.config.js with proper nonces.
 */
const securityHeaders: Record<string, string> = {
	// HSTS - Force HTTPS for 1 year, include subdomains
	'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',

	// Prevent MIME type sniffing
	'X-Content-Type-Options': 'nosniff',

	// Enable XSS protection in older browsers
	'X-XSS-Protection': '1; mode=block',

	// Prevent clickjacking
	'X-Frame-Options': 'SAMEORIGIN',

	// Referrer policy for privacy
	'Referrer-Policy': 'strict-origin-when-cross-origin',

	// Permissions policy - restrict powerful features
	'Permissions-Policy':
		'accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()'
};

/**
 * Cache headers for static assets.
 */
const staticCacheHeaders: Record<string, string> = {
	'Cache-Control': 'public, max-age=31536000, immutable'
};

/**
 * Cache headers for PMTiles.
 */
const tilesCacheHeaders: Record<string, string> = {
	'Cache-Control': 'public, max-age=86400, stale-while-revalidate=604800'
};

/**
 * Cache headers for API responses.
 * Short cache (5 min) with stale-while-revalidate for snappy UX.
 */
const apiCacheHeaders: Record<string, string> = {
	'Cache-Control': 'public, max-age=300, stale-while-revalidate=3600'
};

/**
 * Cache headers for stats API (uses materialized views, less volatile).
 * Longer cache (15 min) since data changes infrequently.
 */
const statsCacheHeaders: Record<string, string> = {
	'Cache-Control': 'public, max-age=900, stale-while-revalidate=3600'
};

/**
 * Main request handler hook.
 * Adds security headers to all responses.
 * Rejects requests during shutdown.
 */
export const handle: Handle = async ({ event, resolve }) => {
	const { pathname } = event.url;

	// Reject new requests during shutdown
	if (isShuttingDown) {
		return new Response('Service is shutting down', {
			status: 503,
			headers: {
				'Retry-After': '30',
				'Content-Type': 'text/plain'
			}
		});
	}

	// Rate limiting for API endpoints only
	if (pathname.startsWith('/api/')) {
		// Get client IP (Fly.io forwards real IP in Fly-Client-IP header)
		const ip =
			event.request.headers.get('Fly-Client-IP') ||
			event.request.headers.get('X-Forwarded-For')?.split(',')[0]?.trim() ||
			event.getClientAddress();

		const rateLimit = rateLimiter.isAllowed(ip);

		if (!rateLimit.allowed) {
			logger.warn('Rate limit exceeded', { ip, pathname });
			return new Response(
				JSON.stringify({
					error: 'Too Many Requests',
					message: 'Rate limit exceeded. Please wait before making more requests.',
					retryAfter: Math.ceil(rateLimit.resetMs / 1000)
				}),
				{
					status: 429,
					headers: {
						'Content-Type': 'application/json',
						'Retry-After': Math.ceil(rateLimit.resetMs / 1000).toString(),
						'X-RateLimit-Limit': '100',
						'X-RateLimit-Remaining': '0',
						'X-RateLimit-Reset': Math.ceil(rateLimit.resetMs / 1000).toString()
					}
				}
			);
		}
	}

	const response = await resolve(event);

	// Add security headers to all responses
	for (const [header, value] of Object.entries(securityHeaders)) {
		response.headers.set(header, value);
	}

	// Add cache headers based on content type
	if (pathname.startsWith('/tiles/')) {
		// PMTiles get aggressive caching
		for (const [header, value] of Object.entries(tilesCacheHeaders)) {
			response.headers.set(header, value);
		}
	} else if (pathname === '/api/stats') {
		// Stats API uses materialized views, cache longer
		for (const [header, value] of Object.entries(statsCacheHeaders)) {
			response.headers.set(header, value);
		}
	} else if (pathname.startsWith('/api/')) {
		// Other API endpoints get shorter cache
		for (const [header, value] of Object.entries(apiCacheHeaders)) {
			response.headers.set(header, value);
		}
	} else if (
		pathname.match(/\.(js|css|woff2?|ttf|otf|png|jpg|jpeg|gif|svg|ico|webp)$/)
	) {
		// Static assets get immutable caching
		for (const [header, value] of Object.entries(staticCacheHeaders)) {
			response.headers.set(header, value);
		}
	}

	return response;
};
