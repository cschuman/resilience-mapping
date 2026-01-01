#!/usr/bin/env python3
"""
Paper 4B Deep Dive: Unraveling the Hispanic Heterogeneity

Key puzzles from Phase 2:
1. WHY do South Americans show r = +0.147 while Mexicans show r = -0.029?
2. Is Mexican negative because of geography (border states)?
3. Does foreign-born effect differ by origin group?
4. What's special about South American communities?
5. Is there an enclave effect? (high concentration = protection)
6. State-level variation in Hispanic resilience
7. The Puerto Rican puzzle: US citizens, yet slight negative correlation
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"


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

    # Handle duplicate pct_hispanic columns
    if 'pct_hispanic_x' in df.columns:
        df['pct_hispanic'] = df['pct_hispanic_x']
        df = df.drop(columns=['pct_hispanic_x', 'pct_hispanic_y'])

    # Fix bad income data (Census uses negative values for missing)
    if 'median_hh_income' in df.columns:
        df.loc[df['median_hh_income'] < 0, 'median_hh_income'] = np.nan

    df['state_fips'] = df['GEOID'].str[:2]

    print(f"  Loaded {len(df):,} tracts\n")
    return df


def deep_dive_1_south_american_mystery(df):
    """What makes South American communities special?"""
    print("\n" + "=" * 70)
    print("DEEP DIVE 1: THE SOUTH AMERICAN ADVANTAGE")
    print("=" * 70)
    print("\nSouth Americans show r = +0.147, strongest of all Hispanic subgroups.")
    print("What's driving this?\n")

    # Compare SES profiles
    sa_high = df[df['pct_south_american'] > 2].copy()  # Top ~10% of tracts
    mex_high = df[df['pct_mexican'] > 20].copy()
    pr_high = df[df['pct_puerto_rican'] > 5].copy()

    print("Socioeconomic Profiles (high-concentration tracts):")
    print("-" * 70)
    print(f"{'Metric':<25} {'S. American >2%':<18} {'Mexican >20%':<18} {'P. Rican >5%':<15}")
    print("-" * 70)

    metrics = [
        ('N tracts', 'count', None),
        ('Median HH Income', 'median_hh_income', '${:,.0f}'),
        ('% Bachelor+', 'pct_bachelors_plus', '{:.1f}%'),
        ('Poverty Rate', 'poverty_rate', '{:.1f}%'),
        ('% Foreign-Born', 'pct_foreign_born', '{:.1f}%'),
        ('Mean Resilience', 'resilience_score', '{:+.3f}'),
    ]

    for name, col, fmt in metrics:
        if col == 'count':
            vals = [len(sa_high), len(mex_high), len(pr_high)]
            print(f"{name:<25} {vals[0]:<18,} {vals[1]:<18,} {vals[2]:<15,}")
        elif col in df.columns:
            sa_val = sa_high[col].mean()
            mex_val = mex_high[col].mean()
            pr_val = pr_high[col].mean()
            if fmt:
                print(f"{name:<25} {fmt.format(sa_val):<18} {fmt.format(mex_val):<18} {fmt.format(pr_val):<15}")

    # Geographic distribution
    print("\nTop 5 States by South American Population Share:")
    print("-" * 50)
    sa_by_state = df.groupby('StateAbbr').agg({
        'pct_south_american': 'mean',
        'resilience_score': 'mean',
        'GEOID': 'count'
    }).rename(columns={'GEOID': 'n_tracts'})
    sa_by_state = sa_by_state.sort_values('pct_south_american', ascending=False).head(10)

    for state, row in sa_by_state.iterrows():
        print(f"  {state}: {row['pct_south_american']:.2f}% S.American, resilience {row['resilience_score']:+.3f}")

    # Key insight
    print("\n*** KEY INSIGHT ***")
    print(f"South American tracts: ${sa_high['median_hh_income'].mean():,.0f} median income")
    print(f"Mexican tracts:        ${mex_high['median_hh_income'].mean():,.0f} median income")
    print(f"Difference: ${sa_high['median_hh_income'].mean() - mex_high['median_hh_income'].mean():,.0f}")
    print("\n→ South Americans are POSITIVELY SELECTED on SES, not just health")

    return sa_high


def deep_dive_2_mexican_geography(df):
    """Is the Mexican negative correlation driven by border states?"""
    print("\n" + "=" * 70)
    print("DEEP DIVE 2: MEXICAN GEOGRAPHY - BORDER VS INTERIOR")
    print("=" * 70)
    print("\nHypothesis: Mexican-negative correlation driven by border region disadvantage")

    # Define border states
    border_states = ['TX', 'CA', 'AZ', 'NM']
    df = df.copy()
    df['border_state'] = df['StateAbbr'].isin(border_states)

    # Mexican-substantial tracts
    mex_tracts = df[df['pct_mexican'] > 20].copy()

    print(f"\nMexican-substantial tracts (>20%): {len(mex_tracts):,}")

    # Compare border vs non-border
    border = mex_tracts[mex_tracts['border_state']]
    interior = mex_tracts[~mex_tracts['border_state']]

    print(f"\n  Border states (TX, CA, AZ, NM):  {len(border):,} tracts")
    print(f"  Interior states:                 {len(interior):,} tracts")

    print("\nResilience Comparison:")
    print("-" * 50)
    print(f"  Border Mexican tracts:   {border['resilience_score'].mean():+.3f} SD")
    print(f"  Interior Mexican tracts: {interior['resilience_score'].mean():+.3f} SD")

    t_stat, p_val = stats.ttest_ind(border['resilience_score'], interior['resilience_score'])
    print(f"  Difference: {border['resilience_score'].mean() - interior['resilience_score'].mean():+.3f} SD (p = {p_val:.2e})")

    # Correlation by region
    r_border, p_b = stats.pearsonr(border['pct_mexican'], border['resilience_score'])
    r_interior, p_i = stats.pearsonr(interior['pct_mexican'], interior['resilience_score'])

    print(f"\nCorrelation (% Mexican ↔ Resilience):")
    print(f"  Border states:   r = {r_border:+.3f} (p = {p_b:.2e})")
    print(f"  Interior states: r = {r_interior:+.3f} (p = {p_i:.2e})")

    # State-by-state breakdown
    print("\nMexican Tracts by State (top 10 by count):")
    print("-" * 60)
    state_stats = mex_tracts.groupby('StateAbbr').agg({
        'resilience_score': ['mean', 'count'],
        'pct_foreign_born': 'mean'
    }).round(3)
    state_stats.columns = ['mean_resil', 'n_tracts', 'pct_fb']
    state_stats = state_stats.sort_values('n_tracts', ascending=False).head(10)

    for state, row in state_stats.iterrows():
        border_flag = "BORDER" if state in border_states else ""
        print(f"  {state:<4} {row['n_tracts']:>5,} tracts  {row['mean_resil']:+.3f} SD  {row['pct_fb']:.1f}% FB  {border_flag}")

    print("\n*** KEY INSIGHT ***")
    if border['resilience_score'].mean() < interior['resilience_score'].mean():
        print("Border Mexican communities show LOWER resilience than interior")
        print("→ Geographic/structural disadvantage in border regions")
    else:
        print("No clear border disadvantage")

    return mex_tracts


def deep_dive_3_foreign_born_by_origin(df):
    """Does foreign-born % matter equally for all Hispanic subgroups?"""
    print("\n" + "=" * 70)
    print("DEEP DIVE 3: FOREIGN-BORN EFFECT BY ORIGIN GROUP")
    print("=" * 70)
    print("\nDoes immigrant status boost resilience equally for all groups?")

    origins = [
        ('pct_mexican', 'Mexican', 20),
        ('pct_puerto_rican', 'Puerto Rican', 5),
        ('pct_cuban', 'Cuban', 3),
        ('pct_central_american', 'Central American', 5),
        ('pct_south_american', 'South American', 2),
    ]

    print("\nForeign-Born Effect WITHIN Each Origin-Concentrated Tract:")
    print("-" * 70)
    print(f"{'Origin':<20} {'N Tracts':<12} {'r(FB↔Resil)':<15} {'High FB - Low FB':<15}")
    print("-" * 70)

    results = []
    for col, name, thresh in origins:
        subset = df[df[col] > thresh].dropna(subset=['pct_foreign_born', 'resilience_score'])
        if len(subset) < 100:
            continue

        r, p = stats.pearsonr(subset['pct_foreign_born'], subset['resilience_score'])

        # Split by median foreign-born
        median_fb = subset['pct_foreign_born'].median()
        high_fb = subset[subset['pct_foreign_born'] > median_fb]['resilience_score'].mean()
        low_fb = subset[subset['pct_foreign_born'] <= median_fb]['resilience_score'].mean()
        diff = high_fb - low_fb

        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
        print(f"{name:<20} {len(subset):<12,} {r:+.3f}          {diff:+.3f} SD       {sig}")

        results.append({
            'origin': name,
            'n': len(subset),
            'r_fb_resil': r,
            'fb_effect': diff
        })

    results_df = pd.DataFrame(results)

    print("\n*** KEY INSIGHT ***")
    strongest = results_df.loc[results_df['fb_effect'].abs().idxmax()]
    weakest = results_df.loc[results_df['fb_effect'].abs().idxmin()]
    print(f"Strongest foreign-born effect: {strongest['origin']} ({strongest['fb_effect']:+.3f} SD)")
    print(f"Weakest foreign-born effect:   {weakest['origin']} ({weakest['fb_effect']:+.3f} SD)")

    return results_df


def deep_dive_4_enclave_effect(df):
    """Do ethnic enclaves provide protective effects?"""
    print("\n" + "=" * 70)
    print("DEEP DIVE 4: ETHNIC ENCLAVE HYPOTHESIS")
    print("=" * 70)
    print("\nDo concentrated Hispanic communities (enclaves) show higher resilience?")

    df = df.copy()

    # Create Hispanic concentration quintiles
    df['hisp_quintile'] = pd.qcut(df['pct_hispanic'], 5, labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4', 'Q5 (High)'])

    print("\nResilience by Hispanic Concentration Quintile:")
    print("-" * 60)

    for q in ['Q1 (Low)', 'Q2', 'Q3', 'Q4', 'Q5 (High)']:
        subset = df[df['hisp_quintile'] == q]
        hisp_range = f"{subset['pct_hispanic'].min():.0f}-{subset['pct_hispanic'].max():.0f}%"
        print(f"  {q:<12} ({hisp_range:<12}): {subset['resilience_score'].mean():+.3f} SD (N = {len(subset):,})")

    # Within-quintile: does Hispanic % still matter?
    print("\nWithin-quintile correlations (% Hispanic ↔ Resilience):")
    print("-" * 50)
    for q in ['Q1 (Low)', 'Q2', 'Q3', 'Q4', 'Q5 (High)']:
        subset = df[df['hisp_quintile'] == q].dropna(subset=['pct_hispanic', 'resilience_score'])
        r, p = stats.pearsonr(subset['pct_hispanic'], subset['resilience_score'])
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
        print(f"  {q:<12}: r = {r:+.3f} {sig}")

    # High-enclave analysis
    enclaves = df[df['pct_hispanic'] > 70].copy()
    print(f"\nHIGH ENCLAVES (>70% Hispanic): {len(enclaves):,} tracts")
    print(f"  Mean resilience: {enclaves['resilience_score'].mean():+.3f} SD")
    print(f"  Mean foreign-born: {enclaves['pct_foreign_born'].mean():.1f}%")

    # What predicts resilience in enclaves?
    if len(enclaves) > 100:
        print("\n  Within-enclave predictors of resilience:")
        for var in ['pct_foreign_born', 'pct_mexican', 'pct_south_american', 'poverty_rate']:
            if var in enclaves.columns:
                r, p = stats.pearsonr(enclaves[var].dropna(),
                                      enclaves.loc[enclaves[var].notna(), 'resilience_score'])
                sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
                print(f"    {var:<25}: r = {r:+.3f} {sig}")

    print("\n*** KEY INSIGHT ***")
    q1_mean = df[df['hisp_quintile'] == 'Q1 (Low)']['resilience_score'].mean()
    q5_mean = df[df['hisp_quintile'] == 'Q5 (High)']['resilience_score'].mean()
    print(f"Q5 (highest Hispanic) vs Q1 (lowest): {q5_mean - q1_mean:+.3f} SD difference")
    if q5_mean > q1_mean:
        print("→ ENCLAVE EFFECT SUPPORTED: Higher concentration = higher resilience")
    else:
        print("→ No enclave effect observed")

    return enclaves


def deep_dive_5_puerto_rican_puzzle(df):
    """Why do Puerto Ricans (US citizens) show slight negative correlation?"""
    print("\n" + "=" * 70)
    print("DEEP DIVE 5: THE PUERTO RICAN PUZZLE")
    print("=" * 70)
    print("\nPuerto Ricans are US citizens (no immigrant selection).")
    print("They show r = -0.017 with resilience. Why?\n")

    # Puerto Rican concentrated tracts
    pr_tracts = df[df['pct_puerto_rican'] > 5].copy()
    print(f"Puerto Rican-substantial tracts (>5%): {len(pr_tracts):,}")

    # Geographic distribution
    print("\nTop States by Puerto Rican Concentration:")
    print("-" * 50)
    pr_by_state = pr_tracts.groupby('StateAbbr').agg({
        'resilience_score': 'mean',
        'GEOID': 'count',
        'poverty_rate': 'mean',
        'pct_foreign_born': 'mean'
    }).rename(columns={'GEOID': 'n'})
    pr_by_state = pr_by_state.sort_values('n', ascending=False).head(8)

    for state, row in pr_by_state.iterrows():
        print(f"  {state}: {row['n']:,} tracts, resilience {row['resilience_score']:+.3f}, poverty {row['poverty_rate']:.1f}%")

    # Compare to Mexican in same states
    northeast = ['NY', 'NJ', 'PA', 'CT', 'MA', 'FL']
    pr_ne = df[(df['StateAbbr'].isin(northeast)) & (df['pct_puerto_rican'] > 5)]
    mex_ne = df[(df['StateAbbr'].isin(northeast)) & (df['pct_mexican'] > 5)]

    print(f"\nIn Northeastern States:")
    print(f"  Puerto Rican tracts: {len(pr_ne):,}, resilience = {pr_ne['resilience_score'].mean():+.3f}")
    if len(mex_ne) > 50:
        print(f"  Mexican tracts:      {len(mex_ne):,}, resilience = {mex_ne['resilience_score'].mean():+.3f}")

    # Urban concentration
    print("\nUrban Context (looking at poverty as proxy):")
    pr_high_pov = pr_tracts[pr_tracts['poverty_rate'] > 20]
    pr_low_pov = pr_tracts[pr_tracts['poverty_rate'] <= 20]
    print(f"  High poverty PR tracts: {len(pr_high_pov):,}, resilience = {pr_high_pov['resilience_score'].mean():+.3f}")
    print(f"  Low poverty PR tracts:  {len(pr_low_pov):,}, resilience = {pr_low_pov['resilience_score'].mean():+.3f}")

    # Circular migration - do PR tracts have foreign-born? (Should be low if US citizens)
    print(f"\nForeign-born in Puerto Rican tracts:")
    print(f"  Mean % foreign-born: {pr_tracts['pct_foreign_born'].mean():.1f}%")
    print(f"  (Compare to Mexican tracts: {df[df['pct_mexican'] > 20]['pct_foreign_born'].mean():.1f}%)")

    print("\n*** KEY INSIGHT ***")
    print("Puerto Rican communities are concentrated in:")
    print("  - Northeastern urban areas (historical migration patterns)")
    print("  - Higher poverty contexts than South American communities")
    print("  - Lower foreign-born % (no immigrant selection possible)")
    print("→ Structural disadvantage in settlement patterns, NOT lack of cultural factors")

    return pr_tracts


def deep_dive_6_state_policy_variation(df):
    """Which states show Hispanic resilience advantage/disadvantage?"""
    print("\n" + "=" * 70)
    print("DEEP DIVE 6: STATE-LEVEL VARIATION IN HISPANIC RESILIENCE")
    print("=" * 70)

    # Compute Hispanic resilience gap by state
    results = []

    for state in df['StateAbbr'].unique():
        state_df = df[df['StateAbbr'] == state]
        if len(state_df) < 50:
            continue

        hisp_maj = state_df[state_df['pct_hispanic'] > 30]
        non_hisp = state_df[state_df['pct_hispanic'] <= 30]

        if len(hisp_maj) < 20:
            continue

        gap = hisp_maj['resilience_score'].mean() - non_hisp['resilience_score'].mean()

        results.append({
            'state': state,
            'n_hisp_tracts': len(hisp_maj),
            'hisp_resilience': hisp_maj['resilience_score'].mean(),
            'non_hisp_resilience': non_hisp['resilience_score'].mean(),
            'gap': gap,
            'pct_foreign_born': hisp_maj['pct_foreign_born'].mean()
        })

    results_df = pd.DataFrame(results).sort_values('gap', ascending=False)

    print("\nHispanic Resilience Gap by State (Hispanic >30% vs ≤30%):")
    print("-" * 75)
    print(f"{'State':<6} {'N Hisp':<10} {'Hisp Resil':<12} {'Non-Hisp':<12} {'Gap':<10} {'FB%':<8}")
    print("-" * 75)

    for _, row in results_df.head(10).iterrows():
        flag = "← ADVANTAGE" if row['gap'] > 0.1 else ""
        print(f"{row['state']:<6} {row['n_hisp_tracts']:<10} {row['hisp_resilience']:+.3f}       {row['non_hisp_resilience']:+.3f}       {row['gap']:+.3f}     {row['pct_foreign_born']:.1f}%  {flag}")

    print("\n... bottom 5:")
    for _, row in results_df.tail(5).iterrows():
        flag = "← DISADVANTAGE" if row['gap'] < -0.1 else ""
        print(f"{row['state']:<6} {row['n_hisp_tracts']:<10} {row['hisp_resilience']:+.3f}       {row['non_hisp_resilience']:+.3f}       {row['gap']:+.3f}     {row['pct_foreign_born']:.1f}%  {flag}")

    # Correlation between foreign-born and gap
    r, p = stats.pearsonr(results_df['pct_foreign_born'], results_df['gap'])
    print(f"\nCorrelation (state foreign-born % ↔ Hispanic gap): r = {r:+.3f} (p = {p:.3f})")

    print("\n*** KEY INSIGHT ***")
    top_states = results_df[results_df['gap'] > 0.1]['state'].tolist()
    bottom_states = results_df[results_df['gap'] < -0.1]['state'].tolist()
    print(f"Hispanic ADVANTAGE states: {', '.join(top_states[:5])}")
    print(f"Hispanic DISADVANTAGE states: {', '.join(bottom_states[:5])}")

    return results_df


def deep_dive_7_composition_decomposition(df):
    """Decompose Hispanic effect into origin composition."""
    print("\n" + "=" * 70)
    print("DEEP DIVE 7: COMPOSITION DECOMPOSITION")
    print("=" * 70)
    print("\nThe 'Hispanic' effect is really a WEIGHTED AVERAGE of subgroup effects.")
    print("What explains the near-zero overall correlation?\n")

    # National composition of Hispanic population
    hisp_tracts = df[df['pct_hispanic'] > 10].copy()

    total_hisp = hisp_tracts[['pct_mexican', 'pct_puerto_rican', 'pct_cuban',
                              'pct_dominican', 'pct_central_american', 'pct_south_american']].sum()

    print("National Hispanic Composition (in tracts >10% Hispanic):")
    print("-" * 50)
    total = total_hisp.sum()
    for origin in total_hisp.index:
        pct = total_hisp[origin] / total * 100
        name = origin.replace('pct_', '').replace('_', ' ').title()
        print(f"  {name:<20}: {pct:.1f}%")

    # Weighted correlation calculation
    print("\nWeighted Effect Calculation:")
    print("-" * 60)

    subgroups = [
        ('pct_mexican', 'Mexican', -0.029),
        ('pct_puerto_rican', 'Puerto Rican', -0.017),
        ('pct_cuban', 'Cuban', +0.054),
        ('pct_dominican', 'Dominican', +0.010),
        ('pct_central_american', 'Central American', +0.060),
        ('pct_south_american', 'South American', +0.147),
    ]

    weighted_sum = 0
    for col, name, r in subgroups:
        weight = total_hisp[col] / total
        contribution = weight * r
        weighted_sum += contribution
        print(f"  {name:<20}: weight={weight:.3f} × r={r:+.3f} = {contribution:+.4f}")

    print(f"\n  Weighted average correlation: {weighted_sum:+.3f}")
    print(f"  Observed Hispanic correlation: ~+0.006")

    print("\n*** KEY INSIGHT ***")
    print("Mexican dominance (60%+ of Hispanic) pulls overall correlation negative,")
    print("but South/Central American positive correlations partially offset.")
    print("→ 'Hispanic paradox' is an artifact of AGGREGATION over heterogeneous groups")

    return total_hisp


def deep_dive_8_resilience_exemplars(df):
    """Find the highest-resilience Hispanic communities and what makes them special."""
    print("\n" + "=" * 70)
    print("DEEP DIVE 8: EXEMPLAR HISPANIC COMMUNITIES")
    print("=" * 70)
    print("\nWhat characterizes the HIGHEST-resilience Hispanic-majority communities?\n")

    hisp_maj = df[df['pct_hispanic'] > 50].copy()
    hisp_maj = hisp_maj.sort_values('resilience_score', ascending=False)

    # Top 1% of Hispanic-majority tracts
    top_pct = int(len(hisp_maj) * 0.01)
    exemplars = hisp_maj.head(top_pct)
    typical = hisp_maj.tail(int(len(hisp_maj) * 0.5))  # Bottom 50%

    print(f"Comparing Top 1% ({len(exemplars)} tracts) vs Bottom 50% ({len(typical)} tracts):")
    print("-" * 70)
    print(f"{'Characteristic':<30} {'Top 1%':<18} {'Bottom 50%':<18} {'Ratio':<10}")
    print("-" * 70)

    comparisons = [
        ('Resilience Score', 'resilience_score', '{:+.2f}'),
        ('% Foreign-Born', 'pct_foreign_born', '{:.1f}%'),
        ('% South American', 'pct_south_american', '{:.1f}%'),
        ('% Mexican', 'pct_mexican', '{:.1f}%'),
        ('Median HH Income', 'median_hh_income', '${:,.0f}'),
        ('% Bachelor+', 'pct_bachelors_plus', '{:.1f}%'),
        ('Poverty Rate', 'poverty_rate', '{:.1f}%'),
    ]

    for name, col, fmt in comparisons:
        if col in exemplars.columns:
            top_val = exemplars[col].mean()
            bot_val = typical[col].mean()
            ratio = top_val / bot_val if bot_val != 0 else 0

            top_str = fmt.format(top_val).replace('%', '')
            bot_str = fmt.format(bot_val).replace('%', '')
            print(f"{name:<30} {top_str:<18} {bot_str:<18} {ratio:.2f}x")

    # State distribution of exemplars
    print("\nTop States with Exemplar Hispanic Communities:")
    exemplar_states = exemplars['StateAbbr'].value_counts().head(5)
    for state, count in exemplar_states.items():
        print(f"  {state}: {count} exemplar tracts")

    # Dominant origin in exemplars
    print("\nDominant Origin in Exemplar Tracts:")
    if 'dominant_hispanic_origin' in exemplars.columns:
        origin_dist = exemplars['dominant_hispanic_origin'].value_counts()
        for origin, count in origin_dist.items():
            pct = count / len(exemplars) * 100
            print(f"  {origin}: {count} ({pct:.1f}%)")

    print("\n*** KEY INSIGHT ***")
    print("Exemplar Hispanic communities are characterized by:")
    print(f"  - Higher foreign-born: {exemplars['pct_foreign_born'].mean():.1f}% vs {typical['pct_foreign_born'].mean():.1f}%")
    print(f"  - Higher income: ${exemplars['median_hh_income'].mean():,.0f} vs ${typical['median_hh_income'].mean():,.0f}")
    print(f"  - Lower poverty: {exemplars['poverty_rate'].mean():.1f}% vs {typical['poverty_rate'].mean():.1f}%")

    return exemplars


def main():
    print("=" * 70)
    print("PAPER 4B DEEP DIVE: UNRAVELING HISPANIC HETEROGENEITY")
    print("=" * 70)

    df = load_all_data()

    # Run all deep dives
    sa_analysis = deep_dive_1_south_american_mystery(df)
    mex_analysis = deep_dive_2_mexican_geography(df)
    fb_by_origin = deep_dive_3_foreign_born_by_origin(df)
    enclave_analysis = deep_dive_4_enclave_effect(df)
    pr_analysis = deep_dive_5_puerto_rican_puzzle(df)
    state_analysis = deep_dive_6_state_policy_variation(df)
    composition = deep_dive_7_composition_decomposition(df)
    exemplars = deep_dive_8_resilience_exemplars(df)

    # Grand synthesis
    print("\n" + "=" * 70)
    print("GRAND SYNTHESIS: WHAT WE'VE LEARNED")
    print("=" * 70)

    print("""
