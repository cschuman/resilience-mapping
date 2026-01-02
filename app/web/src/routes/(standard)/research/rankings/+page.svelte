<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	// State name lookup
	const STATE_NAMES: Record<string, string> = {
		AL: 'Alabama', AK: 'Alaska', AZ: 'Arizona', AR: 'Arkansas', CA: 'California',
		CO: 'Colorado', CT: 'Connecticut', DE: 'Delaware', DC: 'Washington DC', FL: 'Florida',
		GA: 'Georgia', HI: 'Hawaii', ID: 'Idaho', IL: 'Illinois', IN: 'Indiana',
		IA: 'Iowa', KS: 'Kansas', KY: 'Kentucky', LA: 'Louisiana', ME: 'Maine',
		MD: 'Maryland', MA: 'Massachusetts', MI: 'Michigan', MN: 'Minnesota', MS: 'Mississippi',
		MO: 'Missouri', MT: 'Montana', NE: 'Nebraska', NV: 'Nevada', NH: 'New Hampshire',
		NJ: 'New Jersey', NM: 'New Mexico', NY: 'New York', NC: 'North Carolina', ND: 'North Dakota',
		OH: 'Ohio', OK: 'Oklahoma', OR: 'Oregon', PA: 'Pennsylvania', RI: 'Rhode Island',
		SC: 'South Carolina', SD: 'South Dakota', TN: 'Tennessee', TX: 'Texas', UT: 'Utah',
		VT: 'Vermont', VA: 'Virginia', WA: 'Washington', WV: 'West Virginia', WI: 'Wisconsin',
		WY: 'Wyoming'
	};

	type TabId = 'states' | 'top-counties' | 'bottom-counties' | 'inequality';
	let activeTab: TabId = $state('states');

	const tabs: { id: TabId; label: string }[] = [
		{ id: 'states', label: 'All States' },
		{ id: 'top-counties', label: 'Top Counties' },
		{ id: 'bottom-counties', label: 'Bottom Counties' },
		{ id: 'inequality', label: 'Widest Gaps' }
	];
</script>

<svelte:head>
	<title>State & County Rankings | odds.health Research</title>
	<meta
		name="description"
		content="Complete state and county rankings for community health resilience across the United States. Find how your area compares."
	/>
</svelte:head>

