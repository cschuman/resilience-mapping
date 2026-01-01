#!/usr/bin/env python3
"""
Calculate proper resilience scores for Florida tracts.

The model_table_corrected.csv is missing Florida (0 tracts).
This script:
1. Loads PLACES and FARA data including Florida
2. Calculates burden z-scores
3. Runs OLS model with state fixed effects
4. Calculates resilience = -residual / std(residuals)
5. Creates combined model table with all states including Florida
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

def load_places_burden():
    """Load PLACES data and calculate burden z-scores."""
    print("Loading PLACES data...")

    # Use harmonized 2022 data which has Florida
    places = pd.read_csv(DATA_DIR / "interim" / "places_harmonized_2022.csv")
    print(f"  Total tracts: {len(places):,}")

    # Get column names
    cols = places.columns.tolist()
    print(f"  Columns: {cols[:10]}...")

    # The file has TractFIPS, Year, State, County, Pop, then health measures
    # Based on the structure, identify burden components
    places['TractFIPS'] = places.iloc[:, 0].astype(str).str.zfill(11)
    places['StateAbbr'] = places.iloc[:, 2]

    # The burden measures should be: OBESITY, DIABETES, CHD, BPHIGH, LPA
    # Need to identify which columns these are
    # Let's check the raw data structure
    print(f"  Sample row: {places.iloc[0].tolist()[:15]}")

    return places


def load_fara():
    """Load FARA food access data."""
    print("\nLoading FARA data...")

    fara = pd.read_csv(DATA_DIR / "input" / "fara_2019.csv")
    fara['GEOID'] = fara['CensusTract'].astype(str).str.zfill(11)

    print(f"  Total tracts: {len(fara):,}")
    print(f"  Florida tracts: {len(fara[fara['State'] == 'Florida']):,}")

    return fara


def load_existing_model_table():
    """Load existing model table to understand the structure."""
    print("\nLoading existing model table...")

    model = pd.read_csv(DATA_DIR / "processed" / "model_table_corrected.csv")
    print(f"  Existing tracts: {len(model):,}")
    print(f"  States: {model['StateAbbr'].nunique()}")
    print(f"  Columns: {model.columns.tolist()}")
    print(f"  Sample: \n{model.head(2)}")

    return model


def load_prediction_dataset():
    """Load prediction dataset which has burden data for all states including FL."""
    print("\nLoading prediction dataset (has Florida)...")

    pred = pd.read_csv(DATA_DIR / "processed" / "prediction_dataset_rich.csv")
    pred['GEOID'] = pred['TractFIPS'].astype(str).str.zfill(11)

    print(f"  Total tracts: {len(pred):,}")
    print(f"  Florida tracts: {len(pred[pred['StateAbbr'] == 'FL']):,}")
    print(f"  Burden column: CHBI_prev (mean: {pred['CHBI_prev'].mean():.2f})")

    return pred


def calculate_resilience_with_florida():
    """
    Calculate proper resilience scores for all states including Florida.

    Uses OLS regression: burden ~ LILA + LI + rural + state_FE
    Resilience = -residual / std(residuals)
    """
    # Load data
    pred = load_prediction_dataset()
    fara = load_fara()
    existing = load_existing_model_table()

    # Use the prediction dataset's burden (CHBI_prev) as our burden measure
    # This is already z-scored
    burden_df = pred[['GEOID', 'TractFIPS', 'StateAbbr', 'CHBI_prev', 'CHBI_zscore_prev']].copy()
    burden_df = burden_df.rename(columns={'CHBI_prev': 'burden_raw', 'CHBI_zscore_prev': 'burden'})

    # Merge with FARA for control variables
    fara_subset = fara[['GEOID', 'LILATracts_1And10', 'LowIncomeTracts', 'Urban', 'GroupQuartersFlag']].copy()
    fara_subset = fara_subset.rename(columns={'LowIncomeTracts': 'LI'})

    merged = burden_df.merge(fara_subset, on='GEOID', how='inner')
    merged['rural'] = 1 - merged['Urban'].fillna(0)
    merged['LILATracts_1And10'] = pd.to_numeric(merged['LILATracts_1And10'], errors='coerce').fillna(0)
    merged['LI'] = pd.to_numeric(merged['LI'], errors='coerce').fillna(0)

    # Filter institutional tracts
    merged = merged[merged['GroupQuartersFlag'] != 1].copy()

    print(f"\n  Merged dataset: {len(merged):,} tracts")
    print(f"  Florida: {len(merged[merged['StateAbbr'] == 'FL']):,} tracts")

    # Reset index to ensure alignment
    merged = merged.reset_index(drop=True)

    # Create state dummies
    states = sorted(merged['StateAbbr'].unique())
    print(f"  States in model: {len(states)}")

    # Build design matrix
    n = len(merged)
    X = pd.DataFrame({
        'intercept': np.ones(n),
        'LILA': merged['LILATracts_1And10'].values,
        'LI': merged['LI'].values,
        'rural': merged['rural'].values
    })

    # State fixed effects (drop first as reference)
    for state in states[1:]:
        X[f'state_{state}'] = (merged['StateAbbr'] == state).astype(float).values

    y = merged['burden'].values

    # Debug: check for NaN
    print(f"  y NaN count: {np.isnan(y).sum()}")
    print(f"  X shape: {X.shape}")
    print(f"  X NaN per column: {X.isnull().sum().sum()}")

    # Remove rows with NaN in y only (X should be clean)
    valid_mask = ~np.isnan(y)
    X_valid = X.loc[valid_mask].reset_index(drop=True)
    y_valid = y[valid_mask]
    merged_valid = merged.loc[valid_mask].reset_index(drop=True)

    print(f"  Valid observations: {len(y_valid):,}")

    # Fit OLS
    print("\nFitting OLS model...")
    model = sm.OLS(y_valid, X_valid)
    results = model.fit()

    print(f"  R-squared: {results.rsquared:.4f}")
    print(f"  Adjusted R-squared: {results.rsquared_adj:.4f}")

    # Calculate residuals and resilience scores
    residuals = y_valid - results.fittedvalues
    residual_std = np.std(residuals)
    resilience_scores = -residuals / residual_std

    print(f"  Residual std: {residual_std:.4f}")
    print(f"  Resilience score range: [{resilience_scores.min():.2f}, {resilience_scores.max():.2f}]")

    # Create output dataframe
    output = pd.DataFrame({
        'TractFIPS': merged_valid['TractFIPS'].values,
        'StateAbbr': merged_valid['StateAbbr'].values,
        'GEOID': merged_valid['GEOID'].values,
        'burden': y_valid,
        'resid': residuals,
        'resilience_score': resilience_scores
    })

    # Summary by state
    print("\n" + "=" * 60)
    print("RESILIENCE BY STATE (including Florida)")
    print("=" * 60)

    state_summary = output.groupby('StateAbbr').agg({
        'resilience_score': ['mean', 'std', 'count'],
        'burden': 'mean'
    }).round(3)
    state_summary.columns = ['mean_resil', 'std_resil', 'n_tracts', 'mean_burden']
    state_summary = state_summary.sort_values('mean_resil', ascending=False)

    print(state_summary.head(20))

    # Florida specifically
    fl = output[output['StateAbbr'] == 'FL']
    print(f"\n Florida Summary:")
    print(f"  N tracts: {len(fl):,}")
    print(f"  Mean resilience: {fl['resilience_score'].mean():.3f}")
    print(f"  Std resilience: {fl['resilience_score'].std():.3f}")
    print(f"  Mean burden: {fl['burden'].mean():.3f}")

    # Compare to existing model table (for validation)
    print("\n" + "=" * 60)
    print("VALIDATION: Compare to existing model_table_corrected.csv")
    print("=" * 60)

    # Ensure GEOID is string in both
    existing['GEOID'] = existing['GEOID'].astype(str).str.zfill(11)
    output['GEOID'] = output['GEOID'].astype(str).str.zfill(11)

    # Merge on GEOID and compare resilience scores
    comparison = existing.merge(
        output[['GEOID', 'resilience_score']],
        on='GEOID',
        how='inner',
        suffixes=('_old', '_new')
    )

    corr = np.corrcoef(comparison['resilience_score_old'], comparison['resilience_score_new'])[0, 1]
    print(f"  Correlation between old and new scores: r = {corr:.4f}")
    print(f"  Mean difference: {(comparison['resilience_score_new'] - comparison['resilience_score_old']).mean():.4f}")

    # Save combined model table
    output_path = DATA_DIR / "processed" / "model_table_with_florida.csv"
    output.to_csv(output_path, index=False)
    print(f"\n Saved: {output_path}")
    print(f"  Total tracts: {len(output):,}")

    return output, results


def main():
    print("=" * 60)
    print("CALCULATING PROPER RESILIENCE SCORES FOR FLORIDA")
    print("=" * 60)

    output, results = calculate_resilience_with_florida()

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)

    return output


if __name__ == "__main__":
    output = main()
