import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { sql } from '$lib/server/db';
import { logger } from '$lib/server/logger';

/**
 * Health check endpoint for Fly.io and monitoring.
 *
 * GET /health
 *
 * Returns:
 * - 200: Service is healthy, database connected
 * - 503: Service unhealthy (database unreachable, etc.)
 */
export const GET: RequestHandler = async () => {
	const startTime = Date.now();

	try {
		// Test database connectivity with a simple query
		const [result] = await sql`SELECT 1 as health_check, NOW() as timestamp`;

		const responseTime = Date.now() - startTime;

		const healthData = {
			status: 'healthy',
			version: '1.0.0',
			timestamp: new Date().toISOString(),
			checks: {
				database: {
					status: 'healthy',
					responseTimeMs: responseTime
				}
			},
			uptime: process.uptime()
		};

		logger.info('Health check passed', { responseTimeMs: responseTime });

		return json(healthData, {
			headers: {
				'Cache-Control': 'no-cache, no-store, must-revalidate'
			}
		});
	} catch (err) {
		const responseTime = Date.now() - startTime;

		const errorMessage = err instanceof Error ? err.message : 'Unknown error';

		logger.error('Health check failed', {
			error: errorMessage,
			responseTimeMs: responseTime
		});

		return json(
			{
				status: 'unhealthy',
				version: '1.0.0',
				timestamp: new Date().toISOString(),
				checks: {
					database: {
						status: 'unhealthy',
						error: errorMessage,
						responseTimeMs: responseTime
					}
				},
				uptime: process.uptime()
			},
			{ status: 503 }
		);
	}
};
