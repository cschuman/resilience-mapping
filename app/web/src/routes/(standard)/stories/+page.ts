import type { PageLoad } from './$types';

export const load: PageLoad = ({ url }) => {
	const category = url.searchParams.get('category') || undefined;

	return {
		category
	};
};
