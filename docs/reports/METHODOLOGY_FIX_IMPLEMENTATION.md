# Methodology Fix Implementation Guide

**Technical Specification for Addressing Peer Review Criticisms**
**Version 1.0 | December 30, 2025**

---

## Quick Reference: Key Thresholds

| Parameter | Value | Source |
|-----------|-------|--------|
| Minimum population | 500 persons | Census Bureau guidance + practical |
| CI width suppression | > 0.30 | NCHS Data Presentation Standards |
| RSE suppression | > 30% | NCHS/CDC standard |
| Resilience score cap | ±3.5 SD | Statistical convention |
| Spatial autocorrelation threshold | Moran's I p < 0.05 | Standard practice |
| External validation target | r > 0.3 with mortality | SVI benchmark |

---

## 1. Population Threshold Implementation

### Download Population Data

```python
# Required: Census tract population from ACS 2020 5-year
# Variable: B01001_001E (Total population)

import pandas as pd

# Load our current model table
model = pd.read_csv('data/input/model_table_with_residuals.csv')

# Load population data (must download from Census API or data.census.gov)
# Example structure:
# pop = pd.read_csv('data/raw/acs_population_2020.csv')
# pop columns: GEOID, total_population, adult_population

# Merge
model_with_pop = model.merge(pop, left_on='TractFIPS', right_on='GEOID')
```

### Apply Exclusion Criteria

```python
# Exclusion tiers
MINIMUM_POPULATION = 500

# Create exclusion flags
model_with_pop['exclude_low_pop'] = model_with_pop['total_population'] < MINIMUM_POPULATION
model_with_pop['flag_uncertain'] = (
    (model_with_pop['total_population'] >= MINIMUM_POPULATION) &
    (model_with_pop['total_population'] < 1200)
)

# Count exclusions
n_excluded_pop = model_with_pop['exclude_low_pop'].sum()
print(f"Excluded for low population (<{MINIMUM_POPULATION}): {n_excluded_pop:,} tracts")
print(f"Flagged for uncertainty (500-1200): {model_with_pop['flag_uncertain'].sum():,} tracts")

# Apply exclusion
model_valid = model_with_pop[~model_with_pop['exclude_low_pop']].copy()
```

### Expected Impact

- Estimated 2-4% of tracts excluded (1,300-2,600 tracts)
- Zero-population tracts: 100% excluded
- Low-population institutional areas: Mostly excluded

---

## 2. Confidence Interval Integration

### Download PLACES Data with CIs

```python
# CDC PLACES 2024 Census Tract Data includes:
# - Data_Value: Point estimate
# - Low_Confidence_Limit: 2.5th percentile
# - High_Confidence_Limit: 97.5th percentile

# Download from: https://data.cdc.gov/500-Cities-Places/PLACES-Local-Data-for-Better-Health-Census-Tract-D/cwsq-ngmh

places = pd.read_csv('data/raw/places_2024/places_tract_2024.csv')

# Filter to our 5 burden components
burden_measures = ['OBESITY', 'DIABETES', 'CHD', 'BPHIGH', 'LPA']
places_burden = places[places['MeasureId'].isin(burden_measures)].copy()

# Pivot to wide format with CIs
places_wide = places_burden.pivot_table(
    index='LocationID',
    columns='MeasureId',
    values=['Data_Value', 'Low_Confidence_Limit', 'High_Confidence_Limit'],
    aggfunc='first'
).reset_index()

# Flatten column names
places_wide.columns = ['_'.join(col).strip('_') for col in places_wide.columns]
```

### Compute CI-Based Exclusions

```python
# Calculate CI width for each measure
for measure in burden_measures:
    places_wide[f'CI_width_{measure}'] = (
        places_wide[f'High_Confidence_Limit_{measure}'] -
        places_wide[f'Low_Confidence_Limit_{measure}']
    )

# NCHS standard: exclude if ANY component has CI width > 0.30 (30 percentage points)
CI_WIDTH_THRESHOLD = 30.0  # percentage points

places_wide['exclude_wide_ci'] = False
for measure in burden_measures:
    places_wide['exclude_wide_ci'] |= places_wide[f'CI_width_{measure}'] > CI_WIDTH_THRESHOLD

n_excluded_ci = places_wide['exclude_wide_ci'].sum()
print(f"Excluded for wide CI (>{CI_WIDTH_THRESHOLD}pp): {n_excluded_ci:,} tracts")
```

