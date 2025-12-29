<script lang="ts">
	/**
	 * Map Layout
	 *
	 * Full-screen layout for the interactive map.
	 * Provides minimal chrome to maximize map real estate.
	 */
	let { children } = $props();
</script>

<div class="map-layout">
	{@render children()}
</div>

<style>
	.map-layout {
		height: 100vh;
		width: 100vw;
		overflow: hidden;
		background: #0C0A08;
	}
</style>
