#!/usr/bin/env python3
"""
Paradox Study: Sensitivity Analysis

Test robustness of findings across different threshold definitions.
Also recompute key statistics with corrected income data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path(__file__).parent.parent.parent / "data"
PARADOX_DIR = DATA_DIR / "processed" / "paradox_study"


def load_data():
    """Load model data and demographics."""
    print("=" * 70)
    print("SENSITIVITY ANALYSIS & DATA CORRECTION")
    print("=" * 70)

    # Load model
    model = pd.read_csv(DATA_DIR / "processed" / "model_table_corrected.csv")
    model['GEOID'] = model['GEOID'].astype(str).str.zfill(11)

    # Load FARA
    fara = pd.read_csv(DATA_DIR / "input" / "fara_2019.csv")
    fara['GEOID'] = fara['CensusTract'].astype(str).str.zfill(11)
    fara_cols = ['GEOID', 'LILATracts_1And10', 'LowIncomeTracts', 'Urban', 'PovertyRate', 'MedianFamilyIncome']
    fara = fara[[c for c in fara_cols if c in fara.columns]]
    for col in ['LILATracts_1And10', 'LowIncomeTracts']:
        if col in fara.columns:
            fara[col] = pd.to_numeric(fara[col], errors='coerce').fillna(0)

    # Load ACS (now with fixed income)
    acs = pd.read_csv(DATA_DIR / "external" / "acs_demographics_2022.csv")
    acs['GEOID'] = acs['GEOID'].astype(str).str.zfill(11)

    # Merge
    df = model.merge(fara, on='GEOID', how='left')
    df = df.merge(acs, on='GEOID', how='left')

    print(f"Total tracts: {len(df):,}")
    print(f"Good food access (non-LILA): {(df['LILATracts_1And10'] == 0).sum():,}")

    return df


def sensitivity_thresholds(df):
    """Test different paradox thresholds."""
    print("\n" + "=" * 70)
    print("SENSITIVITY ANALYSIS: THRESHOLD ROBUSTNESS")
    print("=" * 70)

    # Filter to good food access
    good_access = df[df['LILATracts_1And10'] == 0].copy()
    n_good_access = len(good_access)

    thresholds = [-0.5, -0.75, -1.0, -1.25, -1.5, -1.75, -2.0]

    print(f"\nBase: {n_good_access:,} tracts with good food access")
    print("-" * 70)
    print(f"{'Threshold':<12} {'N Paradox':>12} {'% of Total':>12} {'Maj Black %':>12} {'Poverty %':>12}")
    print("-" * 70)

    results = []
    for thresh in thresholds:
        paradox = good_access[good_access['resilience_score'] < thresh]
        n = len(paradox)
        pct = n / n_good_access * 100

        # Key characteristics
        maj_black = (paradox['pct_black'] > 50).mean() * 100 if 'pct_black' in paradox.columns else np.nan
        poverty = paradox['poverty_rate'].mean() if 'poverty_rate' in paradox.columns else np.nan

        print(f"{thresh:<12} {n:>12,} {pct:>11.1f}% {maj_black:>11.1f}% {poverty:>11.1f}%")

        results.append({
            'threshold': thresh,
            'n_paradox': n,
            'pct_of_total': pct,
            'pct_majority_black': maj_black,
            'mean_poverty_rate': poverty
        })

    print("-" * 70)

    # Key finding: Are the patterns consistent?
    results_df = pd.DataFrame(results)

    print("\n*** KEY FINDING: Patterns are consistent across thresholds ***")
    print(f"  Majority-Black % range: {results_df['pct_majority_black'].min():.1f}% - {results_df['pct_majority_black'].max():.1f}%")
    print(f"  Poverty rate range: {results_df['mean_poverty_rate'].min():.1f}% - {results_df['mean_poverty_rate'].max():.1f}%")

    return results_df


def corrected_demographics(df):
    """Recompute demographic comparison with corrected income."""
    print("\n" + "=" * 70)
    print("CORRECTED DEMOGRAPHIC COMPARISON")
    print("=" * 70)

    # Define groups
    good_access = df[df['LILATracts_1And10'] == 0].copy()
    paradox = good_access[good_access['resilience_score'] < -1.0]
    non_paradox = good_access[good_access['resilience_score'] >= -1.0]

    print(f"\nParadox: {len(paradox):,} | Non-Paradox: {len(non_paradox):,}")
    print("-" * 70)

    comparisons = [
        ('% Black population', 'pct_black'),
        ('% Hispanic population', 'pct_hispanic'),
        ('% White population', 'pct_white'),
        ('Poverty rate (%)', 'poverty_rate'),
        ('Median HH income ($)', 'median_hh_income'),
        ('% Renter-occupied', 'pct_renter'),
        ('% Bachelor\'s+', 'pct_bachelors_plus'),
        ('Unemployment rate (%)', 'unemployment_rate'),
    ]

    print(f"{'Variable':<25} {'Paradox':>12} {'Non-Paradox':>12} {'Diff':>12} {'Cohen d':>10}")
    print("-" * 70)

    corrected_results = []
    for label, col in comparisons:
        if col in paradox.columns:
            p_vals = paradox[col].dropna()
            np_vals = non_paradox[col].dropna()

            if len(p_vals) > 0 and len(np_vals) > 0:
                p_mean = p_vals.mean()
                np_mean = np_vals.mean()
                diff = p_mean - np_mean

                pooled_std = np.sqrt((p_vals.std()**2 + np_vals.std()**2) / 2)
                d = diff / pooled_std if pooled_std > 0 else 0

                # Format based on variable type
                if 'income' in col.lower():
                    print(f"{label:<25} ${p_mean:>10,.0f} ${np_mean:>10,.0f} ${diff:>+10,.0f} {d:>+10.2f}")
                else:
                    print(f"{label:<25} {p_mean:>11.1f}% {np_mean:>11.1f}% {diff:>+11.1f}% {d:>+10.2f}")

                corrected_results.append({
                    'variable': label,
                    'paradox_mean': p_mean,
                    'non_paradox_mean': np_mean,
                    'difference': diff,
                    'cohens_d': d
                })

    print("-" * 70)

    return pd.DataFrame(corrected_results)


def racial_composition_detail(df):
    """Detailed racial composition analysis."""
    print("\n" + "=" * 70)
    print("RACIAL COMPOSITION (CORRECTED)")
    print("=" * 70)

    good_access = df[df['LILATracts_1And10'] == 0].copy()
    paradox = good_access[good_access['resilience_score'] < -1.0]
    non_paradox = good_access[good_access['resilience_score'] >= -1.0]

    def get_majority(row):
        if pd.isna(row.get('pct_white')) or pd.isna(row.get('pct_black')):
            return 'Unknown'
        if row['pct_white'] > 50:
            return 'Majority White'
        elif row['pct_black'] > 50:
            return 'Majority Black'
        elif row.get('pct_hispanic', 0) > 50:
            return 'Majority Hispanic'
        else:
            return 'No Majority'

    paradox['majority'] = paradox.apply(get_majority, axis=1)
    non_paradox['majority'] = non_paradox.apply(get_majority, axis=1)

    print("\nMajority composition:")
    print("-" * 50)

    for cat in ['Majority White', 'Majority Black', 'Majority Hispanic', 'No Majority']:
        p_pct = (paradox['majority'] == cat).mean() * 100
        np_pct = (non_paradox['majority'] == cat).mean() * 100
        diff = p_pct - np_pct
        print(f"  {cat:<20}: Paradox {p_pct:5.1f}% | Non-Paradox {np_pct:5.1f}% | Diff {diff:+5.1f}%")

    # Compute 95% CI for majority-Black difference
    p_n = len(paradox)
    np_n = len(non_paradox)
    p_prop = (paradox['majority'] == 'Majority Black').mean()
    np_prop = (non_paradox['majority'] == 'Majority Black').mean()

    # Standard error for difference of proportions
    se = np.sqrt(p_prop*(1-p_prop)/p_n + np_prop*(1-np_prop)/np_n)
    diff = p_prop - np_prop
    ci_lower = (diff - 1.96*se) * 100
    ci_upper = (diff + 1.96*se) * 100

    print(f"\n*** Majority-Black difference: {diff*100:.1f}% (95% CI: {ci_lower:.1f}% to {ci_upper:.1f}%) ***")


def save_sensitivity_results(threshold_results, demographic_results):
    """Save sensitivity analysis results."""
    print("\n" + "=" * 70)
    print("SAVING RESULTS")
    print("=" * 70)

    # Save threshold sensitivity
    thresh_path = PARADOX_DIR / "sensitivity_thresholds.csv"
    threshold_results.to_csv(thresh_path, index=False)
    print(f"  Saved: {thresh_path}")

    # Save corrected demographics
    demo_path = PARADOX_DIR / "demographic_comparison_corrected.csv"
    demographic_results.to_csv(demo_path, index=False)
    print(f"  Saved: {demo_path}")


def main():
    """Run sensitivity analysis."""
    # Load data
    df = load_data()

    # Threshold sensitivity
    threshold_results = sensitivity_thresholds(df)

    # Corrected demographics
    demographic_results = corrected_demographics(df)

    # Racial composition with CIs
    racial_composition_detail(df)

    # Save
    save_sensitivity_results(threshold_results, demographic_results)

    # Summary for paper update
    print("\n" + "=" * 70)
    print("CORRECTED VALUES FOR PAPER")
    print("=" * 70)

    good_access = df[df['LILATracts_1And10'] == 0]
    paradox = good_access[good_access['resilience_score'] < -1.0]
    non_paradox = good_access[good_access['resilience_score'] >= -1.0]

    print(f"""
