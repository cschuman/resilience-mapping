<script lang="ts">
	import { page } from '$app/stores';
</script>

<svelte:head>
	<title>Page Not Found | Community Resilience Mapping</title>
	<meta name="robots" content="noindex" />
</svelte:head>

<div class="error-page">
	<div class="container">
		<div class="error-content">
			<span class="error-code">{$page.status}</span>
			<h1 class="error-title">
				{#if $page.status === 404}
					Page Not Found
				{:else}
					Something Went Wrong
				{/if}
			</h1>
			<p class="error-message">
				{#if $page.status === 404}
					The page you're looking for doesn't exist or has been moved.
				{:else}
					{$page.error?.message || 'An unexpected error occurred.'}
				{/if}
			</p>
			<div class="error-actions">
				<a href="/" class="btn btn--primary">Go Home</a>
				<a href="/map" class="btn btn--secondary">Explore Map</a>
			</div>
			<div class="error-links">
				<p>Or try one of these:</p>
				<ul>
					<li><a href="/data">Browse Data</a></li>
					<li><a href="/research">View Research</a></li>
					<li><a href="/about">Read Methodology</a></li>
				</ul>
			</div>
		</div>
	</div>
</div>

<style>
	.error-page {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		background: var(--color-foundation-deep);
		color: var(--color-text-secondary);
		padding: var(--space-8);
	}

	.container {
		max-width: 480px;
		text-align: center;
	}

	.error-content {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-2xl);
		padding: var(--space-10);
	}

	.error-code {
		display: inline-block;
		font-family: var(--font-mono);
		font-size: var(--text-6xl);
		font-weight: var(--font-weight-bold);
		color: var(--color-accent-primary);
		line-height: 1;
		margin-bottom: var(--space-4);
	}

	.error-title {
		font-family: var(--font-display);
		font-size: var(--text-2xl);
		color: var(--color-text-primary);
		margin-bottom: var(--space-3);
	}

	.error-message {
		color: var(--color-text-muted);
		margin-bottom: var(--space-6);
	}

	.error-actions {
		display: flex;
		gap: var(--space-3);
		justify-content: center;
		margin-bottom: var(--space-8);
	}

	.btn {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		padding: var(--space-3) var(--space-5);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		border-radius: var(--radius-lg);
		text-decoration: none;
		transition: all var(--duration-fast) var(--ease-out);
		border: none;
		cursor: pointer;
	}

	.btn--primary {
		background: var(--color-accent-primary);
		color: white;
	}

	.btn--primary:hover {
		filter: brightness(1.1);
	}

	.btn--secondary {
		background: var(--color-foundation-surface);
		color: var(--color-text-primary);
		border: 1px solid var(--color-border-default);
	}

	.btn--secondary:hover {
		background: var(--color-foundation-deep);
		border-color: var(--color-border-strong);
	}

	.error-links {
		border-top: 1px solid var(--color-border-subtle);
		padding-top: var(--space-6);
	}

	.error-links p {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		margin-bottom: var(--space-3);
	}

	.error-links ul {
		list-style: none;
		padding: 0;
		margin: 0;
		display: flex;
		gap: var(--space-4);
		justify-content: center;
		flex-wrap: wrap;
	}

	.error-links a {
		color: var(--color-accent-primary);
		text-decoration: none;
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
	}

	.error-links a:hover {
		text-decoration: underline;
	}

	@media (max-width: 480px) {
		.error-actions {
			flex-direction: column;
		}

		.error-links ul {
			flex-direction: column;
			gap: var(--space-2);
		}
	}
</style>
