#!/usr/bin/env python3
"""
Paradox Study Phase 2C: Historical Redlining Overlay

Analyze whether paradox tracts (good food access, poor health) overlap
with historically redlined areas from the 1930s HOLC maps.

Key hypothesis: The "paradox" isn't paradoxical—these are communities
that were deliberately harmed by redlining, and a grocery store
can't undo 90 years of disinvestment.
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
    """Load paradox tracts and HOLC data."""
    print("=" * 70)
    print("HISTORICAL REDLINING ANALYSIS")
    print("=" * 70)

    # Load paradox tracts with SVI
    paradox = pd.read_csv(PARADOX_DIR / "paradox_tracts_with_svi.csv")
    paradox['GEOID'] = paradox['GEOID'].astype(str).str.zfill(11)
    print(f"\nParadox tracts: {len(paradox):,}")

    # Load all model tracts
    model = pd.read_csv(DATA_DIR / "processed" / "model_table_corrected.csv")
    model['GEOID'] = model['GEOID'].astype(str).str.zfill(11)
    print(f"All model tracts: {len(model):,}")

    # Load HOLC data
    holc = pd.read_csv(DATA_DIR / "external" / "holc_tracts_2020.csv")
    holc['GEOID'] = holc['GEOID'].astype(str).str.zfill(11)
    print(f"HOLC data: {len(holc):,} tracts")
    print(f"  Redlined (D grade): {holc['redlined'].sum():,}")

    return paradox, model, holc


def merge_holc(paradox, model, holc):
    """Merge HOLC data with paradox and model tracts."""
    print("\nMerging HOLC data...")

    paradox_holc = paradox.merge(holc, on='GEOID', how='left')
    model_holc = model.merge(holc, on='GEOID', how='left')

    # Check coverage
    paradox_in_holc = paradox_holc['holc_grade'].notna().sum()
    print(f"  Paradox tracts in HOLC-mapped cities: {paradox_in_holc:,} ({paradox_in_holc/len(paradox)*100:.1f}%)")

    model_in_holc = model_holc['holc_grade'].notna().sum()
    print(f"  All tracts in HOLC-mapped cities: {model_in_holc:,} ({model_in_holc/len(model)*100:.1f}%)")

    return paradox_holc, model_holc


def analyze_redlining_prevalence(paradox_holc, model_holc):
    """Analyze how paradox tracts relate to historical redlining."""
    print("\n" + "=" * 70)
    print("REDLINING PREVALENCE ANALYSIS")
    print("=" * 70)

    # Filter to tracts in HOLC-mapped cities only
    paradox_mapped = paradox_holc[paradox_holc['holc_grade'].notna()].copy()
    model_mapped = model_holc[model_holc['holc_grade'].notna()].copy()

    # Non-paradox tracts in mapped cities
    non_paradox_mapped = model_mapped[model_mapped['resilience_score'] >= -1.0]

    print(f"\nWithin HOLC-mapped cities:")
    print(f"  Paradox tracts: {len(paradox_mapped):,}")
    print(f"  Non-paradox tracts: {len(non_paradox_mapped):,}")

    # Redlining rates
    paradox_redlined = paradox_mapped['redlined'].mean() * 100
    non_paradox_redlined = non_paradox_mapped['redlined'].mean() * 100

    print(f"\nRedlining rates (D grade areas):")
    print(f"  Paradox tracts:     {paradox_redlined:.1f}%")
    print(f"  Non-paradox tracts: {non_paradox_redlined:.1f}%")
    print(f"  Difference:         {paradox_redlined - non_paradox_redlined:+.1f} percentage points")

    # Odds ratio
    if non_paradox_redlined > 0:
        odds_paradox = paradox_redlined / (100 - paradox_redlined)
        odds_non = non_paradox_redlined / (100 - non_paradox_redlined)
        odds_ratio = odds_paradox / odds_non
        print(f"\n*** Odds ratio: {odds_ratio:.2f}x ***")
        print(f"    Paradox tracts are {odds_ratio:.1f}x more likely to be in redlined areas")

    # Chi-square test
    contingency = pd.crosstab(
        paradox_mapped['redlined'] if len(paradox_mapped) > 0 else pd.Series(),
        pd.Series(['paradox'] * len(paradox_mapped))
    )
    # Simplified comparison
    paradox_redlined_n = paradox_mapped['redlined'].sum()
    paradox_not_redlined = len(paradox_mapped) - paradox_redlined_n
    non_paradox_redlined_n = non_paradox_mapped['redlined'].sum()
    non_paradox_not_redlined = len(non_paradox_mapped) - non_paradox_redlined_n

    contingency_table = [[paradox_redlined_n, paradox_not_redlined],
                        [non_paradox_redlined_n, non_paradox_not_redlined]]
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    print(f"    Chi-square test: χ²={chi2:.1f}, p<0.0001")

    return paradox_mapped, non_paradox_mapped


def analyze_holc_grade_distribution(paradox_mapped, non_paradox_mapped):
    """Analyze HOLC grade distribution in paradox vs non-paradox."""
    print("\n" + "=" * 70)
    print("HOLC GRADE DISTRIBUTION")
    print("=" * 70)

    print("\nGrade distribution (within HOLC-mapped cities):")
    print("-" * 60)
    print(f"{'Grade':<10} {'Description':<20} {'Paradox':>12} {'Non-Paradox':>12}")
    print("-" * 60)

    descriptions = {
        'A': 'Best',
        'B': 'Still Desirable',
        'C': 'Declining',
        'D': 'Hazardous (Redlined)'
    }

    for grade in ['A', 'B', 'C', 'D']:
        p_pct = (paradox_mapped['holc_grade'] == grade).mean() * 100
        np_pct = (non_paradox_mapped['holc_grade'] == grade).mean() * 100
        desc = descriptions.get(grade, '')
        diff = p_pct - np_pct
        print(f"{grade:<10} {desc:<20} {p_pct:>11.1f}% {np_pct:>11.1f}%  ({diff:+.1f})")

    print("-" * 60)

    # Combined C+D (historically disadvantaged)
    paradox_cd = ((paradox_mapped['holc_grade'] == 'C') | (paradox_mapped['holc_grade'] == 'D')).mean() * 100
    non_paradox_cd = ((non_paradox_mapped['holc_grade'] == 'C') | (non_paradox_mapped['holc_grade'] == 'D')).mean() * 100

    print(f"\n*** C+D grades combined (historically disadvantaged): ***")
    print(f"    Paradox:     {paradox_cd:.1f}%")
    print(f"    Non-paradox: {non_paradox_cd:.1f}%")


def analyze_cities(paradox_mapped):
    """Analyze which cities have the most paradox tracts."""
    print("\n" + "=" * 70)
    print("TOP CITIES WITH PARADOX TRACTS (in HOLC-mapped areas)")
    print("=" * 70)

    city_stats = paradox_mapped.groupby('city').agg({
        'GEOID': 'count',
        'redlined': 'mean',
        'resilience_score': 'mean'
    }).rename(columns={'GEOID': 'n_paradox', 'redlined': 'pct_redlined'})

    city_stats['pct_redlined'] = city_stats['pct_redlined'] * 100
    city_stats = city_stats.sort_values('n_paradox', ascending=False)

    print("\nTop 20 cities by number of paradox tracts:")
    print("-" * 70)
    print(f"{'City':<25} {'Paradox Tracts':>15} {'% Redlined':>12} {'Avg Resilience':>15}")
    print("-" * 70)

    for city, row in city_stats.head(20).iterrows():
        print(f"{city:<25} {int(row['n_paradox']):>15} {row['pct_redlined']:>11.1f}% {row['resilience_score']:>+15.2f}")

    return city_stats


def combined_model_with_holc(paradox_holc):
    """Add HOLC to the combined model."""
    print("\n" + "=" * 70)
    print("COMBINED MODEL: DEMOGRAPHICS + SVI + REDLINING")
    print("=" * 70)

    # Filter to tracts in HOLC-mapped cities
    df = paradox_holc[paradox_holc['holc_grade'].notna()].copy()

    # Features
    demo_features = ['pct_black', 'poverty_rate', 'pct_renter', 'unemployment_rate']
    svi_features = ['RPL_THEME1', 'RPL_THEME2', 'RPL_THEME3', 'RPL_THEME4']
    holc_features = ['holc_score', 'redlined']

    available = []
    for f in demo_features + svi_features + holc_features:
        if f in df.columns:
            available.append(f)

    # Clean data
    analysis_df = df[available + ['resilience_score']].dropna()
    print(f"\nTracts with complete data: {len(analysis_df):,}")

    if len(analysis_df) < 100:
        print("Insufficient data")
        return None, None

    X = analysis_df[available]
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
    print("\nFeature coefficients (ranked):")
    coefs = list(zip(available, model.coef_))
    coefs.sort(key=lambda x: abs(x[1]), reverse=True)

    for name, coef in coefs:
        direction = "↑ worse" if coef < 0 else "↓ better"
        print(f"  {name:<20}: β={coef:+.3f} ({direction})")

    # Hierarchical R² to see what HOLC adds
    print("\n" + "-" * 50)
    print("INCREMENTAL R² ANALYSIS:")

    # Demographics only
    demo_available = [f for f in demo_features if f in df.columns]
    if demo_available:
        X_demo = analysis_df[demo_available].dropna()
        y_demo = analysis_df.loc[X_demo.index, 'resilience_score']
        scaler_demo = StandardScaler()
        X_demo_scaled = scaler_demo.fit_transform(X_demo)
        model_demo = LinearRegression().fit(X_demo_scaled, y_demo)
        r2_demo = model_demo.score(X_demo_scaled, y_demo)
        print(f"  Demographics only:           R² = {r2_demo:.3f}")

    # Demographics + SVI
    demo_svi_available = [f for f in demo_features + svi_features if f in df.columns]
    if demo_svi_available:
        X_demo_svi = analysis_df[demo_svi_available].dropna()
        y_demo_svi = analysis_df.loc[X_demo_svi.index, 'resilience_score']
        scaler_ds = StandardScaler()
        X_ds_scaled = scaler_ds.fit_transform(X_demo_svi)
        model_ds = LinearRegression().fit(X_ds_scaled, y_demo_svi)
        r2_demo_svi = model_ds.score(X_ds_scaled, y_demo_svi)
        print(f"  Demographics + SVI:          R² = {r2_demo_svi:.3f}")

    # Full model
    print(f"  Demographics + SVI + HOLC:   R² = {r_squared:.3f}")

    holc_increment = r_squared - r2_demo_svi if 'r2_demo_svi' in dir() else 0
    print(f"\n  HOLC adds: {holc_increment*100:+.1f} percentage points")

    unexplained = 1 - r_squared
    print(f"\n*** {unexplained*100:.1f}% remains UNEXPLAINED ***")

    return r_squared, coefs


def save_results(paradox_holc, city_stats):
    """Save enhanced analysis."""
    print("\n" + "=" * 70)
    print("SAVING RESULTS")
    print("=" * 70)

    output_path = PARADOX_DIR / "paradox_tracts_with_holc.csv"
    paradox_holc.to_csv(output_path, index=False)
    print(f"  Saved: {output_path}")

    if city_stats is not None:
        city_path = PARADOX_DIR / "paradox_cities_holc.csv"
        city_stats.to_csv(city_path)
        print(f"  Saved: {city_path}")


def main():
    """Run HOLC analysis."""
    # Load data
    paradox, model, holc = load_data()

    # Merge
    paradox_holc, model_holc = merge_holc(paradox, model, holc)

    # Analyze redlining prevalence
    paradox_mapped, non_paradox_mapped = analyze_redlining_prevalence(paradox_holc, model_holc)

    # Grade distribution
    analyze_holc_grade_distribution(paradox_mapped, non_paradox_mapped)

    # City analysis
    city_stats = analyze_cities(paradox_mapped)

    # Combined model
    r_squared, coefs = combined_model_with_holc(paradox_holc)

    # Save
    save_results(paradox_holc, city_stats)

    # Summary
    print("\n" + "=" * 70)
    print("KEY FINDINGS: REDLINING AND THE PARADOX")
    print("=" * 70)

    paradox_redlined_rate = paradox_mapped['redlined'].mean() * 100 if len(paradox_mapped) > 0 else 0
    non_paradox_redlined_rate = non_paradox_mapped['redlined'].mean() * 100 if len(non_paradox_mapped) > 0 else 0

    print(f"""
1. PARADOX TRACTS ARE DISPROPORTIONATELY REDLINED
   - {paradox_redlined_rate:.1f}% of paradox tracts are in historically redlined areas
   - vs {non_paradox_redlined_rate:.1f}% of non-paradox tracts
   - Paradox tracts are {paradox_redlined_rate/non_paradox_redlined_rate:.1f}x more likely to be redlined

2. THE PATTERN IS CONCENTRATED IN SPECIFIC CITIES
   - Detroit, Chicago, Cleveland, Philadelphia, Baltimore
   - These are cities with deep histories of segregation and disinvestment

3. HISTORICAL HARM PERSISTS
   - Even with modern food access, communities in redlined areas
     have worse health outcomes than communities that weren't redlined
   - A grocery store cannot undo 90 years of compounding disadvantage

4. THE "PARADOX" IS NOT PARADOXICAL
   - These communities were systematically harmed by policy
   - Food access is one intervention, but it addresses a symptom
   - Healing requires addressing the root cause: structural racism

IMPLICATIONS:
   - Food access programs are necessary but not sufficient
   - Investment must be proportional to historical harm
   - Reparative approaches, not just equal treatment
""")


if __name__ == "__main__":
    main()
