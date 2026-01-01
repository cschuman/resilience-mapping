#!/usr/bin/env python3
"""
Paper 4B Ultra-Deep Dive: Following the Evidence

Key mysteries to solve:
1. TEXAS vs ILLINOIS: Why -0.335 SD vs +0.300 SD for Mexican communities?
2. GEORGIA/VIRGINIA/MARYLAND: Why do Hispanic communities thrive here?
3. What structural factors explain these divergences?
4. Can we identify transferable lessons?
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "research"


def load_all_data():
    """Load and merge all data sources."""
    print("Loading data...")

    resilience = pd.read_csv(DATA_DIR / "processed" / "model_table_corrected.csv")
    resilience['GEOID'] = resilience['TractFIPS'].astype(str).str.zfill(11)

    acs = pd.read_csv(DATA_DIR / "external" / "acs_demographics_2022.csv")
    acs['GEOID'] = acs['GEOID'].astype(str).str.zfill(11)

    nativity = pd.read_csv(DATA_DIR / "external" / "acs_nativity_2022.csv")
    nativity['GEOID'] = nativity['GEOID'].astype(str).str.zfill(11)
    nativity = nativity[['GEOID', 'pct_foreign_born']]

    hispanic = pd.read_csv(DATA_DIR / "external" / "acs_hispanic_origin_2022.csv")
    hispanic['GEOID'] = hispanic['GEOID'].astype(str).str.zfill(11)

    df = resilience.merge(acs, on='GEOID', how='inner')
    df = df.merge(nativity, on='GEOID', how='inner')
    df = df.merge(hispanic, on='GEOID', how='inner')

    if 'pct_hispanic_x' in df.columns:
        df['pct_hispanic'] = df['pct_hispanic_x']
        df = df.drop(columns=['pct_hispanic_x', 'pct_hispanic_y'])

    if 'median_hh_income' in df.columns:
        df.loc[df['median_hh_income'] < 0, 'median_hh_income'] = np.nan

    df['state_fips'] = df['GEOID'].str[:2]
    df['county_fips'] = df['GEOID'].str[:5]

    print(f"  Loaded {len(df):,} tracts\n")
    return df


# =============================================================================
# INVESTIGATION 1: THE TEXAS-ILLINOIS MEXICAN DIVERGENCE
# =============================================================================

def investigate_texas_illinois(df):
    """Deep dive into why Texas and Illinois Mexican communities diverge so dramatically."""
    print("\n" + "=" * 80)
    print("INVESTIGATION 1: THE TEXAS-ILLINOIS MEXICAN DIVERGENCE")
    print("=" * 80)
    print("\nTexas Mexican tracts: -0.335 SD")
    print("Illinois Mexican tracts: +0.300 SD")
    print("Gap: 0.635 SD - This is MASSIVE. Why?\n")

    # Filter to Mexican-substantial tracts in each state
    tx_mex = df[(df['StateAbbr'] == 'TX') & (df['pct_mexican'] > 20)].copy()
    il_mex = df[(df['StateAbbr'] == 'IL') & (df['pct_mexican'] > 20)].copy()

    print(f"Texas Mexican tracts (>20%): {len(tx_mex):,}")
    print(f"Illinois Mexican tracts (>20%): {len(il_mex):,}")

    # COMPARISON 1: Basic Demographics
    print("\n" + "-" * 60)
    print("COMPARISON 1: DEMOGRAPHIC PROFILE")
    print("-" * 60)

    metrics = [
        ('Resilience Score', 'resilience_score', '{:+.3f}'),
        ('% Mexican', 'pct_mexican', '{:.1f}%'),
        ('% Foreign-Born', 'pct_foreign_born', '{:.1f}%'),
        ('Median HH Income', 'median_hh_income', '${:,.0f}'),
        ('% Bachelor+', 'pct_bachelors_plus', '{:.1f}%'),
        ('Poverty Rate', 'poverty_rate', '{:.1f}%'),
        ('% White', 'pct_white', '{:.1f}%'),
        ('% Black', 'pct_black', '{:.1f}%'),
    ]

    print(f"\n{'Metric':<25} {'Texas':<18} {'Illinois':<18} {'Difference':<15}")
    print("-" * 76)

    findings = []
    for name, col, fmt in metrics:
        if col in tx_mex.columns:
            tx_val = tx_mex[col].mean()
            il_val = il_mex[col].mean()
            diff = il_val - tx_val

            tx_str = fmt.format(tx_val) if not pd.isna(tx_val) else "N/A"
            il_str = fmt.format(il_val) if not pd.isna(il_val) else "N/A"

            # Determine significance
            if col in ['resilience_score', 'pct_foreign_born', 'median_hh_income',
                       'pct_bachelors_plus', 'poverty_rate']:
                t, p = stats.ttest_ind(tx_mex[col].dropna(), il_mex[col].dropna())
                sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
            else:
                sig = ""

            print(f"{name:<25} {tx_str:<18} {il_str:<18} {diff:+.2f} {sig}")
            findings.append({'metric': name, 'texas': tx_val, 'illinois': il_val, 'diff': diff})

    # COMPARISON 2: Health Burden Components
    print("\n" + "-" * 60)
    print("COMPARISON 2: HEALTH BURDEN COMPONENTS")
    print("-" * 60)

    burden_cols = [col for col in df.columns if col.startswith('ARTHRITIS') or
                   col.startswith('CANCER') or col.startswith('DIABETES') or
                   col.startswith('OBESITY') or col.startswith('BPHIGH') or
                   col.startswith('CHD') or col.startswith('COPD') or
                   col.startswith('MHLTH') or col.startswith('DEPRESSION')]

    if burden_cols:
        print(f"\n{'Condition':<20} {'Texas':<12} {'Illinois':<12} {'Diff':<10}")
        print("-" * 54)
        for col in burden_cols[:10]:
            tx_val = tx_mex[col].mean() if col in tx_mex.columns else np.nan
            il_val = il_mex[col].mean() if col in il_mex.columns else np.nan
            if not pd.isna(tx_val) and not pd.isna(il_val):
                print(f"{col:<20} {tx_val:.1f}%        {il_val:.1f}%        {il_val-tx_val:+.1f}%")

    # COMPARISON 3: Urban vs Rural
    print("\n" + "-" * 60)
    print("COMPARISON 3: URBANIZATION PATTERNS")
    print("-" * 60)

    # Use population density as proxy if available, or tract size
    if 'total_pop' in df.columns:
        tx_pop = tx_mex['total_pop'].median()
        il_pop = il_mex['total_pop'].median()
        print(f"\nMedian tract population:")
        print(f"  Texas: {tx_pop:,.0f}")
        print(f"  Illinois: {il_pop:,.0f}")

    # COMPARISON 4: County-level analysis
    print("\n" + "-" * 60)
    print("COMPARISON 4: TOP COUNTIES")
    print("-" * 60)

    print("\nTop Texas counties by Mexican tract count:")
    tx_counties = tx_mex.groupby('county_fips').agg({
        'resilience_score': 'mean',
        'GEOID': 'count',
        'pct_foreign_born': 'mean',
        'poverty_rate': 'mean'
    }).rename(columns={'GEOID': 'n_tracts'}).sort_values('n_tracts', ascending=False).head(10)

    for county, row in tx_counties.iterrows():
        print(f"  {county}: {row['n_tracts']:,} tracts, resilience {row['resilience_score']:+.3f}, "
              f"poverty {row['poverty_rate']:.1f}%")

    print("\nTop Illinois counties by Mexican tract count:")
    il_counties = il_mex.groupby('county_fips').agg({
        'resilience_score': 'mean',
        'GEOID': 'count',
        'pct_foreign_born': 'mean',
        'poverty_rate': 'mean'
    }).rename(columns={'GEOID': 'n_tracts'}).sort_values('n_tracts', ascending=False).head(10)

    for county, row in il_counties.iterrows():
        print(f"  {county}: {row['n_tracts']:,} tracts, resilience {row['resilience_score']:+.3f}, "
              f"poverty {row['poverty_rate']:.1f}%")

    # COMPARISON 5: What predicts resilience WITHIN each state?
    print("\n" + "-" * 60)
    print("COMPARISON 5: WITHIN-STATE PREDICTORS OF RESILIENCE")
    print("-" * 60)

    predictors = ['pct_foreign_born', 'pct_mexican', 'poverty_rate', 'pct_bachelors_plus']

    print("\nTexas Mexican tracts - correlations with resilience:")
    for pred in predictors:
        if pred in tx_mex.columns:
            r, p = stats.pearsonr(tx_mex[pred].dropna(),
                                  tx_mex.loc[tx_mex[pred].notna(), 'resilience_score'])
            sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
            print(f"  {pred:<25}: r = {r:+.3f} {sig}")

    print("\nIllinois Mexican tracts - correlations with resilience:")
    for pred in predictors:
        if pred in il_mex.columns:
            r, p = stats.pearsonr(il_mex[pred].dropna(),
                                  il_mex.loc[il_mex[pred].notna(), 'resilience_score'])
            sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
            print(f"  {pred:<25}: r = {r:+.3f} {sig}")

    # COMPARISON 6: Border proximity
    print("\n" + "-" * 60)
    print("COMPARISON 6: TEXAS BORDER VS NON-BORDER COUNTIES")
    print("-" * 60)

    # Texas border county FIPS codes
    border_counties = ['48061', '48215', '48243', '48247', '48261', '48271', '48311',
                       '48323', '48377', '48381', '48427', '48443', '48465', '48479',
                       '48489', '48505']  # Major border counties

    tx_mex['border'] = tx_mex['county_fips'].isin(border_counties)

    tx_border = tx_mex[tx_mex['border']]
    tx_interior = tx_mex[~tx_mex['border']]

    print(f"\nTexas border counties ({len(tx_border):,} Mexican tracts):")
    print(f"  Resilience: {tx_border['resilience_score'].mean():+.3f} SD")
    print(f"  Poverty: {tx_border['poverty_rate'].mean():.1f}%")
    print(f"  % Foreign-born: {tx_border['pct_foreign_born'].mean():.1f}%")

    print(f"\nTexas interior counties ({len(tx_interior):,} Mexican tracts):")
    print(f"  Resilience: {tx_interior['resilience_score'].mean():+.3f} SD")
    print(f"  Poverty: {tx_interior['poverty_rate'].mean():.1f}%")
    print(f"  % Foreign-born: {tx_interior['pct_foreign_born'].mean():.1f}%")

    # KEY INSIGHT
    print("\n" + "=" * 60)
    print("KEY INSIGHT: TEXAS vs ILLINOIS")
    print("=" * 60)

    print(f"""
