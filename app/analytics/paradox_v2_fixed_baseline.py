#!/usr/bin/env python3
"""
Paradox Study V2: Fixed Baseline Model

CRITICAL FIX: The original analysis was circular - it excluded race and poverty
from the baseline model, then "discovered" that paradox tracts were Black and poor.

This version uses a PROPER baseline model that includes all known predictors,
then identifies tracts with unexpectedly poor health GIVEN their demographics.

The question becomes: "Which communities have worse health than demographics predict?"
rather than "Which communities are Black and poor?"
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path(__file__).parent.parent.parent / "data"
PARADOX_DIR = DATA_DIR / "processed" / "paradox_study"


def load_all_data():
    """Load and merge all data sources."""
    print("=" * 70)
    print("PARADOX STUDY V2: FIXED BASELINE MODEL")
    print("=" * 70)
    print("\nCRITICAL CHANGE: Baseline now includes demographics")
    print("This eliminates the circular reasoning critique.\n")

    # Load model
    model = pd.read_csv(DATA_DIR / "processed" / "model_table_corrected.csv")
    model['GEOID'] = model['GEOID'].astype(str).str.zfill(11)

    # Load FARA
    fara = pd.read_csv(DATA_DIR / "input" / "fara_2019.csv")
    fara['GEOID'] = fara['CensusTract'].astype(str).str.zfill(11)
    fara['LILATracts_1And10'] = pd.to_numeric(fara['LILATracts_1And10'], errors='coerce').fillna(0)

    # Load ACS
    acs = pd.read_csv(DATA_DIR / "external" / "acs_demographics_2022.csv")
    acs['GEOID'] = acs['GEOID'].astype(str).str.zfill(11)

    # Load SVI
    svi = pd.read_csv(DATA_DIR / "external" / "svi_2022_us.csv")
    svi['GEOID'] = svi['FIPS'].astype(str).str.zfill(11)
    svi_cols = ['GEOID', 'RPL_THEMES', 'RPL_THEME1', 'RPL_THEME2', 'RPL_THEME3', 'RPL_THEME4']
    svi = svi[[c for c in svi_cols if c in svi.columns]]

    # Load EJI
    eji = pd.read_csv(DATA_DIR / "external" / "EJI_2022_United_States" / "EJI_2022_United_States.csv")
    eji['GEOID'] = eji['GEOID'].astype(str).str.zfill(11)
    eji_cols = ['GEOID', 'RPL_EJI', 'RPL_EBM']
    eji = eji[[c for c in eji_cols if c in eji.columns]]

    # Merge
    df = model.merge(fara[['GEOID', 'LILATracts_1And10']], on='GEOID', how='left')
    df = df.merge(acs, on='GEOID', how='left')
    df = df.merge(svi, on='GEOID', how='left')
    df = df.merge(eji, on='GEOID', how='left')

    print(f"Total tracts: {len(df):,}")
    print(f"Good food access (non-LILA): {(df['LILATracts_1And10'] == 0).sum():,}")

    return df


def build_comprehensive_baseline(df):
    """
    Build a baseline model that includes ALL known predictors of health.

    The residuals from this model represent health that is UNEXPLAINED
    by demographics, SES, food access, and structural factors.
    """
    print("\n" + "=" * 70)
    print("BUILDING COMPREHENSIVE BASELINE MODEL")
    print("=" * 70)

    # Filter to good food access
    good_access = df[df['LILATracts_1And10'] == 0].copy()

    # Define predictors (INCLUDE race and SES - this is the fix)
    predictors = [
        'pct_black',
        'pct_white',
        'pct_hispanic',
        'poverty_rate',
        'median_hh_income',
        'pct_bachelors_plus',
        'unemployment_rate',
        'pct_renter',
        'RPL_THEMES',  # SVI overall
    ]

    # Add state fixed effects
    good_access['state'] = good_access['GEOID'].str[:2]

    # Prepare data
    available_predictors = [p for p in predictors if p in good_access.columns]
    print(f"\nPredictors in model: {available_predictors}")

    # Rename burden column for clarity
    good_access['health_burden'] = good_access['burden']

    # Drop missing
    model_df = good_access.dropna(subset=available_predictors + ['health_burden'])
    print(f"Tracts with complete data: {len(model_df):,}")

    # Create state dummies
    state_dummies = pd.get_dummies(model_df['state'], prefix='state', drop_first=True)

    # Combine predictors
    X = pd.concat([
        model_df[available_predictors].reset_index(drop=True),
        state_dummies.reset_index(drop=True)
    ], axis=1)

    y = model_df['health_burden'].values

    # Standardize continuous predictors (not dummies)
    scaler = StandardScaler()
    X_continuous = scaler.fit_transform(model_df[available_predictors])

    # Combine with dummies
    X_full = np.hstack([X_continuous, state_dummies.values])

    # Fit model
    baseline_model = LinearRegression()
    baseline_model.fit(X_full, y)
    r2 = baseline_model.score(X_full, y)

    print(f"\nBaseline R²: {r2:.4f} ({r2*100:.1f}%)")
    print("(This is how much of health burden is EXPLAINED by demographics + SES)")

    # Calculate residuals
    predictions = baseline_model.predict(X_full)
    residuals = y - predictions

    # Create new resilience score from comprehensive model
    std_resid = np.std(residuals)
    model_df = model_df.copy()
    model_df['v2_residual'] = residuals
    model_df['v2_resilience_score'] = -residuals / std_resid

    print(f"\nResidual stats:")
    print(f"  Mean: {np.mean(residuals):.4f}")
    print(f"  Std: {std_resid:.4f}")
    print(f"  Min: {np.min(residuals):.4f}")
    print(f"  Max: {np.max(residuals):.4f}")

    # Feature importance
    print("\nFeature coefficients (standardized):")
    print("-" * 50)
    for var, coef in zip(available_predictors, baseline_model.coef_[:len(available_predictors)]):
        print(f"  {var:<25}: β = {coef:+.4f}")

    return model_df, baseline_model, r2


def identify_v2_paradox(model_df):
    """
    Identify paradox tracts using the new comprehensive baseline.

    These are tracts where health is WORSE than what demographics predict -
    meaning something BEYOND demographics is harming them.
    """
    print("\n" + "=" * 70)
    print("IDENTIFYING V2 PARADOX TRACTS")
    print("=" * 70)

    # Define paradox using new residuals
    model_df['v2_is_paradox'] = model_df['v2_resilience_score'] < -1.0

    n_paradox = model_df['v2_is_paradox'].sum()
    pct_paradox = n_paradox / len(model_df) * 100

    print(f"\nV2 Paradox tracts: {n_paradox:,} ({pct_paradox:.1f}%)")

    # Compare to original
    model_df['original_is_paradox'] = model_df['resilience_score'] < -1.0
    n_original = model_df['original_is_paradox'].sum()

    print(f"Original paradox tracts: {n_original:,}")
    print(f"Reduction: {n_original - n_paradox:,} ({(n_original - n_paradox)/n_original*100:.1f}%)")

    # Overlap analysis
    both = (model_df['v2_is_paradox'] & model_df['original_is_paradox']).sum()
    only_original = (model_df['original_is_paradox'] & ~model_df['v2_is_paradox']).sum()
    only_v2 = (model_df['v2_is_paradox'] & ~model_df['original_is_paradox']).sum()

    print(f"\nOverlap:")
    print(f"  Both: {both:,}")
    print(f"  Only in original (explained by demographics): {only_original:,}")
    print(f"  Only in V2 (new paradox): {only_v2:,}")

    return model_df


def analyze_v2_paradox(model_df):
    """Analyze what distinguishes V2 paradox tracts."""
    print("\n" + "=" * 70)
    print("V2 PARADOX CHARACTERIZATION")
    print("=" * 70)

    v2_paradox = model_df[model_df['v2_is_paradox'] == True]
    v2_non_paradox = model_df[model_df['v2_is_paradox'] == False]

    print(f"\nV2 Paradox: {len(v2_paradox):,} | Non-Paradox: {len(v2_non_paradox):,}")

    # Key question: Are V2 paradox tracts STILL disproportionately Black?
    # If we controlled for demographics, they should NOT be.

    comparisons = [
        ('% Black', 'pct_black'),
        ('% White', 'pct_white'),
        ('Poverty rate', 'poverty_rate'),
        ('Median income', 'median_hh_income'),
        ('SVI score', 'RPL_THEMES'),
        ('EJI score', 'RPL_EJI'),
        ('Env burden', 'RPL_EBM'),
    ]

    print("\n" + "-" * 70)
    print(f"{'Variable':<20} {'V2 Paradox':>12} {'Non-Paradox':>12} {'Diff':>10} {'Cohen d':>10}")
    print("-" * 70)

    results = []
    for label, col in comparisons:
        if col in model_df.columns:
            p_vals = v2_paradox[col].dropna()
            np_vals = v2_non_paradox[col].dropna()

            if len(p_vals) > 100 and len(np_vals) > 100:
                p_mean = p_vals.mean()
                np_mean = np_vals.mean()
                diff = p_mean - np_mean

                pooled_std = np.sqrt((p_vals.std()**2 + np_vals.std()**2) / 2)
                d = diff / pooled_std if pooled_std > 0 else 0

                # 95% CI for Cohen's d
                se_d = np.sqrt((len(p_vals) + len(np_vals)) / (len(p_vals) * len(np_vals)) + d**2 / (2 * (len(p_vals) + len(np_vals))))
                ci_lower = d - 1.96 * se_d
                ci_upper = d + 1.96 * se_d

                if 'income' in col.lower():
                    print(f"{label:<20} ${p_mean:>10,.0f} ${np_mean:>10,.0f} ${diff:>+9,.0f} {d:>+10.2f}")
                else:
                    print(f"{label:<20} {p_mean:>11.1f}% {np_mean:>11.1f}% {diff:>+9.1f}% {d:>+10.2f}")

                results.append({
                    'variable': label,
                    'v2_paradox_mean': p_mean,
                    'non_paradox_mean': np_mean,
                    'difference': diff,
                    'cohens_d': d,
                    'ci_lower': ci_lower,
                    'ci_upper': ci_upper
                })

    print("-" * 70)

    # KEY TEST: Is there still a racial disparity after controlling for demographics?
    black_d = [r for r in results if r['variable'] == '% Black'][0]['cohens_d']
    print(f"\n*** KEY TEST: After controlling for demographics ***")
    print(f"  % Black Cohen's d = {black_d:.3f}")

    if abs(black_d) < 0.2:
        print("  INTERPRETATION: Small or no racial disparity - demographics explain the original finding")
    else:
        print("  INTERPRETATION: Racial disparity persists beyond demographics - structural factors matter")

    return pd.DataFrame(results)


def what_explains_v2_paradox(model_df):
    """
    The V2 paradox tracts have worse health than demographics predict.
    What explains this? Look at factors NOT in the baseline model.
    """
    print("\n" + "=" * 70)
    print("WHAT EXPLAINS V2 PARADOX?")
    print("=" * 70)
    print("(Factors NOT in baseline: EJI environmental burden, healthcare access)")

    v2_paradox = model_df[model_df['v2_is_paradox'] == True]
    v2_non_paradox = model_df[model_df['v2_is_paradox'] == False]

    # EJI Environmental Burden (not in baseline)
    if 'RPL_EBM' in model_df.columns:
        p_ebm = v2_paradox['RPL_EBM'].dropna()
        np_ebm = v2_non_paradox['RPL_EBM'].dropna()

        p_mean = p_ebm.mean()
        np_mean = np_ebm.mean()
        pooled_std = np.sqrt((p_ebm.std()**2 + np_ebm.std()**2) / 2)
        d = (p_mean - np_mean) / pooled_std if pooled_std > 0 else 0

        print(f"\nEnvironmental Burden (EJI):")
        print(f"  V2 Paradox: {p_mean:.3f}")
        print(f"  Non-Paradox: {np_mean:.3f}")
        print(f"  Cohen's d: {d:.3f}")

        if d > 0.2:
            print("  → Environmental burden is HIGHER in V2 paradox tracts")
            print("  → This is a NOVEL finding - environment affects health beyond demographics")

    # What percentage of V2 paradox is in high environmental burden areas?
    if 'RPL_EBM' in v2_paradox.columns:
        high_burden = (v2_paradox['RPL_EBM'] > 0.75).mean() * 100
        print(f"\n  V2 paradox tracts in top 25% environmental burden: {high_burden:.1f}%")


def save_v2_results(model_df, v2_comparison, baseline_r2):
    """Save V2 analysis results."""
    print("\n" + "=" * 70)
    print("SAVING V2 RESULTS")
    print("=" * 70)

    # Save V2 paradox tracts
    v2_paradox = model_df[model_df['v2_is_paradox'] == True]
    v2_path = PARADOX_DIR / "v2_paradox_tracts.csv"
    v2_paradox.to_csv(v2_path, index=False)
    print(f"  Saved: {v2_path} ({len(v2_paradox):,} tracts)")

    # Save comparison
    comp_path = PARADOX_DIR / "v2_demographic_comparison.csv"
    v2_comparison.to_csv(comp_path, index=False)
    print(f"  Saved: {comp_path}")

    # Save summary
    summary_path = PARADOX_DIR / "v2_summary.txt"
    with open(summary_path, 'w') as f:
        f.write("V2 PARADOX STUDY - FIXED BASELINE\n")
        f.write("=" * 50 + "\n\n")
        f.write("CRITICAL CHANGE: Baseline model now includes demographics\n\n")
        f.write(f"Baseline R²: {baseline_r2:.4f} ({baseline_r2*100:.1f}%)\n")
        f.write(f"V2 Paradox tracts: {len(v2_paradox):,}\n")
        f.write(f"Original paradox tracts: {model_df['original_is_paradox'].sum():,}\n")
    print(f"  Saved: {summary_path}")


def main():
    """Run V2 analysis with fixed baseline."""
    # Load data
    df = load_all_data()

    # Build comprehensive baseline
    model_df, baseline_model, baseline_r2 = build_comprehensive_baseline(df)

    # Identify V2 paradox
    model_df = identify_v2_paradox(model_df)

    # Analyze V2 paradox
    v2_comparison = analyze_v2_paradox(model_df)

    # What explains V2?
    what_explains_v2_paradox(model_df)

    # Save
    save_v2_results(model_df, v2_comparison, baseline_r2)

    # Summary
    print("\n" + "=" * 70)
    print("CRITICAL METHODOLOGICAL FIX SUMMARY")
    print("=" * 70)

    original_n = model_df['original_is_paradox'].sum()
    v2_n = model_df['v2_is_paradox'].sum()
    reduction = original_n - v2_n

    print(f"""
THE CIRCULAR REASONING PROBLEM:
  Original analysis excluded demographics from baseline
  → "Discovered" paradox tracts were Black and poor
  → This was circular - we manufactured the finding

THE FIX:
  Include demographics in baseline model
  → Baseline R² = {baseline_r2*100:.1f}% (demographics explain this much of health)
  → V2 paradox = tracts with WORSE health than demographics predict

THE RESULT:
  Original paradox tracts: {original_n:,}
  V2 paradox tracts: {v2_n:,}
  Reduction: {reduction:,} ({reduction/original_n*100:.1f}%)

INTERPRETATION:
  {reduction/original_n*100:.1f}% of the original "paradox" was explained by demographics
  These were not paradoxes - they were predictable given race and poverty

  The V2 paradox tracts are the TRUE unexplained cases:
  Communities with worse health than their demographics predict

  This is the honest finding: {v2_n:,} tracts have unexplained poor health
""")


if __name__ == "__main__":
    main()
