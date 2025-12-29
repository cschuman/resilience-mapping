<script lang="ts">
	import type { ScoreCategory } from './types';
	import { SCORE_COLORS, SCORE_LABELS, SCORE_RANGES } from './types';

	interface Props {
		visible?: boolean;
		position?: 'bottom-left' | 'bottom-right' | 'top-left' | 'top-right';
		onClose?: () => void;
	}

	let { visible = true, position = 'bottom-left', onClose }: Props = $props();

	const categories: ScoreCategory[] = [
		'very-high',
		'high',
		'medium',
		'low',
		'very-low',
		'no-data'
	];

	const positionClasses: Record<string, string> = {
		'bottom-left': 'bottom-4 left-4',
		'bottom-right': 'bottom-4 right-4',
		'top-left': 'top-4 left-4',
		'top-right': 'top-4 right-4'
	};
</script>

{#if visible}
	<div
		class="legend absolute {positionClasses[position]} z-10"
		role="region"
		aria-label="Map legend showing resilience score categories"
	>
		<div class="legend__content">
			<div class="legend__header">
				<h3 class="legend__title">Resilience Score</h3>
				{#if onClose}
					<button type="button" class="legend__close" onclick={onClose} aria-label="Close legend">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
							<path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
						</svg>
					</button>
				{/if}
			</div>
			<ul class="legend__items" role="list">
				{#each categories as category}
					<li class="legend__item">
						<span
							class="legend__swatch"
							style="background-color: {SCORE_COLORS[category]}"
							aria-hidden="true"
						></span>
						<span class="legend__label">{SCORE_LABELS[category]}</span>
						<span class="legend__range">{SCORE_RANGES[category]}</span>
					</li>
				{/each}
			</ul>
			<p class="legend__note">
				Teal = thriving communities<br />
				Terra cotta = needs support
			</p>
		</div>
	</div>
{/if}

<style>
	.legend {
		pointer-events: auto;
	}

	.legend__content {
		background: rgba(255, 255, 255, 0.96);
		backdrop-filter: blur(12px);
		-webkit-backdrop-filter: blur(12px);
		border-radius: var(--radius-xl, 14px);
		box-shadow: var(--shadow-lg, 0 8px 24px rgba(0, 0, 0, 0.25));
		min-width: 200px;
		overflow: hidden;
	}

	.legend__header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem 1rem;
		border-bottom: 1px solid rgba(0, 0, 0, 0.06);
	}

	.legend__title {
		font-family: var(--font-body, system-ui);
		font-size: 0.875rem;
		font-weight: 600;
		color: #0f172a;
		margin: 0;
	}

	.legend__close {
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

	.legend__close svg {
		width: 16px;
		height: 16px;
	}

	.legend__close:hover {
		background: #f1f5f9;
		color: #0f172a;
	}

	.legend__items {
		list-style: none;
		margin: 0;
		padding: 0.5rem 0;
	}

	.legend__item {
		display: grid;
		grid-template-columns: 16px 1fr auto;
		gap: 0.5rem;
		align-items: center;
		padding: 0.375rem 1rem;
	}

	.legend__swatch {
		width: 16px;
		height: 16px;
		border-radius: 4px;
	}

	.legend__label {
		font-size: 0.8125rem;
		color: #1C1410;
	}

	.legend__range {
		font-family: var(--font-mono, ui-monospace);
		font-size: 0.75rem;
		color: #64748b;
	}

	.legend__note {
		font-size: 0.6875rem;
		color: #64748b;
		margin: 0;
		padding: 0.5rem 1rem 0.75rem;
		border-top: 1px solid rgba(0, 0, 0, 0.06);
		line-height: 1.4;
	}
</style>