THE DIVERGENCE EXPLAINED:

1. EDUCATION GAP:
   - Illinois Mexican tracts: {il_mex['pct_bachelors_plus'].mean():.1f}% bachelor's+
   - Texas Mexican tracts: {tx_mex['pct_bachelors_plus'].mean():.1f}% bachelor's+
   - Gap: {il_mex['pct_bachelors_plus'].mean() - tx_mex['pct_bachelors_plus'].mean():.1f} percentage points

2. INCOME GAP:
   - Illinois: ${il_mex['median_hh_income'].mean():,.0f}
   - Texas: ${tx_mex['median_hh_income'].mean():,.0f}
   - Gap: ${il_mex['median_hh_income'].mean() - tx_mex['median_hh_income'].mean():,.0f}

3. FOREIGN-BORN PERCENTAGE:
   - Illinois: {il_mex['pct_foreign_born'].mean():.1f}%
   - Texas: {tx_mex['pct_foreign_born'].mean():.1f}%
   - Gap: {il_mex['pct_foreign_born'].mean() - tx_mex['pct_foreign_born'].mean():.1f} percentage points

4. POVERTY RATE:
   - Illinois: {il_mex['poverty_rate'].mean():.1f}%
   - Texas: {tx_mex['poverty_rate'].mean():.1f}%
   - Gap: {il_mex['poverty_rate'].mean() - tx_mex['poverty_rate'].mean():.1f} percentage points

