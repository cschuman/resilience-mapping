<script lang="ts">
	interface Props {
		background?: string;
		objective?: string;
		methods?: string;
		results?: string;
		conclusions?: string;
		keywords?: string[];
	}

	let { background, objective, methods, results, conclusions, keywords = [] }: Props = $props();
</script>

<section class="abstract-box" aria-labelledby="abstract-heading">
	<h2 id="abstract-heading" class="abstract-box__title">Abstract</h2>

	<div class="abstract-box__content">
		{#if background}
			<div class="abstract-box__section">
				<span class="abstract-box__label">Background:</span>
				<span class="abstract-box__text">{background}</span>
			</div>
		{/if}

		{#if objective}
			<div class="abstract-box__section">
				<span class="abstract-box__label">Objective:</span>
				<span class="abstract-box__text">{objective}</span>
			</div>
		{/if}

		{#if methods}
			<div class="abstract-box__section">
				<span class="abstract-box__label">Methods:</span>
				<span class="abstract-box__text">{methods}</span>
			</div>
		{/if}

		{#if results}
			<div class="abstract-box__section">
				<span class="abstract-box__label">Results:</span>
				<span class="abstract-box__text">{results}</span>
			</div>
		{/if}

		{#if conclusions}
			<div class="abstract-box__section">
				<span class="abstract-box__label">Conclusions:</span>
				<span class="abstract-box__text">{conclusions}</span>
			</div>
		{/if}
	</div>

	{#if keywords.length > 0}
		<div class="abstract-box__keywords">
			<span class="abstract-box__keywords-label">Keywords:</span>
			{#each keywords as keyword, i}
				<span class="abstract-box__keyword">{keyword}</span>
				{#if i < keywords.length - 1}<span class="abstract-box__keyword-sep">,</span>{/if}
			{/each}
		</div>
	{/if}
</section>

<style>
	.abstract-box {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
		margin: var(--space-8) 0;
	}

	.abstract-box__title {
		font-family: var(--font-display);
		font-size: var(--text-lg);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-4);
		padding-bottom: var(--space-3);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.abstract-box__content {
		display: flex;
		flex-direction: column;
		gap: var(--space-3);
	}

	.abstract-box__section {
		font-size: var(--text-sm);
		line-height: var(--leading-relaxed);
	}

	.abstract-box__label {
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-right: var(--space-1);
	}

	.abstract-box__text {
		color: var(--color-text-secondary);
	}

	.abstract-box__keywords {
		margin-top: var(--space-5);
		padding-top: var(--space-4);
		border-top: 1px solid var(--color-border-subtle);
		font-size: var(--text-sm);
	}

	.abstract-box__keywords-label {
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-right: var(--space-2);
	}

	.abstract-box__keyword {
		color: var(--color-accent-primary);
	}

	.abstract-box__keyword-sep {
		color: var(--color-text-muted);
		margin-right: var(--space-1);
	}
</style>
