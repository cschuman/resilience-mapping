<script lang="ts">
	import {
		PaperLayout,
		AbstractBox,
		LimitationBox,
		KeyMessages,
		MisuseWarning,
		PlainLanguageSummary,
		EquityWarning
	} from '$lib/components/research';

	const paper = {
		title: 'Beyond the Hispanic Paradox: Immigrant Health Advantage, Structural Poverty, and the Aggregation Artifact in Community Health Resilience',
		authors: ['Corey Schuman'],
		publishedDate: '2025-01-01',
		version: '1.0.0',
		status: 'preprint' as const,
		pdfUrl: '/research/papers/immigrant-health-advantage-v1.0.0.pdf'
	};

	const abstract = {
		background:
			'The "Hispanic Paradox"—the observation that Hispanic Americans show better-than-expected health outcomes despite socioeconomic disadvantage—has been debated for decades. We examined whether this pattern reflects genuine cultural protection or methodological and structural artifacts.',
		objective:
			'To test whether the Hispanic Paradox reflects (1) an aggregation artifact, (2) immigrant selection operating across ethnic groups, or (3) context-dependent structural factors.',
		methods:
			'Using CDC PLACES health data and American Community Survey demographics for 165,393 census tracts, we calculated community health resilience scores. We disaggregated by Hispanic origin (Mexican, Puerto Rican, Cuban, South/Central American) and tested immigrant selection effects across racial/ethnic groups using clustered standard errors at the county level.',
		results:
			'The overall Hispanic-resilience correlation (r = +0.006) masked profound heterogeneity: South American (r = +0.147), Central American (r = +0.060), Mexican (r = -0.029), Puerto Rican (r = -0.017). Within Texas, Mexican-majority border communities showed -1.08 SD resilience versus Austin\'s +1.53 SD—a 2.61 SD gap despite similar ethnicity. Black-majority tracts showed a positive foreign-born association with resilience (r = +0.221), stronger than Hispanic-majority tracts (r = +0.133). All findings remained significant with county-clustered standard errors (5x larger than unclustered).',
		conclusions:
			'At the community level, the "Hispanic Paradox" reflects an aggregation artifact masking heterogeneous subgroup effects, patterns consistent with immigrant selection operating across racial/ethnic groups, and context-dependence where structural poverty may offset immigrant health advantages. We propose reframing from "Hispanic Paradox" to "Immigrant Health Advantage."',
		keywords: [
			'Hispanic Paradox',
			'immigrant health',
			'aggregation artifact',
			'structural determinants',
			'health disparities',
			'foreign-born'
		]
	};

	const misuseWarnings = [
		'Claim Hispanic culture is irrelevant to health (we measured community composition, not individual cultural practices)',
		'Use these findings to restrict immigration (immigrant-rich communities show better health outcomes)',
		'Ignore border communities\' needs (the -1.08 SD finding indicates urgent public health need)',
		'Apply individual-level interventions based on ecological data (tract correlations ≠ individual effects)',
		'Argue that structural factors are more important than cultural factors without intervention studies'
	];

	const limitations = [
		{
			title: 'Ecological fallacy',
			description:
				'Tract-level associations do not establish individual-level relationships. We cannot claim immigrants themselves are healthier, only that immigrant-rich communities show better outcomes.'
		},
		{
			title: 'Cross-sectional design',
			description:
				'Cannot establish causation or true generational decay. The foreign-born quintile gradient could reflect selection into different tracts rather than within-community change.'
		},
		{
			title: 'Unmeasured confounders',
			description:
				'Documentation status, healthcare access, English proficiency, and employer-provided insurance could not be measured and may differ systematically across regions.'
		},
		{
			title: 'Spatial autocorrelation',
			description:
				'County-clustered standard errors inflated SEs 5x, reflecting substantial within-county correlation. All findings remained significant with conservative estimates.'
		},
		{
			title: 'CDC PLACES circularity',
			description:
				'CDC\'s model-based estimates use demographic variables in prediction. Observed associations may partly reflect the prediction model\'s structure.'
		},
		{
			title: 'Small regional samples',
			description:
				'Austin (N=156) and border (N=188) comparisons involve relatively small samples, though >99% power for the observed 2.61 SD effect.'
		}
	];

	const keyMessages = [
		{
			title: 'The "Hispanic Paradox" is an aggregation artifact',
			description:
				'The near-zero overall correlation (r = +0.006) masks opposite effects: South American (r = +0.147) vs. Mexican (r = -0.029). Treating "Hispanic" as monolithic obscures meaningful patterns.'
		},
		{
			title: 'Black immigrants show STRONGER health advantage',
			description:
				'Black-majority tracts show r = +0.221 for foreign-born association vs. Hispanic-majority r = +0.133. The advantage transcends ethnicity—it\'s about immigration, not Hispanic culture.'
		},
		{
			title: 'Same ethnicity, same state, 2.61 SD gap',
			description:
				'Austin (+1.53 SD) vs. Texas border (-1.08 SD). Border has MORE immigrants but WORSE outcomes. Structural poverty overwhelms immigrant advantage.'
		},
		{
			title: 'Reframe: "Immigrant Health Advantage"',
			description:
				'The phenomenon is neither uniquely Hispanic nor paradoxical. It reflects immigrant selection operating across ethnic groups, contingent on economic context.'
		},
		{
			title: 'Robust to spatial autocorrelation',
			description:
				'All findings remain significant with county-clustered SEs (5x larger). Medicaid expansion was not a significant confounder (p = 0.77).'
		}
	];
