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
		// Increase warning limit slightly (MapLibre is legitimately large)
		chunkSizeWarningLimit: 600,

		rollupOptions: {
			output: {
				// Manual chunks for better code splitting
				manualChunks: (id: string) => {
					// MapLibre GL gets its own chunk (loaded only on /map route)
					if (id.includes('maplibre-gl')) {
						return 'maplibre';
					}
					// PMTiles gets its own chunk
					if (id.includes('pmtiles')) {
						return 'pmtiles';
					}
					// Zod validation library
					if (id.includes('zod')) {
						return 'validation';
					}
				}
			}
		}
	}
});