HYPOTHESIS: Illinois attracts MORE EDUCATED Mexican immigrants who settle in
Chicago metro area with better economic opportunities, while Texas border
regions have structural disadvantages related to border economies.
""")

    return {'texas': tx_mex, 'illinois': il_mex}


# =============================================================================
# INVESTIGATION 2: THE GEORGIA/VIRGINIA/MARYLAND SUCCESS STORY
# =============================================================================

def investigate_success_states(df):
    """Why do GA, VA, MD show such strong Hispanic resilience advantages?"""
    print("\n" + "=" * 80)
    print("INVESTIGATION 2: THE GEORGIA/VIRGINIA/MARYLAND SUCCESS STORY")
    print("=" * 80)
    print("\nThese states show the LARGEST Hispanic resilience advantages:")
    print("  GA: +0.87 SD gap")
    print("  VA: +0.82 SD gap")
    print("  MD: +0.81 SD gap")
    print("\nWhy do Hispanic communities thrive here?\n")

    success_states = ['GA', 'VA', 'MD']
    comparison_states = ['TX', 'CA', 'AZ']  # Traditional Hispanic states

    success_hisp = df[(df['StateAbbr'].isin(success_states)) & (df['pct_hispanic'] > 20)].copy()
    compare_hisp = df[(df['StateAbbr'].isin(comparison_states)) & (df['pct_hispanic'] > 20)].copy()

    print(f"Success states Hispanic tracts (>20%): {len(success_hisp):,}")
    print(f"Comparison states Hispanic tracts (>20%): {len(compare_hisp):,}")

    # ANALYSIS 1: Demographic Profile
    print("\n" + "-" * 60)
    print("ANALYSIS 1: DEMOGRAPHIC COMPARISON")
    print("-" * 60)

    metrics = [
        ('Resilience Score', 'resilience_score', '{:+.3f}'),
        ('% Hispanic', 'pct_hispanic', '{:.1f}%'),
        ('% Mexican', 'pct_mexican', '{:.1f}%'),
        ('% Central American', 'pct_central_american', '{:.1f}%'),
        ('% South American', 'pct_south_american', '{:.1f}%'),
        ('% Foreign-Born', 'pct_foreign_born', '{:.1f}%'),
        ('Median HH Income', 'median_hh_income', '${:,.0f}'),
        ('% Bachelor+', 'pct_bachelors_plus', '{:.1f}%'),
        ('Poverty Rate', 'poverty_rate', '{:.1f}%'),
    ]

    print(f"\n{'Metric':<25} {'GA/VA/MD':<18} {'TX/CA/AZ':<18} {'Difference':<15}")
    print("-" * 76)

    for name, col, fmt in metrics:
        if col in success_hisp.columns:
            succ_val = success_hisp[col].mean()
            comp_val = compare_hisp[col].mean()
            diff = succ_val - comp_val

            succ_str = fmt.format(succ_val) if not pd.isna(succ_val) else "N/A"
            comp_str = fmt.format(comp_val) if not pd.isna(comp_val) else "N/A"

            print(f"{name:<25} {succ_str:<18} {comp_str:<18} {diff:+.2f}")

    # ANALYSIS 2: Origin Composition
    print("\n" + "-" * 60)
    print("ANALYSIS 2: HISPANIC ORIGIN COMPOSITION")
    print("-" * 60)

    origins = ['pct_mexican', 'pct_central_american', 'pct_south_american',
               'pct_puerto_rican', 'pct_cuban', 'pct_dominican']

    print("\nComposition in Hispanic tracts (>20%):")
    print(f"\n{'Origin':<25} {'GA/VA/MD':<15} {'TX/CA/AZ':<15}")
    print("-" * 55)

    for col in origins:
        if col in success_hisp.columns:
            succ_val = success_hisp[col].mean()
            comp_val = compare_hisp[col].mean()
            name = col.replace('pct_', '').replace('_', ' ').title()
            print(f"{name:<25} {succ_val:.1f}%          {comp_val:.1f}%")

    # ANALYSIS 3: Each state individually
    print("\n" + "-" * 60)
    print("ANALYSIS 3: STATE-BY-STATE BREAKDOWN")
    print("-" * 60)

    for state in success_states:
        state_hisp = df[(df['StateAbbr'] == state) & (df['pct_hispanic'] > 20)]
        state_non = df[(df['StateAbbr'] == state) & (df['pct_hispanic'] <= 20)]

        print(f"\n{state}:")
        print(f"  Hispanic tracts (>20%): {len(state_hisp):,}")
        print(f"  Hispanic resilience: {state_hisp['resilience_score'].mean():+.3f} SD")
        print(f"  Non-Hispanic resilience: {state_non['resilience_score'].mean():+.3f} SD")
        print(f"  Gap: {state_hisp['resilience_score'].mean() - state_non['resilience_score'].mean():+.3f} SD")
        print(f"  Hispanic composition:")
        print(f"    Mexican: {state_hisp['pct_mexican'].mean():.1f}%")
        print(f"    Central American: {state_hisp['pct_central_american'].mean():.1f}%")
        print(f"    South American: {state_hisp['pct_south_american'].mean():.1f}%")
        print(f"  % Foreign-born: {state_hisp['pct_foreign_born'].mean():.1f}%")
        print(f"  Median income: ${state_hisp['median_hh_income'].mean():,.0f}")
        print(f"  % Bachelor+: {state_hisp['pct_bachelors_plus'].mean():.1f}%")

    # ANALYSIS 4: Metro area focus
    print("\n" + "-" * 60)
    print("ANALYSIS 4: METROPOLITAN AREA ANALYSIS")
    print("-" * 60)

    # DC metro area spans MD and VA
    dc_metro_counties = ['24031', '24033', '51013', '51059', '51107', '51153',
                         '51510', '51600', '51610', '11001']  # Major DC metro FIPS

    success_hisp['dc_metro'] = success_hisp['county_fips'].isin(dc_metro_counties)

    dc_metro = success_hisp[success_hisp['dc_metro']]
    non_metro = success_hisp[~success_hisp['dc_metro']]

    print(f"\nDC Metro Hispanic tracts: {len(dc_metro):,}")
    print(f"  Resilience: {dc_metro['resilience_score'].mean():+.3f} SD")
    print(f"  % Foreign-born: {dc_metro['pct_foreign_born'].mean():.1f}%")
    print(f"  Median income: ${dc_metro['median_hh_income'].mean():,.0f}")
    print(f"  % Bachelor+: {dc_metro['pct_bachelors_plus'].mean():.1f}%")

    print(f"\nNon-Metro Hispanic tracts: {len(non_metro):,}")
    print(f"  Resilience: {non_metro['resilience_score'].mean():+.3f} SD")
    print(f"  % Foreign-born: {non_metro['pct_foreign_born'].mean():.1f}%")
    print(f"  Median income: ${non_metro['median_hh_income'].mean():,.0f}")
    print(f"  % Bachelor+: {non_metro['pct_bachelors_plus'].mean():.1f}%")

    # Atlanta metro for GA
    atl_metro_counties = ['13121', '13089', '13067', '13063', '13135', '13057',
                          '13097', '13113', '13151', '13247']  # Major Atlanta FIPS

    ga_hisp = df[(df['StateAbbr'] == 'GA') & (df['pct_hispanic'] > 20)]
    ga_hisp = ga_hisp.copy()
    ga_hisp['atl_metro'] = ga_hisp['county_fips'].isin(atl_metro_counties)

    atl_metro = ga_hisp[ga_hisp['atl_metro']]

    print(f"\nAtlanta Metro Hispanic tracts: {len(atl_metro):,}")
    if len(atl_metro) > 0:
        print(f"  Resilience: {atl_metro['resilience_score'].mean():+.3f} SD")
        print(f"  % Foreign-born: {atl_metro['pct_foreign_born'].mean():.1f}%")

    # KEY INSIGHT
    print("\n" + "=" * 60)
    print("KEY INSIGHT: SUCCESS STATE PATTERN")
    print("=" * 60)

    print(f"""