<div class="rankings-page">
	<div class="container">
		<nav class="breadcrumb" aria-label="Breadcrumb">
			<a href="/research">Research</a>
			<span class="separator">/</span>
			<span class="current">Rankings</span>
		</nav>

		<header class="header">
			<h1 class="header__title">State & County Rankings</h1>
			<p class="header__subtitle">
				Complete rankings based on average community health resilience scores.
				<strong>{data.stateCount} states</strong> and <strong>{data.countyCount.toLocaleString()} counties</strong> with sufficient data.
			</p>
		</header>

		<!-- Tab Navigation -->
		<div class="tabs" role="tablist">
			{#each tabs as tab}
				<button
					role="tab"
					aria-selected={activeTab === tab.id}
					class="tab"
					class:tab--active={activeTab === tab.id}
					onclick={() => activeTab = tab.id}
				>
					{tab.label}
				</button>
			{/each}
		</div>

		<!-- Tab Panels -->
		<div class="panel">
			{#if activeTab === 'states'}
				<div class="table-container">
					<table class="data-table">
						<thead>
							<tr>
								<th class="col-rank">Rank</th>
								<th class="col-name">State</th>
								<th class="col-score">Avg Resilience</th>
								<th class="col-tracts">Tracts</th>
								<th class="col-pop">Population</th>
							</tr>
						</thead>
						<tbody>
							{#each data.allStates as state, i}
								<tr>
									<td class="col-rank">{i + 1}</td>
									<td class="col-name">{STATE_NAMES[state.state] || state.state}</td>
									<td class="col-score" class:positive={state.avgResilience > 0} class:negative={state.avgResilience < 0}>
										{state.avgResilience > 0 ? '+' : ''}{state.avgResilience.toFixed(3)}
									</td>
									<td class="col-tracts">{state.tractCount.toLocaleString()}</td>
									<td class="col-pop">{(state.population / 1_000_000).toFixed(1)}M</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>

			{:else if activeTab === 'top-counties'}
				<p class="panel__intro">Top 50 counties by average resilience (minimum 10 census tracts)</p>
				<div class="table-container">
					<table class="data-table">
						<thead>
							<tr>
								<th class="col-rank">Rank</th>
								<th class="col-name">County</th>
								<th class="col-state">State</th>
								<th class="col-score">Avg Resilience</th>
								<th class="col-tracts">Tracts</th>
							</tr>
						</thead>
						<tbody>
							{#each data.topCounties as county, i}
								<tr>
									<td class="col-rank">{i + 1}</td>
									<td class="col-name">{county.county}</td>
									<td class="col-state">{county.state}</td>
									<td class="col-score positive">+{county.avgResilience.toFixed(3)}</td>
									<td class="col-tracts">{county.tractCount}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>

			{:else if activeTab === 'bottom-counties'}
				<p class="panel__intro">Bottom 50 counties by average resilience (minimum 10 census tracts)</p>
				<div class="table-container">
					<table class="data-table">
						<thead>
							<tr>
								<th class="col-rank">Rank</th>
								<th class="col-name">County</th>
								<th class="col-state">State</th>
								<th class="col-score">Avg Resilience</th>
								<th class="col-tracts">Tracts</th>
							</tr>
						</thead>
						<tbody>
							{#each data.bottomCounties as county, i}
								<tr>
									<td class="col-rank">{data.countyCount - i}</td>
									<td class="col-name">{county.county}</td>
									<td class="col-state">{county.state}</td>
									<td class="col-score negative">{county.avgResilience.toFixed(3)}</td>
									<td class="col-tracts">{county.tractCount}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>

			{:else if activeTab === 'inequality'}
				<p class="panel__intro">
					Counties with the widest gap between their best and worst neighborhoods (minimum 20 tracts)
				</p>
				<div class="table-container">
					<table class="data-table">
						<thead>
							<tr>
								<th class="col-rank">Rank</th>
								<th class="col-name">County</th>
								<th class="col-state">State</th>
								<th class="col-gap">Gap</th>
								<th class="col-range">Best → Worst</th>
								<th class="col-tracts">Tracts</th>
							</tr>
						</thead>
						<tbody>
							{#each data.mostUnequalCounties as county, i}
								<tr>
									<td class="col-rank">{i + 1}</td>
									<td class="col-name">{county.county}</td>
									<td class="col-state">{county.state}</td>
									<td class="col-gap">{county.range.toFixed(1)} pts</td>
									<td class="col-range">
										<span class="positive">+{county.maxScore.toFixed(1)}</span>
										→
										<span class="negative">{county.minScore.toFixed(1)}</span>
									</td>
									<td class="col-tracts">{county.tractCount}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{/if}
		</div>

		<section class="methodology">
			<h2>Methodology Note</h2>
			<p>
				Rankings are based on the average resilience score of all residential census tracts within each geography.
				County rankings require at least 10 tracts for statistical reliability; inequality rankings require 20.
				Resilience is measured as the standardized residual from regression predicting health burden from socioeconomic factors.
			</p>
			<a href="/research/papers-list" class="link">Read our methodology papers →</a>
		</section>
	</div>
</div>

<style>
	.rankings-page {
		color: var(--color-text-primary);
	}

	.container {
		max-width: var(--container-lg);
		margin: 0 auto;
		padding: var(--space-8) var(--space-6) var(--space-16);
	}

	.breadcrumb {
		display: flex;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-sm);
		margin-bottom: var(--space-6);
	}

	.breadcrumb a {
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	.breadcrumb a:hover {
		text-decoration: underline;
	}

	.breadcrumb .separator {
		color: var(--color-text-muted);
	}

	.breadcrumb .current {
		color: var(--color-text-secondary);
	}

	.header {
		margin-bottom: var(--space-8);
	}

	.header__title {
		font-family: var(--font-display);
		font-size: var(--text-3xl);
		font-weight: var(--font-weight-normal);
		margin-bottom: var(--space-3);
	}

	.header__subtitle {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
	}

	.header__subtitle strong {
		color: var(--color-text-primary);
	}

	/* Tabs */
	.tabs {
		display: flex;
		gap: var(--space-2);
		margin-bottom: var(--space-6);
		border-bottom: 1px solid var(--color-border-subtle);
		padding-bottom: var(--space-1);
		overflow-x: auto;
	}

	.tab {
		padding: var(--space-3) var(--space-4);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-text-secondary);
		background: none;
		border: none;
		border-bottom: 2px solid transparent;
		cursor: pointer;
		white-space: nowrap;
		transition: all var(--duration-fast);
	}

	.tab:hover {
		color: var(--color-text-primary);
	}

	.tab--active {
		color: var(--color-accent-primary);
		border-bottom-color: var(--color-accent-primary);
	}

	/* Panel */
	.panel {
		margin-bottom: var(--space-12);
	}

	.panel__intro {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-4);
	}

	/* Table */
	.table-container {
		overflow-x: auto;
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-lg);
	}

	.data-table {
		width: 100%;
		border-collapse: collapse;
		font-size: var(--text-sm);
	}

	.data-table th {
		text-align: left;
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-secondary);
		background: var(--color-foundation-mid);
		padding: var(--space-3) var(--space-4);
		border-bottom: 1px solid var(--color-border-subtle);
		white-space: nowrap;
	}

	.data-table td {
		padding: var(--space-3) var(--space-4);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.data-table tr:last-child td {
		border-bottom: none;
	}

	.data-table tr:hover td {
		background: var(--color-foundation-mid);
	}

	.col-rank {
		width: 60px;
		text-align: center;
		font-weight: var(--font-weight-medium);
		color: var(--color-text-muted);
	}

	.col-name {
		font-weight: var(--font-weight-medium);
	}

	.col-state {
		color: var(--color-text-secondary);
	}

	.col-score {
		font-family: var(--font-mono);
		font-weight: var(--font-weight-medium);
		text-align: right;
	}

	.col-tracts,
	.col-pop {
		text-align: right;
		color: var(--color-text-secondary);
	}

	.col-gap {
		font-family: var(--font-mono);
		font-weight: var(--font-weight-semibold);
		color: var(--color-warning);
		background: rgba(232, 165, 71, 0.1);
		text-align: center;
	}

	.col-range {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
	}

	.positive {
		color: var(--color-score-high);
	}

	.negative {
		color: var(--color-score-low);
	}

	/* Methodology */
	.methodology {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
	}

	.methodology h2 {
		font-size: var(--text-lg);
		font-weight: var(--font-weight-semibold);
		margin-bottom: var(--space-3);
	}

	.methodology p {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-4);
	}

	.methodology .link {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	.methodology .link:hover {
		text-decoration: underline;
	}

	@media (max-width: 640px) {
		.container {
			padding: var(--space-6) var(--space-4) var(--space-12);
		}

		.tabs {
			gap: 0;
		}

		.tab {
			padding: var(--space-2) var(--space-3);
			font-size: var(--text-xs);
		}

		.data-table {
			font-size: var(--text-xs);
		}

		.data-table th,
		.data-table td {
			padding: var(--space-2) var(--space-3);
		}
	}
</style>
