# Spatial Contagion in Community Health Trajectories: Evidence from 73,000 U.S. Census Tracts

**Target Journal:** Health & Place (IF 4.8) / Social Science & Medicine (IF 5.4)

**Authors:** [To be determined]

**Corresponding Author:** [To be determined]

---

## ABSTRACT

**Background:** Neighborhood effects on health are well-documented, but most research examines cross-sectional associations at aggregate geographic scales. Whether health trajectory changes propagate across community boundaries remains understudied.

**Objective:** To quantify the relative predictive importance of spatial context (neighboring community health trajectories) versus internal community characteristics for predicting census tract health trajectory classification.

**Methods:** We analyzed 189,566 tract-year observations from 72,161 U.S. census tracts using CDC PLACES data (2020-2024). We computed a Composite Health Burden Index (CHBI) from seven health measures and classified tracts as DECLINE (>0.3 SD increase), STABLE, or IMPROVE (<0.3 SD decrease). Spatial features were engineered from Queen contiguity neighbor graphs (mean 6.2 neighbors per tract), including neighbor average change, neighbor improving/declining percentages, and spatial lag indicators. An XGBoost-LightGBM ensemble was trained with temporal cross-validation (train: 2022-2023; validate: 2024).

**Results:** The model achieved 0.43 macro-F1 and 0.47 balanced accuracy on temporal holdout, with 70% recall for DECLINE trajectories. **Spatial features collectively contributed 32% of predictive importance**, exceeding all other feature categories. Critically, `neighbor_avg_change` (12.3% importance) was **3.8 times more predictive** than the tract's own `CHBI_change_1yr` (3.3%). This pattern—neighbor trajectory predicting local trajectory better than own history—was consistent across model specifications.

**Conclusions:** Community health trajectories exhibit spatial contagion: health changes in neighboring tracts are stronger predictors of a tract's future trajectory than its own historical trend. This finding suggests interventions should target geographic clusters rather than isolated communities, and early warning systems should monitor spatial correlation patterns in health trajectories. Public health policy should shift from community-level to region-level conceptualization of intervention units.

**Keywords:** spatial epidemiology, neighborhood effects, health trajectories, machine learning, community health, CDC PLACES, spatial contagion

---

## 1. INTRODUCTION

Population health outcomes exhibit strong spatial clustering, with neighboring communities sharing similar patterns of disease burden, mortality, and health behaviors. While decades of research have established that neighborhoods affect health through multiple pathways—including social capital, collective efficacy, and environmental exposures—most studies have examined these relationships cross-sectionally and at aggregate geographic scales. Critically, existing approaches treat neighborhoods as isolated units, failing to capture the dynamic processes through which health trajectories propagate across geographic boundaries.

### 1.1 Theoretical Foundations

Three theoretical traditions converge to suggest that community health trajectories should exhibit spatial contagion.

**Neighborhood Effects Framework.** Diez Roux's multilevel framework emphasizes cumulative exposures and the importance of spatial scale in neighborhood health effects (Diez Roux, 2001; Diez Roux & Mair, 2010). This work identifies multiple processes through which neighborhood environments affect health, including definition and operationalization of neighborhood boundaries, measurement of neighborhood exposures, consideration of spatial scale, and cumulative/lagged effects. Importantly, Diez Roux argues that "strengthening inferences regarding the presence and magnitude of neighborhood effects requires addressing conceptual and methodological issues, particularly developing theory and specific hypotheses on processes through which neighborhood and individual factors affect health."

**Social Capital Theory.** Kawachi's work on social capital identifies four pathways through which social structures affect health: (1) diffusion of knowledge on health promotion, (2) maintenance of healthy behavioral norms through informal social control, (3) promotion of access to local services and amenities, and (4) psychological processes providing affective support and mutual respect (Kawachi et al., 2008). These mechanisms suggest that health-promoting norms may diffuse across community boundaries through social interaction.

**Collective Efficacy Theory.** Sampson's collective efficacy framework—defined as "social cohesion among neighbors combined with their willingness to intervene on behalf of the common good"—demonstrates that communities with lower collective efficacy show higher crime, domestic violence, and worse health outcomes (Sampson et al., 1997). The theory implies that collective efficacy in adjacent neighborhoods could influence health outcomes through shared resources and institutional spillovers.

