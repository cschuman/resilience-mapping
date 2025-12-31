<script lang="ts">
	import { page } from '$app/stores';

	interface Props {
		variant?: 'default' | 'minimal';
	}

	let { variant = 'default' }: Props = $props();

	let mobileMenuOpen = $state(false);

	const navLinks = [
		{ href: '/', label: 'Home' },
		{ href: '/map', label: 'Map' },
		{ href: '/data', label: 'Data' },
		{ href: '/research', label: 'Research' },
		{ href: '/about', label: 'About' }
	];

	function toggleMobileMenu() {
		mobileMenuOpen = !mobileMenuOpen;
	}

	function closeMobileMenu() {
		mobileMenuOpen = false;
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape' && mobileMenuOpen) {
			closeMobileMenu();
		}
	}

	function isActive(href: string, currentPath: string): boolean {
		if (href === '/') {
			return currentPath === '/';
		}
		return currentPath.startsWith(href);
	}
</script>

<svelte:window onkeydown={handleKeydown} />

<nav class="nav" class:nav--minimal={variant === 'minimal'} aria-label="Main navigation">
	<div class="nav__container">
		<!-- Logo/Brand -->
		<a href="/" class="nav__brand" onclick={closeMobileMenu}>
			<span class="nav__brand-mark" aria-hidden="true">R</span>
			{#if variant === 'default'}
				<span class="nav__brand-text">Resilience</span>
			{/if}
		</a>

		<!-- Desktop Navigation -->
		<div class="nav__links">
			{#each navLinks as link}
				<a
					href={link.href}
					class="nav__link"
					class:nav__link--active={isActive(link.href, $page.url.pathname)}
					aria-current={isActive(link.href, $page.url.pathname) ? 'page' : undefined}
				>
					{link.label}
				</a>
			{/each}
			<a href="/api/stats" class="nav__link nav__link--api">API</a>
		</div>

		<!-- Mobile Menu Button -->
		<button
			type="button"
			class="nav__mobile-toggle"
			onclick={toggleMobileMenu}
			aria-expanded={mobileMenuOpen}
			aria-controls="mobile-menu"
			aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
		>
			<span class="nav__hamburger" class:nav__hamburger--open={mobileMenuOpen}>
				<span></span>
				<span></span>
				<span></span>
			</span>
		</button>
	</div>

	<!-- Mobile Menu -->
	{#if mobileMenuOpen}
		<div
			id="mobile-menu"
			class="nav__mobile-menu"
			role="dialog"
			aria-modal="true"
			aria-label="Navigation menu"
		>
			<div class="nav__mobile-links">
				{#each navLinks as link}
					<a
						href={link.href}
						class="nav__mobile-link"
						class:nav__mobile-link--active={isActive(link.href, $page.url.pathname)}
						onclick={closeMobileMenu}
						aria-current={isActive(link.href, $page.url.pathname) ? 'page' : undefined}
					>
						{link.label}
					</a>
				{/each}
				<a href="/api/stats" class="nav__mobile-link nav__mobile-link--api" onclick={closeMobileMenu}>
					API Documentation
				</a>
			</div>
		</div>
	{/if}
</nav>

<style>
	.nav {
		position: sticky;
		top: 0;
		z-index: var(--z-sticky, 200);
		background: var(--color-foundation-deep);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.nav--minimal {
		background: rgba(18, 24, 38, 0.92);
		backdrop-filter: blur(12px);
		-webkit-backdrop-filter: blur(12px);
	}

	.nav__container {
		display: flex;
		align-items: center;
		justify-content: space-between;
		max-width: var(--container-xl);
		margin: 0 auto;
		padding: var(--space-3) var(--space-6);
	}

	.nav__brand {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		text-decoration: none;
		transition: opacity var(--duration-fast) var(--ease-out);
	}

	.nav__brand:hover {
		opacity: 0.8;
	}

	.nav__brand-mark {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 32px;
		height: 32px;
		background: var(--color-accent-primary);
		color: white;
		font-family: var(--font-display);
		font-size: var(--text-lg);
		font-weight: var(--font-weight-normal);
		border-radius: var(--radius-md);
	}

	.nav__brand-text {
		display: none;
		font-family: var(--font-display);
		font-size: var(--text-xl);
		color: var(--color-text-primary);
		letter-spacing: var(--tracking-tight);
	}

	@media (min-width: 640px) {
		.nav__brand-text {
			display: inline;
		}
	}

	.nav__links {
		display: none;
		align-items: center;
		gap: var(--space-1);
	}

	@media (min-width: 768px) {
		.nav__links {
			display: flex;
		}
	}

	.nav__link {
		padding: var(--space-2) var(--space-4);
		color: var(--color-text-tertiary);
		text-decoration: none;
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
		border-radius: var(--radius-md);
		transition: all var(--duration-fast) var(--ease-out);
	}

	.nav__link:hover {
		color: var(--color-text-primary);
		background: var(--color-foundation-surface);
	}

	.nav__link--active {
		color: var(--color-accent-primary);
		background: var(--color-accent-primary-subtle);
	}

	.nav__link--active:hover {
		color: var(--color-accent-primary);
		background: var(--color-accent-primary-glow);
	}

	.nav__link--api {
		margin-left: var(--space-2);
		padding: var(--space-2) var(--space-3);
		color: var(--color-accent-primary);
		border: 1px solid var(--color-accent-primary);
		border-radius: var(--radius-md);
		font-size: var(--text-xs);
		font-weight: var(--font-weight-semibold);
		letter-spacing: var(--tracking-wide);
		text-transform: uppercase;
	}

	.nav__link--api:hover {
		background: var(--color-accent-primary-subtle);
	}

	/* Hamburger Menu */
	.nav__mobile-toggle {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 44px;
		height: 44px;
		background: transparent;
		border: none;
		border-radius: var(--radius-md);
		cursor: pointer;
		transition: background var(--duration-fast) var(--ease-out);
	}

	.nav__mobile-toggle:hover {
		background: var(--color-foundation-surface);
	}

	@media (min-width: 768px) {
		.nav__mobile-toggle {
			display: none;
		}
	}

	.nav__hamburger {
		position: relative;
		width: 20px;
		height: 14px;
	}

	.nav__hamburger span {
		position: absolute;
		left: 0;
		width: 100%;
		height: 2px;
		background: var(--color-text-secondary);
		border-radius: 1px;
		transition: all var(--duration-normal) var(--ease-spring);
	}

	.nav__hamburger span:nth-child(1) {
		top: 0;
	}

	.nav__hamburger span:nth-child(2) {
		top: 6px;
	}

	.nav__hamburger span:nth-child(3) {
		top: 12px;
	}

	.nav__hamburger--open span:nth-child(1) {
		top: 6px;
		transform: rotate(45deg);
	}

	.nav__hamburger--open span:nth-child(2) {
		opacity: 0;
		transform: translateX(-8px);
	}

	.nav__hamburger--open span:nth-child(3) {
		top: 6px;
		transform: rotate(-45deg);
	}

	/* Mobile Menu */
	.nav__mobile-menu {
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		background: var(--color-foundation-deep);
		border-bottom: 1px solid var(--color-border-subtle);
		padding: var(--space-2);
		animation: slideDown var(--duration-normal) var(--ease-spring);
	}

	@keyframes slideDown {
		from {
			opacity: 0;
			transform: translateY(-8px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.nav__mobile-links {
		display: flex;
		flex-direction: column;
		gap: var(--space-1);
	}

	.nav__mobile-link {
		display: block;
		padding: var(--space-4);
		color: var(--color-text-secondary);
		text-decoration: none;
		font-size: var(--text-base);
		font-weight: var(--font-weight-medium);
		border-radius: var(--radius-lg);
		transition: all var(--duration-fast) var(--ease-out);
	}

	.nav__mobile-link:hover {
		background: var(--color-foundation-surface);
		color: var(--color-text-primary);
	}

	.nav__mobile-link--active {
		color: var(--color-accent-primary);
		background: var(--color-accent-primary-subtle);
	}

	.nav__mobile-link--api {
		margin-top: var(--space-2);
		padding-top: var(--space-4);
		border-top: 1px solid var(--color-border-subtle);
		color: var(--color-accent-primary);
	}
</style>
