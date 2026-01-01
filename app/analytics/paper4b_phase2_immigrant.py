#!/usr/bin/env python3
"""
Paper 4B Phase 2: Immigrant Selectivity Analysis

Key questions:
1. Does % foreign-born explain the Hispanic paradox in resilience?
2. Is the Hispanic × Foreign-born interaction significant?
3. Do Mexican-origin communities (strong selection) differ from Puerto Rican (US citizens)?
4. Does the paradox weaken in US-born Hispanic communities?
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def load_all_data():
    """Load and merge resilience, demographics, nativity, and Hispanic origin data."""
    print("Loading data...")

    # Resilience scores
    resilience = pd.read_csv(DATA_DIR / "processed" / "model_table_corrected.csv")
    resilience['GEOID'] = resilience['TractFIPS'].astype(str).str.zfill(11)
    print(f"  Resilience: {len(resilience):,} tracts")

    # ACS demographics (already have pct_hispanic, pct_black, etc.)
    acs = pd.read_csv(DATA_DIR / "external" / "acs_demographics_2022.csv")
    acs['GEOID'] = acs['GEOID'].astype(str).str.zfill(11)
    print(f"  ACS Demographics: {len(acs):,} tracts")

    # Nativity data
    nativity = pd.read_csv(DATA_DIR / "external" / "acs_nativity_2022.csv")
    nativity['GEOID'] = nativity['GEOID'].astype(str).str.zfill(11)
    nativity = nativity[['GEOID', 'pct_foreign_born']]
    print(f"  Nativity: {len(nativity):,} tracts")

    # Hispanic origin data
    hispanic = pd.read_csv(DATA_DIR / "external" / "acs_hispanic_origin_2022.csv")
    hispanic['GEOID'] = hispanic['GEOID'].astype(str).str.zfill(11)
    hispanic_cols = ['GEOID', 'pct_mexican', 'pct_puerto_rican', 'pct_cuban',
                     'pct_dominican', 'pct_central_american', 'pct_south_american',
                     'pct_mexican_of_hispanic', 'pct_puerto_rican_of_hispanic',
                     'dominant_hispanic_origin']
    hispanic = hispanic[hispanic_cols]
    print(f"  Hispanic Origin: {len(hispanic):,} tracts")

    # Merge all
    df = resilience.merge(acs, on='GEOID', how='inner')
    df = df.merge(nativity, on='GEOID', how='inner')
    df = df.merge(hispanic, on='GEOID', how='inner')

    df['state_fips'] = df['GEOID'].str[:2]

    print(f"\n  Final merged: {len(df):,} tracts")
    return df


def analysis_1_foreign_born_correlation(df):
    """Test if foreign-born % correlates with resilience."""
    print("\n" + "=" * 70)
    print("ANALYSIS 1: Foreign-Born % and Resilience")
    print("=" * 70)

    valid = df.dropna(subset=['resilience_score', 'pct_foreign_born', 'pct_hispanic'])

    # Overall correlation
    r_fb, p_fb = stats.pearsonr(valid['pct_foreign_born'], valid['resilience_score'])
    print(f"\nOverall correlation (N = {len(valid):,}):")
    print(f"  % Foreign-born ↔ Resilience: r = {r_fb:+.3f} (p = {p_fb:.2e})")

    # In Hispanic-majority tracts
    hisp_maj = valid[valid['pct_hispanic'] > 50]
    if len(hisp_maj) > 100:
        r_fb_hisp, p_fb_hisp = stats.pearsonr(hisp_maj['pct_foreign_born'], hisp_maj['resilience_score'])
        print(f"\nIn Hispanic-majority tracts (N = {len(hisp_maj):,}):")
        print(f"  % Foreign-born ↔ Resilience: r = {r_fb_hisp:+.3f} (p = {p_fb_hisp:.2e})")

    # Compare high vs low foreign-born Hispanic tracts
    hisp_tracts = valid[valid['pct_hispanic'] > 30]
    median_fb = hisp_tracts['pct_foreign_born'].median()

    high_fb = hisp_tracts[hisp_tracts['pct_foreign_born'] > median_fb]
    low_fb = hisp_tracts[hisp_tracts['pct_foreign_born'] <= median_fb]

    print(f"\nHispanic tracts (>30%) split by foreign-born median ({median_fb:.1f}%):")
    print(f"  High foreign-born ({len(high_fb):,} tracts): Mean resilience = {high_fb['resilience_score'].mean():+.3f}")
    print(f"  Low foreign-born ({len(low_fb):,} tracts):  Mean resilience = {low_fb['resilience_score'].mean():+.3f}")

    t_stat, p_val = stats.ttest_ind(high_fb['resilience_score'], low_fb['resilience_score'])
    print(f"  Difference: {high_fb['resilience_score'].mean() - low_fb['resilience_score'].mean():+.3f} SD (p = {p_val:.2e})")

    return {
        'r_foreign_born_overall': r_fb,
        'high_fb_resilience': high_fb['resilience_score'].mean(),
        'low_fb_resilience': low_fb['resilience_score'].mean()
    }


def analysis_2_interaction_model(df):
    """Test Hispanic × Foreign-born interaction in predicting resilience."""
    print("\n" + "=" * 70)
    print("ANALYSIS 2: Hispanic × Foreign-Born Interaction Model")
    print("=" * 70)

    valid = df.dropna(subset=['resilience_score', 'pct_hispanic', 'pct_foreign_born',
                               'pct_black', 'poverty_rate']).copy()

    # Standardize predictors
    valid['hisp_z'] = (valid['pct_hispanic'] - valid['pct_hispanic'].mean()) / valid['pct_hispanic'].std()
    valid['fb_z'] = (valid['pct_foreign_born'] - valid['pct_foreign_born'].mean()) / valid['pct_foreign_born'].std()
    valid['black_z'] = (valid['pct_black'] - valid['pct_black'].mean()) / valid['pct_black'].std()
    valid['pov_z'] = (valid['poverty_rate'] - valid['poverty_rate'].mean()) / valid['poverty_rate'].std()

    # Create interaction term
    valid['hisp_x_fb'] = valid['hisp_z'] * valid['fb_z']

    # Model 1: Main effects only
    X1 = valid[['hisp_z', 'fb_z', 'black_z', 'pov_z']]
    X1 = sm.add_constant(X1)
    y = valid['resilience_score']

    model1 = sm.OLS(y, X1).fit()

    print("\nModel 1: Main Effects Only")
    print("-" * 50)
    print(f"  R² = {model1.rsquared:.4f}")
    print(f"  Hispanic (z):      β = {model1.params['hisp_z']:+.4f} (p = {model1.pvalues['hisp_z']:.2e})")
    print(f"  Foreign-born (z):  β = {model1.params['fb_z']:+.4f} (p = {model1.pvalues['fb_z']:.2e})")
    print(f"  Black (z):         β = {model1.params['black_z']:+.4f} (p = {model1.pvalues['black_z']:.2e})")
    print(f"  Poverty (z):       β = {model1.params['pov_z']:+.4f} (p = {model1.pvalues['pov_z']:.2e})")

    # Model 2: With interaction
    X2 = valid[['hisp_z', 'fb_z', 'black_z', 'pov_z', 'hisp_x_fb']]
    X2 = sm.add_constant(X2)

    model2 = sm.OLS(y, X2).fit()

    print("\nModel 2: With Hispanic × Foreign-Born Interaction")
    print("-" * 50)
    print(f"  R² = {model2.rsquared:.4f} (ΔR² = {model2.rsquared - model1.rsquared:.4f})")
    print(f"  Hispanic (z):      β = {model2.params['hisp_z']:+.4f} (p = {model2.pvalues['hisp_z']:.2e})")
    print(f"  Foreign-born (z):  β = {model2.params['fb_z']:+.4f} (p = {model2.pvalues['fb_z']:.2e})")
    print(f"  Black (z):         β = {model2.params['black_z']:+.4f} (p = {model2.pvalues['black_z']:.2e})")
    print(f"  Poverty (z):       β = {model2.params['pov_z']:+.4f} (p = {model2.pvalues['pov_z']:.2e})")
    print(f"  Hispanic × FB:     β = {model2.params['hisp_x_fb']:+.4f} (p = {model2.pvalues['hisp_x_fb']:.2e})")

    # Interpretation
    print("\n*** INTERPRETATION ***")
    if model2.pvalues['hisp_x_fb'] < 0.05:
        if model2.params['hisp_x_fb'] > 0:
            print("POSITIVE INTERACTION: Foreign-born % AMPLIFIES Hispanic resilience advantage")
            print("  → Immigrant selectivity hypothesis SUPPORTED")
        else:
            print("NEGATIVE INTERACTION: Foreign-born % REDUCES Hispanic effect")
            print("  → Immigrant selectivity hypothesis NOT supported")
    else:
        print("NO SIGNIFICANT INTERACTION: Foreign-born % doesn't modify Hispanic effect")
        print("  → Hispanic resilience pattern NOT explained by immigrant composition")

    return model2


def analysis_3_mexican_vs_puerto_rican(df):
    """Compare Mexican-origin (immigrant selection) vs Puerto Rican (US citizens)."""
    print("\n" + "=" * 70)
    print("ANALYSIS 3: Mexican vs Puerto Rican - The Key Test")
    print("=" * 70)
    print("\nRationale: Mexican immigrants undergo selection; Puerto Ricans are US citizens.")
    print("If immigrant selection explains paradox, Mexican should show it, Puerto Rican should NOT.")

    valid = df.dropna(subset=['resilience_score', 'pct_mexican', 'pct_puerto_rican'])

    # Correlations with resilience
    r_mex, p_mex = stats.pearsonr(valid['pct_mexican'], valid['resilience_score'])
    r_pr, p_pr = stats.pearsonr(valid['pct_puerto_rican'], valid['resilience_score'])

    print(f"\nCorrelations with Resilience (N = {len(valid):,}):")
    print(f"  % Mexican:      r = {r_mex:+.3f} (p = {p_mex:.2e})")
    print(f"  % Puerto Rican: r = {r_pr:+.3f} (p = {p_pr:.2e})")

    # Fisher z-test for difference
    z_mex = np.arctanh(r_mex)
    z_pr = np.arctanh(r_pr)
    se_diff = np.sqrt(2 / (len(valid) - 3))
    z_diff = (z_mex - z_pr) / se_diff
    p_diff = 2 * (1 - stats.norm.cdf(abs(z_diff)))

    print(f"\nDifference test: z = {z_diff:.2f}, p = {p_diff:.2e}")

    # Compare majority tracts
    mex_maj = valid[valid['pct_mexican'] > 30]
    pr_maj = valid[valid['pct_puerto_rican'] > 10]  # Lower threshold due to smaller population

    print(f"\nMean Resilience in Concentrated Areas:")
    print(f"  Mexican >30% ({len(mex_maj):,} tracts):      {mex_maj['resilience_score'].mean():+.3f} SD")
    print(f"  Puerto Rican >10% ({len(pr_maj):,} tracts): {pr_maj['resilience_score'].mean():+.3f} SD")

    # Key interpretation
    print("\n*** KEY FINDING ***")
    if r_mex > r_pr:
        print(f"Mexican correlation ({r_mex:+.3f}) > Puerto Rican ({r_pr:+.3f})")
        if p_diff < 0.05:
            print("DIFFERENCE IS SIGNIFICANT")
            print("→ Immigrant selection hypothesis SUPPORTED")
            print("  Mexican communities (immigrant selection) show paradox")
            print("  Puerto Rican communities (US citizens) show weaker/no paradox")
        else:
            print("But difference is NOT statistically significant")
    else:
        print(f"Puerto Rican correlation ({r_pr:+.3f}) ≥ Mexican ({r_mex:+.3f})")
        print("→ Immigrant selection hypothesis NOT supported")
        print("  Paradox exists even without immigrant selection")

    return {
        'r_mexican': r_mex,
        'r_puerto_rican': r_pr,
        'p_difference': p_diff
    }


def analysis_4_subgroup_patterns(df):
    """Analyze all Hispanic subgroups."""
    print("\n" + "=" * 70)
    print("ANALYSIS 4: All Hispanic Subgroup Correlations")
    print("=" * 70)

    valid = df.dropna(subset=['resilience_score'])

    subgroups = [
        ('pct_mexican', 'Mexican'),
        ('pct_puerto_rican', 'Puerto Rican'),
        ('pct_cuban', 'Cuban'),
        ('pct_dominican', 'Dominican'),
        ('pct_central_american', 'Central American'),
        ('pct_south_american', 'South American'),
    ]

    print(f"\nCorrelations with Resilience Score (N = {len(valid):,}):")
    print("-" * 60)
    print(f"{'Subgroup':<20} {'r':<10} {'p-value':<15} {'Mean %':<10}")
    print("-" * 60)

    results = []
    for col, name in subgroups:
        subset = valid.dropna(subset=[col])
        r, p = stats.pearsonr(subset[col], subset['resilience_score'])
        mean_pct = subset[col].mean()

        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
        print(f"{name:<20} {r:+.3f}     {p:.2e}      {mean_pct:.1f}% {sig}")

        results.append({
            'subgroup': name,
            'correlation': r,
            'p_value': p,
            'mean_pct': mean_pct
        })

    # Compare to Black for reference
    r_black, p_black = stats.pearsonr(valid['pct_black'], valid['resilience_score'])
    print("-" * 60)
    print(f"{'Black (reference)':<20} {r_black:+.3f}     {p_black:.2e}      {valid['pct_black'].mean():.1f}%")

    # Interpretation
    results_df = pd.DataFrame(results)
    most_positive = results_df.loc[results_df['correlation'].idxmax()]
    most_negative = results_df.loc[results_df['correlation'].idxmin()]

    print(f"\n*** PATTERN ***")
    print(f"Most positive: {most_positive['subgroup']} (r = {most_positive['correlation']:+.3f})")
    print(f"Most negative: {most_negative['subgroup']} (r = {most_negative['correlation']:+.3f})")

    return results_df


def analysis_5_foreign_born_within_hispanic(df):
    """Within Hispanic-majority tracts, does foreign-born % predict resilience?"""
    print("\n" + "=" * 70)
    print("ANALYSIS 5: Foreign-Born Effect WITHIN Hispanic Communities")
    print("=" * 70)

    # Focus on Hispanic-majority tracts
    hisp_maj = df[df['pct_hispanic'] > 50].dropna(subset=['resilience_score', 'pct_foreign_born']).copy()

    print(f"\nWithin Hispanic-majority tracts (>50% Hispanic, N = {len(hisp_maj):,}):")

    # Tertiles of foreign-born
    hisp_maj['fb_tertile'] = pd.qcut(hisp_maj['pct_foreign_born'], 3, labels=['Low', 'Medium', 'High'])

    print("\nResilience by Foreign-Born Tertile:")
    print("-" * 50)

    for tertile in ['Low', 'Medium', 'High']:
        subset = hisp_maj[hisp_maj['fb_tertile'] == tertile]
        fb_range = f"{subset['pct_foreign_born'].min():.0f}-{subset['pct_foreign_born'].max():.0f}%"
        print(f"  {tertile:<8} ({fb_range:<12}): {subset['resilience_score'].mean():+.3f} SD (N = {len(subset):,})")

    # ANOVA
    low = hisp_maj[hisp_maj['fb_tertile'] == 'Low']['resilience_score']
    med = hisp_maj[hisp_maj['fb_tertile'] == 'Medium']['resilience_score']
    high = hisp_maj[hisp_maj['fb_tertile'] == 'High']['resilience_score']

    f_stat, p_val = stats.f_oneway(low, med, high)
    print(f"\nANOVA: F = {f_stat:.2f}, p = {p_val:.2e}")

    # Linear trend
    r, p = stats.pearsonr(hisp_maj['pct_foreign_born'], hisp_maj['resilience_score'])
    print(f"Linear correlation: r = {r:+.3f}, p = {p:.2e}")

    print("\n*** INTERPRETATION ***")
    if p < 0.05 and r > 0:
        print("WITHIN Hispanic communities, higher foreign-born → higher resilience")
        print("→ First-generation immigrants show strongest paradox")
    elif p < 0.05 and r < 0:
        print("WITHIN Hispanic communities, higher foreign-born → LOWER resilience")
        print("→ Paradox NOT driven by immigrant composition")
    else:
        print("No significant relationship between foreign-born % and resilience")
        print("→ Immigrant composition alone doesn't explain Hispanic resilience")

    return {'r_within_hispanic': r, 'p_value': p}


def analysis_6_dominant_origin_comparison(df):
    """Compare resilience by dominant Hispanic origin in tract."""
    print("\n" + "=" * 70)
    print("ANALYSIS 6: Resilience by Dominant Hispanic Origin")
    print("=" * 70)

    # Focus on Hispanic-substantial tracts
    hisp_tracts = df[df['pct_hispanic'] > 20].dropna(subset=['resilience_score', 'dominant_hispanic_origin'])

    print(f"\nIn tracts with >20% Hispanic (N = {len(hisp_tracts):,}):")
    print("-" * 60)
    print(f"{'Dominant Origin':<20} {'N Tracts':<12} {'Mean Resilience':<15} {'SD':<10}")
    print("-" * 60)

    results = []
    for origin in hisp_tracts['dominant_hispanic_origin'].unique():
        subset = hisp_tracts[hisp_tracts['dominant_hispanic_origin'] == origin]
        if len(subset) >= 50:
            print(f"{origin:<20} {len(subset):<12,} {subset['resilience_score'].mean():+.3f}           {subset['resilience_score'].std():.3f}")
            results.append({
                'origin': origin,
                'n': len(subset),
                'mean_resilience': subset['resilience_score'].mean(),
                'sd': subset['resilience_score'].std()
            })

    results_df = pd.DataFrame(results).sort_values('mean_resilience', ascending=False)

    if len(results_df) >= 2:
        best = results_df.iloc[0]
        worst = results_df.iloc[-1]
        print(f"\n*** KEY FINDING ***")
        print(f"Highest resilience: {best['origin']} ({best['mean_resilience']:+.3f} SD)")
        print(f"Lowest resilience:  {worst['origin']} ({worst['mean_resilience']:+.3f} SD)")
        print(f"Gap: {best['mean_resilience'] - worst['mean_resilience']:.3f} SD")

    return results_df


def main():
    print("=" * 70)
    print("PAPER 4B PHASE 2: IMMIGRANT SELECTIVITY ANALYSIS")
    print("=" * 70)

    df = load_all_data()

    # Run all analyses
    fb_results = analysis_1_foreign_born_correlation(df)
    interaction_model = analysis_2_interaction_model(df)
    mex_pr_results = analysis_3_mexican_vs_puerto_rican(df)
    subgroup_results = analysis_4_subgroup_patterns(df)
    within_hisp_results = analysis_5_foreign_born_within_hispanic(df)
    origin_results = analysis_6_dominant_origin_comparison(df)

    # Final verdict
    print("\n" + "=" * 70)
    print("PHASE 2 VERDICT: IMMIGRANT SELECTIVITY HYPOTHESIS")
    print("=" * 70)

    print("""
