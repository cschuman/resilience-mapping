import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		paper: {
			slug: 'regression-to-mean',
			title: 'Regression to the Mean in Small-Area Health Estimates: Why CDC PLACES-Based Trajectory Prediction Fails',
			authors: ['Corey Schuman'],
			publishedDate: '2024-12-31',
			version: '1.0.0',
			status: 'preprint',
			doi: null,
			medrxivUrl: null,
			pdfUrl: '/research/papers/regression-to-mean-v1.0.0.pdf'
		}
	};
};