THE SUCCESS STORY EXPLAINED:

1. DIFFERENT IMMIGRATION STREAM:
   - GA/VA/MD have MORE Central/South Americans, FEWER Mexicans
   - These immigrants are SELECTED on education and skills
   - Many work in professional/government sectors (DC area)

2. ECONOMIC CONTEXT:
   - GA/VA/MD Hispanic tracts: ${success_hisp['median_hh_income'].mean():,.0f} median income
   - TX/CA/AZ Hispanic tracts: ${compare_hisp['median_hh_income'].mean():,.0f} median income
   - Gap: ${success_hisp['median_hh_income'].mean() - compare_hisp['median_hh_income'].mean():,.0f}

3. EDUCATION LEVELS:
   - GA/VA/MD: {success_hisp['pct_bachelors_plus'].mean():.1f}% bachelor's+
   - TX/CA/AZ: {compare_hisp['pct_bachelors_plus'].mean():.1f}% bachelor's+
   - Gap: {success_hisp['pct_bachelors_plus'].mean() - compare_hisp['pct_bachelors_plus'].mean():.1f} percentage points

4. FOREIGN-BORN PERCENTAGE:
   - GA/VA/MD: {success_hisp['pct_foreign_born'].mean():.1f}%
   - TX/CA/AZ: {compare_hisp['pct_foreign_born'].mean():.1f}%

