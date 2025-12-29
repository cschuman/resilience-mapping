<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';
	import type { GeocoderResponse, GeocoderResult, ScoreCategory } from '$lib/components/map/types';
	import { SCORE_COLORS } from '$lib/components/map/types';

	interface Props {
		/** Placeholder text for input */
		placeholder?: string;
		/** Callback when a result is selected */
		onSelect?: (result: GeocoderResult) => void;
	}

	let { placeholder = 'Search by address...', onSelect }: Props = $props();

	// Component state
	let inputValue = $state('');
	let results: GeocoderResult[] = $state([]);
	let isLoading = $state(false);
	let isOpen = $state(false);
	let error = $state<string | null>(null);
	let selectedIndex = $state(-1);
	let inputElement: HTMLInputElement;
	let debounceTimeout: ReturnType<typeof setTimeout>;

	// AbortController for cancelling in-flight requests
	let abortController: AbortController | null = null;

	// Generate unique IDs for ARIA (only in browser to avoid hydration mismatch)
	let listboxId = $state('search-results');

	onMount(() => {
		// Generate unique ID only in browser to avoid hydration mismatch
		listboxId = `search-results-${crypto.randomUUID().slice(0, 8)}`;
	});

	// Cleanup on destroy
	onDestroy(() => {
		// Clear any pending debounce
		clearTimeout(debounceTimeout);
		// Abort any in-flight request
		abortController?.abort();
	});

	/**
	 * Debounced search function.
	 */
	function handleInput(): void {
		clearTimeout(debounceTimeout);
		error = null;
		selectedIndex = -1;

		if (inputValue.trim().length < 3) {
			results = [];
			isOpen = false;
			return;
		}

		isLoading = true;
		debounceTimeout = setTimeout(async () => {
			await performSearch();
		}, 400);
	}

	/**
	 * Perform the geocode search with AbortController to cancel stale requests.
	 */
	async function performSearch(): Promise<void> {
		const searchValue = inputValue.trim();

		if (searchValue.length < 3) {
			isLoading = false;
			return;
		}

		// Abort any previous in-flight request
		abortController?.abort();
		abortController = new AbortController();

		try {
			const response = await fetch(
				`/api/geocode?address=${encodeURIComponent(searchValue)}`,
				{ signal: abortController.signal }
			);

			// Handle HTTP error responses with specific messages
			if (!response.ok) {
				if (response.status === 429) {
					const data = await response.json();
					error = data.error || 'Too many requests. Please wait.';
				} else if (response.status === 504) {
					error = 'Search is taking too long. Please try again.';
				} else if (response.status === 502 || response.status === 503) {
					error = 'Geocoding service is temporarily unavailable.';
				} else {
					error = 'Search failed. Please try again.';
				}
				results = [];
				isOpen = true;
				return;
			}

			const data: GeocoderResponse = await response.json();

			if (!data.success) {
				error = data.error || 'Search failed';
				results = [];
			} else if (data.results.length === 0) {
				error = 'No results found for this address';
				results = [];
			} else {
				results = data.results;
				error = null;
			}

			isOpen = results.length > 0 || error !== null;
		} catch (err) {
			// Ignore abort errors - they're expected when we cancel stale requests
			if (err instanceof Error && err.name === 'AbortError') {
				return;
			}

			error = 'Network error. Please check your connection.';
			results = [];
			isOpen = true;
		} finally {
			isLoading = false;
		}
	}

	/**
	 * Handle keyboard navigation.
	 */
	function handleKeydown(e: KeyboardEvent): void {
		if (!isOpen) {
			if (e.key === 'ArrowDown' && results.length > 0) {
				isOpen = true;
				selectedIndex = 0;
				e.preventDefault();
			}
			return;
		}

		switch (e.key) {
			case 'ArrowDown':
				e.preventDefault();
				selectedIndex = Math.min(selectedIndex + 1, results.length - 1);
				break;
			case 'ArrowUp':
				e.preventDefault();
				selectedIndex = Math.max(selectedIndex - 1, 0);
				break;
			case 'Enter':
				e.preventDefault();
				if (selectedIndex >= 0 && results[selectedIndex]) {
					selectResult(results[selectedIndex]);
				}
				break;
			case 'Escape':
				e.preventDefault();
				closeDropdown();
				break;
			case 'Tab':
				closeDropdown();
				break;
		}
	}

	/**
	 * Select a result.
	 */
	function selectResult(result: GeocoderResult): void {
		inputValue = result.matchedAddress;
		closeDropdown();
		onSelect?.(result);
	}

	/**
	 * Close the dropdown.
	 */
	function closeDropdown(): void {
		isOpen = false;
		selectedIndex = -1;
	}

	/**
	 * Handle focus out.
	 */
	function handleFocusOut(e: FocusEvent): void {
		// Close dropdown if focus moves outside the component
		const relatedTarget = e.relatedTarget as HTMLElement | null;
		if (!relatedTarget?.closest('.search-container')) {
			closeDropdown();
		}
	}

	/**
	 * Format score for display.
	 */
	function formatScore(score: number | null | undefined): string {
		if (score == null) return 'N/A';
		return score >= 0 ? `+${score.toFixed(2)}` : score.toFixed(2);
	}

	/**
	 * Get color for score category.
	 */
	function getCategoryColor(category: ScoreCategory): string {
		return SCORE_COLORS[category] || SCORE_COLORS['no-data'];
	}

	/**
	 * Clear the input.
	 */
	function clearInput(): void {
		inputValue = '';
		results = [];
		error = null;
		isOpen = false;
		inputElement?.focus();
	}
</script>

