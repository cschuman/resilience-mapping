# Community Health Trajectory Prediction System: Research Design

## Executive Summary

This document outlines the design for a novel **Community Health Trajectory Prediction** system - an early warning system that predicts which census tracts will experience health burden **DECLINE or IMPROVEMENT** before it happens. This represents a significant advancement over existing cross-sectional analyses by incorporating temporal dynamics and predictive modeling.

**Key Innovation**: Moving from "which communities are resilient now?" to "which communities are about to tip toward decline or improvement?"

---

## 1. Research Question and Novel Contribution

### Primary Research Question
**Can we predict 12-24 month ahead changes in community health trajectories using longitudinal CDC PLACES data, social determinants of health, and spatiotemporal features?**

### What Makes This Novel and Publishable

Based on comprehensive literature review, this work would be **genuinely novel** in these ways:

1. **First Application of Trajectory Prediction to CDC PLACES Data**
   - CDC PLACES has only been available since 2020, with longitudinal data now spanning 5+ years
   - Existing literature focuses on cross-sectional analysis or simple trend detection
   - No published work uses PLACES for prospective trajectory prediction at census tract level

2. **Multi-Outcome Composite Health Trajectory**
   - Rather than predicting single outcomes (diabetes, obesity), we predict **composite health burden trajectory**
   - Captures syndemics and co-occurring conditions more realistically
   - Aligns with social determinants of health framework

3. **Hybrid Spatiotemporal Model Architecture**
   - Combines temporal sequence modeling (LSTM) with spatial autocorrelation features
   - Addresses both "when will it happen" and "where will it spread"
   - Novel feature engineering incorporating neighborhood change indicators

4. **Actionable Early Warning System**
   - Designed for public health intervention planning (not just academic prediction)
   - Provides probabilistic risk scores with uncertainty quantification
   - Identifies "tipping point" communities in time for intervention

5. **Gentrification-Health Trajectory Integration**
   - Links neighborhood socioeconomic change to health trajectory shifts
   - Tests hypothesis that gentrification patterns predict health transitions
   - Uses satellite imagery and census data to detect early neighborhood change signals

### Target Journals
- **American Journal of Public Health** (high impact, public health focus)
- **Health & Place** (spatial epidemiology)
- **JAMA Network Open** (broad medical audience, open access)
- **Social Science & Medicine** (SDOH focus)

---

## 2. Data Sources and Temporal Structure

### 2.1 Primary Longitudinal Data: CDC PLACES

**Available Years**: 2020, 2021, 2022, 2023, 2024, 2025 (6 annual releases)

**Key Health Outcomes** (40 measures total in 2025 release):
- Health Outcomes (12): Obesity, diabetes, CHD, stroke, COPD, kidney disease, cancer, asthma, depression, etc.
- Prevention (7): Checkups, dental visits, vaccines, screenings
- Health Risk Behaviors (4): Smoking, binge drinking, physical inactivity, sleep
- Disability (7): Cognitive, hearing, vision, mobility, self-care, independent living
- Health Status (3): General health, physical health days, mental health days
- Health-Related Social Needs (7): Food insecurity, housing instability, transportation barriers, etc.

**Critical Methodological Note**: PLACES uses model-based estimates (multilevel regression and poststratification), not direct measurements. This means:
- Estimates include uncertainty (confidence intervals)
- Temporal changes may reflect model updates, not true population changes
- Need to account for this in validation strategy

### 2.2 Social Determinants Features (Census ACS 5-Year Estimates)

**Demographic Change Indicators**:
- Population change rate
- Age distribution shifts (median age delta)
- Racial/ethnic composition changes
- Educational attainment trends
- Household structure changes

**Economic Trajectory Indicators**:
- Median income change (absolute and percentile)
- Poverty rate trends
- Employment/unemployment rate changes
- Housing cost burden changes
- Rent/home value appreciation rates

**Neighborhood Change Indicators** (Gentrification Proxies):
- College-educated population growth
- Median income percentile shift within metro area
- Rent/home value growth vs metro median
- White population share change (in historically non-white areas)
- Change in share of new residents

