<script lang="ts">
	/**
	 * Community Stories Page
	 *
	 * Showcases real-world examples of community resilience,
	 * demonstrating how data-driven insights can inform
	 * positive community development.
	 */

	interface Story {
		id: string;
		title: string;
		location: string;
		tractFips: string;
		summary: string;
		category: 'health' | 'food-access' | 'community' | 'economic';
		imageUrl?: string;
	}

	// Sample stories - in production these would come from a CMS or database
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

	const categoryLabels: Record<Story['category'], string> = {
		health: 'Health',
		'food-access': 'Food Access',
		community: 'Community',
		economic: 'Economic'
	};

	const categoryColors: Record<Story['category'], string> = {
		health: '#10b981', // emerald-500
		'food-access': '#f59e0b', // amber-500
		community: '#8b5cf6', // violet-500
		economic: '#3b82f6' // blue-500
	};
</script>

<svelte:head>
	<title>Community Stories | Community Resilience Mapping</title>
	<meta
		name="description"
		content="Real stories of community resilience from across the United States. Learn how communities are overcoming challenges and building healthier futures."
	/>
</svelte:head>

<div class="stories-page">
	<header class="header">
		<a href="/" class="back-link" aria-label="Back to home">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 20 20"
				fill="currentColor"
				class="back-icon"
				aria-hidden="true"
			>
				<path
					fill-rule="evenodd"
					d="M17 10a.75.75 0 01-.75.75H5.612l4.158 3.96a.75.75 0 11-1.04 1.08l-5.5-5.25a.75.75 0 010-1.08l5.5-5.25a.75.75 0 111.04 1.08L5.612 9.25H16.25A.75.75 0 0117 10z"
					clip-rule="evenodd"
				/>
			</svg>
			<span>Back</span>
		</a>
	</header>

	<main id="main-content" class="content">
		<section class="hero">
			<h1 class="hero-title">Community Stories</h1>
			<p class="hero-subtitle">
				Real examples of resilience from communities across America. These stories highlight how
				neighborhoods with similar challenges have found innovative solutions to improve health,
				food access, and quality of life.
			</p>
		</section>

		<section class="stories-grid" aria-label="Community stories">
			{#each stories as story}
				<article class="story-card">
					<div class="story-header">
						<span
							class="story-category"
							style="background-color: {categoryColors[story.category]}20; color: {categoryColors[
								story.category
							]}"
						>
							{categoryLabels[story.category]}
						</span>
						<span class="story-location">{story.location}</span>
					</div>
					<h2 class="story-title">{story.title}</h2>
					<p class="story-summary">{story.summary}</p>
					<footer class="story-footer">
						<a href="/map?tract={story.tractFips}" class="story-link">
							View on map
							<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 20 20"
								fill="currentColor"
								class="link-icon"
								aria-hidden="true"
							>
								<path
									fill-rule="evenodd"
									d="M3 10a.75.75 0 01.75-.75h10.638L10.23 5.29a.75.75 0 111.04-1.08l5.5 5.25a.75.75 0 010 1.08l-5.5 5.25a.75.75 0 11-1.04-1.08l4.158-3.96H3.75A.75.75 0 013 10z"
									clip-rule="evenodd"
								/>
							</svg>
						</a>
					</footer>
				</article>
			{/each}
		</section>

		<section class="cta-section">
			<h2 class="cta-title">Share Your Story</h2>
			<p class="cta-text">
				Does your community have a resilience success story? We'd love to hear about initiatives
				that are making a difference in your neighborhood.
			</p>
			<a href="mailto:stories@resilience-mapping.org" class="cta-button">
				Submit a Story
			</a>
		</section>
	</main>

	<footer class="page-footer">
		<p>
			<a href="/about">About the methodology</a>
			<span class="separator" aria-hidden="true">|</span>
			<a href="/map">Explore the map</a>
		</p>
	</footer>
</div>

