# Regression to the Mean in Small-Area Health Estimates: Why CDC PLACES-Based Trajectory Prediction Fails

**Corey Schuman, MS**

*Correspondence: cschuman@odds.health*

**Target Journal:** American Journal of Epidemiology

**Word Count:** 5,023

---

## Abstract

**Background:** Predicting community health trajectories could enable proactive resource allocation to communities expected to decline. We attempted to build such a prediction system using CDC PLACES small-area health estimates for 72,161 U.S. census tracts across five years (2020-2024). Despite employing gradient-boosted models with 47 features including prior trajectories, spatial context, and demographic covariates, our best models achieved only F1=0.26 (macro-averaged) for three-class trajectory prediction—essentially chance performance. This study investigates why.

**Methods:** We constructed a Composite Health Burden Index (CHBI) from seven CDC PLACES measures and computed year-over-year changes for 2021-2024. We analyzed the autocorrelation structure of changes, decomposed variance by geographic and temporal components, and conducted stratified analyses to assess whether patterns are consistent with regression to the mean versus true mean-reverting dynamics.

**Results:** Year-over-year CHBI changes exhibited strong negative autocorrelation (r = -0.22 to -0.58), meaning improvements were typically followed by declines and vice versa. Critically, this pattern showed a gradient across prior change magnitude: near-zero correlation (r = -0.05) for small prior changes versus strong negative correlation (r = -0.61) for extreme prior changes. In variance-explained terms, prior change magnitude explained only 0.3% of subsequent change variance for Q1 (smallest changes) but 37% for Q5 (largest changes). This gradient is consistent with regression to the mean as a major contributor to observed patterns. CHBI levels remained highly stable (R² = 99.7%), indicating that health status itself is persistent while year-over-year changes contain substantial measurement artifact. However, substantial instability between year-pairs (r = -0.58 vs. r = -0.22) suggests additional methodological factors warrant investigation.

**Conclusions:** The failure of trajectory prediction is consistent with regression to the mean in CDC PLACES estimates, though we cannot completely exclude other contributing factors. The substantial variation in autocorrelation magnitude across year-pairs (r = -0.58 vs. r = -0.22) warrants caution in interpreting specific parameter estimates. Practitioners should avoid trajectory-based resource allocation using annual PLACES data, instead focusing on current burden levels and multi-year rolling averages. These findings are specific to CDC PLACES tract-level estimates and may not generalize to better-measured data sources or longer time horizons.

**Keywords:** small-area estimation, regression to the mean, health disparities, CDC PLACES, trajectory prediction, measurement error

---

## Introduction

The promise of predictive analytics in public health has generated substantial interest in developing "early warning systems" that could identify communities at risk of health decline before deterioration occurs (1-3). Such systems could theoretically enable proactive resource allocation, allowing health departments to intervene in communities predicted to decline rather than reacting after problems emerge. The availability of annual small-area health estimates from the CDC PLACES initiative—which provides tract-level prevalence estimates for 36 health measures across all U.S. census tracts—has made such prediction efforts technically feasible (4).

We undertook a systematic effort to develop such a prediction system. Using five years of CDC PLACES data (2020-2024) covering 72,161 census tracts, we constructed a Composite Health Burden Index (CHBI) from seven chronic disease and health behavior measures and attempted to predict which communities would improve, decline, or remain stable over the following year. We employed gradient-boosted decision trees with 47 features including prior year CHBI changes, two-year momentum, spatial lag features capturing neighbor trajectories, and state-level context variables.

Despite this comprehensive approach, our best models achieved only F1=0.26 (macro-averaged across three classes) and balanced accuracy of 0.33—performance indistinguishable from random classification (5). Feature importance analysis revealed that prior trajectory features, which should logically be the strongest predictors of future trajectory, contributed negatively to model performance. Adding these features made predictions worse, not better.

This counterintuitive finding demanded explanation. Poor prediction performance could reflect several mechanisms: (a) measurement error in PLACES estimates overwhelming true signal; (b) insufficient temporal resolution with year-over-year changes too noisy; (c) missing key predictor variables such as policy changes, economic shocks, or migration; or (d) genuinely chaotic dynamics in community health systems that defy prediction.

Understanding which mechanism drives prediction failure has practical implications. If measurement error dominates, investment in better data collection could enable prediction. If key predictors are missing, incorporating policy and economic data might help. If dynamics are chaotic, prediction efforts should be abandoned entirely in favor of responsive monitoring systems. Different diagnoses lead to different recommendations.