### 2.3 Spatial Features

**Geographic Context**:
- Spatial lag (average health of neighboring tracts)
- Local Moran's I (spatial clustering statistic)
- Distance to healthcare facilities
- Tract-level walkability/transit access scores

**Administrative Geography**:
- County fixed effects
- Metropolitan vs rural classification
- State policy environment indicators

### 2.4 External Validation Data

**Food Access (USDA FARA)**: 2015, 2019 releases
- Low-Income Low-Access (LILA) designation
- Supermarket proximity
- Vehicle access rates

**County Health Rankings**: Annual rankings of health factors and outcomes

---

## 3. Trajectory Definition and Target Variable

### 3.1 Composite Health Burden Index (CHBI)

We construct a **Composite Health Burden Index** from PLACES data:

```
CHBI = weighted_mean([
    Obesity_prevalence,
    Diabetes_prevalence,
    CHD_prevalence,
    BPHIGH_prevalence,
    Physical_inactivity,
    Poor_mental_health_days,
    Poor_physical_health_days
])
```

Weights determined by:
- Mortality burden (years of life lost)
- Healthcare cost impact
- Prevention amenability

**Standardization**: Z-score within each year to account for:
- National trend changes
- Model estimation improvements
- Population aging effects

### 3.2 Trajectory Classification (Target Variable)

**Three-Class Problem**:

1. **DECLINE** (health burden increasing):
   - CHBI increases by >0.5 SD over next 12-24 months
   - OR crosses critical threshold (e.g., top quartile)
   - OR acceleration in negative direction (2nd derivative test)

2. **STABLE** (minimal change):
   - CHBI change within ±0.5 SD
   - Trajectory slope not significantly different from zero

3. **IMPROVE** (health burden decreasing):
   - CHBI decreases by >0.5 SD over next 12-24 months
   - OR drops below critical threshold
   - OR acceleration in positive direction

**Alternative: Continuous Trajectory Modeling**
- Predict CHBI_t+12 - CHBI_t (regression)
- Predict probability distribution over future CHBI (distributional forecasting)
- Predict time-to-event (survival analysis for crossing thresholds)

**Recommended Approach**: Start with 3-class classification (interpretable, actionable), then extend to continuous for increased precision.

### 3.3 Temporal Horizon

**Prediction Target**: 12-month ahead (primary), 24-month ahead (secondary)

**Rationale**:
- 12 months aligns with annual planning cycles for health departments
- 24 months allows for multi-year intervention design
- Longer horizons (36+ months) likely too uncertain given data limitations

---

## 4. Feature Engineering Strategy

### 4.1 Temporal Features (From PLACES Time Series)

**Trend Features** (requires 3+ historical observations):
```python
# Linear trend slope
slope = linregress(years, CHBI_values).slope

# Acceleration (2nd derivative)
acceleration = CHBI[t] - 2*CHBI[t-1] + CHBI[t-2]

# Volatility (standard deviation of year-to-year changes)
volatility = std(diff(CHBI_values))

# Momentum (rate of change)
momentum = (CHBI[t] - CHBI[t-1]) / CHBI[t-1]

# Relative position (percentile within distribution)
percentile_rank = percentileofscore(all_tracts_CHBI, tract_CHBI)

# Distance from threshold
distance_to_high_risk = threshold_95th_percentile - CHBI[t]
```

**Outcome-Specific Trends**:
- Individual slopes for obesity, diabetes, CHD, etc.
- Identifies which conditions are driving overall burden changes

### 4.2 Social Determinant Change Features

**Economic Mobility Indicators**:
```python
# Income trajectory (3-year moving average)
income_trajectory = (income[t] - income[t-3]) / income[t-3]

# Income acceleration
income_acceleration = income[t] - 2*income[t-1] + income[t-2]

# Relative position within metro area
income_metro_percentile_change = percentile[t] - percentile[t-3]

# Poverty rate velocity
poverty_velocity = poverty_rate[t] - poverty_rate[t-1]
```

