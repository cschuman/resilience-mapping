<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	// State name lookup
	const STATE_NAMES: Record<string, string> = {
		AL: 'Alabama', AK: 'Alaska', AZ: 'Arizona', AR: 'Arkansas', CA: 'California',
		CO: 'Colorado', CT: 'Connecticut', DE: 'Delaware', DC: 'Washington DC', FL: 'Florida',
		GA: 'Georgia', HI: 'Hawaii', ID: 'Idaho', IL: 'Illinois', IN: 'Indiana',
		IA: 'Iowa', KS: 'Kansas', KY: 'Kentucky', LA: 'Louisiana', ME: 'Maine',
		MD: 'Maryland', MA: 'Massachusetts', MI: 'Michigan', MN: 'Minnesota', MS: 'Mississippi',
		MO: 'Missouri', MT: 'Montana', NE: 'Nebraska', NV: 'Nevada', NH: 'New Hampshire',
		NJ: 'New Jersey', NM: 'New Mexico', NY: 'New York', NC: 'North Carolina', ND: 'North Dakota',
		OH: 'Ohio', OK: 'Oklahoma', OR: 'Oregon', PA: 'Pennsylvania', RI: 'Rhode Island',
		SC: 'South Carolina', SD: 'South Dakota', TN: 'Tennessee', TX: 'Texas', UT: 'Utah',
		VT: 'Vermont', VA: 'Virginia', WA: 'Washington', WV: 'West Virginia', WI: 'Wisconsin',
		WY: 'Wyoming'
	};

	function formatScore(score: number): string {
		return score > 0 ? `+${score.toFixed(3)}` : score.toFixed(3);
	}
</script>

<svelte:head>
	<title>Special Populations | Community Resilience Mapping</title>
	<meta
		name="description"
		content="Analysis of health resilience in college towns, military bases, and correctional facilities. Discover the 4 standard deviation gap between education and incarceration."
	/>
</svelte:head>