### Propagate Uncertainty to Burden Index

```python
import numpy as np

# Approximate SE from CI (assuming normal distribution)
# SE = (CI_high - CI_low) / 3.92  (for 95% CI)

for measure in burden_measures:
    places_wide[f'SE_{measure}'] = places_wide[f'CI_width_{measure}'] / 3.92

# Z-score each measure
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

for measure in burden_measures:
    mean_val = places_wide[f'Data_Value_{measure}'].mean()
    std_val = places_wide[f'Data_Value_{measure}'].std()

    # Z-score the point estimate
    places_wide[f'z_{measure}'] = (places_wide[f'Data_Value_{measure}'] - mean_val) / std_val

    # Scale the SE to z-score units
    places_wide[f'z_SE_{measure}'] = places_wide[f'SE_{measure}'] / std_val

# Composite burden = mean of z-scores
z_cols = [f'z_{m}' for m in burden_measures]
places_wide['burden'] = places_wide[z_cols].mean(axis=1)

# Propagated SE for composite (assuming independence)
se_cols = [f'z_SE_{m}' for m in burden_measures]
places_wide['burden_SE'] = np.sqrt((places_wide[se_cols]**2).sum(axis=1)) / len(burden_measures)

# 95% CI for burden
places_wide['burden_CI_low'] = places_wide['burden'] - 1.96 * places_wide['burden_SE']
places_wide['burden_CI_high'] = places_wide['burden'] + 1.96 * places_wide['burden_SE']
```

### Propagate to Resilience Score

```python
# After running regression to get residuals:
# resilience = -residual / residual_std

# SE of resilience (approximation, ignoring regression uncertainty)
places_wide['resilience_SE'] = places_wide['burden_SE'] / residual_std

# 95% CI for resilience
places_wide['resilience_CI_low'] = places_wide['resilience_score'] - 1.96 * places_wide['resilience_SE']
places_wide['resilience_CI_high'] = places_wide['resilience_score'] + 1.96 * places_wide['resilience_SE']

# Flag tracts where CI includes zero (not significantly different from expected)
places_wide['resilience_significant'] = (
    (places_wide['resilience_CI_low'] > 0) |  # Significantly resilient
    (places_wide['resilience_CI_high'] < 0)   # Significantly vulnerable
)
```

---

## 3. Winsorization of Extreme Values

```python
# Cap resilience scores at ±3.5 SD
RESILIENCE_CAP = 3.5

model_valid['resilience_winsorized'] = np.clip(
    model_valid['resilience_score'],
    -RESILIENCE_CAP,
    RESILIENCE_CAP
)

# Document impact
n_capped_high = (model_valid['resilience_score'] > RESILIENCE_CAP).sum()
n_capped_low = (model_valid['resilience_score'] < -RESILIENCE_CAP).sum()

print(f"Capped at +{RESILIENCE_CAP}: {n_capped_high:,} tracts")
print(f"Capped at -{RESILIENCE_CAP}: {n_capped_low:,} tracts")

# Use winsorized scores for all downstream analysis
```

---

## 4. Spatial Autocorrelation Testing

### Compute Global Moran's I

```python
import geopandas as gpd
from pysal.lib import weights
from esda.moran import Moran

# Load tract shapefile
tracts = gpd.read_file('data/raw/census_tracts_2020/tl_2020_us_tract.shp')

# Merge with model results
tracts_with_scores = tracts.merge(
    model_valid[['TractFIPS', 'resilience_winsorized']],
    left_on='GEOID',
    right_on='TractFIPS'
)

# Create spatial weights (queen contiguity)
w = weights.Queen.from_dataframe(tracts_with_scores)
w.transform = 'r'  # Row standardize

# Compute Moran's I
moran = Moran(tracts_with_scores['resilience_winsorized'], w)

print(f"Global Moran's I: {moran.I:.4f}")
print(f"Expected I: {moran.EI:.4f}")
print(f"p-value (permutation): {moran.p_sim:.4f}")

if moran.p_sim < 0.05:
    print("WARNING: Significant spatial autocorrelation detected")
    print("Must apply spatial regression methods")
else:
    print("No significant spatial autocorrelation")
```

### If Significant: Spatial Error Model