**Gentrification Risk Score**:
```python
# Based on Freeman (2005) and Ding et al. (2016) definitions
gentrification_risk = (
    (college_educated_growth > metro_median) * 0.3 +
    (income_percentile_increase > 10) * 0.3 +
    (rent_growth > metro_median * 1.5) * 0.2 +
    (white_population_increase AND historically_nonwhite) * 0.2
)
```

**Population Churn**:
```python
# Residential instability (predictor of health disruption)
churn_rate = (moved_in_last_year / total_population)
churn_acceleration = churn_rate[t] - churn_rate[t-1]
```

### 4.3 Spatial Features

**Spatial Lag** (average of neighbors):
```python
# Queen contiguity (shares edge or vertex)
W = spatial_weights_matrix(tracts, type='queen')

# Spatial lag of CHBI
spatial_lag_CHBI = W @ CHBI_values

# Spatial lag of CHBI change
spatial_lag_change = W @ (CHBI[t] - CHBI[t-1])

# Spatial spillover (are neighbors improving or declining?)
neighbor_trajectory = W @ trajectory_labels
```

**Local Spatial Autocorrelation**:
```python
# Local Moran's I (clustering statistic)
local_morans_I = calculate_local_morans(CHBI_values, W)

# Cluster classification
# HH = High-High (hot spot)
# LL = Low-Low (cold spot)
# HL = High-Low (outlier)
# LH = Low-High (outlier)
cluster_type = classify_clusters(local_morans_I)
```

**Distance-Based Features**:
```python
# Distance to nearest declining tract
distance_to_decline = min_distance(tract, declining_tracts)

# Count of declining tracts within 5km
decline_density = count_within_radius(tract, declining_tracts, radius=5)
```

### 4.4 Interaction Features

**Critical Interactions**:
- `gentrification_risk × low_income` (displacement vulnerability)
- `spatial_lag_decline × residential_instability` (contagion risk)
- `poverty_acceleration × lack_healthcare_access` (healthcare utilization barrier)
- `population_churn × social_capital_proxy` (resilience vs fragmentation)

---

## 5. Modeling Approach: Hybrid Spatiotemporal Architecture

### 5.1 Recommended Model: Ensemble of Specialized Models

Based on literature review, no single model dominates for spatiotemporal health prediction. Recommendation: **Stacked ensemble combining complementary strengths**.

#### Tier 1: Base Models

**Model 1: Gradient Boosted Trees (XGBoost/LightGBM)**
- **Strengths**: Handles non-linear relationships, feature interactions, missing data
- **Architecture**:
  - Input: All engineered features (tabular format)
  - Loss: Multi-class log loss (3-class trajectory)
  - Regularization: Max depth=6, min_child_weight=5, subsample=0.8
  - Feature importance via SHAP values

**Model 2: LSTM Sequence Model**
- **Strengths**: Captures temporal dependencies, irregular time intervals
- **Architecture**:
  - Input: Sequence of CHBI and SDOH features over T=4 historical years
  - Hidden layers: 2-layer LSTM (64 units each) + Dropout (0.3)
  - Output: Softmax over 3 trajectory classes
  - Attention mechanism to weight recent vs distant past

**Model 3: Spatial Autoregressive Model (SAR)**
- **Strengths**: Explicitly models spatial spillovers and neighborhood effects
- **Architecture**:
  - Spatial lag specification: Y = ρWY + Xβ + ε
  - Where W = spatial weights matrix, ρ = spatial autocorrelation parameter
  - Combined with logistic regression for classification

**Model 4: Random Forest (Baseline)**
- **Strengths**: Robust, interpretable, requires minimal tuning
- **Architecture**:
  - 500 trees, max_features='sqrt'
  - Used as benchmark and for feature importance validation

#### Tier 2: Ensemble Meta-Learner

**Stacking Approach**:
```python
# Base model predictions as meta-features
meta_features = [
    xgboost_probs,      # (N, 3) - class probabilities
    lstm_probs,         # (N, 3)
    sar_probs,          # (N, 3)
    rf_probs,           # (N, 3)
    xgboost_leaf_index, # (N, num_trees) - for diversity
]

# Meta-learner: Logistic regression with L2 regularization
meta_model = LogisticRegressionCV(cv=5, penalty='l2')
final_predictions = meta_model.fit(meta_features, trajectory_labels)
```

