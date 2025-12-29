<script lang="ts">
	interface Props {
		variant?: 'minimal' | 'full';
	}

	let { variant = 'full' }: Props = $props();
</script>

<footer class="footer" class:footer--minimal={variant === 'minimal'}>
	<div class="footer__container">
		{#if variant === 'full'}
			<div class="footer__content">
				<div class="footer__brand">
					<span class="footer__mark" aria-hidden="true">R</span>
					<div class="footer__brand-text">
						<span class="footer__name">Resilience Mapping</span>
						<span class="footer__tagline">Data for community insight</span>
					</div>
				</div>

				<div class="footer__grid">
					<div class="footer__section">
						<h3 class="footer__heading">Explore</h3>
						<nav class="footer__nav" aria-label="Explore links">
							<a href="/map">Interactive Map</a>
							<a href="/stories">Community Stories</a>
							<a href="/about">Methodology</a>
						</nav>
					</div>

					<div class="footer__section">
						<h3 class="footer__heading">Data</h3>
						<nav class="footer__nav" aria-label="Data links">
							<a href="/api/stats">API Statistics</a>
							<a href="/api/tracts?limit=10">Census Tracts</a>
							<a href="/about#api-heading">API Documentation</a>
						</nav>
					</div>

					<div class="footer__section">
						<h3 class="footer__heading">Sources</h3>
						<nav class="footer__nav" aria-label="Data source links">
							<a href="https://www.cdc.gov/places" target="_blank" rel="noopener">CDC PLACES</a>
							<a href="https://www.ers.usda.gov/data-products/food-access-research-atlas/" target="_blank" rel="noopener">USDA Food Access</a>
							<a href="https://www.census.gov/programs-surveys/acs" target="_blank" rel="noopener">Census ACS</a>
						</nav>
					</div>
				</div>
			</div>
		{/if}

		<div class="footer__bottom">
			<p class="footer__copyright">
				Community Resilience Mapping
			</p>
			<nav class="footer__links" aria-label="Footer links">
				<a href="/">Home</a>
				<a href="/map">Map</a>
				<a href="/about">About</a>
			</nav>
		</div>
	</div>
</footer>

<style>
	.footer {
		background: var(--color-foundation-deepest);
		border-top: 1px solid var(--color-border-subtle);
		padding: var(--space-12) var(--space-6) var(--space-8);
	}

	.footer--minimal {
		padding: var(--space-6);
	}

	.footer__container {
		max-width: var(--container-xl);
		margin: 0 auto;
	}

	.footer__content {
		display: flex;
		flex-direction: column;
		gap: var(--space-8);
		margin-bottom: var(--space-8);
		padding-bottom: var(--space-8);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	@media (min-width: 768px) {
		.footer__content {
			flex-direction: row;
			align-items: flex-start;
			gap: var(--space-12);
		}
	}

	.footer__brand {
		display: flex;
		align-items: flex-start;
		gap: var(--space-3);
	}

	.footer__mark {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 40px;
		height: 40px;
		background: var(--color-accent-primary);
		color: white;
		font-family: var(--font-display);
		font-size: var(--text-xl);
		border-radius: var(--radius-md);
		flex-shrink: 0;
	}

	.footer__brand-text {
		display: flex;
		flex-direction: column;
		gap: var(--space-1);
	}

	.footer__name {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		color: var(--color-text-primary);
		letter-spacing: var(--tracking-tight);
	}

	.footer__tagline {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
	}

	.footer__grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
		gap: var(--space-8);
	}

	@media (min-width: 768px) {
		.footer__grid {
			gap: var(--space-12);
		}
	}

	.footer__section {
		display: flex;
		flex-direction: column;
		gap: var(--space-3);
	}

	.footer__heading {
		font-family: var(--font-body);
		font-size: var(--text-xs);
		font-weight: var(--font-weight-semibold);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		color: var(--color-text-muted);
		margin: 0;
	}

	.footer__nav {
		display: flex;
		flex-direction: column;
		gap: var(--space-2);
	}

	.footer__nav a {
		color: var(--color-text-tertiary);
		text-decoration: none;
		font-size: var(--text-sm);
		transition: color var(--duration-fast) var(--ease-out);
	}

	.footer__nav a:hover {
		color: var(--color-accent-primary);
	}

	.footer__bottom {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--space-4);
		text-align: center;
	}

	@media (min-width: 640px) {
		.footer__bottom {
			flex-direction: row;
			justify-content: space-between;
		}
	}

	.footer__copyright {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		margin: 0;
	}

	.footer__links {
		display: flex;
		align-items: center;
		gap: var(--space-6);
		font-size: var(--text-sm);
	}

	.footer__links a {
		color: var(--color-text-tertiary);
		text-decoration: none;
		transition: color var(--duration-fast) var(--ease-out);
	}

	.footer__links a:hover {
		color: var(--color-accent-primary);
	}
</style>
