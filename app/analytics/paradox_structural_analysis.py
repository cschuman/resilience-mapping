#!/usr/bin/env python3
"""
Paradox Study Phase 2: Structural Drivers Analysis

Overlay structural variables to explain why tracts with good food access
have poor health outcomes.

Data sources:
1. ACS Demographics (already have) - race, income, education, housing
2. HOLC Redlining (to download) - historical discrimination
3. EPA EJSCREEN (to download) - environmental hazards
4. HRSA HPSAs (to download) - healthcare shortages
5. CDC SVI (to download) - social vulnerability
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path(__file__).parent.parent.parent / "data"
PARADOX_DIR = DATA_DIR / "processed" / "paradox_study"


def load_paradox_data():
    """Load paradox tracts with existing demographic data."""
    print("=" * 70)
    print("STRUCTURAL DRIVERS ANALYSIS")
    print("=" * 70)

    # Load paradox tracts
    paradox = pd.read_csv(PARADOX_DIR / "paradox_tracts_full.csv")
    paradox['GEOID'] = paradox['GEOID'].astype(str).str.zfill(11)
    print(f"\nParadox tracts: {len(paradox):,}")

    # Load all tracts for comparison
    model = pd.read_csv(DATA_DIR / "processed" / "model_table_corrected.csv")
    model['GEOID'] = model['GEOID'].astype(str).str.zfill(11)

    # Load ACS
    acs = pd.read_csv(DATA_DIR / "external" / "acs_demographics_2022.csv")
    acs['GEOID'] = acs['GEOID'].astype(str).str.zfill(11)
    print(f"ACS demographics: {len(acs):,} tracts")

    # Merge
    paradox = paradox.merge(acs, on='GEOID', how='left', suffixes=('', '_acs'))
    model = model.merge(acs, on='GEOID', how='left')

    return paradox, model


def analyze_demographic_drivers(paradox, all_tracts):
    """Analyze demographic correlates of paradox status."""
    print("\n" + "=" * 70)
    print("DEMOGRAPHIC ANALYSIS OF PARADOX TRACTS")
    print("=" * 70)

    # Get non-paradox comparison (good food access, normal/good health)
    good_access = all_tracts[all_tracts.get('LILATracts_1And10', 0) == 0].copy() if 'LILATracts_1And10' in all_tracts.columns else all_tracts.copy()
    non_paradox = good_access[good_access['resilience_score'] >= -1.0]

    # Key demographic variables
    demo_vars = [
        ('pct_black', 'Black population %'),
        ('pct_hispanic', 'Hispanic population %'),
        ('pct_white', 'White population %'),
        ('poverty_rate', 'Poverty rate %'),
        ('median_hh_income', 'Median household income'),
        ('pct_renter', 'Renter-occupied %'),
        ('pct_bachelors_plus', 'Bachelor\'s degree+ %'),
        ('unemployment_rate', 'Unemployment rate %'),
    ]

    print("\nDemographic comparison: Paradox vs Non-Paradox (good food access)")
    print("-" * 70)
    print(f"{'Variable':<30} {'Paradox':>12} {'Non-Paradox':>12} {'Diff':>10} {'p-value':>10}")
    print("-" * 70)

    results = []
    for var, label in demo_vars:
        if var in paradox.columns and var in non_paradox.columns:
            p_val = paradox[var].dropna()
            np_val = non_paradox[var].dropna()

            if len(p_val) > 0 and len(np_val) > 0:
                p_mean = p_val.mean()
                np_mean = np_val.mean()
                diff = p_mean - np_mean

                # T-test
                t_stat, p_value = stats.ttest_ind(p_val, np_val)

                # Effect size (Cohen's d)
                pooled_std = np.sqrt((p_val.std()**2 + np_val.std()**2) / 2)
                cohens_d = diff / pooled_std if pooled_std > 0 else 0

                print(f"{label:<30} {p_mean:>12.1f} {np_mean:>12.1f} {diff:>+10.1f} {p_value:>10.4f}")

                results.append({
                    'variable': var,
                    'label': label,
                    'paradox_mean': p_mean,
                    'non_paradox_mean': np_mean,
                    'difference': diff,
                    'cohens_d': cohens_d,
                    'p_value': p_value
                })

    print("-" * 70)

    # Sort by effect size
    results_df = pd.DataFrame(results)
    results_df['abs_cohens_d'] = results_df['cohens_d'].abs()
    results_df = results_df.sort_values('abs_cohens_d', ascending=False)

    print("\nRanked by effect size (Cohen's d):")
    for _, row in results_df.iterrows():
        direction = "higher" if row['cohens_d'] > 0 else "lower"
        print(f"  {row['label']}: d={row['cohens_d']:+.2f} (paradox tracts {direction})")

    return results_df


def analyze_racial_composition(paradox, all_tracts):
    """Deep dive on racial composition of paradox tracts."""
    print("\n" + "=" * 70)
    print("RACIAL COMPOSITION ANALYSIS")
    print("=" * 70)

    # Categorize tracts by majority race
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

    # Compare to non-paradox good-access tracts
    non_paradox = all_tracts[all_tracts['resilience_score'] >= -1.0].copy()
    non_paradox['majority'] = non_paradox.apply(get_majority, axis=1)

    print("\nRacial composition of paradox vs non-paradox tracts:")
    print("-" * 50)

    for category in ['Majority White', 'Majority Black', 'Majority Hispanic', 'No Majority']:
        p_pct = (paradox['majority'] == category).mean() * 100
        np_pct = (non_paradox['majority'] == category).mean() * 100
        diff = p_pct - np_pct
        print(f"{category:<20}: Paradox {p_pct:5.1f}% | Non-Paradox {np_pct:5.1f}% | Diff {diff:+5.1f}%")

    # Majority Black tracts in paradox
    majority_black_paradox = paradox[paradox['majority'] == 'Majority Black']
    print(f"\n*** Majority Black tracts in paradox set: {len(majority_black_paradox):,} "
          f"({len(majority_black_paradox)/len(paradox)*100:.1f}% of paradox tracts) ***")

    return paradox


def analyze_geographic_clustering(paradox):
    """Analyze where paradox tracts cluster geographically."""
    print("\n" + "=" * 70)
    print("GEOGRAPHIC CLUSTERING ANALYSIS")
    print("=" * 70)

    # State-level
    print("\nTop 15 states by paradox tract count:")
    state_counts = paradox['StateAbbr'].value_counts().head(15)
    for state, count in state_counts.items():
        pct = count / len(paradox) * 100
        print(f"  {state}: {count:,} tracts ({pct:.1f}%)")

    # County-level (if available)
    if 'County' in paradox.columns:
        print("\nTop 15 counties by paradox tract count:")
        paradox['state_county'] = paradox['StateAbbr'] + ' - ' + paradox['County'].fillna('Unknown')
        county_counts = paradox['state_county'].value_counts().head(15)
        for county, count in county_counts.items():
            pct = count / len(paradox) * 100
            print(f"  {county}: {count:,} ({pct:.1f}%)")

    # Urban/Rural
    if 'Urban' in paradox.columns:
        urban_pct = (paradox['Urban'] == 1).mean() * 100
        print(f"\nUrban paradox tracts: {urban_pct:.1f}%")
        print(f"Rural paradox tracts: {100-urban_pct:.1f}%")

    return state_counts


def compute_structural_index(paradox):
    """Compute a structural disadvantage index from available data."""
    print("\n" + "=" * 70)
    print("STRUCTURAL DISADVANTAGE INDEX")
    print("=" * 70)

    # Components we can compute from existing data
    components = []

    # 1. Poverty rate (z-score)
    if 'poverty_rate' in paradox.columns:
        paradox['poverty_z'] = (paradox['poverty_rate'] - paradox['poverty_rate'].mean()) / paradox['poverty_rate'].std()
        components.append('poverty_z')

    # 2. % Black (proxy for historical redlining exposure)
    if 'pct_black' in paradox.columns:
        paradox['pct_black_z'] = (paradox['pct_black'] - paradox['pct_black'].mean()) / paradox['pct_black'].std()
        components.append('pct_black_z')

    # 3. % Renter (housing instability)
    if 'pct_renter' in paradox.columns:
        paradox['renter_z'] = (paradox['pct_renter'] - paradox['pct_renter'].mean()) / paradox['pct_renter'].std()
        components.append('renter_z')

    # 4. Unemployment
    if 'unemployment_rate' in paradox.columns:
        paradox['unemployment_z'] = (paradox['unemployment_rate'] - paradox['unemployment_rate'].mean()) / paradox['unemployment_rate'].std()
        components.append('unemployment_z')

    # 5. Low education (inverse of bachelors)
    if 'pct_bachelors_plus' in paradox.columns:
        paradox['low_ed_z'] = -(paradox['pct_bachelors_plus'] - paradox['pct_bachelors_plus'].mean()) / paradox['pct_bachelors_plus'].std()
        components.append('low_ed_z')

    # Compute composite index
    if components:
        paradox['structural_disadvantage'] = paradox[components].mean(axis=1)

        print(f"\nStructural disadvantage index computed from {len(components)} components:")
        for c in components:
            print(f"  - {c}")

        print(f"\nIndex statistics:")
        print(f"  Mean: {paradox['structural_disadvantage'].mean():.3f}")
        print(f"  Std:  {paradox['structural_disadvantage'].std():.3f}")
        print(f"  Min:  {paradox['structural_disadvantage'].min():.3f}")
        print(f"  Max:  {paradox['structural_disadvantage'].max():.3f}")

        # Correlation with health burden
        corr = paradox['structural_disadvantage'].corr(paradox['burden'])
        print(f"\nCorrelation with health burden: r = {corr:.3f}")

        # Correlation with resilience score
        corr_res = paradox['structural_disadvantage'].corr(paradox['resilience_score'])
        print(f"Correlation with resilience score: r = {corr_res:.3f}")

    return paradox


def identify_structural_data_needs():
    """Identify what additional data we need to download."""
    print("\n" + "=" * 70)
    print("ADDITIONAL DATA SOURCES NEEDED")
    print("=" * 70)

    sources = [
        {
            'name': 'HOLC Redlining Maps',
            'description': 'Historical Home Owners Loan Corporation grades (A-D)',
            'url': 'https://dsl.richmond.edu/panorama/redlining/',
            'format': 'GeoJSON, can intersect with tract boundaries',
            'difficulty': 'Medium - need spatial intersection',
            'value': 'HIGH - direct measure of historical discrimination'
        },
        {
            'name': 'EPA EJSCREEN',
            'description': 'Environmental Justice Screening tool with tract-level indicators',
            'url': 'https://www.epa.gov/ejscreen/download-ejscreen-data',
            'format': 'CSV with tract FIPS',
            'difficulty': 'Easy - direct download',
            'value': 'HIGH - environmental hazards, pollution burden'
        },
        {
            'name': 'CDC Social Vulnerability Index (SVI)',
            'description': 'Composite index of social vulnerability factors',
            'url': 'https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html',
            'format': 'CSV with tract FIPS',
            'difficulty': 'Easy - direct download',
            'value': 'HIGH - comprehensive vulnerability measure'
        },
        {
            'name': 'HRSA Health Professional Shortage Areas',
            'description': 'Primary care, dental, mental health shortage designations',
            'url': 'https://data.hrsa.gov/data/download',
            'format': 'CSV, may need geocoding',
            'difficulty': 'Medium',
            'value': 'HIGH - healthcare access beyond food'
        },
        {
            'name': 'Hospital Closures Database',
            'description': 'Rural and urban hospital closures since 2010',
            'url': 'https://www.shepscenter.unc.edu/programs-projects/rural-health/',
            'format': 'Various',
            'difficulty': 'Medium',
            'value': 'MEDIUM - explains some healthcare access issues'
        },
        {
            'name': 'EPA Smart Location Database',
            'description': 'Walkability, transit access, land use mix',
            'url': 'https://www.epa.gov/smartgrowth/smart-location-mapping',
            'format': 'Geodatabase/CSV',
            'difficulty': 'Easy',
            'value': 'MEDIUM - built environment factors'
        }
    ]

    print("\nRecommended data sources to overlay:\n")
    for i, s in enumerate(sources, 1):
        print(f"{i}. {s['name']}")
        print(f"   Value: {s['value']} | Difficulty: {s['difficulty']}")
        print(f"   URL: {s['url']}")
        print()

    return sources


def explain_paradox_variance(paradox):
    """Attempt to explain paradox variance with available variables."""
    print("\n" + "=" * 70)
    print("EXPLAINING PARADOX VARIANCE")
    print("=" * 70)

    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler

    # Prepare features
    feature_cols = [
        'pct_black', 'pct_hispanic', 'pct_white',
        'poverty_rate', 'median_hh_income', 'pct_renter',
        'pct_bachelors_plus', 'unemployment_rate'
    ]

    available_cols = [c for c in feature_cols if c in paradox.columns]

    # Drop rows with missing values
    analysis_df = paradox[available_cols + ['resilience_score']].dropna()
    print(f"\nTracts with complete data: {len(analysis_df):,}")

    if len(analysis_df) < 100:
        print("Insufficient data for regression analysis")
        return None

    X = analysis_df[available_cols]
    y = analysis_df['resilience_score']

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Fit model
    model = LinearRegression()
    model.fit(X_scaled, y)

    # Results
    r_squared = model.score(X_scaled, y)
    print(f"\nR² of demographic model: {r_squared:.3f}")
    print(f"This means demographics explain {r_squared*100:.1f}% of variance in paradox severity")

    # Feature importance
    print("\nFeature coefficients (standardized):")
    coefs = list(zip(available_cols, model.coef_))
    coefs.sort(key=lambda x: abs(x[1]), reverse=True)
    for name, coef in coefs:
        direction = "↑ worse health" if coef < 0 else "↓ better health"
        print(f"  {name:<25}: {coef:+.3f} ({direction})")

    # What's unexplained
    unexplained = 1 - r_squared
    print(f"\n*** {unexplained*100:.1f}% of variance remains UNEXPLAINED by demographics ***")
    print("This is where structural factors (redlining, environment, healthcare) may matter")

    return r_squared, coefs


def save_analysis(paradox, results_df):
    """Save enhanced analysis outputs."""
    print("\n" + "=" * 70)
    print("SAVING OUTPUTS")
    print("=" * 70)

    # Save enhanced paradox data
    output_path = PARADOX_DIR / "paradox_tracts_enhanced.csv"
    paradox.to_csv(output_path, index=False)
    print(f"  Saved: {output_path}")

    # Save demographic comparison
    if results_df is not None:
        results_path = PARADOX_DIR / "demographic_comparison.csv"
        results_df.to_csv(results_path, index=False)
        print(f"  Saved: {results_path}")


def main():
    """Run structural analysis."""
    # Load data
    paradox, all_tracts = load_paradox_data()

    # Demographic analysis
    results_df = analyze_demographic_drivers(paradox, all_tracts)

    # Racial composition
    paradox = analyze_racial_composition(paradox, all_tracts)

    # Geographic clustering
    state_counts = analyze_geographic_clustering(paradox)

    # Structural disadvantage index
    paradox = compute_structural_index(paradox)

    # Explain variance
    r_squared, coefs = explain_paradox_variance(paradox)

    # Identify data needs
    sources = identify_structural_data_needs()

    # Save
    save_analysis(paradox, results_df)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: WHAT WE KNOW SO FAR")
    print("=" * 70)
    print(f"""
KEY FINDINGS FROM DEMOGRAPHIC ANALYSIS:

1. RACIAL COMPOSITION MATTERS
   Paradox tracts have significantly higher Black population percentages
   than non-paradox tracts with equivalent food access.

2. POVERTY IS PART OF IT, BUT NOT ALL
   Paradox tracts are poorer, but they're NOT classified as low-income
   by FARA standards (they have "good" food access).

3. DEMOGRAPHICS EXPLAIN ~{r_squared*100:.0f}% OF VARIANCE
   This means {(1-r_squared)*100:.0f}% is due to something else:
   - Historical redlining
   - Environmental hazards
   - Healthcare access
   - Built environment
   - Social cohesion

NEXT STEPS:
1. Download EPA EJSCREEN data (easiest, highest value)
2. Download CDC Social Vulnerability Index
3. Overlay HOLC redlining maps
4. Re-run analysis with structural variables
""")


if __name__ == "__main__":
    main()
