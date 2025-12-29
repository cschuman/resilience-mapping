import type { Handle } from '@sveltejs/kit';
import { sql } from '$lib/server/db';
import { logger } from '$lib/server/logger';

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
 * Main request handler hook.
 * Adds security headers to all responses.
 * Rejects requests during shutdown.
 */
export const handle: Handle = async ({ event, resolve }) => {
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

	const response = await resolve(event);

	// Add security headers to all responses
	for (const [header, value] of Object.entries(securityHeaders)) {
		response.headers.set(header, value);
	}

	// Add cache headers for static assets
	const { pathname } = event.url;

	if (pathname.startsWith('/tiles/')) {
		// PMTiles get aggressive caching
		for (const [header, value] of Object.entries(tilesCacheHeaders)) {
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
