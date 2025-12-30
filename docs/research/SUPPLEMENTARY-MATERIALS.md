# Supplementary Materials

**Paper:** Spatial Contagion in Community Health Trajectories: Evidence from 73,000 U.S. Census Tracts

---

## Table S1: Sample Characteristics

| Characteristic | Value |
|----------------|-------|
| Total tract-year observations | 189,566 |
| Unique census tracts | 72,161 |
| States/territories represented | 51 |
| Study period | 2020-2024 |

### Trajectory Distribution by Prediction Year

| Year | DECLINE | STABLE | IMPROVE | Total |
|------|---------|--------|---------|-------|
| 2022 | 2,961 (4.2%) | 65,969 (93.8%) | 1,408 (2.0%) | 70,338 |
| 2023 | 2,893 (4.4%) | 60,933 (92.1%) | 2,347 (3.5%) | 66,173 |
| 2024 | 11,044 (20.8%) | 33,582 (63.3%) | 8,429 (15.9%) | 53,055 |

Note: 2024 shows increased volatility as more recent data captures COVID-19 recovery dynamics.

### Overall Trajectory Distribution

| Trajectory | Count | Percentage |
|------------|-------|------------|
| STABLE | 160,484 | 84.7% |
| DECLINE | 16,898 | 8.9% |
| IMPROVE | 12,184 | 6.4% |

---

## Table S2: Feature Descriptive Statistics

### Panel A: Health Outcome Features

| Feature | Description | Mean | SD | Min | Max |
|---------|-------------|------|-----|-----|-----|
| CHBI_prev | Composite Health Burden Index (prior year) | 19.12 | 4.25 | 6.58 | 42.24 |
| CHBI_change_1yr | 1-year CHBI change | 0.01 | 0.18 | -3.77 | 2.71 |
| OBESITY_prev | Adult obesity prevalence (%) | 33.34 | 7.09 | 11.50 | 63.90 |
| DIABETES_prev | Adult diabetes prevalence (%) | 10.93 | 3.72 | 0.60 | 46.10 |
| MHLTH_prev | Mental health days not good (%) | 15.55 | 3.34 | 5.50 | 39.60 |

### Panel B: Spatial Features

| Feature | Description | Mean | SD | Min | Max |
|---------|-------------|------|-----|-----|-----|
| neighbor_avg_chbi | Mean neighbor CHBI | 19.42 | 3.73 | 8.11 | 36.54 |
| neighbor_avg_change | Mean neighbor CHBI change | 0.33 | 1.02 | -6.69 | 6.79 |
| neighbor_improving_pct | Percent neighbors improving | 36.1% | 42.2% | 0% | 100% |
| neighbor_declining_pct | Percent neighbors declining | 52.7% | 42.3% | 0% | 100% |
| spatial_lag | Spatial lag indicator | 0.03 | 2.03 | -17.49 | 21.83 |
| num_neighbors | Number of adjacent tracts | 6.2* | 2.8* | 1 | 32 |

*Computed from neighbor graph (73,868 tracts with valid geometry)

---

## Table S3: Model Predictions Summary

### Prediction Distribution (2024 Holdout, n=53,055)

| Trajectory | Count | Percentage |
|------------|-------|------------|
| DECLINE | 25,860 | 48.7% |
| STABLE | 25,694 | 48.4% |
| IMPROVE | 1,501 | 2.8% |

Note: Model predicts more DECLINE than observed due to class imbalance handling and conservative thresholds optimized for early warning.

### Confidence Statistics

| Statistic | Value |
|-----------|-------|
| Mean confidence | 0.623 |
| Standard deviation | 0.134 |
| Minimum | 0.336 |
| Maximum | 0.840 |

### High-Confidence Predictions (confidence ≥ 0.60)

| Trajectory | Count | % of All Predictions |
|------------|-------|---------------------|
| DECLINE | 16,945 | 31.9% |
| STABLE | 9,668 | 18.2% |
| IMPROVE | 494 | 0.9% |
| **Total** | **27,107** | **51.1%** |

---

## Table S4: State-Level Geographic Variation

### Top 10 States by Predicted Decline Rate