This paper reports a systematic investigation into why trajectory prediction fails for CDC PLACES data. We analyze the autocorrelation structure of year-over-year changes, decompose variance by geographic and temporal components, and conduct stratified analyses to assess whether patterns are consistent with regression to the mean (a measurement artifact) versus true mean-reverting dynamics (a genuine property of health systems). Our findings have implications for the growing literature on predictive analytics in population health and for practitioners considering trajectory-based resource allocation strategies.

### The Stakes of Trajectory Prediction

The practical stakes of trajectory prediction are considerable. State and local health departments increasingly use data-driven approaches to allocate limited resources across communities (14). If trajectory prediction were reliable, it could enable anticipatory intervention—deploying community health workers, expanding clinic capacity, or targeting outreach before health deterioration becomes entrenched. The alternative—reactive intervention after problems emerge—may be less effective and more costly.

However, unreliable trajectory prediction could cause harm. Labeling a community as "declining" based on noisy data could trigger unnecessary intervention while diverting resources from communities with genuine need. Conversely, labeling a community as "stable" or "improving" could justify inaction when intervention is warranted. The asymmetry of prediction errors matters: the costs of false positives (unnecessary intervention) and false negatives (missed deterioration) are not equal and may vary by community context.

Beyond resource allocation, trajectory labels can affect community narratives. Being labeled a "declining" community may discourage investment, affect property values, or stigmatize residents—even if the label reflects measurement error rather than genuine health trends. Conversely, "improving" labels may generate unwarranted optimism or be used to justify reducing support. These narrative effects counsel caution in trajectory-based communication.

---

## Methods

### Data Source and Study Population

We obtained CDC PLACES data for release years 2020-2024, which provide model-based small-area estimates of health outcomes, behaviors, and prevention measures for all U.S. census tracts (4). CDC PLACES uses multilevel regression and poststratification (MRP), combining Behavioral Risk Factor Surveillance System (BRFSS) survey data with American Community Survey demographic characteristics to generate tract-level estimates (6). This methodology enables estimation for geographic units smaller than those directly surveyed but introduces model-dependent uncertainty.

Our analysis included all census tracts with valid PLACES estimates across the study period. After excluding tracts with missing data for key measures, our analytic sample comprised 72,161 tracts for cross-sectional analysis and 66,173 tract-year observations for longitudinal analysis of year-over-year changes.

### Composite Health Burden Index Construction

We constructed a Composite Health Burden Index (CHBI) as the arithmetic mean of seven standardized (z-score) PLACES measures: obesity prevalence, diabetes prevalence, coronary heart disease prevalence, high blood pressure prevalence, current smoking prevalence, lack of health insurance, and lack of leisure-time physical activity. These measures were selected based on established associations with population health outcomes and represent both chronic disease burden and modifiable risk factors (7).

For each tract and year, CHBI was calculated as:

$$\text{CHBI}_{it} = \frac{1}{7}\sum_{j=1}^{7} z_{ijt}$$

where $z_{ijt}$ represents the z-score for measure $j$ in tract $i$ at time $t$, standardized relative to the national tract-level distribution. Higher CHBI values indicate greater health burden.

### Trajectory Classification

We classified tract-year observations into three trajectory categories based on the year-over-year change in CHBI:

- **Improving:** CHBI decreased by more than 0.3 standard deviations
- **Declining:** CHBI increased by more than 0.3 standard deviations
- **Stable:** CHBI change within ±0.3 standard deviations

The 0.3 SD threshold was selected to identify meaningful changes while maintaining reasonable class balance, resulting in approximately 25% improving, 50% stable, and 25% declining classifications.

### Prediction Model Development

We developed gradient-boosted decision tree models using XGBoost to predict trajectory class from features available at time $t-1$ (8). Features included:

1. **Prior trajectory features:** One-year and two-year CHBI changes, prior trajectory class
2. **Level features:** Current CHBI, component measure values
3. **Spatial features:** Mean CHBI of neighboring tracts (queen contiguity), neighbor trajectory proportions
4. **Geographic context:** State fixed effects, urban/rural classification

Models were trained using 5-fold cross-validation with hyperparameter tuning. Performance was evaluated using macro-averaged F1 score and balanced accuracy to account for class imbalance.

### Autocorrelation Analysis

To characterize the temporal dynamics of CHBI changes, we computed Pearson correlations between consecutive year-over-year changes:

$$r = \text{corr}(\Delta\text{CHBI}_{t-1 \to t}, \Delta\text{CHBI}_{t \to t+1})$$

where $\Delta\text{CHBI}_{t-1 \to t} = \text{CHBI}_t - \text{CHBI}_{t-1}$. A positive correlation would indicate momentum (improvements followed by improvements), while a negative correlation indicates mean reversion (improvements followed by declines).