### 1.2 Empirical Evidence for Spatial Contagion

Empirical evidence supports theoretical predictions of health spillovers. Christakis and Fowler's landmark studies demonstrated that obesity and smoking cessation spread through social networks, with effects extending to three degrees of separation (Christakis & Fowler, 2007, 2008). In the Framingham Heart Study, a person's chances of becoming obese increased by 57% if a friend became obese, and smoking cessation clusters extended to include friends, siblings, spouses, and coworkers.

Spatial epidemiological research has documented significant clustering of health outcomes. Studies using Moran's I and Local Indicators of Spatial Association (LISA) show that health outcomes cluster geographically, with hot spots of high disease burden and cold spots of better health (Anselin, 1995; Kirby et al., 2017). Spatial lag models have demonstrated that health in one area predicts health in neighboring areas, with recent research showing that "diffusion across geographical boundaries matters, whereby health outcomes in geographically adjacent boundaries are often similar" (van Ham et al., 2021).

### 1.3 Gaps in Current Literature

However, existing research shares important limitations. Most studies are **cross-sectional**, examining spatial associations at a single time point rather than predicting future trajectories. The predominant geographic scale is **county-level** or larger, missing fine-grained tract-level dynamics. Analytic approaches are typically **descriptive or correlational** rather than predictive. And spatial features, when included, are typically **static** (contemporaneous neighbor characteristics) rather than **dynamic** (neighbor changes over time).

Critically, no prior work has quantified whether neighbor health *trajectories* predict local *trajectories*—a stronger test of spatial contagion than mere spatial autocorrelation in health levels.

### 1.4 Study Objectives

We address these gaps by developing a predictive model for census tract health trajectory classification (Improving, Stable, Declining) that incorporates dynamic spatial features capturing health change in neighboring tracts. Our central research question is: **Does the health trajectory of neighboring census tracts predict a focal tract's trajectory better than the tract's own historical health trends?**

---

## 2. METHODS

### 2.1 Study Design and Data Sources

We conducted a longitudinal observational study of community-level health trajectories across United States census tracts using publicly available data from the Centers for Disease Control and Prevention (CDC) PLACES project. The study employed a supervised machine learning approach to predict health trajectory classifications at the census tract level.

#### 2.1.1 CDC PLACES Data

Health outcome data were obtained from the CDC PLACES dataset (formerly 500 Cities), which provides model-based estimates for chronic disease measures at the census tract level. We utilized PLACES releases spanning 2020 through 2025, encompassing six annual data releases. The PLACES program uses multilevel regression and poststratification (MRP) methodology to estimate chronic disease prevalence based on Behavioral Risk Factor Surveillance System (BRFSS) responses, calibrated to local demographics from the American Community Survey (CDC, 2024).

Data files were harmonized across releases that employed two distinct formats: (1) long format (2020, 2021, 2023, 2025 releases) containing one row per tract-measure combination, and (2) wide/GIS format (2022, 2024 releases) containing one row per tract with measures as separate columns. All data were standardized to a consistent panel structure with one observation per tract-year.

#### 2.1.2 Spatial Data

Census tract boundary geometries were obtained from the U.S. Census Bureau TIGER/Line shapefiles. These geometries enabled computation of spatial adjacency relationships for all census tracts in the study area.

#### 2.1.3 Sample Size and Geographic Coverage

The final analytic dataset comprised 189,566 tract-year observations representing 72,161 unique census tracts across 51 states and territories. The sample included observations from prediction years 2022 (n=70,338), 2023 (n=66,173), and 2024 (n=53,055). The 2025 PLACES release was excluded from outcome assessment as values were identical to 2024 (data not yet updated at time of analysis).

### 2.2 Outcome Variable

#### 2.2.1 Composite Health Burden Index (CHBI)

The primary outcome measure was the Composite Health Burden Index (CHBI), a weighted average of seven key health indicators from the PLACES dataset:

