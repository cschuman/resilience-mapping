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

	const paperMeta = {
		title: 'Regression to the Mean in Small-Area Health Estimates',
		subtitle: 'Why CDC PLACES-Based Trajectory Prediction Fails',
		authors: ['Corey Schuman, MS'],
		correspondence: 'cschuman@odds.health',
		targetJournal: 'American Journal of Epidemiology',
		wordCount: '5,023',
		status: 'preprint' as const,
		doi: undefined,
		publishedDate: undefined
	};

	// LEAD WITH THE FINDING
	const abstract = {
		background:
			'We tried to predict which communities would get healthier or sicker—and failed completely. Our best machine learning models achieved F1=0.26, indistinguishable from random guessing. This paper explains why: the year-over-year "changes" in CDC PLACES data are mostly measurement noise, not real health trends.',
		objective:
			'To investigate why trajectory prediction fails for CDC PLACES small-area health estimates and determine whether the failure reflects measurement error or genuine unpredictability in community health dynamics.',
		methods:
			'We analyzed autocorrelation structure of year-over-year changes in a Composite Health Burden Index (CHBI) across 72,161 census tracts. We stratified by prior change magnitude to distinguish regression to the mean from true mean-reverting dynamics.',
		results:
			'Year-over-year changes showed strong negative autocorrelation (r = -0.22 to -0.58). Critically, this correlation scaled with prior change magnitude: near-zero (r = -0.05) for small prior changes, strongly negative (r = -0.61) for extreme prior changes. This quintile gradient is consistent with regression to the mean. However, CHBI levels were 99.7% persistent—community health burden itself is highly stable.',
		conclusions:
			'Annual trajectory labels ("improving," "declining") based on PLACES data are unreliable and should not be used for resource allocation. Focus on burden levels, not year-over-year changes. Use 3-year rolling averages when trend information is needed.',
		keywords: [
			'small-area estimation',
			'regression to the mean',
			'health disparities',
			'CDC PLACES',
			'trajectory prediction',
			'measurement error'
		]
	};

	// Paper-specific misuse warnings
	const misuseWarnings = [
		'Claim that community health is fundamentally unpredictable (levels are 99.7% stable)',
		'Argue that investment in high-burden communities is futile',
		'Use single-year PLACES changes to justify reducing funding to "improving" areas',
		'Create "early warning systems" based on annual PLACES trajectory labels',
		'Remove trajectory monitoring entirely (use 3-year rolling averages instead)'
	];

	const limitations = [
		{
			title: 'Cannot fully exclude true dynamics',
			description:
				'While the quintile gradient strongly suggests regression to the mean dominates, we cannot completely rule out some component of genuine mean-reverting health dynamics.'
		},
		{
			title: 'Year-pair instability unexplained',
			description:
				'Autocorrelation varied substantially between year-pairs (r = -0.58 for 2022-2023 vs r = -0.22 for 2023-2024). This may reflect COVID effects, methodology changes, or sample attrition.'
		},
		{
			title: 'Specific to CDC PLACES',
			description:
				'Findings apply to CDC PLACES tract-level estimates. State-level BRFSS, Medicare claims, or other data sources may support more reliable trajectory analysis.'
		},
		{
			title: 'Limited time horizon',
			description:
				'Five-year PLACES time series limits ability to test longer prediction horizons. 3-year or 5-year trajectories may be more reliable than annual changes.'
		}
	];

	const keyMessages = [
		{
			audience: 'Health Departments',
			message:
				'Remove trajectory labels from dashboards. A tract classified as "improving" is more likely to be "declining" next year than to stay "improving." Focus on burden levels.',
			icon: 'policy'
		},
		{
			audience: 'Researchers',
			message:
				'Before interpreting negative autocorrelation as mean reversion, conduct stratified RTM analysis. If correlation scales with extremity, measurement error likely dominates.',
			icon: 'research'
		},
		{
			audience: 'Funders',
			message:
				'Don\'t reduce investment in communities showing single-year "improvement." Apparent gains often reflect noise. Sustained investment requires sustained commitment.',
			icon: 'community'
		}
	];
</script>

