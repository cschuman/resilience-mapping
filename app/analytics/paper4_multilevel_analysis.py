#!/usr/bin/env python3
"""
Paper 4 Multilevel Analysis: Properly account for tract-within-state clustering

PROBLEM: The original t-test (t=40.02) ignored clustering - tracts within states
are not independent. Actual ICC ~0.002 yields design effect ~2.9 and effective N ~18,760.

SOLUTION: Use mixed effects models with state random intercepts to:
1. Account for clustering
2. Get proper standard errors
3. Report corrected test statistics and confidence intervals
4. Calculate design effect and effective N

This addresses the biostatistician's concern about inflated test statistics.
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.formula.api as smf
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def load_data():
    """Load merged tract-level data with resilience scores and demographics."""

    print("Loading data...")

    # Load resilience scores from model_table_corrected.csv
    resilience = pd.read_csv(DATA_DIR / "processed" / "model_table_corrected.csv")
    resilience['GEOID'] = resilience['TractFIPS'].astype(str).str.zfill(11)

    # Load ACS demographics
    acs = pd.read_csv(DATA_DIR / "external" / "acs_demographics_2022.csv")
    acs['GEOID'] = acs['GEOID'].astype(str).str.zfill(11)

    # Merge
    df = resilience.merge(acs, on='GEOID', how='inner')

    print(f"  Resilience tracts: {len(resilience):,}")
    print(f"  ACS tracts: {len(acs):,}")
    print(f"  Merged: {len(df):,}")

    # Extract state FIPS from GEOID
    df['state_fips'] = df['GEOID'].str[:2]

    # Create majority classification
    df['majority_minority'] = (df['pct_white'] < 50).astype(int)

    return df


def compute_icc(df, outcome_col='resilience_score', group_col='state_fips'):
    """Compute Intraclass Correlation Coefficient (ICC) for clustering."""

    # Fit null model with random intercept
    null_model = smf.mixedlm(
        f"{outcome_col} ~ 1",
        data=df.dropna(subset=[outcome_col, group_col]),
        groups=group_col
    ).fit(method='powell')

    # ICC = variance_between / (variance_between + variance_within)
    var_between = float(null_model.cov_re.iloc[0, 0])
    var_within = null_model.scale

    icc = var_between / (var_between + var_within)

    return icc, var_between, var_within


def compute_design_effect(icc, avg_cluster_size):
    """Compute design effect due to clustering."""
    # DEFF = 1 + (m - 1) * ICC where m = average cluster size
    deff = 1 + (avg_cluster_size - 1) * icc
    return deff


def run_multilevel_model(df, outcome_col='resilience_score'):
    """Run multilevel model with proper clustering adjustment."""

    # Prepare data
    analysis_df = df.dropna(subset=[outcome_col, 'majority_minority', 'state_fips']).copy()

    print(f"\nFitting mixed effects model with {len(analysis_df):,} tracts in {analysis_df['state_fips'].nunique()} states...")

    # Fixed effect: majority_minority
    # Random effect: state intercept
    model = smf.mixedlm(
        f"{outcome_col} ~ majority_minority",
        data=analysis_df,
        groups='state_fips'
    ).fit(method='powell')

    return model, analysis_df


def naive_comparison(df, outcome_col='resilience_score'):
    """Run naive t-test for comparison (the problematic approach)."""

    analysis_df = df.dropna(subset=[outcome_col, 'majority_minority']).copy()

    group0 = analysis_df[analysis_df['majority_minority'] == 0][outcome_col]
    group1 = analysis_df[analysis_df['majority_minority'] == 1][outcome_col]

    t_stat, p_val = stats.ttest_ind(group0, group1)

    return {
        'white_mean': group0.mean(),
        'white_sd': group0.std(),
        'white_n': len(group0),
        'minority_mean': group1.mean(),
        'minority_sd': group1.std(),
        'minority_n': len(group1),
        't_statistic': t_stat,
        'p_value': p_val
    }


def main():
    print("=" * 70)
    print("PAPER 4: Multilevel Analysis with Proper Clustering Adjustment")
    print("=" * 70)

    # Load data
    df = load_data()
    print(f"\nLoaded {len(df):,} tracts")

    # Verify we have resilience_score column
    if 'resilience_score' not in df.columns:
        raise ValueError("resilience_score column not found in data")

    # Compute ICC
    print("\n" + "-" * 70)
    print("INTRACLASS CORRELATION (ICC)")
    print("-" * 70)

    icc, var_between, var_within = compute_icc(df)
    avg_cluster_size = len(df) / df['state_fips'].nunique()
    deff = compute_design_effect(icc, avg_cluster_size)
    n_eff = len(df) / deff

    print(f"\nVariance components:")
    print(f"  Between-state variance: {var_between:.4f}")
    print(f"  Within-state variance:  {var_within:.4f}")
    print(f"  ICC (rho):              {icc:.4f}")
    print(f"\nClustering adjustment:")
    print(f"  Average tracts/state:   {avg_cluster_size:.0f}")
    print(f"  Design effect (DEFF):   {deff:.1f}")
    print(f"  Nominal N:              {len(df):,}")
    print(f"  Effective N:            {n_eff:.0f}")

    # Naive analysis (problematic)
    print("\n" + "-" * 70)
    print("NAIVE ANALYSIS (IGNORING CLUSTERING) - THE PROBLEMATIC APPROACH")
    print("-" * 70)

    naive = naive_comparison(df)
    print(f"\nMajority-White:    Mean = {naive['white_mean']:.3f}, SD = {naive['white_sd']:.3f}, N = {naive['white_n']:,}")
    print(f"Majority-Minority: Mean = {naive['minority_mean']:.3f}, SD = {naive['minority_sd']:.3f}, N = {naive['minority_n']:,}")
    print(f"\nNaive t-test:      t = {naive['t_statistic']:.2f}, p = {naive['p_value']:.2e}")
    print("\n⚠ This t-statistic is INFLATED due to ignoring state clustering!")

    # Corrected analysis (multilevel)
    print("\n" + "-" * 70)
    print("MULTILEVEL ANALYSIS (ACCOUNTING FOR CLUSTERING) - CORRECT APPROACH")
    print("-" * 70)

    model, analysis_df = run_multilevel_model(df)

    print("\nFixed Effects:")
    print(model.summary().tables[1])

    # Extract coefficient and SE for majority_minority
    coef = model.fe_params['majority_minority']
    se = model.bse_fe['majority_minority']
    z_stat = coef / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    print(f"\nEffect of majority-minority status:")
    print(f"  Coefficient:   {coef:.3f}")
    print(f"  Std. Error:    {se:.3f}")
    print(f"  z-statistic:   {z_stat:.2f}")
    print(f"  p-value:       {p_value:.4f}")
    print(f"  95% CI:        [{coef - 1.96*se:.3f}, {coef + 1.96*se:.3f}]")

    # Comparison
    print("\n" + "-" * 70)
    print("COMPARISON: NAIVE vs MULTILEVEL")
    print("-" * 70)

    print("\n                         Naive          Multilevel        Ratio")
    print("-" * 70)
    print(f"Test statistic:         {naive['t_statistic']:>8.2f}         {z_stat:>8.2f}        {naive['t_statistic']/z_stat:.1f}x inflation")
    print(f"Standard error:         {abs(naive['white_mean'] - naive['minority_mean'])/naive['t_statistic']:>8.4f}         {se:>8.4f}        {se/(abs(naive['white_mean'] - naive['minority_mean'])/naive['t_statistic']):.1f}x larger")

    # Effect still significant?
    print("\n" + "-" * 70)
    print("CONCLUSION")
    print("-" * 70)

    if p_value < 0.05:
        print(f"\n✓ Effect REMAINS SIGNIFICANT after accounting for clustering")
        print(f"  z = {z_stat:.2f}, p = {p_value:.4f}")
        print(f"\n  The gap between majority-white and majority-minority communities")
        print(f"  is real and not just an artifact of ignoring state clustering.")
    else:
        print(f"\n⚠ Effect LOSES SIGNIFICANCE after accounting for clustering")
        print(f"  z = {z_stat:.2f}, p = {p_value:.4f}")

    print(f"\n  Original t = {naive['t_statistic']:.2f} was inflated ~{naive['t_statistic']/abs(z_stat):.0f}x")
    print(f"  due to treating {len(df):,} tracts as independent")
    print(f"  when effective N ≈ {n_eff:.0f}")

    print("\n" + "=" * 70)

    return {
        'icc': icc,
        'deff': deff,
        'n_eff': n_eff,
        'naive_t': naive['t_statistic'],
        'multilevel_z': z_stat,
        'multilevel_p': p_value,
        'coefficient': coef,
        'se': se
    }


if __name__ == "__main__":
    results = main()