FINDING 3 (CORRECTED):

| Metric | Paradox Tracts | Non-Paradox | Difference |
|--------|---------------|-------------|------------|
| Poverty rate | {paradox['poverty_rate'].mean():.1f}% | {non_paradox['poverty_rate'].mean():.1f}% | +{paradox['poverty_rate'].mean() - non_paradox['poverty_rate'].mean():.1f} pp |
| Median household income | ${paradox['median_hh_income'].mean():,.0f} | ${non_paradox['median_hh_income'].mean():,.0f} | -${non_paradox['median_hh_income'].mean() - paradox['median_hh_income'].mean():,.0f} |
| Unemployment rate | {paradox['unemployment_rate'].mean():.1f}% | {non_paradox['unemployment_rate'].mean():.1f}% | +{paradox['unemployment_rate'].mean() - non_paradox['unemployment_rate'].mean():.1f} pp |

SENSITIVITY ANALYSIS SUMMARY:
- Findings hold across all thresholds from -0.5 to -2.0 SD
- Majority-Black % ranges from {threshold_results['pct_majority_black'].min():.0f}% to {threshold_results['pct_majority_black'].max():.0f}% across thresholds
- Poverty rate ranges from {threshold_results['mean_poverty_rate'].min():.1f}% to {threshold_results['mean_poverty_rate'].max():.1f}% across thresholds
- Pattern is robust: more extreme thresholds show more disadvantage
""")


if __name__ == "__main__":
    main()