```python
from pysal.model import spreg

# Spatial error model
model_spatial = spreg.ML_Error(
    y=model_valid['burden'].values.reshape(-1, 1),
    x=X_features.values,  # Design matrix from original regression
    w=w,
    name_y='burden',
    name_x=feature_names
)

print(model_spatial.summary)

# Compare coefficients
print("\nCoefficient comparison:")
print("Variable | OLS | Spatial | % Change")
for i, name in enumerate(feature_names):
    ols_coef = ols_coefficients[i]
    spatial_coef = model_spatial.betas[i]
    pct_change = (spatial_coef - ols_coef) / abs(ols_coef) * 100
    print(f"{name} | {ols_coef:.4f} | {spatial_coef[0]:.4f} | {pct_change[0]:.1f}%")
```

---

## 5. External Validation

### Obtain Mortality Data

```bash
# CDC WONDER: Underlying Cause of Death
# Request census tract-level mortality rates (may require special access)
# Alternative: County-level mortality, aggregate tracts to county

# Variables needed:
# - All-cause mortality rate (age-adjusted)
# - Specific cause mortality (heart disease, diabetes, etc.)
```

### Validation Analysis

```python
# Load external outcome data
mortality = pd.read_csv('data/raw/cdc_wonder_mortality.csv')

# Merge with our resilience scores
validation = model_valid.merge(mortality, on='TractFIPS')

# Test 1: Correlation
from scipy import stats

r, p = stats.pearsonr(validation['resilience_winsorized'], validation['mortality_rate'])
print(f"Resilience-Mortality correlation: r = {r:.3f}, p = {p:.4f}")

# Expect: Negative correlation (higher resilience = lower mortality)
if r < 0 and p < 0.05:
    print("VALIDATION PASSED: Resilience negatively associated with mortality")
else:
    print("VALIDATION FAILED: No significant protective association")

# Test 2: Regression controlling for SES
import statsmodels.api as sm

X_val = validation[['resilience_winsorized', 'median_income', 'pct_poverty', 'pct_uninsured']]
X_val = sm.add_constant(X_val)
y_val = validation['mortality_rate']

val_model = sm.OLS(y_val, X_val).fit()
print(val_model.summary())

# Key result: Is resilience coefficient significant after controlling for SES?
resilience_pvalue = val_model.pvalues['resilience_winsorized']
resilience_coef = val_model.params['resilience_winsorized']

if resilience_pvalue < 0.05 and resilience_coef < 0:
    print("VALIDATION PASSED: Resilience independently predicts lower mortality")
else:
    print("VALIDATION FAILED: Resilience does not independently predict mortality")
```

### Compare to SVI Performance

```python
# Load CDC Social Vulnerability Index
svi = pd.read_csv('data/raw/svi_2020.csv')

# Merge
comparison = validation.merge(svi[['FIPS', 'RPL_THEMES']], left_on='TractFIPS', right_on='FIPS')

# Compare predictive validity
from sklearn.metrics import r2_score

# Our resilience
resilience_r2 = r2_score(
    comparison['mortality_rate'],
    comparison['resilience_winsorized'] * -1  # Flip sign for comparison
)

# SVI (higher = more vulnerable = higher mortality)
svi_r2 = r2_score(
    comparison['mortality_rate'],
    comparison['RPL_THEMES']
)

print(f"Resilience R² with mortality: {resilience_r2:.4f}")
print(f"SVI R² with mortality: {svi_r2:.4f}")

if resilience_r2 > svi_r2:
    print("Our index outperforms SVI for mortality prediction")
elif resilience_r2 > 0.1:
    print("Our index has meaningful predictive validity")
else:
    print("WARNING: Poor predictive validity - construct may be invalid")
```

---

## 6. Construct Independence Check

### Compute Orthogonal Resilience

