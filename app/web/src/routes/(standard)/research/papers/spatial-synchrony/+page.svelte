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
		title: 'Spatial Synchrony, Not Contagion: A Methodological Correction in Community Health Trajectory Prediction',
		authors: ['Corey Schuman'],
		publishedDate: '2024-12-30',
		version: '1.0.0',
		status: 'preprint' as const,
		pdfUrl: '/research/papers/spatial-synchrony-v1.0.0.pdf'
	};

	// REVISED ABSTRACT: Lead with the finding, not the error
	const abstract = {
		background:
			'We found no evidence that neighboring community health trajectories predict focal community trajectories. The apparent "spatial contagion" reported in preliminary analyses—where neighbor trajectories appeared 3.8x more predictive than a community\'s own history—was entirely due to temporal data leakage in our feature construction.',
		objective:
			'To test whether the spatial contagion effect was genuine or an artifact of improper temporal alignment (using future data to predict the future).',
		methods:
			'We analyzed 189,566 tract-year observations from 72,161 U.S. census tracts using CDC PLACES data (2020-2024). We compared leaked features (using year T data to predict year T outcomes) versus properly lagged features (using only year T-1 and earlier). We used permutation importance with bootstrap confidence intervals on held-out 2024 data.',
		results:
			'The spatial contagion effect vanished when we fixed the temporal alignment. With leaked features, neighbor change was 16.7x more important than own-tract change. With proper lagging, both had negligible importance (ratio: 1.12x, overlapping CIs). Critical context: even our best model achieves only F1=0.26—meaning no features we tested enable meaningful trajectory prediction.',
		conclusions:
			'Communities exhibit spatial synchrony (changing together due to shared labor markets, healthcare systems, and policies) but NOT predictive contagion. Don\'t expect health improvements to "spread" to neighbors—address root causes directly.',
		keywords: [
			'spatial epidemiology',
			'temporal data leakage',
			'health trajectories',
			'methodological correction',
			'CDC PLACES',
			'spatial synchrony'
		]
	};

	// Paper-specific misuse warnings
	const misuseWarnings = [
		'Justify cuts to regional or spatial public health programs',
		'Claim geographic factors are irrelevant to health (shared regional causes matter enormously)',
		'Defund health equity initiatives based on "no spatial contagion"',
		'Assume our predictive failure means intervention failure (prediction ≠ causation)',
		'Ignore labor markets, healthcare systems, and policies that create spatial patterns'
	];

	const limitations = [
		{
			title: 'Modeled estimates',
			description:
				'CDC PLACES provides modeled estimates, not direct measurements. Spatial smoothing in the MRP methodology may contribute to apparent spatial patterns.'
		},
		{
			title: 'COVID-19 period',
			description:
				'The 2020-2024 study period includes unprecedented pandemic health shocks that may not reflect normal spatial dynamics.'
		},
		{
			title: 'Arbitrary boundaries',
			description:
				'Census tracts are arbitrary administrative units. The Modifiable Areal Unit Problem (MAUP) means findings may differ at other scales.'
		},
		{
			title: 'Single spatial weights',
			description:
				'We used Queen contiguity exclusively (mean 6.2 neighbors). Alternative specifications might yield different results.'
		},
		{
			title: 'No equity analysis',
			description:
				'We did not examine whether model performance or spatial patterns differ by neighborhood racial/ethnic composition.'
		},
		{
			title: 'Poor baseline performance',
			description:
				'Even our best model achieves only F1=0.26. The negative finding about spatial features is within a context where no features predict well.'
		}
	];

	const keyMessages = [
		{
			title: 'No evidence of geographic "spillover" effects',
			description:
				'Health improvements in one community do not appear to spread to neighbors. Do not design interventions expecting diffusion.'
		},
		{
			title: 'Communities change together due to shared causes',
			description:
				'Regional patterns reflect common exposures (labor markets, healthcare systems, policy) not causal contagion.'
		},
		{
			title: 'Target root causes, not geography',
			description:
				'Effective interventions must address the shared factors driving regional patterns, not assume geographic proximity enables diffusion.'
		},
		{
			title: 'Prediction of trajectories remains difficult',
			description:
				'Current data and methods cannot reliably predict which communities will improve or decline. "Early warning systems" based on these models would generate mostly false alarms.'
		},
		{
			title: 'Methodological caution for researchers',
			description:
				'Spatial features must use only pre-outcome data. Temporal leakage can create dramatic but spurious findings.'
		}
	];
