<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		title: string;
		id: string;
		defaultOpen?: boolean;
		children: Snippet;
	}

	let { title, id, defaultOpen = false, children }: Props = $props();

	let isOpen = $state(defaultOpen);

	function toggle() {
		isOpen = !isOpen;
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			toggle();
		}
	}
</script>

<div class="accordion" class:accordion--open={isOpen}>
	<button
		type="button"
		class="accordion__trigger"
		id="{id}-trigger"
		aria-expanded={isOpen}
		aria-controls="{id}-content"
		onclick={toggle}
		onkeydown={handleKeydown}
	>
		<span class="accordion__title">{title}</span>
		<svg
			class="accordion__icon"
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 20 20"
			fill="currentColor"
			aria-hidden="true"
		>
			<path
				fill-rule="evenodd"
				d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
				clip-rule="evenodd"
			/>
		</svg>
	</button>

	<div
		id="{id}-content"
		class="accordion__content"
		role="region"
		aria-labelledby="{id}-trigger"
		hidden={!isOpen}
	>
		<div class="accordion__body">
			{@render children()}
		</div>
	</div>
</div>

<style>
	.accordion {
		border: 1px solid var(--color-border-default);
		border-radius: var(--radius-xl);
		overflow: hidden;
		background: var(--color-foundation-mid);
		margin-bottom: var(--space-4);
	}

	.accordion__trigger {
		display: flex;
		align-items: center;
		justify-content: space-between;
		width: 100%;
		padding: var(--space-4) var(--space-5);
		background: transparent;
		border: none;
		color: var(--color-text-primary);
		font-family: var(--font-display);
		font-size: var(--text-lg);
		font-weight: var(--font-weight-medium);
		text-align: left;
		cursor: pointer;
		transition: background var(--duration-fast) var(--ease-out);
	}

	.accordion__trigger:hover {
		background: var(--color-foundation-surface);
	}

	.accordion__trigger:focus-visible {
		outline: 2px solid var(--color-accent-primary);
		outline-offset: -2px;
	}

	.accordion__title {
		flex: 1;
	}

	.accordion__icon {
		width: 20px;
		height: 20px;
		color: var(--color-text-muted);
		transition: transform var(--duration-normal) var(--ease-spring);
		flex-shrink: 0;
	}

	.accordion--open .accordion__icon {
		transform: rotate(180deg);
	}

	.accordion__content {
		overflow: hidden;
	}

	.accordion__content[hidden] {
		display: none;
	}

	.accordion__body {
		padding: 0 var(--space-5) var(--space-5);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		font-size: var(--text-base);
	}

	.accordion__body :global(p) {
		margin: 0 0 var(--space-4);
	}

	.accordion__body :global(p:last-child) {
		margin-bottom: 0;
	}

	.accordion__body :global(ul) {
		margin: 0 0 var(--space-4);
		padding-left: var(--space-6);
	}

	.accordion__body :global(li) {
		margin-bottom: var(--space-2);
	}

	.accordion__body :global(strong) {
		color: var(--color-text-primary);
		font-weight: var(--font-weight-semibold);
	}

	.accordion__body :global(code) {
		font-family: var(--font-mono);
		font-size: 0.875em;
		background: var(--color-foundation-deepest);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
		color: var(--color-text-muted);
	}

	.accordion__body :global(pre) {
		background: var(--color-foundation-deepest);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-lg);
		padding: var(--space-4);
		overflow-x: auto;
		margin: var(--space-4) 0;
	}

	.accordion__body :global(pre code) {
		background: none;
		padding: 0;
	}
</style>
