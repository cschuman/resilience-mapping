#!/usr/bin/env python3
"""
Run Corrected Analysis Pipeline

This script runs the corrected resilience model and generates comparison reports.
Uses actual data file locations from the project.
"""

import pandas as pd
import numpy as np
import os
import sys

# Add analytics directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from resilience_model import (
    filter_institutional_populations,
    prepare_design_matrix,
    fit_ols_model,
    calculate_resilience_scores,
    OLSResult
)

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_INPUT = os.path.join(PROJECT_ROOT, 'data', 'input')
DATA_PROCESSED = os.path.join(PROJECT_ROOT, 'data', 'processed')
DATA_OUTPUT = os.path.join(PROJECT_ROOT, 'data', 'output')

# Ensure output directories exist
os.makedirs(DATA_PROCESSED, exist_ok=True)
os.makedirs(os.path.join(DATA_OUTPUT, 'figures'), exist_ok=True)


def load_data():
    """Load the source data files."""
    print("=" * 60)
    print("LOADING DATA")
    print("=" * 60)

    # Load burden table (pre-calculated health burden by tract)
    burden_path = os.path.join(DATA_INPUT, 'burden_table.csv')
    burden = pd.read_csv(burden_path)
    print(f"Burden data: {len(burden):,} tracts")

    # Load FARA data
    fara_path = os.path.join(DATA_INPUT, 'fara_2019.csv')
    fara = pd.read_csv(fara_path, low_memory=False)
    print(f"FARA data: {len(fara):,} tracts")

    # Load original model results (buggy)
    old_path = os.path.join(DATA_INPUT, 'model_table_with_residuals.csv')
    old_results = pd.read_csv(old_path)
    print(f"Original results: {len(old_results):,} tracts")

    return burden, fara, old_results


