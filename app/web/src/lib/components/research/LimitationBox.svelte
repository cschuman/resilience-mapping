<script lang="ts">
	interface Limitation {
		title: string;
		description: string;
	}

	interface Props {
		limitations: Limitation[];
		expanded?: boolean;
	}

	let { limitations, expanded = false }: Props = $props();

	let isExpanded = $state(expanded);
</script>

<aside class="limitation-box" aria-label="Study Limitations">
	<div class="limitation-box__header">
		<div class="limitation-box__icon">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
				<path
					fill-rule="evenodd"
					d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 5zm0 9a1 1 0 100-2 1 1 0 000 2z"
					clip-rule="evenodd"
				/>
			</svg>
		</div>
		<h3 class="limitation-box__title">Important Limitations</h3>
	</div>

	<ul class="limitation-box__list">
		{#each limitations.slice(0, isExpanded ? limitations.length : 3) as limitation}
			<li class="limitation-box__item">
				<strong>{limitation.title}:</strong>
				{limitation.description}
			</li>
		{/each}
	</ul>

	{#if limitations.length > 3}
		<button
			class="limitation-box__toggle"
			onclick={() => (isExpanded = !isExpanded)}
			aria-expanded={isExpanded}
		>
			{isExpanded ? 'Show fewer' : `Show ${limitations.length - 3} more limitations`}
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 20 20"
				fill="currentColor"
				class:rotated={isExpanded}
				aria-hidden="true"
			>
				<path
					fill-rule="evenodd"
					d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
					clip-rule="evenodd"
				/>
			</svg>
		</button>
	{/if}
</aside>

<style>
	.limitation-box {
		background: rgba(232, 165, 71, 0.08);
		border: 1px solid rgba(232, 165, 71, 0.3);
		border-radius: var(--radius-xl);
		padding: var(--space-5);
		margin: var(--space-6) 0;
	}

	.limitation-box__header {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		margin-bottom: var(--space-4);
	}

	.limitation-box__icon {
		width: 32px;
		height: 32px;
		background: rgba(232, 165, 71, 0.15);
		border-radius: var(--radius-lg);
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}

	.limitation-box__icon svg {
		width: 18px;
		height: 18px;
		color: var(--color-warning);
	}

	.limitation-box__title {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		color: var(--color-warning);
		margin: 0;
	}

	.limitation-box__list {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	.limitation-box__item {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		padding: var(--space-2) 0;
		border-bottom: 1px solid rgba(232, 165, 71, 0.15);
	}

	.limitation-box__item:last-child {
		border-bottom: none;
	}

	.limitation-box__item strong {
		color: var(--color-text-primary);
	}

	.limitation-box__toggle {
		display: inline-flex;
		align-items: center;
		gap: var(--space-1);
		margin-top: var(--space-3);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-warning);
		background: none;
		border: none;
		cursor: pointer;
		padding: 0;
	}

	.limitation-box__toggle:hover {
		text-decoration: underline;
	}

	.limitation-box__toggle svg {
		width: 16px;
		height: 16px;
		transition: transform var(--duration-fast) var(--ease-out);
	}

	.limitation-box__toggle svg.rotated {
		transform: rotate(180deg);
	}
</style>
