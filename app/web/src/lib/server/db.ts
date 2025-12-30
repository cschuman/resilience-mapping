import postgres from 'postgres';
import { env } from '$env/dynamic/private';

// Create postgres client with environment-aware SSL configuration
const dbUrl = env.DATABASE_URL || '';

// SSL configuration:
// - Production external connections: require SSL
// - Fly.io internal network (.internal hostnames): SSL not needed
// - Local development: SSL not needed
const isInternalFlyNetwork = dbUrl.includes('.internal');
const isLocalDev = dbUrl.includes('localhost') || dbUrl.includes('127.0.0.1');
const requireSSL = !isInternalFlyNetwork && !isLocalDev && env.NODE_ENV === 'production';

export const sql = postgres(dbUrl, {
	ssl: requireSSL ? 'require' : false,
	max: 10,
	idle_timeout: 20,
	connect_timeout: 10
});

// Types for our data
export interface Tract {
	id: number;
	tract_fips: string;
	state_abbr: string;
	county: string;
	total_pop: number;
	resilience_score: number;
	burden: number;
	gq_college_pct: number;
	gq_military_pct: number;
	gq_correctional_pct: number;
	geometry?: unknown; // PostGIS geometry
	created_at: Date;
}

export interface Community {
	id: number;
	tract_fips: string;
	name: string;
	description?: string;
	story?: string;
	consent_given: boolean;
	created_at: Date;
}
