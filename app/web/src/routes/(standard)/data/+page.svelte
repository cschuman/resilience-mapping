<script lang="ts">
	import type { PageData } from './$types';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	let { data }: { data: PageData } = $props();

	function updateSort(column: string) {
		const currentSort = data.filters.sort;
		const currentOrder = data.filters.order;

		let newOrder = 'desc';
		if (currentSort === column && currentOrder === 'desc') {
			newOrder = 'asc';
		}

		const params = new URLSearchParams($page.url.searchParams);
		params.set('sort', column);
		params.set('order', newOrder);
		params.set('page', '1');
		goto(`?${params.toString()}`);
	}

	function updateState(state: string) {
		const params = new URLSearchParams($page.url.searchParams);
		if (state) {
			params.set('state', state);
		} else {
			params.delete('state');
		}
		params.set('page', '1');
		goto(`?${params.toString()}`);
	}

	function goToPage(pageNum: number) {
		const params = new URLSearchParams($page.url.searchParams);
		params.set('page', pageNum.toString());
		goto(`?${params.toString()}`);
	}

	function formatScore(score: string | null): string {
		if (!score) return '—';
		const num = parseFloat(score);
		return num >= 0 ? `+${score}` : score;
	}

	function getScoreClass(score: string | null): string {
		if (!score) return '';
		const num = parseFloat(score);
		if (num >= 2) return 'score--very-high';
		if (num >= 1) return 'score--high';
		if (num >= 0) return 'score--medium';
		if (num >= -1) return 'score--low';
		return 'score--very-low';
	}

	function getSortIcon(column: string): string {
		if (data.filters.sort !== column) return '↕';
		return data.filters.order === 'desc' ? '↓' : '↑';
	}
</script>

<svelte:head>
	<title>Data Explorer | Community Resilience Mapping</title>
	<meta name="description" content="Browse and filter census tract resilience data." />
</svelte:head>