def run_corrected_model(burden, fara):
    """Run the corrected OLS model with state fixed effects."""
    print("\n" + "=" * 60)
    print("RUNNING CORRECTED MODEL")
    print("=" * 60)

    # Prepare data
    # FARA uses CensusTract, burden uses TractFIPS
    fara = fara.copy()
    burden = burden.copy()

    # Standardize tract IDs
    fara['GEOID'] = fara['CensusTract'].astype(str).str.zfill(11)
    burden['TractFIPS'] = burden['TractFIPS'].astype(str).str.zfill(11)

    # Check LILA column
    if 'LILATracts_1And10' in fara.columns:
        fara['LILATracts_1And10'] = pd.to_numeric(fara['LILATracts_1And10'], errors='coerce').fillna(0)
        lila_count = fara['LILATracts_1And10'].sum()
        print(f"LILA tracts (1 and 10): {int(lila_count):,}")

    # Check LI (low income) column
    if 'LowIncomeTracts' in fara.columns:
        fara['LI'] = pd.to_numeric(fara['LowIncomeTracts'], errors='coerce').fillna(0)
    elif 'LI' not in fara.columns:
        print("WARNING: No LowIncomeTracts column, creating from PovertyRate")
        fara['PovertyRate'] = pd.to_numeric(fara['PovertyRate'], errors='coerce').fillna(0)
        fara['LI'] = (fara['PovertyRate'] >= 20).astype(float)

    # Filter institutional populations
    print("\n--- Institutional Population Filter ---")
    if 'PCTGQTRS' in fara.columns:
        # Use percentage column
        fara['PCTGQTRS'] = pd.to_numeric(fara['PCTGQTRS'], errors='coerce').fillna(0)
        threshold = 10.0  # 10%
        excluded = fara[fara['PCTGQTRS'] > threshold].copy()
        fara_filtered = fara[fara['PCTGQTRS'] <= threshold].copy()
        print(f"Threshold: {threshold}% group quarters")
        print(f"Excluded tracts: {len(excluded):,}")
        print(f"Remaining tracts: {len(fara_filtered):,}")

        # Save excluded tracts
        excluded_path = os.path.join(DATA_PROCESSED, 'excluded_institutional_tracts.csv')
        excluded[['CensusTract', 'State', 'County', 'PCTGQTRS', 'GroupQuartersFlag']].to_csv(
            excluded_path, index=False
        )
        print(f"Saved: {excluded_path}")
    elif 'GroupQuartersFlag' in fara.columns:
        # Use binary flag
        fara['GroupQuartersFlag'] = pd.to_numeric(fara['GroupQuartersFlag'], errors='coerce').fillna(0)
        excluded = fara[fara['GroupQuartersFlag'] == 1].copy()
        fara_filtered = fara[fara['GroupQuartersFlag'] != 1].copy()
        print(f"Using GroupQuartersFlag filter")
        print(f"Excluded tracts: {len(excluded):,}")
        print(f"Remaining tracts: {len(fara_filtered):,}")
    else:
        print("WARNING: No group quarters column found, skipping filter")
        fara_filtered = fara
        excluded = pd.DataFrame()

    # Build design matrix directly (bypassing the reusable function due to data issues)
    print("\n--- Building Design Matrix ---")

    # Merge datasets
    merged = burden.merge(fara_filtered, left_on='TractFIPS', right_on='GEOID', how='inner')
    print(f"Merged tracts: {len(merged):,}")

    # Get sorted list of states
    state_list = sorted(merged['StateAbbr'].unique())
    print(f"States: {len(state_list)} (reference: {state_list[0]})")

    # Build feature matrix
    n_rows = len(merged)

    # Convert features to numeric
    merged['LILATracts_1And10'] = pd.to_numeric(merged['LILATracts_1And10'], errors='coerce').fillna(0)
    merged['LI'] = pd.to_numeric(merged['LowIncomeTracts'], errors='coerce').fillna(0)
    merged['Urban'] = pd.to_numeric(merged['Urban'], errors='coerce').fillna(0)
    merged['rural'] = 1 - merged['Urban']

    # Build X DataFrame
    X_features = pd.DataFrame({
        'intercept': np.ones(n_rows),
        'LILATracts_1And10': merged['LILATracts_1And10'].values,
        'LI': merged['LI'].values,
        'rural': merged['rural'].values
    })

    # Add state fixed effects (drop first for reference)
    for state in state_list[1:]:
        X_features[f'state_{state}'] = (merged['StateAbbr'] == state).astype(float).values

    # Response variable
    y = merged['burden'].values

    # Metadata for output
    tract_ids = merged['TractFIPS'].values
    state_abbrs = merged['StateAbbr'].values
    geoids = merged['GEOID'].values

    print(f"Features: {len(X_features.columns)}")

    # Check for any issues
    print(f"NaN in X: {X_features.isna().sum().sum()}")
    print(f"NaN in y: {np.isnan(y).sum()}")

    # Fit model
    print("\n--- Fitting OLS Model ---")
    import statsmodels.api as sm

    model = sm.OLS(y, X_features)
    results = model.fit()

    # Calculate residuals and resilience scores
    residuals = y - results.fittedvalues
    residual_std = np.std(residuals)
    resilience_scores = -residuals / (residual_std + 1e-9)

    # Build output table
    model_table = pd.DataFrame({
        'TractFIPS': tract_ids,
        'StateAbbr': state_abbrs,
        'GEOID': geoids,
        'burden': y,
        'resid': residuals,
        'resilience_score': resilience_scores
    })

    # Print results
    print(f"\n--- Model Results ---")
    print(f"R-squared: {results.rsquared:.4f}")
    print(f"Adjusted R-squared: {results.rsquared_adj:.4f}")
    print(f"N observations: {len(y):,}")
    print(f"N states: {len(state_list)}")
    print(f"Residual std: {residual_std:.4f}")

    # Print key coefficients
    print(f"\nKey Coefficients:")
    coef_names = ['intercept', 'LILATracts_1And10', 'LI', 'rural']
    for name in coef_names:
        if name in X_features.columns:
            idx = list(X_features.columns).index(name)
            coef = results.params[idx]
            se = results.bse[idx]
            pval = results.pvalues[idx]
            sig = '***' if pval < 0.001 else '**' if pval < 0.01 else '*' if pval < 0.05 else ''
            print(f"  {name}: {coef:.4f} (SE: {se:.4f}) {sig}")

    # Classification summary
    resilient = (model_table['resilience_score'] > 1.645).sum()
    vulnerable = (model_table['resilience_score'] < -1.645).sum()
    expected = len(model_table) - resilient - vulnerable

    print(f"\n--- Classification Summary ---")
    print(f"Resilient (score > 1.645): {resilient:,} tracts ({resilient/len(model_table)*100:.1f}%)")
    print(f"Vulnerable (score < -1.645): {vulnerable:,} tracts ({vulnerable/len(model_table)*100:.1f}%)")
    print(f"Expected: {expected:,} tracts ({expected/len(model_table)*100:.1f}%)")

    # Save corrected results
    output_path = os.path.join(DATA_PROCESSED, 'model_table_corrected.csv')
    model_table.to_csv(output_path, index=False)
    print(f"\nSaved: {output_path}")

    return model_table, results, excluded


