# Community Health Trajectory Prediction System

## Quick Start Guide

This guide walks you through implementing the novel Community Health Trajectory Prediction system designed to identify census tracts that will experience health burden DECLINE or IMPROVEMENT 12-24 months in advance.

---

## Prerequisites

### Required Data

You need to download the following datasets:

#### 1. CDC PLACES Data (2020-2025)

**Download from**: https://data.cdc.gov/browse?category=500+Cities+%26+Places

For each year (2020-2025), download the census tract-level file:
- File: "PLACES: Local Data for Better Health, Census Tract Data [YEAR] release"
- Format: CSV
- Save as: `/data/raw/places_tract_2020.csv`, `/data/raw/places_tract_2021.csv`, etc.

**Key columns**:
- `TractFIPS` or `LocationID`: 11-digit census tract FIPS code
- `MeasureId`: Health outcome identifier (OBESITY, DIABETES, CHD, etc.)
- `Data_Value`: Prevalence estimate (%)
- `Low_Confidence_Limit`, `High_Confidence_Limit`: 95% confidence interval
- `Year`: Data year
- `StateAbbr`, `CountyName`: Geographic identifiers

**What you get**: 40 health measures per tract per year (obesity, diabetes, mental health, etc.)

#### 2. Census American Community Survey (ACS) 5-Year Estimates

**Download from**: https://data.census.gov/ or https://www.nhgis.org/

**Variables needed** (Table IDs from ACS):

| Variable | Table | Description |
|----------|-------|-------------|
| Total Population | B01003 | Tract population |
| Median Household Income | B19013 | Income in past 12 months |
| Poverty Status | B17001 | Persons below poverty level |
| Educational Attainment | B15003 | Bachelor's degree or higher |
| Median Gross Rent | B25064 | Housing cost |
| Median Home Value | B25077 | Owner-occupied housing value |
| Race/Ethnicity | B03002 | Hispanic/Latino and race |
| Moved in Last Year | B07003 | Residential mobility |
| Means of Transportation | B08301 | Vehicle availability |

**Years needed**: 2015-2023 (to cover PLACES 2020-2025 with historical trends)

**Save as**: `/data/raw/acs_2019_tract.csv`, `/data/raw/acs_2021_tract.csv`, etc.

**Format requirements**:
- One row per census tract
- Column `GEOID`: 11-digit FIPS code
- Prefix column names with table ID (e.g., `B19013_001E` for median income estimate)

#### 3. Census Tract Boundary Shapefiles (Optional - for spatial analysis)

**Download from**: https://www.census.gov/cgi-bin/geo/shapefiles/index.php

- Product: "TIGER/Line Shapefiles"
- Layer: "Census Tracts"
- Year: 2020 (or 2010 for backwards compatibility)

**Save to**: `/data/raw/census_tracts_2020/`

### Software Requirements

**Python 3.9+** with the following packages:

```bash
# Core data science
pip install pandas>=2.0 numpy>=1.24 scipy>=1.10

# Geospatial (for spatial features)
pip install geopandas>=0.13 libpysal>=4.7 esda>=2.5 shapely>=2.0

# Machine learning
pip install scikit-learn>=1.3 xgboost>=2.0 lightgbm>=4.0

# Deep learning (for LSTM model)
pip install torch>=2.0 pytorch-lightning>=2.0

# Model interpretation
pip install shap>=0.42

# Visualization
pip install matplotlib>=3.7 seaborn>=0.12 plotly>=5.14

# Utilities
pip install pyarrow>=12.0 tqdm pyyaml

# Optional: Graph neural networks
pip install torch-geometric>=2.3
```

Or use the requirements file:

```bash
cd /Users/corey/Projects/resilience-mapping-go/app/analytics/trajectory_prediction
pip install -r requirements.txt
```

---

## Implementation Steps

### Step 1: Prepare Data (Phase 1)

**Goal**: Load and merge CDC PLACES, Census ACS, and geometries into analysis-ready format.

```bash
cd /Users/corey/Projects/resilience-mapping-go/app/analytics/trajectory_prediction
python data_preparation.py
```

