import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		paper: {
			slug: 'spatial-synchrony',
			title: 'Spatial Synchrony, Not Contagion: A Methodological Correction in Community Health Trajectory Prediction',
			authors: ['Corey Schuman'],
			publishedDate: '2024-12-30',
			version: '1.0.0',
			status: 'preprint',
			doi: null,
			medrxivUrl: null, // Will be updated after submission
			pdfUrl: '/research/papers/spatial-synchrony-v1.0.0.pdf'
		}
	};
};
