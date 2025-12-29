<script lang="ts">
	import { Navigation, Footer } from '$lib/components/layout';

	let { children } = $props();
</script>

<div class="standard-layout">
	<Navigation />

	<main id="main-content" class="standard-layout__content">
		{@render children()}
	</main>

	<Footer />
</div>

<style>
	.standard-layout {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		background: linear-gradient(to bottom, #0C0A08, #1C1410);
	}

	.standard-layout__content {
		flex: 1;
	}
</style>