**What it does**:
1. Loads PLACES data for all available years (2020-2025)
2. Creates Composite Health Burden Index (CHBI) from multiple health outcomes
3. Loads Census ACS data with social determinant variables
4. Merges everything by census tract and year
5. Saves to `/data/processed/trajectory_analysis_ready.parquet`

**Expected output**:
```
Loading PLACES data for years: [2020, 2021, 2022, 2023, 2024, 2025]
  Loaded 2,550,000 records for 2023
Creating Composite Health Burden Index (CHBI)
  CHBI calculated for 340,000 tract-years
Merging CHBI, ACS, and geometry data
Final dataset: 340,000 rows, 85 columns
Saved to /data/processed/trajectory_analysis_ready.parquet
```

**Troubleshooting**:
- If PLACES files not found: Check file names match pattern `places_tract_2023.csv`
- If ACS files not found: You'll get warnings but pipeline will continue (spatial features will be missing)
- If memory issues: Process years one at a time and concatenate

### Step 2: Engineer Features (Phase 2)

**Goal**: Create temporal trends, spatial features, and trajectory labels.

```bash
python feature_engineering.py
```

**What it does**:
1. **Temporal features**: Trend slopes, acceleration, volatility, momentum
2. **SDOH change features**: Income mobility, gentrification risk, poverty trends
3. **Spatial features**: Spatial lag, Local Moran's I, clustering (requires geometries)
4. **Interaction features**: Displacement risk, contagion risk, etc.
5. **Target labels**: Classifies each tract-year as DECLINE, STABLE, or IMPROVE
6. Saves to `/data/processed/features_and_targets.parquet`

**Expected output**:
```
PHASE 2: FEATURE ENGINEERING
Calculating temporal features for CHBI_zscore
  Added 6 temporal features
Calculating SDOH change features
  Added SDOH change features
Creating interaction features
  Added interaction features
Creating trajectory labels with 1-year horizon

Trajectory label distribution:
  DECLINE: 45,234 (15.2%)
  STABLE: 201,456 (67.8%)
  IMPROVE: 50,678 (17.0%)

Total features created: 58
Saved to /data/processed/features_and_targets.parquet
```

**Key parameters to adjust**:
- `horizon_years=1`: How far ahead to predict (1=12 months, 2=24 months)
- `decline_threshold=0.5`: Z-score change defining DECLINE (higher = stricter definition)
- `include_spatial=True`: Whether to calculate spatial features (requires geometries)

### Step 3: Explore Trajectories (Phase 3)

**Goal**: Understand patterns in declining/improving communities.

```bash
python exploratory_analysis.py
```

**What it does**:
1. Descriptive statistics of trajectory distribution
2. Maps of declining/improving tracts
3. Time series plots of high-risk communities
4. Feature correlation analysis
5. Generates publication-quality figures

**Outputs**:
- `/figures/trajectory/trajectory_distribution_by_state.png`
- `/figures/trajectory/declining_tracts_map.html` (interactive)
- `/figures/trajectory/feature_correlations.png`
- `/docs/research/eda_trajectory_patterns.md` (summary report)

### Step 4: Train Models (Phase 4)

**Goal**: Train and evaluate trajectory prediction models.

```bash
python train_trajectory_models.py
```

**What it does**:
1. Sets up temporal cross-validation (no data leakage)
2. Trains baseline models (persistence, linear regression)
3. Trains Tier 1 models:
   - XGBoost (gradient boosting)
   - LSTM (sequence model)
   - Random Forest (ensemble)
   - Spatial Autoregressive (if geometries available)
4. Trains stacked ensemble meta-learner
5. Evaluates on all CV splits

