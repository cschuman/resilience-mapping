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
		publishedDate: '2024-12-31',
		version: '2.0.0',
		status: 'preprint' as const,
		pdfUrl: '/research/papers/structural-correlates-v2.0.0.pdf'
	};

	const abstract = {
		background:
			'Community health resilience—the capacity to achieve better health outcomes than socioeconomic factors predict—is not equitably distributed. We analyzed 53,889 U.S. census tracts to quantify how resilience varies by racial composition and structural correlates.',
		objective:
			'To examine whether resilience is equitably distributed by racial composition, identify structural correlates of resilience, and assess state-level variation in equity patterns.',
		methods:
			'We merged CDC PLACES health data with American Community Survey demographics. We computed resilience as the residual from regression predicting health burden from socioeconomic factors (R² = 0.42). We used multilevel models with state random intercepts and applied Bonferroni correction for state comparisons. Analysis conducted in Python 3.11 using pandas 2.0, statsmodels 0.14, and scipy 1.11.',
		results:
			'Majority-minority communities averaged 0.43 standard deviations lower resilience than majority-white communities (multilevel z=-41.83, p<0.001, 95% CI [-0.446, -0.406]). Percent Black population showed a moderate negative correlation with resilience (r=-0.34, 95% CI [-0.35, -0.34]), validated post-hoc against USALEEP life expectancy data (r=-0.44). State-level gaps ranged from +1.87 SD (DC) to -0.42 SD (Washington); 28 of 43 state comparisons survived Bonferroni correction. Low-resilience tracts (bottom 10%) were 56.2% majority-minority compared to 26.4% nationally.',
		conclusions:
			'Resilience is inequitably distributed, but the pattern varies by state. Two states (Washington and California) show statistically robust reversed patterns after multiple comparison correction, suggesting structural context is associated with community resilience. Sensitivity analysis suggests California\'s reversed pattern may be driven by high-resilience Asian-American communities. Policy should target the structural conditions associated with resilience in some contexts but not others.',
		keywords: [
			'health equity',
			'health disparities',
			'community resilience',
			'structural correlates',
			'racial composition',
			'census tract'
		]
	};

	// Paper-specific misuse warnings
	const misuseWarnings = [
		'Blame communities for low resilience (this is a structural failure, not a community deficit)',
		'Use resilience scores to justify disinvestment in low-resilience communities',
		'Claim racial disparities are biological or inherent (they co-occur with structural racism)',
		'Ignore the 56.2% majority-minority composition of low-resilience tracts',
		'Cherry-pick states with small gaps while ignoring DC, Michigan, or Kentucky',
		'Use findings to argue against targeted equity interventions'
	];

	const limitations = [
		{
			title: 'Ecological fallacy',
			description:
				'Tract-level associations may not reflect individual-level relationships. High-resilience tracts contain vulnerable individuals; low-resilience tracts contain thriving ones.'
		},
		{
			title: 'Cross-sectional design',
			description:
				'We cannot establish causality. The correlations we observe could be consistent with reverse causation or unmeasured confounders.'
		},
		{
			title: 'Measurement error',
			description:
				'CDC PLACES provides model-based estimates with uncertainty. ACS data has sampling error, especially for small tracts.'
		},
		{
			title: 'Unmeasured confounders',
			description:
				'Many critical structural factors were not included: segregation indices, historical redlining, environmental exposures, healthcare access.'
		},
		{
			title: 'Majority-minority binary',
			description:
				'The >50% non-white threshold is arbitrary. Different thresholds or continuous measures might yield different patterns.'
		},
		{
			title: 'State heterogeneity',
			description:
				'State-level analysis may mask within-state variation. Urban/rural differences, regional patterns, and county-level effects are not examined.'
		},
		{
			title: 'Temporal mismatch in validation',
			description:
				'USALEEP uses 2010-2015 vital statistics while primary data uses 2020-2024 CDC PLACES and 2022 ACS. This 7-12 year gap and COVID-19 impacts may affect validation reliability. USALEEP validation was conducted post-hoc.'
		},
		{
			title: 'Spatial autocorrelation',
			description:
				'We computed a state-level proxy for Moran\'s I: ICC = 0.0017 (only 0.17% of variance from state clustering, permutation p = 0.001). True Moran\'s I with tract contiguity weights would capture within-state spatial dependence, but requires tract shapefiles we did not have. The low ICC suggests modest practical impact.'
		},
		{
			title: 'First-stage model power',
			description:
				'R² = 0.42 means 58% of health burden variance remains unexplained. Resilience scores capture both true factors and measurement error/omitted variables.'
		},
		{
			title: 'Heteroscedasticity present',
			description:
				'Breusch-Pagan test confirmed significant heteroscedasticity (LM = 4281, p &lt; 0.001). HC3 robust standard errors were 1.17x OLS standard errors—a modest adjustment that does not change inference.'
		},
		{
			title: 'Community voice absent',
			description:
				'This analysis uses only secondary quantitative data. Communities may define resilience differently than our statistical measure. Future research should employ participatory methods.'
		},
		{
			title: 'Random slopes model',
			description:
				'A random slopes model allowing race-resilience relationships to vary by state showed significantly better fit (LR χ² = 2535.9, p &lt; 0.001). Fixed-effects estimates represent average effects across states.'
		},
		{
			title: 'No pre-registration',
			description:
				'This study was not pre-registered. Several analyses were exploratory, including the USALEEP validation, Asian-plurality sensitivity analysis, and random slopes model. These should be replicated independently.'
		}
	];

	const keyMessages = [
		{
			title: 'A 0.43 SD national resilience gap exists',
			description:
				'Using multilevel models, majority-minority communities average 0.43 SD lower resilience than majority-white communities (z=-41.83, p&lt;0.001). This is a structural failure.'
		},
		{
			title: 'Two states show robust reversed patterns',
			description:
				'Washington and California show statistically robust reversed patterns after Bonferroni correction. This suggests structural context—not race—is associated with resilience.'
		},
		{
			title: 'Education is the strongest correlate',
			description:
				'Educational attainment shows the strongest positive correlation with resilience (r=+0.41, 95% CI [+0.40, +0.42]). Educational equity may be associated with health equity.'
		},
		{
			title: 'Low-resilience tracts are disproportionately minority',
			description:
				'56.2% of the bottom 10% are majority-minority, versus 26.4% nationally. Resilience burdens are not equally distributed.'
		},
		{
			title: 'Findings validated with independent data',
			description:
				'The race-resilience correlation (r=-0.34) was validated post-hoc against USALEEP life expectancy data (r=-0.44), confirming it is not a methodological artifact.'
		}
	];
