<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		title: string;
		authors: string[];
		publishedDate: string;
		version?: string;
		doi?: string;
		pdfUrl?: string;
		status?: 'preprint' | 'under-review' | 'published' | 'working-paper';
		children: Snippet;
	}

	let {
		title,
		authors,
		publishedDate,
		version = '1.0.0',
		doi,
		pdfUrl,
		status = 'preprint',
		children
	}: Props = $props();

	const statusLabels: Record<string, { label: string; class: string }> = {
		preprint: { label: 'Pre-print', class: 'status--preprint' },
		'under-review': { label: 'Under Review', class: 'status--review' },
		published: { label: 'Peer-Reviewed', class: 'status--published' },
		'working-paper': { label: 'Working Paper', class: 'status--draft' }
	};

	const statusInfo = statusLabels[status] || statusLabels.preprint;
</script>

<article class="paper-layout">
	<header class="paper-header">
		<div class="paper-header__meta">
			<span class="paper-header__status {statusInfo.class}">{statusInfo.label}</span>
			<span class="paper-header__version">v{version}</span>
			<time class="paper-header__date" datetime={publishedDate}>{publishedDate}</time>
		</div>

		<h1 class="paper-header__title">{title}</h1>

		<div class="paper-header__authors">
			{#each authors as author, i}
				<span class="paper-header__author">{author}</span>
				{#if i < authors.length - 1}<span class="paper-header__separator">,</span>{/if}
			{/each}
		</div>

		<div class="paper-header__actions">
			{#if pdfUrl}
				<a href={pdfUrl} class="btn btn--primary" download>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 20 20"
						fill="currentColor"
						aria-hidden="true"
					>
						<path
							d="M10.75 2.75a.75.75 0 00-1.5 0v8.614L6.295 8.235a.75.75 0 10-1.09 1.03l4.25 4.5a.75.75 0 001.09 0l4.25-4.5a.75.75 0 00-1.09-1.03l-2.955 3.129V2.75z"
						/>
						<path
							d="M3.5 12.75a.75.75 0 00-1.5 0v2.5A2.75 2.75 0 004.75 18h10.5A2.75 2.75 0 0018 15.25v-2.5a.75.75 0 00-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5z"
						/>
					</svg>
					Download PDF
				</a>
			{/if}
			<button class="btn btn--outline" onclick={() => navigator.clipboard.writeText(window.location.href)}>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
					aria-hidden="true"
				>
					<path
						fill-rule="evenodd"
						d="M15.621 4.379a3 3 0 00-4.242 0l-7 7a3 3 0 004.241 4.243h.001l.497-.5a.75.75 0 011.064 1.057l-.498.501-.002.002a4.5 4.5 0 01-6.364-6.364l7-7a4.5 4.5 0 016.368 6.36l-3.455 3.553A2.625 2.625 0 119.52 9.52l3.45-3.451a.75.75 0 111.061 1.06l-3.45 3.451a1.125 1.125 0 001.587 1.595l3.454-3.553a3 3 0 000-4.242z"
						clip-rule="evenodd"
					/>
				</svg>
				Copy Link
			</button>
		</div>

		{#if doi}
			<div class="paper-header__doi">
				<span class="paper-header__doi-label">DOI:</span>
				<a href="https://doi.org/{doi}" class="paper-header__doi-link">{doi}</a>
			</div>
		{/if}
	</header>

	<div class="paper-content">
		{@render children()}
	</div>

	<footer class="paper-footer">
		<div class="paper-footer__citation">
			<h3>How to Cite</h3>
			<code class="citation-block">
				{authors.join(', ')} ({new Date(publishedDate).getFullYear()}). {title}. odds.health.
				{#if doi}https://doi.org/{doi}{:else}https://odds.health/research/papers/spatial-synchrony{/if}
			</code>
		</div>
	</footer>
</article>

<style>
	.paper-layout {
		max-width: 800px;
		margin: 0 auto;
		padding: var(--space-8) var(--space-6);
	}

	/* Header */
	.paper-header {
		margin-bottom: var(--space-12);
		padding-bottom: var(--space-8);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.paper-header__meta {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		margin-bottom: var(--space-4);
	}

	.paper-header__status {
		font-size: var(--text-xs);
		font-weight: var(--font-weight-bold);
		padding: var(--space-1) var(--space-3);
		border-radius: var(--radius-full);
	}

	.status--preprint {
		background: var(--color-accent-secondary-glow);
		color: var(--color-accent-secondary);
	}

	.status--review {
		background: rgba(232, 165, 71, 0.15);
		color: var(--color-warning);
	}

	.status--published {
		background: var(--color-score-high-bg);
		color: var(--color-score-high);
	}

	.status--draft {
		background: rgba(148, 163, 184, 0.15);
		color: var(--color-text-secondary);
	}

	.paper-header__version {
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.paper-header__date {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.paper-header__title {
		font-family: var(--font-display);
		font-size: clamp(var(--text-2xl), 4vw, var(--text-3xl));
		font-weight: var(--font-weight-normal);
		color: var(--color-text-primary);
		line-height: var(--leading-tight);
		margin-bottom: var(--space-4);
	}

	.paper-header__authors {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-6);
	}

	.paper-header__author {
		color: var(--color-text-primary);
	}

	.paper-header__separator {
		color: var(--color-text-muted);
		margin-right: var(--space-1);
	}

	.paper-header__actions {
		display: flex;
		gap: var(--space-3);
		flex-wrap: wrap;
		margin-bottom: var(--space-4);
	}

	.paper-header__doi {
		font-size: var(--text-sm);
	}

	.paper-header__doi-label {
		color: var(--color-text-muted);
		margin-right: var(--space-2);
	}

	.paper-header__doi-link {
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	.paper-header__doi-link:hover {
		text-decoration: underline;
	}

	/* Content */
	.paper-content {
		font-size: var(--text-base);
		line-height: var(--leading-relaxed);
		color: var(--color-text-primary);
	}

	.paper-content :global(h2) {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-top: var(--space-10);
		margin-bottom: var(--space-4);
		padding-bottom: var(--space-2);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.paper-content :global(h3) {
		font-size: var(--text-lg);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-top: var(--space-8);
		margin-bottom: var(--space-3);
	}

	.paper-content :global(p) {
		margin-bottom: var(--space-4);
	}

	.paper-content :global(table) {
		width: 100%;
		border-collapse: collapse;
		margin: var(--space-6) 0;
		font-size: var(--text-sm);
	}

	.paper-content :global(th),
	.paper-content :global(td) {
		padding: var(--space-3);
		border: 1px solid var(--color-border-subtle);
		text-align: left;
	}

	.paper-content :global(th) {
		background: var(--color-foundation-mid);
		font-weight: var(--font-weight-semibold);
	}

	.paper-content :global(code) {
		font-family: var(--font-mono);
		font-size: 0.9em;
		background: var(--color-foundation-surface);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	.paper-content :global(pre) {
		background: var(--color-foundation-surface);
		padding: var(--space-4);
		border-radius: var(--radius-lg);
		overflow-x: auto;
		margin: var(--space-6) 0;
	}

	.paper-content :global(pre code) {
		background: none;
		padding: 0;
	}

	/* Footer */
	.paper-footer {
		margin-top: var(--space-12);
		padding-top: var(--space-8);
		border-top: 1px solid var(--color-border-subtle);
	}

	.paper-footer__citation h3 {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-3);
	}

	.citation-block {
		display: block;
		font-family: var(--font-mono);
		font-size: var(--text-sm);
		background: var(--color-foundation-surface);
		padding: var(--space-4);
		border-radius: var(--radius-lg);
		border: 1px solid var(--color-border-subtle);
		color: var(--color-text-secondary);
		word-break: break-word;
	}

	/* Buttons */
	.btn {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		padding: var(--space-2) var(--space-4);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		border-radius: var(--radius-lg);
		text-decoration: none;
		transition: all var(--duration-fast) var(--ease-out);
		cursor: pointer;
		border: none;
	}

	.btn svg {
		width: 16px;
		height: 16px;
	}

	.btn--primary {
		background: var(--color-accent-primary);
		color: white;
	}

	.btn--primary:hover {
		background: var(--color-accent-primary-hover);
	}

	.btn--outline {
		background: transparent;
		color: var(--color-accent-primary);
		border: 1px solid var(--color-accent-primary);
	}

	.btn--outline:hover {
		background: var(--color-accent-primary);
		color: white;
	}

	/* Responsive */
	@media (max-width: 640px) {
		.paper-layout {
			padding: var(--space-6) var(--space-4);
		}

		.paper-header__actions {
			flex-direction: column;
		}

		.btn {
			width: 100%;
			justify-content: center;
		}
	}
</style>