**Expected output**:
```
PHASE 4: MODEL TRAINING

Temporal CV Splits:
  Split 1: Train 2020-2021 → Validate 2022 (n_train=136,340, n_val=68,170)
  Split 2: Train 2020-2022 → Validate 2023 (n_train=204,510, n_val=68,170)
  Split 3: Train 2020-2023 → Validate 2024 (n_train=272,680, n_val=68,170)

Training XGBoost...
  Split 1: F1=0.687, Balanced Accuracy=0.712, AUC=0.809
  Split 2: F1=0.695, Balanced Accuracy=0.718, AUC=0.816
  Split 3: F1=0.701, Balanced Accuracy=0.724, AUC=0.821
  Mean: F1=0.694 ± 0.007

Training LSTM...
  Split 1: F1=0.672, Balanced Accuracy=0.698, AUC=0.795
  ...

Training Ensemble (Stacking)...
  Split 1: F1=0.715, Balanced Accuracy=0.738, AUC=0.831
  Split 2: F1=0.723, Balanced Accuracy=0.745, AUC=0.838
  Split 3: F1=0.729, Balanced Accuracy=0.751, AUC=0.843
  Mean: F1=0.722 ± 0.007

Best model: Ensemble (F1=0.722, +5.1% vs best single model)

Saved models to /models/trajectory_prediction/
Saved results to /results/cv_performance.csv
```

**Hyperparameter tuning** (if time allows):
```bash
python train_trajectory_models.py --tune-hyperparameters --n-trials=50
```

This uses Optuna for Bayesian optimization of hyperparameters.

### Step 5: Interpret Models (Phase 5)

**Goal**: Understand what drives trajectory predictions.

```bash
python interpret_models.py
```

**What it does**:
1. SHAP value analysis (global feature importance)
2. Partial dependence plots for key features
3. Local explanations for example tracts
4. Case studies of correct vs incorrect predictions

**Outputs**:
- `/figures/trajectory/shap_summary.png`: Top 20 most important features
- `/figures/trajectory/shap_dependence_*.png`: How features affect predictions
- `/figures/trajectory/case_study_*.png`: Example tract trajectories
- `/docs/research/model_interpretation.md`: Narrative report

**Example findings**:
```
Top 10 Most Important Features for Predicting DECLINE:

1. trend_slope (slope of CHBI over time)
2. spatial_lag_CHBI (average CHBI of neighbors)
3. gentrification_risk (rapid neighborhood change)
4. poverty_velocity (accelerating poverty)
5. income_trajectory (declining income)
6. volatility (unstable health trends)
7. churn_rate (residential instability)
8. percentile_rank (current health position)
9. displacement_risk (gentrification × poverty)
10. local_morans_I (spatial clustering)

Key Insights:
- Tracts already on negative trajectory (high trend_slope) have 3.2x odds of DECLINE
- Gentrification increases DECLINE risk by 1.8x in low-income areas
- Spatial spillovers are significant: neighboring decline increases risk by 2.1x
```

### Step 6: Validate and Robustness (Phase 6)

**Goal**: Ensure model generalizes and is robust.

```bash
python validate_trajectories.py
```

**What it does**:
1. Spatial cross-validation (leave-one-state-out)
2. Subgroup analysis (urban vs rural, by region, by baseline health)
3. Sensitivity analysis (feature subsets, hyperparameters)
4. Uncertainty quantification (prediction confidence intervals)
5. External validation (if 2026 data becomes available)

**Outputs**:
- `/results/robustness_checks.md`: Summary of all analyses
- `/results/spatial_cv_performance.csv`: State-level performance
- `/results/subgroup_analysis.csv`: Performance by tract characteristics

### Step 7: Deploy (Phase 7)

**Goal**: Create interactive web application for early warning system.

**Backend API** (`/app/web/src/routes/api/trajectory/predict/+server.ts`):
```typescript
import type { RequestHandler } from './$types';
import { loadModel, predictTrajectory } from '$lib/server/trajectory';

export const POST: RequestHandler = async ({ request }) => {
    const { tract_fips, features } = await request.json();

    // Load trained ensemble model
    const model = await loadModel('ensemble_final.pkl');

    // Generate prediction
    const prediction = await predictTrajectory(model, features);

    return json({
        tract_fips,
        trajectory: prediction.label,  // DECLINE, STABLE, IMPROVE
        probabilities: prediction.probs,  // [P(decline), P(stable), P(improve)]
        risk_score: prediction.probs[0],  // P(decline)
        confidence: prediction.confidence,
        feature_importance: prediction.shap_values,
        explanation: prediction.narrative
    });
};
```