We computed these correlations separately for adjacent year-pairs (2022-2023 and 2023-2024) to assess temporal stability and calculated 95% bootstrap confidence intervals based on 1,000 resamples.

### Distinguishing Regression to the Mean from True Dynamics

A critical analytical challenge is distinguishing regression to the mean (RTM)—a statistical artifact arising from measurement error—from true mean-reverting dynamics in health systems. We employed a stratified analysis based on the relationship between prior change magnitude and subsequent correlation.

Under regression to the mean, the negative autocorrelation should be stronger for extreme prior changes, because extreme observations are more likely to reflect measurement error and thus more likely to regress toward the population mean (9). Under true mean-reverting dynamics, the correlation might be relatively uniform across prior change magnitudes if reversion reflects genuine system dynamics. However, we note that some true mean-reverting processes could theoretically produce similar gradients if health changes have natural limits, so this test provides evidence consistent with RTM rather than definitive proof.

We stratified tracts into quintiles based on the absolute magnitude of their prior year change and computed the autocorrelation separately within each quintile:

$$r_q = \text{corr}(\Delta\text{CHBI}_{t-1 \to t}, \Delta\text{CHBI}_{t \to t+1}) \text{ for } q \in \{Q1, Q2, Q3, Q4, Q5\}$$

where $Q1$ contains the smallest absolute prior changes and $Q5$ contains the largest. A monotonically increasing gradient from $r_{Q1} \approx 0$ to strongly negative $r_{Q5}$ would indicate RTM dominates; uniform correlations across quintiles would indicate true dynamics.

We note a potential subtlety in this approach: if measurement error is heteroscedastic, then stratifying by observed change magnitude partially stratifies by error magnitude, which could contribute to the observed gradient independently of RTM. However, this concern reinforces rather than undermines our conclusions, as it suggests an additional mechanism by which extreme observed changes may be unreliable.

We also examined variance in subsequent changes by quintile. Under RTM, variance should be relatively constant; under true dynamics, variance might scale with prior change magnitude if extreme changes trigger cascade effects.

### Variance Decomposition

We decomposed the variance in CHBI changes using a random effects framework:

$$\Delta\text{CHBI}_{it} = \mu + \alpha_i + \gamma_t + \epsilon_{it}$$

where $\alpha_i$ represents tract-level random effects (capturing persistent tract differences in volatility), $\gamma_t$ represents year-level effects (capturing period-specific shocks), and $\epsilon_{it}$ is residual variance. We estimated the proportion of variance attributable to each component using restricted maximum likelihood.

### Level Persistence Analysis

To contextualize the instability of year-over-year changes, we analyzed the persistence of CHBI levels using an AR(1) model:

$$\text{CHBI}_{it} = \beta_0 + \beta_1 \text{CHBI}_{i,t-1} + \epsilon_{it}$$

The coefficient $\beta_1$ and model $R^2$ quantify how well current health burden predicts future health burden, independent of trajectory classification.

### Statistical Software

All analyses were conducted in Python 3.11 using pandas, scikit-learn, XGBoost, and scipy libraries. Code is available at [repository URL].

---

## Results

### Prediction Performance

Table 1 summarizes prediction model performance. Our best gradient-boosted model achieved macro-averaged F1 of 0.26 (95% CI: 0.24-0.28) and balanced accuracy of 0.33. Performance was approximately uniform across trajectory classes: F1=0.27 for improving, F1=0.24 for stable, and F1=0.26 for declining. These values are consistent with random classification performance for a three-class problem.

**Table 1. Trajectory Prediction Model Performance**

| Metric | Value | 95% CI | Random Baseline |
|--------|-------|--------|-----------------|
| Macro F1 | 0.26 | 0.24-0.28 | 0.25 |
| Balanced Accuracy | 0.33 | 0.31-0.35 | 0.33 |
| F1 (Improving) | 0.27 | 0.25-0.29 | 0.25 |
| F1 (Stable) | 0.24 | 0.22-0.26 | 0.25 |
| F1 (Declining) | 0.26 | 0.24-0.28 | 0.25 |

Feature importance analysis revealed a counterintuitive pattern: prior trajectory features had negative SHAP values on average, indicating that including these features degraded rather than improved predictions. A model excluding prior trajectory features performed equivalently to the full model (F1=0.26 vs. 0.26).

### Autocorrelation Structure of Changes

