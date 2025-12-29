<script lang="ts">
	import { onMount } from 'svelte';

	interface Props {
		/** Fallback content when error occurs */
		fallback?: import('svelte').Snippet<[Error]>;
		/** Callback when error is caught */
		onError?: (error: Error) => void;
		/** Children to render */
		children: import('svelte').Snippet;
	}

	let { fallback, onError, children }: Props = $props();

	let error: Error | null = $state(null);

	/**
	 * Reset the error state to retry rendering.
	 */
	export function reset(): void {
		error = null;
	}

	/**
	 * Handle errors from child components.
	 */
	function handleError(e: ErrorEvent): void {
		error = e.error instanceof Error ? e.error : new Error(String(e.error));
		onError?.(error);
		e.preventDefault();
	}

	onMount(() => {
		// Listen for unhandled errors in this subtree
		window.addEventListener('error', handleError);
		return () => window.removeEventListener('error', handleError);
	});
</script>

{#if error}
	{#if fallback}
		{@render fallback(error)}
	{:else}
		<div class="error-boundary" role="alert">
			<div class="error-content">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					fill="currentColor"
					class="error-icon"
					aria-hidden="true"
				>
					<path
						fill-rule="evenodd"
						d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003zM12 8.25a.75.75 0 01.75.75v3.75a.75.75 0 01-1.5 0V9a.75.75 0 01.75-.75zm0 8.25a1 1 0 100-1.5.75.75 0 000 1.5z"
						clip-rule="evenodd"
					/>
				</svg>
				<h2>Something went wrong</h2>
				<p class="error-message">{error.message}</p>
				<button type="button" onclick={() => reset()}>Try again</button>
			</div>
		</div>
	{/if}
{:else}
	{@render children()}
{/if}

<style>
	.error-boundary {
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: 200px;
		padding: 2rem;
		background: #0f172a;
		color: #f87171;
	}

	.error-content {
		text-align: center;
		max-width: 400px;
	}

	.error-icon {
		width: 48px;
		height: 48px;
		margin: 0 auto 1rem;
	}

	h2 {
		font-size: 1.25rem;
		font-weight: 600;
		color: white;
		margin: 0 0 0.5rem;
	}

	.error-message {
		font-size: 0.875rem;
		color: #94a3b8;
		margin: 0 0 1rem;
	}

	button {
		padding: 0.5rem 1rem;
		background: #334155;
		border: none;
		border-radius: 6px;
		color: white;
		font-size: 0.875rem;
		cursor: pointer;
		transition: background 0.15s ease;
	}

	button:hover {
		background: #475569;
	}

	button:focus-visible {
		outline: 2px solid #10b981;
		outline-offset: 2px;
	}
</style>