<div class="data-page">
	<div class="container">
		<header class="header">
			<div class="header__text">
				<p class="header__eyebrow">Browse Dataset</p>
				<h1 class="header__title">Data Explorer</h1>
				<p class="header__subtitle">
					{data.pagination.total.toLocaleString()} census tracts with resilience scores
				</p>
			</div>
			<div class="header__actions">
				<a href="/api/tracts?format=csv" class="btn btn--primary" download>
					<svg viewBox="0 0 20 20" fill="currentColor">
						<path d="M10.75 2.75a.75.75 0 00-1.5 0v8.614L6.295 8.235a.75.75 0 10-1.09 1.03l4.25 4.5a.75.75 0 001.09 0l4.25-4.5a.75.75 0 00-1.09-1.03l-2.955 3.129V2.75z" />
						<path d="M3.5 12.75a.75.75 0 00-1.5 0v2.5A2.75 2.75 0 004.75 18h10.5A2.75 2.75 0 0018 15.25v-2.5a.75.75 0 00-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5z" />
					</svg>
					Download CSV
				</a>
			</div>
		</header>

		<!-- Filters -->
		<div class="filters">
			<div class="filter">
				<label for="state-filter" class="filter__label">State</label>
				<select
					id="state-filter"
					class="filter__select"
					value={data.filters.state}
					onchange={(e) => updateState(e.currentTarget.value)}
				>
					<option value="">All States</option>
					{#each data.states as state}
						<option value={state}>{state}</option>
					{/each}
				</select>
			</div>
		</div>

		<!-- Table -->
		<div class="table-wrapper">
			<table class="table">
				<thead>
					<tr>
						<th class="th-location">
							<button class="sort-btn" onclick={() => updateSort('state_abbr')}>
								Location {getSortIcon('state_abbr')}
							</button>
						</th>
						<th>
							<button class="sort-btn" onclick={() => updateSort('resilience_score')}>
								Score {getSortIcon('resilience_score')}
							</button>
						</th>
						<th>
							<button class="sort-btn" onclick={() => updateSort('total_pop')}>
								Population {getSortIcon('total_pop')}
							</button>
						</th>
						<th></th>
					</tr>
				</thead>
				<tbody>
					{#each data.tracts as tract}
						<tr>
							<td class="location">{tract.location}</td>
							<td>
								<span class="score {getScoreClass(tract.score)}">
									{formatScore(tract.score)}
								</span>
							</td>
							<td>{tract.population?.toLocaleString() ?? '—'}</td>
							<td>
								<a href="/map?tract={tract.fips}" class="view-link">View</a>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>

		<!-- Pagination -->
		<nav class="pagination" aria-label="Table pagination">
			<span class="pagination__info">
				Page {data.pagination.page} of {data.pagination.totalPages}
			</span>
			<div class="pagination__buttons">
				<button
					class="pagination__btn"
					disabled={data.pagination.page <= 1}
					onclick={() => goToPage(data.pagination.page - 1)}
				>
					Previous
				</button>
				<button
					class="pagination__btn"
					disabled={data.pagination.page >= data.pagination.totalPages}
					onclick={() => goToPage(data.pagination.page + 1)}
				>
					Next
				</button>
			</div>
		</nav>
	</div>
</div>

<style>
	.data-page {
		color: var(--color-text-secondary);
	}

	.container {
		max-width: var(--container-xl);
		margin: 0 auto;
		padding: var(--space-8) var(--space-6) var(--space-16);
	}

	/* Header */
	.header {
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		align-items: flex-start;
		gap: var(--space-6);
		margin-bottom: var(--space-8);
	}

	.header__eyebrow {
		font-size: var(--text-xs);
		font-weight: var(--font-weight-semibold);
		color: var(--color-accent-primary);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		margin-bottom: var(--space-2);
	}

	.header__title {
		font-family: var(--font-display);
		font-size: var(--text-3xl);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.header__subtitle {
		color: var(--color-text-muted);
	}

	.header__actions {
		flex-shrink: 0;
	}

	/* Button */
	.btn {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		padding: var(--space-2) var(--space-4);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		border-radius: var(--radius-lg);
		text-decoration: none;
		transition: all var(--duration-fast) var(--ease-out);
		border: none;
		cursor: pointer;
	}

	.btn svg {
		width: 16px;
		height: 16px;
	}

	.btn--primary {
		background: var(--color-accent-primary);
		color: white;
	}

	.btn--primary:hover {
		filter: brightness(1.1);
	}

	/* Filters */
	.filters {
		display: flex;
		gap: var(--space-4);
		margin-bottom: var(--space-6);
	}

	.filter__label {
		display: block;
		font-size: var(--text-xs);
		font-weight: var(--font-weight-medium);
		color: var(--color-text-muted);
		margin-bottom: var(--space-1);
	}

	.filter__select {
		padding: var(--space-2) var(--space-3);
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-default);
		border-radius: var(--radius-md);
		color: var(--color-text-primary);
		font-size: var(--text-sm);
		min-width: 120px;
	}

	.filter__select:focus {
		outline: none;
		border-color: var(--color-accent-primary);
	}

	/* Table */
	.table-wrapper {
		overflow-x: auto;
		margin-bottom: var(--space-6);
	}

	.table {
		width: 100%;
		border-collapse: collapse;
		font-size: var(--text-sm);
	}

	.table th {
		text-align: left;
		padding: var(--space-3) var(--space-4);
		background: var(--color-foundation-mid);
		color: var(--color-text-muted);
		font-weight: var(--font-weight-medium);
		font-size: var(--text-xs);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wider);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.table td {
		padding: var(--space-3) var(--space-4);
		border-bottom: 1px solid var(--color-border-subtle);
		color: var(--color-text-secondary);
	}

	.table tbody tr:hover {
		background: var(--color-foundation-surface);
	}

	.sort-btn {
		background: none;
		border: none;
		color: inherit;
		font: inherit;
		cursor: pointer;
		display: flex;
		align-items: center;
		gap: var(--space-1);
	}

	.sort-btn:hover {
		color: var(--color-accent-primary);
	}

	.th-location {
		min-width: 240px;
	}

	.location {
		color: var(--color-text-primary);
		font-weight: var(--font-weight-medium);
	}

	.score {
		font-family: var(--font-mono);
		font-weight: var(--font-weight-semibold);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.score--very-high {
		color: var(--color-score-very-high);
		background: var(--color-score-very-high-bg);
	}

	.score--high {
		color: var(--color-score-high);
		background: rgba(61, 154, 136, 0.15);
	}

	.score--medium {
		color: var(--color-score-medium);
		background: rgba(166, 124, 82, 0.15);
	}

	.score--low {
		color: var(--color-score-low);
		background: rgba(212, 145, 93, 0.15);
	}

	.score--very-low {
		color: var(--color-score-very-low);
		background: rgba(199, 93, 58, 0.15);
	}

	.view-link {
		color: var(--color-accent-primary);
		text-decoration: none;
		font-weight: var(--font-weight-medium);
	}

	.view-link:hover {
		text-decoration: underline;
	}

	/* Pagination */
	.pagination {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.pagination__info {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	.pagination__buttons {
		display: flex;
		gap: var(--space-2);
	}

	.pagination__btn {
		padding: var(--space-2) var(--space-4);
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-default);
		border-radius: var(--radius-md);
		color: var(--color-text-secondary);
		font-size: var(--text-sm);
		cursor: pointer;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.pagination__btn:hover:not(:disabled) {
		background: var(--color-foundation-surface);
		border-color: var(--color-border-strong);
	}

	.pagination__btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}
</style>
