/**
 * Zod schemas for runtime validation.
 *
 * These schemas ensure type safety at runtime for:
 * - Database query results
 * - External API responses
 * - User input
 */

import { z } from 'zod';

// ============================================================================
// Database Schemas
// ============================================================================

/**
 * Schema for a tract record from the database.
 */
export const TractDbSchema = z.object({
	id: z.number().optional(),
	tract_fips: z.string().length(11),
	state_abbr: z.string().length(2).nullable(),
	county: z.string().nullable(),
	total_pop: z.number().int().nullable(),
	resilience_score: z.union([z.string(), z.number()]).nullable().transform(val =>
		val === null ? null : typeof val === 'string' ? parseFloat(val) : val
	),
	burden: z.union([z.string(), z.number()]).nullable().transform(val =>
		val === null ? null : typeof val === 'string' ? parseFloat(val) : val
	),
	gq_college_pct: z.union([z.string(), z.number()]).nullable().transform(val =>
		val === null ? null : typeof val === 'string' ? parseFloat(val) : val
	),
	gq_military_pct: z.union([z.string(), z.number()]).nullable().transform(val =>
		val === null ? null : typeof val === 'string' ? parseFloat(val) : val
	),
	gq_correctional_pct: z.union([z.string(), z.number()]).nullable().transform(val =>
		val === null ? null : typeof val === 'string' ? parseFloat(val) : val
	),
	gq_nursing_pct: z.union([z.string(), z.number()]).nullable().transform(val =>
		val === null ? null : typeof val === 'string' ? parseFloat(val) : val
	)
});

export type TractDb = z.infer<typeof TractDbSchema>;

/**
 * Schema for stats aggregation result.
 */
export const StatsDbSchema = z.object({
	total_tracts: z.union([z.string(), z.number()]).transform(val =>
		typeof val === 'string' ? parseInt(val, 10) : val
	),
	avg_resilience: z.union([z.string(), z.number()]).nullable().transform(val =>
		val === null ? null : typeof val === 'string' ? parseFloat(val) : val
	),
	min_resilience: z.union([z.string(), z.number()]).nullable().transform(val =>
		val === null ? null : typeof val === 'string' ? parseFloat(val) : val
	),
	max_resilience: z.union([z.string(), z.number()]).nullable().transform(val =>
		val === null ? null : typeof val === 'string' ? parseFloat(val) : val
	),
	total_population: z.union([z.string(), z.number()]).nullable().transform(val =>
		val === null ? null : typeof val === 'string' ? parseInt(val, 10) : val
	)
});

export type StatsDb = z.infer<typeof StatsDbSchema>;

/**
 * Schema for percentile calculation result.
 */
export const PercentileDbSchema = z.object({
	resilience_score: z.union([z.string(), z.number()]).nullable().transform(val =>
		val === null ? null : typeof val === 'string' ? parseFloat(val) : val
	),
	percentile: z.union([z.string(), z.number()]).nullable().transform(val =>
		val === null ? null : typeof val === 'string' ? parseFloat(val) : val
	)
});

export type PercentileDb = z.infer<typeof PercentileDbSchema>;

/**
 * Schema for count result.
 */
export const CountDbSchema = z.object({
	count: z.union([z.string(), z.number()]).transform(val =>
		typeof val === 'string' ? parseInt(val, 10) : val
	)
});

export type CountDb = z.infer<typeof CountDbSchema>;

// ============================================================================
// Census API Schemas
// ============================================================================

/**
 * Schema for Census Geocoder tract geography.
 */
export const CensusTractSchema = z.object({
	GEOID: z.string(),
	STATE: z.string(),
	COUNTY: z.string(),
	TRACT: z.string(),
	NAME: z.string()
});

/**
 * Schema for Census Geocoder address match.
 */
export const CensusAddressMatchSchema = z.object({
	matchedAddress: z.string(),
	coordinates: z.object({
		x: z.number(),
		y: z.number()
	}),
	geographies: z.object({
		'Census Tracts': z.array(CensusTractSchema).optional()
	}).optional()
});

/**
 * Schema for Census Geocoder API response.
 */
