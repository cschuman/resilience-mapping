import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),

	kit: {
		adapter: adapter(),

		// Content Security Policy with nonces for inline scripts
		csp: {
			mode: 'auto',
			directives: {
				'default-src': ['self'],
				'script-src': ['self'],
				'style-src': ['self', 'unsafe-inline'], // MapLibre GL needs inline styles
				'img-src': ['self', 'data:', 'blob:', 'https://basemaps.cartocdn.com', 'https://*.cartocdn.com'],
				'font-src': ['self'],
				'connect-src': ['self', 'https://geocoding.geo.census.gov', 'https://basemaps.cartocdn.com', 'https://*.cartocdn.com'],
				'worker-src': ['self', 'blob:'],
				'frame-ancestors': ['self'],
				'form-action': ['self'],
				'base-uri': ['self'],
				'object-src': ['none']
			}
		}
	}
};

export default config;