**Frontend Dashboard** (`/app/web/src/routes/trajectory/+page.svelte`):
```svelte
<script>
    import TrajectoryMap from './TrajectoryMap.svelte';
    import RiskScore from './RiskScore.svelte';
    import FeatureExplanation from './FeatureExplanation.svelte';

    let selectedTract = null;
    let predictions = [];
</script>

<div class="dashboard">
    <h1>Community Health Trajectory Predictor</h1>
    <p>Early warning system identifying census tracts at risk of health decline</p>

    <!-- Interactive map -->
    <TrajectoryMap
        {predictions}
        on:selectTract={(e) => selectedTract = e.detail}
    />

    {#if selectedTract}
        <!-- Risk score card -->
        <RiskScore tract={selectedTract} />

        <!-- Feature explanations (SHAP waterfall) -->
        <FeatureExplanation tract={selectedTract} />
    {/if}
</div>
```

**Deploy to production**:
```bash
cd /Users/corey/Projects/resilience-mapping-go/app/web
npm run build
fly deploy
```

Access at: `https://resilience-mapping.fly.dev/trajectory`

---

## Understanding the Output

### Model Performance Metrics

**Balanced Accuracy**:
- Overall accuracy accounting for class imbalance
- Target: >0.70 (vs 0.33 for random guessing with 3 classes)
- Interpretation: 0.72 = model correctly classifies 72% of tracts on average

**F1-Score (Macro)**:
- Harmonic mean of precision and recall, averaged across classes
- Target: >0.65
- Interpretation: 0.72 = good balance of precision (avoiding false alarms) and recall (catching true declines)

**AUC-ROC (One-vs-Rest)**:
- Discrimination ability for each class vs others
- Target: >0.80 for DECLINE class (priority)
- Interpretation: 0.83 = 83% chance model ranks a random declining tract higher than a random non-declining tract

**Cohen's Kappa**:
- Agreement beyond chance
- Target: >0.60 (substantial agreement)
- Interpretation: 0.68 = 68% of predictions are better than random

### Feature Importance (SHAP Values)

**How to read SHAP plots**:

1. **Summary Plot**: Shows global importance
   - Features ranked top to bottom by importance
   - Each point is a tract (color = feature value)
   - Horizontal position = impact on prediction
   - Red dots pushing right = high feature value increases DECLINE risk
   - Blue dots pushing left = low feature value decreases DECLINE risk

2. **Dependence Plot**: Shows feature effect
   - X-axis: Feature value
   - Y-axis: SHAP value (impact on prediction)
   - Slope shows relationship (positive = increases risk, negative = decreases)
   - Color shows interaction with another feature

**Example interpretation**:
```
Feature: trend_slope
SHAP value: +0.15 (for a tract with trend_slope = 0.8)

Interpretation:
- This tract has a positive CHBI trend (health burden increasing)
- This increases its predicted probability of DECLINE by 15 percentage points
- If we could reduce trend_slope to 0, probability of DECLINE would drop 15%
```

### Trajectory Labels

**DECLINE**: Health burden increasing by >0.5 SD over next 12 months
- These tracts need proactive intervention
- Target for outreach, resource allocation, program expansion

**STABLE**: Health burden changing by <0.5 SD
- Monitor but no urgent action needed
- May benefit from prevention programs

**IMPROVE**: Health burden decreasing by >0.5 SD
- Study these for protective factors
- Potential case studies for replication

---

## Customization and Extensions

### Adjusting Prediction Horizon

To predict 24 months ahead instead of 12:

```python
# In feature_engineering.py
df = create_trajectory_labels(df, horizon_years=2)
```

### Adding Custom Features

Edit `feature_engineering.py`:

```python
def calculate_custom_features(df):
    """Add your domain-specific features"""

    # Example: Hospital closure events
    df['hospital_closed_recently'] = (
        df['hospitals_count'] < df.groupby('LocationID')['hospitals_count'].shift(1)
    ).astype(int)

    # Example: Policy intervention
    df['medicaid_expanded'] = df['State'].isin([
        'CA', 'NY', 'MA', ...  # States that expanded Medicaid
    ]).astype(int)

    return df
```

