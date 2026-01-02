import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		paper: {
			slug: 'structural-determinants',
			title: 'Structural Determinants of Community Health Resilience: A Tract-Level Analysis of 53,889 U.S. Communities',
			authors: ['Corey Schuman'],
			publishedDate: '2025-12-31',
			version: '1.0.0',
			status: 'preprint',
			doi: null,
			medrxivUrl: null,
			pdfUrl: '/research/papers/structural-determinants-v1.0.0.pdf'
		}
	};
};
