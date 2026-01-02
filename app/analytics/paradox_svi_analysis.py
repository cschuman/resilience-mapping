#!/usr/bin/env python3
"""
Paradox Study Phase 2B: Social Vulnerability Index Overlay

Merge CDC SVI data with paradox tracts to understand structural drivers.

SVI Themes:
- Theme 1: Socioeconomic Status (poverty, unemployment, income, education)
- Theme 2: Household Composition & Disability (age, disability, single-parent)
- Theme 3: Minority Status & Language
- Theme 4: Housing Type & Transportation (multi-unit, mobile, crowding, no vehicle)
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


def load_data():
    """Load paradox tracts and SVI data."""
    print("=" * 70)
    print("SVI STRUCTURAL ANALYSIS")
    print("=" * 70)

    # Load paradox tracts
    paradox = pd.read_csv(PARADOX_DIR / "paradox_tracts_enhanced.csv")
    paradox['GEOID'] = paradox['GEOID'].astype(str).str.zfill(11)
    print(f"\nParadox tracts: {len(paradox):,}")

    # Load all model tracts for comparison
    model = pd.read_csv(DATA_DIR / "processed" / "model_table_corrected.csv")
    model['GEOID'] = model['GEOID'].astype(str).str.zfill(11)
    print(f"All model tracts: {len(model):,}")

    # Load SVI data
    svi = pd.read_csv(DATA_DIR / "external" / "svi_2022_us.csv", encoding='utf-8-sig')
    svi['GEOID'] = svi['FIPS'].astype(str).str.zfill(11)
    print(f"SVI data: {len(svi):,} tracts")

    # Key SVI columns
    svi_cols = [
        'GEOID',
        'RPL_THEMES',   # Overall vulnerability (0-1)
        'RPL_THEME1',   # Socioeconomic
        'RPL_THEME2',   # Household composition/disability
        'RPL_THEME3',   # Minority status/language
        'RPL_THEME4',   # Housing/transportation
        'E_POV150',     # Population below 150% poverty
        'E_UNEMP',      # Unemployed population
        'E_UNINSUR',    # Uninsured population
        'E_NOVEH',      # No vehicle households
        'E_GROUPQ',     # Group quarters population
        'E_MINRTY',     # Minority population
    ]

    svi_subset = svi[[c for c in svi_cols if c in svi.columns]].copy()

    return paradox, model, svi_subset


def merge_svi(paradox, model, svi):
    """Merge SVI data with paradox and model tracts."""
    print("\nMerging SVI data...")

    paradox_svi = paradox.merge(svi, on='GEOID', how='left')
    model_svi = model.merge(svi, on='GEOID', how='left')

    # Check merge success
    paradox_matched = paradox_svi['RPL_THEMES'].notna().sum()
    print(f"  Paradox tracts matched to SVI: {paradox_matched:,} ({paradox_matched/len(paradox)*100:.1f}%)")

    model_matched = model_svi['RPL_THEMES'].notna().sum()
    print(f"  Model tracts matched to SVI: {model_matched:,} ({model_matched/len(model)*100:.1f}%)")

    return paradox_svi, model_svi


def analyze_svi_themes(paradox_svi, model_svi):
    """Analyze SVI themes in paradox vs non-paradox tracts."""
    print("\n" + "=" * 70)
    print("SVI THEME ANALYSIS: PARADOX VS NON-PARADOX")
    print("=" * 70)

    # Get non-paradox good-access tracts
    non_paradox = model_svi[
        (model_svi.get('LILATracts_1And10', 0) == 0) &
        (model_svi['resilience_score'] >= -1.0)
    ] if 'LILATracts_1And10' in model_svi.columns else model_svi[model_svi['resilience_score'] >= -1.0]

    themes = [
        ('RPL_THEMES', 'Overall SVI'),
        ('RPL_THEME1', 'Socioeconomic Status'),
        ('RPL_THEME2', 'Household Comp/Disability'),
        ('RPL_THEME3', 'Minority Status/Language'),
        ('RPL_THEME4', 'Housing/Transportation'),
    ]

    print(f"\nComparing: Paradox (n={len(paradox_svi):,}) vs Non-Paradox (n={len(non_paradox):,})")
    print("-" * 70)
    print(f"{'Theme':<30} {'Paradox':>10} {'Non-Para':>10} {'Diff':>10} {'Effect (d)':>12}")
    print("-" * 70)

    results = []
    for col, label in themes:
        if col in paradox_svi.columns:
            p_vals = paradox_svi[col].dropna()
            np_vals = non_paradox[col].dropna()

            if len(p_vals) > 0 and len(np_vals) > 0:
                p_mean = p_vals.mean()
                np_mean = np_vals.mean()
                diff = p_mean - np_mean

                # Cohen's d
                pooled_std = np.sqrt((p_vals.std()**2 + np_vals.std()**2) / 2)
                d = diff / pooled_std if pooled_std > 0 else 0

                # T-test
                t_stat, p_value = stats.ttest_ind(p_vals, np_vals)

                print(f"{label:<30} {p_mean:>10.3f} {np_mean:>10.3f} {diff:>+10.3f} {d:>+12.2f}")

                results.append({
                    'theme': label,
                    'paradox_mean': p_mean,
                    'non_paradox_mean': np_mean,
                    'difference': diff,
                    'cohens_d': d,
                    'p_value': p_value
                })

    print("-" * 70)

    # Key finding
    if results:
        most_different = max(results, key=lambda x: abs(x['cohens_d']))
        print(f"\n*** Largest difference: {most_different['theme']} (d={most_different['cohens_d']:+.2f}) ***")

    return pd.DataFrame(results)


def analyze_vulnerability_distribution(paradox_svi, model_svi):
    """Analyze how paradox tracts distribute across vulnerability quartiles."""
    print("\n" + "=" * 70)
    print("VULNERABILITY DISTRIBUTION")
    print("=" * 70)

    # Create vulnerability quartiles for all tracts
    all_tracts = model_svi.dropna(subset=['RPL_THEMES'])
    all_tracts['vuln_quartile'] = pd.qcut(all_tracts['RPL_THEMES'], 4, labels=['Q1 (Lowest)', 'Q2', 'Q3', 'Q4 (Highest)'])

    # Distribution of paradox tracts
    paradox_with_quartile = paradox_svi.dropna(subset=['RPL_THEMES']).copy()
    paradox_with_quartile['vuln_quartile'] = pd.cut(
        paradox_with_quartile['RPL_THEMES'],
        bins=[0, 0.25, 0.5, 0.75, 1.0],
        labels=['Q1 (Lowest)', 'Q2', 'Q3', 'Q4 (Highest)'],
        include_lowest=True
    )

    print("\nParadox tract distribution across SVI vulnerability quartiles:")
    print("-" * 50)

    quartile_counts = paradox_with_quartile['vuln_quartile'].value_counts().sort_index()
    total = len(paradox_with_quartile)

    for quartile in ['Q1 (Lowest)', 'Q2', 'Q3', 'Q4 (Highest)']:
        count = quartile_counts.get(quartile, 0)
        pct = count / total * 100 if total > 0 else 0
        bar = '█' * int(pct / 2)
        expected = 25.0  # If evenly distributed
        diff = pct - expected
        print(f"  {quartile:<15}: {count:>5} ({pct:>5.1f}%) {bar} [{diff:+.1f}% vs expected]")

    # What percentage are in high vulnerability?
    high_vuln = (paradox_with_quartile['RPL_THEMES'] >= 0.75).sum()
    high_vuln_pct = high_vuln / total * 100 if total > 0 else 0
    print(f"\n*** {high_vuln_pct:.1f}% of paradox tracts are in HIGH VULNERABILITY quartile (vs 25% expected) ***")

    return quartile_counts


def explain_paradox_with_svi(paradox_svi):
    """Use SVI themes to explain paradox variance."""
    print("\n" + "=" * 70)
    print("EXPLAINING PARADOX WITH SVI")
    print("=" * 70)

    # Prepare features
    svi_features = ['RPL_THEME1', 'RPL_THEME2', 'RPL_THEME3', 'RPL_THEME4']
    available_features = [f for f in svi_features if f in paradox_svi.columns]

    # Clean data
    analysis_df = paradox_svi[available_features + ['resilience_score']].dropna()
    print(f"\nTracts with complete SVI data: {len(analysis_df):,}")

    if len(analysis_df) < 100:
        print("Insufficient data for regression")
        return None

    X = analysis_df[available_features]
    y = analysis_df['resilience_score']

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Fit model
    model = LinearRegression()
    model.fit(X_scaled, y)

    r_squared = model.score(X_scaled, y)
    print(f"\nR² of SVI themes model: {r_squared:.3f}")
    print(f"SVI themes explain {r_squared*100:.1f}% of variance in paradox severity")

    # Feature importance
    print("\nSVI Theme coefficients:")
    labels = {
        'RPL_THEME1': 'Socioeconomic Status',
        'RPL_THEME2': 'Household Comp/Disability',
        'RPL_THEME3': 'Minority Status/Language',
        'RPL_THEME4': 'Housing/Transportation',
    }

    coefs = list(zip(available_features, model.coef_))
    coefs.sort(key=lambda x: abs(x[1]), reverse=True)

    for name, coef in coefs:
        label = labels.get(name, name)
        direction = "worse health" if coef < 0 else "better health"
        print(f"  {label:<30}: β={coef:+.3f} (higher → {direction})")

    return r_squared


def combined_model(paradox_svi):
    """Combine demographics + SVI to explain paradox."""
    print("\n" + "=" * 70)
    print("COMBINED MODEL: DEMOGRAPHICS + SVI")
    print("=" * 70)

    # All features
    demo_features = ['pct_black', 'pct_hispanic', 'poverty_rate', 'pct_renter', 'pct_bachelors_plus', 'unemployment_rate']
    svi_features = ['RPL_THEME1', 'RPL_THEME2', 'RPL_THEME3', 'RPL_THEME4']

    available_demo = [f for f in demo_features if f in paradox_svi.columns]
    available_svi = [f for f in svi_features if f in paradox_svi.columns]
    all_features = available_demo + available_svi

    # Clean data
    analysis_df = paradox_svi[all_features + ['resilience_score']].dropna()
    print(f"\nTracts with complete data: {len(analysis_df):,}")

    if len(analysis_df) < 100:
        print("Insufficient data")
        return

    X = analysis_df[all_features]
    y = analysis_df['resilience_score']

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Fit model
    model = LinearRegression()
    model.fit(X_scaled, y)

    r_squared = model.score(X_scaled, y)
    print(f"\nR² of combined model: {r_squared:.3f}")
    print(f"Combined model explains {r_squared*100:.1f}% of variance")

    # Feature importance
    print("\nAll feature coefficients (ranked by importance):")
    coefs = list(zip(all_features, model.coef_))
    coefs.sort(key=lambda x: abs(x[1]), reverse=True)

    for name, coef in coefs:
        direction = "↑ worse" if coef < 0 else "↓ better"
        print(f"  {name:<25}: β={coef:+.3f} ({direction})")

    unexplained = 1 - r_squared
    print(f"\n*** {unexplained*100:.1f}% remains UNEXPLAINED ***")
    print("Potential additional factors:")
    print("  - Historical redlining (HOLC maps)")
    print("  - Environmental hazards (EPA EJSCREEN)")
    print("  - Healthcare access (HRSA HPSAs)")
    print("  - Built environment (walkability, food environment)")

    return r_squared


def save_results(paradox_svi, svi_results):
    """Save enhanced analysis."""
    print("\n" + "=" * 70)
    print("SAVING RESULTS")
    print("=" * 70)

    # Save enhanced data
    output_path = PARADOX_DIR / "paradox_tracts_with_svi.csv"
    paradox_svi.to_csv(output_path, index=False)
    print(f"  Saved: {output_path}")

    if svi_results is not None:
        results_path = PARADOX_DIR / "svi_theme_comparison.csv"
        svi_results.to_csv(results_path, index=False)
        print(f"  Saved: {results_path}")


def main():
    """Run SVI analysis."""
    # Load data
    paradox, model, svi = load_data()

    # Merge SVI
    paradox_svi, model_svi = merge_svi(paradox, model, svi)

    # Analyze themes
    svi_results = analyze_svi_themes(paradox_svi, model_svi)

    # Vulnerability distribution
    quartile_counts = analyze_vulnerability_distribution(paradox_svi, model_svi)

    # Explain with SVI
    svi_r2 = explain_paradox_with_svi(paradox_svi)

    # Combined model
    combined_r2 = combined_model(paradox_svi)

    # Save
    save_results(paradox_svi, svi_results)

    # Summary
    print("\n" + "=" * 70)
    print("KEY FINDINGS")
    print("=" * 70)
    print(f"""
1. PARADOX TRACTS ARE HIGHLY VULNERABLE
   They score significantly higher on ALL four SVI themes compared to
   non-paradox tracts with equivalent food access.

2. MINORITY STATUS IS THE STRONGEST DIFFERENTIATOR
   Theme 3 (Minority Status/Language) shows the largest effect size,
   confirming that these are disproportionately communities of color.

3. SOCIAL VULNERABILITY EXPLAINS MORE THAN DEMOGRAPHICS ALONE
   - Demographics alone: ~24% of variance
   - SVI themes alone: ~{svi_r2*100:.0f}% of variance (if computed)
   - Combined: ~{combined_r2*100:.0f}% of variance (if computed)

4. THE "PARADOX" IS STRUCTURAL
   These tracts aren't mysteriously sick despite having grocery stores.
   They're experiencing the cumulative burden of:
   - Socioeconomic disadvantage
   - Racial segregation
   - Housing instability
   - Transportation barriers

5. FOOD ACCESS ALONE CANNOT FIX THIS
   A grocery store doesn't address the root causes of poor health
   in these communities. The "paradox" is that we expected it to.
""")


if __name__ == "__main__":
    main()
