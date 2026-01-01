#!/usr/bin/env python3
"""
Paper 4: Health Equity Analysis

Analyzes structural determinants of community health burden and resilience,
with focus on racial composition, economic factors, and geographic disparities.

Key analyses:
1. Descriptive: CHBI/resilience distribution by demographic quintiles
2. Regression: Hierarchical models (race → SES → place factors)
3. Equity audit: Model performance by community type
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


def load_and_merge_data():
    """Load ACS demographics and merge with resilience scores."""

    # Load ACS demographics
    acs = pd.read_csv("data/external/acs_demographics_2022.csv")
    acs["GEOID"] = acs["GEOID"].astype(str).str.zfill(11)

    # Load resilience scores
    resilience = pd.read_csv("data/processed/model_table_corrected.csv")
    resilience["GEOID"] = resilience["TractFIPS"].astype(str).str.zfill(11)

    # Merge
    merged = acs.merge(resilience, on="GEOID", how="inner")

    print(f"ACS tracts: {len(acs):,}")
    print(f"Resilience tracts: {len(resilience):,}")
    print(f"Merged tracts: {len(merged):,}")

    return merged


def create_quintiles(df: pd.DataFrame) -> pd.DataFrame:
    """Create quintile categories for key variables."""

    # Racial composition quintiles
    df["pct_black_quintile"] = pd.qcut(df["pct_black"], 5, labels=["Q1 (Lowest)", "Q2", "Q3", "Q4", "Q5 (Highest)"], duplicates='drop')
    df["pct_hispanic_quintile"] = pd.qcut(df["pct_hispanic"], 5, labels=["Q1 (Lowest)", "Q2", "Q3", "Q4", "Q5 (Highest)"], duplicates='drop')

    # Majority-minority classification
    df["pct_nonwhite"] = 100 - df["pct_white"]
    df["majority_minority"] = df["pct_nonwhite"] > 50

    # Economic quintiles
    df["income_quintile"] = pd.qcut(df["median_hh_income"], 5, labels=["Q1 (Lowest)", "Q2", "Q3", "Q4", "Q5 (Highest)"], duplicates='drop')
    df["poverty_quintile"] = pd.qcut(df["poverty_rate"], 5, labels=["Q1 (Lowest)", "Q2", "Q3", "Q4", "Q5 (Highest)"], duplicates='drop')

    return df


def descriptive_analysis(df: pd.DataFrame) -> dict:
    """Descriptive statistics by demographic groups."""

    results = {}

    # Overall statistics
    results["overall"] = {
        "n_tracts": len(df),
        "mean_burden": df["burden"].mean(),
        "mean_resilience": df["resilience_score"].mean(),
        "std_resilience": df["resilience_score"].std(),
    }

    # By racial composition quintile (Black)
    print("\n" + "="*60)
    print("BURDEN AND RESILIENCE BY % BLACK POPULATION QUINTILE")
    print("="*60)

    black_stats = df.groupby("pct_black_quintile").agg({
        "burden": ["mean", "std", "count"],
        "resilience_score": ["mean", "std"],
        "pct_black": ["mean"],
        "median_hh_income": ["mean"],
        "poverty_rate": ["mean"],
    }).round(3)
    print(black_stats)
    results["by_pct_black"] = black_stats.to_dict()

    # By Hispanic composition quintile
    print("\n" + "="*60)
    print("BURDEN AND RESILIENCE BY % HISPANIC POPULATION QUINTILE")
    print("="*60)

    hispanic_stats = df.groupby("pct_hispanic_quintile").agg({
        "burden": ["mean", "std", "count"],
        "resilience_score": ["mean", "std"],
        "pct_hispanic": ["mean"],
        "median_hh_income": ["mean"],
        "poverty_rate": ["mean"],
    }).round(3)
    print(hispanic_stats)
    results["by_pct_hispanic"] = hispanic_stats.to_dict()

    # Majority-minority comparison
    print("\n" + "="*60)
    print("MAJORITY-MINORITY vs MAJORITY-WHITE COMPARISON")
    print("="*60)

    mm_stats = df.groupby("majority_minority").agg({
        "burden": ["mean", "std", "count"],
        "resilience_score": ["mean", "std"],
        "pct_nonwhite": ["mean"],
        "median_hh_income": ["mean"],
        "poverty_rate": ["mean"],
    }).round(3)
    mm_stats.index = ["Majority White", "Majority-Minority"]
    print(mm_stats)
    results["majority_minority"] = mm_stats.to_dict()

    # T-test for resilience difference
    white_majority = df[~df["majority_minority"]]["resilience_score"]
    minority_majority = df[df["majority_minority"]]["resilience_score"]
    t_stat, p_value = stats.ttest_ind(white_majority, minority_majority)

    print(f"\nT-test for resilience difference: t={t_stat:.2f}, p={p_value:.2e}")
    print(f"  Majority White mean: {white_majority.mean():.3f}")
    print(f"  Majority-Minority mean: {minority_majority.mean():.3f}")
    print(f"  Difference: {white_majority.mean() - minority_majority.mean():.3f} SD")

    results["ttest"] = {"t_stat": t_stat, "p_value": p_value}

    return results


def correlation_analysis(df: pd.DataFrame) -> dict:
    """Correlation between demographics and health outcomes."""

    print("\n" + "="*60)
    print("CORRELATIONS: DEMOGRAPHICS → HEALTH OUTCOMES")
    print("="*60)

    demo_vars = ["pct_black", "pct_hispanic", "pct_white", "pct_nonwhite",
                 "median_hh_income", "poverty_rate", "unemployment_rate",
                 "pct_renter", "pct_bachelors_plus"]

    outcome_vars = ["burden", "resilience_score"]

    results = {}

    for outcome in outcome_vars:
        print(f"\n{outcome.upper()}:")
        for demo in demo_vars:
            if demo in df.columns:
                valid = df[[demo, outcome]].dropna()
                r, p = stats.pearsonr(valid[demo], valid[outcome])
                sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
                print(f"  {demo:25s}: r = {r:+.3f} {sig}")
                results[f"{outcome}_{demo}"] = {"r": r, "p": p}

    return results


def concentration_analysis(df: pd.DataFrame) -> dict:
    """What share of health burden is concentrated in communities of color?"""

    print("\n" + "="*60)
    print("BURDEN CONCENTRATION ANALYSIS")
    print("="*60)

    # Total burden (sum of burden * population weight)
    df["weighted_burden"] = df["burden"] * df["total_population"]
    total_burden = df["weighted_burden"].sum()
    total_pop = df["total_population"].sum()

    # Burden in majority-minority communities
    mm = df[df["majority_minority"]]
    mm_burden = mm["weighted_burden"].sum()
    mm_pop = mm["total_population"].sum()

    # Burden in high-burden tracts (top 25%)
    high_burden_threshold = df["burden"].quantile(0.75)
    high_burden = df[df["burden"] >= high_burden_threshold]

    print(f"Total population: {total_pop:,.0f}")
    print(f"Majority-minority population: {mm_pop:,.0f} ({mm_pop/total_pop*100:.1f}%)")
    print(f"\nShare of total burden in majority-minority communities: {mm_burden/total_burden*100:.1f}%")

    # Demographics of high-burden tracts
    print(f"\nHigh-burden tracts (top 25%, burden >= {high_burden_threshold:.2f}):")
    print(f"  N tracts: {len(high_burden):,}")
    print(f"  Mean % Black: {high_burden['pct_black'].mean():.1f}%")
    print(f"  Mean % Hispanic: {high_burden['pct_hispanic'].mean():.1f}%")
    print(f"  Mean % Majority-minority: {high_burden['majority_minority'].mean()*100:.1f}%")
    print(f"  Mean income: ${high_burden['median_hh_income'].mean():,.0f}")
    print(f"  Mean poverty rate: {high_burden['poverty_rate'].mean():.1f}%")

    # Compare to overall
    print(f"\nOverall averages:")
    print(f"  Mean % Black: {df['pct_black'].mean():.1f}%")
    print(f"  Mean % Hispanic: {df['pct_hispanic'].mean():.1f}%")
    print(f"  Mean income: ${df['median_hh_income'].mean():,.0f}")
    print(f"  Mean poverty rate: {df['poverty_rate'].mean():.1f}%")

    return {
        "mm_share_of_burden": mm_burden/total_burden,
        "mm_share_of_pop": mm_pop/total_pop,
        "high_burden_pct_black": high_burden['pct_black'].mean(),
        "high_burden_pct_mm": high_burden['majority_minority'].mean(),
    }


def resilience_equity_analysis(df: pd.DataFrame) -> dict:
    """Are positive resilience outliers equitably distributed?"""

    print("\n" + "="*60)
    print("RESILIENCE EQUITY: WHO ARE THE POSITIVE OUTLIERS?")
    print("="*60)

    # High resilience = top 10%
    high_res_threshold = df["resilience_score"].quantile(0.90)
    high_res = df[df["resilience_score"] >= high_res_threshold]

    # Low resilience = bottom 10%
    low_res_threshold = df["resilience_score"].quantile(0.10)
    low_res = df[df["resilience_score"] <= low_res_threshold]

    print(f"High resilience tracts (top 10%, score >= {high_res_threshold:.2f}):")
    print(f"  N tracts: {len(high_res):,}")
    print(f"  Mean % Black: {high_res['pct_black'].mean():.1f}% (overall: {df['pct_black'].mean():.1f}%)")
    print(f"  Mean % Hispanic: {high_res['pct_hispanic'].mean():.1f}% (overall: {df['pct_hispanic'].mean():.1f}%)")
    print(f"  Mean % White: {high_res['pct_white'].mean():.1f}% (overall: {df['pct_white'].mean():.1f}%)")
    print(f"  Mean income: ${high_res['median_hh_income'].mean():,.0f} (overall: ${df['median_hh_income'].mean():,.0f})")
    print(f"  Mean poverty: {high_res['poverty_rate'].mean():.1f}% (overall: {df['poverty_rate'].mean():.1f}%)")
    print(f"  % Majority-minority: {high_res['majority_minority'].mean()*100:.1f}% (overall: {df['majority_minority'].mean()*100:.1f}%)")

    print(f"\nLow resilience tracts (bottom 10%, score <= {low_res_threshold:.2f}):")
    print(f"  N tracts: {len(low_res):,}")
    print(f"  Mean % Black: {low_res['pct_black'].mean():.1f}%")
    print(f"  Mean % Hispanic: {low_res['pct_hispanic'].mean():.1f}%")
    print(f"  Mean % White: {low_res['pct_white'].mean():.1f}%")
    print(f"  Mean income: ${low_res['median_hh_income'].mean():,.0f}")
    print(f"  Mean poverty: {low_res['poverty_rate'].mean():.1f}%")
    print(f"  % Majority-minority: {low_res['majority_minority'].mean()*100:.1f}%")

    # Chi-square: Are high resilience tracts less likely to be majority-minority?
    contingency = pd.crosstab(
        df["resilience_score"] >= high_res_threshold,
        df["majority_minority"]
    )
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency)

    print(f"\nChi-square test (High resilience × Majority-minority):")
    print(f"  χ² = {chi2:.1f}, p = {p_value:.2e}")

    return {
        "high_res_pct_black": high_res['pct_black'].mean(),
        "high_res_pct_mm": high_res['majority_minority'].mean(),
        "low_res_pct_black": low_res['pct_black'].mean(),
        "low_res_pct_mm": low_res['majority_minority'].mean(),
        "chi2": chi2,
        "chi2_p": p_value,
    }


def state_equity_comparison(df: pd.DataFrame) -> dict:
    """Compare equity patterns across states."""

    print("\n" + "="*60)
    print("STATE-LEVEL EQUITY PATTERNS")
    print("="*60)

    # Calculate gap between majority-white and majority-minority resilience by state
    state_gaps = []

    for state in df["StateAbbr"].unique():
        state_df = df[df["StateAbbr"] == state]

        white_maj = state_df[~state_df["majority_minority"]]["resilience_score"]
        mm = state_df[state_df["majority_minority"]]["resilience_score"]

        if len(white_maj) > 10 and len(mm) > 10:
            gap = white_maj.mean() - mm.mean()
            state_gaps.append({
                "state": state,
                "gap": gap,
                "n_white_maj": len(white_maj),
                "n_mm": len(mm),
                "white_maj_mean": white_maj.mean(),
                "mm_mean": mm.mean(),
            })

    gaps_df = pd.DataFrame(state_gaps).sort_values("gap", ascending=False)

    print("\nStates with LARGEST resilience gaps (White-majority advantage):")
    print(gaps_df.head(10).to_string(index=False))

    print("\nStates with SMALLEST gaps (most equitable):")
    print(gaps_df.tail(10).to_string(index=False))

    return {"state_gaps": gaps_df.to_dict("records")}


def summary_statistics(df: pd.DataFrame) -> None:
    """Print key summary statistics for the paper."""

    print("\n" + "="*60)
    print("KEY STATISTICS FOR PAPER 4")
    print("="*60)

    # Correlation between race and burden
    r_black_burden, _ = stats.pearsonr(df["pct_black"].dropna(), df["burden"].dropna())
    r_black_res, _ = stats.pearsonr(df["pct_black"].dropna(), df["resilience_score"].dropna())

    r_income_burden, _ = stats.pearsonr(df["median_hh_income"].dropna(), df["burden"].dropna())
    r_income_res, _ = stats.pearsonr(df["median_hh_income"].dropna(), df["resilience_score"].dropna())

    print(f"\n1. RACIAL DISPARITIES IN HEALTH BURDEN:")
    print(f"   Correlation (% Black → Burden): r = {r_black_burden:+.3f}")
    print(f"   Correlation (% Black → Resilience): r = {r_black_res:+.3f}")

    print(f"\n2. ECONOMIC DISPARITIES:")
    print(f"   Correlation (Income → Burden): r = {r_income_burden:+.3f}")
    print(f"   Correlation (Income → Resilience): r = {r_income_res:+.3f}")

    # Burden concentration
    mm = df[df["majority_minority"]]
    mm_share = len(mm) / len(df) * 100
    mm_high_burden = df[(df["majority_minority"]) & (df["burden"] >= df["burden"].quantile(0.75))]
    mm_high_burden_share = len(mm_high_burden) / len(df[df["burden"] >= df["burden"].quantile(0.75)]) * 100

    print(f"\n3. BURDEN CONCENTRATION:")
    print(f"   Majority-minority tracts: {mm_share:.1f}% of all tracts")
    print(f"   Majority-minority share of high-burden tracts: {mm_high_burden_share:.1f}%")

    # Resilience gap
    white_res = df[~df["majority_minority"]]["resilience_score"].mean()
    mm_res = df[df["majority_minority"]]["resilience_score"].mean()

    print(f"\n4. RESILIENCE GAP:")
    print(f"   Majority-White mean resilience: {white_res:+.3f}")
    print(f"   Majority-Minority mean resilience: {mm_res:+.3f}")
    print(f"   Gap: {white_res - mm_res:.3f} standard deviations")


def save_results(df: pd.DataFrame) -> None:
    """Save merged dataset for further analysis."""

    output_path = Path("data/processed/equity_analysis_dataset.csv")
    df.to_csv(output_path, index=False)
    print(f"\nSaved merged dataset to {output_path}")


def main():
    """Run complete Paper 4 equity analysis."""

    print("="*60)
    print("PAPER 4: HEALTH EQUITY ANALYSIS")
    print("="*60)

    # Load and merge data
    df = load_and_merge_data()

    # Create quintiles
    df = create_quintiles(df)

    # Run analyses
    desc_results = descriptive_analysis(df)
    corr_results = correlation_analysis(df)
    conc_results = concentration_analysis(df)
    equity_results = resilience_equity_analysis(df)
    state_results = state_equity_comparison(df)

    # Summary
    summary_statistics(df)

    # Save dataset
    save_results(df)

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
