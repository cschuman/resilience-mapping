/**
 * Integration Tests
 *
 * Tests validation schemas and error handling.
 * Note: Svelte 5 component tests require more complex setup with vitest.
 * These tests focus on the critical server-side logic.
 */

import { describe, it, expect } from 'vitest';

describe('Error Handling', () => {
	it('API validation schemas handle malformed data gracefully', async () => {
		// Import validation schemas
		const { safeParse, GeocoderResultSchema } = await import('$lib/server/schemas');

		// Test with malformed data
		const malformedData = {
			lat: 'not a number',
			lng: null,
			tractFips: 12345, // should be string
			matchedAddress: undefined
		};

		const result = safeParse(GeocoderResultSchema, malformedData);
		expect(result).toBeUndefined();
	});

	it('API validation schemas accept valid data', async () => {
		const { safeParse, GeocoderResultSchema } = await import('$lib/server/schemas');

		const validData = {
			lat: 40.7128,
			lng: -74.0060,
			tractFips: '36061000100',
			matchedAddress: '123 Main St, New York, NY 10001',
			state: 'NY',
			county: '061',
			resilienceScore: 1.5,
			percentile: 85,
			scoreCategory: 'high'
		};

		const result = safeParse(GeocoderResultSchema, validData);
		expect(result).toBeDefined();
		expect(result?.lat).toBe(40.7128);
		expect(result?.tractFips).toBe('36061000100');
	});
});