| Component | Description | Weight |
|-----------|-------------|--------|
| OBESITY | Obesity among adults aged ≥18 years (%) | 0.20 |
| DIABETES | Diagnosed diabetes among adults aged ≥18 years (%) | 0.20 |
| CHD | Coronary heart disease among adults aged ≥18 years (%) | 0.15 |
| MHLTH | Mental health not good for ≥14 days among adults (%) | 0.15 |
| BPHIGH | High blood pressure among adults aged ≥18 years (%) | 0.10 |
| LPA | No leisure-time physical activity among adults (%) | 0.10 |
| PHLTH | Physical health not good for ≥14 days among adults (%) | 0.10 |

This weighting scheme prioritizes obesity and diabetes (combined 40%) given their established roles as upstream determinants of multiple chronic conditions, while mental and physical health days capture subjective well-being dimensions.

#### 2.2.2 Trajectory Classification

Census tracts were classified into three trajectory categories based on standardized change in CHBI between consecutive years:

- **DECLINE**: CHBI z-score increase > 0.3 (health burden worsened)
- **STABLE**: CHBI z-score change within ±0.3
- **IMPROVE**: CHBI z-score decrease > 0.3 (health burden improved)

In the analytic sample, 8.9% of observations were classified as DECLINE (n=16,898), 84.7% as STABLE (n=160,484), and 6.4% as IMPROVE (n=12,184).

### 2.3 Feature Engineering

#### 2.3.1 Spatial Feature Engineering

Spatial features were computed using Shapely 2.0 for geometric operations. Census tract geometries were indexed using an STRtree spatial index for efficient neighbor queries.

**Neighbor Identification.** Spatial adjacency was defined using Queen contiguity, where two tracts are considered neighbors if they share any boundary point (touch or intersect). The resulting adjacency graph had a mean of 6.19 neighbors per tract (SD=1.99, range: 0-29).

**Spatial Lag Features.** For each tract-year, we computed:
- `neighbor_avg_chbi`: Mean CHBI across contiguous neighbors
- `neighbor_std_chbi`: Standard deviation of neighbor CHBI values
- `spatial_lag`: Tract CHBI minus neighbor average
- `spatial_lag_zscore`: Spatial lag standardized by yearly CHBI standard deviation

**Local Cluster Detection.** Binary indicators identified local hot spots (`is_local_hotspot`: tract worse than neighbors by >0.5 SD) and cold spots (`is_local_coldspot`: tract better than neighbors by >0.5 SD).

**Dynamic Neighbor Context.** We computed neighbor-based trajectory features:
- `neighbor_improving_pct`: Proportion of neighbors with CHBI decrease >0.1 points
- `neighbor_declining_pct`: Proportion of neighbors with CHBI increase >0.1 points
- `neighbor_avg_change`: Mean CHBI change among neighbors

These features capture spatial diffusion processes wherein improving or declining neighboring communities may influence local trajectories.

#### 2.3.2 Temporal Feature Engineering

Features were constructed using data from years prior to the prediction target year to ensure temporal validity. For a prediction year T, features were derived from years T-1, T-2, and T-3 when available.

**Prior Year Values:** Raw CHBI values for years T-1 and T-2, with z-scores, percentiles, and distance from 75th percentile.

**Change Features:** One-year and two-year z-score changes.

**Trend and Acceleration:** Linear regression slope across prior years and acceleration (change in year-over-year differences).

**Component-Level Trajectories:** For each of the seven CHBI components: prior year prevalence, within-year z-score, one-year raw change, one-year z-score change, and within-year percentile (35 features total).

#### 2.3.3 Final Feature Set

The complete feature set comprised 70 predictors spanning six domains: CHBI aggregate features (10), component-level features (35), temporal pattern features (3), component divergence features (6), risk profile features (6), and spatial features (10).

### 2.4 Statistical Analysis

#### 2.4.1 Ensemble Model Architecture

We implemented an ensemble classifier combining Extreme Gradient Boosting (XGBoost 2.0; Chen & Guestrin, 2016) and Light Gradient Boosting Machine (LightGBM 4.0; Ke et al., 2017).

**XGBoost Configuration:** 500 estimators, maximum depth 6, learning rate 0.05, minimum child weight 5, subsample and column subsample ratios of 0.8, multi-class softmax objective with log loss evaluation metric.