<PaperLayout
	title={paperMeta.title}
	subtitle={paperMeta.subtitle}
	authors={paperMeta.authors}
	correspondence={paperMeta.correspondence}
	targetJournal={paperMeta.targetJournal}
	wordCount={paperMeta.wordCount}
	status={paperMeta.status}
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
		<h4>What we tried to do</h4>
		<p>
			We built machine learning models to predict which neighborhoods would get healthier or
			sicker next year. If this worked, health departments could intervene <em>before</em>
			problems develop instead of reacting after.
		</p>

		<h4>What happened</h4>
		<p>
			Total failure. Our predictions were no better than flipping a coin. A neighborhood
			labeled "improving" one year was actually <em>more likely</em> to be labeled "declining"
			the next year than to keep improving.
		</p>

		<h4>Why it failed</h4>
		<p>
			The year-to-year "changes" in CDC health data are mostly measurement noise, not real
			health trends. It's like weighing yourself on a wobbly scale—the number bounces around,
			but your actual weight hasn't changed.
		</p>

		<h4>The good news</h4>
		<p>
			While year-to-year <em>changes</em> are noisy, the underlying health <em>levels</em>
			are 99.7% stable. High-burden communities stay high-burden. This is actionable: focus
			on where the burden IS, not where you think it's going.
		</p>
	</PlainLanguageSummary>

	<EquityWarning
		status="Equity analysis not yet conducted"
		estimatedCompletion="Paper 4 in series"
	/>

	<MisuseWarning warnings={misuseWarnings} />

	<section id="why-publishing" class="context-section">
		<h2>Why We're Publishing This</h2>
		<p>
			<strong>We spent months building prediction models that don't work.</strong> Machine
			learning, gradient boosting, 47 features, careful cross-validation—and the result was
			indistinguishable from random guessing.
		</p>
		<p>
			<strong>This matters because "early warning systems" are tempting.</strong> Health
			departments want to identify communities that will decline so they can intervene early.
			Funders want to predict which investments will pay off. The appeal is obvious.
		</p>
		<p>
			But with CDC PLACES data, these systems cannot work as intended. We're publishing this
			so others don't waste resources chasing the same dead end—and so practitioners know
			to focus on burden levels rather than trajectory labels.
		</p>
	</section>

	<LimitationBox {limitations} />

	<section id="introduction">
		<h2>Introduction</h2>
		<p>
			The promise of predictive analytics in public health has generated substantial interest
			in developing "early warning systems" that could identify communities at risk of health
			decline before deterioration occurs. Such systems could theoretically enable proactive
			resource allocation, allowing health departments to intervene in communities predicted
			to decline rather than reacting after problems emerge.
		</p>
		<p>
			We undertook a systematic effort to develop such a prediction system. Using five years
			of CDC PLACES data (2020-2024) covering 72,161 census tracts, we constructed a Composite
			Health Burden Index (CHBI) and attempted to predict which communities would improve,
			decline, or remain stable. We employed gradient-boosted decision trees with 47 features
			including prior trajectories, spatial context, and demographic covariates.
		</p>
		<p>
			Despite this comprehensive approach, our best models achieved only <strong>F1=0.26</strong>—performance
			indistinguishable from random classification. Feature importance analysis revealed that
			prior trajectory features contributed <em>negatively</em> to model performance. Adding
			these features made predictions worse, not better.
		</p>
		<p>
			This counterintuitive finding demanded explanation.
		</p>
	</section>

	<section id="the-stakes">
		<h2>The Stakes of Trajectory Prediction</h2>
		<p>
			The practical stakes are considerable. If trajectory prediction were reliable, it could
			enable anticipatory intervention—deploying resources before health deterioration becomes
			entrenched.
		</p>
		<p>
			However, <strong>unreliable trajectory prediction could cause harm</strong>. Labeling a
			community as "declining" based on noisy data could trigger unnecessary intervention while
			diverting resources from communities with genuine need. Labeling a community as "improving"
			could justify inaction when intervention is warranted.
		</p>
		<p>
			Beyond resource allocation, trajectory labels affect community narratives. Being labeled
			a "declining" community may discourage investment, affect property values, or stigmatize
			residents—even if the label reflects measurement error rather than genuine health trends.
		</p>
	</section>

	<section id="methods">
		<h2>Methods</h2>

		<h3>Data Source</h3>
		<p>
			We obtained CDC PLACES data for release years 2020-2024, which provide model-based
			small-area estimates of health outcomes for all U.S. census tracts. CDC PLACES uses
			multilevel regression and poststratification (MRP), combining BRFSS survey data with
			American Community Survey demographics.
		</p>

		<h3>Composite Health Burden Index</h3>
		<p>
			We constructed a CHBI as the arithmetic mean of seven standardized PLACES measures:
			obesity, diabetes, coronary heart disease, high blood pressure, smoking, lack of
			insurance, and physical inactivity.
		</p>

		<h3>Trajectory Classification</h3>
		<p>Three classes based on year-over-year CHBI change:</p>
		<ul>
			<li><strong>Improving:</strong> CHBI decreased by &gt;0.3 SD</li>
			<li><strong>Declining:</strong> CHBI increased by &gt;0.3 SD</li>
			<li><strong>Stable:</strong> CHBI change within ±0.3 SD</li>
		</ul>

		<h3>Distinguishing RTM from True Dynamics</h3>
		<p>
			Under regression to the mean (RTM), negative autocorrelation should be stronger for
			extreme prior changes—because extreme observations are more likely to reflect measurement
			error. We stratified tracts into quintiles by prior change magnitude and computed
			autocorrelation within each quintile.
		</p>
	</section>

	<section id="results">
		<h2>Results</h2>

		<h3>Prediction Performance</h3>
		<div class="results-table">
			<table>
				<thead>
					<tr>
						<th>Metric</th>
						<th>Value</th>
						<th>Random Baseline</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td>Macro F1</td>
						<td>0.26</td>
						<td>0.25</td>
					</tr>
					<tr>
						<td>Balanced Accuracy</td>
						<td>0.33</td>
						<td>0.33</td>
					</tr>
				</tbody>
			</table>
		</div>
		<p>
			Performance was indistinguishable from chance. Prior trajectory features had
			<em>negative</em> SHAP values—including them made predictions worse.
		</p>

		<h3>The Quintile Gradient</h3>
		<div class="results-table">
			<table>
				<thead>
					<tr>
						<th>Prior Change Quintile</th>
						<th>Correlation (r)</th>
						<th>Variance Explained</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td>Q1 (smallest changes)</td>
						<td>-0.05</td>
						<td>0.3%</td>
					</tr>
					<tr>
						<td>Q2</td>
						<td>-0.16</td>
						<td>2.4%</td>
					</tr>
					<tr>
						<td>Q3</td>
						<td>-0.29</td>
						<td>8.1%</td>
					</tr>
					<tr>
						<td>Q4</td>
						<td>-0.42</td>
						<td>17.7%</td>
					</tr>
					<tr>
						<td>Q5 (largest changes)</td>
						<td>-0.61</td>
						<td>37.0%</td>
					</tr>
				</tbody>
			</table>
		</div>
		<p>
			<strong>This gradient is the signature of regression to the mean.</strong> Only extreme
			prior changes show strong negative autocorrelation. Near-zero correlation for small
			changes indicates no genuine mean reversion among stable tracts.
		</p>

		<h3>Level Persistence</h3>
		<p>
			Despite unstable year-over-year changes, CHBI <em>levels</em> were highly persistent:
		</p>
		<div class="highlight-box">
			<p class="highlight-stat">R² = 99.7%</p>
			<p class="highlight-label">of next-year health burden explained by current burden</p>
		</div>
		<p>
			High-burden communities remain high-burden. The "unpredictability" is confined to
			year-over-year noise, not to underlying health status.
		</p>
	</section>

	<section id="discussion">
		<h2>Discussion</h2>

		<h3>Principal Findings</h3>
		<p>
			Trajectory prediction failed because year-over-year changes in PLACES estimates contain
			substantial measurement error. The quintile gradient—where extreme changes show strong
			reversion but small changes show none—is consistent with regression to the mean as the
			dominant mechanism.
		</p>

		<h3>Implications for Practice</h3>
		<ul>
			<li>
				<strong>Avoid trajectory labels.</strong> A tract classified as "improving" is more
				likely to be "declining" next year than to remain "improving."
			</li>
			<li>
				<strong>Focus on levels, not changes.</strong> CHBI levels are 99.7% persistent.
				High-burden tracts remain high-burden—this is actionable.
			</li>
			<li>
				<strong>Use 3-year rolling averages.</strong> Multi-year averages smooth measurement
				noise when trend information is needed.
			</li>
			<li>
				<strong>Build monitoring systems, not early warning systems.</strong> Prediction
				cannot work; responsive monitoring can.
			</li>
		</ul>

		<h3>What This Means for CDC PLACES</h3>
		<p>
			These findings do not impugn CDC PLACES—they identify appropriate and inappropriate uses.
			PLACES excels at cross-sectional snapshots: identifying high-burden areas for targeting.
			The limitation concerns longitudinal trajectory analysis, where model-based estimation
			may introduce systematic artifacts.
		</p>
	</section>

	<section id="conclusions">
		<h2>Conclusions</h2>
		<p>
			The failure of CDC PLACES-based trajectory prediction (F1=0.26) is consistent with
			regression to the mean in small-area health estimates. Annual trajectory labels are
			unreliable and should not be used for resource allocation.
		</p>
		<p><strong>Specific recommendations:</strong></p>
		<ol>
			<li>Remove trajectory labels from Community Health Improvement Plans and dashboards</li>
			<li>Focus resource allocation on current burden levels, which are stable and reliable</li>
			<li>Use three-year rolling averages when trend information is needed</li>
			<li>Target communities with persistently high burden (3+ years above threshold)</li>
			<li>Build responsive monitoring systems rather than predictive early warning systems</li>
		</ol>
		<p>
			We close by emphasizing what our findings do <em>not</em> mean. Community health is not
			chaotic—levels are 99.7% stable. The challenge is that annual changes in PLACES estimates
			are too noisy to support trajectory prediction. Better measurement could enable better
			prediction; in the interim, focusing on burden levels represents the most defensible
			use of available data.
		</p>
	</section>

	<KeyMessages messages={keyMessages} />
