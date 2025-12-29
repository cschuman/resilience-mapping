import { describe, it, expect } from 'vitest';

/**
 * Tests for API validation utilities.
 * These functions are tested in isolation from the actual API endpoints.
 */

// Re-implement the validation functions for testing
// In production, these would be imported from a shared module

function parseFloatParam(
	value: string | null,
	defaultValue: number,
	min: number,
	max: number
): number {
	if (!value) return defaultValue;
	const parsed = parseFloat(value);
	if (isNaN(parsed) || !isFinite(parsed)) return defaultValue;
	return Math.max(min, Math.min(max, parsed));
}

function parseIntParam(
	value: string | null,
	defaultValue: number,
	min: number,
	max: number
): number {
	if (!value) return defaultValue;
	const parsed = parseInt(value, 10);
	if (isNaN(parsed)) return defaultValue;
	return Math.max(min, Math.min(max, parsed));
}

const ALLOWED_SORT_FIELDS = [
	'resilience_score',
	'total_pop',
	'burden',
	'tract_fips',
	'state_abbr'
] as const;

type SortField = (typeof ALLOWED_SORT_FIELDS)[number];

function validateSortField(field: string | null): SortField {
	if (!field) return 'resilience_score';
	return ALLOWED_SORT_FIELDS.includes(field as SortField)
		? (field as SortField)
		: 'resilience_score';
}

const STATE_PATTERN = /^[A-Z]{2}$/;

function validateState(state: string | null): string | null {
	if (!state) return null;
	const upper = state.toUpperCase();
	return STATE_PATTERN.test(upper) ? upper : null;
}

function validateAddress(
	address: string | null
): { valid: boolean; sanitized: string; error?: string } {
	if (!address) {
		return { valid: false, sanitized: '', error: 'Address is required' };
	}

	const trimmed = address.trim();

	if (trimmed.length < 3) {
		return { valid: false, sanitized: '', error: 'Address must be at least 3 characters' };
	}

	if (trimmed.length > 200) {
		return { valid: false, sanitized: '', error: 'Address too long (max 200 characters)' };
	}

	const sanitized = trimmed.replace(/[\r\n\t]/g, ' ');

	if (sanitized.includes('://') || sanitized.includes('@')) {
		return { valid: false, sanitized: '', error: 'Invalid address format' };
	}

	return { valid: true, sanitized };
}

function escapeHtml(str: string | null | undefined): string {
	if (!str) return '';
	return str
		.replace(/&/g, '&amp;')
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/"/g, '&quot;')
		.replace(/'/g, '&#039;');
}

describe('parseFloatParam', () => {
	it('returns default for null input', () => {
		expect(parseFloatParam(null, 5, 0, 10)).toBe(5);
	});

	it('parses valid float', () => {
		expect(parseFloatParam('3.14', 0, 0, 10)).toBe(3.14);
	});

	it('clamps to minimum', () => {
		expect(parseFloatParam('-5', 0, 0, 10)).toBe(0);
	});

	it('clamps to maximum', () => {
		expect(parseFloatParam('15', 0, 0, 10)).toBe(10);
	});

	it('returns default for NaN', () => {
		expect(parseFloatParam('abc', 5, 0, 10)).toBe(5);
	});

	it('returns default for Infinity', () => {
		expect(parseFloatParam('Infinity', 5, 0, 10)).toBe(5);
	});
});

describe('parseIntParam', () => {
	it('returns default for null input', () => {
		expect(parseIntParam(null, 100, 1, 1000)).toBe(100);
	});

	it('parses valid integer', () => {
		expect(parseIntParam('50', 100, 1, 1000)).toBe(50);
	});

	it('clamps to minimum', () => {
		expect(parseIntParam('0', 100, 1, 1000)).toBe(1);
	});

	it('clamps to maximum', () => {
		expect(parseIntParam('5000', 100, 1, 1000)).toBe(1000);
	});

	it('returns default for invalid string', () => {
		expect(parseIntParam('abc', 100, 1, 1000)).toBe(100);
	});
});

describe('validateSortField', () => {
	it('returns default for null', () => {
		expect(validateSortField(null)).toBe('resilience_score');
	});

	it('accepts valid sort field', () => {
		expect(validateSortField('total_pop')).toBe('total_pop');
	});

	it('rejects invalid sort field (SQL injection attempt)', () => {
		expect(validateSortField('resilience_score; DROP TABLE--')).toBe('resilience_score');
	});

	it('rejects unknown field', () => {
		expect(validateSortField('unknown_field')).toBe('resilience_score');
	});
});

describe('validateState', () => {
	it('returns null for null input', () => {
		expect(validateState(null)).toBeNull();
	});

	it('accepts valid uppercase state', () => {
		expect(validateState('CA')).toBe('CA');
	});

	it('converts lowercase to uppercase', () => {
		expect(validateState('ny')).toBe('NY');
	});

	it('rejects invalid state code', () => {
		expect(validateState('XYZ')).toBeNull();
	});

	it('rejects single character', () => {
		expect(validateState('A')).toBeNull();
	});

	it('rejects numeric input', () => {
		expect(validateState('12')).toBeNull();
	});
});

describe('validateAddress', () => {
	it('rejects null address', () => {
		const result = validateAddress(null);
		expect(result.valid).toBe(false);
		expect(result.error).toBe('Address is required');
	});

	it('rejects empty address', () => {
		const result = validateAddress('');
		expect(result.valid).toBe(false);
	});

	it('rejects too short address', () => {
		const result = validateAddress('ab');
		expect(result.valid).toBe(false);
		expect(result.error).toBe('Address must be at least 3 characters');
	});

	it('rejects too long address', () => {
		const result = validateAddress('a'.repeat(201));
		expect(result.valid).toBe(false);
		expect(result.error).toBe('Address too long (max 200 characters)');
	});

	it('accepts valid address', () => {
		const result = validateAddress('123 Main Street');
		expect(result.valid).toBe(true);
		expect(result.sanitized).toBe('123 Main Street');
	});

	it('sanitizes newlines and tabs', () => {
		const result = validateAddress('123\nMain\tStreet\r');
		expect(result.valid).toBe(true);
		// The \r at the end becomes a space after trim and replace
		expect(result.sanitized).toBe('123 Main Street');
	});

	it('rejects URL patterns', () => {
		const result = validateAddress('https://evil.com');
		expect(result.valid).toBe(false);
		expect(result.error).toBe('Invalid address format');
	});

	it('rejects email patterns', () => {
		const result = validateAddress('test@example.com');
		expect(result.valid).toBe(false);
		expect(result.error).toBe('Invalid address format');
	});
});

describe('escapeHtml', () => {
	it('returns empty string for null', () => {
		expect(escapeHtml(null)).toBe('');
	});

	it('returns empty string for undefined', () => {
		expect(escapeHtml(undefined)).toBe('');
	});

	it('escapes ampersand', () => {
		expect(escapeHtml('A & B')).toBe('A &amp; B');
	});

	it('escapes less than', () => {
		expect(escapeHtml('<script>')).toBe('&lt;script&gt;');
	});

	it('escapes quotes', () => {
		expect(escapeHtml('"quoted"')).toBe('&quot;quoted&quot;');
	});

	it('escapes single quotes', () => {
		expect(escapeHtml("it's")).toBe('it&#039;s');
	});

	it('handles XSS attempt', () => {
		const xss = '<script>alert("XSS")</script>';
		const escaped = escapeHtml(xss);
		expect(escaped).not.toContain('<');
		expect(escaped).not.toContain('>');
		expect(escaped).toBe('&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;');
	});
});
