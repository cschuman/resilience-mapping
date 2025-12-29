<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<meta name="theme-color" content="#0f172a" />
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