<div class="search-container">
	<div class="input-wrapper">
		<svg
			class="search-icon"
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 20 20"
			fill="currentColor"
			aria-hidden="true"
		>
			<path
				fill-rule="evenodd"
				d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z"
				clip-rule="evenodd"
			/>
		</svg>
		<input
			bind:this={inputElement}
			bind:value={inputValue}
			oninput={handleInput}
			onkeydown={handleKeydown}
			onfocusout={handleFocusOut}
			type="text"
			class="search-input"
			{placeholder}
			autocomplete="off"
			role="combobox"
			aria-autocomplete="list"
			aria-expanded={isOpen}
			aria-haspopup="listbox"
			aria-controls={listboxId}
			aria-activedescendant={selectedIndex >= 0 ? `result-${selectedIndex}` : undefined}
		/>
		{#if isLoading}
			<div class="loading-spinner" aria-hidden="true"></div>
		{:else if inputValue.length > 0}
			<button
				type="button"
				class="clear-button"
				onclick={clearInput}
				aria-label="Clear search"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
					class="w-4 h-4"
				>
					<path
						d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
					/>
				</svg>
			</button>
		{/if}
	</div>

	{#if isOpen}
		<ul class="results-dropdown" id={listboxId} role="listbox" aria-label="Search results">
			{#if error}
				<li class="error-message" role="status">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 20 20"
						fill="currentColor"
						class="w-4 h-4"
						aria-hidden="true"
					>
						<path
							fill-rule="evenodd"
							d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z"
							clip-rule="evenodd"
						/>
					</svg>
					<span>{error}</span>
				</li>
			{:else}
				{#each results as result, index}
					<li
						id={`result-${index}`}
						class="result-item"
						class:selected={index === selectedIndex}
						role="option"
						aria-selected={index === selectedIndex}
						onclick={() => selectResult(result)}
						onkeydown={(e) => e.key === 'Enter' && selectResult(result)}
						onmouseenter={() => (selectedIndex = index)}
					>
						<div class="result-main">
							<span class="result-address">{result.matchedAddress}</span>
							<span class="result-fips">{result.tractFips}</span>
						</div>
						<div class="result-details">
							<span class="result-location">
								{result.state} &middot; County {result.county}
							</span>
							{#if result.resilienceScore !== null}
								<span
									class="result-score"
									style="color: {getCategoryColor(result.scoreCategory)}"
								>
									{formatScore(result.resilienceScore)}
									{#if result.percentile !== null}
										<span class="result-percentile">
											({result.percentile}th percentile)
										</span>
									{/if}
								</span>
							{:else}
								<span class="result-no-data">No data</span>
							{/if}
						</div>
					</li>
				{/each}
			{/if}
		</ul>
	{/if}
</div>

<style>
	.search-container {
		position: relative;
		width: 100%;
	}

	.input-wrapper {
		position: relative;
		display: flex;
		align-items: center;
	}

	.search-icon {
		position: absolute;
		left: 0.75rem;
		width: 1rem;
		height: 1rem;
		color: #64748b;
		pointer-events: none;
	}

	.search-input {
		width: 100%;
		padding: 0.5rem 2.25rem 0.5rem 2.25rem;
		background: #334155;
		border: 1px solid transparent;
		border-radius: 8px;
		color: white;
		font-size: 0.875rem;
		outline: none;
		transition: all 0.15s ease;
	}

	.search-input::placeholder {
		color: #94a3b8;
	}

	.search-input:focus {
		border-color: #10b981;
		background: #1e293b;
	}

	.loading-spinner {
		position: absolute;
		right: 0.75rem;
		width: 16px;
		height: 16px;
		border: 2px solid rgba(255, 255, 255, 0.2);
		border-top-color: #10b981;
		border-radius: 50%;
		animation: spin 0.8s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	.clear-button {
		position: absolute;
		right: 0.5rem;
		display: flex;
		align-items: center;
		justify-content: center;
		width: 24px;
		height: 24px;
		border: none;
		background: transparent;
		color: #64748b;
		cursor: pointer;
		border-radius: 4px;
		transition: all 0.15s ease;
	}

	.clear-button:hover {
		color: white;
		background: rgba(255, 255, 255, 0.1);
	}

	.results-dropdown {
		position: absolute;
		top: calc(100% + 4px);
		left: 0;
		right: 0;
		max-height: 320px;
		overflow-y: auto;
		background: #1e293b;
		border: 1px solid #334155;
		border-radius: 8px;
		box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
		list-style: none;
		margin: 0;
		padding: 0.25rem 0;
		z-index: 50;
	}

	.error-message {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.75rem 1rem;
		color: #f87171;
		font-size: 0.875rem;
	}

	.result-item {
		padding: 0.75rem 1rem;
		cursor: pointer;
		transition: background 0.1s ease;
	}

	.result-item:hover,
	.result-item.selected {
		background: #334155;
	}

	.result-main {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: 0.5rem;
		margin-bottom: 0.25rem;
	}

	.result-address {
		font-size: 0.875rem;
		color: white;
		line-height: 1.4;
	}

	.result-fips {
		font-size: 0.75rem;
		font-family: ui-monospace, monospace;
		color: #94a3b8; /* slate-400 - 5.6:1 contrast on dark bg */
		white-space: nowrap;
	}

	.result-details {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 0.5rem;
	}

	.result-location {
		font-size: 0.75rem;
		color: #cbd5e1; /* slate-300 - 8.1:1 contrast on dark bg */
	}

	.result-score {
		font-size: 0.875rem;
		font-weight: 600;
	}

	.result-percentile {
		font-size: 0.6875rem;
		font-weight: 400;
		opacity: 0.8;
	}

	.result-no-data {
		font-size: 0.75rem;
		color: #94a3b8; /* slate-400 - 5.6:1 contrast on dark bg */
		font-style: italic;
	}
</style>
