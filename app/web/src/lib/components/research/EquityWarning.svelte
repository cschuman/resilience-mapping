<script lang="ts">
	interface Props {
		status?: string;
		estimatedCompletion?: string;
	}

	let {
		status = 'Equity analysis in progress',
		estimatedCompletion = 'January 2026'
	}: Props = $props();
</script>

<aside class="equity-warning" role="alert" aria-live="assertive">
	<div class="equity-warning__header">
		<div class="equity-warning__icon">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
				<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a.75.75 0 000 1.5h.253a.25.25 0 01.244.304l-.459 2.066A1.75 1.75 0 0010.747 15H11a.75.75 0 000-1.5h-.253a.25.25 0 01-.244-.304l.459-2.066A1.75 1.75 0 009.253 9H9z" clip-rule="evenodd" />
			</svg>
		</div>
		<h3 class="equity-warning__title">Incomplete Analysis</h3>
	</div>

	<div class="equity-warning__content">
		<p class="equity-warning__main">
			<strong>This research lacks demographic-stratified validation.</strong> We have not examined
			whether findings differ by neighborhood racial/ethnic composition.
		</p>

		<p class="equity-warning__action">
			<strong>Do not use for policy decisions affecting marginalized communities</strong> without
			first conducting community-specific validation.
		</p>

		<div class="equity-warning__status">
			<span class="equity-warning__label">Status:</span>
			<span class="equity-warning__value">{status}</span>
			{#if estimatedCompletion}
				<span class="equity-warning__completion">• Expected: {estimatedCompletion}</span>
			{/if}
		</div>
	</div>
</aside>

<style>
	.equity-warning {
		background: rgba(232, 165, 71, 0.12);
		border: 2px solid var(--color-warning);
		border-radius: var(--radius-xl);
		padding: var(--space-5);
		margin: var(--space-6) 0;
	}

	.equity-warning__header {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		margin-bottom: var(--space-4);
	}

	.equity-warning__icon {
		width: 40px;
		height: 40px;
		background: var(--color-warning);
		border-radius: var(--radius-lg);
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}

	.equity-warning__icon svg {
		width: 24px;
		height: 24px;
		color: white;
	}

	.equity-warning__title {
		font-size: var(--text-lg);
		font-weight: var(--font-weight-bold);
		color: var(--color-warning);
		margin: 0;
	}

	.equity-warning__content {
		font-size: var(--text-sm);
		line-height: var(--leading-relaxed);
	}

	.equity-warning__main {
		color: var(--color-text-primary);
		margin-bottom: var(--space-3);
	}

	.equity-warning__action {
		color: var(--color-text-primary);
		background: rgba(232, 165, 71, 0.15);
		padding: var(--space-3);
		border-radius: var(--radius-lg);
		margin-bottom: var(--space-3);
	}

	.equity-warning__status {
		display: flex;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.equity-warning__label {
		font-weight: var(--font-weight-medium);
	}

	.equity-warning__value {
		color: var(--color-warning);
		font-weight: var(--font-weight-semibold);
	}

	.equity-warning__completion {
		color: var(--color-text-muted);
	}
</style>
