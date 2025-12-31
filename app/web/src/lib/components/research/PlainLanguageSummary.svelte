<script lang="ts">
	interface Props {
		title?: string;
	}

	let { title = 'The Short Version' }: Props = $props();
</script>

<aside class="plain-language" aria-label="Summary">
	<div class="plain-language__header">
		<div class="plain-language__icon">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
				<path d="M10 8a3 3 0 100-6 3 3 0 000 6zM3.465 14.493a1.23 1.23 0 00.41 1.412A9.957 9.957 0 0010 18c2.31 0 4.438-.784 6.131-2.1.43-.333.604-.903.408-1.41a7.002 7.002 0 00-13.074.003z" />
			</svg>
		</div>
		<h3 class="plain-language__title">{title}</h3>
	</div>

	<div class="plain-language__content">
		<slot />
	</div>
</aside>

<style>
	.plain-language {
		background: linear-gradient(135deg, var(--color-foundation-mid), var(--color-accent-secondary-glow));
		border: 1px solid var(--color-accent-secondary);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
		margin: var(--space-6) 0;
	}

	.plain-language__header {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		margin-bottom: var(--space-4);
	}

	.plain-language__icon {
		width: 36px;
		height: 36px;
		background: var(--color-accent-secondary);
		border-radius: var(--radius-lg);
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}

	.plain-language__icon svg {
		width: 20px;
		height: 20px;
		color: white;
	}

	.plain-language__title {
		font-size: var(--text-lg);
		font-weight: var(--font-weight-semibold);
		color: var(--color-accent-secondary);
		margin: 0;
	}

	.plain-language__content {
		font-size: var(--text-base);
		line-height: var(--leading-relaxed);
		color: var(--color-text-primary);
	}

	.plain-language__content :global(h4) {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-bold);
		color: var(--color-accent-secondary);
		margin-top: var(--space-4);
		margin-bottom: var(--space-2);
	}

	.plain-language__content :global(h4:first-child) {
		margin-top: 0;
	}

	.plain-language__content :global(p) {
		margin-bottom: var(--space-3);
		color: var(--color-text-secondary);
	}

	.plain-language__content :global(ul) {
		margin: 0;
		padding-left: var(--space-5);
	}

	.plain-language__content :global(li) {
		margin-bottom: var(--space-2);
		color: var(--color-text-secondary);
	}
</style>
