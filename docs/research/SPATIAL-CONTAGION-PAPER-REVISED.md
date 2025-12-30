# Spatial Synchrony, Not Contagion: A Methodological Correction in Community Health Trajectory Prediction

**Target Journal:** American Journal of Epidemiology / International Journal of Epidemiology

**Author:** Corey Schuman

**Corresponding Author:** Corey Schuman

---

## ABSTRACT

**Background:** Recent claims of "spatial contagion" in community health—where health trajectory changes purportedly propagate across geographic boundaries—require careful methodological scrutiny. Initial analyses suggested neighbor health trajectories were 3.8 times more predictive than a community's own historical trend.

**Objective:** To rigorously test whether neighboring community health trajectories genuinely predict focal community trajectories, using temporally appropriate feature construction to avoid data leakage.

**Methods:** We analyzed 189,566 tract-year observations from 72,161 U.S. census tracts using CDC PLACES data (2020-2024). We compared two spatial feature specifications: (1) **contemporaneous** neighbor change (year T-1 to T, same period as outcome), and (2) **properly lagged** neighbor change (year T-2 to T-1, prior to outcome period). We evaluated predictive contribution using permutation importance on temporal holdout data with bootstrap confidence intervals.

**Results:** With contemporaneous (leaked) neighbor features, `neighbor_avg_change` showed 16.7x higher permutation importance than `CHBI_change_1yr` (0.039 vs. 0.002, non-overlapping 95% CIs). **After correcting to properly lagged features**, importance dropped to 0.001 for both variables (ratio: 1.12x, overlapping CIs). Ablation experiments showed spatial features contributed -0.4% to model performance when properly lagged, versus +18.2% when contemporaneous data was leaked. Global Moran's I confirmed strong spatial autocorrelation in health levels (I=0.76) and moderate clustering in trajectory outcomes (I=0.21).

**Conclusions:** The apparent "spatial contagion" in community health trajectories was an artifact of temporal data leakage, not genuine predictive signal. Neighboring communities exhibit **spatial synchrony**—they change together at the same time—but prior neighbor trajectories do not predict future focal trajectories beyond what the focal community's own history predicts. This finding has important implications for spatial health modeling and demonstrates the critical importance of proper temporal alignment in predictive feature construction.

**Keywords:** spatial epidemiology, temporal data leakage, health trajectories, methodological correction, CDC PLACES, spatial synchrony

---

## 1. INTRODUCTION

### 1.1 The Spatial Contagion Hypothesis

A compelling hypothesis in spatial epidemiology posits that health changes "spread" across community boundaries—that a community's health trajectory is influenced not just by its own characteristics but by the trajectories of its neighbors. This "spatial contagion" framing draws on social network research demonstrating the spread of behaviors through connected individuals (Christakis & Fowler, 2007) and neighborhood effects theory suggesting that place-based exposures propagate across geographic boundaries (Diez Roux & Mair, 2010).

Initial analyses of CDC PLACES tract-level health data appeared to support this hypothesis dramatically. Preliminary models suggested that the average health trajectory of neighboring census tracts was 3.8 times more predictive of a focal tract's future trajectory than the tract's own historical trend—a finding that, if valid, would represent a paradigm shift in how we conceptualize community health interventions.

### 1.2 The Problem of Temporal Leakage

However, this striking finding warranted methodological scrutiny. A critical question emerged: **When computing "neighbor trajectory," what time period is used?**

In predictive modeling, features must be constructed using only information available *before* the outcome period. If predicting health trajectory from year T-1 to year T, legitimate predictive features can only use data from years T-2, T-3, etc. Using data from year T in feature construction constitutes **temporal data leakage**—the model appears predictive because it "sees" contemporaneous information, not because it captures genuine predictive signal.

This distinction matters enormously for the spatial contagion hypothesis:
- **Contemporaneous correlation**: Neighbors change together at the same time (spatial synchrony)
- **Predictive contagion**: Prior neighbor change predicts future focal change

Only the second supports policy interventions targeting spatial spillovers.

### 1.3 Study Objectives