</PaperLayout>

<style>
	section {
		margin-bottom: var(--space-10);
	}

	h2 {
		font-family: var(--font-display);
		font-size: var(--text-2xl);
		font-weight: var(--font-weight-normal);
		color: var(--color-text-primary);
		margin-bottom: var(--space-5);
		padding-bottom: var(--space-3);
		border-bottom: 1px solid var(--color-border-subtle);
		letter-spacing: var(--tracking-display);
	}

	h3 {
		font-size: var(--text-lg);
		font-weight: var(--font-weight-semibold);
		color: var(--color-accent-primary);
		margin-top: var(--space-6);
		margin-bottom: var(--space-3);
	}

	p {
		font-size: var(--text-base);
		line-height: var(--leading-relaxed);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-4);
	}

	ul,
	ol {
		margin-bottom: var(--space-4);
		padding-left: var(--space-6);
	}

	li {
		font-size: var(--text-base);
		line-height: var(--leading-relaxed);
		color: var(--color-text-secondary);
		margin-bottom: var(--space-2);
	}

	li strong {
		color: var(--color-text-primary);
	}

	em {
		font-style: italic;
		color: var(--color-text-primary);
	}

	/* Results tables */
	.results-table {
		margin: var(--space-5) 0;
		overflow-x: auto;
	}

	table {
		width: 100%;
		border-collapse: collapse;
		font-size: var(--text-sm);
	}

	th {
		text-align: left;
		padding: var(--space-3) var(--space-4);
		background: var(--color-foundation-surface);
		color: var(--color-text-primary);
		font-weight: var(--font-weight-semibold);
		border-bottom: 2px solid var(--color-border-default);
	}

	td {
		padding: var(--space-3) var(--space-4);
		color: var(--color-text-secondary);
		border-bottom: 1px solid var(--color-border-subtle);
	}

	tr:hover td {
		background: var(--color-foundation-mid);
	}

	/* Highlight box */
	.highlight-box {
		background: linear-gradient(135deg, var(--color-foundation-mid), var(--color-accent-primary-glow));
		border: 1px solid var(--color-accent-primary);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
		text-align: center;
		margin: var(--space-6) 0;
	}

	.highlight-stat {
		font-family: var(--font-display);
		font-size: var(--text-4xl);
		font-weight: var(--font-weight-bold);
		color: var(--color-accent-primary);
		margin-bottom: var(--space-2);
	}

	.highlight-label {
		font-size: var(--text-base);
		color: var(--color-text-secondary);
		margin: 0;
	}

	/* Context sections */
	.context-section {
		background: linear-gradient(135deg, var(--color-foundation-mid), var(--color-accent-primary-glow));
		border: 1px solid var(--color-accent-primary);
		border-radius: var(--radius-xl);
		padding: var(--space-6);
		margin: var(--space-8) 0;
	}

	.context-section h2 {
		margin-top: 0;
		color: var(--color-accent-primary);
		border-bottom: none;
		padding-bottom: 0;
	}

	.context-section p {
		color: var(--color-text-secondary);
	}

	/* Links */
	a {
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	a:hover {
		text-decoration: underline;
	}
</style>