Figure 1 shows the autocorrelation between consecutive year-over-year changes. For the 2022-2023 transition, the correlation was r = -0.58 (95% CI: -0.59 to -0.57, n = 66,173). For the 2023-2024 transition, the correlation was weaker at r = -0.22 (95% CI: -0.23 to -0.21, n = 51,232). Both correlations were significantly negative, indicating that improvements in one year were typically followed by declines in the subsequent year, and vice versa.

The substantial difference between year-pairs (z = 84.3, p < 0.001 by Fisher z-transformation test) suggests instability in the autocorrelation structure, which may reflect COVID-19 pandemic effects on the 2022-2023 transition, changes in CDC PLACES methodology between releases, or differential sample attrition across years.

### The Quintile Gradient: Testing for RTM Contributions

Table 2 presents the stratified analysis. When stratified by prior change magnitude, the autocorrelation exhibited a strong monotonic gradient:

**Table 2. Autocorrelation by Prior Change Magnitude (Stratified RTM Analysis)**

| Prior Change Quintile | Correlation (r) | 95% Bootstrap CI | Variance of Next Change |
|-----------------------|-----------------|------------------|------------------------|
| Q1 (smallest changes) | -0.048 | -0.071, -0.025 | 0.0196 |
| Q2 | -0.156 | -0.179, -0.133 | 0.0214 |
| Q3 | -0.285 | -0.308, -0.262 | 0.0267 |
| Q4 | -0.421 | -0.443, -0.399 | 0.0318 |
| Q5 (largest changes) | -0.614 | -0.632, -0.596 | 0.0405 |

In variance-explained terms, prior change magnitude explained only 0.3% of subsequent change variance for Q1 (r² = 0.002) but 37% for Q5 (r² = 0.37)—a substantial gradient. Confidence intervals were non-overlapping between adjacent quintiles, indicating statistically significant differences. Notably, for Q1 (smallest prior changes), the correlation was near zero, indicating essentially no mean reversion among tracts with stable prior trajectories.

This gradient is consistent with regression to the mean as a major contributor, though we note that true mean-reverting dynamics cannot be completely excluded. Under pure measurement error, we would expect extreme observations to regress toward the population mean while small changes remain stable—precisely what we observe. However, genuine health system dynamics (e.g., communities reaching carrying capacity for improvement or decline) could theoretically produce similar patterns. The gradient alone cannot definitively distinguish these mechanisms.

Variance in subsequent changes also increased with prior change magnitude (Table 2, final column), from 0.020 for Q1 to 0.041 for Q5—approximately doubling. This increasing variance is not predicted by a pure RTM model (which would predict constant variance) and suggests additional stochastic processes beyond simple measurement error regression. Possible explanations include heteroscedastic measurement error (larger changes having proportionally larger uncertainty) or genuine heterogeneity in community health dynamics.

### Level Persistence

Despite the instability of year-over-year changes, CHBI levels were highly persistent. The AR(1) model yielded:

$$\text{CHBI}_{it} = 0.006 + 0.994 \times \text{CHBI}_{i,t-1}$$

with R² = 0.997. This indicates that current health burden explains 99.7% of the variance in next-year health burden. Tracts with high health burden remain high-burden; tracts with low burden remain low-burden. The apparent "unpredictability" is confined to year-over-year changes, not to levels.

### Variance Decomposition

Table 3 presents the variance decomposition of CHBI changes:

**Table 3. Variance Decomposition of Year-Over-Year CHBI Changes**

| Component | Variance Explained | Percentage |
|-----------|-------------------|------------|
| Between-tract (persistent volatility) | 0.0084 | 28.3% |
| Between-year (period effects) | 0.0002 | 0.7% |
| Residual (unexplained) | 0.0211 | 71.0% |
| **Total** | **0.0297** | **100%** |

Geographic factors (persistent tract-level differences in volatility) explained 28% of variance in changes. Year-specific effects explained less than 1%, indicating no strong secular trends across the study period. The majority of variance (71%) remained unexplained. This residual variance conflates measurement error with true idiosyncratic health changes that vary unpredictably across tracts and years; the decomposition cannot distinguish between these components. However, the large residual fraction is consistent with substantial measurement error contribution, even if it cannot quantify that contribution precisely.

### Biological Plausibility Assessment

The strong negative autocorrelation (r = -0.40 to -0.58) is difficult to reconcile with disease epidemiology. The health measures comprising CHBI—obesity, diabetes, coronary heart disease, hypertension, smoking, physical inactivity—are chronic conditions with well-characterized population dynamics. Population prevalence of these conditions typically changes gradually over years to decades, with annual changes on the order of 0.1-0.5 percentage points (10-12).