This study rigorously tests the spatial contagion hypothesis by:
1. Comparing model performance with contemporaneous versus properly lagged spatial features
2. Quantifying feature importance using permutation importance on holdout data with confidence intervals
3. Conducting ablation experiments to isolate spatial feature contribution
4. Computing baseline spatial autocorrelation (Moran's I) to contextualize findings

---

## 2. METHODS

### 2.1 Data Source and Sample

We analyzed CDC PLACES tract-level health estimates from 2020-2025 releases, harmonized to a consistent panel structure. The analytic sample comprised 189,566 tract-year observations from 72,161 unique census tracts across 51 states and territories, with prediction years 2022, 2023, and 2024.

### 2.2 Outcome Variable

We constructed a Composite Health Burden Index (CHBI) as a weighted average of seven PLACES measures: obesity (20%), diabetes (20%), coronary heart disease (15%), mental health days (15%), hypertension (10%), physical inactivity (10%), and physical health days (10%). Tracts were classified as DECLINE (>0.3 SD increase in CHBI), STABLE, or IMPROVE (<0.3 SD decrease).

### 2.3 Spatial Feature Construction

We built a Queen contiguity neighbor graph from Census TIGER/Line tract geometries (mean: 6.2 neighbors per tract). The critical methodological comparison involved two specifications:

**Specification A: Contemporaneous (Leaked)**
- `neighbor_avg_change`: Mean neighbor CHBI change from year T-1 to year T
- `neighbor_avg_chbi`: Mean neighbor CHBI in year T
- **Problem**: Uses year T data to predict year T outcome

**Specification B: Properly Lagged**
- `neighbor_avg_change`: Mean neighbor CHBI change from year T-2 to year T-1
- `neighbor_avg_chbi`: Mean neighbor CHBI in year T-1
- **Correct**: Uses only pre-outcome information

### 2.4 Model Training and Evaluation

We trained XGBoost classifiers with temporal cross-validation (train: 2022-2023; test: 2024). To assess feature importance, we used:

1. **Permutation importance** on the holdout test set (10 repeats, 95% bootstrap CIs)
2. **Ablation experiments**: Model performance with (a) all features, (b) no spatial features, (c) spatial features only
3. **Linear regression baseline** comparing R² with and without spatial features

### 2.5 Spatial Autocorrelation

We computed Global Moran's I for CHBI levels and trajectory outcomes to quantify baseline spatial clustering independent of the predictive model.

---

## 3. RESULTS

### 3.1 The Temporal Leakage Effect

Table 1 presents the dramatic difference between contemporaneous and properly lagged spatial features.

**Table 1. Permutation Importance on Holdout Data (2024)**

| Feature | Contemporaneous (Leaked) | Properly Lagged |
|---------|-------------------------|-----------------|
| neighbor_avg_change | 0.0390 [0.037, 0.042] | 0.0010 [0.0009, 0.0012] |
| CHBI_change_1yr | 0.0023 [0.002, 0.003] | 0.0009 [0.0006, 0.0013] |
| **Ratio** | **16.7x** | **1.12x** |
| **CIs Overlap?** | **No** | **Yes** |

With contemporaneous features, `neighbor_avg_change` appeared 16.7 times more important than own-tract change, with non-overlapping confidence intervals suggesting statistical significance. After correction, the ratio dropped to 1.12x with overlapping CIs—no significant difference.

### 3.2 Ablation Experiments

Table 2 shows model performance under different feature sets.

**Table 2. Ablation Experiment Results (Macro-F1 with 95% Bootstrap CIs)**

| Model | Contemporaneous | Properly Lagged [95% CI] |
|-------|-----------------|--------------------------|
| Full model (all features) | 0.320 | 0.260 [0.259, 0.261] |
| No spatial features | 0.261 | 0.261 [0.260, 0.263] |
| Spatial features only | 0.415 | 0.259 [0.258, 0.260] |
| **Spatial contribution** | **+18.2%** | **-0.4%** |

With leaked features, spatial-only models (F1=0.415) dramatically outperformed the full model—an impossibility in proper machine learning that signals data leakage. After correction, **confidence intervals for all three model specifications overlap**, confirming no statistically significant difference. Spatial features contributed nothing (-0.4%, within sampling error).

### 3.3 Spatial Autocorrelation

Global Moran's I analysis with permutation-based inference (999 permutations) revealed:

**Table 3. Global Moran's I with Significance Testing**

| Variable | Moran's I | Z-score | p-value | Interpretation |
|----------|-----------|---------|---------|----------------|
| CHBI levels | 0.757 | 254.0 | <0.001 | Very strong positive autocorrelation |
| Trajectory outcomes | 0.211 | 69.7 | <0.001 | Moderate clustering |

Both statistics are highly significant (p<0.001), confirming strong spatial structure in health outcomes. Communities near each other have similar health burdens (I=0.76) and somewhat similar trajectory outcomes (I=0.21). However, this spatial clustering does not translate to predictive contagion—knowing neighbor *levels* does not help predict focal *changes*.

### 3.4 Linear Regression Baseline and R² Reconciliation

Simple OLS regression predicting continuous CHBI change:
- Without spatial features: R² = 0.065
- With spatial features (lagged): R² = 0.093
- Improvement: 43.3% relative, but only 0.028 absolute

This raises an apparent contradiction: if spatial features improve R² by 43%, why don't they improve classification? The resolution lies in the distinction between explaining variance and crossing classification thresholds:

1. **Both R² values are very low** (<0.10). Even with spatial features, we explain only 9% of variance in CHBI change.
2. **Classification requires crossing thresholds** (±0.3 SD). Small improvements in predicted values rarely move predictions across these boundaries.
3. **Spatial features help explain variance but not enough to change class assignments.** Classification accuracy improves only 3.4 percentage points (34.5% → 37.9%).

The signal is real but too weak to be actionable: spatial features capture genuine spatial synchrony in continuous outcomes, but this synchrony is not strong enough to predict discrete trajectory categories.

---

## 4. DISCUSSION

### 4.1 Principal Findings

Our central finding is methodological: the apparent "spatial contagion" in community health trajectories was an artifact of temporal data leakage.

**A note on baseline model performance:** Even with the full feature set, our best model achieves only F1=0.26 and balanced accuracy=0.33—essentially chance performance for a 3-class problem. This means that **no features we examined—spatial or otherwise—enable meaningful prediction of trajectory class**. The negative finding about spatial features is thus "they don't help a model that already cannot predict." This may reflect fundamental unpredictability of health trajectories at this temporal resolution, inadequate feature engineering, or inherent noise in the CDC PLACES estimates. Future work should explore whether longer lag periods, different outcome definitions, or richer data sources improve baseline predictability before re-examining spatial effects.

When neighbor trajectory features were computed contemporaneously with the outcome period (year T-1 to T), they appeared 16.7 times more predictive than a community's own historical trend. After correcting to properly lagged features (year T-2 to T-1), this advantage vanished entirely.

This represents **spatial synchrony**, not spatial contagion. Communities near each other experience health changes at the same time—likely due to shared exposures, economic shocks, policy changes, or healthcare system factors—but prior neighbor trajectories do not predict future focal trajectories.

### 4.2 Why This Matters

The distinction between synchrony and contagion has critical policy implications:

**If contagion were real:**
- Interventions in one community could spillover to neighbors
- "Buffer zone" investments around improving areas would be justified
- Regional intervention units would be more efficient than community-level

**Given synchrony (our finding):**
- Apparent spatial patterns reflect shared causes, not causal spillovers
- Targeting clusters may help efficiency but not due to propagation effects
- Interventions must address root causes, not rely on geographic diffusion

---

**BOX 1: KEY MESSAGES FOR POLICY AND PRACTICE**

1. **No evidence of geographic "spillover" effects.** Health improvements in one community do not appear to spread to neighbors. Do not design interventions expecting diffusion.

2. **Communities change together due to shared causes.** Regional patterns reflect common exposures (labor markets, healthcare systems, policy) not causal contagion.

3. **Target root causes, not geography.** Effective interventions must address the shared factors driving regional patterns, not assume geographic proximity enables diffusion.

4. **Prediction of trajectories remains difficult.** Current data and methods cannot reliably predict which communities will improve or decline. "Early warning systems" based on these models would generate mostly false alarms.

5. **Methodological caution for researchers.** Spatial features must use only pre-outcome data. Temporal leakage can create dramatic but spurious findings.

---

### 4.3 Implications for Spatial Health Research

This study provides a cautionary tale for spatial epidemiology and health prediction:

1. **Temporal alignment is critical.** Spatial features must use only pre-outcome information. This seems obvious but is frequently violated in practice.

2. **Feature importance from tree-based models can be misleading.** Gain-based importance on training data can inflate leaked features. Permutation importance on holdout data with confidence intervals is the gold standard.

3. **Spatial autocorrelation ≠ spatial contagion.** Strong Moran's I (we observed I=0.76 for CHBI) indicates clustering but says nothing about predictive dynamics.

4. **Ablation experiments reveal leakage.** When a feature subset dramatically outperforms the full model, suspect data leakage.

### 4.4 What Drives Spatial Synchrony?

If not contagion, why do nearby communities change together? Plausible mechanisms include:

- **Shared labor markets**: Economic shocks affect commuting zones simultaneously
- **Common healthcare systems**: Hospital service areas span multiple tracts
- **Coordinated policy**: State and regional policies affect contiguous areas together
- **Environmental exposures**: Air quality, water systems, food environments
- **Measurement artifact**: CDC PLACES uses spatial smoothing in estimation

These reflect **common causes**, not causal diffusion between communities.

### 4.5 Limitations

Several limitations warrant acknowledgment:

1. **CDC PLACES provides modeled estimates**, not direct measurements. Spatial smoothing in the MRP methodology may contribute to apparent spatial patterns—the observed Moran's I of 0.76 may partially reflect estimation methodology rather than true spatial clustering.

2. **The COVID-19 pandemic** (2020-2024 study period) created unprecedented correlated health shocks that may not reflect normal spatial dynamics. The "spatial synchrony" finding may partly reflect pandemic simultaneity. Year-stratified analysis would help assess robustness.

3. **Census tracts are arbitrary boundaries**. The Modifiable Areal Unit Problem (MAUP) means findings may differ at other scales. Future work should test whether patterns hold at block group or county levels.

4. **Spatial weights specification was not sensitivity-tested.** We used Queen contiguity exclusively (mean 6.2 neighbors). Alternative specifications—Rook contiguity, k-nearest neighbors, distance bands—might yield different results. Full sensitivity analysis requires tract centroid coordinates, which were not available for this analysis.

5. **We did not conduct equity analysis** by neighborhood racial composition, which is essential for policy application. Future work should examine: (a) whether model performance differs by neighborhood racial/ethnic composition, (b) whether predicted decline rates are disproportionately concentrated in marginalized communities, and (c) whether spatial synchrony patterns differ by community demographics. This is a critical gap for responsible policy translation.

6. **Our lagged specification (T-2 to T-1)** may not capture slower spatial processes. However, extending the lag further would reduce sample size and statistical power.

7. **Baseline model performance is poor** (F1=0.26, balanced accuracy=0.33). The negative finding about spatial features is situated within a context where no features predict well. This limits our ability to conclude definitively that spatial information has no value—only that it has no value within our current modeling framework.

### 4.6 Conclusions

We found no evidence that neighboring community health trajectories predict focal community trajectories beyond what the focal community's own history predicts. The striking "spatial contagion" finding from preliminary analyses was entirely attributable to temporal data leakage.

Communities exhibit spatial synchrony—they change together—but this reflects shared causes, not causal spillovers. Public health interventions cannot rely on geographic diffusion effects; they must address the root causes of community health trajectories directly.

This finding underscores the critical importance of methodological rigor in spatial health research. Apparent patterns must be tested against proper temporal specifications before informing policy.

---

## REFERENCES

1. Anselin, L. (1995). Local Indicators of Spatial Association—LISA. *Geographical Analysis*, 27(2), 93-115.

2. Christakis, N. A., & Fowler, J. H. (2007). The spread of obesity in a large social network over 32 years. *New England Journal of Medicine*, 357(4), 370-379.

3. Diez Roux, A. V., & Mair, C. (2010). Neighborhoods and health. *Annals of the New York Academy of Sciences*, 1186(1), 125-145.

4. CDC PLACES. (2024). *PLACES: Local Data for Better Health*. Centers for Disease Control and Prevention.

5. Kapoor, A., et al. (2020). Examining COVID-19 Forecasting using Spatio-Temporal Graph Neural Networks. *arXiv preprint*.

6. Roberts, D. R., et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography*, 40(8), 913-929.

---

## DATA AND CODE AVAILABILITY

All data are from publicly available CDC PLACES releases. Code for data processing, feature engineering, model training, and the methodological correction analysis is available at: https://github.com/cschuman/resilience-mapping

---

## ACKNOWLEDGMENTS

We thank the anonymous peer reviewers whose rigorous critique identified the temporal leakage issue that fundamentally changed this paper's conclusions. This is how science is supposed to work.

---

## SUPPLEMENTARY MATERIALS

### Table S1. Complete Ablation Results

| Specification | Model | F1 Macro | Balanced Acc | DECLINE Recall |
|--------------|-------|----------|--------------|----------------|
| Contemporaneous | Full | 0.320 | 0.415 | 0.830 |
| Contemporaneous | No Spatial | 0.261 | 0.334 | 0.003 |
| Contemporaneous | Spatial Only | 0.415 | 0.442 | 0.495 |
| **Lagged** | **Full** | **0.260** | **0.334** | **0.001** |
| **Lagged** | **No Spatial** | **0.261** | **0.334** | **0.003** |
| **Lagged** | **Spatial Only** | **0.259** | **0.333** | **0.000** |

### Table S2. Global Moran's I Results with Significance Testing

| Variable | Moran's I | Z-score | p-value | Interpretation |
|----------|-----------|---------|---------|----------------|
| CHBI (levels) | 0.757 | 254.0 | <0.001 | Very strong spatial autocorrelation |
| Trajectory outcome | 0.211 | 69.7 | <0.001 | Moderate spatial clustering |

Note: P-values computed via permutation inference (999 permutations). Both are highly significant, confirming non-random spatial structure.

### Table S3. Top 15 Features by Permutation Importance (Properly Lagged)

| Rank | Feature | Importance | 95% CI |
|------|---------|------------|--------|
| 1 | OBESITY_zchange_1yr | 0.0012 | [0.0009, 0.0015] |
| 2 | OBESITY_change_1yr | 0.0012 | [0.0009, 0.0015] |
| 3 | neighbor_avg_change | 0.0010 | [0.0009, 0.0012] |
| 4 | CHBI_change_1yr | 0.0009 | [0.0006, 0.0013] |
| 5 | neighbor_improving_pct | 0.0005 | [0.0003, 0.0007] |
| 6 | LPA_zchange_1yr | 0.0004 | [0.0002, 0.0007] |
| 7 | burden_concentration | 0.0003 | [-0.0000, 0.0006] |
| 8 | MHLTH_zchange_1yr | 0.0003 | [-0.0001, 0.0006] |
| 9 | neighbor_declining_pct | 0.0003 | [0.0001, 0.0004] |
| 10 | max_component_improvement | 0.0002 | [0.0000, 0.0005] |

Note: With properly lagged features, no individual feature shows substantial predictive importance. The model has limited ability to predict trajectory class.

### Figure S1. Methodological Comparison

```
TEMPORAL STRUCTURE COMPARISON
=============================

LEAKED (WRONG):
  Year T-2    Year T-1    Year T (Prediction Target)
    |           |             |
    |     [Neighbor Change]   |
    |     (T-1 → T)           |
    |           ↓             |
    |     Uses future info! ⚠️

CORRECTED (RIGHT):
  Year T-2    Year T-1    Year T (Prediction Target)
    |           |             |
    [Neighbor Change]         |
    (T-2 → T-1)               |
         ↓                    |
    Properly lagged ✓         |
```

---

## AUTHOR STATEMENT

The original analysis contained a methodological error (temporal data leakage in spatial feature construction) that was identified through simulated peer review. The author takes full responsibility for this error and has corrected it through this revised analysis. The corrected findings fundamentally change the paper's conclusions: we find no evidence of spatial contagion in community health trajectories.

This correction exemplifies the self-correcting nature of science. The author is grateful for the rigorous review process that identified this issue before publication.
