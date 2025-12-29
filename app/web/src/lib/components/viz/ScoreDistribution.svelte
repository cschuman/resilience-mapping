<script lang="ts">
	/**
	 * Score Distribution Histogram
	 *
	 * Visualizes the distribution of resilience scores with color-coded bars.
	 */
	interface Props {
		buckets: number[];
		min?: number;
		max?: number;
	}

	let { buckets, min = -4, max = 4 }: Props = $props();

	const width = 400;
	const height = 120;
	const padding = { top: 10, right: 10, bottom: 24, left: 10 };
	const chartWidth = width - padding.left - padding.right;
	const chartHeight = height - padding.top - padding.bottom;

	// Calculate bar dimensions
	const barCount = buckets.length;
	const barWidth = chartWidth / barCount;
	const maxCount = Math.max(...buckets);

	// Get color for a score value
	function getColor(bucketIndex: number): string {
		const score = min + (bucketIndex + 0.5) * ((max - min) / barCount);
		if (score >= 2) return 'var(--color-score-very-high)';
		if (score >= 1) return 'var(--color-score-high)';
		if (score >= 0) return 'var(--color-score-medium)';
		if (score >= -1) return 'var(--color-score-low)';
		return 'var(--color-score-very-low)';
	}

	// X-axis labels
	const xLabels = [-4, -2, 0, 2, 4];
</script>

<div class="distribution">
	<svg viewBox="0 0 {width} {height}" class="distribution__chart">
		<!-- Bars -->
		<g transform="translate({padding.left}, {padding.top})">
			{#each buckets as count, i}
				{@const barHeight = maxCount > 0 ? (count / maxCount) * chartHeight : 0}
				<rect
					x={i * barWidth + 1}
					y={chartHeight - barHeight}
					width={barWidth - 2}
					height={barHeight}
					fill={getColor(i)}
					rx="2"
				/>
			{/each}
		</g>

		<!-- Zero line -->
		<line
			x1={padding.left + chartWidth / 2}
			y1={padding.top}
			x2={padding.left + chartWidth / 2}
			y2={padding.top + chartHeight}
			stroke="var(--color-text-muted)"
			stroke-width="1"
			stroke-dasharray="4,4"
			opacity="0.5"
		/>

		<!-- X-axis -->
		<g transform="translate({padding.left}, {padding.top + chartHeight})">
			{#each xLabels as label}
				{@const x = ((label - min) / (max - min)) * chartWidth}
				<text
					{x}
					y="16"
					text-anchor="middle"
					class="distribution__label"
				>
					{label > 0 ? '+' : ''}{label}
				</text>
			{/each}
		</g>
	</svg>

	<div class="distribution__legend">
		<span class="distribution__legend-item">
			<span class="distribution__dot distribution__dot--low"></span>
			Struggling
		</span>
		<span class="distribution__legend-item">
			<span class="distribution__dot distribution__dot--mid"></span>
			Average
		</span>
		<span class="distribution__legend-item">
			<span class="distribution__dot distribution__dot--high"></span>
			Thriving
		</span>
	</div>
</div>

<style>
	.distribution {
		width: 100%;
		max-width: 400px;
	}

	.distribution__chart {
		width: 100%;
		height: auto;
	}

	.distribution__label {
		font-family: var(--font-mono);
		font-size: 10px;
		fill: var(--color-text-muted);
	}

	.distribution__legend {
		display: flex;
		justify-content: center;
		gap: var(--space-4);
		margin-top: var(--space-2);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.distribution__legend-item {
		display: flex;
		align-items: center;
		gap: var(--space-1);
	}

	.distribution__dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
	}

	.distribution__dot--low {
		background: var(--color-score-very-low);
	}

	.distribution__dot--mid {
		background: var(--color-score-medium);
	}

	.distribution__dot--high {
		background: var(--color-score-very-high);
	}
</style>