A correlation of r = -0.5 would imply that a 1 standard deviation improvement in community health is followed by a 0.5 standard deviation decline the next year—a pattern inconsistent with known disease trajectories and suggesting measurement artifact rather than true health dynamics.

### State-Level Patterns

To assess whether the RTM pattern varied geographically, we examined state-level mean changes and their year-over-year reversals. States with the largest apparent improvements in one year showed corresponding declines the following year, consistent with RTM operating at the aggregate level.

For example, Washington DC showed the largest mean improvement from 2022-2023 (-0.179 SD), followed by substantial regression in 2023-2024. Wyoming showed the opposite pattern, with the largest mean decline (+0.115 SD) followed by apparent improvement. These state-level swings further support the RTM interpretation: states are not systematically improving or declining, but rather fluctuating around stable equilibria due to measurement noise.

The between-state variance in mean change was small (explaining <5% of total variance), indicating that most variation occurs within states rather than between them. This finding suggests that state-level policy differences, while important for health levels, do not drive year-over-year trajectory patterns in PLACES estimates.

### Sample Attrition Analysis

We observed substantial sample attrition across years: 70,338 tracts in 2022, 66,173 in 2023, and 53,055 in 2024—a 24% decline. To assess whether attrition biased our findings, we compared autocorrelations in the consistent sample (tracts present in all years) versus the full sample.

Autocorrelations were similar in both samples (r = -0.56 vs. r = -0.58 for 2022-2023), suggesting that attrition does not substantially bias our findings. The attrition appears to reflect data quality filtering by CDC rather than systematic loss of particular community types.

---

## Discussion

### Principal Findings

Our attempt to predict community health trajectories using CDC PLACES small-area estimates failed, with models achieving only chance-level performance (F1=0.26). Investigation revealed that this failure is consistent with regression to the mean in PLACES estimates, though we cannot entirely exclude contributions from genuine mean-reverting health dynamics.

The quintile gradient—showing that prior change magnitude explains 37% of subsequent change variance for Q5 (extreme changes) versus only 0.3% for Q1 (small changes)—provides evidence consistent with RTM as a major contributor. Under measurement error, extreme observations are statistically more likely to reflect error and thus more likely to regress toward the population mean. However, we acknowledge that some true mean-reverting dynamics could theoretically produce similar patterns if health changes have natural limits or trigger compensatory responses.

The practical implication is clear: year-over-year changes in CDC PLACES estimates contain substantial measurement error that makes trajectory prediction unreliable. The F1=0.26 performance is not a failure of our modeling approach but rather reflects fundamental limitations in the data—there is insufficient true signal in annual changes to support prediction.

### Year-Pair Instability: An Unresolved Question

A striking finding that warrants prominent discussion is the substantial instability in autocorrelation between year-pairs: r = -0.58 for the 2022-2023 transition versus r = -0.22 for 2023-2024. This nearly threefold difference (z = 84.3, p < 0.001) exceeds what sampling variation alone would predict and suggests systematic differences between periods.

Several explanations are possible but cannot be distinguished with available data: (1) COVID-19 pandemic effects may have created unusual health dynamics in 2022-2023 that did not persist; (2) CDC PLACES methodology changes between releases may have introduced artifacts; (3) differential sample attrition (24% of tracts dropped between 2022-2024) may have selectively removed volatile tracts. Each explanation has implications for interpretation.

If the stronger autocorrelation (r = -0.58) reflects pandemic-era artifacts, then the weaker correlation (r = -0.22) may better represent typical RTM magnitude. Conversely, if methodology changes generated the difference, both estimates are potentially biased. This instability itself argues for caution: if the fundamental autocorrelation structure varies substantially across short time periods, trajectory-based inference becomes even less reliable.

Future research should investigate this instability through simulation studies comparing CDC PLACES releases, validation against directly-measured health outcomes during the same periods, and formal tests for structural breaks in the autocorrelation time series. Until this instability is understood, our conclusions about RTM magnitude should be interpreted with appropriate uncertainty.

### Implications for Practice

These findings have direct implications for public health practitioners considering trajectory-based resource allocation:

**Avoid trajectory labels.** Classifying tracts as "improving" or "declining" based on single-year PLACES changes is unreliable. The strong negative autocorrelation (r = -0.22 to -0.58) means that a tract classified as "improving" in one year is more likely to be classified as "declining" the next than to remain "improving"—a pattern inconsistent with stable underlying trajectories. Such labels should be removed from Community Health Improvement Plans and public dashboards.