export const CensusGeocoderResponseSchema = z.object({
	result: z.object({
		addressMatches: z.array(CensusAddressMatchSchema)
	})
});

export type CensusGeocoderResponse = z.infer<typeof CensusGeocoderResponseSchema>;

// ============================================================================
// API Response Schemas
// ============================================================================

/**
 * Score category enum.
 */
export const ScoreCategorySchema = z.enum([
	'very-high',
	'high',
	'medium',
	'low',
	'very-low',
	'no-data'
]);

export type ScoreCategory = z.infer<typeof ScoreCategorySchema>;

/**
 * Schema for geocoder result.
 */
export const GeocoderResultSchema = z.object({
	lat: z.number(),
	lng: z.number(),
	tractFips: z.string(),
	matchedAddress: z.string(),
	state: z.string(),
	county: z.string(),
	resilienceScore: z.number().nullable(),
	percentile: z.number().nullable(),
	scoreCategory: ScoreCategorySchema
});

export type GeocoderResult = z.infer<typeof GeocoderResultSchema>;

/**
 * Schema for geocoder API response.
 */
export const GeocoderResponseSchema = z.object({
	success: z.boolean(),
	results: z.array(GeocoderResultSchema),
	error: z.string().optional()
});

export type GeocoderResponse = z.infer<typeof GeocoderResponseSchema>;

// ============================================================================
// Input Validation Schemas
// ============================================================================

/**
 * Schema for address input validation.
 */
export const AddressInputSchema = z.string()
	.min(3, 'Address must be at least 3 characters')
	.max(200, 'Address too long (max 200 characters)')
	.transform(val => val.trim().replace(/[\r\n\t]/g, ' '))
	.refine(
		val => !val.includes('://') && !val.includes('@'),
		{ message: 'Invalid address format' }
	);

/**
 * Schema for state abbreviation.
 */
export const StateAbbrSchema = z.string()
	.length(2)
	.regex(/^[A-Z]{2}$/, 'Invalid state abbreviation')
	.optional();

/**
 * Schema for sort field validation.
 */
export const SortFieldSchema = z.enum([
	'resilience_score',
	'total_pop',
	'burden',
	'tract_fips',
	'state_abbr'
]).default('resilience_score');

/**
 * Schema for sort order validation.
 */
export const SortOrderSchema = z.enum(['ASC', 'DESC']).default('DESC');

/**
 * Schema for pagination parameters.
 */
export const PaginationSchema = z.object({
	limit: z.number().int().min(1).max(1000).default(100),
	offset: z.number().int().min(0).max(1000000).default(0)
});

// ============================================================================
// Map Feature Schemas
// ============================================================================

/**
 * Schema for tract properties from PMTiles/MapLibre.
 */
export const TractPropertiesSchema = z.object({
	GEOID: z.string(),
	STATEFP: z.string().optional(),
	COUNTYFP: z.string().optional(),
	TRACTCE: z.string().optional(),
	NAME: z.string().optional(),
	state_abbr: z.string().nullable().optional(),
	resilience_score: z.number().nullable().optional(),
	burden: z.number().nullable().optional(),
	score_category: ScoreCategorySchema.optional()
});

export type TractProperties = z.infer<typeof TractPropertiesSchema>;

// ============================================================================
// Validation Helpers
// ============================================================================

/**
 * Safely parse and validate data with a Zod schema.
 * Returns undefined on validation failure instead of throwing.
 */
export function safeParse<T>(schema: z.ZodSchema<T>, data: unknown): T | undefined {
	const result = schema.safeParse(data);
	return result.success ? result.data : undefined;
}

/**
 * Parse and validate data, throwing a descriptive error on failure.
 */
export function parseOrThrow<T>(schema: z.ZodSchema<T>, data: unknown, context: string): T {
	const result = schema.safeParse(data);
	if (!result.success) {
		const errorMessages = result.error.issues.map(e => `${e.path.join('.')}: ${e.message}`).join(', ');
		throw new Error(`Validation failed for ${context}: ${errorMessages}`);
	}
	return result.data;
}
