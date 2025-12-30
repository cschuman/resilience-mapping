/**
 * Comprehensive tests for Zod schemas.
 * Tests validation of database results, API responses, and user input.
 */

import { describe, it, expect } from 'vitest';
import {
	TractDbSchema,
	StatsDbSchema,
	GeocoderResultSchema,
	AddressInputSchema,
	StateAbbrSchema,
	SortFieldSchema,
	PaginationSchema,
	ScoreCategorySchema,
	safeParse,
	parseOrThrow
} from '$lib/server/schemas';

describe('TractDbSchema', () => {
	it('validates a complete tract record', () => {
		const tract = {
			id: 1,
			tract_fips: '06001400100',
			state_abbr: 'CA',
			county: 'Alameda',
			total_pop: 5000,
			resilience_score: '1.5',
			burden: '-0.3',
			gq_college_pct: '0.05',
			gq_military_pct: '0.00',
			gq_correctional_pct: '0.00',
			gq_nursing_pct: '0.02'
		};

		const result = TractDbSchema.safeParse(tract);
		expect(result.success).toBe(true);
		if (result.success) {
			expect(result.data.resilience_score).toBe(1.5);
			expect(result.data.burden).toBe(-0.3);
		}
	});

	it('handles null values correctly', () => {
		const tract = {
			tract_fips: '06001400100',
			state_abbr: null,
			county: null,
			total_pop: null,
			resilience_score: null,
			burden: null,
			gq_college_pct: null,
			gq_military_pct: null,
			gq_correctional_pct: null,
			gq_nursing_pct: null
		};

		const result = TractDbSchema.safeParse(tract);
		expect(result.success).toBe(true);
		if (result.success) {
			expect(result.data.resilience_score).toBeNull();
		}
	});

	it('rejects invalid tract_fips length', () => {
		const tract = {
			tract_fips: '123', // Too short
			state_abbr: 'CA',
			county: 'Test',
			total_pop: 100,
			resilience_score: 0,
			burden: 0,
			gq_college_pct: 0,
			gq_military_pct: 0,
			gq_correctional_pct: 0,
			gq_nursing_pct: 0
		};

		const result = TractDbSchema.safeParse(tract);
		expect(result.success).toBe(false);
	});

	it('transforms string numbers to floats', () => {
		const tract = {
			tract_fips: '06001400100',
			state_abbr: 'CA',
			county: 'Test',
			total_pop: 100,
			resilience_score: '2.75',
			burden: '-1.25',
			gq_college_pct: '0.15',
			gq_military_pct: '0',
			gq_correctional_pct: '0',
			gq_nursing_pct: '0'
		};

		const result = TractDbSchema.safeParse(tract);
		expect(result.success).toBe(true);
		if (result.success) {
			expect(typeof result.data.resilience_score).toBe('number');
			expect(result.data.resilience_score).toBe(2.75);
		}
	});
});

describe('StatsDbSchema', () => {
	it('validates stats aggregation result', () => {
		const stats = {
			total_tracts: '68170',
			avg_resilience: '0.123',
			min_resilience: '-4.5',
			max_resilience: '4.75',
			total_population: '330000000'
		};

		const result = StatsDbSchema.safeParse(stats);
		expect(result.success).toBe(true);
		if (result.success) {
			expect(result.data.total_tracts).toBe(68170);
			expect(typeof result.data.avg_resilience).toBe('number');
		}
	});

	it('handles numeric values directly', () => {
		const stats = {
			total_tracts: 1000,
			avg_resilience: 0.5,
			min_resilience: -2,
			max_resilience: 3,
			total_population: 5000000
		};

		const result = StatsDbSchema.safeParse(stats);
		expect(result.success).toBe(true);
	});
});

describe('GeocoderResultSchema', () => {
	it('validates a complete geocoder result', () => {
		const result = {
			lat: 40.7128,
			lng: -74.006,
			tractFips: '36061000100',
			matchedAddress: '123 Main St, New York, NY 10001',
			state: 'NY',
			county: '061',
			resilienceScore: 1.5,
			percentile: 85,
			scoreCategory: 'high'
		};

		const parsed = GeocoderResultSchema.safeParse(result);
		expect(parsed.success).toBe(true);
	});

	it('accepts null scores', () => {
		const result = {
			lat: 40.7128,
			lng: -74.006,
			tractFips: '36061000100',
			matchedAddress: '123 Main St, New York, NY 10001',
			state: 'NY',
			county: '061',
			resilienceScore: null,
			percentile: null,
			scoreCategory: 'no-data'
		};

		const parsed = GeocoderResultSchema.safeParse(result);
		expect(parsed.success).toBe(true);
	});

	it('rejects invalid score category', () => {
		const result = {
			lat: 40.7128,
			lng: -74.006,
			tractFips: '36061000100',
			matchedAddress: '123 Main St',
			state: 'NY',
			county: '061',
			resilienceScore: 1,
			percentile: 50,
			scoreCategory: 'invalid-category'
		};

		const parsed = GeocoderResultSchema.safeParse(result);
		expect(parsed.success).toBe(false);
	});
});