**Why Stacking?**
- Combines temporal modeling (LSTM) with spatial modeling (SAR) and non-linear feature learning (XGBoost)
- Reduces variance compared to single models
- Achieves better calibration of predicted probabilities

### 5.2 Alternative Cutting-Edge Approach: Spatiotemporal Graph Neural Network

**If Computational Resources Allow**:

Use **Graph Convolutional Network + Gated Recurrent Units (GCN-GRU)**:
- Nodes = census tracts
- Edges = spatial adjacency (queen contiguency) + similarity (demographic distance)
- Node features = time series of CHBI and SDOH indicators
- GCN layers capture spatial dependencies
- GRU layers capture temporal dynamics
- Output = trajectory class probabilities

**Advantages**:
- Joint spatiotemporal modeling (no separate spatial/temporal steps)
- Learns optimal spatial connectivity (vs fixed weights matrix)
- State-of-the-art for traffic forecasting, epidemic modeling

**Disadvantages**:
- Requires deep learning expertise
- Less interpretable (black box)
- Needs large training sample (may be marginal with ~70k tracts)

**Recommendation**: Start with ensemble approach (more interpretable, proven), explore GCN-GRU as extension for ML-focused journal.

---

## 6. Validation Strategy: Temporal Cross-Validation

### 6.1 Critical Challenge: Avoiding Data Leakage

**The Problem**:
Standard k-fold CV is invalid for temporal prediction - creates "future information leakage"

**Example of Leakage**:
```
Train on 2022-2023 → Predict 2024 ✓ VALID
Train on 2024 → Predict 2023 ✗ INVALID (using future to predict past)
```

### 6.2 Proper Temporal Validation: Expanding Window

**Strategy**: Mimic real-world deployment where we only have data up to time T to predict T+1.

```python
# Temporal splits (assuming 2020-2025 data)
splits = [
    # Split 1: Train on 2020-2021, validate on 2022 prediction (using 2020-2021 to predict 2022)
    {
        'train_years': [2020, 2021],
        'predict_year': 2022,
        'features_cutoff': 2021,  # Only use data available by end of 2021
        'target': '2022 trajectory'
    },
    # Split 2: Train on 2020-2022, validate on 2023 prediction
    {
        'train_years': [2020, 2021, 2022],
        'predict_year': 2023,
        'features_cutoff': 2022,
        'target': '2023 trajectory'
    },
    # Split 3: Train on 2020-2023, validate on 2024 prediction
    {
        'train_years': [2020, 2021, 2022, 2023],
        'predict_year': 2024,
        'features_cutoff': 2023,
        'target': '2024 trajectory'
    },
    # Split 4: Train on 2020-2024, validate on 2025 prediction
    {
        'train_years': [2020, 2021, 2022, 2023, 2024],
        'predict_year': 2025,
        'features_cutoff': 2024,
        'target': '2025 trajectory'
    }
]
```

**Final Model**: Train on all 2020-2024 data to predict 2026 trajectories (true out-of-sample forecast).

### 6.3 Performance Metrics

**Classification Metrics**:
- **Balanced Accuracy**: Account for class imbalance (most tracts are STABLE)
- **F1-Score (Macro)**: Harmonic mean of precision/recall across classes
- **AUC-ROC (One-vs-Rest)**: Discrimination ability for each trajectory class
- **Cohen's Kappa**: Agreement beyond chance (accounts for imbalance)

**Probabilistic Calibration**:
- **Brier Score**: Mean squared error of predicted probabilities
- **Expected Calibration Error (ECE)**: Are 70% confidence predictions correct 70% of time?
- **Reliability Diagrams**: Visual assessment of calibration

**Early Warning Performance**:
- **Sensitivity for DECLINE class**: Primary goal is catching deteriorating tracts
- **Positive Predictive Value (PPV)**: Of tracts flagged for intervention, what % actually decline?
- **Lead Time**: How many months in advance can we predict transitions?