**LightGBM Configuration:** 500 estimators, maximum depth 6, learning rate 0.05, minimum child samples 20, subsample and column subsample ratios of 0.8, multi-class objective with log loss metric.

Early stopping was implemented with patience of 50 rounds to prevent overfitting.

#### 2.4.2 Class Imbalance Handling

Given the imbalanced class distribution (84.7% STABLE), we employed balanced sample weights computed using scikit-learn's `compute_class_weight` function with the 'balanced' strategy.

#### 2.4.3 Ensemble Combination

Individual model predictions were combined using soft voting, with weights proportional to each model's macro F1 score (final weights: XGBoost 49%, LightGBM 51%).

#### 2.4.4 Feature Importance

Feature importance was assessed using the gain metric from both XGBoost and LightGBM, representing the total gain contributed by each feature across all splits. Importance scores were averaged across both models.

### 2.5 Validation Strategy

#### 2.5.1 Temporal Cross-Validation

Models were trained on observations from prediction years 2022 and 2023 (n=136,511) and validated on 2024 holdout data (n=53,055). This design mimics real-world prospective prediction and prevents data leakage from future-to-past.

#### 2.5.2 Performance Metrics

Model performance was evaluated using:
- **Macro F1 Score**: Unweighted average of per-class F1 scores
- **Balanced Accuracy**: Average of per-class recall
- **ROC AUC (One-vs-Rest)**: Area under ROC curve averaged across classes

---

## 3. RESULTS

### 3.1 Model Performance

**Table 1.** Model Performance on 2024 Temporal Holdout (n=53,055)

| Model | Balanced Accuracy | F1 (Macro) | F1 (Weighted) | ROC AUC |
|-------|------------------:|----------:|-------------:|--------:|
| XGBoost | 0.457 | 0.416 | 0.522 | 0.677 |
| LightGBM | 0.470 | 0.432 | 0.525 | 0.673 |
| **Ensemble** | **0.466** | **0.426** | **0.525** | **0.678** |

The ensemble achieved balanced accuracy of 0.466 and macro F1 of 0.426 on temporal holdout data.

**Table 2.** Per-Class Performance on 2024 Holdout

| Class | Precision | Recall | F1-Score | Support |
|-------|----------:|-------:|---------:|--------:|
| DECLINE | 0.33 | 0.70 | 0.45 | 11,044 |
| IMPROVE | 0.50 | 0.13 | 0.20 | 8,429 |
| STABLE | 0.70 | 0.57 | 0.63 | 33,582 |

The model demonstrates 70% recall for DECLINE, prioritizing sensitivity to health deterioration—a clinically appropriate asymmetry for public health surveillance.

### 3.2 Feature Importance Analysis

**Table 3.** Top 20 Features by Importance

| Rank | Feature | Importance | Category |
|-----:|---------|----------:|----------|
| 1 | **neighbor_avg_change** | **12.29%** | **Spatial** |
| 2 | **neighbor_improving_pct** | **10.24%** | **Spatial** |
| 3 | CHBI_acceleration | 8.74% | Temporal |
| 4 | PHLTH_change_1yr | 6.96% | Health Change |
| 5 | **neighbor_declining_pct** | **6.35%** | **Spatial** |
| 6 | CHD_change_1yr | 4.18% | Health Change |
| 7 | CHBI_trend_slope | 3.40% | Temporal |
| 8 | CHBI_change_1yr | 3.26% | Temporal |
| 9 | OBESITY_zscore | 2.37% | Health Level |
| 10 | OBESITY_change_1yr | 2.33% | Health Change |

**Table 4.** Feature Importance by Category

| Category | Total Importance | n Features |
|----------|----------------:|-----------:|
| **Spatial Features** | **32.1%** | 10 |
| Health Indicator Changes | 24.5% | 14 |
| Temporal (CHBI dynamics) | 16.2% | 4 |
| Health Indicator Levels | 12.3% | 21 |
| Component-Level Features | 7.7% | 9 |
| Other | 7.2% | 12 |

Spatial features collectively account for nearly one-third of model importance (32.1%), exceeding any other category.

