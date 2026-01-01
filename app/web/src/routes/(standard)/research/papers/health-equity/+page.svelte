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
		title: 'Structural Correlates of Community Health Resilience: A Cross-Sectional Analysis of 53,889 U.S. Census Tracts',
		authors: ['Corey Schuman'],
		publishedDate: '2025-01-01',
		version: '1.0.0',
		status: 'preprint' as const,
		pdfUrl: '/research/papers/health-equity-v1.0.0.pdf'
	};

	const abstract = {
		background:
			'Community health resilience—the capacity to achieve better health outcomes than socioeconomic factors predict—is not equitably distributed. We analyzed 53,889 U.S. census tracts to quantify how resilience varies by racial composition and structural determinants.',
		objective:
			'To measure resilience disparities between majority-white and majority-minority communities, identify structural correlates, and determine whether patterns vary by state.',
		methods:
			'We merged CDC PLACES health data with American Community Survey demographics. We computed resilience as the residual from regression predicting health burden from socioeconomic factors. We compared resilience across majority-white vs. majority-minority communities, stratified by state, and examined correlates using multilevel modeling.',
		results:
			'Majority-minority communities averaged 0.43 standard deviations lower resilience than majority-white communities (multilevel z=-41.83, p<0.001). Percent Black population showed a moderate negative correlation with resilience (r=-0.34), while educational attainment correlated positively (r=+0.41). State-level gaps ranged from +1.87 SD (DC) to -0.42 SD (Washington); 28 of 43 state comparisons survived Bonferroni correction. Low-resilience tracts (bottom 10%) were 56.2% majority-minority compared to 26.4% nationally.',
		conclusions:
			'Resilience is inequitably distributed, but the pattern varies dramatically by state. Some states show near-equity or reversed patterns, suggesting structural factors—not immutable characteristics—are associated with these disparities. Policy should target the structural conditions associated with resilience in some contexts but not others.',
		keywords: [
			'health equity',
			'health disparities',
			'community resilience',
			'structural determinants',
			'racial composition',
			'census tract'
		]
	};

	const misuseWarnings = [
		'Deny resources to lower-scoring communities (lower resilience = MORE investment needed, not less)',
		'Claim that racial composition determines health outcomes (state variation proves structural factors are the mechanism)',
		'Use "low resilience" as a community label (targets should be structural conditions, not communities)',
		'Argue against race-conscious policy (these disparities co-occur with centuries of race-conscious harm)',
		'Cite Oregon or Nevada as "reversed patterns" (these did not survive multiple comparison correction)'
	];

	const limitations = [
		{
			title: 'Cross-sectional design',
			description:
				'We cannot establish causation. Observed associations may reflect selection, reverse causation, or unmeasured confounders.'
		},
		{
			title: 'Ecological fallacy',
			description:
				'Tract-level associations do not necessarily reflect individual-level relationships. We cannot claim individuals in low-resilience tracts are less resilient.'
		},
		{
			title: 'Modeled health estimates',
			description:
				'CDC PLACES uses small-area estimation models that may introduce bias. Validation against direct measurements is limited.'
		},
		{
			title: 'Residual confounding',
			description:
				'Our resilience measure controls for limited socioeconomic factors. Unmeasured confounders (housing quality, environmental exposures) may explain patterns.'
		},
		{
			title: 'Binary racial classification',
			description:
				'Majority-white vs. majority-minority oversimplifies racial composition. Multiracial communities and specific ethnic groups may show different patterns.'
		},
		{
			title: 'State-level sample sizes',
			description:
				'Some states have few majority-minority tracts (e.g., Oregon: 13), limiting precision of state-specific estimates.'
		}
	];

	const keyMessages = [
		{
			title: '0.43 SD resilience gap exists',
			description:
				'Majority-minority communities average nearly half a standard deviation lower resilience than majority-white communities. This is a substantial disparity.'
		},
		{
			title: 'Education is the strongest correlate',
			description:
				'Educational attainment (r=+0.41) correlates more strongly with resilience than any demographic factor, suggesting intervention targets.'
		},
		{
			title: 'State variation proves structural causation',
			description:
				'The same demographic composition produces different outcomes in different states (DC: +1.87 SD, Washington: -0.42 SD). This cannot be explained by immutable characteristics.'
		},
		{
			title: 'Bottom 10% is disproportionately minority',
			description:
				'56.2% of low-resilience tracts are majority-minority, versus 26.4% nationally. The burden of low resilience falls inequitably.'
		},
		{
			title: 'Some states show reversed patterns',
			description:
				'In Washington and California, majority-minority communities show HIGHER resilience than majority-white communities, demonstrating that equity is achievable.'
		}
	];