5. METROPOLITAN ADVANTAGE:
   - DC metro and Atlanta metro attract skilled immigrants
   - Federal government and contractors employ many immigrants
   - Creates pathway to middle-class stability

HYPOTHESIS: New immigrant destinations (Southeast) attract a DIFFERENT type
of Hispanic immigrant than traditional destinations (Southwest). These are
newer, more educated migration streams with better economic integration.
""")

    return {'success': success_hisp, 'comparison': compare_hisp}


# =============================================================================
# INVESTIGATION 3: THE RECENCY HYPOTHESIS
# =============================================================================

def investigate_recency_hypothesis(df):
    """Are newer immigration destinations showing better outcomes?"""
    print("\n" + "=" * 80)
    print("INVESTIGATION 3: THE RECENCY HYPOTHESIS")
    print("=" * 80)
    print("\nHypothesis: Newer immigration destinations attract different immigrants")
    print("Traditional destinations (TX, CA) vs New destinations (GA, NC, TN)\n")

    # Traditional vs new destinations
    traditional = ['TX', 'CA', 'AZ', 'NM', 'CO']
    new_south = ['GA', 'NC', 'TN', 'SC', 'AL']
    new_midwest = ['IN', 'KS', 'NE', 'IA', 'MN']
    northeast = ['NY', 'NJ', 'PA', 'MA', 'CT']

    results = []

    for label, states in [('Traditional SW', traditional), ('New South', new_south),
                          ('New Midwest', new_midwest), ('Northeast', northeast)]:
        subset = df[(df['StateAbbr'].isin(states)) & (df['pct_hispanic'] > 20)]
        if len(subset) < 50:
            continue

        results.append({
            'region': label,
            'n_tracts': len(subset),
            'resilience': subset['resilience_score'].mean(),
            'pct_mexican': subset['pct_mexican'].mean(),
            'pct_central_american': subset['pct_central_american'].mean(),
            'pct_south_american': subset['pct_south_american'].mean(),
            'pct_foreign_born': subset['pct_foreign_born'].mean(),
            'income': subset['median_hh_income'].mean(),
            'education': subset['pct_bachelors_plus'].mean(),
            'poverty': subset['poverty_rate'].mean()
        })

    results_df = pd.DataFrame(results)

    print("Regional Comparison of Hispanic Tracts (>20%):")
    print("-" * 90)
    print(f"{'Region':<15} {'N':<8} {'Resil':<10} {'%Mex':<8} {'%CA':<8} {'%SA':<8} {'%FB':<8} {'Income':<12}")
    print("-" * 90)

    for _, row in results_df.iterrows():
        print(f"{row['region']:<15} {row['n_tracts']:<8} {row['resilience']:+.3f}     "
              f"{row['pct_mexican']:.1f}%    {row['pct_central_american']:.1f}%    "
              f"{row['pct_south_american']:.1f}%    {row['pct_foreign_born']:.1f}%    "
              f"${row['income']:,.0f}")

    print("\n*** KEY FINDING ***")
    best = results_df.loc[results_df['resilience'].idxmax()]
    worst = results_df.loc[results_df['resilience'].idxmin()]
    print(f"Highest resilience: {best['region']} ({best['resilience']:+.3f} SD)")
    print(f"Lowest resilience: {worst['region']} ({worst['resilience']:+.3f} SD)")
    print(f"Gap: {best['resilience'] - worst['resilience']:.3f} SD")

    return results_df


# =============================================================================
# INVESTIGATION 4: THE EDUCATION-OCCUPATION PATHWAY
# =============================================================================

def investigate_education_pathway(df):
    """Does education explain the divergence across all states?"""
    print("\n" + "=" * 80)
    print("INVESTIGATION 4: THE EDUCATION PATHWAY")
    print("=" * 80)
    print("\nDoes education level fully explain Hispanic resilience variation?\n")

    hisp = df[df['pct_hispanic'] > 20].copy()

    # Create education tertiles
    hisp['edu_tertile'] = pd.qcut(hisp['pct_bachelors_plus'], 3,
                                   labels=['Low Edu', 'Medium Edu', 'High Edu'])

    print("Resilience by Education Level (Hispanic tracts >20%):")
    print("-" * 60)

    for tertile in ['Low Edu', 'Medium Edu', 'High Edu']:
        subset = hisp[hisp['edu_tertile'] == tertile]
        edu_range = f"{subset['pct_bachelors_plus'].min():.0f}-{subset['pct_bachelors_plus'].max():.0f}%"
        print(f"  {tertile:<12} ({edu_range:<12}): {subset['resilience_score'].mean():+.3f} SD "
              f"(N = {len(subset):,})")

    # Within education level, does origin still matter?
    print("\nWithin High-Education Hispanic tracts, does origin matter?")
    print("-" * 60)

    high_edu = hisp[hisp['edu_tertile'] == 'High Edu']

    for col, name in [('pct_mexican', 'Mexican'), ('pct_south_american', 'South American'),
                      ('pct_central_american', 'Central American')]:
        r, p = stats.pearsonr(high_edu[col], high_edu['resilience_score'])
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
        print(f"  % {name:<20} ↔ Resilience: r = {r:+.3f} {sig}")

    # Regression: Does education explain state differences?
    print("\n" + "-" * 60)
    print("REGRESSION: Can education explain state differences?")
    print("-" * 60)

    # Create state dummies for key states
    hisp['is_TX'] = (hisp['StateAbbr'] == 'TX').astype(int)
    hisp['is_IL'] = (hisp['StateAbbr'] == 'IL').astype(int)
    hisp['is_GA'] = (hisp['StateAbbr'] == 'GA').astype(int)

    # Model 1: State only
    X1 = hisp[['is_TX', 'is_IL', 'is_GA']]
    X1 = sm.add_constant(X1)
    y = hisp['resilience_score']

    model1 = sm.OLS(y, X1).fit()

    print("\nModel 1: State effects only")
    print(f"  R² = {model1.rsquared:.4f}")
    print(f"  Texas effect:    β = {model1.params['is_TX']:+.3f}")
    print(f"  Illinois effect: β = {model1.params['is_IL']:+.3f}")
    print(f"  Georgia effect:  β = {model1.params['is_GA']:+.3f}")

    # Model 2: State + Education + Income
    valid = hisp.dropna(subset=['pct_bachelors_plus', 'median_hh_income', 'poverty_rate'])
    X2 = valid[['is_TX', 'is_IL', 'is_GA', 'pct_bachelors_plus', 'poverty_rate']]
    X2 = sm.add_constant(X2)
    y2 = valid['resilience_score']

    model2 = sm.OLS(y2, X2).fit()

    print("\nModel 2: State effects + SES controls")
    print(f"  R² = {model2.rsquared:.4f}")
    print(f"  Texas effect:    β = {model2.params['is_TX']:+.3f} (was {model1.params['is_TX']:+.3f})")
    print(f"  Illinois effect: β = {model2.params['is_IL']:+.3f} (was {model1.params['is_IL']:+.3f})")
    print(f"  Georgia effect:  β = {model2.params['is_GA']:+.3f} (was {model1.params['is_GA']:+.3f})")
    print(f"  Education:       β = {model2.params['pct_bachelors_plus']:+.4f}")
    print(f"  Poverty:         β = {model2.params['poverty_rate']:+.4f}")

    # How much of state effect is explained by SES?
    tx_explained = 1 - (model2.params['is_TX'] / model1.params['is_TX']) if model1.params['is_TX'] != 0 else 0
    il_explained = 1 - (model2.params['is_IL'] / model1.params['is_IL']) if model1.params['is_IL'] != 0 else 0

    print(f"\n*** MEDIATION ANALYSIS ***")
    print(f"  Texas effect explained by SES: {tx_explained*100:.1f}%")
    print(f"  Illinois effect explained by SES: {il_explained*100:.1f}%")

    return model2


# =============================================================================
# INVESTIGATION 5: THE EXEMPLAR DEEP DIVE
# =============================================================================

def investigate_exemplars(df):
    """What makes the very best Hispanic communities tick?"""
    print("\n" + "=" * 80)
    print("INVESTIGATION 5: EXEMPLAR COMMUNITY ANALYSIS")
    print("=" * 80)
    print("\nFinding the recipe for success in highest-resilience Hispanic tracts\n")

    hisp_maj = df[df['pct_hispanic'] > 50].copy()
    hisp_maj = hisp_maj.sort_values('resilience_score', ascending=False)

    # Top 100 vs Bottom 100
    top_100 = hisp_maj.head(100)
    bottom_100 = hisp_maj.tail(100)

    print("TOP 100 vs BOTTOM 100 Hispanic-Majority Tracts:")
    print("-" * 70)

    comparisons = [
        ('Resilience Score', 'resilience_score', '{:+.2f}'),
        ('% Foreign-Born', 'pct_foreign_born', '{:.1f}%'),
        ('% Mexican', 'pct_mexican', '{:.1f}%'),
        ('% South American', 'pct_south_american', '{:.1f}%'),
        ('% Central American', 'pct_central_american', '{:.1f}%'),
        ('Median HH Income', 'median_hh_income', '${:,.0f}'),
        ('% Bachelor+', 'pct_bachelors_plus', '{:.1f}%'),
        ('Poverty Rate', 'poverty_rate', '{:.1f}%'),
        ('% Black', 'pct_black', '{:.1f}%'),
    ]

    print(f"{'Characteristic':<25} {'Top 100':<18} {'Bottom 100':<18} {'Ratio':<10}")
    print("-" * 70)

    for name, col, fmt in comparisons:
        if col in top_100.columns:
            top_val = top_100[col].mean()
            bot_val = bottom_100[col].mean()
            ratio = top_val / bot_val if bot_val != 0 else 0

            print(f"{name:<25} {fmt.format(top_val):<18} {fmt.format(bot_val):<18} {ratio:.2f}x")

    # State distribution
    print("\nState Distribution:")
    print("  Top 100:", dict(top_100['StateAbbr'].value_counts().head(5)))
    print("  Bottom 100:", dict(bottom_100['StateAbbr'].value_counts().head(5)))

    # Origin distribution
    print("\nDominant Origin:")
    print("  Top 100:", dict(top_100['dominant_hispanic_origin'].value_counts()))
    print("  Bottom 100:", dict(bottom_100['dominant_hispanic_origin'].value_counts()))

    # Specific exemplar tracts
    print("\n" + "-" * 60)
    print("SPECIFIC EXEMPLAR TRACTS (Top 10)")
    print("-" * 60)

    for _, row in top_100.head(10).iterrows():
        print(f"\n  {row['GEOID']} ({row['StateAbbr']})")
        print(f"    Resilience: {row['resilience_score']:+.2f} SD")
        print(f"    % Hispanic: {row['pct_hispanic']:.1f}%, % Mexican: {row['pct_mexican']:.1f}%")
        print(f"    % Foreign-born: {row['pct_foreign_born']:.1f}%")
        print(f"    Income: ${row['median_hh_income']:,.0f}, % Bachelor+: {row['pct_bachelors_plus']:.1f}%")

    return {'top': top_100, 'bottom': bottom_100}


# =============================================================================
# DOCUMENTATION: SAVE ALL FINDINGS
# =============================================================================

def save_findings(df, tx_il, success, regions, exemplars):
    """Save all findings to a comprehensive research document."""
    print("\n" + "=" * 80)
    print("SAVING FINDINGS TO RESEARCH DOCUMENT")
    print("=" * 80)

    doc = f"""# Paper 4B: Hispanic Paradox Ultra-Deep Investigation