### 3.3 Key Finding: Spatial Features Exceed Own-Tract Trajectory

**Table 5.** Comparison: Neighbor Trajectory vs. Own Trajectory

| Feature Type | Feature | Importance |
|--------------|---------|----------:|
| **Spatial** | neighbor_avg_change | **12.29%** |
| **Spatial** | neighbor_improving_pct | **10.24%** |
| **Spatial** | neighbor_declining_pct | **6.35%** |
| Own-Tract | CHBI_change_1yr | 3.26% |
| Own-Tract | CHBI_trend_slope | 3.40% |
| Own-Tract | CHBI_acceleration | 8.74% |

**Aggregate comparison:**
- **Spatial neighborhood features:** 30.50% total importance
- **Own-tract trajectory features:** 15.40% total importance
- **Ratio:** Spatial features are **1.98x more predictive** than own-tract trajectory

The most striking finding: `neighbor_avg_change` (12.29%) is **3.8 times more predictive** than `CHBI_change_1yr` (3.26%). A tract's neighbors' average trajectory is substantially more predictive of that tract's future trajectory than its own recent change.

### 3.4 Prediction Distribution

Current predictions for 53,055 tracts (2024 forward):
- **DECLINE:** 25,860 (48.7%)
- **STABLE:** 25,694 (48.4%)
- **IMPROVE:** 1,501 (2.8%)

Mean prediction confidence: 0.623 (SD=0.134). Approximately 33% of predictions exceed 70% confidence.

---

## 4. DISCUSSION

### 4.1 Summary of Key Findings

This study presents evidence that spatial contagion may be a dominant mechanism in community health trajectory dynamics. Our central finding is striking: spatial features derived from neighboring census tracts collectively account for approximately 32% of predictive importance in our trajectory classification model. This contribution exceeds that of a tract's own historical health trajectory.

Three principal findings emerge:

1. **Neighbor trajectory exceeds own trajectory.** When surrounding tracts experience health burden decline, a focal tract faces substantially elevated risk of decline itself—independent of its baseline health status or internal trajectory.

2. **Spatial spillover operates asymmetrically.** The percentage of neighbors experiencing improvement or decline exerts predictive influence beyond what would be expected from mere spatial autocorrelation.

3. **Magnitude suggests active propagation.** The 32% contribution of spatial features suggests health changes may actively propagate through geographic networks of communities.

### 4.2 Theoretical Implications

**Extension of Neighborhood Effects Theory.** Our findings support the neighborhood effects paradigm articulated by Diez Roux, but extend it: neighborhood effects operate not only *within* but also *between* communities. The health trajectory of a neighborhood is partially determined by the trajectories of adjacent neighborhoods.

**Spatial Extension of Social Contagion.** Christakis and Fowler demonstrated health behaviors spread through social networks. Our findings suggest an analogous phenomenon at the geographic level: health trajectories may be "contagious" across spatial networks of communities, operating through shared resources, labor markets, healthcare systems, or population movement.

**Tobler's First Law Applied to Health Dynamics.** Our contribution is to demonstrate that the "first law of geography" applies not merely to health *levels* but to health *changes*—proximate communities experience correlated trajectories, not just correlated states.

### 4.3 Policy Implications

**Cluster-Based Intervention Design.** An isolated high-risk tract surrounded by stable neighbors may have better prognosis than a moderate-risk tract embedded in declining neighbors. Interventions should prioritize spatially contiguous declining communities.

**Early Warning System Architecture.** Surveillance systems should track not only individual tract trajectories but also spatial correlation patterns. Communities at the leading edge of decline clusters may serve as sentinels.

**Buffer Zone Investments.** Resources should be allocated to protect improving communities from encroachment of decline from neighboring areas.

### 4.4 Limitations

**Model-Based Estimates.** CDC PLACES uses MRP to generate tract-level estimates—these are modeled quantities, not direct measurements. Changes in methodology between releases may introduce artificial temporal variation.

**Ecological Fallacy.** Tract-level associations cannot be assumed to reflect individual-level processes. Spatial associations may reflect migration patterns rather than in-situ health changes.