**Spatial Validation**:
- **Leave-One-County-Out CV**: Test generalization to new geographies
- **Urban vs Rural Stratification**: Ensure model works across contexts

### 6.4 Benchmark Comparisons

**Naive Baselines**:
1. **Persistence Model**: Predict future trajectory = current trajectory
2. **Historical Average**: Predict based on long-term mean trajectory
3. **Linear Trend Extrapolation**: Fit linear trend, extrapolate forward

**Informed Baselines**:
1. **Logistic Regression**: Using all engineered features (tests if complexity helps)
2. **ARIMA**: Classical time series forecasting for CHBI

**Success Criterion**:
- Ensemble model should improve F1-score by ≥10% over best baseline
- Particularly strong improvement on DECLINE class (early warning utility)

---

## 7. Implementation Roadmap

### Phase 1: Data Preparation (Weeks 1-2)

**Tasks**:
1. Download CDC PLACES data for all years (2020-2025)
2. Download Census ACS 5-year estimates (2015-2023)
3. Create unified tract ID mapping (handle 2010 vs 2020 census boundary changes)
4. Merge data into analysis-ready format

**Deliverable**: `/data/processed/trajectory_analysis_ready.parquet`

**Code Location**: `/app/analytics/prepare_trajectory_data.py`

### Phase 2: Feature Engineering (Weeks 3-4)