</script>

<svelte:head>
	<title>{paper.title} | odds.health Research</title>
	<meta
		name="description"
		content="Peer-reviewed methodological correction showing apparent spatial contagion in community health was a temporal leakage artifact."
	/>

	<!-- Open Graph -->
	<meta property="og:type" content="article" />
	<meta property="og:title" content={paper.title} />
	<meta
		property="og:description"
		content="Communities exhibit spatial synchrony—they change together—but prior neighbor trajectories do not predict future focal trajectories."
	/>
	<meta property="og:image" content="https://odds.health/og-image.svg" />

	<!-- Google Scholar -->
	<meta name="citation_title" content={paper.title} />
	<meta name="citation_author" content="Schuman, Corey" />
	<meta name="citation_publication_date" content="2024/12/30" />
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
			Health changes don't "spread" from one neighborhood to its neighbors like a virus. When we
			see whole regions getting healthier or sicker at the same time, it's because they share the
			same underlying problems—not because change spreads from place to place.
		</p>

		<h4>What went wrong in our first analysis</h4>
		<p>
			We accidentally used data from the future to predict the future. Imagine trying to predict
			tomorrow's weather by peeking at tomorrow's weather report—you'd seem like an amazing
			forecaster, but you'd be cheating. That's what we did with neighborhood health data.
		</p>

		<h4>What's really happening</h4>
		<p>
			Nearby neighborhoods change at the SAME TIME because they share the same jobs, hospitals,
			pollution, and policies. They're not influencing each other—they're just riding the same
			waves.
		</p>

		<h4>Why this matters for policy</h4>
		<p>
			Don't expect health improvements in one community to automatically spread to neighbors.
			If you want healthier communities, you have to fix what's actually making people sick—the
			shared root causes—not hope that good health will somehow flow across neighborhood boundaries.
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
			<strong>We got it wrong, and that matters.</strong> Our preliminary analysis suggested a
			dramatic finding: that health changes "spread" across community boundaries with neighbor
			trajectories being 3.8x more predictive than a community's own history. This would have
			been a paradigm shift in public health intervention design.
		</p>
		<p>
			<strong>It was wrong.</strong> What we found was an artifact of a methodological error
			called temporal data leakage—we accidentally used future data to predict the future.
			When we fixed the error, the "spatial contagion" effect vanished completely.
		</p>
		<p>
			We're publishing this correction prominently because:
		</p>
		<ul>
			<li>
				<strong>Science requires transparency about errors.</strong> Burying mistakes creates
				a misleading scientific record.
			</li>
			<li>
				<strong>This error is easy to make.</strong> Others working with spatial health data
				may benefit from seeing how temporal leakage manifests.
			</li>
			<li>
				<strong>The negative finding matters for policy.</strong> Interventions designed around
				"spillover effects" would waste resources if those effects don't exist.
			</li>
			<li>
				<strong>Trust requires honesty.</strong> We want policymakers to trust our findings—and
				that means being upfront about what we got wrong.
			</li>
		</ul>
	</section>

	<LimitationBox {limitations} />

	<section id="introduction">
		<h2>1. Introduction</h2>

		<h3>1.1 The Spatial Contagion Hypothesis</h3>
		<p>
			A compelling hypothesis in spatial epidemiology posits that health changes "spread" across
			community boundaries—that a community's health trajectory is influenced not just by its own
			characteristics but by the trajectories of its neighbors. This "spatial contagion" framing
			draws on social network research demonstrating the spread of behaviors through connected
			individuals and neighborhood effects theory suggesting that place-based exposures propagate
			across geographic boundaries.
		</p>
		<p>
			Initial analyses of CDC PLACES tract-level health data appeared to support this hypothesis
			dramatically. Preliminary models suggested that the average health trajectory of neighboring
			census tracts was <strong>3.8 times more predictive</strong> of a focal tract's future
			trajectory than the tract's own historical trend—a finding that, if valid, would represent a
			paradigm shift in how we conceptualize community health interventions.
		</p>

		<h3>1.2 The Problem of Temporal Leakage</h3>
		<p>
			However, this striking finding warranted methodological scrutiny. A critical question emerged:
			<strong>When computing "neighbor trajectory," what time period is used?</strong>
		</p>
		<p>
			In predictive modeling, features must be constructed using only information available
			<em>before</em> the outcome period. If predicting health trajectory from year T-1 to year T,
			legitimate predictive features can only use data from years T-2, T-3, etc. Using data from
			year T in feature construction constitutes <strong>temporal data leakage</strong>—the model
			appears predictive because it "sees" contemporaneous information, not because it captures
			genuine predictive signal.
		</p>
		<p>This distinction matters enormously for the spatial contagion hypothesis:</p>
		<ul>
			<li>
				<strong>Contemporaneous correlation:</strong> Neighbors change together at the same time
				(spatial synchrony)
			</li>
			<li>
				<strong>Predictive contagion:</strong> Prior neighbor change predicts future focal change
			</li>
		</ul>
		<p>Only the second supports policy interventions targeting spatial spillovers.</p>
	</section>

	<section id="methods">
		<h2>2. Methods</h2>

		<h3>2.1 Data Source and Sample</h3>
		<p>
			We analyzed CDC PLACES tract-level health estimates from 2020-2026 releases, harmonized to a
			consistent panel structure. The analytic sample comprised <strong>189,566 tract-year
			observations</strong> from <strong>72,161 unique census tracts</strong> across 51 states and
			territories, with prediction years 2022, 2023, and 2024.
		</p>

		<h3>2.2 Outcome Variable</h3>
		<p>
			We constructed a Composite Health Burden Index (CHBI) as a weighted average of seven PLACES
			measures: obesity (20%), diabetes (20%), coronary heart disease (15%), mental health days
			(15%), hypertension (10%), physical inactivity (10%), and physical health days (10%). Tracts
			were classified as DECLINE (>0.3 SD increase in CHBI), STABLE, or IMPROVE (&lt;0.3 SD
			decrease).
		</p>

		<h3>2.3 Spatial Feature Construction</h3>
		<p>
			We built a Queen contiguity neighbor graph from Census TIGER/Line tract geometries (mean: 6.2
			neighbors per tract). The critical methodological comparison involved two specifications:
		</p>

		<div class="method-comparison">
			<div class="method-box method-box--wrong">
				<h4>Specification A: Contemporaneous (Leaked)</h4>
				<ul>
					<li><code>neighbor_avg_change</code>: Mean neighbor CHBI change from year T-1 to year T</li>
					<li><code>neighbor_avg_chbi</code>: Mean neighbor CHBI in year T</li>
				</ul>
				<p class="method-problem">Problem: Uses year T data to predict year T outcome</p>
			</div>

			<div class="method-box method-box--correct">
				<h4>Specification B: Properly Lagged</h4>
				<ul>
					<li><code>neighbor_avg_change</code>: Mean neighbor CHBI change from year T-2 to year T-1</li>
					<li><code>neighbor_avg_chbi</code>: Mean neighbor CHBI in year T-1</li>
				</ul>
				<p class="method-correct">Correct: Uses only pre-outcome information</p>
			</div>
		</div>

		<h3>2.4 Model Training and Evaluation</h3>
		<p>
			We trained XGBoost classifiers with temporal cross-validation (train: 2022-2023; test: 2024).
			To assess feature importance, we used:
		</p>
		<ol>
			<li>Permutation importance on the holdout test set (10 repeats, 95% bootstrap CIs)</li>
			<li>Ablation experiments: Model performance with (a) all features, (b) no spatial features, (c) spatial features only</li>
			<li>Linear regression baseline comparing R² with and without spatial features</li>
		</ol>
	</section>

	<section id="results">
		<h2>3. Results</h2>

		<h3>3.1 The Temporal Leakage Effect</h3>

		<div class="results-table">
			<h4>Table 1. Permutation Importance on Holdout Data (2024)</h4>
			<table>
				<thead>
					<tr>
						<th>Feature</th>
						<th>Contemporaneous (Leaked)</th>
						<th>Properly Lagged</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td>neighbor_avg_change</td>
						<td>0.0390 [0.037, 0.042]</td>
						<td>0.0010 [0.0009, 0.0012]</td>
					</tr>
					<tr>
						<td>CHBI_change_1yr</td>
						<td>0.0023 [0.002, 0.003]</td>
						<td>0.0009 [0.0006, 0.0013]</td>
					</tr>
					<tr class="highlight-row">
						<td><strong>Ratio</strong></td>
						<td><strong>16.7x</strong></td>
						<td><strong>1.12x</strong></td>
					</tr>
					<tr class="highlight-row">
						<td><strong>CIs Overlap?</strong></td>
						<td><strong>No</strong></td>
						<td><strong>Yes</strong></td>
					</tr>
				</tbody>
			</table>
		</div>

		<p>
			With contemporaneous features, <code>neighbor_avg_change</code> appeared 16.7 times more
			important than own-tract change, with non-overlapping confidence intervals suggesting
			statistical significance. <strong>After correction, the ratio dropped to 1.12x with
			overlapping CIs—no significant difference.</strong>
		</p>

		<h3>3.2 Ablation Experiments</h3>

		<div class="results-table">
			<h4>Table 2. Ablation Experiment Results (Macro-F1 with 95% Bootstrap CIs)</h4>
			<table>
				<thead>
					<tr>
						<th>Model</th>
						<th>Contemporaneous</th>
						<th>Properly Lagged [95% CI]</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td>Full model (all features)</td>
						<td>0.320</td>
						<td>0.260 [0.259, 0.261]</td>
					</tr>
					<tr>
						<td>No spatial features</td>
						<td>0.261</td>
						<td>0.261 [0.260, 0.263]</td>
					</tr>
					<tr>
						<td>Spatial features only</td>
						<td>0.415</td>
						<td>0.259 [0.258, 0.260]</td>
					</tr>
					<tr class="highlight-row">
						<td><strong>Spatial contribution</strong></td>
						<td><strong>+18.2%</strong></td>
						<td><strong>-0.4%</strong></td>
					</tr>
				</tbody>
			</table>
		</div>

		<p>
			With leaked features, spatial-only models (F1=0.415) dramatically outperformed the full
			model—an impossibility in proper machine learning that signals data leakage. After correction,
			<strong>confidence intervals for all three model specifications overlap</strong>, confirming
			no statistically significant difference.
		</p>

		<h3>3.3 Spatial Autocorrelation</h3>

		<div class="results-table">
			<h4>Table 3. Global Moran's I with Significance Testing</h4>
			<table>
				<thead>
					<tr>
						<th>Variable</th>
						<th>Moran's I</th>
						<th>Z-score</th>
						<th>p-value</th>
						<th>Interpretation</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td>CHBI levels</td>
						<td>0.757</td>
						<td>254.0</td>
						<td>&lt;0.001</td>
						<td>Very strong positive autocorrelation</td>
					</tr>
					<tr>
						<td>Trajectory outcomes</td>
						<td>0.211</td>
						<td>69.7</td>
						<td>&lt;0.001</td>
						<td>Moderate clustering</td>
					</tr>
				</tbody>
			</table>
		</div>

		<p>
			Both statistics are highly significant (p&lt;0.001), confirming strong spatial structure in
			health outcomes. Communities near each other have similar health burdens (I=0.76) and somewhat
			similar trajectory outcomes (I=0.21). However, <strong>this spatial clustering does not
			translate to predictive contagion</strong>—knowing neighbor levels does not help predict focal
			changes.
		</p>
	</section>

	<section id="discussion">
		<h2>4. Discussion</h2>

		<h3>4.1 Principal Findings</h3>
		<p>
			Our central finding is methodological: the apparent "spatial contagion" in community health
			trajectories was an artifact of temporal data leakage.
		</p>
		<p>
			When neighbor trajectory features were computed contemporaneously with the outcome period
			(year T-1 to T), they appeared 16.7 times more predictive than a community's own historical
			trend. <strong>After correcting to properly lagged features</strong> (year T-2 to T-1),
			<strong>this advantage vanished entirely.</strong>
		</p>
		<p>
			This represents <strong>spatial synchrony</strong>, not spatial contagion. Communities near
			each other experience health changes at the same time—likely due to shared exposures, economic
			shocks, policy changes, or healthcare system factors—but prior neighbor trajectories do not
			predict future focal trajectories.
		</p>

		<h3>4.2 Why This Matters</h3>
		<p>The distinction between synchrony and contagion has critical policy implications:</p>

		<div class="policy-comparison">
			<div class="policy-box">
				<h4>If contagion were real:</h4>
				<ul>
					<li>Interventions in one community could spillover to neighbors</li>
					<li>"Buffer zone" investments around improving areas would be justified</li>
					<li>Regional intervention units would be more efficient than community-level</li>
				</ul>
			</div>

			<div class="policy-box policy-box--highlight">
				<h4>Given synchrony (our finding):</h4>
				<ul>
					<li>Apparent spatial patterns reflect shared causes, not causal spillovers</li>
					<li>Targeting clusters may help efficiency but not due to propagation effects</li>
					<li>Interventions must address root causes, not rely on geographic diffusion</li>
				</ul>
			</div>
		</div>
	</section>

	<KeyMessages messages={keyMessages} />

	<section id="conclusion">
		<h2>5. Conclusions</h2>
		<p>
			We found no evidence that neighboring community health trajectories predict focal community
			trajectories beyond what the focal community's own history predicts. The striking "spatial
			contagion" finding from preliminary analyses was entirely attributable to temporal data
			leakage.
		</p>
		<p>
			Communities exhibit spatial synchrony—they change together—but this reflects shared causes,
			not causal spillovers. <strong>Public health interventions cannot rely on geographic diffusion
			effects; they must address the root causes of community health trajectories directly.</strong>
		</p>
		<p>
			This finding underscores the critical importance of methodological rigor in spatial health
			research. Apparent patterns must be tested against proper temporal specifications before
			informing policy.
		</p>
	</section>

	<section id="acknowledgments">
		<h2>Acknowledgments</h2>
		<p>
			We thank the anonymous peer reviewers whose rigorous critique identified the temporal leakage
			issue that fundamentally changed this paper's conclusions. This is how science is supposed to
			work.
		</p>
	</section>

	<section id="data-availability">
		<h2>Data Availability</h2>
		<p>
			All data are from publicly available CDC PLACES releases. Code for data processing, feature
			engineering, model training, and the methodological correction analysis is available at:
			<a href="https://github.com/cschuman/resilience-mapping">github.com/cschuman/resilience-mapping</a>
		</p>
	</section>
