<script lang="ts">
	interface Props {
		warnings?: string[];
	}

	let { warnings = [] }: Props = $props();

	const defaultWarnings = [
		'Justify cuts to public health programs based on "resilience"',
		'Claim certain communities "don\'t need help" because they show resilience',
		'Target "improving" areas for gentrification or speculation',
		'Make causal claims about what creates resilience without intervention studies',
		'Assume spatial patterns imply geographic interventions will work'
	];

	const displayWarnings = warnings.length > 0 ? warnings : defaultWarnings;

	let showDetails = $state(false);
</script>

<aside class="misuse-warning" role="alert">
	<div class="misuse-warning__header">
		<div class="misuse-warning__icon">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
				<path
					fill-rule="evenodd"
					d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z"
					clip-rule="evenodd"
				/>
			</svg>
		</div>
		<h3 class="misuse-warning__title">Do NOT Use This Research To:</h3>
	</div>

	<ul class="misuse-warning__list">
		{#each displayWarnings as warning}
			<li class="misuse-warning__item">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
					<path
						fill-rule="evenodd"
						d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
						clip-rule="evenodd"
					/>
				</svg>
				{warning}
			</li>
		{/each}
	</ul>

	<button
		class="misuse-warning__details-toggle"
		onclick={() => (showDetails = !showDetails)}
		aria-expanded={showDetails}
	>
		{showDetails ? 'Hide explanation' : 'Why this warning exists'}
		<svg
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 20 20"
			fill="currentColor"
			class:rotated={showDetails}
			aria-hidden="true"
		>
			<path
				fill-rule="evenodd"
				d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
				clip-rule="evenodd"
			/>
		</svg>
	</button>

	{#if showDetails}
		<div class="misuse-warning__details">
			<p>
				Research on community resilience has been misused historically to justify disinvestment
				in marginalized communities. The logic goes: "If they're resilient, they don't need help."
				This is a fundamental misreading of what resilience research shows.
			</p>
			<p>
				<strong>Resilience is not a substitute for resources.</strong> Communities that show
				resilience despite adversity deserve more support, not less. Identifying resilience
				should complement efforts to address structural inequities, not replace them.
			</p>
			<p>
				If you see this research being misused, please contact us at
				<a href="mailto:research@odds.health">research@odds.health</a>.
			</p>
		</div>
	{/if}
</aside>

<style>
	.misuse-warning {
		background: rgba(209, 104, 71, 0.08);
		border: 1px solid rgba(209, 104, 71, 0.3);
		border-radius: var(--radius-xl);
		padding: var(--space-5);
		margin: var(--space-6) 0;
	}

	.misuse-warning__header {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		margin-bottom: var(--space-4);
	}

	.misuse-warning__icon {
		width: 32px;
		height: 32px;
		background: rgba(209, 104, 71, 0.15);
		border-radius: var(--radius-lg);
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}

	.misuse-warning__icon svg {
		width: 18px;
		height: 18px;
		color: var(--color-score-low);
	}

	.misuse-warning__title {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		color: var(--color-score-low);
		margin: 0;
	}

	.misuse-warning__list {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	.misuse-warning__item {
		display: flex;
		align-items: flex-start;
		gap: var(--space-2);
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		padding: var(--space-2) 0;
	}

	.misuse-warning__item svg {
		width: 16px;
		height: 16px;
		color: var(--color-score-low);
		flex-shrink: 0;
		margin-top: 2px;
	}

	.misuse-warning__details-toggle {
		display: inline-flex;
		align-items: center;
		gap: var(--space-1);
		margin-top: var(--space-4);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		color: var(--color-text-secondary);
		background: none;
		border: none;
		cursor: pointer;
		padding: 0;
	}

	.misuse-warning__details-toggle:hover {
		color: var(--color-text-primary);
	}

	.misuse-warning__details-toggle svg {
		width: 16px;
		height: 16px;
		transition: transform var(--duration-fast) var(--ease-out);
	}

	.misuse-warning__details-toggle svg.rotated {
		transform: rotate(180deg);
	}

	.misuse-warning__details {
		margin-top: var(--space-4);
		padding-top: var(--space-4);
		border-top: 1px solid rgba(209, 104, 71, 0.2);
	}

	.misuse-warning__details p {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-3);
	}

	.misuse-warning__details p:last-child {
		margin-bottom: 0;
	}

	.misuse-warning__details strong {
		color: var(--color-text-primary);
	}

	.misuse-warning__details a {
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	.misuse-warning__details a:hover {
		text-decoration: underline;
	}
</style>