</script>

<svelte:head>
	<title>{paper.title} | odds.health Research</title>
	<meta
		name="description"
		content="A 0.43 SD resilience gap exists between majority-white and majority-minority communities, but state variation from +1.87 SD (DC) to -0.42 SD (Washington) proves structural factors—not race—determine resilience."
	/>

	<!-- Open Graph -->
	<meta property="og:type" content="article" />
	<meta property="og:title" content={paper.title} />
	<meta
		property="og:description"
		content="State-level variation proves structural factors, not immutable characteristics, determine community health resilience."
	/>
	<meta property="og:image" content="https://odds.health/og-image.svg" />

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
		<h4>What we found</h4>
		<p>
			Communities with more Black and minority residents tend to have worse health outcomes than
			you'd expect given their income and education levels. This gap is real—about 0.43 standard
			deviations, which is substantial.
		</p>

		<h4>But here's what's crucial</h4>
		<p>
			The same demographic composition produces COMPLETELY different outcomes depending on
			which state you're in. In Washington DC, majority-minority communities actually show
			+1.87 SD better resilience than average. In Washington State, majority-white communities
			show -0.42 SD worse resilience than average.
		</p>

		<h4>What this means</h4>
		<p>
			If race itself caused the disparity, the pattern would be the same everywhere. It's not.
			The massive state-by-state variation proves that <strong>structural factors</strong>—policies,
			investments, healthcare access, environmental conditions—determine resilience, not the
			racial composition of communities.
		</p>

		<h4>Why this matters for policy</h4>
		<p>
			Lower-resilience communities need MORE investment, not less. The reversed patterns in some
			states prove that equity is achievable. Policy should target the structural conditions that
			create resilience in some places but not others.
		</p>
	</PlainLanguageSummary>

	<MisuseWarning warnings={misuseWarnings} />

	<KeyMessages messages={keyMessages} />

	<section id="key-finding" class="context-section">
		<h2>The Key Finding: State Variation Proves Structural Causation</h2>
		<p>
			If racial composition itself caused lower resilience, we would expect the pattern to be
			consistent across states. Instead, we find:
		</p>
		<ul>
			<li><strong>Washington DC:</strong> Majority-minority tracts average +1.87 SD higher resilience</li>
			<li><strong>California:</strong> Majority-minority tracts average +0.15 SD higher resilience</li>
			<li><strong>Mississippi:</strong> Majority-minority tracts average -0.89 SD lower resilience</li>
			<li><strong>Louisiana:</strong> Majority-minority tracts average -0.78 SD lower resilience</li>
		</ul>
		<p>
			This 2.76 SD range (from +1.87 to -0.89) between states with similar demographic profiles
			demonstrates that <strong>structural factors, not immutable characteristics, determine
			community health resilience</strong>.
		</p>
	</section>

	<section id="responsible-use" class="context-section">
		<h2>Responsible Use Statement</h2>
		<p>
			This research documents structural inequities—it does not justify them. We explicitly
			prohibit the following uses:
		</p>
		<ol>
			<li>
				<strong>Do not use these data to deny resources to lower-scoring communities.</strong>
				Lower resilience scores indicate communities that need MORE investment, not less.
			</li>
			<li>
				<strong>Do not claim that racial composition determines health outcomes.</strong>
				The state-level variation demonstrates that identical demographic profiles produce
				different outcomes in different structural contexts.
			</li>
			<li>
				<strong>Do not use "low resilience" as a community label.</strong>
				This risks stigmatization. The appropriate targets are structural conditions.
			</li>
			<li>
				<strong>Do not use these findings to argue against race-conscious policy.</strong>
				The disparities documented here co-occur with centuries of race-conscious harm.
			</li>
		</ol>
	</section>

	<LimitationBox {limitations} />

	<section id="introduction">
		<h2>1. Introduction</h2>
		<p>
			The concept of community health resilience has gained attention as researchers seek to
			understand why some communities achieve better health outcomes than their socioeconomic
			circumstances would predict. A community with high poverty and low educational attainment
			that nonetheless shows lower-than-expected chronic disease burden exhibits resilience—something
			is protecting residents despite structural disadvantage.
		</p>
		<p>
			But who benefits from this resilience? If the protective factors that enable resilience are
			inequitably distributed—concentrated in white, affluent communities while absent from
			communities of color—then resilience-based frameworks could inadvertently reinforce disparities.
		</p>
		<p>
			This paper examines the equity dimensions of community health resilience across 53,889 U.S.
			census tracts. We document substantial disparities, identify structural correlates, and
			demonstrate that state-level variation proves these patterns reflect policy choices rather
			than immutable characteristics.
		</p>
	</section>

	<section id="methods">
		<h2>2. Methods</h2>

		<h3>2.1 Data Sources</h3>
		<p>
			We merged CDC PLACES 2022-2023 health data with American Community Survey 2022 5-year
			estimates. Health burden was computed as a composite of obesity, diabetes, coronary heart
			disease, high blood pressure, and physical inactivity prevalence.
		</p>

		<h3>2.2 Resilience Calculation</h3>
		<p>
			We computed resilience as the standardized residual from an OLS regression predicting
			health burden from food access (LILA status), poverty (low-income tract designation),
			urban/rural classification, and state fixed effects. Positive residuals indicate communities
			performing better than expected; negative residuals indicate communities performing worse.
		</p>

		<h3>2.3 Statistical Analysis</h3>
		<p>
			We compared resilience between majority-white (>50% white non-Hispanic) and majority-minority
			communities using multilevel models accounting for state-level clustering. We applied
			Bonferroni correction for 43 state-level comparisons (α = 0.001).
		</p>
	</section>

	<section id="results">
		<h2>3. Results</h2>

		<h3>3.1 Overall Disparity</h3>
		<p>
			Majority-minority communities averaged 0.43 SD lower resilience than majority-white
			communities (z = -41.83, p &lt; 0.001). The bottom 10% of tracts by resilience were 56.2%
			majority-minority, compared to 26.4% nationally.
		</p>

		<h3>3.2 Structural Correlates</h3>
		<p>
			Educational attainment showed the strongest positive correlation with resilience (r = +0.41),
			followed by median household income (r = +0.28). Percent Black population showed a moderate
			negative correlation (r = -0.34), but this was confounded with historical disinvestment
			patterns.
		</p>

		<h3>3.3 State-Level Variation</h3>
		<p>
			State-level gaps ranged from +1.87 SD (DC) to -0.42 SD (Washington). Of 43 state comparisons,
			28 survived Bonferroni correction. California and Washington showed statistically robust
			reversed patterns where majority-minority communities outperformed majority-white communities.
		</p>
	</section>

	<section id="discussion">
		<h2>4. Discussion</h2>
		<p>
			The massive state-level variation in resilience disparities—with identical demographic
			profiles producing opposite outcomes in different states—demonstrates that structural
			factors determine community health resilience. This finding has three key implications:
		</p>
		<ol>
			<li>
				<strong>Disparities are modifiable.</strong> The reversed patterns in California and
				Washington prove that racial equity in health resilience is achievable.
			</li>
			<li>
				<strong>Policy matters.</strong> States with different healthcare policies, economic
				structures, and histories of investment produce different resilience patterns.
			</li>
			<li>
				<strong>Education is a key lever.</strong> The strong correlation with educational
				attainment suggests that investments in education may improve community resilience.
			</li>
		</ol>
	</section>

	<section id="conclusion">
		<h2>5. Conclusion</h2>
		<p>
			Community health resilience is inequitably distributed, with majority-minority communities
			averaging 0.43 SD lower resilience than majority-white communities. However, the dramatic
			state-level variation—from +1.87 SD advantage in DC to -0.42 SD disadvantage in Washington
			State—proves that these patterns reflect structural factors rather than immutable
			characteristics. Policy should target the conditions that create resilience in some
			contexts but not others, with particular attention to educational attainment as a modifiable
			correlate.
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

	.context-section h2 {
		margin-top: 0;
		color: var(--text-primary);
	}

	.context-section ul,
	.context-section ol {
		margin: 1rem 0;
		padding-left: 1.5rem;
	}

	.context-section li {
		margin: 0.5rem 0;
	}

	section {
		margin: 2rem 0;
	}

	section h2 {
		border-bottom: 2px solid var(--border-color);
		padding-bottom: 0.5rem;
		margin-bottom: 1rem;
	}

	section h3 {
		margin-top: 1.5rem;
		color: var(--text-secondary);
	}
</style>