</PaperLayout>

<style>
	/* Method comparison boxes */
	.method-comparison {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: var(--space-4);
		margin: var(--space-6) 0;
	}

	.method-box {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-lg);
		padding: var(--space-4);
	}

	.method-box h4 {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		margin-bottom: var(--space-3);
	}

	.method-box ul {
		margin: 0;
		padding-left: var(--space-4);
		font-size: var(--text-sm);
	}

	.method-box li {
		margin-bottom: var(--space-2);
	}

	.method-box--wrong {
		border-color: rgba(209, 104, 71, 0.3);
	}

	.method-box--correct {
		border-color: rgba(78, 167, 117, 0.3);
	}

	.method-problem {
		margin-top: var(--space-3);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		color: var(--color-score-low);
	}

	.method-correct {
		margin-top: var(--space-3);
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		color: var(--color-score-high);
	}

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

	/* Policy comparison */
	.policy-comparison {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: var(--space-4);
		margin: var(--space-6) 0;
	}

	.policy-box {
		background: var(--color-foundation-mid);
		border: 1px solid var(--color-border-subtle);
		border-radius: var(--radius-lg);
		padding: var(--space-4);
	}

	.policy-box h4 {
		font-size: var(--text-sm);
		font-weight: var(--font-weight-semibold);
		margin-bottom: var(--space-3);
	}

	.policy-box ul {
		margin: 0;
		padding-left: var(--space-4);
		font-size: var(--text-sm);
	}

	.policy-box li {
		margin-bottom: var(--space-2);
	}

	.policy-box--highlight {
		background: linear-gradient(135deg, var(--color-foundation-mid), var(--color-accent-primary-glow));
		border-color: var(--color-accent-primary);
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

	code {
		font-family: var(--font-mono);
		font-size: 0.9em;
		background: var(--color-foundation-surface);
		padding: var(--space-1) var(--space-2);
		border-radius: var(--radius-sm);
	}

	a {
		color: var(--color-accent-primary);
		text-decoration: none;
	}

	a:hover {
		text-decoration: underline;
	}

	/* Context sections (Why We're Publishing This, etc.) */
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

	.context-section ul {
		margin-top: var(--space-3);
	}

	.context-section li {
		color: var(--color-text-secondary);
	}
</style>