def compare_results(old_results, new_results):
    """Compare old (buggy) vs new (corrected) results."""
    print("\n" + "=" * 60)
    print("COMPARING OLD VS NEW RESULTS")
    print("=" * 60)

    # Standardize tract IDs
    old = old_results.copy()
    new = new_results.copy()
    old['TractFIPS'] = old['TractFIPS'].astype(str).str.zfill(11)
    new['TractFIPS'] = new['TractFIPS'].astype(str).str.zfill(11)

    # Merge
    merged = old[['TractFIPS', 'StateAbbr', 'burden', 'resilience_score']].merge(
        new[['TractFIPS', 'resilience_score']],
        on='TractFIPS',
        how='inner',
        suffixes=('_old', '_new')
    )

    print(f"\nMatched tracts: {len(merged):,}")

    # Calculate changes
    merged['score_change'] = merged['resilience_score_new'] - merged['resilience_score_old']

    # Classification
    def classify(score):
        if score > 1.645:
            return 'resilient'
        elif score < -1.645:
            return 'vulnerable'
        else:
            return 'expected'

    merged['old_class'] = merged['resilience_score_old'].apply(classify)
    merged['new_class'] = merged['resilience_score_new'].apply(classify)
    merged['class_changed'] = merged['old_class'] != merged['new_class']

    # Summary stats
    print(f"\n--- Score Change Statistics ---")
    print(f"Mean change: {merged['score_change'].mean():.4f}")
    print(f"Median change: {merged['score_change'].median():.4f}")
    print(f"Std of change: {merged['score_change'].std():.4f}")
    print(f"Max increase: {merged['score_change'].max():.4f}")
    print(f"Max decrease: {merged['score_change'].min():.4f}")
    print(f"Correlation (old vs new): {merged['resilience_score_old'].corr(merged['resilience_score_new']):.4f}")

    # Classification changes
    n_changed = merged['class_changed'].sum()
    print(f"\n--- Classification Changes ---")
    print(f"Tracts that changed class: {n_changed:,} ({n_changed/len(merged)*100:.1f}%)")

    # Transition matrix
    print(f"\nTransition Matrix:")
    transition = pd.crosstab(merged['old_class'], merged['new_class'], margins=True)
    print(transition)

    # Specific transitions
    became_resilient = ((merged['old_class'] != 'resilient') & (merged['new_class'] == 'resilient')).sum()
    lost_resilient = ((merged['old_class'] == 'resilient') & (merged['new_class'] != 'resilient')).sum()
    became_vulnerable = ((merged['old_class'] != 'vulnerable') & (merged['new_class'] == 'vulnerable')).sum()
    lost_vulnerable = ((merged['old_class'] == 'vulnerable') & (merged['new_class'] != 'vulnerable')).sum()

    print(f"\nKey Transitions:")
    print(f"  Became resilient: {became_resilient:,}")
    print(f"  Lost resilient status: {lost_resilient:,}")
    print(f"  Became vulnerable: {became_vulnerable:,}")
    print(f"  Lost vulnerable status: {lost_vulnerable:,}")

    # Save comparison
    comparison_path = os.path.join(DATA_PROCESSED, 'score_comparison.csv')
    merged.to_csv(comparison_path, index=False)
    print(f"\nSaved: {comparison_path}")

    # Top changes
    print(f"\n--- Top 10 Score INCREASES ---")
    top_increases = merged.nlargest(10, 'score_change')
    print(top_increases[['TractFIPS', 'StateAbbr', 'resilience_score_old', 'resilience_score_new', 'score_change']].to_string())

    print(f"\n--- Top 10 Score DECREASES ---")
    top_decreases = merged.nsmallest(10, 'score_change')
    print(top_decreases[['TractFIPS', 'StateAbbr', 'resilience_score_old', 'resilience_score_new', 'score_change']].to_string())

    # State-level analysis
    print(f"\n--- State-Level Mean Score Changes (Top 10) ---")
    state_changes = merged.groupby('StateAbbr').agg({
        'score_change': ['mean', 'std'],
        'class_changed': 'sum',
        'TractFIPS': 'count'
    })
    state_changes.columns = ['mean_change', 'std_change', 'n_changed', 'n_tracts']
    state_changes = state_changes.sort_values('mean_change', ascending=False)
    print(state_changes.head(10))

    state_path = os.path.join(DATA_PROCESSED, 'state_change_analysis.csv')
    state_changes.to_csv(state_path)
    print(f"\nSaved: {state_path}")

    return merged


