import { sveltekit } from '@sveltejs/kit/vite';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],

	// Optimization for MapLibre GL JS and PMTiles
	optimizeDeps: {
		include: ['maplibre-gl', 'pmtiles']
	},

	build: {
		// MapLibre GL JS is large, increase warning limit
		chunkSizeWarningLimit: 1000
	}
});