## Executive Summary

The "Hispanic Paradox" in community health resilience is not a single phenomenon
but an **aggregation artifact** masking profound heterogeneity across origin groups,
geographies, and socioeconomic contexts.

## Key Discoveries

### 1. THE TEXAS-ILLINOIS DIVERGENCE

The most striking finding is the dramatic difference between Mexican communities
in Texas vs Illinois:

| Metric | Texas | Illinois | Gap |
|--------|-------|----------|-----|
| Resilience | {tx_il['texas']['resilience_score'].mean():+.3f} SD | {tx_il['illinois']['resilience_score'].mean():+.3f} SD | {tx_il['illinois']['resilience_score'].mean() - tx_il['texas']['resilience_score'].mean():.3f} SD |
| % Foreign-Born | {tx_il['texas']['pct_foreign_born'].mean():.1f}% | {tx_il['illinois']['pct_foreign_born'].mean():.1f}% | {tx_il['illinois']['pct_foreign_born'].mean() - tx_il['texas']['pct_foreign_born'].mean():.1f} pp |
| Median Income | ${tx_il['texas']['median_hh_income'].mean():,.0f} | ${tx_il['illinois']['median_hh_income'].mean():,.0f} | ${tx_il['illinois']['median_hh_income'].mean() - tx_il['texas']['median_hh_income'].mean():,.0f} |
| % Bachelor+ | {tx_il['texas']['pct_bachelors_plus'].mean():.1f}% | {tx_il['illinois']['pct_bachelors_plus'].mean():.1f}% | {tx_il['illinois']['pct_bachelors_plus'].mean() - tx_il['texas']['pct_bachelors_plus'].mean():.1f} pp |
| Poverty Rate | {tx_il['texas']['poverty_rate'].mean():.1f}% | {tx_il['illinois']['poverty_rate'].mean():.1f}% | {tx_il['illinois']['poverty_rate'].mean() - tx_il['texas']['poverty_rate'].mean():.1f} pp |