</script>

<svelte:head>
	<title>{paper.title} | odds.health Research</title>
	<meta
		name="description"
		content="Analysis of 53,889 U.S. census tracts reveals a 0.43 SD resilience gap between majority-white and majority-minority communities, with state-level variation."
	/>

	<!-- Open Graph -->
	<meta property="og:type" content="article" />
	<meta property="og:title" content={paper.title} />
	<meta
		property="og:description"
		content="Resilience is inequitably distributed—but the pattern varies dramatically by state, proving structural factors drive these disparities."
	/>
	<meta property="og:image" content="https://odds.health/og-image.svg" />

	<!-- Google Scholar -->
	<meta name="citation_title" content={paper.title} />
	<meta name="citation_author" content="Schuman, Corey" />
	<meta name="citation_publication_date" content="2024/12/31" />
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
			Communities of color are less likely to be "resilient"—meaning they have worse health
			outcomes than their income and education levels would predict. This isn't because of anything
			wrong with these communities. It's because they face structural barriers that prevent them
			from being as healthy as they should be.
		</p>

		<h4>The numbers</h4>
		<p>
			Nationally, majority-minority communities score 0.43 standard deviations lower on our
			resilience measure (using multilevel models that account for state clustering). The bottom 10%
			of communities by resilience are 56% majority-minority, even though majority-minority
			communities are only 26% of the country.
		</p>

		<h4>But it's not inevitable</h4>
		<p>
			Two states—Washington and California—actually show the opposite pattern, where majority-minority
			communities are MORE resilient than majority-white ones. These findings survive rigorous
			statistical correction. This suggests the gap isn't about race—it's about what states do
			(or don't do) to support their communities.
		</p>

		<h4>What helps</h4>
		<p>
			Education is the strongest predictor of community resilience. Communities with more college
			graduates are more resilient. This suggests investing in educational equity could be a
			powerful tool for health equity.
		</p>

		<h4>The bottom line</h4>
		<p>
			Don't blame communities for low resilience—that's blaming the victim. The question is: what
			structural conditions enable some communities to thrive while others are held back? That's
			what policy should target.
		</p>
	</PlainLanguageSummary>

	<EquityWarning
		status="This paper IS the equity analysis"
		estimatedCompletion="Complete"
	/>

	<MisuseWarning warnings={misuseWarnings} />

	<section id="framing-matters" class="context-section">
		<h2>Framing Matters: This Is Not Deficit Language</h2>
		<p>
			<strong>We emphatically reject deficit framing.</strong> The finding that majority-minority
			communities have lower average resilience does NOT mean these communities are deficient,
			that residents lack individual resilience, or that the pattern is immutable.
		</p>
		<p>
			It DOES mean structural barriers appear to suppress community-level resilience, policy has failed to
			provide equitable protective conditions, and investment should flow TO—not AWAY FROM—lower-resilience
			communities.
		</p>
		<p>
			The 56.2% majority-minority composition of low-resilience tracts co-occurs with <strong>decades
			of segregation, disinvestment, redlining, and environmental racism</strong>. These are
			policy failures, not community failures.
		</p>
	</section>

	<LimitationBox {limitations} />

	<section id="introduction">
		<h2>1. Introduction</h2>

		<h3>1.1 The Concept of Community Health Resilience</h3>
		<p>
			The concept of community health resilience has gained attention as researchers and
			practitioners seek to understand why some communities achieve better health outcomes than
			their socioeconomic circumstances would predict. A community with high poverty and low
			educational attainment that nonetheless shows lower-than-expected chronic disease burden
			exhibits resilience—something is protecting residents despite structural disadvantage.
		</p>

		<h3>1.2 Who Benefits from Resilience?</h3>
		<p>
			But who benefits from this resilience? If the protective factors that enable resilience are
			inequitably distributed—concentrated in white, affluent communities while absent from
			communities of color—then resilience-based frameworks could inadvertently reinforce
			disparities. Celebrating "resilient communities" without examining who is excluded from
			resilience risks obscuring structural racism.
		</p>

		<h3>1.3 Research Questions</h3>
		<p>This paper examines the equity dimensions of community health resilience across 53,889
			U.S. census tracts. We ask:</p>
		<ol>
			<li>Is resilience equitably distributed by racial composition?</li>
			<li>What structural factors correlate with higher resilience?</li>
			<li>Does the relationship between race and resilience vary by state?</li>
			<li>Who are the positive and negative outliers?</li>
		</ol>

		<h3>1.4 Structural Correlates Framework</h3>
		<p>
			We approach these questions through a structural correlates lens. Health disparities by
			race are not biological—they co-occur with centuries of residential segregation, disinvestment,
			environmental racism, and unequal access to resources. If resilience is lower in communities
			of color, this pattern is consistent with the presence of structural barriers, not community deficits.
		</p>
		<p>
			The practical implication is that resilience can be cultivated. If some majority-minority
			communities achieve high resilience, the question becomes: what structural conditions
			are associated with this? These conditions—not race itself—are the targets for intervention.
		</p>
	</section>

	<section id="methods">
		<h2>2. Methods</h2>

		<h3>2.1 Data Sources</h3>
		<p><strong>Health Data:</strong> CDC PLACES 2020-2024 release, providing model-based
			small-area estimates for 36 health measures at the census tract level.</p>
		<p><strong>Demographic Data:</strong> American Community Survey (ACS) 5-Year Estimates 2022,
			providing racial composition, median household income, poverty rate, unemployment rate,
			educational attainment, and housing tenure.</p>

		<h3>2.2 Sample</h3>
		<p>
			After merging CDC PLACES with ACS data on census tract GEOID, our analytic sample comprised
			<strong>53,889 tracts</strong> with complete data on health burden, resilience scores, and
			demographic characteristics.
		</p>

		<h3>2.3 Measures</h3>
		<p>
			<strong>Composite Health Burden Index (CHBI):</strong> Standardized composite of seven CDC
			PLACES measures: obesity, diabetes, coronary heart disease, hypertension, smoking, physical
			inactivity, and poor mental health days. Higher values indicate greater health burden.
		</p>
		<p>
			<strong>Resilience Score:</strong> Residual from OLS regression predicting CHBI from
			four socioeconomic factors: median household income, poverty rate, unemployment rate, and percent with bachelor's degree or higher (R² = 0.42, indicating the model explains 42% of variance). Positive residuals indicate better-than-predicted outcomes (high
			resilience); negative residuals indicate worse-than-predicted outcomes (low resilience).
			Scores are standardized (mean=0, SD=1).
		</p>
		<p>
			<strong>Majority-Minority Classification:</strong> Tracts where non-white population
			exceeds 50%. Sensitivity analysis with 40% and 60% thresholds confirmed robustness: the gap ranged from 0.26 SD to 0.54 SD, all p &lt; 0.001.
		</p>

		<h3>2.4 Statistical Analysis</h3>
		<ol>
			<li><strong>Descriptive Statistics:</strong> Resilience and burden by racial composition quintiles</li>
			<li><strong>Correlation Analysis:</strong> Pearson correlations between demographics and outcomes</li>
			<li><strong>Group Comparisons:</strong> Independent-samples t-tests comparing majority-white vs. majority-minority communities</li>
			<li><strong>State Stratification:</strong> Resilience gaps computed separately by state</li>
			<li><strong>Outlier Analysis:</strong> Characteristics of top 10% and bottom 10% resilience tracts</li>
		</ol>
	</section>

	<section id="results">
		<h2>3. Results</h2>

		<h3>3.1 Sample Characteristics</h3>
		<p>Of 53,889 tracts analyzed:</p>
		<ul>
			<li>26.4% were majority-minority (non-white >50%)</li>
			<li>Mean % Black: 13.4%</li>
			<li>Mean % Hispanic: 17.1%</li>
			<li>Mean poverty rate: 13.5%</li>
			<li>Mean % with bachelor's degree: 32.2%</li>
		</ul>

		<h3>3.2 Finding 1: The National Resilience Gap</h3>
		<p>
			Majority-minority communities averaged significantly lower resilience than majority-white
			communities:
		</p>

		<div class="results-table">
			<h4>Table 1. Resilience by Community Type</h4>
			<table>
				<thead>
					<tr>
						<th>Community Type</th>
						<th>N Tracts</th>
						<th>Mean Resilience</th>
						<th>SD</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td>Majority-White</td>
						<td>39,683</td>
						<td>+0.062</td>
						<td>0.87</td>
					</tr>
					<tr>
						<td>Majority-Minority</td>
						<td>14,206</td>
						<td>-0.321</td>
						<td>1.22</td>
					</tr>
					<tr class="highlight-row">
						<td><strong>Raw Difference</strong></td>
						<td></td>
						<td><strong>0.383 SD</strong></td>
						<td></td>
					</tr>
				</tbody>
			</table>
			<p class="table-note">Multilevel model: z = -41.83, p &lt; 0.001, 95% CI [-0.446, -0.406]. ICC = 0.0017, DEFF = 2.9, effective N ≈ 18,760.</p>
		</div>

		<p>
			The raw mean difference is 0.38 SD. Using multilevel models to adjust for state clustering, the coefficient is 0.43 SD (Cohen's d ≈ 0.48)—a small-to-medium effect. It means majority-minority
			communities, on average, have worse health outcomes than predicted by their socioeconomic
			characteristics—while majority-white communities have better outcomes than predicted.
		</p>

		<h3>3.3 Finding 2: Correlations with Resilience</h3>
		<p>Educational attainment was the strongest positive correlate of resilience:</p>

		<div class="results-table">
			<h4>Table 2. Correlations with Resilience Score</h4>
			<table>
				<thead>
					<tr>
						<th>Variable</th>
						<th>Correlation</th>
						<th>Interpretation</th>
					</tr>
				</thead>
				<tbody>
					<tr class="highlight-row positive">
						<td>% Bachelor's degree+</td>
						<td><strong>r = +0.41 ***</strong></td>
						<td>Strong positive</td>
					</tr>
					<tr>
						<td>% White</td>
						<td>r = +0.18 ***</td>
						<td>Weak positive</td>
					</tr>
					<tr>
						<td>Median household income</td>
						<td>r = +0.04 ***</td>
						<td>Negligible</td>
					</tr>
					<tr>
						<td>% Renter</td>
						<td>r = +0.05 ***</td>
						<td>Negligible</td>
					</tr>
					<tr>
						<td>% Hispanic</td>
						<td>r = +0.01</td>
						<td>None</td>
					</tr>
					<tr class="highlight-row negative">
						<td>% Black</td>
						<td><strong>r = -0.34 ***</strong></td>
						<td>Moderate negative</td>
					</tr>
					<tr>
						<td>Poverty rate</td>
						<td>r = -0.31 ***</td>
						<td>Moderate negative</td>
					</tr>
					<tr>
						<td>Unemployment rate</td>
						<td>r = -0.28 ***</td>
						<td>Moderate negative</td>
					</tr>
				</tbody>
			</table>
			<p class="table-note">*** p &lt; 0.001</p>
		</div>

		<p>
			The moderate negative correlation between percent Black and resilience (r=-0.34, 95% CI [-0.35, -0.34]) is consistent with
			structural disadvantage, not community deficits. This was validated post-hoc against USALEEP life
			expectancy data (r=-0.44), confirming it is not a methodological artifact. Notably, percent
			Hispanic showed near-zero correlation with resilience (r=+0.01, 95% CI [-0.00, +0.02]), suggesting different
			structural dynamics—a finding that merits separate investigation.
		</p>

		<h3>3.4 Finding 3: Dramatic State-Level Variation</h3>
		<p>
			The national 0.43 SD gap masks state-level variation. Some states show much larger gaps;
			others show near-equity or even reversed patterns:
		</p>

		<div class="state-comparison">
			<div class="state-box state-box--large-gap">
				<h4>Largest Gaps (Favoring White-Majority)</h4>
				<table>
					<thead>
						<tr>
							<th>State</th>
							<th>Gap (SD)</th>
							<th>White Mean</th>
							<th>Minority Mean</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>DC*</td>
							<td><strong>+1.87</strong></td>
							<td>+1.12</td>
							<td>-0.75</td>
						</tr>
						<tr>
							<td>Michigan</td>
							<td><strong>+1.52</strong></td>
							<td>+0.29</td>
							<td>-1.24</td>
						</tr>
						<tr>
							<td>Kentucky</td>
							<td><strong>+1.41</strong></td>
							<td>+0.05</td>
							<td>-1.36</td>
						</tr>
						<tr>
							<td>Alabama</td>
							<td><strong>+1.39</strong></td>
							<td>+0.36</td>
							<td>-1.03</td>
						</tr>
						<tr>
							<td>Ohio</td>
							<td><strong>+1.31</strong></td>
							<td>+0.20</td>
							<td>-1.11</td>
						</tr>
					</tbody>
				</table>
				<p class="table-note">*DC is a federal district, not directly comparable to states. Its +1.87 SD gap reflects unique urban dynamics and federal workforce composition.</p>
			</div>

			<div class="state-box state-box--equity">
				<h4>Smallest Gaps or Reversed Patterns</h4>
				<table>
					<thead>
						<tr>
							<th>State</th>
							<th>Gap (SD)</th>
							<th>Bonferroni</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>New York</td>
							<td>+0.12</td>
							<td>Yes</td>
						</tr>
						<tr>
							<td>Arizona</td>
							<td>+0.00</td>
							<td>No</td>
						</tr>
						<tr>
							<td>California</td>
							<td><strong>-0.15</strong></td>
							<td><strong>Yes</strong></td>
						</tr>
						<tr>
							<td>Washington</td>
							<td><strong>-0.42</strong></td>
							<td><strong>Yes</strong></td>
						</tr>
					</tbody>
				</table>
				<p class="table-note">Bonferroni threshold: α = 0.05/43 = 0.00116. 28 of 43 state comparisons survived correction. Oregon (-0.53, p=0.03, only 13 MM tracts) and Nevada (-0.12) did not survive and are excluded.</p>
			</div>
		</div>

		<p>
			<strong>Interpretation:</strong> In Washington and California, majority-minority communities show
			HIGHER resilience than majority-white communities—a pattern that survives Bonferroni correction.
			This suggests that structural context, not racial composition per se, is associated with
			community resilience.
		</p>

		<h3>3.5 Finding 4: Who Are the Outliers?</h3>

		<div class="outlier-comparison">
			<div class="outlier-box outlier-box--high">
				<h4>High Resilience Tracts (Top 10%, score &ge; +1.11)</h4>
				<ul>
					<li><strong>N:</strong> 5,389 tracts</li>
					<li><strong>Mean % Black:</strong> 10.3% (vs. 13.4% nationally)</li>
					<li><strong>Mean % Hispanic:</strong> 17.0% (vs. 17.1% nationally)</li>
					<li><strong>Majority-minority:</strong> 26.5% (same as national)</li>
					<li><strong>Mean poverty rate:</strong> 12.5% (vs. 13.5% nationally)</li>
					<li><strong>Mean % Bachelor's+:</strong> 48.9% (vs. 32.2% nationally)</li>
				</ul>
			</div>

			<div class="outlier-box outlier-box--low">
				<h4>Low Resilience Tracts (Bottom 10%, score &le; -1.21)</h4>
				<ul>
					<li><strong>N:</strong> 5,389 tracts</li>
					<li><strong>Mean % Black:</strong> <span class="highlight">39.7%</span> (vs. 13.4% nationally)</li>
					<li><strong>Mean % Hispanic:</strong> 16.6% (vs. 17.1% nationally)</li>
					<li><strong>Majority-minority:</strong> <span class="highlight">56.2%</span> (vs. 26.4% nationally)</li>
					<li><strong>Mean poverty rate:</strong> 24.4% (vs. 13.5% nationally)</li>
					<li><strong>Mean % Bachelor's+:</strong> 19.2% (vs. 32.2% nationally)</li>
				</ul>
			</div>
		</div>

		<p>
			Low-resilience tracts are disproportionately Black (39.7% vs. 13.4%) and majority-minority
			(56.2% vs. 26.4%). High-resilience tracts are slightly less Black than average but show
			similar Hispanic composition.
		</p>
	</section>

	<section id="discussion">
		<h2>4. Discussion</h2>

		<h3>4.1 Principal Findings</h3>
		<p>
			Our analysis reveals a 0.43 standard deviation gap in community health resilience between
			majority-white and majority-minority communities nationally (multilevel z=-41.83, p&lt;0.001, 95% CI [-0.446, -0.406]).
			This gap is consistent with structural disadvantage—majority-minority communities appear to face barriers
			associated with worse health outcomes than their socioeconomic profile would predict.
		</p>
		<p>
			The state-level variation (from +1.87 SD in DC to -0.42 SD in Washington) suggests that this
			pattern is not inevitable. Two states (Washington and California) show statistically robust
			reversed patterns after Bonferroni correction. This variation is consistent with the hypothesis
			that <strong>structural context—not racial composition per se—is associated with community
			resilience</strong>, though cross-sectional design precludes causal inference.
		</p>

		<h3>4.2 The Hispanic Paradox in Resilience</h3>
		<p>
			One of our most striking findings is the near-zero correlation between percent Hispanic and
			resilience (r=+0.01), validated at r=+0.002 with USALEEP life expectancy data. This stands
			in stark contrast to the moderate negative correlation for percent Black (r=-0.34).
		</p>
		<p>
			This pattern is consistent with the well-documented "Hispanic paradox"—the observation that
			Hispanic Americans often show health outcomes similar to or better than non-Hispanic whites
			despite lower average socioeconomic status. Proposed mechanisms include healthy immigrant
			selection, protective social and family networks, and dietary patterns. This finding merits
			dedicated investigation.
		</p>

		<h3>4.3 The Education Gradient</h3>
		<p>
			Educational attainment showed the strongest positive correlation with resilience (r=+0.41, 95% CI [+0.40, +0.42]).
			This association may operate through multiple pathways:
		</p>
		<ol>
			<li><strong>Health literacy:</strong> Higher education enables better navigation of health systems</li>
			<li><strong>Employment quality:</strong> College graduates access jobs with better health benefits</li>
			<li><strong>Neighborhood selection:</strong> Education enables residential choice in healthier environments</li>
			<li><strong>Social capital:</strong> Educational networks provide health-promoting resources</li>
		</ol>
		<p>
			The policy implication is that <strong>investment in educational equity may be associated with
			improved health equity</strong>, though causal inference requires longitudinal or experimental designs.
		</p>

		<h3>4.4 Why Some States Show Equity</h3>
		<p>
			Two states—Washington and California—show statistically robust reversed patterns after
			Bonferroni correction. Potential explanations include:
		</p>
		<ol>
			<li><strong>Immigration and selection:</strong> The healthy immigrant effect may boost resilience in communities with higher foreign-born populations</li>
			<li><strong>Policy environment:</strong> State-level health and social policies may buffer structural disadvantage</li>
			<li><strong>Community organization:</strong> Strong ethnic enclaves may provide protective social capital</li>
			<li><strong>Demographic composition:</strong> The specific mix of racial/ethnic groups and their geographic distribution may matter</li>
		</ol>
		<p>
			<strong>Critical sensitivity finding:</strong> Majority-minority tracts in Washington and California have notably higher Asian composition (20.2% and 19.7%, respectively) compared to 10.0% nationally. When excluding Asian-plurality tracts from California, the "reversed" pattern disappears entirely (gap becomes +0.18 SD, favoring white-majority tracts). This suggests California's reversed pattern may be attributable primarily to tracts with high Asian composition rather than a general structural advantage for all minority groups. Washington's reversed pattern persists even after this sensitivity test, suggesting different dynamics.
		</p>
		<p>
			<strong>Important caveats:</strong> (1) "Asian-American" aggregates heterogeneous communities with vastly different health patterns (e.g., Hmong vs. Indian American). (2) We interpret this as reflecting structural factors (selective immigration policies, metropolitan healthcare infrastructure), not inherent community characteristics. (3) This pattern should not invoke "model minority" narratives.
		</p>
		<p>
			These explanations are speculative. Further research should investigate what structural
			conditions are associated with resilience equity in Washington and California, ideally using
			longitudinal or quasi-experimental designs that can better address causality.
		</p>

		<h3>4.5 Implications for Practice</h3>
		<div class="practice-implications">
			<div class="implication-box">
				<h4>1. Screen for equity in resilience-based programs</h4>
				<p>
					Before using resilience scores for resource allocation, examine whether the metric
					shows equity across community types. If majority-minority communities systematically
					score lower, the metric may encode rather than address disparities.
				</p>
			</div>
			<div class="implication-box">
				<h4>2. Target structural determinants, not communities</h4>
				<p>
					Rather than labeling communities as "low resilience" (which risks stigmatization),
					identify the structural conditions that suppress resilience: segregation, disinvestment,
					food deserts, pollution, lack of healthcare access. These conditions are actionable.
				</p>
			</div>
			<div class="implication-box">
				<h4>3. Learn from equity exemplars</h4>
				<p>
					Washington demonstrates resilience equity even after sensitivity testing; California's pattern
					requires further investigation given its dependence on Asian-plurality tracts. Specific
					majority-minority communities with high resilience offer opportunities for qualitative study.
				</p>
			</div>
			<div class="implication-box">
				<h4>4. Invest in education</h4>
				<p>
					The strong association between educational attainment and resilience suggests that
					educational equity is health equity. This requires sustained investment, not single
					interventions.
				</p>
			</div>
		</div>
	</section>

	<KeyMessages messages={keyMessages} />

	<section id="conclusion">
		<h2>5. Conclusions</h2>
		<p>
			Community health resilience is not equitably distributed. Majority-minority communities
			average 0.43 standard deviations lower resilience than majority-white communities nationally
			(multilevel z=-41.83, p&lt;0.001), and the bottom 10% of tracts are 56.2% majority-minority.
		</p>
		<p>
			State-level variation is substantial—from +1.87 SD (DC) to -0.42 SD (Washington)—and two
			states (Washington and California) show statistically robust reversed patterns after
			Bonferroni correction. This suggests that the relationship between racial composition
			and resilience is context-dependent, consistent with the role of structural factors.
		</p>
		<p>
			Educational attainment emerged as the strongest correlate of resilience (r=+0.41). Investment
			in educational equity may be associated with improved health equity.
		</p>
		<p>Practitioners should:</p>
		<ol>
			<li>Audit resilience metrics for equity before use in resource allocation</li>
			<li>Target structural determinants rather than labeling communities</li>
			<li>Learn from states and communities that achieve resilience equity</li>
			<li>Frame findings around structural barriers, not community deficits</li>
		</ol>
		<p>
			<strong>The goal is not to celebrate resilience in some communities while ignoring its
			absence in others. The goal is to create structural conditions that enable all communities
			to thrive.</strong>
		</p>
	</section>

	<section id="acknowledgments">
		<h2>Acknowledgments</h2>
		<p>
			We acknowledge the communities represented in this analysis and the structural barriers they
			face. Data alone does not solve disparities; policy action does.
		</p>
	</section>

	<section id="data-availability">
		<h2>Data Availability</h2>
		<p>
			CDC PLACES and ACS data are publicly available. Analysis code is available at:
			<a href="https://github.com/cschuman/resilience-mapping">github.com/cschuman/resilience-mapping</a>
		</p>
	</section>
</PaperLayout>

<style>
	/* Results tables */
	.results-table {
		margin: var(--space-6) 0;
		overflow-x: auto;
	}

	.results-table h4 {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-bottom: var(--space-3);
	}

	.results-table table {
		width: 100%;
		border-collapse: collapse;
		font-size: var(--text-sm);
	}

	.results-table th,
	.results-table td {
		padding: var(--space-3);
		border: 1px solid var(--color-border-subtle);
		text-align: left;
	}

	.results-table th {
		background: var(--color-foundation-mid);
		font-weight: var(--font-weight-semibold);
	}

	.results-table .highlight-row {
		background: var(--color-accent-primary-glow);
	}

	.results-table .highlight-row.positive {
		background: rgba(78, 167, 117, 0.15);
	}

	.results-table .highlight-row.negative {
		background: rgba(209, 104, 71, 0.15);
	}

	.table-note {
		font-size: var(--text-xs);
		color: var(--color-text-muted);
		margin-top: var(--space-2);
	}

	/* State comparison boxes */
	.state-comparison {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
		gap: var(--space-4);
		margin: var(--space-6) 0;
	}

	.state-box {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-lg);
		padding: var(--space-4);
	}

	.state-box h4 {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		margin-bottom: var(--space-3);
	}

	.state-box table {
		width: 100%;
		border-collapse: collapse;
		font-size: var(--text-xs);
	}

	.state-box th,
	.state-box td {
		padding: var(--space-2);
		border: 1px solid var(--color-border-subtle);
		text-align: left;
	}

	.state-box th {
		background: var(--color-foundation-surface);
	}

	.state-box--large-gap {
		border-color: rgba(209, 104, 71, 0.3);
	}

	.state-box--large-gap h4 {
		color: var(--color-score-low);
	}

	.state-box--equity {
		border-color: rgba(78, 167, 117, 0.3);
	}

	.state-box--equity h4 {
		color: var(--color-score-high);
	}

	/* Outlier comparison */
	.outlier-comparison {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: var(--space-4);
		margin: var(--space-6) 0;
	}

	.outlier-box {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-lg);
		padding: var(--space-4);
	}

	.outlier-box h4 {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		margin-bottom: var(--space-3);
	}

	.outlier-box ul {
		margin: 0;
		padding-left: var(--space-4);
		font-size: var(--text-sm);
	}

	.outlier-box li {
		margin-bottom: var(--space-2);
	}

	.outlier-box--high {
		border-color: rgba(78, 167, 117, 0.3);
	}

	.outlier-box--high h4 {
		color: var(--color-score-high);
	}

	.outlier-box--low {
		border-color: rgba(209, 104, 71, 0.3);
	}

	.outlier-box--low h4 {
		color: var(--color-score-low);
	}

	.outlier-box .highlight {
		font-weight: var(--font-weight-bold);
		color: var(--color-score-low);
	}

	/* Practice implications */
	.practice-implications {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: var(--space-4);
		margin: var(--space-6) 0;
	}

	.implication-box {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-lg);
		padding: var(--space-4);
	}

	.implication-box h4 {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		color: var(--color-accent-primary);
		margin-bottom: var(--space-2);
	}

	.implication-box p {
		font-size: var(--text-sm);
		margin: 0;
	}

	/* General content styling */
	section {
		margin-bottom: var(--space-8);
	}

	h2 {
		font-family: var(--font-display);
		font-size: var(--text-xl);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-top: var(--space-10);
		margin-bottom: var(--space-4);
		padding-bottom: var(--space-2);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	h3 {
		font-size: var(--text-lg);
		font-weight: var(--font-weight-semibold);
		color: var(--color-text-primary);
		margin-top: var(--space-6);
		margin-bottom: var(--space-3);
	}

	p {
		margin-bottom: var(--space-4);
		line-height: var(--leading-relaxed);
	}

	ul,
	ol {
		margin-bottom: var(--space-4);
		padding-left: var(--space-6);
	}

	li {
		margin-bottom: var(--space-2);
	}

	a {
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	a:hover {
		text-decoration: underline;
	}

	/* Context sections */
	.context-section {
		background: linear-gradient(135deg, var(--color-foundation-mid), rgba(209, 104, 71, 0.1));
		border: 1px solid rgba(209, 104, 71, 0.3);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
		margin: var(--space-8) 0;
	}

	.context-section h2 {
		margin-top: 0;
		color: var(--color-score-low);
		border-bottom: none;
		padding-bottom: 0;
	}

	.context-section p {
		color: var(--color-text-secondary);
	}
</style>