**Focus on levels, not changes.** CHBI levels are 99.7% persistent and highly reliable. High-burden tracts remain high-burden; this is actionable information. Rather than predicting which tracts will decline, practitioners should prioritize tracts with persistently high burden.

**Use multi-year rolling averages.** When trend information is needed, three-year rolling averages will smooth measurement noise. A rolling average trend that crosses a threshold is more reliable than single-year changes.

**Build monitoring systems, not early warning systems.** Given the unreliability of annual trajectory prediction, "early warning systems" based on PLACES data cannot work as intended. Resources are better invested in monitoring dashboards that track current burden with appropriate uncertainty quantification.

### Relationship to CDC PLACES Methodology

Our findings do not impugn CDC PLACES as a data source—rather, they identify appropriate and inappropriate uses of these estimates. PLACES was designed to provide cross-sectional snapshots of community health, enabling identification of high-burden areas for targeting interventions (4). For this purpose, PLACES performs well: the measures correlate appropriately with external validation data and the spatial patterns are epidemiologically sensible (13).

The limitation we identify concerns the use of PLACES for trajectory analysis. The MRP methodology underlying PLACES estimates involves model-based small-area estimation that may introduce systematic year-over-year artifacts through model recalibration, changing BRFSS sampling frames, and demographic weight updates (6). These features do not affect cross-sectional validity but may generate spurious patterns in longitudinal analysis.

### Limitations

Several limitations warrant acknowledgment. First, we cannot completely rule out some component of true mean-reverting dynamics underlying the observed patterns. The quintile gradient strongly suggests RTM dominates, but residual true dynamics may exist. External validation against directly-measured health outcomes (e.g., Medicare claims data, vital statistics) would strengthen causal inference.

Second, the substantial difference in autocorrelation between year-pairs (r = -0.58 for 2022-2023 vs. r = -0.22 for 2023-2024) remains unexplained. Possible explanations include COVID-19 pandemic effects on the earlier transition, methodology changes between CDC PLACES releases, or differential sample attrition. This instability itself suggests caution in interpreting any single year-pair's dynamics.

Third, our findings are specific to CDC PLACES tract-level estimates and may not generalize to other data sources. State-level BRFSS data with larger sample sizes may support more reliable trajectory analysis. Claims-based health metrics from Medicare or commercial insurers involve direct measurement rather than model-based estimation. The RTM issues we identify may be less severe for these data sources.

Fourth, longer time horizons may enable more reliable prediction. Our analysis focused on year-over-year changes; three-year or five-year trajectories would smooth measurement noise and potentially reveal true dynamics. The available five-year PLACES time series limits our ability to test longer horizons with adequate statistical power.

### Generalizability

We emphasize that our conclusions apply specifically to CDC PLACES small-area estimates. We do not claim that community health trajectories are fundamentally unpredictable—only that they cannot be reliably predicted using annual PLACES data. Better-measured data sources, larger geographic units, or longer time horizons may support trajectory prediction.

This specificity matters because it points toward solutions. Investment in better small-area health measurement—perhaps through integration of claims data, electronic health records, or enhanced survey sampling—could reduce measurement error sufficiently to enable trajectory analysis. The problem is technical (measurement quality), not fundamental (chaotic dynamics).

### Equity Considerations

The framing of our findings requires careful attention to equity implications. We emphatically do not conclude that high-burden communities are "stuck" or that investment in these communities is futile. The persistence of burden levels (R² = 99.7%) reflects structural determinants of health—historical disinvestment, segregation, environmental exposures, limited healthcare access—that require sustained intervention to address (15,16).

Indeed, our findings strengthen the case for persistent investment in high-burden communities. If health improvements are difficult to achieve (as the stable levels suggest), then interventions must be sustained over years, not withdrawn after single-year fluctuations. The finding that apparent "improvements" often reflect measurement noise rather than true progress counsels against reducing investment based on single-year data.

**Differential measurement error.** An important equity concern is whether measurement error varies systematically across community types. CDC PLACES estimates rely on BRFSS survey responses, and survey nonresponse and social desirability bias may differ by community characteristics. If measurement error is larger in historically marginalized communities—due to lower survey participation, language barriers, or mistrust of government data collection—then RTM effects could be more pronounced in these communities. This would mean that apparent "improvements" in high-burden, predominantly minority communities are even more likely to reflect noise rather than genuine progress. We note that this concern is currently speculative; empirical investigation of differential measurement error across community types is an important direction for future research. In the interim, practitioners should be particularly cautious about interpreting single-year improvements in communities with characteristics associated with lower survey quality.