</script>

<svelte:head>
	<title>{paper.title} | odds.health Research</title>
	<meta
		name="description"
		content="The 'Hispanic Paradox' is an aggregation artifact. Black immigrants show stronger health advantages than Hispanic immigrants. We propose reframing to 'Immigrant Health Advantage.'"
	/>

	<!-- Open Graph -->
	<meta property="og:type" content="article" />
	<meta property="og:title" content="The Hispanic Paradox Is a 40-Year Statistical Illusion" />
	<meta
		property="og:description"
		content="Black immigrants show STRONGER health advantages than Hispanic immigrants. The 'paradox' reflects immigration selection, not Hispanic culture."
	/>
	<meta property="og:image" content="https://odds.health/og-hispanic-paradox.svg" />

	<!-- Google Scholar -->
	<meta name="citation_title" content={paper.title} />
	<meta name="citation_author" content="Schuman, Corey" />
	<meta name="citation_publication_date" content="2025/01/01" />
	<meta name="citation_journal_title" content="odds.health Research" />
</svelte:head>

<PaperLayout
	title={paper.title}
	authors={paper.authors}
	publishedDate={paper.publishedDate}
	version={paper.version}
	status={paper.status}
	pdfUrl={paper.pdfUrl}
>
	<AbstractBox
		background={abstract.background}
		objective={abstract.objective}
		methods={abstract.methods}
		results={abstract.results}
		conclusions={abstract.conclusions}
		keywords={abstract.keywords}
	/>

	<PlainLanguageSummary>
		<h4>The 40-year mystery, solved</h4>
		<p>
			For decades, researchers puzzled over why Hispanic Americans seemed healthier than their
			income and education levels would predict. They called it the "Hispanic Paradox" and
			attributed it to strong family bonds, traditional diets, and cultural protection.
		</p>

		<h4>We found it's a statistical illusion</h4>
		<p>
			When you lump all Hispanic groups together, the positive effects (South Americans: r = +0.147)
			and negative effects (Mexicans: r = -0.029) cancel out to near zero (r = +0.006). There is
			no single "Hispanic effect"—there are many different effects that average to nothing.
		</p>

		<h4>The smoking gun</h4>
		<p>
			<strong>Black immigrants show a STRONGER health advantage than Hispanic immigrants.</strong>
			If the "paradox" were about Hispanic culture, this wouldn't happen. It's about immigration
			itself—the selection process that brings healthy, motivated people to a new country.
		</p>

		<h4>But here's the catch</h4>
		<p>
			The Texas border has MORE immigrants than Austin (25.5% vs 17.6%) but WORSE health outcomes
			(-1.08 SD vs +1.53 SD). The immigrant advantage exists, but <strong>structural poverty
			can overwhelm it</strong>. A century of disinvestment in border communities matters more
			than any immigrant health advantage.
		</p>

		<h4>What we should call it instead</h4>
		<p>
			"Immigrant Health Advantage"—not "Hispanic Paradox." It's not about Hispanic culture.
			It's about the selection effects of immigration operating across all ethnic groups,
			contingent on what kind of economic opportunity awaits immigrants when they arrive.
		</p>
	</PlainLanguageSummary>

	<MisuseWarning warnings={misuseWarnings} />

	<KeyMessages messages={keyMessages} />

	<section id="headline-finding" class="context-section context-section--featured">
		<h2>The Headline Finding</h2>
		<div class="finding-grid">
			<div class="finding-card">
				<div class="finding-value positive">+0.147</div>
				<div class="finding-label">South American r</div>
			</div>
			<div class="finding-card">
				<div class="finding-value negative">-0.029</div>
				<div class="finding-label">Mexican r</div>
			</div>
			<div class="finding-card">
				<div class="finding-value neutral">+0.006</div>
				<div class="finding-label">"Hispanic" r (artifact)</div>
			</div>
		</div>
		<p>
			The "Hispanic Paradox" (r ≈ 0) is what happens when you average opposite effects together.
			South Americans show strong positive associations; Mexicans show slight negative.
			Together, they cancel out to nothing—creating a "paradox" that isn't there.
		</p>
	</section>

	<section id="cross-ethnic" class="context-section">
		<h2>The Cross-Ethnic Test</h2>
		<p>
			If the "Hispanic Paradox" were about Hispanic culture, we wouldn't expect to see it
			in Black communities. But we do:
		</p>
		<div class="comparison-table">
			<div class="comparison-row">
				<span class="comparison-label">Black-majority tracts</span>
				<span class="comparison-value">r = +0.221</span>
			</div>
			<div class="comparison-row">
				<span class="comparison-label">Hispanic-majority tracts</span>
				<span class="comparison-value">r = +0.133</span>
			</div>
		</div>
		<p>
			Black immigrants show a <strong>stronger</strong> positive association between
			foreign-born composition and community resilience than Hispanic immigrants.
			The phenomenon transcends ethnicity—it's about immigration selection, not culture.
		</p>
	</section>

	<section id="texas-case" class="context-section">
		<h2>The Texas Case Study: When Poverty Overwhelms</h2>
		<div class="texas-comparison">
			<div class="texas-card austin">
				<h3>Austin</h3>
				<div class="stat">+1.53 SD</div>
				<div class="detail">17.6% foreign-born</div>
				<div class="detail">17.2% poverty</div>
				<div class="detail">$76,026 median income</div>
			</div>
			<div class="texas-card border">
				<h3>Texas Border</h3>
				<div class="stat">-1.08 SD</div>
				<div class="detail">25.5% foreign-born</div>
				<div class="detail">27.9% poverty</div>
				<div class="detail">$46,477 median income</div>
			</div>
		</div>
		<p>
			<strong>Same ethnicity. Same state. 2.61 standard deviations apart.</strong>
		</p>
		<p>
			The border has MORE immigrants but WORSE outcomes. Why? A century of structural
			disinvestment, colonias without infrastructure, an economy designed for labor
			extraction rather than community development. The immigrant health advantage exists,
			but concentrated poverty can overwhelm it.
		</p>
	</section>

	<section id="robustness" class="context-section">
		<h2>Robustness: These Findings Hold Up</h2>
		<p>
			We addressed two major methodological concerns:
		</p>
		<ul>
			<li>
				<strong>Spatial autocorrelation:</strong> County-clustered standard errors are 5x larger
				than unclustered estimates. All findings remain significant (p < 0.001).
			</li>
			<li>
				<strong>Medicaid expansion:</strong> Texas hasn't expanded Medicaid; Illinois has.
				After controlling for expansion status, it's not a significant confounder (β = -0.020,
				p = 0.77).
			</li>
		</ul>
		<p>
			The confidence intervals are wider (more honest), but the conclusions are unchanged.
		</p>
	</section>

	<LimitationBox {limitations} />

	<section id="implications">
		<h2>Policy Implications</h2>
		<ol>
			<li>
				<strong>Disaggregate Hispanic data.</strong> National surveys should report outcomes
				separately for Mexican, Puerto Rican, Cuban, Central American, and South American
				populations. Aggregated "Hispanic" statistics obscure actionable information.
			</li>
			<li>
				<strong>Invest in the Texas border.</strong> The -1.08 SD resilience represents a
				public health crisis requiring infrastructure, healthcare, and economic development—not
				because of ethnicity, but because of systematic underinvestment.
			</li>
			<li>
				<strong>Recognize immigrant communities as health assets.</strong> The consistent
				positive association between immigrant composition and community health suggests
				immigrant-receiving communities show better outcomes than expected.
			</li>
			<li>
				<strong>Address structural determinants.</strong> The poverty coefficient (β = -0.38)
				is 3x larger than the immigrant coefficient (β = +0.14). Structural economic factors
				show stronger associations with resilience than immigrant composition.
			</li>
		</ol>
	</section>

	<section id="conclusion">
		<h2>Conclusion</h2>
		<p>
			The "Hispanic Paradox" is neither paradoxical nor uniquely Hispanic. It reflects:
		</p>
		<ul>
			<li>An <strong>aggregation artifact</strong> masking divergent subgroup patterns</li>
			<li><strong>Immigrant selection</strong> operating across racial/ethnic groups</li>
			<li><strong>Context-dependence</strong>—structural poverty can offset immigrant advantages</li>
		</ul>
		<p>
			We propose reframing from "Hispanic Paradox" to "Immigrant Health Advantage." The
			40-year mystery was a statistical illusion created by lumping heterogeneous groups
			together. The real story is simpler: immigration selects for healthy people, but
			what happens after arrival depends on the structural conditions they encounter.
		</p>
	</section>