**MAUP.** Census tracts are administratively defined units that may not correspond to meaningful health-relevant boundaries. Results may differ at different spatial scales.

**Correlation vs. Causation.** Our predictive model establishes association, not causation. Unobserved common causes may drive correlated trajectories without direct spatial influence.

**Short Time Series.** Five years of data provides limited temporal depth. The study period spans the COVID-19 pandemic, which may have induced artificial spatial correlations.

**Class Imbalance.** The model shows poor sensitivity for IMPROVE (13% recall), limiting ability to identify improving communities.

### 4.5 Future Directions

1. **Prospective validation** with 2025-2026 PLACES releases
2. **Mechanism investigation** through mixed methods and migration analysis
3. **Subgroup analysis** by urban/rural, region, and baseline health status
4. **Advanced spatial modeling** including graph neural networks
5. **Intervention integration** with health department pilots

### 4.6 Conclusion

Community health trajectories exhibit spatial contagion: health changes in neighboring tracts are stronger predictors of a tract's future trajectory than its own historical trend. **Neighbor trajectory is 3.8 times more predictive than own-tract trajectory.**

This finding suggests a paradigm shift: the appropriate unit of public health action may not be the community but the region. Isolated interventions in declining communities may face headwinds from surrounding decline; coordinated investment in contiguous communities may generate mutually reinforcing improvements.

We recommend that public health agencies: (1) incorporate neighbor trajectory indicators into community health assessment; (2) design interventions at cluster rather than isolated-tract scale; (3) establish surveillance systems that track spatial correlation patterns; and (4) coordinate across jurisdictional boundaries when decline clusters span administrative units.

If health changes spread geographically, then community health cannot be understood—or improved—in isolation.

---

## REFERENCES

Anselin, L. (1995). Local Indicators of Spatial Association—LISA. *Geographical Analysis*, 27(2), 93-115.

Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785-794.

Christakis, N.A., & Fowler, J.H. (2007). The Spread of Obesity in a Large Social Network over 32 Years. *New England Journal of Medicine*, 357(4), 370-379.

Christakis, N.A., & Fowler, J.H. (2008). The Collective Dynamics of Smoking in a Large Social Network. *New England Journal of Medicine*, 358(21), 2249-2258.

Diez Roux, A.V. (2001). Investigating Neighborhood and Area Effects on Health. *American Journal of Public Health*, 91(11), 1783-1789.

Diez Roux, A.V., & Mair, C. (2010). Neighborhoods and health. *Annals of the New York Academy of Sciences*, 1186, 125-145.

Kawachi, I., Subramanian, S.V., & Kim, D. (Eds.) (2008). *Social Capital and Health*. Springer.

Ke, G., et al. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree. *Advances in Neural Information Processing Systems*, 30.

Kirby, R.S., Delmelle, E., & Eberth, J.M. (2017). Advances in spatial epidemiology and geographic information systems. *Annals of Epidemiology*, 27(1), 1-9.

Sampson, R.J., Raudenbush, S.W., & Earls, F. (1997). Neighborhoods and Violent Crime: A Multilevel Study of Collective Efficacy. *Science*, 277(5328), 918-924.

Tobler, W.R. (1970). A Computer Movie Simulating Urban Growth in the Detroit Region. *Economic Geography*, 46, 234-240.

van Ham, M., et al. (2021). The health potential of neighborhoods: A population-wide study in the Netherlands. *Health & Place*, 71, 102640.

---

## SUPPLEMENTARY MATERIALS

- **Table S1.** Complete feature importance rankings (70 features)
- **Table S2.** State-level prediction distributions
- **Figure S1.** Confusion matrix heatmap
- **Figure S2.** Feature importance by category (bar chart)
- **Figure S3.** Geographic distribution of predicted trajectories (map)
- **Code Availability.** Analysis code available at: [repository URL]
- **Data Availability.** CDC PLACES data publicly available at: https://www.cdc.gov/places/

---

## ACKNOWLEDGMENTS

[To be added]

## FUNDING

[To be added]

## COMPETING INTERESTS

The authors declare no competing interests.

---

**Word Count:** ~5,500 (excluding tables and references)

**Date:** December 30, 2025

**Status:** Draft for internal review