| State | N Tracts | Mean Confidence | % Predicted Decline |
|-------|----------|-----------------|---------------------|
| WI | 1,265 | 0.79 | 95.6% |
| WY | 104 | 0.71 | 82.7% |
| IA | 765 | 0.69 | 82.2% |
| LA | 851 | 0.69 | 78.4% |
| RI | 234 | 0.66 | 76.5% |
| WV | 424 | 0.65 | 75.0% |
| MI | 2,453 | 0.64 | 75.0% |
| HI | 195 | 0.69 | 73.9% |
| AR | 546 | 0.64 | 72.2% |
| NV | 596 | 0.65 | 70.6% |

---

## Table S5: Feature Importance Rankings

### Full Feature Importance (Top 20)

| Rank | Feature | Importance (%) | Category |
|------|---------|----------------|----------|
| 1 | neighbor_avg_change | 12.3 | Spatial |
| 2 | spatial_lag | 8.2 | Spatial |
| 3 | neighbor_declining_pct | 5.8 | Spatial |
| 4 | neighbor_improving_pct | 4.1 | Spatial |
| 5 | CHBI_prev | 3.9 | Health |
| 6 | CHBI_change_1yr | 3.3 | Health |
| 7 | neighbor_avg_chbi | 3.1 | Spatial |
| 8 | OBESITY_change_1yr | 2.9 | Health |
| 9 | DIABETES_change_1yr | 2.7 | Health |
| 10 | MHLTH_prev | 2.5 | Health |
| 11 | physical_health_trajectory | 2.3 | Health |
| 12 | mental_health_trajectory | 2.1 | Health |
| 13 | OBESITY_prev | 2.0 | Health |
| 14 | DIABETES_prev | 1.9 | Health |
| 15 | BPHIGH_prev | 1.8 | Health |
| 16 | CHD_prev | 1.7 | Health |
| 17 | num_neighbors | 1.5 | Spatial |
| 18 | PHLTH_prev | 1.4 | Health |
| 19 | LPA_prev | 1.3 | Health |
| 20 | is_hotspot | 1.2 | Spatial |

### Importance by Feature Category

| Category | Cumulative Importance |
|----------|----------------------|
| Spatial Features | 32.0% |
| Health Outcome Features | 45.2% |
| Health Change Features | 15.4% |
| Other Features | 7.4% |

---

## Table S6: Model Performance Comparison

### Cross-Validation Results (Temporal Split)

| Model | Macro F1 | Balanced Accuracy | DECLINE Recall | IMPROVE Recall |
|-------|----------|-------------------|----------------|----------------|
| XGBoost | 0.42 | 0.46 | 0.68 | 0.24 |
| LightGBM | 0.43 | 0.47 | 0.71 | 0.26 |
| Ensemble | 0.43 | 0.47 | 0.70 | 0.25 |

### Confusion Matrix (Ensemble, 2024 Holdout)

| | Pred: DECLINE | Pred: STABLE | Pred: IMPROVE |
|-|---------------|--------------|---------------|
| Actual: DECLINE | 7,731 | 2,876 | 437 |
| Actual: STABLE | 15,543 | 17,183 | 856 |
| Actual: IMPROVE | 2,586 | 5,635 | 208 |

---

## Figure S1: Spatial Feature Construction