SUMMARY OF EVIDENCE:

1. FOREIGN-BORN CORRELATION: Does % foreign-born correlate with resilience?
   → If YES, immigrant composition matters

2. INTERACTION EFFECT: Does Hispanic × Foreign-born interaction exist?
   → If YES (positive), immigrants amplify Hispanic resilience

3. MEXICAN vs PUERTO RICAN: Key test of immigrant selection
   → Mexican (immigrants) should show paradox
   → Puerto Rican (US citizens) should NOT if selection is key

4. SUBGROUP PATTERNS: Which Hispanic origins show strongest paradox?
   → Immigrant groups should show stronger effects

5. WITHIN-HISPANIC ANALYSIS: Does foreign-born % matter within Hispanic tracts?
   → Tests generational hypothesis

CONCLUSION: Based on these analyses, the immigrant selectivity hypothesis is:
""")

    # Make verdict based on results
    mex_stronger = mex_pr_results['r_mexican'] > mex_pr_results['r_puerto_rican']
    sig_diff = mex_pr_results['p_difference'] < 0.05
    within_positive = within_hisp_results['r_within_hispanic'] > 0 and within_hisp_results['p_value'] < 0.05

    if mex_stronger and sig_diff and within_positive:
        print("  *** STRONGLY SUPPORTED ***")
        print("  Mexican > Puerto Rican AND foreign-born predicts resilience within Hispanic communities")
    elif mex_stronger or within_positive:
        print("  *** PARTIALLY SUPPORTED ***")
        print("  Some evidence for immigrant selection, but not definitive")
    else:
        print("  *** NOT SUPPORTED ***")
        print("  Hispanic paradox exists independent of immigrant composition")
        print("  Other factors (cultural, social cohesion) likely responsible")

    return {
        'foreign_born': fb_results,
        'interaction_model': interaction_model,
        'mexican_vs_pr': mex_pr_results,
        'subgroups': subgroup_results,
        'within_hispanic': within_hisp_results,
        'by_origin': origin_results
    }


if __name__ == "__main__":
    results = main()
