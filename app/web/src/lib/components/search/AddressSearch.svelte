<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import type { GeocoderResponse, GeocoderResult, ScoreCategory } from '$lib/components/map/types';
	import { SCORE_COLORS } from '$lib/components/map/types';

	interface Props {
		placeholder?: string;
		onSelect?: (result: GeocoderResult) => void;
	}

	let { placeholder = 'Search by address...', onSelect }: Props = $props();

	// State
	let inputValue = $state('');
	let results: GeocoderResult[] = $state([]);
	let isLoading = $state(false);
	let isLocating = $state(false);
	let isOpen = $state(false);
	let error = $state<string | null>(null);
	let selectedIndex = $state(-1);
	let inputElement: HTMLInputElement;
	let debounceTimeout: ReturnType<typeof setTimeout>;
	let abortController: AbortController | null = null;
	let listboxId = $state('search-results');

	// Check if geolocation is available
	const hasGeolocation = typeof navigator !== 'undefined' && 'geolocation' in navigator;

	onMount(() => {
		listboxId = `search-results-${crypto.randomUUID().slice(0, 8)}`;
	});

	onDestroy(() => {
		clearTimeout(debounceTimeout);
		abortController?.abort();
	});

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

	async function performSearch(): Promise<void> {
		const searchValue = inputValue.trim();
		if (searchValue.length < 3) {
			isLoading = false;
			return;
		}

		abortController?.abort();
		abortController = new AbortController();

		try {
			const response = await fetch(
				`/api/geocode?address=${encodeURIComponent(searchValue)}`,
				{ signal: abortController.signal }
			);

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
			if (err instanceof Error && err.name === 'AbortError') return;
			error = 'Network error. Please check your connection.';
			results = [];
			isOpen = true;
		} finally {
			isLoading = false;
		}
	}

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

	function selectResult(result: GeocoderResult): void {
		inputValue = result.matchedAddress;
		closeDropdown();
		onSelect?.(result);
	}

	function closeDropdown(): void {
		isOpen = false;
		selectedIndex = -1;
	}

	function handleFocusOut(e: FocusEvent): void {
		const relatedTarget = e.relatedTarget as HTMLElement | null;
		if (!relatedTarget?.closest('.search')) {
			closeDropdown();
		}
	}

	function formatScore(score: number | null | undefined): string {
		if (score == null) return 'N/A';
		return score >= 0 ? `+${score.toFixed(2)}` : score.toFixed(2);
	}

	function getCategoryColor(category: ScoreCategory): string {
		return SCORE_COLORS[category] || SCORE_COLORS['no-data'];
	}

	function clearInput(): void {
		inputValue = '';
		results = [];
		error = null;
		isOpen = false;
		inputElement?.focus();
	}

	/**
	 * Get user's current location and find their tract.
	 */
	async function useMyLocation(): Promise<void> {
		if (!hasGeolocation || isLocating) return;

		isLocating = true;
		error = null;
		results = [];
		isOpen = false;

		try {
			// Get browser location
			const position = await new Promise<GeolocationPosition>((resolve, reject) => {
				navigator.geolocation.getCurrentPosition(resolve, reject, {
					enableHighAccuracy: true,
					timeout: 10000,
					maximumAge: 60000
				});
			});

			const { latitude, longitude } = position.coords;

			// Call reverse geocode API
			abortController?.abort();
			abortController = new AbortController();

			const response = await fetch(
				`/api/geocode/reverse?lat=${latitude}&lng=${longitude}`,
				{ signal: abortController.signal }
			);

			if (!response.ok) {
				if (response.status === 429) {
					error = 'Too many requests. Please wait.';
				} else {
					error = 'Failed to find your location. Please try again.';
				}
				isOpen = true;
				return;
			}

			const data: GeocoderResponse = await response.json();

			if (!data.success || data.results.length === 0) {
				error = data.error || 'Could not find census tract at your location';
				isOpen = true;
				return;
			}

			// Success - select the result
			const result = data.results[0];
			inputValue = result.matchedAddress;
			onSelect?.(result);
		} catch (err) {
			if (err instanceof Error) {
				if (err.name === 'AbortError') return;

				// Handle geolocation errors
				if ('code' in err) {
					const geoErr = err as GeolocationPositionError;
					switch (geoErr.code) {
						case 1: // PERMISSION_DENIED
							error = 'Location access denied. Please enable location permissions.';
							break;
						case 2: // POSITION_UNAVAILABLE
							error = 'Location unavailable. Please try again.';
							break;
						case 3: // TIMEOUT
							error = 'Location request timed out. Please try again.';
							break;
						default:
							error = 'Could not get your location.';
					}
				} else {
					error = 'Could not get your location. Please try again.';
				}
			} else {
				error = 'Could not get your location. Please try again.';
			}
			isOpen = true;
		} finally {
			isLocating = false;
		}
	}