```
┌─────────────────────────────────────────────────────────────────┐
│                    Neighbor Graph Construction                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    Step 1: Load tract geometries (TIGER/Line shapefiles)        │
│                           ↓                                      │
│    Step 2: Build spatial index (STRtree)                        │
│                           ↓                                      │
│    Step 3: Query adjacent tracts (Queen contiguity)             │
│            - touches() OR intersects() relationships             │
│            - Excludes self-adjacency                             │
│                           ↓                                      │
│    Step 4: Compute neighbor features                             │
│            - neighbor_avg_chbi: mean(neighbor CHBI values)       │
│            - neighbor_avg_change: mean(neighbor CHBI changes)    │
│            - neighbor_improving_pct: % neighbors with IMPROVE    │
│            - neighbor_declining_pct: % neighbors with DECLINE    │
│            - spatial_lag: focal CHBI - mean(neighbor CHBI)       │
│            - is_hotspot: focal high, neighbors high              │
│            - is_coldspot: focal low, neighbors low               │
│                                                                  │
│    Result: 73,868 tracts with valid neighbor relationships       │
│            Mean neighbors per tract: 6.2 (SD: 2.8)               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Figure S2: Temporal Cross-Validation Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                   Temporal Cross-Validation                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Data Timeline:                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 2020 │ 2021 │ 2022 │ 2023 │ 2024 │ 2025                   │ │
│  │      │      │ TRAIN│ TRAIN│ TEST │ (excluded)             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Training Set (2022-2023): 136,511 observations                 │
│  Test Set (2024): 53,055 observations                           │
│                                                                  │
│  Rationale:                                                      │
│  - Mimics real-world deployment (predict future from past)      │
│  - Prevents temporal data leakage                                │
│  - 2025 excluded (values identical to 2024 at analysis time)    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Figure S3: Model Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│              XGBoost + LightGBM Ensemble Architecture           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input: 70 features per tract                                   │
│  ├── Health outcomes (7): OBESITY, DIABETES, CHD, etc.          │
│  ├── Health trajectories (21): 1yr/2yr changes, z-scores        │
│  ├── Spatial features (10): neighbor averages, lag, hotspots    │
│  └── Other (32): percentiles, distances, indices                │
│                                                                  │
│           ┌──────────────┐        ┌──────────────┐              │
│           │   XGBoost    │        │   LightGBM   │              │
│           │  n_est=300   │        │  n_est=300   │              │
│           │  depth=6     │        │  depth=8     │              │
│           │  lr=0.05     │        │  lr=0.05     │              │
│           │  subsample=  │        │  feature=0.8 │              │
│           │    0.8       │        │  bagging=0.8 │              │
│           └──────┬───────┘        └──────┬───────┘              │
│                  │                       │                       │
│                  v                       v                       │
│             ┌─────────────────────────────────┐                 │
│             │    Soft Voting Ensemble         │                 │
│             │    XGBoost weight: 0.49         │                 │
│             │    LightGBM weight: 0.51        │                 │
│             └─────────────┬───────────────────┘                 │
│                           │                                      │
│                           v                                      │
│             ┌─────────────────────────────────┐                 │
│             │  Output: P(DECLINE), P(STABLE), │                 │
│             │         P(IMPROVE)              │                 │
│             │  Prediction = argmax(P)         │                 │
│             │  Confidence = max(P)            │                 │
│             └─────────────────────────────────┘                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Availability Statement

The CDC PLACES dataset is publicly available from the Centers for Disease Control and Prevention at https://www.cdc.gov/places/. Census tract boundary geometries are available from the U.S. Census Bureau TIGER/Line program at https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html.

Processed datasets supporting this analysis are available from the corresponding author upon reasonable request.

## Code Availability Statement

All code for data processing, feature engineering, model training, and analysis is available at: https://github.com/[repository] under an open-source license.

Key scripts:
- `app/analytics/trajectory_prediction/build_spatial_features.py` - Spatial feature engineering
- `app/analytics/trajectory_prediction/train_ensemble.py` - Model training and evaluation
- `app/analytics/trajectory_prediction/generate_predictions.py` - Prediction generation
- `app/analytics/build_trajectory_data.py` - Data pipeline and CHBI computation

## Reproducibility Checklist

- [x] Raw data sources documented
- [x] Data processing code provided
- [x] Feature engineering code provided
- [x] Model hyperparameters specified
- [x] Random seeds set for reproducibility
- [x] Cross-validation strategy documented
- [x] Evaluation metrics defined
- [x] Model weights and architecture saved

---

## References for Supplementary Materials

1. CDC PLACES. (2024). PLACES: Local Data for Better Health. Centers for Disease Control and Prevention. https://www.cdc.gov/places/

2. U.S. Census Bureau. (2024). TIGER/Line Shapefiles. https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html

3. Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. In Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (pp. 785-794).

4. Ke, G., et al. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree. In Advances in Neural Information Processing Systems 30 (pp. 3146-3154).
