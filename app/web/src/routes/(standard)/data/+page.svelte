<script lang="ts">
	import type { PageData } from './$types';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	let { data }: { data: PageData } = $props();

	// Focus management for keyboard navigation
	let tableRef: HTMLTableElement | null = $state(null);
	let focusedRow = $state(-1);

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

	function updateFilter(key: string, value: string | number) {
		const params = new URLSearchParams($page.url.searchParams);
		if (value === '' || value === null || value === undefined) {
			params.delete(key);
		} else {
			params.set(key, String(value));
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

	function getSortLabel(column: string): string {
		if (data.filters.sort !== column) return 'Sort';
		return data.filters.order === 'desc' ? 'Sorted descending' : 'Sorted ascending';
	}

	// Keyboard navigation for table
	function handleTableKeydown(event: KeyboardEvent) {
		if (!tableRef) return;
		const rows = tableRef.querySelectorAll('tbody tr');
		if (rows.length === 0) return;

		switch (event.key) {
			case 'ArrowDown':
				event.preventDefault();
				focusedRow = Math.min(focusedRow + 1, rows.length - 1);
				(rows[focusedRow] as HTMLElement).focus();
				break;
			case 'ArrowUp':
				event.preventDefault();
				focusedRow = Math.max(focusedRow - 1, 0);
				(rows[focusedRow] as HTMLElement).focus();
				break;
			case 'Enter':
			case ' ':
				if (focusedRow >= 0) {
					event.preventDefault();
					const link = rows[focusedRow].querySelector('.view-link') as HTMLAnchorElement;
					if (link) link.click();
				}
				break;
			case 'Home':
				event.preventDefault();
				focusedRow = 0;
				(rows[0] as HTMLElement).focus();
				break;
			case 'End':
				event.preventDefault();
				focusedRow = rows.length - 1;
				(rows[rows.length - 1] as HTMLElement).focus();
				break;
		}
	}

	function clearAllFilters() {
		goto('/data');
	}

	const hasActiveFilters = $derived(
		data.filters.state ||
			data.filters.minScore > -10 ||
			data.filters.maxScore < 10 ||
			data.filters.minPop > 0
	);
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
					{data.pagination.total.toLocaleString()} residential census tracts
					{#if hasActiveFilters}
						<span class="header__filter-note">(filtered)</span>
					{/if}
				</p>
			</div>
			<div class="header__actions">
				<a
					href={data.csvUrl}
					class="btn btn--primary"
					download="resilience-data.csv"
					aria-label="Download filtered data as CSV"
				>
					<svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
						<path
							d="M10.75 2.75a.75.75 0 00-1.5 0v8.614L6.295 8.235a.75.75 0 10-1.09 1.03l4.25 4.5a.75.75 0 001.09 0l4.25-4.5a.75.75 0 00-1.09-1.03l-2.955 3.129V2.75z"
						/>
						<path
							d="M3.5 12.75a.75.75 0 00-1.5 0v2.5A2.75 2.75 0 004.75 18h10.5A2.75 2.75 0 0018 15.25v-2.5a.75.75 0 00-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5z"
						/>
					</svg>
					Download CSV
				</a>
			</div>
		</header>

		<!-- Filters -->
		<div class="filters" role="search" aria-label="Filter data">
			<div class="filter">
				<label for="state-filter" class="filter__label">State</label>
				<select
					id="state-filter"
					class="filter__select"
					value={data.filters.state}
					onchange={(e) => updateFilter('state', e.currentTarget.value)}
					aria-describedby="state-filter-desc"
				>
					<option value="">All States</option>
					{#each data.states as state}
						<option value={state}>{state}</option>
					{/each}
				</select>
				<span id="state-filter-desc" class="sr-only">Filter tracts by state</span>
			</div>

			<div class="filter filter--range">
				<label for="min-score" class="filter__label">Score Range</label>
				<div class="filter__range-inputs">
					<input
						type="number"
						id="min-score"
						class="filter__input filter__input--small"
						value={data.filters.minScore}
						min="-10"
						max="10"
						step="0.5"
						onchange={(e) => updateFilter('min_score', e.currentTarget.value)}
						aria-label="Minimum score"
					/>
					<span class="filter__range-sep">to</span>
					<input
						type="number"
						id="max-score"
						class="filter__input filter__input--small"
						value={data.filters.maxScore}
						min="-10"
						max="10"
						step="0.5"
						onchange={(e) => updateFilter('max_score', e.currentTarget.value)}
						aria-label="Maximum score"
					/>
				</div>
			</div>

			<div class="filter">
				<label for="min-pop" class="filter__label">Min Population</label>
				<input
					type="number"
					id="min-pop"
					class="filter__input"
					value={data.filters.minPop}
					min="0"
					max="100000"
					step="100"
					onchange={(e) => updateFilter('min_pop', e.currentTarget.value)}
					aria-describedby="min-pop-desc"
				/>
				<span id="min-pop-desc" class="sr-only">Minimum population threshold</span>
			</div>

			{#if hasActiveFilters}
				<div class="filter filter--clear">
					<button type="button" class="btn btn--ghost" onclick={clearAllFilters}>
						Clear Filters
					</button>
				</div>
			{/if}
		</div>

		<!-- Table -->
		<div class="table-wrapper" role="region" aria-label="Census tract data" tabindex="0">
			<table
				class="table"
				bind:this={tableRef}
				onkeydown={handleTableKeydown}
				role="grid"
				aria-rowcount={data.pagination.total}
				aria-colcount={4}
			>
				<thead>
					<tr role="row">
						<th scope="col" class="th-location" aria-sort={data.filters.sort === 'state_abbr' ? (data.filters.order === 'asc' ? 'ascending' : 'descending') : 'none'}>
							<button
								class="sort-btn"
								onclick={() => updateSort('state_abbr')}
								aria-label={`Location, ${getSortLabel('state_abbr')}`}
							>
								Location {getSortIcon('state_abbr')}
							</button>
						</th>
						<th scope="col" aria-sort={data.filters.sort === 'resilience_score' ? (data.filters.order === 'asc' ? 'ascending' : 'descending') : 'none'}>
							<button
								class="sort-btn"
								onclick={() => updateSort('resilience_score')}
								aria-label={`Score, ${getSortLabel('resilience_score')}`}
							>
								Score {getSortIcon('resilience_score')}
							</button>
						</th>
						<th scope="col" aria-sort={data.filters.sort === 'total_pop' ? (data.filters.order === 'asc' ? 'ascending' : 'descending') : 'none'}>
							<button
								class="sort-btn"
								onclick={() => updateSort('total_pop')}
								aria-label={`Population, ${getSortLabel('total_pop')}`}
							>
								Population {getSortIcon('total_pop')}
							</button>
						</th>
						<th scope="col">
							<span class="sr-only">Actions</span>
						</th>
					</tr>
				</thead>
				<tbody>
					{#each data.tracts as tract, i}
						<tr
							role="row"
							tabindex={focusedRow === i ? 0 : -1}
							class:tr--focused={focusedRow === i}
							aria-rowindex={(data.pagination.page - 1) * data.pagination.limit + i + 1}
						>
							<td role="gridcell" class="location">
								<span class="location__name">{tract.location}</span>
								<span class="location__fips">{tract.fips}</span>
							</td>
							<td role="gridcell">
								<span class="score {getScoreClass(tract.score)}" aria-label={`Resilience score: ${tract.score ?? 'not available'}`}>
									{formatScore(tract.score)}
								</span>
							</td>
							<td role="gridcell">{tract.population?.toLocaleString() ?? '—'}</td>
							<td role="gridcell">
								<a href="/map?tract={tract.fips}" class="view-link" aria-label="View {tract.location} on map">
									View
								</a>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>

		<!-- Pagination -->
		<nav class="pagination" aria-label="Table pagination">
			<p class="pagination__info" aria-live="polite">
				Showing {((data.pagination.page - 1) * data.pagination.limit) + 1}–{Math.min(data.pagination.page * data.pagination.limit, data.pagination.total)} of {data.pagination.total.toLocaleString()} tracts
			</p>
			<div class="pagination__buttons">
				<button
					class="pagination__btn"
					disabled={!data.pagination.hasPrev}
					onclick={() => goToPage(1)}
					aria-label="Go to first page"
				>
					First
				</button>
				<button
					class="pagination__btn"
					disabled={!data.pagination.hasPrev}
					onclick={() => goToPage(data.pagination.page - 1)}
					aria-label="Go to previous page"
				>
					Previous
				</button>
				<span class="pagination__current">
					Page {data.pagination.page} of {data.pagination.totalPages}
				</span>
				<button
					class="pagination__btn"
					disabled={!data.pagination.hasNext}
					onclick={() => goToPage(data.pagination.page + 1)}
					aria-label="Go to next page"
				>
					Next
				</button>
				<button
					class="pagination__btn"
					disabled={!data.pagination.hasNext}
					onclick={() => goToPage(data.pagination.totalPages)}
					aria-label="Go to last page"
				>
					Last
				</button>
			</div>
		</nav>

		<!-- Data notes -->
		<aside class="data-notes" aria-labelledby="data-notes-heading">
			<h2 id="data-notes-heading" class="sr-only">Data Notes</h2>
			<p>
				<strong>Note:</strong> Only residential tracts are shown. Industrial, commercial, and zero-population tracts are excluded.
				Scores range from -10 (most burdened) to +10 (most resilient). Download includes up to 10,000 filtered tracts.
			</p>
		</aside>
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

	/* Screen reader only */
	.sr-only {
		position: absolute;
		width: 1px;
		height: 1px;
		padding: 0;
		margin: -1px;
		overflow: hidden;
		clip: rect(0, 0, 0, 0);
		white-space: nowrap;
		border: 0;
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

	.header__filter-note {
		color: var(--color-accent-primary);
		font-style: italic;
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

	.btn--ghost {
		background: transparent;
		color: var(--color-text-muted);
		padding: var(--space-2) var(--space-3);
	}

	.btn--ghost:hover {
		color: var(--color-text-primary);
		background: var(--color-foundation-surface);
	}

	/* Filters */
	.filters {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-4);
		margin-bottom: var(--space-6);
		padding: var(--space-4);
		background: var(--color-foundation-mid);
		border-radius: var(--radius-lg);
		border: 1px solid var(--color-border-subtle);
	}

	.filter {
		display: flex;
		flex-direction: column;
		gap: var(--space-1);
	}

	.filter--range {
		flex-direction: column;
	}

	.filter--clear {
		align-self: flex-end;
		margin-left: auto;
	}

	.filter__label {
		font-size: var(--text-xs);
		font-weight: var(--font-weight-medium);
		color: var(--color-text-muted);
	}

	.filter__select,
	.filter__input {
		padding: var(--space-2) var(--space-3);
		background: var(--color-foundation-deep);
		border: 1px solid var(--color-border-default);
		border-radius: var(--radius-md);
		color: var(--color-text-primary);
		font-size: var(--text-sm);
	}

	.filter__select {
		min-width: 140px;
	}

	.filter__input {
		min-width: 100px;
	}

	.filter__input--small {
		min-width: 70px;
		width: 70px;
	}

	.filter__select:focus,
	.filter__input:focus {
		outline: none;
		border-color: var(--color-accent-primary);
		box-shadow: 0 0 0 2px var(--color-accent-primary-subtle);
	}

	.filter__range-inputs {
		display: flex;
		align-items: center;
		gap: var(--space-2);
	}

	.filter__range-sep {
		color: var(--color-text-muted);
		font-size: var(--text-sm);
	}

	/* Table */
	.table-wrapper {
		overflow-x: auto;
		margin-bottom: var(--space-6);
		border-radius: var(--radius-lg);
		border: 1px solid var(--color-border-subtle);
	}

	.table-wrapper:focus {
		outline: 2px solid var(--color-accent-primary);
		outline-offset: 2px;
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

	.table tbody tr:hover,
	.table tbody tr.tr--focused {
		background: var(--color-foundation-surface);
	}

	.table tbody tr:focus {
		outline: 2px solid var(--color-accent-primary);
		outline-offset: -2px;
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
		padding: var(--space-1);
		margin: calc(-1 * var(--space-1));
		border-radius: var(--radius-sm);
	}

	.sort-btn:hover {
		color: var(--color-accent-primary);
	}

	.sort-btn:focus {
		outline: 2px solid var(--color-accent-primary);
		outline-offset: 2px;
	}

	.th-location {
		min-width: 240px;
	}

	.location {
		color: var(--color-text-primary);
	}

	.location__name {
		display: block;
		font-weight: var(--font-weight-medium);
	}

	.location__fips {
		display: block;
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		font-family: var(--font-mono);
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
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.view-link:hover {
		text-decoration: underline;
	}

	.view-link:focus {
		outline: 2px solid var(--color-accent-primary);
		outline-offset: 2px;
	}

	/* Pagination */
	.pagination {
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		align-items: center;
		gap: var(--space-4);
	}

	.pagination__info {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	.pagination__buttons {
		display: flex;
		align-items: center;
		gap: var(--space-2);
	}

	.pagination__current {
		padding: 0 var(--space-3);
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	.pagination__btn {
		padding: var(--space-2) var(--space-3);
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

	.pagination__btn:focus {
		outline: 2px solid var(--color-accent-primary);
		outline-offset: 2px;
	}

	.pagination__btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	/* Data notes */
	.data-notes {
		margin-top: var(--space-8);
		padding: var(--space-4);
		background: var(--color-foundation-mid);
		border-radius: var(--radius-lg);
		border-left: 3px solid var(--color-accent-primary);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	.data-notes strong {
		color: var(--color-text-secondary);
	}

	/* Responsive */
	@media (max-width: 640px) {
		.filters {
			flex-direction: column;
		}

		.filter--clear {
			margin-left: 0;
		}

		.pagination {
			flex-direction: column;
			align-items: stretch;
		}

		.pagination__buttons {
			justify-content: center;
			flex-wrap: wrap;
		}

		.pagination__current {
			text-align: center;
			order: -1;
			width: 100%;
		}
	}
</style>