</script>

<div class="search">
	<div class="search__input-wrapper">
		<svg class="search__icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
			<path fill-rule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clip-rule="evenodd" />
		</svg>
		<input
			bind:this={inputElement}
			bind:value={inputValue}
			oninput={handleInput}
			onkeydown={handleKeydown}
			onfocusout={handleFocusOut}
			type="text"
			class="search__input"
			{placeholder}
			autocomplete="off"
			role="combobox"
			aria-autocomplete="list"
			aria-expanded={isOpen}
			aria-haspopup="listbox"
			aria-controls={listboxId}
			aria-activedescendant={selectedIndex >= 0 ? `result-${selectedIndex}` : undefined}
		/>
		{#if isLoading || isLocating}
			<div class="search__spinner" aria-hidden="true"></div>
		{:else}
			{#if inputValue.length > 0}
				<button type="button" class="search__clear" onclick={clearInput} aria-label="Clear search">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
						<path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
					</svg>
				</button>
			{/if}
			{#if hasGeolocation}
				<button
					type="button"
					class="search__location"
					onclick={useMyLocation}
					aria-label="Use my location"
					title="Use my location"
				>
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
						<path fill-rule="evenodd" d="M9.69 18.933l.003.001C9.89 19.02 10 19 10 19s.11.02.308-.066l.002-.001.006-.003.018-.008a5.741 5.741 0 00.281-.14c.186-.096.446-.24.757-.433.62-.384 1.445-.966 2.274-1.765C15.302 14.988 17 12.493 17 9A7 7 0 103 9c0 3.492 1.698 5.988 3.355 7.584a13.731 13.731 0 002.273 1.765 11.842 11.842 0 00.976.544l.062.029.018.008.006.003zM10 11.25a2.25 2.25 0 100-4.5 2.25 2.25 0 000 4.5z" clip-rule="evenodd" />
					</svg>
				</button>
			{/if}
		{/if}
	</div>

	{#if isOpen}
		<ul class="search__dropdown" id={listboxId} role="listbox" aria-label="Search results">
			{#if error}
				<li class="search__error" role="status">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
						<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
					</svg>
					<span>{error}</span>
				</li>
			{:else}
				{#each results as result, index}
					<li
						id={`result-${index}`}
						class="search__result"
						class:search__result--selected={index === selectedIndex}
						role="option"
						aria-selected={index === selectedIndex}
						onclick={() => selectResult(result)}
						onkeydown={(e) => e.key === 'Enter' && selectResult(result)}
						onmouseenter={() => (selectedIndex = index)}
					>
						<div class="search__result-main">
							<span class="search__result-address">{result.matchedAddress}</span>
							<span class="search__result-fips">{result.tractFips}</span>
						</div>
						<div class="search__result-details">
							<span class="search__result-location">
								{result.state} &middot; {result.county}
							</span>
							{#if result.resilienceScore !== null}
								<span class="search__result-score" style="color: {getCategoryColor(result.scoreCategory)}">
									{formatScore(result.resilienceScore)}
								</span>
							{:else}
								<span class="search__result-no-data">No data</span>
							{/if}
						</div>
					</li>
				{/each}
			{/if}
		</ul>
	{/if}
</div>

<style>
	.search {
		position: relative;
		width: 100%;
	}

	.search__input-wrapper {
		position: relative;
		display: flex;
		align-items: center;
	}

	.search__icon {
		position: absolute;
		left: var(--space-3);
		width: 16px;
		height: 16px;
		color: var(--color-text-muted);
		pointer-events: none;
	}

	.search__input {
		width: 100%;
		padding: var(--space-3) var(--space-10);
		padding-right: calc(var(--space-2) + 56px); /* Room for clear + location buttons */
		background: var(--color-foundation-surface);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-lg);
		color: var(--color-text-primary);
		font-size: var(--text-sm);
		outline: none;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.search__input::placeholder {
		color: var(--color-text-muted);
	}

	.search__input:focus {
		border-color: var(--color-accent-primary);
		background: var(--color-foundation-mid);
		box-shadow: 0 0 0 3px var(--color-accent-primary-subtle);
	}

	.search__spinner {
		position: absolute;
		right: var(--space-3);
		width: 16px;
		height: 16px;
		border: 2px solid var(--color-border-default);
		border-top-color: var(--color-accent-primary);
		border-radius: 50%;
		animation: spin 0.8s linear infinite;
	}

	@keyframes spin {
		to { transform: rotate(360deg); }
	}

	.search__clear {
		position: absolute;
		right: var(--space-2);
		display: flex;
		align-items: center;
		justify-content: center;
		width: 24px;
		height: 24px;
		background: transparent;
		border: none;
		color: var(--color-text-muted);
		cursor: pointer;
		border-radius: var(--radius-sm);
		transition: all var(--duration-fast) var(--ease-out);
	}

	.search__clear:hover {
		color: var(--color-text-primary);
		background: var(--color-foundation-elevated);
	}

	.search__clear svg {
		width: 16px;
		height: 16px;
	}

	.search__location {
		position: absolute;
		right: var(--space-2);
		display: flex;
		align-items: center;
		justify-content: center;
		width: 24px;
		height: 24px;
		background: transparent;
		border: none;
		color: var(--color-text-muted);
		cursor: pointer;
		border-radius: var(--radius-sm);
		transition: all var(--duration-fast) var(--ease-out);
	}

	/* When clear button is visible, move location button left */
	.search__clear + .search__location {
		right: calc(var(--space-2) + 28px);
	}

	.search__location:hover {
		color: var(--color-accent-primary);
		background: var(--color-foundation-elevated);
	}

	.search__location:focus-visible {
		outline: 2px solid var(--color-accent-primary);
		outline-offset: 2px;
	}

	.search__location svg {
		width: 16px;
		height: 16px;
	}

	.search__dropdown {
		position: absolute;
		top: calc(100% + var(--space-1));
		left: 0;
		right: 0;
		max-height: 320px;
		overflow-y: auto;
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-default);
		border-radius: var(--radius-lg);
		box-shadow: var(--shadow-lg);
		list-style: none;
		margin: 0;
		padding: var(--space-1) 0;
		z-index: var(--z-dropdown);
	}

	.search__error {
		display: flex;
		align-items: center;
		gap: var(--space-2);
		padding: var(--space-3) var(--space-4);
		color: var(--color-error);
		font-size: var(--text-sm);
	}

	.search__error svg {
		width: 16px;
		height: 16px;
		flex-shrink: 0;
	}

	.search__result {
		padding: var(--space-3) var(--space-4);
		cursor: pointer;
		transition: background var(--duration-instant) var(--ease-out);
	}

	.search__result:hover,
	.search__result--selected {
		background: var(--color-foundation-surface);
	}

	.search__result-main {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: var(--space-2);
		margin-bottom: var(--space-1);
	}

	.search__result-address {
		font-size: var(--text-sm);
		color: var(--color-text-primary);
		line-height: var(--leading-snug);
	}

	.search__result-fips {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		white-space: nowrap;
	}

	.search__result-details {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: var(--space-2);
	}

	.search__result-location {
		font-size: var(--text-xs);
		color: var(--color-text-tertiary);
	}

	.search__result-score {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
	}

	.search__result-no-data {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		font-style: italic;
	}
</style>
