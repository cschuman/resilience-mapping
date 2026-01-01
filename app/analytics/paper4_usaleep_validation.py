#!/usr/bin/env python3
"""
Paper 4 Validation: Test if race-health correlations survive with non-MRP data

CRITICAL TEST: The peer review identified that CDC PLACES uses MRP (Multilevel
Regression with Poststratification) which includes race as a covariate. This means
our r=-0.34 correlation between %Black and resilience might be an artifact.

USALEEP (U.S. Small-area Life Expectancy Estimates) uses vital statistics
(actual death records), NOT MRP modeling. If the correlation persists with
USALEEP data, our findings are robust. If it disappears, we have an artifact.

Expected outcome if findings are REAL:
  - r(pct_black, life_expectancy) ≈ -0.30 to -0.40 (negative: higher Black % = lower LE)
  - This would validate that the health-race relationship is real, not an MRP artifact

Expected outcome if findings are ARTIFACT:
  - r(pct_black, life_expectancy) ≈ 0 to -0.10
  - Would indicate CDC PLACES correlations are inflated by methodology
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "external"
USALEEP_PATH = Path(__file__).parent / "data" / "external" / "USALEEP_US_A.CSV"


def load_usaleep():
    """Load USALEEP life expectancy data."""
    df = pd.read_csv(USALEEP_PATH)

    # Format Tract ID to 11-digit GEOID with leading zeros
    df['GEOID'] = df['Tract ID'].astype(str).str.zfill(11)

    # Rename columns
    df = df.rename(columns={
        'e(0)': 'life_expectancy',
        'se(e(0))': 'life_expectancy_se'
    })

    return df[['GEOID', 'life_expectancy', 'life_expectancy_se']]


def load_acs():
    """Load ACS demographic data."""
    df = pd.read_csv(DATA_DIR / "acs_demographics_2022.csv")
    df['GEOID'] = df['GEOID'].astype(str).str.zfill(11)
    return df


def compute_correlations(df):
    """Compute correlations between demographics and life expectancy."""

    # Variables to correlate with life expectancy
    demo_vars = [
        'pct_black', 'pct_white', 'pct_hispanic', 'pct_asian',
        'median_hh_income', 'poverty_rate', 'unemployment_rate',
        'pct_bachelors_plus', 'pct_renter'
    ]

    results = []
    for var in demo_vars:
        if var not in df.columns:
            continue

        # Drop missing
        valid = df[[var, 'life_expectancy']].dropna()
        if len(valid) < 100:
            continue

        r, p = stats.pearsonr(valid[var], valid['life_expectancy'])
        results.append({
            'variable': var,
            'correlation': r,
            'p_value': p,
            'n': len(valid)
        })

    return pd.DataFrame(results)


def compare_majority_groups(df):
    """Compare life expectancy between majority-white and majority-minority tracts."""

    # Classify tracts
    df['majority_type'] = np.where(df['pct_white'] > 50, 'Majority-White', 'Majority-Minority')

    maj_white = df[df['majority_type'] == 'Majority-White']['life_expectancy'].dropna()
    maj_minority = df[df['majority_type'] == 'Majority-Minority']['life_expectancy'].dropna()

    # T-test (naive - we know this is problematic due to clustering, but for comparison)
    t_stat, p_value = stats.ttest_ind(maj_white, maj_minority)

    # Effect size (Cohen's d)
    pooled_std = np.sqrt((maj_white.std()**2 + maj_minority.std()**2) / 2)
    cohens_d = (maj_white.mean() - maj_minority.mean()) / pooled_std

    return {
        'majority_white_n': len(maj_white),
        'majority_white_mean': maj_white.mean(),
        'majority_white_std': maj_white.std(),
        'majority_minority_n': len(maj_minority),
        'majority_minority_mean': maj_minority.mean(),
        'majority_minority_std': maj_minority.std(),
        'difference_years': maj_white.mean() - maj_minority.mean(),
        't_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d
    }


def main():
    print("=" * 70)
    print("PAPER 4 VALIDATION: Testing findings with non-MRP data (USALEEP)")
    print("=" * 70)
    print()

    # Load data
    print("Loading data...")
    usaleep = load_usaleep()
    acs = load_acs()

    print(f"  USALEEP tracts: {len(usaleep):,}")
    print(f"  ACS tracts: {len(acs):,}")

    # Merge
    df = usaleep.merge(acs, on='GEOID', how='inner')
    print(f"  Merged tracts: {len(df):,}")
    print()

    # NOTE: USALEEP is from 2010-2015, ACS is 2022 - there's a temporal mismatch
    # This is a limitation but demographics change slowly at tract level
    print("NOTE: USALEEP (2010-2015) vs ACS (2022) - temporal mismatch acknowledged")
    print()

    # Correlations
    print("-" * 70)
    print("CORRELATION ANALYSIS: Demographics vs Life Expectancy")
    print("-" * 70)
    print()

    corr_df = compute_correlations(df)
    corr_df = corr_df.sort_values('correlation')

    print("Variable                    r       p-value         N")
    print("-" * 55)
    for _, row in corr_df.iterrows():
        sig = "***" if row['p_value'] < 0.001 else "**" if row['p_value'] < 0.01 else "*" if row['p_value'] < 0.05 else ""
        print(f"{row['variable']:<24} {row['correlation']:>7.3f}   {row['p_value']:<12.2e}   {row['n']:>6,} {sig}")

    # Key comparison
    print()
    print("-" * 70)
    print("CRITICAL COMPARISON: Paper 4 findings vs USALEEP validation")
    print("-" * 70)
    print()

    pct_black_corr = corr_df[corr_df['variable'] == 'pct_black']['correlation'].values[0]
    pct_hispanic_corr = corr_df[corr_df['variable'] == 'pct_hispanic']['correlation'].values[0]

    print("                           Paper 4 (CDC PLACES)    USALEEP (Vital Stats)")
    print("-" * 70)
    print(f"r(pct_black, outcome)         r = -0.34              r = {pct_black_corr:+.3f}")
    print(f"r(pct_hispanic, outcome)      r = +0.01              r = {pct_hispanic_corr:+.3f}")
    print()

    # Interpretation
    if pct_black_corr < -0.25:
        print("✓ VALIDATED: Black-health correlation persists with non-MRP data")
        print(f"  The r={pct_black_corr:.3f} correlation with life expectancy confirms")
        print("  that the relationship is NOT an artifact of CDC PLACES methodology.")
    elif pct_black_corr < -0.10:
        print("⚠ PARTIAL VALIDATION: Correlation weaker but present")
        print(f"  The r={pct_black_corr:.3f} is weaker than r=-0.34 in Paper 4.")
        print("  Some of the original finding may be methodological artifact.")
    else:
        print("✗ NOT VALIDATED: Correlation much weaker with non-MRP data")
        print(f"  The r={pct_black_corr:.3f} suggests the r=-0.34 in Paper 4")
        print("  may be substantially inflated by CDC PLACES methodology.")

    print()

    # Majority group comparison
    print("-" * 70)
    print("MAJORITY GROUP COMPARISON: Life Expectancy Gap")
    print("-" * 70)
    print()

    group_stats = compare_majority_groups(df)

    print(f"Majority-White tracts:    N = {group_stats['majority_white_n']:,}")
    print(f"  Mean life expectancy:   {group_stats['majority_white_mean']:.2f} years")
    print(f"  SD:                     {group_stats['majority_white_std']:.2f} years")
    print()
    print(f"Majority-Minority tracts: N = {group_stats['majority_minority_n']:,}")
    print(f"  Mean life expectancy:   {group_stats['majority_minority_mean']:.2f} years")
    print(f"  SD:                     {group_stats['majority_minority_std']:.2f} years")
    print()
    print(f"LIFE EXPECTANCY GAP:      {group_stats['difference_years']:.2f} years")
    print(f"  (Majority-White - Majority-Minority)")
    print()
    print(f"Effect size (Cohen's d):  {group_stats['cohens_d']:.3f}")
    print(f"t-statistic:              {group_stats['t_statistic']:.2f}")
    print(f"p-value:                  {group_stats['p_value']:.2e}")
    print()

    # Paper 4 comparison
    print("-" * 70)
    print("COMPARISON WITH PAPER 4 FINDINGS")
    print("-" * 70)
    print()
    print("                              Paper 4        USALEEP Validation")
    print("-" * 70)
    print(f"Effect size (Cohen's d):      0.38 SD        {group_stats['cohens_d']:.2f} SD")
    print(f"Gap interpretation:           0.38 SD in     {group_stats['difference_years']:.1f} years in")
    print(f"                              health burden  life expectancy")
    print()

    # Final verdict
    print("=" * 70)
    print("VALIDATION VERDICT")
    print("=" * 70)
    print()

    if abs(pct_black_corr) > 0.25 and group_stats['cohens_d'] > 0.3:
        print("✓ FINDINGS VALIDATED")
        print("  The race-health relationship in Paper 4 is CONFIRMED by USALEEP data.")
        print("  The correlation is NOT an artifact of CDC PLACES MRP methodology.")
        print()
        print("  Key evidence:")
        print(f"  - %Black correlates r={pct_black_corr:.3f} with life expectancy")
        print(f"  - Life expectancy gap of {group_stats['difference_years']:.1f} years between groups")
        print(f"  - Effect size d={group_stats['cohens_d']:.2f} is meaningful")
    else:
        print("⚠ FINDINGS REQUIRE CAUTION")
        print("  The validation shows some discrepancy with Paper 4 findings.")
        print("  Consider revising correlation estimates and effect sizes.")

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