<div class="special-populations">
	<div class="container">
		<!-- Header -->
		<header class="header">
			<nav class="breadcrumb" aria-label="Breadcrumb">
				<a href="/research">Research</a>
				<span aria-hidden="true">/</span>
				<span>Special Populations</span>
			</nav>
			<h1 class="header__title">Special Population Analysis</h1>
			<p class="header__subtitle">
				How institutional environments shape community health resilience:
				college towns, military bases, and correctional facilities.
			</p>
		</header>

		<!-- Key Finding Banner -->
		<section class="key-finding" aria-labelledby="key-finding-heading">
			<div class="key-finding__content">
				<h2 id="key-finding-heading" class="key-finding__title">The 4 Standard Deviation Gap</h2>
				<p class="key-finding__text">
					College communities average <strong class="positive">+{data.summary.college?.avgResilience.toFixed(2)}</strong> resilience
					while correctional communities average <strong class="negative">{data.summary.correctional?.avgResilience.toFixed(2)}</strong>.
					That's a <strong>{data.summary.resilienceGap.toFixed(2)} point gap</strong> &mdash;
					nearly 4 standard deviations separating education from incarceration.
				</p>
			</div>
		</section>

		<!-- Summary Cards -->
		<section class="summary" aria-labelledby="summary-heading">
			<h2 id="summary-heading" class="sr-only">Population Type Summary</h2>
			<div class="summary__grid">
				<!-- College -->
				{#if data.summary.college}
					<div class="summary-card summary-card--college">
						<div class="summary-card__icon">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
								<path d="M11.7 2.805a.75.75 0 01.6 0A60.65 60.65 0 0122.83 8.72a.75.75 0 01-.231 1.337 49.949 49.949 0 00-9.902 3.912l-.003.002-.34.18a.75.75 0 01-.707 0A50.009 50.009 0 007.5 12.174v-.224c0-.131.067-.248.172-.311a54.614 54.614 0 014.653-2.52.75.75 0 00-.65-1.352 56.129 56.129 0 00-4.78 2.589 1.858 1.858 0 00-.859 1.228 49.803 49.803 0 00-4.634-1.527.75.75 0 01-.231-1.337A60.653 60.653 0 0111.7 2.805z" />
								<path d="M13.06 15.473a48.45 48.45 0 017.666-3.282c.134 1.414.22 2.843.255 4.285a.75.75 0 01-.46.71 47.878 47.878 0 00-8.105 4.342.75.75 0 01-.832 0 47.877 47.877 0 00-8.104-4.342.75.75 0 01-.461-.71c.035-1.442.121-2.87.255-4.286A48.4 48.4 0 016 13.18v1.27a1.5 1.5 0 00-.14 2.508c-.09.38-.222.753-.397 1.11.452.213.901.434 1.346.661a6.729 6.729 0 00.551-1.608 1.5 1.5 0 00.14-2.67v-.645a48.549 48.549 0 013.44 1.668 2.25 2.25 0 002.12 0z" />
								<path d="M4.462 19.462c.42-.419.753-.89 1-1.394.453.213.902.434 1.347.661a6.743 6.743 0 01-1.286 1.794.75.75 0 11-1.06-1.06z" />
							</svg>
						</div>
						<h3 class="summary-card__title">College Communities</h3>
						<div class="summary-card__score positive">
							{formatScore(data.summary.college.avgResilience)}
						</div>
						<p class="summary-card__label">Average Resilience</p>
						<div class="summary-card__stats">
							<span>{data.summary.college.count} tracts</span>
							<span>{data.summary.college.population.toLocaleString()} people</span>
						</div>
					</div>
				{/if}

				<!-- Military -->
				{#if data.summary.military}
					<div class="summary-card summary-card--military">
						<div class="summary-card__icon">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
								<path fill-rule="evenodd" d="M12.963 2.286a.75.75 0 00-1.071-.136 9.742 9.742 0 00-3.539 6.177A7.547 7.547 0 016.648 6.61a.75.75 0 00-1.152-.082A9 9 0 1015.68 4.534a7.46 7.46 0 01-2.717-2.248zM15.75 14.25a3.75 3.75 0 11-7.313-1.172c.628.465 1.35.81 2.133 1a5.99 5.99 0 011.925-3.545 3.75 3.75 0 013.255 3.717z" clip-rule="evenodd" />
							</svg>
						</div>
						<h3 class="summary-card__title">Military Bases</h3>
						<div class="summary-card__score positive">
							{formatScore(data.summary.military.avgResilience)}
						</div>
						<p class="summary-card__label">Average Resilience</p>
						<div class="summary-card__stats">
							<span>{data.summary.military.count} tracts</span>
							<span>{data.summary.military.population.toLocaleString()} people</span>
						</div>
					</div>
				{/if}

				<!-- Correctional -->
				{#if data.summary.correctional}
					<div class="summary-card summary-card--correctional">
						<div class="summary-card__icon">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
								<path fill-rule="evenodd" d="M12 1.5a5.25 5.25 0 00-5.25 5.25v3a3 3 0 00-3 3v6.75a3 3 0 003 3h10.5a3 3 0 003-3v-6.75a3 3 0 00-3-3v-3c0-2.9-2.35-5.25-5.25-5.25zm3.75 8.25v-3a3.75 3.75 0 10-7.5 0v3h7.5z" clip-rule="evenodd" />
							</svg>
						</div>
						<h3 class="summary-card__title">Correctional Facilities</h3>
						<div class="summary-card__score negative">
							{formatScore(data.summary.correctional.avgResilience)}
						</div>
						<p class="summary-card__label">Average Resilience</p>
						<div class="summary-card__stats">
							<span>{data.summary.correctional.count} tracts</span>
							<span>{data.summary.correctional.population.toLocaleString()} people</span>
						</div>
					</div>
				{/if}
			</div>
		</section>

		<!-- College Tracts Detail -->
		<section class="detail-section" aria-labelledby="college-heading">
			<h2 id="college-heading" class="section-title">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
					<path d="M11.7 2.805a.75.75 0 01.6 0A60.65 60.65 0 0122.83 8.72a.75.75 0 01-.231 1.337 49.949 49.949 0 00-9.902 3.912l-.003.002-.34.18a.75.75 0 01-.707 0A50.009 50.009 0 007.5 12.174v-.224c0-.131.067-.248.172-.311a54.614 54.614 0 014.653-2.52.75.75 0 00-.65-1.352 56.129 56.129 0 00-4.78 2.589 1.858 1.858 0 00-.859 1.228 49.803 49.803 0 00-4.634-1.527.75.75 0 01-.231-1.337A60.653 60.653 0 0111.7 2.805z" />
				</svg>
				College Communities
			</h2>
			<p class="section-intro">
				Census tracts where 50%+ of the population lives in college dormitories.
				These communities show exceptional resilience, likely due to access to university healthcare,
				younger demographics, walkable infrastructure, and stable institutional employment.
			</p>
			{#if data.collegeTracts.length > 0}
				<div class="tract-table-wrapper">
					<table class="tract-table">
						<thead>
							<tr>
								<th>Location</th>
								<th>Population</th>
								<th>College %</th>
								<th>Resilience</th>
								<th>Burden</th>
							</tr>
						</thead>
						<tbody>
							{#each data.collegeTracts as tract}
								<tr>
									<td>
										<span class="tract-location">{tract.county}, {STATE_NAMES[tract.state] || tract.state}</span>
										<span class="tract-fips">{tract.fips}</span>
									</td>
									<td>{tract.population.toLocaleString()}</td>
									<td>{tract.collegePct}%</td>
									<td class="score positive">{formatScore(tract.resilience)}</td>
									<td class="score" class:negative={tract.burden > 0}>{formatScore(tract.burden)}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{:else}
				<p class="empty-state">No college-dominated tracts found.</p>
			{/if}
		</section>

		<!-- Military Tracts Detail -->
		<section class="detail-section" aria-labelledby="military-heading">
			<h2 id="military-heading" class="section-title">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
					<path fill-rule="evenodd" d="M12.963 2.286a.75.75 0 00-1.071-.136 9.742 9.742 0 00-3.539 6.177A7.547 7.547 0 016.648 6.61a.75.75 0 00-1.152-.082A9 9 0 1015.68 4.534a7.46 7.46 0 01-2.717-2.248zM15.75 14.25a3.75 3.75 0 11-7.313-1.172c.628.465 1.35.81 2.133 1a5.99 5.99 0 011.925-3.545 3.75 3.75 0 013.255 3.717z" clip-rule="evenodd" />
				</svg>
				Military Bases
			</h2>
			<p class="section-intro">
				Census tracts where 25%+ of the population lives in military quarters.
				These communities benefit from VA healthcare access, stable employment,
				strong social cohesion, and institutional support systems.
			</p>
			{#if data.militaryTracts.length > 0}
				<div class="tract-table-wrapper">
					<table class="tract-table">
						<thead>
							<tr>
								<th>Location</th>
								<th>Population</th>
								<th>Military %</th>
								<th>Resilience</th>
								<th>Burden</th>
							</tr>
						</thead>
						<tbody>
							{#each data.militaryTracts as tract}
								<tr>
									<td>
										<span class="tract-location">{tract.county}, {STATE_NAMES[tract.state] || tract.state}</span>
										<span class="tract-fips">{tract.fips}</span>
									</td>
									<td>{tract.population.toLocaleString()}</td>
									<td>{tract.militaryPct}%</td>
									<td class="score" class:positive={tract.resilience > 0} class:negative={tract.resilience < 0}>{formatScore(tract.resilience)}</td>
									<td class="score" class:negative={tract.burden > 0}>{formatScore(tract.burden)}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{:else}
				<p class="empty-state">No military-dominated tracts found.</p>
			{/if}
		</section>

		<!-- Correctional Tracts Detail -->
		<section class="detail-section" aria-labelledby="correctional-heading">
			<h2 id="correctional-heading" class="section-title">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
					<path fill-rule="evenodd" d="M12 1.5a5.25 5.25 0 00-5.25 5.25v3a3 3 0 00-3 3v6.75a3 3 0 003 3h10.5a3 3 0 003-3v-6.75a3 3 0 00-3-3v-3c0-2.9-2.35-5.25-5.25-5.25zm3.75 8.25v-3a3.75 3.75 0 10-7.5 0v3h7.5z" clip-rule="evenodd" />
				</svg>
				Correctional Facilities
			</h2>
			<p class="section-intro">
				Census tracts where 25%+ of the population is in correctional facilities.
				These communities face significant health burdens, with limited healthcare access,
				high chronic disease rates, and compounding socioeconomic challenges for surrounding areas.
			</p>
			{#if data.correctionalTracts.length > 0}
				<div class="tract-table-wrapper">
					<table class="tract-table">
						<thead>
							<tr>
								<th>Location</th>
								<th>Population</th>
								<th>Correctional %</th>
								<th>Resilience</th>
								<th>Burden</th>
							</tr>
						</thead>
						<tbody>
							{#each data.correctionalTracts as tract}
								<tr>
									<td>
										<span class="tract-location">{tract.county}, {STATE_NAMES[tract.state] || tract.state}</span>
										<span class="tract-fips">{tract.fips}</span>
									</td>
									<td>{tract.population.toLocaleString()}</td>
									<td>{tract.correctionalPct}%</td>
									<td class="score" class:positive={tract.resilience > 0} class:negative={tract.resilience < 0}>{formatScore(tract.resilience)}</td>
									<td class="score negative">{formatScore(tract.burden)}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{:else}
				<p class="empty-state">No correctional-dominated tracts found.</p>
			{/if}
		</section>

		<!-- Research Implications -->
		<section class="implications" aria-labelledby="implications-heading">
			<h2 id="implications-heading" class="section-title">Research Implications</h2>
			<div class="implications__grid">
				<div class="implication">
					<h3>The Education Effect</h3>
					<p>
						College towns demonstrate that concentrated educational infrastructure,
						healthcare access, and younger demographics create measurable health advantages.
						This effect may extend to surrounding communities through economic spillovers.
					</p>
				</div>
				<div class="implication">
					<h3>Military Model</h3>
					<p>
						Military bases show that co-located healthcare (VA hospitals), stable employment,
						and strong social infrastructure can produce high resilience even in otherwise
						challenging geographic areas.
					</p>
				</div>
				<div class="implication">
					<h3>Carceral Burden</h3>
					<p>
						Prison communities represent concentrated health vulnerability.
						The nearly 4 standard deviation gap with college communities
						raises questions about resource allocation and public health priorities.
					</p>
				</div>
			</div>
		</section>

		<!-- Back Link -->
		<nav class="back-nav" aria-label="Back navigation">
			<a href="/research" class="back-link">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
					<path fill-rule="evenodd" d="M17 10a.75.75 0 01-.75.75H5.612l4.158 3.96a.75.75 0 11-1.04 1.08l-5.5-5.25a.75.75 0 010-1.08l5.5-5.25a.75.75 0 111.04 1.08L5.612 9.25H16.25A.75.75 0 0117 10z" clip-rule="evenodd" />
				</svg>
				Back to Research
			</a>
		</nav>
	</div>
</div>

<style>
	.special-populations {
		color: var(--color-text-primary);
	}

	.container {
		max-width: var(--container-lg);
		margin: 0 auto;
		padding: var(--space-8) var(--space-6) var(--space-16);
	}

	/* Breadcrumb */
	.breadcrumb {
		display: flex;
		align-items: center;
		gap: var(--space-2);
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		margin-bottom: var(--space-4);
	}

	.breadcrumb a {
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	.breadcrumb a:hover {
		text-decoration: underline;
	}

	/* Header */
	.header {
		margin-bottom: var(--space-8);
		padding-top: var(--space-4);
	}

	.header__title {
		font-family: var(--font-display);
		font-size: clamp(var(--text-2xl), 4vw, var(--text-3xl));
		font-weight: var(--font-weight-normal);
		color: var(--color-text-primary);
		margin-bottom: var(--space-3);
	}

	.header__subtitle {
		font-size: var(--text-lg);
		color: var(--color-text-secondary);
		max-width: 700px;
	}

	/* Key Finding Banner */
	.key-finding {
		background: linear-gradient(135deg, var(--color-accent-primary-glow), rgba(16, 185, 129, 0.1));
		border: 1px solid var(--color-accent-primary);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
		margin-bottom: var(--space-10);
	}

	.key-finding__title {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		font-weight: var(--font-weight-semibold);
		color: var(--color-accent-primary);
		margin-bottom: var(--space-2);
	}

	.key-finding__text {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	.key-finding__text strong {
		font-weight: var(--font-weight-bold);
	}

	.key-finding__text strong.positive {
		color: var(--color-score-high);
	}

	.key-finding__text strong.negative {
		color: var(--color-score-low);
	}

	/* Summary Cards */
	.summary {
		margin-bottom: var(--space-12);
	}

	.summary__grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
		gap: var(--space-6);
	}

	.summary-card {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
		text-align: center;
	}

	.summary-card__icon {
		width: 48px;
		height: 48px;
		margin: 0 auto var(--space-4);
		border-radius: var(--radius-lg);
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.summary-card__icon svg {
		width: 28px;
		height: 28px;
	}

	.summary-card--college .summary-card__icon {
		background: var(--color-score-high-bg);
		color: var(--color-score-high);
	}

	.summary-card--military .summary-card__icon {
		background: var(--color-accent-secondary-glow);
		color: var(--color-accent-secondary);
	}

	.summary-card--correctional .summary-card__icon {
		background: var(--color-score-low-bg);
		color: var(--color-score-low);
	}

	.summary-card__title {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-3);
	}

	.summary-card__score {
		font-family: var(--font-mono);
		font-size: var(--text-3xl);
		font-weight: var(--font-weight-bold);
		margin-bottom: var(--space-1);
	}

	.summary-card__score.positive {
		color: var(--color-score-high);
	}

	.summary-card__score.negative {
		color: var(--color-score-low);
	}

	.summary-card__label {
		font-size: var(--text-sm);
		color: var(--color-text-muted);
		margin-bottom: var(--space-4);
	}

	.summary-card__stats {
		display: flex;
		justify-content: center;
		gap: var(--space-4);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	/* Section Title */
	.section-title {
		display: flex;
		align-items: center;
		gap: var(--space-3);
		font-family: var(--font-display);
		font-size: var(--text-xl);
		color: var(--color-text-primary);
		margin-bottom: var(--space-3);
		padding-bottom: var(--space-3);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.section-title svg {
		width: 24px;
		height: 24px;
		color: var(--color-accent-primary);
	}

	.section-intro {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
		margin-bottom: var(--space-6);
		max-width: 800px;
	}

	/* Detail Section */
	.detail-section {
		margin-bottom: var(--space-12);
	}

	/* Tract Table */
	.tract-table-wrapper {
		overflow-x: auto;
		border-radius: var(--radius-lg);
		border: 1px solid var(--color-border-subtle);
	}

	.tract-table {
		width: 100%;
		border-collapse: collapse;
		font-size: var(--text-sm);
	}

	.tract-table th {
		background: var(--color-foundation-surface);
		padding: var(--space-3) var(--space-4);
		text-align: left;
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.tract-table td {
		padding: var(--space-3) var(--space-4);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	.tract-table tbody tr:last-child td {
		border-bottom: none;
	}

	.tract-table tbody tr:hover {
		background: var(--color-foundation-surface);
	}

	.tract-location {
		display: block;
		color: var(--color-text-primary);
	}

	.tract-fips {
		display: block;
		font-family: var(--font-mono);
		font-size: var(--text-xs);
		color: var(--color-text-muted);
	}

	.score {
		font-family: var(--font-mono);
		font-weight: var(--font-weight-medium);
	}

	.score.positive {
		color: var(--color-score-high);
	}

	.score.negative {
		color: var(--color-score-low);
	}

	.empty-state {
		padding: var(--space-8);
		text-align: center;
		color: var(--color-text-muted);
		background: var(--color-foundation-mid);
		border-radius: var(--radius-lg);
	}

	/* Implications */
	.implications {
		margin-bottom: var(--space-12);
	}

	.implications__grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: var(--space-6);
	}

	.implication {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
	}

	.implication h3 {
		font-size: var(--text-base);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-2);
	}

	.implication p {
		font-size: var(--text-sm);
		color: var(--color-text-secondary);
		line-height: var(--leading-relaxed);
	}

	/* Back Navigation */
	.back-nav {
		margin-top: var(--space-8);
		padding-top: var(--space-6);
		border-top: 1px solid var(--color-border-subtle);
	}

	.back-link {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		color: var(--color-accent-primary);
		text-decoration: none;
		font-size: var(--text-sm);
		font-weight: var(--font-weight-medium);
	}

	.back-link:hover {
		text-decoration: underline;
	}

	.back-link svg {
		width: 18px;
		height: 18px;
	}

	/* Utility */
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

	/* Responsive */
	@media (max-width: 640px) {
		.container {
			padding: var(--space-6) var(--space-4) var(--space-12);
		}

		.summary__grid {
			grid-template-columns: 1fr;
		}

		.tract-table th,
		.tract-table td {
			padding: var(--space-2) var(--space-3);
		}
	}
</style>
