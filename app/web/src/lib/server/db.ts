import postgres from 'postgres';
import { env } from '$env/dynamic/private';

// Create postgres client with environment-aware SSL configuration
const dbUrl = env.DATABASE_URL || '';

// SSL configuration:
// - Fly.io internal network: SSL not needed (6pn addresses)
// - Local development: SSL not needed
// Note: On Fly.io we use internal networking which doesn't require SSL
const isInternalFlyNetwork = dbUrl.includes('.internal') || dbUrl.includes('.flycast');
const isLocalDev = dbUrl.includes('localhost') || dbUrl.includes('127.0.0.1');
const isFlyEnvironment = !!env.FLY_APP_NAME;
const requireSSL = !isInternalFlyNetwork && !isLocalDev && !isFlyEnvironment && env.NODE_ENV === 'production';

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
