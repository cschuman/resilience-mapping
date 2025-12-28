<script lang="ts">
	import type { ScoreCategory } from './types';
	import { SCORE_COLORS, SCORE_LABELS, SCORE_RANGES } from './types';

	interface Props {
		/** Whether the legend is visible */
		visible?: boolean;
		/** Position of the legend */
		position?: 'bottom-left' | 'bottom-right' | 'top-left' | 'top-right';
		/** Callback when close button is clicked */
		onClose?: () => void;
	}

	let { visible = true, position = 'bottom-left', onClose }: Props = $props();

	// Categories in display order (high to low)
	const categories: ScoreCategory[] = [
		'very-high',
		'high',
		'medium',
		'low',
		'very-low',
		'no-data'
	];

	// Position classes
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
		<div class="legend-content">
			<div class="legend-header">
				<h3 class="legend-title">Resilience Score</h3>
				{#if onClose}
					<button
						type="button"
						class="close-button"
						onclick={onClose}
						aria-label="Close legend"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 20 20"
							fill="currentColor"
							class="w-4 h-4"
							aria-hidden="true"
						>
							<path
								d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
							/>
						</svg>
					</button>
				{/if}
			</div>
			<ul class="legend-items" role="list">
				{#each categories as category}
					<li class="legend-item">
						<span
							class="color-swatch"
							style="background-color: {SCORE_COLORS[category]}"
							aria-hidden="true"
						></span>
						<span class="category-label">{SCORE_LABELS[category]}</span>
						<span class="category-range">{SCORE_RANGES[category]}</span>
					</li>
				{/each}
			</ul>
			<p class="legend-note">
				Scores represent deviation from predicted health burden
			</p>
		</div>
	</div>
{/if}

<style>
	.legend {
		pointer-events: auto;
	}

	.legend-content {
		background: rgba(255, 255, 255, 0.95);
		backdrop-filter: blur(8px);
		border-radius: 8px;
		box-shadow:
			0 4px 6px -1px rgba(0, 0, 0, 0.1),
			0 2px 4px -2px rgba(0, 0, 0, 0.1);
		min-width: 200px;
		overflow: hidden;
	}

	.legend-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem 1rem;
		border-bottom: 1px solid #e2e8f0;
	}

	.legend-title {
		font-size: 0.875rem;
		font-weight: 600;
		color: #0f172a;
		margin: 0;
	}

	.close-button {
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

	.close-button:hover {
		background: #f1f5f9;
		color: #0f172a;
	}

	.close-button:focus-visible {
		outline: 2px solid #10b981;
		outline-offset: 2px;
	}

	.legend-items {
		list-style: none;
		margin: 0;
		padding: 0.5rem 0;
	}

	.legend-item {
		display: grid;
		grid-template-columns: 16px 1fr auto;
		gap: 0.5rem;
		align-items: center;
		padding: 0.375rem 1rem;
	}

	.color-swatch {
		width: 16px;
		height: 16px;
		border-radius: 3px;
		border: 1px solid rgba(0, 0, 0, 0.1);
	}

	.category-label {
		font-size: 0.8125rem;
		color: #334155;
	}

	.category-range {
		font-size: 0.75rem;
		color: #64748b;
		font-family: ui-monospace, monospace;
	}

	.legend-note {
		font-size: 0.6875rem;
		color: #94a3b8;
		margin: 0;
		padding: 0.5rem 1rem 0.75rem;
		border-top: 1px solid #e2e8f0;
		line-height: 1.4;
	}
</style>