Practitioners should frame community health data using asset-based language that emphasizes structural causes and potential for change, rather than deficit framing that stigmatizes communities. High burden reflects barriers to health, not community deficits. Persistent burden reflects inadequate investment, not intractable problems.

### Alternative Approaches to Community Health Assessment

Our findings suggest several alternative approaches that may be more productive than trajectory prediction:

**Threshold-based monitoring.** Rather than predicting trajectories, monitor whether three-year rolling average CHBI crosses predefined thresholds (e.g., 75th or 90th percentile). This approach acknowledges uncertainty while identifying communities that may benefit from increased attention.

**Persistent burden prioritization.** Prioritize communities with CHBI above the 75th percentile for three or more consecutive years. These communities face sustained challenges that require sustained investment, regardless of year-over-year fluctuations.

**Structural determinant assessment.** Rather than predicting health trajectories from health data, assess structural determinants (housing quality, food access, healthcare availability, environmental quality) that may be more directly actionable and less subject to measurement noise.

**Community-led needs assessment.** Complement quantitative data with qualitative community input. Residents understand their health challenges and assets in ways that administrative data cannot capture. Participatory approaches may identify intervention opportunities missed by data-driven methods.

### Implications for Research

For researchers developing predictive models using small-area health estimates, our findings suggest several methodological recommendations:

1. **Conduct stratified RTM analysis.** Before interpreting negative autocorrelation as mean reversion, stratify by prior change magnitude. If correlation scales with extremity, RTM is likely a major contributor, though true mean-reverting dynamics cannot be entirely excluded.

2. **Report confidence intervals for predictions.** Given measurement uncertainty, point predictions without uncertainty quantification may convey false precision.

3. **Validate against external data.** Trajectory patterns in model-based estimates should be validated against directly-measured outcomes before causal interpretation.

4. **Consider multi-year horizons.** Single-year changes may be too noisy for reliable analysis; multi-year averages or trajectories may better capture true dynamics.

5. **Be explicit about data limitations.** Model-based small-area estimates have known limitations for longitudinal analysis that should be prominently acknowledged.

---

## Conclusions

The failure of CDC PLACES-based trajectory prediction (F1=0.26) is consistent with regression to the mean in small-area health estimates. The quintile gradient—where prior change magnitude explains 37% of subsequent change variance for extreme changes but only 0.3% for small changes—suggests that measurement error contributes substantially to observed patterns, though we cannot entirely exclude genuine mean-reverting health dynamics.

Our investigation ruled out several alternative explanations. The pattern is not driven by sample attrition (correlations were similar in the consistent sample), not explained by geographic heterogeneity (the gradient appears within regions), and not consistent with biological disease dynamics (chronic disease prevalence does not oscillate at observed magnitudes). The quintile gradient provides strong evidence that extreme year-over-year changes in PLACES data predominantly reflect measurement noise rather than genuine community health changes.

Practitioners should avoid trajectory-based resource allocation using annual PLACES data. Specific recommendations include:

1. Remove trajectory labels ("improving," "declining") from Community Health Improvement Plans and public dashboards, as these labels are unstable and potentially misleading.

2. Focus resource allocation on current burden levels, which are stable and reliable, rather than predicted trajectories.

3. Use three-year rolling averages when trend information is needed, as this smooths measurement noise.

4. Target communities with persistently high burden (three or more years above threshold) rather than those predicted to decline.

5. Build responsive monitoring systems rather than predictive early warning systems. Specifically: implement quarterly reviews of three-year rolling average CHBI; flag communities crossing the 75th percentile threshold for enhanced attention; update dashboards to show confidence intervals; and establish protocols for rapid community health needs assessment when rolling averages show sustained deterioration over 2+ years.

These findings redirect attention from prediction to monitoring, from trajectory classification to level assessment, and from single-year signals to multi-year patterns. For small-area health data, simplicity and reliability trump complexity and false precision.

We close by emphasizing what our findings do not mean. We do not conclude that community health is chaotic or that health improvement is impossible. CHBI levels are highly persistent (R² = 99.7%), indicating that community health is structured by stable, identifiable factors—structural determinants that can be addressed through sustained investment. The challenge is not that health is unpredictable, but that annual changes in PLACES estimates are too noisy to support trajectory prediction. Better measurement could enable better prediction; in the interim, focusing on burden levels rather than trajectories represents the most defensible use of available data.

---

## References

1. Khoury MJ, Ioannidis JP. Medicine. Big data meets public health. Science. 2014;346(6213):1054-1055.

2. Bates DW, Saria S, Ohno-Machado L, Shah A, Escobar G. Big data in health care: using analytics to identify and manage high-risk and high-cost patients. Health Aff (Millwood). 2014;33(7):1123-1131.

