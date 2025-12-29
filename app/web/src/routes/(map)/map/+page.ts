import type { PageLoad } from './$types';
import { parseMapParams } from '$lib/utils';

export const load: PageLoad = ({ url }) => {
	const params = parseMapParams(url.searchParams);

	return {
		initialTract: params.tract,
		initialCenter:
			params.lat !== undefined && params.lng !== undefined
				? ([params.lng, params.lat] as [number, number])
				: undefined,
		initialZoom: params.zoom
	};
};
