<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { page } from '$app/stores';

	let { children } = $props();

	const siteTitle = 'Community Resilience Mapping';
	const siteDescription = 'Explore census tract-level community health resilience across the United States. Discover which neighborhoods thrive beyond what statistics predict.';
	const siteUrl = 'https://resilience-mapping.fly.dev';
</script>

<svelte:head>
	<!-- Favicon and theme -->
	<link rel="icon" href={favicon} />
	<meta name="theme-color" content="#0f172a" />

	<!-- Default SEO (can be overridden by individual pages) -->
	<meta name="description" content={siteDescription} />
	<meta name="author" content="Community Resilience Mapping Project" />

	<!-- Open Graph -->
	<meta property="og:type" content="website" />
	<meta property="og:site_name" content={siteTitle} />
	<meta property="og:title" content={siteTitle} />
	<meta property="og:description" content={siteDescription} />
	<meta property="og:url" content={siteUrl + $page.url.pathname} />
	<meta property="og:image" content="{siteUrl}/og-image.svg" />
	<meta property="og:image:type" content="image/svg+xml" />
	<meta property="og:image:width" content="1200" />
	<meta property="og:image:height" content="630" />
	<meta property="og:image:alt" content="Community Resilience Mapping - Explore health resilience patterns across US census tracts" />

	<!-- Twitter Card -->
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content={siteTitle} />
	<meta name="twitter:description" content={siteDescription} />
	<meta name="twitter:image" content="{siteUrl}/og-image.svg" />
	<meta name="twitter:image:alt" content="Community Resilience Mapping - Explore health resilience patterns across US census tracts" />

	<!-- Additional SEO -->
	<link rel="canonical" href={siteUrl + $page.url.pathname} />
	<meta name="robots" content="index, follow" />
	<meta name="googlebot" content="index, follow" />

	<!-- Structured data for Google -->
	{@html `<script type="application/ld+json">
	{
		"@context": "https://schema.org",
		"@type": "WebApplication",
		"name": "${siteTitle}",
		"url": "${siteUrl}",
		"description": "${siteDescription}",
		"applicationCategory": "DataVisualization",
		"operatingSystem": "Any",
		"offers": {
			"@type": "Offer",
			"price": "0",
			"priceCurrency": "USD"
		},
		"creator": {
			"@type": "Organization",
			"name": "Community Resilience Mapping Project"
		}
	}
	</script>`}
</svelte:head>

<!-- Skip link for keyboard navigation - appears on focus -->
<a href="#main-content" class="skip-link">
	Skip to main content
</a>

<!-- Live region for screen reader announcements -->
<div
	id="announcer"
	class="sr-only"
	role="status"
	aria-live="polite"
	aria-atomic="true"
></div>

{@render children()}

<style>
	.skip-link {
		position: fixed;
		top: -100%;
		left: 50%;
		transform: translateX(-50%);
		z-index: 9999;
		padding: 0.75rem 1.5rem;
		background: #10b981;
		color: white;
		font-weight: 600;
		text-decoration: none;
		border-radius: 0 0 8px 8px;
		transition: top 0.2s ease;
	}

	.skip-link:focus {
		top: 0;
		outline: none;
	}

	.sr-only {
		position: absolute;
		width: 1px;
		height: 1px;
		padding: 0;
		margin: -1px;
		overflow: hidden;
		clip: rect(0, 0, 0, 0);
		white-space: nowrap;
		border: 0;
	}
</style>