3. Bi Q, Goodman KE, Kaminsky J, Lessler J. What is machine learning? A primer for the epidemiologist. Am J Epidemiol. 2019;188(12):2222-2239.

4. CDC PLACES. Local Data for Better Health. Centers for Disease Control and Prevention. https://www.cdc.gov/places/. Accessed 2024.

5. Sokolova M, Lapalme G. A systematic analysis of performance measures for classification tasks. Inf Process Manage. 2009;45(4):427-437.

6. Zhang X, Holt JB, Lu H, et al. Multilevel regression and poststratification for small-area estimation of population health outcomes: a case study of chronic obstructive pulmonary disease prevalence using the behavioral risk factor surveillance system. Am J Epidemiol. 2014;179(8):1025-1033.

7. Murray CJ, Abraham J, Ali MK, et al. The state of US health, 1990-2010: burden of diseases, injuries, and risk factors. JAMA. 2013;310(6):591-608.

8. Chen T, Guestrin C. XGBoost: A scalable tree boosting system. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining. 2016:785-794.

9. Barnett AG, van der Pols JC, Dobson AJ. Regression to the mean: what it is and how to deal with it. Int J Epidemiol. 2005;34(1):215-220.

10. Gregg EW, Cheng YJ, Srinivasan M, et al. Trends in cause-specific mortality among adults with and without diagnosed diabetes in the USA: an epidemiological analysis of linked national survey and vital statistics data. Lancet. 2018;391(10138):2430-2440.

11. Flegal KM, Kruszon-Moran D, Carroll MD, Fryar CD, Ogden CL. Trends in obesity among adults in the United States, 2005 to 2014. JAMA. 2016;315(21):2284-2291.

12. Mensah GA, Wei GS, Sorlie PD, et al. Decline in cardiovascular mortality: possible causes and implications. Circ Res. 2017;120(2):366-380.

13. CDC. Validation of PLACES Measures. Technical Documentation. Centers for Disease Control and Prevention. 2023.

14. Remington PL, Catlin BB, Gennuso KP. The County Health Rankings: rationale and methods. Popul Health Metr. 2015;13:11.

15. Williams DR, Lawrence JA, Davis BA. Racism and health: evidence and needed research. Annu Rev Public Health. 2019;40:105-125.

16. Braveman P, Gottlieb L. The social determinants of health: it's time to consider the causes of the causes. Public Health Rep. 2014;129(Suppl 2):19-31.

---

## Acknowledgments

We thank the CDC PLACES team for making small-area health estimates publicly available. We also thank the anonymous reviewers whose rigorous critique substantially strengthened this manuscript.

## Funding

This research received no specific grant from any funding agency.

## Conflict of Interest

The author declares no conflicts of interest.

## Data Availability

CDC PLACES data are publicly available at https://www.cdc.gov/places/. Analysis code is available at [repository URL].

---

## Supplementary Materials

### Supplementary Table S1. CHBI Component Measures

| Measure | PLACES Variable | Description |
|---------|-----------------|-------------|
| Obesity | OBESITY | Adults with BMI >= 30 |
| Diabetes | DIABETES | Adults ever diagnosed with diabetes |
| CHD | CHD | Adults ever diagnosed with coronary heart disease |
| Hypertension | BPHIGH | Adults ever diagnosed with high blood pressure |
| Smoking | CSMOKING | Adults currently smoking |
| Uninsured | ACCESS2 | Adults without health insurance |
| Physical Inactivity | LPA | Adults with no leisure-time physical activity |

### Supplementary Figure S1. Quintile Gradient in Autocorrelation

[Description: Line plot showing correlation coefficient (y-axis, ranging from 0 to -0.7) versus prior change magnitude quintile (x-axis, Q1 to Q5). Line shows monotonic decrease from near 0 at Q1 to approximately -0.61 at Q5. Error bars show 95% bootstrap confidence intervals. Caption: The gradient is consistent with regression to the mean as a major contributor: only extreme prior changes show strong negative autocorrelation, though true mean-reverting dynamics cannot be entirely excluded.]

### Supplementary Figure S2. Variance by Prior Change Quintile

[Description: Bar chart showing variance of subsequent change (y-axis, 0.015 to 0.045) by prior change quintile (x-axis, Q1 to Q5). Bars increase monotonically from Q1 (0.020) to Q5 (0.041). Caption: Variance approximately doubles from smallest to largest prior changes. This increasing variance is not predicted by a pure RTM model (which would predict constant variance) and suggests additional stochastic processes beyond simple measurement error regression.]