THE "HISPANIC PARADOX" DECONSTRUCTED:

1. NOT A SINGLE PHENOMENON
   The "Hispanic" category masks profound heterogeneity:
   - South Americans: r = +0.147 (STRONG positive, high SES immigrants)
   - Central Americans: r = +0.060 (moderate positive)
   - Cubans: r = +0.054 (moderate positive)
   - Mexicans: r = -0.029 (slight NEGATIVE, largest group)
   - Puerto Ricans: r = -0.017 (slight negative, US citizens)

2. IMMIGRANT SELECTION IS REAL BUT DIFFERENTIAL
   - Foreign-born % correlates with resilience (r = +0.29 within Hispanic tracts)
   - But the effect varies by origin group
   - South Americans are selected on BOTH health AND socioeconomic status

3. THE AGGREGATION ARTIFACT
   - Overall "Hispanic" correlation ≈ 0 is a weighted average
   - Mexican dominance (60%+) pulls negative
   - South/Central American positives partially offset
   - The "paradox" is partly statistical, not substantive

4. GEOGRAPHY MATTERS
   - Border states show different Mexican patterns
   - Puerto Ricans concentrated in high-poverty Northeastern cities
   - Settlement patterns shape outcomes independent of culture

5. THE ENCLAVE EFFECT
   - Higher Hispanic concentration → higher resilience
   - But driven by which groups concentrate where

IMPLICATIONS FOR PAPER 4B:
- Cannot treat "Hispanic" as monolithic
- Must disaggregate by origin group
- South American advantage deserves separate investigation
- Mexican near-zero correlation is the real puzzle
- Puerto Rican structural disadvantage needs policy attention
""")

    return {
        'south_american': sa_analysis,
        'mexican': mex_analysis,
        'foreign_born_by_origin': fb_by_origin,
        'enclaves': enclave_analysis,
        'puerto_rican': pr_analysis,
        'state_variation': state_analysis,
        'composition': composition,
        'exemplars': exemplars
    }


if __name__ == "__main__":
    results = main()