<style>
	.stories-page {
		min-height: 100vh;
		background: linear-gradient(to bottom, #0f172a, #1e293b);
		color: white;
	}

	.header {
		padding: 1.5rem 2rem;
		max-width: 1200px;
		margin: 0 auto;
	}

	.back-link {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		color: #94a3b8;
		text-decoration: none;
		font-size: 0.875rem;
		transition: color 0.15s ease;
	}

	.back-link:hover {
		color: white;
	}

	.back-icon {
		width: 1.25rem;
		height: 1.25rem;
	}

	.content {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 2rem 4rem;
	}

	.hero {
		text-align: center;
		margin-bottom: 3rem;
	}

	.hero-title {
		font-size: 2.5rem;
		font-weight: 700;
		margin: 0 0 1rem;
		background: linear-gradient(135deg, #10b981, #34d399);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.hero-subtitle {
		font-size: 1.125rem;
		color: #94a3b8;
		max-width: 600px;
		margin: 0 auto;
		line-height: 1.6;
	}

	.stories-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		gap: 1.5rem;
		margin-bottom: 4rem;
	}

	.story-card {
		background: rgba(30, 41, 59, 0.8);
		border: 1px solid #334155;
		border-radius: 12px;
		padding: 1.5rem;
		display: flex;
		flex-direction: column;
		transition: all 0.2s ease;
	}

	.story-card:hover {
		transform: translateY(-4px);
		border-color: #475569;
		box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
	}

	.story-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1rem;
	}

	.story-category {
		font-size: 0.75rem;
		font-weight: 600;
		padding: 0.25rem 0.75rem;
		border-radius: 9999px;
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.story-location {
		font-size: 0.75rem;
		color: #64748b;
	}

	.story-title {
		font-size: 1.25rem;
		font-weight: 600;
		margin: 0 0 0.75rem;
		color: white;
		line-height: 1.4;
	}

	.story-summary {
		font-size: 0.875rem;
		color: #94a3b8;
		line-height: 1.6;
		margin: 0;
		flex: 1;
	}

	.story-footer {
		margin-top: 1.5rem;
		padding-top: 1rem;
		border-top: 1px solid #334155;
	}

	.story-link {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		color: #10b981;
		text-decoration: none;
		font-size: 0.875rem;
		font-weight: 500;
		transition: gap 0.15s ease;
	}

	.story-link:hover {
		gap: 0.75rem;
	}

	.link-icon {
		width: 1rem;
		height: 1rem;
	}

	.cta-section {
		text-align: center;
		background: rgba(16, 185, 129, 0.1);
		border: 1px solid rgba(16, 185, 129, 0.2);
		border-radius: 16px;
		padding: 3rem 2rem;
	}

	.cta-title {
		font-size: 1.5rem;
		font-weight: 600;
		margin: 0 0 0.75rem;
		color: white;
	}

	.cta-text {
		color: #94a3b8;
		margin: 0 0 1.5rem;
		max-width: 500px;
		margin-left: auto;
		margin-right: auto;
	}

	.cta-button {
		display: inline-block;
		background: #10b981;
		color: white;
		text-decoration: none;
		padding: 0.75rem 1.5rem;
		border-radius: 8px;
		font-weight: 600;
		transition: all 0.15s ease;
	}

	.cta-button:hover {
		background: #059669;
		transform: translateY(-2px);
	}

	.page-footer {
		padding: 2rem;
		text-align: center;
		border-top: 1px solid #334155;
	}

	.page-footer p {
		margin: 0;
		color: #64748b;
		font-size: 0.875rem;
	}

	.page-footer a {
		color: #94a3b8;
		text-decoration: none;
		transition: color 0.15s ease;
	}

	.page-footer a:hover {
		color: #10b981;
	}

	.separator {
		margin: 0 1rem;
	}

	/* Responsive adjustments */
	@media (max-width: 640px) {
		.header {
			padding: 1rem;
		}

		.content {
			padding: 0 1rem 3rem;
		}

		.hero-title {
			font-size: 1.75rem;
		}

		.hero-subtitle {
			font-size: 1rem;
		}

		.stories-grid {
			grid-template-columns: 1fr;
		}

		.cta-section {
			padding: 2rem 1rem;
		}
	}
</style>
