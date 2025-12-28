import postgres from 'postgres';
import { env } from '$env/dynamic/private';

// Create postgres client
// Internal Fly connections use private network (no SSL needed)
// External connections (like local proxy) also don't need SSL
const dbUrl = env.DATABASE_URL || '';
export const sql = postgres(dbUrl, {
	ssl: false,
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
