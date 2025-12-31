<script lang="ts">
	interface Message {
		title: string;
		description: string;
	}

	interface Props {
		messages: Message[];
		title?: string;
	}

	let { messages, title = 'Key Messages for Policy and Practice' }: Props = $props();
</script>

<aside class="key-messages" aria-labelledby="key-messages-heading">
	<h3 id="key-messages-heading" class="key-messages__title">{title}</h3>

	<ol class="key-messages__list">
		{#each messages as message, i}
			<li class="key-messages__item">
				<div class="key-messages__number">{i + 1}</div>
				<div class="key-messages__content">
					<strong class="key-messages__headline">{message.title}</strong>
					<p class="key-messages__text">{message.description}</p>
				</div>
			</li>
		{/each}
	</ol>
</aside>

<style>
	.key-messages {
		background: linear-gradient(135deg, var(--color-foundation-mid), var(--color-accent-primary-glow));
		border: 1px solid var(--color-accent-primary);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
		margin: var(--space-8) 0;
	}

	.key-messages__title {
		font-size: var(--text-lg);
		font-weight: var(--font-weight-semibold);
		color: var(--color-accent-primary);
		margin-bottom: var(--space-5);
		padding-bottom: var(--space-3);
		border-bottom: 1px solid var(--color-accent-primary);
	}

	.key-messages__list {
		list-style: none;
		padding: 0;
		margin: 0;
		display: flex;
		flex-direction: column;
		gap: var(--space-4);
	}

	.key-messages__item {
		display: flex;
		gap: var(--space-4);
	}

	.key-messages__number {
		width: 28px;
		height: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: var(--color-accent-primary);
		color: white;
		font-size: var(--text-sm);
		font-weight: var(--font-weight-bold);
		border-radius: var(--radius-full);
		flex-shrink: 0;
	}

	.key-messages__content {
		flex: 1;
	}

	.key-messages__headline {
		display: block;
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-1);
	}

	.key-messages__text {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin: 0;
	}
</style>
