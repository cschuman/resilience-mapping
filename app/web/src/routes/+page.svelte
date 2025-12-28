<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>Community Resilience Mapping</title>
</svelte:head>

<main class="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800 text-white">
	<div class="container mx-auto px-4 py-16">
		<header class="text-center mb-16">
			<h1 class="text-5xl font-bold mb-4">Community Resilience Mapping</h1>
			<p class="text-xl text-slate-300 max-w-2xl mx-auto">
				Identifying communities with strong social ties and shared experiences
				that aren't captured by traditional demographic metrics.
			</p>
		</header>

		<section class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-16">
			<div class="bg-slate-700/50 rounded-xl p-6 text-center">
				<div class="text-4xl font-bold text-emerald-400">
					{data.stats.totalTracts.toLocaleString()}
				</div>
				<div class="text-slate-300 mt-2">Census Tracts Analyzed</div>
			</div>
			<div class="bg-slate-700/50 rounded-xl p-6 text-center">
				<div class="text-4xl font-bold text-emerald-400">
					{data.stats.stateCount}
				</div>
				<div class="text-slate-300 mt-2">States Covered</div>
			</div>
			<div class="bg-slate-700/50 rounded-xl p-6 text-center">
				<div class="text-4xl font-bold text-emerald-400">
					{data.stats.avgResilience}
				</div>
				<div class="text-slate-300 mt-2">Average Resilience Score</div>
			</div>
			<div class="bg-slate-700/50 rounded-xl p-6 text-center">
				<div class="text-4xl font-bold text-emerald-400">
					{(data.stats.totalPopulation / 1_000_000).toFixed(1)}M
				</div>
				<div class="text-slate-300 mt-2">People in Dataset</div>
			</div>
		</section>

		<section class="bg-slate-700/30 rounded-xl p-8 mb-16">
			<h2 class="text-2xl font-bold mb-6">Top Resilient Communities</h2>
			<div class="overflow-x-auto">
				<table class="w-full text-left">
					<thead class="text-slate-400 border-b border-slate-600">
						<tr>
							<th class="pb-3">Tract FIPS</th>
							<th class="pb-3">State</th>
							<th class="pb-3">Population</th>
							<th class="pb-3 text-right">Resilience Score</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-slate-700">
						{#each data.topTracts as tract}
							<tr class="hover:bg-slate-700/50">
								<td class="py-3 font-mono">{tract.fips}</td>
								<td class="py-3">{tract.state}</td>
								<td class="py-3">{tract.population.toLocaleString()}</td>
								<td class="py-3 text-right">
									<span class="bg-emerald-500/20 text-emerald-400 px-2 py-1 rounded">
										{tract.score}
									</span>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</section>

		<section class="text-center">
			<h2 class="text-2xl font-bold mb-4">API Access</h2>
			<p class="text-slate-300 mb-6">
				Access the data through our REST API
			</p>
			<div class="flex flex-wrap justify-center gap-4">
				<a
					href="/api/stats"
					class="bg-emerald-600 hover:bg-emerald-500 px-6 py-3 rounded-lg font-semibold transition"
				>
					GET /api/stats
				</a>
				<a
					href="/api/tracts?limit=10"
					class="bg-slate-600 hover:bg-slate-500 px-6 py-3 rounded-lg font-semibold transition"
				>
					GET /api/tracts
				</a>
			</div>
		</section>
	</div>
</main>
