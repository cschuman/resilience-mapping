<script lang="ts">
	import { updateUrlParams } from '$lib/utils';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	type Category = 'health' | 'food-access' | 'community' | 'economic';

	interface Story {
		id: string;
		title: string;
		location: string;
		tractFips: string;
		summary: string;
		category: Category;
	}

	// Active filter from URL or 'all'
	let activeFilter = $derived<Category | 'all'>(
		(data.category as Category | undefined) || 'all'
	);

	// Stories data
	const stories: Story[] = [
		{
			id: '1',
			title: 'Urban Garden Network Transforms Food Desert',
			location: 'Detroit, MI',
			tractFips: '26163523900',
			summary:
				'A coalition of neighborhood associations converted vacant lots into productive community gardens, increasing fresh produce access for over 5,000 residents and creating a model for other low-income areas.',
			category: 'food-access'
		},
		{
			id: '2',
			title: 'Community Health Workers Bridge the Gap',
			location: 'El Paso, TX',
			tractFips: '48141003701',
			summary:
				'Promotoras (community health workers) reduced diabetes hospitalizations by 32% through culturally-appropriate education and peer support networks, proving that community-led health initiatives can outperform traditional interventions.',
			category: 'health'
		},
		{
			id: '3',
			title: 'Mutual Aid Network Responds to Crisis',
			location: 'Brooklyn, NY',
			tractFips: '36047036300',
			summary:
				'When formal systems failed during the pandemic, a grassroots mutual aid network delivered 50,000+ meals and connected isolated seniors to essential services, demonstrating the power of neighbor-to-neighbor care.',
			category: 'community'
		},
		{
			id: '4',
			title: 'Worker Cooperative Creates Local Wealth',
			location: 'Cleveland, OH',
			tractFips: '39035101800',
			summary:
				'An employee-owned laundry cooperative provides living wages and ownership opportunities in a historically disinvested neighborhood, keeping wealth circulating locally and building economic resilience.',
			category: 'economic'
		}
	];

	const categoryConfig: Record<Category, { label: string; color: string }> = {
		health: { label: 'Health', color: 'var(--color-score-very-high)' },
		'food-access': { label: 'Food Access', color: 'var(--color-accent-secondary)' },
		community: { label: 'Community', color: 'var(--color-accent-primary)' },
		economic: { label: 'Economic', color: 'var(--color-success)' }
	};

	const filterOptions: Array<{ value: Category | 'all'; label: string }> = [
		{ value: 'all', label: 'All' },
		{ value: 'health', label: 'Health' },
		{ value: 'food-access', label: 'Food Access' },
		{ value: 'community', label: 'Community' },
		{ value: 'economic', label: 'Economic' }
	];

	// Filtered stories
	let filteredStories = $derived(
		activeFilter === 'all'
			? stories
			: stories.filter((story) => story.category === activeFilter)
	);

	function setFilter(category: Category | 'all'): void {
		updateUrlParams({
			category: category === 'all' ? null : category
		});
	}
</script>

<svelte:head>
	<title>Community Stories | Community Resilience Mapping</title>
	<meta
		name="description"
		content="Real stories of community resilience from across the United States."
	/>
</svelte:head>