**Tasks**:
1. Construct Composite Health Burden Index (CHBI)
2. Calculate temporal features (slopes, acceleration, volatility)
3. Engineer SDOH change features (gentrification risk, income mobility)
4. Compute spatial features (lag, Local Moran's I, distances)
5. Create interaction terms
6. Generate target labels (DECLINE, STABLE, IMPROVE)

**Deliverable**: `/data/processed/features_and_targets.parquet`

**Code Location**: `/app/analytics/engineer_trajectory_features.py`

### Phase 3: Exploratory Analysis (Week 5)

**Tasks**:
1. Descriptive statistics of trajectory distribution
2. Visualize spatial patterns of declining/improving tracts
3. Feature correlation analysis
4. Time series plots of high-risk tracts
5. Generate hypothesis-generating plots for paper

**Deliverable**: `/docs/research/eda_trajectory_patterns.md`

**Code Location**: `/app/analytics/explore_trajectories.py`

### Phase 4: Model Development (Weeks 6-8)

**Tasks**:
1. Implement temporal cross-validation framework
2. Train baseline models (persistence, linear regression)
3. Train Tier 1 models (XGBoost, LSTM, SAR, RF)
4. Hyperparameter tuning via nested CV
5. Train meta-learner ensemble
6. Evaluate on all splits

**Deliverable**:
- Trained models in `/models/trajectory_prediction/`
- Evaluation metrics in `/results/cv_performance.csv`

**Code Location**: `/app/analytics/train_trajectory_models.py`

### Phase 5: Model Interpretation (Week 9)

**Tasks**:
1. SHAP value analysis (global and local explanations)
2. Feature importance rankings
3. Partial dependence plots for key features
4. Case studies of correctly vs incorrectly predicted tracts
5. Spatial visualization of predictions

**Deliverable**: `/docs/research/model_interpretation.md`

**Code Location**: `/app/analytics/interpret_models.py`

### Phase 6: Validation and Robustness (Week 10)

**Tasks**:
1. Sensitivity analysis (feature subsets, hyperparameters)
2. Spatial cross-validation (leave-one-state-out)
3. Subgroup analysis (urban/rural, by region, by baseline health)
4. Uncertainty quantification (confidence intervals on predictions)
5. External validation (if additional year of data becomes available)

**Deliverable**: `/results/robustness_checks.md`

**Code Location**: `/app/analytics/validate_trajectories.py`

### Phase 7: Deployment (Week 11-12)

**Tasks**:
1. Create interactive web app for early warning system
2. Dashboard showing:
   - Map of predicted declining/improving tracts
   - Risk scores with confidence intervals
   - Feature explanations (why is this tract at risk?)
   - Historical trajectory plots
3. Generate PDF reports for health departments
4. API endpoint for programmatic access

**Deliverable**:
- Web app deployed to `https://resilience-mapping.fly.dev/trajectory-predictor`
- API documentation

**Code Location**: `/app/web/src/routes/trajectory/`

---

## 8. Expected Results and Publishable Findings

### 8.1 Primary Hypotheses

**H1: Temporal Prediction is Feasible**
- Expected: F1-score ≥ 0.65 for 12-month ahead prediction (vs ~0.50 for random)
- Threshold for publication: Significantly better than persistence baseline (p < 0.01)

**H2: Ensemble Outperforms Single Models**
- Expected: 5-10% improvement in balanced accuracy over best single model
- Demonstrates value of combining temporal + spatial + non-linear modeling

**H3: Gentrification Predicts Health Trajectory Shifts**
- Expected: High gentrification risk score associated with 2-3x odds of DECLINE
- Mechanism: Displacement, stress, loss of social networks
- Novel contribution to gentrification-health literature

**H4: Spatial Spillovers are Significant**
- Expected: Spatial lag features among top 10 most important predictors
- Tracts near declining tracts have 1.5-2x risk of decline themselves
- Supports targeted geographic intervention strategies

**H5: Early Warning Lead Time is 12+ Months**
- Expected: Model can predict trajectory shifts 12-18 months in advance
- Actionable for public health planning (intervention design, resource allocation)

### 8.2 Key Findings for Paper

**Primary Outcome**: Model Performance
- Report temporal CV performance (F1, AUC, balanced accuracy)
- Compare to baselines and prior work
- Visualize predictions on map

**Secondary Outcomes**:
1. **Feature Importance Rankings**: What predicts decline vs improvement?
2. **Spatial Patterns**: Where are tipping point communities?
3. **Subgroup Heterogeneity**: Does model work equally well for urban/rural, different regions?
4. **Case Studies**: Deep dive into exemplar declining and improving tracts

**Policy Implications**:
- Identify high-risk tracts for proactive intervention
- Test whether social determinant changes precede health changes (causal ordering)
- Quantify spillover effects to guide geographic targeting

### 8.3 Limitations and Mitigations

**Limitation 1: Model-Based Estimates in PLACES**
- PLACES uses MRP, not direct measurements
- Temporal changes may reflect model updates, not true population shifts
- **Mitigation**: Validate against external data (BRFSS direct estimates where available), sensitivity analysis excluding tracts with wide confidence intervals

**Limitation 2: Short Time Series (6 years)**
- Limits ability to detect long-term cycles
- Insufficient data for deep learning methods (LSTM may underfit)
- **Mitigation**: Acknowledge as early-stage work, call for replication as more years accumulate

**Limitation 3: Census Boundary Changes**
- 2020 census redefined tract boundaries
- Complicates longitudinal analysis
- **Mitigation**: Use crosswalk files to harmonize to consistent geography, sensitivity analysis with 2010-only tracts

**Limitation 4: Ecological Fallacy**
- Tract-level patterns don't imply individual-level causation
- Compositional vs contextual effects unresolved
- **Mitigation**: Clearly state ecological nature, recommend individual-level validation studies

**Limitation 5: Confounding by Unmeasured Variables**
- Cannot capture all relevant factors (e.g., policy changes, environmental exposures)
- Residual confounding likely
- **Mitigation**: Include comprehensive SDOH features, spatial fixed effects, discuss unmeasured confounders

---

## 9. Extensions and Future Work

### 9.1 Short-Term Extensions (3-6 Months)

1. **Outcome-Specific Predictions**: Separate models for diabetes, obesity, mental health
2. **Survival Analysis**: Time-to-event modeling for crossing thresholds
3. **Uncertainty Quantification**: Bayesian models, conformal prediction intervals
4. **Intervention Simulation**: What-if scenarios (e.g., "what if poverty rate decreases 5%?")

### 9.2 Medium-Term Extensions (6-12 Months)

1. **Causal Inference**: Difference-in-differences for policy interventions (e.g., Medicaid expansion)
2. **Agent-Based Modeling**: Simulate individual-level dynamics driving tract-level patterns
3. **Natural Language Processing**: Extract features from county health improvement plans
4. **Multi-City Deep Dives**: Qualitative validation with health departments

### 9.3 Long-Term Vision (1-2 Years)

1. **Real-Time Monitoring**: Dashboard with quarterly updates as new PLACES data released
2. **Multi-Modal Data Integration**: Satellite imagery (built environment), Google mobility, social media
3. **Intervention Trials**: Partner with health departments to test early warning system in practice
4. **National Rollout**: Deploy as CDC tool for all local health departments

---

## 10. Code Architecture

### Recommended File Structure

```
/app/analytics/trajectory_prediction/
├── __init__.py
├── data_preparation.py          # Phase 1: Load and merge data
├── feature_engineering.py       # Phase 2: Create features and targets
├── exploratory_analysis.py      # Phase 3: EDA and visualization
├── models/
│   ├── __init__.py
│   ├── base_models.py           # Baseline models
│   ├── xgboost_model.py         # Gradient boosting
│   ├── lstm_model.py            # Sequence model (PyTorch)
│   ├── spatial_model.py         # SAR model
│   ├── ensemble.py              # Stacking meta-learner
│   └── graph_neural_net.py      # (Optional) GCN-GRU
├── validation.py                # Temporal CV framework
├── interpretation.py            # SHAP, feature importance
├── evaluation.py                # Metrics, calibration plots
├── utils/
│   ├── spatial_utils.py         # Spatial weights, Moran's I
│   ├── temporal_utils.py        # Trend calculation, differencing
│   └── plot_utils.py            # Visualization helpers
├── config.py                    # Hyperparameters, paths
└── main.py                      # End-to-end pipeline

/app/web/src/routes/trajectory/
├── +page.svelte                 # Trajectory prediction dashboard
├── +page.server.ts              # Load model predictions
└── components/
    ├── TrajectoryMap.svelte     # Interactive map
    ├── RiskScore.svelte         # Tract-level risk display
    └── FeatureExplanation.svelte # SHAP waterfall plot
```

### Key Dependencies

**Python Packages**:
```
# Data manipulation
pandas>=2.0
numpy>=1.24
pyarrow>=12.0  # For parquet files

# Geospatial
geopandas>=0.13
libpysal>=4.7  # Spatial weights, Moran's I
shapely>=2.0

# Machine learning
scikit-learn>=1.3
xgboost>=2.0
lightgbm>=4.0
pytorch>=2.0  # For LSTM, GNN
pytorch-geometric>=2.3  # For GNN (optional)

# Interpretation
shap>=0.42
lime>=0.2

# Visualization
matplotlib>=3.7
seaborn>=0.12
plotly>=5.14

# Utilities
tqdm  # Progress bars
joblib  # Parallel processing
pyyaml  # Config files
```

---

## 11. Timeline and Milestones

| Phase | Duration | Deliverable | Success Metric |
|-------|----------|-------------|----------------|
| 1. Data Prep | 2 weeks | Analysis-ready dataset | 70k+ tracts with complete features |
| 2. Features | 2 weeks | Feature matrix + targets | 50+ features, 3-class labels balanced |
| 3. EDA | 1 week | EDA report | 10+ publication-quality plots |
| 4. Modeling | 3 weeks | Trained ensemble | F1 > 0.65 on validation set |
| 5. Interpretation | 1 week | Feature importance report | Identify top 10 predictors |
| 6. Validation | 1 week | Robustness checks | Consistent performance across splits |
| 7. Deployment | 2 weeks | Web app + API | <2 sec load time, accessible |
| **TOTAL** | **12 weeks** | **Draft manuscript** | **Ready for journal submission** |

---

## 12. Resources and References

### Key Papers Cited in This Design

**Trajectory Modeling Methods**:
- [Hybrid ARIMA-LSTM for COVID-19 prediction](https://pmc.ncbi.nlm.nih.gov/articles/PMC11671211/) - Health Care Science, 2024
- [Cancer symptom trajectory prediction with LSTM](https://pmc.ncbi.nlm.nih.gov/articles/PMC10948138/) - 2024
- [Predictive modeling of biomedical temporal data: review](https://pmc.ncbi.nlm.nih.gov/articles/PMC11519529/) - Frontiers in Physiology, 2024

**Gentrification and Health**:
- [Gentrification prediction using machine learning](https://link.springer.com/chapter/10.1007/978-3-030-33749-0_16) - Springer, 2019
- [Building a predictive ML model of gentrification in Sydney](https://www.sciencedirect.com/science/article/abs/pii/S0264275123000045) - Cities, 2023
- [How we used ML to predict neighborhood change](https://urban-institute.medium.com/how-we-used-machine-learning-to-predict-neighborhood-change-bf52c9f32fda) - Urban Institute

**Social Determinants and ML**:
- [Quantification of neighborhood-level SDOH](https://pmc.ncbi.nlm.nih.gov/articles/PMC6991288/) - JAMA Network Open, 2020
- [Value of neighborhood SES in predicting risk](https://pmc.ncbi.nlm.nih.gov/articles/PMC6324505/) - 2019
- [Incorporating ML and SDOH into prospective risk adjustment](https://bmcpublichealth.biomedcentral.com/articles/10.1186/s12889-020-08735-0) - BMC Public Health, 2020

**Early Warning Systems**:
- [Early warning systems for acute respiratory infections: scoping review](https://publichealth.jmir.org/2024/1/e62641) - JMIR Public Health Surveillance, 2024
- [Effectiveness of early warning systems for infectious disease outbreaks](https://link.springer.com/article/10.1186/s12889-022-14625-4) - BMC Public Health, 2022
- [Toward development of disease early warning systems](https://www.ncbi.nlm.nih.gov/books/NBK222241/) - NCBI Bookshelf

**Spatial Methods**:
- [COVID-19 dynamic monitoring and real-time spatiotemporal forecasting](https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2021.641253/full) - Frontiers Public Health, 2021

**CDC PLACES Documentation**:
- [PLACES: Local Data for Better Health](https://www.cdc.gov/places/index.html)
- [PLACES Methodology](https://www.cdc.gov/places/methodology/index.html)
- [PLACES: 2025 release](https://data.cdc.gov/500-Cities-Places/PLACES-Local-Data-for-Better-Health-Census-Tract-D/cwsq-ngmh)

---

## 13. Summary: Why This is Publishable

### Novelty Checklist

✅ **First application of trajectory prediction to CDC PLACES longitudinal data**
✅ **Combines temporal modeling (LSTM) with spatial autocorrelation (SAR) in ensemble**
✅ **Links gentrification indicators to health trajectory shifts (new mechanism)**
✅ **Actionable early warning system (not just academic prediction)**
✅ **Rigorous temporal validation (no data leakage)**
✅ **Addresses health equity (identifies tipping point communities before decline)**
✅ **Open-source implementation (reproducibility)**

### Expected Impact

**Academic Contributions**:
- Methodological: Demonstrates how to do valid temporal prediction with small-area health data
- Substantive: Tests gentrification → health decline hypothesis with prospective data
- Policy: Provides tool for proactive intervention targeting

**Practical Applications**:
- Local health departments can identify at-risk communities 12+ months in advance
- Enables early intervention (vs reactive response after decline has occurred)
- Supports health equity initiatives by highlighting overlooked communities

**Target Audience**:
- Public health researchers and practitioners
- Urban planners and policy makers
- Health equity advocates
- Machine learning + health informatics community

---

## Contact and Next Steps

**Recommended Next Steps**:
1. Review and refine this design document
2. Begin Phase 1 (data preparation) immediately
3. Set up project structure and Git repository
4. Schedule weekly check-ins to track progress
5. Identify collaborators (statistician, epidemiologist, health department partner)

**Questions to Resolve**:
- Which prediction horizon (12 vs 24 months) to prioritize?
- Should we include county-level policy variables (Medicaid expansion, etc.)?
- Do we have access to computational resources for deep learning (LSTM, GNN)?
- Can we partner with a local health department for real-world validation?

---

**Document Version**: 1.0
**Date**: December 30, 2025
**Author**: Claude (Anthropic) - Data Scientist Agent
**Project**: Community Health Trajectory Prediction System