describe('AddressInputSchema', () => {
	it('accepts valid addresses', () => {
		const result = AddressInputSchema.safeParse('123 Main Street, City, ST 12345');
		expect(result.success).toBe(true);
	});

	it('rejects too short addresses', () => {
		const result = AddressInputSchema.safeParse('ab');
		expect(result.success).toBe(false);
	});

	it('rejects too long addresses', () => {
		const result = AddressInputSchema.safeParse('a'.repeat(201));
		expect(result.success).toBe(false);
	});

	it('sanitizes whitespace', () => {
		const result = AddressInputSchema.safeParse('  123 Main St  ');
		expect(result.success).toBe(true);
		if (result.success) {
			expect(result.data).toBe('123 Main St');
		}
	});

	it('rejects URLs', () => {
		const result = AddressInputSchema.safeParse('https://evil.com/address');
		expect(result.success).toBe(false);
	});

	it('rejects email addresses', () => {
		const result = AddressInputSchema.safeParse('user@domain.com');
		expect(result.success).toBe(false);
	});
});

describe('StateAbbrSchema', () => {
	it('accepts valid state abbreviation', () => {
		const result = StateAbbrSchema.safeParse('CA');
		expect(result.success).toBe(true);
	});

	it('rejects lowercase', () => {
		const result = StateAbbrSchema.safeParse('ca');
		expect(result.success).toBe(false);
	});

	it('rejects invalid length', () => {
		const result = StateAbbrSchema.safeParse('CAL');
		expect(result.success).toBe(false);
	});

	it('accepts undefined (optional)', () => {
		const result = StateAbbrSchema.safeParse(undefined);
		expect(result.success).toBe(true);
	});
});

describe('SortFieldSchema', () => {
	it('accepts valid sort fields', () => {
		const fields = ['resilience_score', 'total_pop', 'burden', 'tract_fips', 'state_abbr'];
		for (const field of fields) {
			const result = SortFieldSchema.safeParse(field);
			expect(result.success).toBe(true);
		}
	});

	it('rejects invalid sort field', () => {
		const result = SortFieldSchema.safeParse('DROP TABLE tracts');
		expect(result.success).toBe(false);
	});

	it('defaults to resilience_score', () => {
		const result = SortFieldSchema.safeParse(undefined);
		expect(result.success).toBe(true);
		if (result.success) {
			expect(result.data).toBe('resilience_score');
		}
	});
});

describe('PaginationSchema', () => {
	it('accepts valid pagination', () => {
		const result = PaginationSchema.safeParse({ limit: 50, offset: 100 });
		expect(result.success).toBe(true);
	});

	it('rejects limit over 1000', () => {
		const result = PaginationSchema.safeParse({ limit: 5000, offset: 0 });
		expect(result.success).toBe(false);
	});

	it('rejects negative offset', () => {
		const result = PaginationSchema.safeParse({ limit: 100, offset: -10 });
		expect(result.success).toBe(false);
	});

	it('applies defaults', () => {
		const result = PaginationSchema.safeParse({});
		expect(result.success).toBe(true);
		if (result.success) {
			expect(result.data.limit).toBe(100);
			expect(result.data.offset).toBe(0);
		}
	});
});

describe('ScoreCategorySchema', () => {
	const validCategories = ['very-high', 'high', 'medium', 'low', 'very-low', 'no-data'];

	it('accepts all valid categories', () => {
		for (const category of validCategories) {
			const result = ScoreCategorySchema.safeParse(category);
			expect(result.success).toBe(true);
		}
	});

	it('rejects invalid category', () => {
		const result = ScoreCategorySchema.safeParse('super-high');
		expect(result.success).toBe(false);
	});
});

describe('safeParse helper', () => {
	it('returns data on success', () => {
		const result = safeParse(ScoreCategorySchema, 'high');
		expect(result).toBe('high');
	});

	it('returns undefined on failure', () => {
		const result = safeParse(ScoreCategorySchema, 'invalid');
		expect(result).toBeUndefined();
	});
});

describe('parseOrThrow helper', () => {
	it('returns data on success', () => {
		const result = parseOrThrow(ScoreCategorySchema, 'high', 'test');
		expect(result).toBe('high');
	});

	it('throws on failure with context', () => {
		expect(() => {
			parseOrThrow(ScoreCategorySchema, 'invalid', 'score category');
		}).toThrow('Validation failed for score category');
	});
});