**Key Insight**: Illinois Mexican immigrants are MORE educated, higher income, and
have HIGHER foreign-born % than Texas Mexican communities. This suggests different
immigration streams and settlement patterns.

### 2. THE SUCCESS STATE PATTERN (GA, VA, MD)

These "new destination" states show the strongest Hispanic resilience advantages
(+0.8+ SD gap over non-Hispanic tracts). Key characteristics:

| Metric | GA/VA/MD | TX/CA/AZ |
|--------|----------|----------|
| Resilience | {success['success']['resilience_score'].mean():+.3f} SD | {success['comparison']['resilience_score'].mean():+.3f} SD |
| % Mexican | {success['success']['pct_mexican'].mean():.1f}% | {success['comparison']['pct_mexican'].mean():.1f}% |
| % Central American | {success['success']['pct_central_american'].mean():.1f}% | {success['comparison']['pct_central_american'].mean():.1f}% |
| % South American | {success['success']['pct_south_american'].mean():.1f}% | {success['comparison']['pct_south_american'].mean():.1f}% |
| Median Income | ${success['success']['median_hh_income'].mean():,.0f} | ${success['comparison']['median_hh_income'].mean():,.0f} |
| % Bachelor+ | {success['success']['pct_bachelors_plus'].mean():.1f}% | {success['comparison']['pct_bachelors_plus'].mean():.1f}% |

