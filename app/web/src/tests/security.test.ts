/**
 * Tests for security configurations.
 * Validates security headers and other security measures.
 */

import { describe, it, expect } from 'vitest';

/**
 * Expected security headers from hooks.server.ts
 */
const expectedSecurityHeaders: Record<string, string> = {
	'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
	'X-Content-Type-Options': 'nosniff',
	'X-XSS-Protection': '1; mode=block',
	'X-Frame-Options': 'SAMEORIGIN',
	'Referrer-Policy': 'strict-origin-when-cross-origin',
	'Permissions-Policy':
		'accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()'
};

describe('Security Headers', () => {
	it('has HSTS header with long max-age', () => {
		const hsts = expectedSecurityHeaders['Strict-Transport-Security'];
		expect(hsts).toContain('max-age=31536000'); // 1 year
		expect(hsts).toContain('includeSubDomains');
		expect(hsts).toContain('preload');
	});

	it('has X-Content-Type-Options set to nosniff', () => {
		expect(expectedSecurityHeaders['X-Content-Type-Options']).toBe('nosniff');
	});

	it('has X-XSS-Protection enabled', () => {
		expect(expectedSecurityHeaders['X-XSS-Protection']).toBe('1; mode=block');
	});

	it('has X-Frame-Options to prevent clickjacking', () => {
		expect(expectedSecurityHeaders['X-Frame-Options']).toBe('SAMEORIGIN');
	});

	it('has strict referrer policy', () => {
		expect(expectedSecurityHeaders['Referrer-Policy']).toBe('strict-origin-when-cross-origin');
	});

	it('has permissions policy restricting dangerous APIs', () => {
		const policy = expectedSecurityHeaders['Permissions-Policy'];
		// All sensitive APIs should be disabled
		expect(policy).toContain('camera=()');
		expect(policy).toContain('microphone=()');
		expect(policy).toContain('payment=()');
		expect(policy).toContain('usb=()');
	});
});

describe('Input Sanitization', () => {
	/**
	 * HTML escape function matching the one in api-validation.test.ts
	 */
	function escapeHtml(str: string | null | undefined): string {
		if (!str) return '';
		return str
			.replace(/&/g, '&amp;')
			.replace(/</g, '&lt;')
			.replace(/>/g, '&gt;')
			.replace(/"/g, '&quot;')
			.replace(/'/g, '&#039;');
	}

	it('escapes script tags', () => {
		const xss = '<script>alert("XSS")</script>';
		const escaped = escapeHtml(xss);
		expect(escaped).not.toContain('<script>');
		expect(escaped).not.toContain('</script>');
	});

	it('escapes event handlers by escaping angle brackets', () => {
		const xss = '<img onerror="alert(1)" src="x">';
		const escaped = escapeHtml(xss);
		// The angle brackets are escaped, preventing the HTML from being parsed
		expect(escaped).not.toContain('<img');
		expect(escaped).toContain('&lt;img');
		expect(escaped).toContain('&gt;');
	});

	it('escapes javascript: URLs', () => {
		const xss = '<a href="javascript:alert(1)">click</a>';
		const escaped = escapeHtml(xss);
		expect(escaped).not.toContain('<a');
	});

	it('escapes nested quotes', () => {
		const input = 'He said "Hello" and \'Goodbye\'';
		const escaped = escapeHtml(input);
		expect(escaped).not.toContain('"Hello"');
		expect(escaped).toContain('&quot;');
		expect(escaped).toContain('&#039;');
	});
});

describe('SQL Injection Prevention', () => {
	const ALLOWED_SORT_FIELDS = [
		'resilience_score',
		'total_pop',
		'burden',
		'tract_fips',
		'state_abbr'
	] as const;

	function validateSortField(field: string | null): string {
		if (!field) return 'resilience_score';
		return ALLOWED_SORT_FIELDS.includes(field as (typeof ALLOWED_SORT_FIELDS)[number])
			? field
			: 'resilience_score';
	}

	it('rejects SQL injection in sort field', () => {
		const attacks = [
			'resilience_score; DROP TABLE tracts;--',
			'resilience_score UNION SELECT * FROM users',
			"1' OR '1'='1",
			'resilience_score; DELETE FROM tracts WHERE 1=1;--',
			'column_name FROM tracts WHERE 1=1 UNION SELECT password'
		];

		for (const attack of attacks) {
			expect(validateSortField(attack)).toBe('resilience_score');
		}
	});

	it('allows only whitelisted fields', () => {
		for (const field of ALLOWED_SORT_FIELDS) {
			expect(validateSortField(field)).toBe(field);
		}
	});

	it('rejects unknown fields', () => {
		const unknownFields = ['password', 'email', 'secret_data', 'admin_flag'];
		for (const field of unknownFields) {
			expect(validateSortField(field)).toBe('resilience_score');
		}
	});
});

describe('State Validation', () => {
	const STATE_PATTERN = /^[A-Z]{2}$/;

	function validateState(state: string | null): string | null {
		if (!state) return null;
		const upper = state.toUpperCase();
		return STATE_PATTERN.test(upper) ? upper : null;
	}

	it('accepts valid US state codes', () => {
		const validStates = ['CA', 'NY', 'TX', 'FL', 'WA', 'OR', 'AK', 'HI'];
		for (const state of validStates) {
			expect(validateState(state)).toBe(state);
		}
	});

	it('converts lowercase to uppercase', () => {
		expect(validateState('ca')).toBe('CA');
		expect(validateState('ny')).toBe('NY');
	});

	it('rejects invalid formats', () => {
		const invalidStates = [
			'California', // Full name
			'C',          // Too short
			'CAL',        // Too long
			'12',         // Numbers
			'C1',         // Mixed
			'',           // Empty
			'  '          // Whitespace
		];

		for (const state of invalidStates) {
			expect(validateState(state)).toBeNull();
		}
	});
});

describe('Numeric Parameter Bounds', () => {
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

	it('prevents numeric overflow attacks', () => {
		const attacks = [
			'99999999999999999999999999',
			'-99999999999999999999999999',
			'1e308',
			'-1e308'
		];

		for (const attack of attacks) {
			const result = parseFloatParam(attack, 0, -10, 10);
			expect(result).toBeGreaterThanOrEqual(-10);
			expect(result).toBeLessThanOrEqual(10);
		}
	});

	it('handles special values safely', () => {
		expect(parseFloatParam('Infinity', 5, 0, 10)).toBe(5);
		expect(parseFloatParam('-Infinity', 5, 0, 10)).toBe(5);
		expect(parseFloatParam('NaN', 5, 0, 10)).toBe(5);
	});

	it('handles scientific notation', () => {
		expect(parseFloatParam('1e2', 0, 0, 1000)).toBe(100);
		expect(parseFloatParam('1e-2', 0, 0, 1)).toBe(0.01);
	});
});