```python
# Goal: Create resilience measure with r < 0.30 with burden

# Step 1: Identify external protective factors
# These should NOT be used in burden calculation
protective_factors = [
    'social_associations',      # From County Health Rankings
    'pct_with_insurance',       # ACS
    'physicians_per_capita',    # AHRF
    'food_program_participation', # SNAP/WIC data
    'community_org_density',    # IRS 990 data
]

# Step 2: Regress residuals on protective factors
# This isolates "explained protective factors" from "unexplained variance"

protective_data = pd.read_csv('data/raw/protective_factors.csv')
residuals_with_protective = model_valid.merge(protective_data, on='TractFIPS')

X_protective = residuals_with_protective[protective_factors]
X_protective = sm.add_constant(X_protective)
y_resid = residuals_with_protective['resid']

protective_model = sm.OLS(y_resid, X_protective).fit()

# Orthogonal resilience = predicted from protective factors
residuals_with_protective['resilience_orthogonal'] = -protective_model.fittedvalues / protective_model.resid.std()

# Unexplained residual = what's left
residuals_with_protective['unexplained_resid'] = protective_model.resid

# Step 3: Check construct independence
r_orthogonal, _ = stats.pearsonr(
    residuals_with_protective['resilience_orthogonal'],
    residuals_with_protective['burden']
)

print(f"Orthogonal resilience - Burden correlation: r = {r_orthogonal:.3f}")

if abs(r_orthogonal) < 0.30:
    print("CONSTRUCT INDEPENDENCE ACHIEVED")
else:
    print("WARNING: Still substantial overlap with burden")
```

---

## 7. Revised Output Tables

### New Top 20 Resilient Tracts (Valid Data Only)

```python
# Apply all exclusions
valid_tracts = model_with_pop[
    ~model_with_pop['exclude_low_pop'] &
    ~model_with_pop['exclude_wide_ci'] &
    model_with_pop['resilience_significant']  # CI excludes zero
].copy()

# Get top 20 by winsorized resilience
top_20_valid = valid_tracts.nlargest(20, 'resilience_winsorized')

# Report with uncertainty
print("TOP 20 RESILIENT TRACTS (VALIDATED)")
print("=" * 80)
for _, row in top_20_valid.iterrows():
    print(f"Tract: {row['TractFIPS']} | State: {row['StateAbbr']}")
    print(f"  Resilience: {row['resilience_winsorized']:.2f} (95% CI: {row['resilience_CI_low']:.2f} to {row['resilience_CI_high']:.2f})")
    print(f"  Population: {row['total_population']:,}")
    print(f"  Burden SE: {row['burden_SE']:.3f}")
    print()

# Save
top_20_valid.to_csv('data/output/tables/top_20_resilient_VALIDATED.csv', index=False)
```

### Summary Statistics with Exclusions

```python
print("ANALYSIS SAMPLE SUMMARY")
print("=" * 60)
print(f"Original tracts: {len(model):,}")
print(f"Excluded (low population): {n_excluded_pop:,}")
print(f"Excluded (wide CI): {n_excluded_ci:,}")
print(f"Final valid sample: {len(valid_tracts):,}")
print()
print(f"Resilience score range (winsorized): [{valid_tracts['resilience_winsorized'].min():.2f}, {valid_tracts['resilience_winsorized'].max():.2f}]")
print(f"Significantly resilient (CI > 0): {(valid_tracts['resilience_CI_low'] > 0).sum():,}")
print(f"Significantly vulnerable (CI < 0): {(valid_tracts['resilience_CI_high'] < 0).sum():,}")
```

---

## 8. Documentation Requirements

Every output file must include:

```python
# Header metadata for all output files
metadata = {
    'analysis_date': '2025-12-30',
    'methodology_version': '2.0',
    'population_threshold': 500,
    'ci_width_threshold': 30.0,
    'resilience_cap': 3.5,
    'n_original': len(model),
    'n_excluded_population': n_excluded_pop,
    'n_excluded_ci': n_excluded_ci,
    'n_final': len(valid_tracts),
    'spatial_morans_i': moran.I,
    'spatial_pvalue': moran.p_sim,
    'external_validation_r': r,
    'external_validation_pvalue': p,
    'caveats': [
        'Residual-based resilience may reflect unmeasured confounders',
        'Cross-sectional data cannot support causal inference',
        'Tract boundaries may not reflect meaningful neighborhoods',
        'PLACES estimates are model-based, not direct measurement'
    ]
}

# Save with every output
import json
with open('data/output/analysis_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
```

---

## Checklist Before Publication

- [ ] Population threshold applied (>=500)
- [ ] CI width exclusions applied (<=30pp)
- [ ] Resilience scores winsorized (±3.5 SD)
- [ ] Uncertainty propagated to all estimates
- [ ] Spatial autocorrelation tested and addressed
- [ ] External validation completed
- [ ] Construct independence documented
- [ ] All output files include metadata
- [ ] Limitations section updated in paper
- [ ] Grade revised from B+ to C- (or better if validation passes)

---

*Implementation guide for methodological fixes. All code is pseudocode requiring adaptation to actual data structures.*