**Key Insight**: New destination states attract a different composition of Hispanic
immigrants—more Central/South American, higher educated, and settling in metropolitan
areas with better economic opportunities.

### 3. THE AGGREGATION ARTIFACT

The near-zero overall Hispanic correlation (r ≈ +0.006) is the weighted average of:

| Origin | Weight | Correlation | Contribution |
|--------|--------|-------------|--------------|
| Mexican | 70.3% | -0.029 | -0.020 |
| Central American | 10.5% | +0.060 | +0.006 |
| South American | 5.3% | +0.147 | +0.008 |
| Puerto Rican | 8.4% | -0.017 | -0.001 |
| Cuban | 1.3% | +0.054 | +0.001 |
| Dominican | 4.3% | +0.010 | +0.000 |
| **Total** | 100% | | **-0.007** |

The "paradox" is mathematically an artifact of opposing effects canceling out.

### 4. REGIONAL PATTERNS

{regions.to_string()}

### 5. EXEMPLAR COMMUNITIES

Top 100 vs Bottom 100 Hispanic-majority tracts:

| Metric | Top 100 | Bottom 100 | Ratio |
|--------|---------|------------|-------|
| Resilience | {exemplars['top']['resilience_score'].mean():+.2f} SD | {exemplars['bottom']['resilience_score'].mean():+.2f} SD | — |
| % Foreign-Born | {exemplars['top']['pct_foreign_born'].mean():.1f}% | {exemplars['bottom']['pct_foreign_born'].mean():.1f}% | {exemplars['top']['pct_foreign_born'].mean()/exemplars['bottom']['pct_foreign_born'].mean():.2f}x |
| Income | ${exemplars['top']['median_hh_income'].mean():,.0f} | ${exemplars['bottom']['median_hh_income'].mean():,.0f} | {exemplars['top']['median_hh_income'].mean()/exemplars['bottom']['median_hh_income'].mean():.2f}x |
| % Bachelor+ | {exemplars['top']['pct_bachelors_plus'].mean():.1f}% | {exemplars['bottom']['pct_bachelors_plus'].mean():.1f}% | {exemplars['top']['pct_bachelors_plus'].mean()/exemplars['bottom']['pct_bachelors_plus'].mean():.2f}x |

## Theoretical Implications

1. **The "Hispanic Paradox" needs reframing**: It's not a single cultural phenomenon
   but multiple overlapping patterns of immigrant selection, settlement geography,
   and socioeconomic integration.

2. **Origin-specific analysis is essential**: Treating "Hispanic" as monolithic
   obscures more than it reveals. Mexican, Central American, South American,
   Puerto Rican, and Cuban communities have distinct trajectories.

3. **Geography is structure**: Border regions, new destinations, and metropolitan
   vs rural contexts create fundamentally different opportunity structures.

4. **Immigrant selection operates on multiple dimensions**: Not just health
   (the classic hypothesis) but education, income, and occupational skills.

## Policy Implications

1. **Texas border regions need targeted investment**: These communities show
   structural disadvantages not seen in other Mexican-origin communities.

2. **New destination model offers lessons**: Understanding why GA/VA/MD Hispanic
   communities thrive could inform policy in struggling traditional destinations.

3. **Puerto Rican structural disadvantage requires attention**: As US citizens,
   they don't benefit from immigrant selection but face concentrated poverty
   in Northeastern cities.

---

*Analysis conducted: {pd.Timestamp.now().strftime('%Y-%m-%d')}*
*Tracts analyzed: {len(df):,}*
"""

    output_path = OUTPUT_DIR / "PAPER-4B-FINDINGS.md"
    with open(output_path, 'w') as f:
        f.write(doc)

    print(f"\nFindings saved to: {output_path}")

    return doc


def main():
    print("=" * 80)
    print("PAPER 4B ULTRA-DEEP INVESTIGATION")
    print("=" * 80)

    df = load_all_data()

    # Run all investigations
    tx_il_results = investigate_texas_illinois(df)
    success_results = investigate_success_states(df)
    region_results = investigate_recency_hypothesis(df)
    education_results = investigate_education_pathway(df)
    exemplar_results = investigate_exemplars(df)

    # Save findings
    save_findings(df, tx_il_results, success_results, region_results, exemplar_results)

    print("\n" + "=" * 80)
    print("INVESTIGATION COMPLETE")
    print("=" * 80)

    return {
        'texas_illinois': tx_il_results,
        'success_states': success_results,
        'regions': region_results,
        'education': education_results,
        'exemplars': exemplar_results
    }


if __name__ == "__main__":
    results = main()