### Changing Class Thresholds

To make DECLINE definition stricter (fewer false alarms):

```python
# In config.py
TRAJECTORY_THRESHOLDS = {
    'decline_threshold': 0.75,  # Was 0.5, now requires larger change
    'improve_threshold': -0.75,
}
```

### Outcome-Specific Models

To predict specific outcomes (e.g., just diabetes):

```python
# In feature_engineering.py
df = calculate_temporal_features(df, target_col='DIABETES')
df = create_trajectory_labels(df, target_col='DIABETES', horizon_years=1)
```

---

## Troubleshooting

### Common Errors

**1. "No PLACES data files found"**
- Check files are in `/data/raw/` directory
- Verify file names match pattern `places_tract_YYYY.csv`
- Ensure files have correct columns (MeasureId, Data_Value, LocationID)

**2. "Insufficient training years for validation"**
- You need at least `min_train_years` (default=2) before first validation year
- If you only have 2020-2022 data, can only validate on 2022
- Wait for more annual PLACES releases or reduce `min_train_years=1`

**3. "SHAP calculation failed"**
- Large datasets (>100k samples) can cause memory issues
- Use `shap.Explainer(..., approximate=True)` for speed
- Or sample 10% of data: `df_sample = df.sample(frac=0.1)`

**4. "Model performance is poor (F1 < 0.55)"**
- Check class balance (need enough DECLINE/IMPROVE examples)
- Verify features have variance (not all NaN or constant)
- Try simpler trajectory definition (lower thresholds)
- Ensure temporal CV is working (no data leakage)

**5. "Spatial features all NaN"**
- Requires geometry column (census tract boundaries)
- Download shapefiles or skip spatial features for now
- Set `include_spatial=False` in feature engineering

### Performance Optimization

**Speed up training**:
```python
# Use fewer trees
XGBOOST_PARAMS['n_estimators'] = 200  # Was 500

# Use histogram-based splitting
XGBOOST_PARAMS['tree_method'] = 'hist'

# Sample data for hyperparameter tuning
df_sample = df.sample(frac=0.2, random_state=42)
```

**Reduce memory usage**:
```python
# Use sparse matrices for one-hot encoded features
from scipy.sparse import csr_matrix

# Convert to float32 instead of float64
df = df.astype({col: 'float32' for col in feature_cols})

# Save as parquet (more efficient than CSV)
df.to_parquet('features.parquet', compression='snappy')
```

---

## Next Steps

### Short-Term (1-2 weeks)

1. **Get the data**: Download CDC PLACES and Census ACS
2. **Run Phase 1-2**: Data preparation and feature engineering
3. **Exploratory analysis**: Understand trajectory patterns
4. **Train baseline models**: Establish performance benchmarks

### Medium-Term (1-2 months)

1. **Optimize models**: Hyperparameter tuning, feature selection
2. **Write paper**: Draft methods and results sections
3. **Create visualizations**: Publication-quality figures
4. **Validation**: Robustness checks, sensitivity analysis

### Long-Term (3-6 months)

1. **Deploy application**: Interactive web dashboard
2. **Partner with health departments**: Real-world validation
3. **Submit manuscript**: Target journals (AJPH, Health & Place)
4. **Disseminate findings**: Conferences, policy briefs

---

## Citation

If you use this system in your research:

```bibtex
@software{trajectory_prediction_2025,
  title = {Community Health Trajectory Prediction System:
           An Early Warning System for Census Tract Health Decline},
  author = {[Your Name]},
  year = {2025},
  url = {https://github.com/yourusername/resilience-mapping},
  note = {Predicts 12-24 month ahead changes in community health
          using CDC PLACES data and machine learning}
}
```

---

## Support

**Questions or issues?**
- Open an issue: https://github.com/yourusername/resilience-mapping/issues
- Email: your.email@example.com
- Documentation: See `/docs/research/trajectory-prediction-design.md` for detailed methodology

**Contributing**:
- Fork the repository
- Create a feature branch
- Submit a pull request with description of changes

---

**Last Updated**: December 30, 2025
**Version**: 0.1.0
**Status**: Implementation Ready