</PaperLayout>

<style>
	.context-section {
		margin: 2rem 0;
		padding: 1.5rem;
		background: var(--surface-secondary);
		border-radius: 8px;
	}

	.context-section--featured {
		background: linear-gradient(135deg, var(--surface-secondary), var(--surface-tertiary));
		border: 2px solid var(--accent-color);
	}

	.context-section h2 {
		margin-top: 0;
		color: var(--text-primary);
	}

	.finding-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 1rem;
		margin: 1.5rem 0;
	}

	.finding-card {
		text-align: center;
		padding: 1rem;
		background: var(--surface-primary);
		border-radius: 8px;
	}

	.finding-value {
		font-size: 2rem;
		font-weight: 700;
		font-family: var(--font-mono);
	}

	.finding-value.positive { color: var(--color-success); }
	.finding-value.negative { color: var(--color-error); }
	.finding-value.neutral { color: var(--text-secondary); }

	.finding-label {
		font-size: 0.875rem;
		color: var(--text-secondary);
		margin-top: 0.5rem;
	}

	.comparison-table {
		margin: 1rem 0;
		padding: 1rem;
		background: var(--surface-primary);
		border-radius: 8px;
	}

	.comparison-row {
		display: flex;
		justify-content: space-between;
		padding: 0.75rem 0;
		border-bottom: 1px solid var(--border-color);
	}

	.comparison-row:last-child {
		border-bottom: none;
	}

	.comparison-value {
		font-family: var(--font-mono);
		font-weight: 600;
		color: var(--color-success);
	}

	.texas-comparison {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1.5rem;
		margin: 1.5rem 0;
	}

	.texas-card {
		padding: 1.5rem;
		border-radius: 8px;
		text-align: center;
	}

	.texas-card.austin {
		background: rgba(34, 197, 94, 0.1);
		border: 2px solid var(--color-success);
	}

	.texas-card.border {
		background: rgba(239, 68, 68, 0.1);
		border: 2px solid var(--color-error);
	}

	.texas-card h3 {
		margin: 0 0 0.5rem 0;
	}

	.texas-card .stat {
		font-size: 2.5rem;
		font-weight: 700;
		font-family: var(--font-mono);
	}

	.austin .stat { color: var(--color-success); }
	.border .stat { color: var(--color-error); }

	.texas-card .detail {
		font-size: 0.875rem;
		color: var(--text-secondary);
		margin-top: 0.25rem;
	}

	section {
		margin: 2rem 0;
	}

	section h2 {
		border-bottom: 2px solid var(--border-color);
		padding-bottom: 0.5rem;
		margin-bottom: 1rem;
	}

	@media (max-width: 768px) {
		.finding-grid,
		.texas-comparison {
			grid-template-columns: 1fr;
		}
	}
</style>
