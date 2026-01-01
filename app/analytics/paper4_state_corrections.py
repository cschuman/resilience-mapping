#!/usr/bin/env python3
"""
Paper 4: Multiple Comparison Corrections for State-Level Analysis

PROBLEM: The paper makes 51 state comparisons. Without correction:
- Oregon gap of -0.53 SD looks significant
- Washington gap of -0.42 SD looks significant
But with Bonferroni: threshold = 0.05/51 = 0.00098

This script applies:
1. Bonferroni correction (most conservative)
2. Holm-Bonferroni (step-down, slightly less conservative)
3. FDR (Benjamini-Hochberg, controls false discovery rate)

And reports which state gaps survive each correction.
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import statsmodels.stats.multitest as smm
import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def load_data():
    """Load merged resilience and demographic data."""
    resilience = pd.read_csv(DATA_DIR / "processed" / "model_table_corrected.csv")
    resilience['GEOID'] = resilience['TractFIPS'].astype(str).str.zfill(11)

    acs = pd.read_csv(DATA_DIR / "external" / "acs_demographics_2022.csv")
    acs['GEOID'] = acs['GEOID'].astype(str).str.zfill(11)

    df = resilience.merge(acs, on='GEOID', how='inner')
    df['majority_minority'] = (df['pct_white'] < 50).astype(int)

    return df


def compute_state_gaps(df):
    """Compute resilience gap for each state with t-tests."""

    results = []

    for state in df['StateAbbr'].unique():
        state_df = df[df['StateAbbr'] == state]

        white_maj = state_df[state_df['majority_minority'] == 0]['resilience_score']
        mm = state_df[state_df['majority_minority'] == 1]['resilience_score']

        if len(white_maj) >= 10 and len(mm) >= 10:
            # Compute gap (positive = white advantage)
            gap = white_maj.mean() - mm.mean()

            # T-test
            t_stat, p_value = stats.ttest_ind(white_maj, mm)

            # Effect size (Cohen's d)
            pooled_std = np.sqrt((white_maj.std()**2 + mm.std()**2) / 2)
            cohens_d = gap / pooled_std if pooled_std > 0 else 0

            results.append({
                'state': state,
                'gap_sd': gap,
                'cohens_d': cohens_d,
                'n_white_maj': len(white_maj),
                'n_mm': len(mm),
                'n_total': len(white_maj) + len(mm),
                'white_maj_mean': white_maj.mean(),
                'mm_mean': mm.mean(),
                't_stat': t_stat,
                'p_value': p_value
            })

    return pd.DataFrame(results)


def apply_corrections(df):
    """Apply multiple comparison corrections."""

    n_tests = len(df)
    p_values = df['p_value'].values

    # Bonferroni
    bonferroni_threshold = 0.05 / n_tests
    df['bonferroni_sig'] = df['p_value'] < bonferroni_threshold

    # Holm-Bonferroni (step-down procedure)
    holm_reject, holm_pvals, _, _ = smm.multipletests(p_values, method='holm')
    df['holm_sig'] = holm_reject

    # FDR (Benjamini-Hochberg)
    fdr_reject, fdr_pvals, _, _ = smm.multipletests(p_values, method='fdr_bh')
    df['fdr_sig'] = fdr_reject

    return df, bonferroni_threshold


def main():
    print("=" * 70)
    print("PAPER 4: Multiple Comparison Corrections for State Analysis")
    print("=" * 70)

    # Load data
    df = load_data()
    print(f"\nLoaded {len(df):,} tracts from {df['StateAbbr'].nunique()} states")

    # Compute state gaps
    print("\nComputing state-level resilience gaps...")
    state_gaps = compute_state_gaps(df)
    state_gaps = state_gaps.sort_values('gap_sd', ascending=False)

    # Apply corrections
    state_gaps, bonf_threshold = apply_corrections(state_gaps)

    print(f"\nTotal state comparisons: {len(state_gaps)}")
    print(f"Bonferroni threshold: α = 0.05 / {len(state_gaps)} = {bonf_threshold:.6f}")

    # Summary of what survives
    print("\n" + "-" * 70)
    print("CORRECTION SUMMARY: How many state gaps remain significant?")
    print("-" * 70)

    print(f"\n                     Uncorrected    Bonferroni    Holm    FDR")
    print("-" * 70)
    n_uncorrected = (state_gaps['p_value'] < 0.05).sum()
    n_bonferroni = state_gaps['bonferroni_sig'].sum()
    n_holm = state_gaps['holm_sig'].sum()
    n_fdr = state_gaps['fdr_sig'].sum()

    print(f"Significant gaps:      {n_uncorrected:>3}            {n_bonferroni:>3}         {n_holm:>3}     {n_fdr:>3}")

    # States with LARGEST gaps
    print("\n" + "-" * 70)
    print("STATES WITH LARGEST GAPS (Favoring White-Majority)")
    print("-" * 70)

    top_gaps = state_gaps.head(10)
    print(f"\n{'State':<8} {'Gap (SD)':<10} {'p-value':<12} {'Bonf':<6} {'FDR':<6}")
    print("-" * 50)
    for _, row in top_gaps.iterrows():
        bonf = "✓" if row['bonferroni_sig'] else "✗"
        fdr = "✓" if row['fdr_sig'] else "✗"
        print(f"{row['state']:<8} {row['gap_sd']:>+8.3f}   {row['p_value']:<12.2e} {bonf:<6} {fdr:<6}")

    # States with REVERSED gaps (minority advantage)
    print("\n" + "-" * 70)
    print("STATES WITH REVERSED GAPS (Favoring Majority-Minority)")
    print("-" * 70)

    reversed_gaps = state_gaps[state_gaps['gap_sd'] < 0].sort_values('gap_sd')
    print(f"\n{'State':<8} {'Gap (SD)':<10} {'p-value':<12} {'Bonf':<6} {'FDR':<6}")
    print("-" * 50)
    for _, row in reversed_gaps.iterrows():
        bonf = "✓" if row['bonferroni_sig'] else "✗"
        fdr = "✓" if row['fdr_sig'] else "✗"
        print(f"{row['state']:<8} {row['gap_sd']:>+8.3f}   {row['p_value']:<12.2e} {bonf:<6} {fdr:<6}")

    # Specific check: Oregon and Washington
    print("\n" + "-" * 70)
    print("CRITICAL CHECK: Do Oregon and Washington survive correction?")
    print("-" * 70)

    for state in ['OR', 'WA', 'CA', 'NV']:
        row = state_gaps[state_gaps['state'] == state]
        if len(row) > 0:
            row = row.iloc[0]
            print(f"\n{state}: Gap = {row['gap_sd']:+.3f} SD")
            print(f"  p-value = {row['p_value']:.4e}")
            print(f"  Survives Bonferroni? {'YES' if row['bonferroni_sig'] else 'NO'}")
            print(f"  Survives FDR?        {'YES' if row['fdr_sig'] else 'NO'}")
            print(f"  N tracts: {row['n_total']:,} ({row['n_white_maj']:,} white-maj, {row['n_mm']:,} mm)")

    # Paper implications
    print("\n" + "-" * 70)
    print("PAPER IMPLICATIONS")
    print("-" * 70)

    # Check if any reversed states survive correction
    reversed_sig = reversed_gaps[reversed_gaps['bonferroni_sig']]

    if len(reversed_sig) == 0:
        print("""
⚠ NO reversed-gap states survive Bonferroni correction.

The Paper 4 claim that Oregon and Washington show "reversed patterns"
where minority-majority communities outperform white-majority communities
does NOT survive multiple comparison correction.

REQUIRED REVISION:
- Cannot claim these states "prove" structural factors drive disparities
- Should note these patterns are not statistically robust
- Should use FDR-corrected results or remove state-level claims entirely
""")
    else:
        print(f"\n✓ {len(reversed_sig)} reversed-gap states survive Bonferroni:")
        for _, row in reversed_sig.iterrows():
            print(f"  {row['state']}: gap = {row['gap_sd']:+.3f} SD, p = {row['p_value']:.2e}")

    # Large gaps that survive
    large_gaps_sig = state_gaps[(state_gaps['gap_sd'] > 1.0) & state_gaps['bonferroni_sig']]
    print(f"\n✓ {len(large_gaps_sig)} states with gaps > 1.0 SD survive correction:")
    for _, row in large_gaps_sig.iterrows():
        print(f"  {row['state']}: gap = {row['gap_sd']:+.3f} SD, p = {row['p_value']:.2e}")

    print("\n" + "=" * 70)

    return state_gaps


if __name__ == "__main__":
    results = main()
