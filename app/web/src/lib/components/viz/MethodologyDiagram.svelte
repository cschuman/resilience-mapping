<script lang="ts">
	/**
	 * Methodology Flow Diagram
	 *
	 * Visual representation of the data pipeline:
	 * Data Sources → Prediction Model → Resilience Score
	 */
</script>

<div class="diagram">
	<div class="diagram__flow">
		<!-- Data Sources -->
		<div class="diagram__step">
			<div class="diagram__box diagram__box--sources">
				<div class="diagram__icon">
					<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
						<path d="M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7c0-2-1-3-3-3H7c-2 0-3 1-3 3z"/>
						<path d="M8 12h8M8 8h8M8 16h4"/>
					</svg>
				</div>
				<span class="diagram__label">Data</span>
				<span class="diagram__sublabel">CDC, USDA, Census</span>
			</div>
		</div>

		<!-- Arrow -->
		<div class="diagram__arrow">
			<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
				<path d="M5 12h14M13 6l6 6-6 6"/>
			</svg>
		</div>

		<!-- Model -->
		<div class="diagram__step">
			<div class="diagram__box diagram__box--model">
				<div class="diagram__icon">
					<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
						<circle cx="12" cy="12" r="3"/>
						<path d="M12 2v4M12 18v4M2 12h4M18 12h4"/>
						<path d="M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
					</svg>
				</div>
				<span class="diagram__label">Model</span>
				<span class="diagram__sublabel">Predict health from factors</span>
			</div>
		</div>

		<!-- Arrow -->
		<div class="diagram__arrow">
			<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
				<path d="M5 12h14M13 6l6 6-6 6"/>
			</svg>
		</div>

		<!-- Score -->
		<div class="diagram__step">
			<div class="diagram__box diagram__box--score">
				<div class="diagram__icon">
					<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
						<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
					</svg>
				</div>
				<span class="diagram__label">Score</span>
				<span class="diagram__sublabel">Actual − Predicted</span>
			</div>
		</div>
	</div>

	<!-- Explanation -->
	<div class="diagram__explain">
		<div class="diagram__formula">
			<span class="diagram__term diagram__term--positive">Better than expected</span>
			<span class="diagram__equals">=</span>
			<span class="diagram__term diagram__term--score">Positive score</span>
		</div>
	</div>
</div>

<style>
	.diagram {
		padding: var(--space-4) 0;
	}

	.diagram__flow {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--space-2);
		flex-wrap: wrap;
	}

	.diagram__step {
		flex-shrink: 0;
	}

	.diagram__box {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--space-1);
		padding: var(--space-3) var(--space-4);
		border-radius: var(--radius-lg);
		background: var(--color-foundation-deep);
		border: 1px solid var(--color-border-subtle);
		min-width: 90px;
		transition: border-color var(--duration-fast) var(--ease-out);
	}

	.diagram__box--sources {
		border-color: var(--color-accent-secondary);
	}

	.diagram__box--model {
		border-color: var(--color-accent-primary);
	}

	.diagram__box--score {
		border-color: var(--color-score-very-high);
	}

	.diagram__icon {
		width: 28px;
		height: 28px;
		color: var(--color-text-muted);
	}

	.diagram__box--sources .diagram__icon {
		color: var(--color-accent-secondary);
	}

	.diagram__box--model .diagram__icon {
		color: var(--color-accent-primary);
	}

	.diagram__box--score .diagram__icon {
		color: var(--color-score-very-high);
	}

	.diagram__label {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
	}

	.diagram__sublabel {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		text-align: center;
	}

	.diagram__arrow {
		width: 24px;
		height: 24px;
		color: var(--color-text-muted);
		flex-shrink: 0;
	}

	.diagram__explain {
		margin-top: var(--space-4);
		text-align: center;
	}

	.diagram__formula {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
	}

	.diagram__term {
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
		background: var(--color-foundation-deep);
	}

	.diagram__term--positive {
		color: var(--color-score-very-high);
	}

	.diagram__term--score {
		color: var(--color-score-very-high);
		background: var(--color-score-very-high-bg);
	}

	.diagram__equals {
		color: var(--color-text-muted);
	}

	@media (max-width: 480px) {
		.diagram__flow {
			flex-direction: column;
			gap: var(--space-1);
		}

		.diagram__arrow {
			transform: rotate(90deg);
		}

		.diagram__box {
			width: 100%;
			max-width: 200px;
		}
	}
</style>