def identify_top_resilient(new_results, fara):
    """Identify top resilient tracts for manual validation."""
    print("\n" + "=" * 60)
    print("TOP RESILIENT TRACTS FOR VALIDATION")
    print("=" * 60)

    # Get top 100 resilient
    top_100 = new_results.nlargest(100, 'resilience_score').copy()

    # Add FARA context
    fara_slim = fara[['CensusTract', 'State', 'County', 'Urban', 'Pop2010',
                       'LILATracts_1And10', 'PCTGQTRS', 'PovertyRate']].copy()
    fara_slim['CensusTract'] = fara_slim['CensusTract'].astype(str).str.zfill(11)

    top_100 = top_100.merge(fara_slim, left_on='TractFIPS', right_on='CensusTract', how='left')

    # Summary
    print(f"\nTop 100 Resilient Tracts Summary:")
    print(f"  Mean resilience score: {top_100['resilience_score'].mean():.3f}")
    print(f"  Min score in top 100: {top_100['resilience_score'].min():.3f}")
    print(f"  States represented: {top_100['StateAbbr'].nunique()}")

    # Urban vs Rural
    if 'Urban' in top_100.columns:
        top_100['Urban'] = pd.to_numeric(top_100['Urban'], errors='coerce').fillna(0)
        urban_pct = top_100['Urban'].mean() * 100
        print(f"  Urban tracts: {urban_pct:.1f}%")

    # Top 20 for manual validation
    print(f"\n--- TOP 20 FOR MANUAL VALIDATION ---")
    top_20 = top_100.head(20)

    display_cols = ['TractFIPS', 'StateAbbr', 'County', 'resilience_score', 'burden', 'Pop2010', 'PCTGQTRS']
    available_cols = [c for c in display_cols if c in top_20.columns]
    print(top_20[available_cols].to_string())

    # Save for validation
    top_100_path = os.path.join(DATA_PROCESSED, 'top_100_resilient_corrected.csv')
    top_100.to_csv(top_100_path, index=False)
    print(f"\nSaved: {top_100_path}")

    return top_100


def main():
    """Run the complete analysis pipeline."""
    print("=" * 60)
    print("CORRECTED RESILIENCE ANALYSIS PIPELINE")
    print("State Fixed Effects Bug Fix - December 24, 2025")
    print("=" * 60)

    # Load data
    burden, fara, old_results = load_data()

    # Run corrected model
    new_results, model, excluded = run_corrected_model(burden, fara)

    # Compare old vs new
    comparison = compare_results(old_results, new_results)

    # Identify top resilient for validation
    top_resilient = identify_top_resilient(new_results, fara)

    # Summary
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)

    print("\nFiles generated:")
    print(f"  - {DATA_PROCESSED}/model_table_corrected.csv")
    print(f"  - {DATA_PROCESSED}/excluded_institutional_tracts.csv")
    print(f"  - {DATA_PROCESSED}/score_comparison.csv")
    print(f"  - {DATA_PROCESSED}/state_change_analysis.csv")
    print(f"  - {DATA_PROCESSED}/top_100_resilient_corrected.csv")

    return new_results, comparison, top_resilient


if __name__ == "__main__":
    new_results, comparison, top_resilient = main()