<div class="stories-page">
	<div class="container">
		<!-- Header -->
		<header class="header">
			<p class="header__eyebrow">Real Impact</p>
			<h1 class="header__title">Community Stories</h1>
			<p class="header__subtitle">
				Real examples of resilience from communities across America.
				Discover how neighborhoods are finding innovative solutions.
			</p>
		</header>

		<!-- Filters -->
		<nav class="filters" aria-label="Filter stories by category">
			{#each filterOptions as option}
				<button
					type="button"
					class="filter"
					class:filter--active={activeFilter === option.value}
					onclick={() => setFilter(option.value)}
					aria-pressed={activeFilter === option.value}
				>
					{option.label}
				</button>
			{/each}
		</nav>

		<!-- Stories Grid -->
		<section class="grid" aria-label="Community stories">
			{#if filteredStories.length === 0}
				<div class="empty">
					<p>No stories found for this category.</p>
					<button type="button" class="filter filter--active" onclick={() => setFilter('all')}>
						View All Stories
					</button>
				</div>
			{/if}
			{#each filteredStories as story}
				<article class="story">
					<div class="story__header">
						<span
							class="story__category"
							style="--category-color: {categoryConfig[story.category].color}"
						>
							{categoryConfig[story.category].label}
						</span>
						<span class="story__location">{story.location}</span>
					</div>
					<h2 class="story__title">{story.title}</h2>
					<p class="story__summary">{story.summary}</p>
					<footer class="story__footer">
						<a href="/map?tract={story.tractFips}" class="story__link">
							<span>View on map</span>
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
								<path fill-rule="evenodd" d="M3 10a.75.75 0 01.75-.75h10.638L10.23 5.29a.75.75 0 111.04-1.08l5.5 5.25a.75.75 0 010 1.08l-5.5 5.25a.75.75 0 11-1.04-1.08l4.158-3.96H3.75A.75.75 0 013 10z" clip-rule="evenodd" />
							</svg>
						</a>
					</footer>
				</article>
			{/each}
		</section>

		<!-- CTA -->
		<section class="cta">
			<h2 class="cta__title">Share Your Story</h2>
			<p class="cta__text">
				Does your community have a resilience success story?
				We'd love to hear about initiatives making a difference.
			</p>
			<a href="mailto:stories@resilience-mapping.org" class="cta__button">
				Submit a Story
			</a>
		</section>
	</div>
</div>

<style>
	.stories-page {
		color: var(--color-text-primary);
	}

	.container {
		max-width: var(--container-lg);
		margin: 0 auto;
		padding: var(--space-8) var(--space-6) var(--space-16);
	}

	/* Header */
	.header {
		text-align: center;
		margin-bottom: var(--space-10);
	}

	.header__eyebrow {
		font-size: var(--text-xs);
		font-weight: var(--font-weight-semibold);
		color: var(--color-accent-secondary);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		margin-bottom: var(--space-3);
	}

	.header__title {
		font-family: var(--font-display);
		font-size: var(--text-4xl);
		color: var(--color-text-primary);
		margin-bottom: var(--space-4);
	}

	.header__subtitle {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
		max-width: 520px;
		margin: 0 auto;
		line-height: var(--leading-relaxed);
	}

	/* Filters */
	.filters {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: var(--space-2);
		margin-bottom: var(--space-10);
	}

	.filter {
		padding: var(--space-2) var(--space-4);
		border: 1px solid var(--color-border-default);
		border-radius: var(--radius-full);
		background: transparent;
		color: var(--color-text-tertiary);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		cursor: pointer;
		transition: all var(--duration-fast) var(--ease-out);
	}

	.filter:hover {
		border-color: var(--color-border-strong);
		color: var(--color-text-primary);
	}

	.filter--active {
		background: var(--color-accent-primary);
		border-color: var(--color-accent-primary);
		color: white;
	}

	.filter--active:hover {
		background: var(--color-accent-primary-hover);
		border-color: var(--color-accent-primary-hover);
	}

	/* Empty State */
	.empty {
		grid-column: 1 / -1;
		text-align: center;
		padding: var(--space-12);
		color: var(--color-text-muted);
	}

	.empty p {
		margin-bottom: var(--space-4);
	}

	/* Grid */
	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		gap: var(--space-6);
		margin-bottom: var(--space-16);
	}

	/* Story Card */
	.story {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
		display: flex;
		flex-direction: column;
		transition: all var(--duration-normal) var(--ease-out);
	}

	.story:hover {
		border-color: var(--color-border-strong);
		box-shadow: var(--shadow-lg);
	}

	.story__header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--space-4);
	}

	.story__category {
		font-size: var(--text-xs);
		font-weight: var(--font-weight-semibold);
		padding: var(--space-1) var(--space-3);
		border-radius: var(--radius-full);
		text-transform: uppercase;
		letter-spacing: var(--tracking-wide);
		background: color-mix(in srgb, var(--category-color) 15%, transparent);
		color: var(--category-color);
	}

	.story__location {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.story__title {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		color: var(--color-text-primary);
		margin-bottom: var(--space-3);
		line-height: var(--leading-snug);
	}

	.story__summary {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		flex: 1;
	}

	.story__footer {
		margin-top: var(--space-5);
		padding-top: var(--space-4);
		border-top: 1px solid var(--color-border-subtle);
	}

	.story__link {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		color: var(--color-accent-primary);
		text-decoration: none;
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
	}

	.story__link svg {
		width: 16px;
		height: 16px;
		transition: transform var(--duration-fast) var(--ease-spring);
	}

	.story__link:hover svg {
		transform: translateX(4px);
	}

	/* CTA */
	.cta {
		text-align: center;
		background: var(--color-accent-primary-subtle);
		border: 1px solid var(--color-accent-primary-glow);
		border-radius: var(--radius-2xl);
		padding: var(--space-12) var(--space-8);
	}

	.cta__title {
		font-family: var(--font-display);
		font-size: var(--text-2xl);
		color: var(--color-text-primary);
		margin-bottom: var(--space-3);
	}

	.cta__text {
		color: var(--color-text-secondary);
		max-width: 400px;
		margin: 0 auto var(--space-6);
	}

	.cta__button {
		display: inline-block;
		background: var(--color-accent-primary);
		color: white;
		text-decoration: none;
		padding: var(--space-3) var(--space-6);
		border-radius: var(--radius-lg);
		font-weight: var(--font-weight-semibold);
		font-size: var(--text-sm);
		transition: all var(--duration-fast) var(--ease-out);
	}

	.cta__button:hover {
		background: var(--color-accent-primary-hover);
		box-shadow: var(--shadow-glow-accent);
	}

	/* Responsive */
	@media (max-width: 640px) {
		.container {
			padding: var(--space-6) var(--space-4) var(--space-12);
		}

		.header__title {
			font-size: var(--text-3xl);
		}

		.header__subtitle {
			font-size: var(--text-base);
		}

		.grid {
			grid-template-columns: 1fr;
		}

		.cta {
			padding: var(--space-8) var(--space-4);
		}
	}
</style>
