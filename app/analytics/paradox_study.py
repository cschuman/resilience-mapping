#!/usr/bin/env python3
"""
Paradox Study: Tracts with GOOD food access but POOR health outcomes

This is the inverse of the core resilience finding. Instead of asking
"who thrives despite barriers?", we ask "who struggles despite advantages?"

Key question: Why do some communities with excellent food access
still have poor health outcomes?
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Paths
DATA_DIR = Path(__file__).parent.parent.parent / "data"
OUTPUT_DIR = DATA_DIR / "processed" / "paradox_study"
OUTPUT_DIR.mkdir(exist_ok=True)


def load_data():
    """Load model results and food access data."""
    print("=" * 70)
    print("PARADOX STUDY: Good Food Access, Poor Health Outcomes")
    print("=" * 70)
    print("\nLoading data...")

    # Load model results (use corrected version)
    model = pd.read_csv(DATA_DIR / "processed" / "model_table_corrected.csv")
    model['GEOID'] = model['GEOID'].astype(str).str.zfill(11)
    print(f"  Model table: {len(model):,} tracts")

    # Load FARA data for food access indicators
    fara = pd.read_csv(DATA_DIR / "input" / "fara_2019.csv")
    fara['GEOID'] = fara['CensusTract'].astype(str).str.zfill(11)
    print(f"  FARA data: {len(fara):,} tracts")

    # Load ACS demographics for context
    acs_path = DATA_DIR / "external" / "acs_demographics_2022.csv"
    if acs_path.exists():
        acs = pd.read_csv(acs_path)
        acs['GEOID'] = acs['GEOID'].astype(str).str.zfill(11)
        print(f"  ACS demographics: {len(acs):,} tracts")
    else:
        acs = None
        print("  ACS demographics: not found")

    return model, fara, acs


def merge_datasets(model, fara, acs):
    """Merge model results with food access and demographics."""
    print("\nMerging datasets...")

    # Select key FARA columns
    fara_cols = [
        'GEOID', 'State', 'County', 'Urban', 'Pop2010',
        'LILATracts_1And10', 'LILATracts_halfAnd10', 'LILATracts_1And20',
        'LowIncomeTracts', 'PovertyRate', 'MedianFamilyIncome'
    ]
    fara_subset = fara[fara_cols].copy()

    # Convert LILA columns to numeric
    for col in ['LILATracts_1And10', 'LILATracts_halfAnd10', 'LILATracts_1And20', 'LowIncomeTracts']:
        fara_subset[col] = pd.to_numeric(fara_subset[col], errors='coerce').fillna(0)

    # Merge
    merged = model.merge(fara_subset, on='GEOID', how='left')
    print(f"  After FARA merge: {len(merged):,} tracts")

    if acs is not None:
        merged = merged.merge(acs, on='GEOID', how='left')
        print(f"  After ACS merge: {len(merged):,} tracts")

    return merged


def identify_paradox_tracts(df):
    """
    Identify paradox tracts: good food access but poor health outcomes.

    Criteria:
    - NOT LILA (good food access): LILATracts_1And10 == 0
    - Poor health: resilience_score < -1.0 (more than 1 SD worse than expected)
    """
    print("\n" + "=" * 70)
    print("IDENTIFYING PARADOX TRACTS")
    print("=" * 70)

    # Filter to tracts with complete data
    df_valid = df.dropna(subset=['LILATracts_1And10', 'resilience_score'])
    print(f"\nTracts with complete data: {len(df_valid):,}")

    # Define good food access (NOT LILA)
    good_access = df_valid[df_valid['LILATracts_1And10'] == 0].copy()
    print(f"Tracts with good food access (not LILA): {len(good_access):,}")

    # Define poor health outcomes (negative resilience = worse than expected)
    # Using different thresholds
    thresholds = {
        'mild': -0.5,      # 0.5 SD worse than expected
        'moderate': -1.0,  # 1 SD worse than expected
        'severe': -1.5,    # 1.5 SD worse than expected
        'extreme': -2.0    # 2 SD worse than expected
    }

    print("\nParadox tract counts by severity:")
    paradox_counts = {}
    for name, threshold in thresholds.items():
        count = (good_access['resilience_score'] < threshold).sum()
        pct = count / len(good_access) * 100
        paradox_counts[name] = count
        print(f"  {name.capitalize()} (<{threshold}): {count:,} tracts ({pct:.1f}%)")

    # Use moderate threshold (-1.0 SD) as primary definition
    paradox = good_access[good_access['resilience_score'] < -1.0].copy()
    print(f"\n*** Primary paradox tracts (moderate): {len(paradox):,} ***")

    return paradox, good_access


def analyze_paradox_characteristics(paradox, good_access):
    """Analyze what distinguishes paradox tracts."""
    print("\n" + "=" * 70)
    print("PARADOX TRACT CHARACTERISTICS")
    print("=" * 70)

    # Compare paradox vs. non-paradox within good-access tracts
    non_paradox = good_access[good_access['resilience_score'] >= -1.0]

    print(f"\nComparison: Paradox (n={len(paradox):,}) vs Non-Paradox (n={len(non_paradox):,})")
    print("-" * 50)

    # Numeric comparisons
    compare_cols = ['burden', 'resilience_score', 'PovertyRate', 'MedianFamilyIncome', 'Pop2010']

    for col in compare_cols:
        if col in paradox.columns:
            p_mean = paradox[col].mean()
            np_mean = non_paradox[col].mean()
            if pd.notna(p_mean) and pd.notna(np_mean):
                diff = p_mean - np_mean
                pct_diff = (diff / np_mean * 100) if np_mean != 0 else 0
                print(f"\n{col}:")
                print(f"  Paradox mean:     {p_mean:,.2f}")
                print(f"  Non-paradox mean: {np_mean:,.2f}")
                print(f"  Difference:       {diff:+,.2f} ({pct_diff:+.1f}%)")

    # Urban vs rural
    if 'Urban' in paradox.columns:
        print("\nUrban/Rural distribution:")
        p_urban = (paradox['Urban'] == 1).mean() * 100
        np_urban = (non_paradox['Urban'] == 1).mean() * 100
        print(f"  Paradox urban:     {p_urban:.1f}%")
        print(f"  Non-paradox urban: {np_urban:.1f}%")

    # State distribution
    print("\nTop 10 states with most paradox tracts:")
    state_counts = paradox['StateAbbr'].value_counts().head(10)
    for state, count in state_counts.items():
        pct = count / len(paradox) * 100
        print(f"  {state}: {count} ({pct:.1f}%)")

    return state_counts


def identify_extreme_cases(paradox):
    """Identify the most extreme paradox cases for investigation."""
    print("\n" + "=" * 70)
    print("EXTREME PARADOX CASES (Top 50)")
    print("=" * 70)

    # Sort by resilience score (most negative = worst paradox)
    extreme = paradox.nsmallest(50, 'resilience_score').copy()

    # Add readable labels
    extreme['tract_label'] = extreme['StateAbbr'] + '-' + extreme['County'].fillna('Unknown')

    print("\nTop 50 tracts with good food access but worst health outcomes:")
    print("-" * 80)

    display_cols = ['GEOID', 'StateAbbr', 'County', 'burden', 'resilience_score', 'PovertyRate']
    available_cols = [c for c in display_cols if c in extreme.columns]

    for i, (_, row) in enumerate(extreme.head(20).iterrows(), 1):
        print(f"{i:2}. {row['StateAbbr']:2} - {str(row.get('County', 'Unknown'))[:25]:25} "
              f"| Burden: {row['burden']:5.2f} | Resilience: {row['resilience_score']:+6.2f}")

    if len(extreme) > 20:
        print(f"... and {len(extreme) - 20} more")

    return extreme


def compare_to_resilient(paradox, df):
    """Compare paradox tracts to resilient tracts."""
    print("\n" + "=" * 70)
    print("PARADOX vs RESILIENT COMPARISON")
    print("=" * 70)

    # Get resilient tracts (LILA + positive resilience)
    resilient = df[(df['LILATracts_1And10'] == 1) & (df['resilience_score'] > 1.0)]

    print(f"\nResilience paradox:")
    print(f"  Resilient (LILA + good health):      {len(resilient):,} tracts")
    print(f"  Paradox (non-LILA + poor health):    {len(paradox):,} tracts")

    print("\n" + "-" * 50)
    print("Side-by-side comparison:")
    print("-" * 50)

    metrics = [
        ('Health burden (mean)', 'burden'),
        ('Resilience score (mean)', 'resilience_score'),
        ('Poverty rate (%)', 'PovertyRate'),
        ('Median family income ($)', 'MedianFamilyIncome'),
    ]

    for label, col in metrics:
        if col in paradox.columns:
            p_val = paradox[col].mean()
            r_val = resilient[col].mean()
            if pd.notna(p_val) and pd.notna(r_val):
                print(f"\n{label}:")
                print(f"  Paradox:   {p_val:>12,.2f}")
                print(f"  Resilient: {r_val:>12,.2f}")

    return resilient


def generate_hypotheses(paradox, good_access):
    """Generate hypotheses about why paradox tracts exist."""
    print("\n" + "=" * 70)
    print("HYPOTHESES FOR PARADOX TRACTS")
    print("=" * 70)

    hypotheses = []

    # Hypothesis 1: High income doesn't mean healthy behavior
    if 'MedianFamilyIncome' in paradox.columns:
        high_income_paradox = paradox[paradox['MedianFamilyIncome'] > 100000]
        if len(high_income_paradox) > 0:
            hypotheses.append({
                'name': 'Affluent Unhealthy',
                'count': len(high_income_paradox),
                'description': 'High-income tracts with poor health - suggests lifestyle factors (sedentary, over-consumption) matter more than food access'
            })

    # Hypothesis 2: Urban food access doesn't translate to health
    if 'Urban' in paradox.columns:
        urban_paradox = paradox[paradox['Urban'] == 1]
        rural_paradox = paradox[paradox['Urban'] == 0]
        urban_rate = len(urban_paradox) / len(paradox) * 100 if len(paradox) > 0 else 0
        hypotheses.append({
            'name': 'Urban Paradox',
            'count': len(urban_paradox),
            'description': f'{urban_rate:.1f}% of paradox tracts are urban - suggests proximity to food doesn\'t ensure healthy choices'
        })

    # Hypothesis 3: Low poverty but poor health
    if 'PovertyRate' in paradox.columns:
        low_poverty_paradox = paradox[paradox['PovertyRate'] < 10]
        hypotheses.append({
            'name': 'Low-Poverty Unhealthy',
            'count': len(low_poverty_paradox),
            'description': 'Tracts with <10% poverty but poor health - material access doesn\'t guarantee health'
        })

    print("\nGenerated hypotheses:")
    for i, h in enumerate(hypotheses, 1):
        print(f"\n{i}. {h['name']} (n={h['count']:,})")
        print(f"   {h['description']}")

    return hypotheses


def save_outputs(paradox, extreme, good_access):
    """Save analysis outputs."""
    print("\n" + "=" * 70)
    print("SAVING OUTPUTS")
    print("=" * 70)

    # Save full paradox dataset
    paradox_path = OUTPUT_DIR / "paradox_tracts_full.csv"
    paradox.to_csv(paradox_path, index=False)
    print(f"  Saved: {paradox_path}")

    # Save extreme cases
    extreme_path = OUTPUT_DIR / "paradox_tracts_extreme.csv"
    extreme.to_csv(extreme_path, index=False)
    print(f"  Saved: {extreme_path}")

    # Save summary statistics
    summary = {
        'total_good_access_tracts': len(good_access),
        'paradox_tracts': len(paradox),
        'paradox_rate': len(paradox) / len(good_access) * 100,
        'mean_burden_paradox': paradox['burden'].mean(),
        'mean_resilience_paradox': paradox['resilience_score'].mean(),
        'top_state': paradox['StateAbbr'].value_counts().index[0] if len(paradox) > 0 else None
    }

    summary_path = OUTPUT_DIR / "paradox_summary.txt"
    with open(summary_path, 'w') as f:
        f.write("PARADOX STUDY SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        for k, v in summary.items():
            f.write(f"{k}: {v}\n")
    print(f"  Saved: {summary_path}")

    return summary


def main():
    """Run the paradox study analysis."""
    # Load data
    model, fara, acs = load_data()

    # Merge datasets
    df = merge_datasets(model, fara, acs)

    # Identify paradox tracts
    paradox, good_access = identify_paradox_tracts(df)

    if len(paradox) == 0:
        print("\nNo paradox tracts found!")
        return

    # Analyze characteristics
    state_counts = analyze_paradox_characteristics(paradox, good_access)

    # Identify extreme cases
    extreme = identify_extreme_cases(paradox)

    # Compare to resilient tracts
    resilient = compare_to_resilient(paradox, df)

    # Generate hypotheses
    hypotheses = generate_hypotheses(paradox, good_access)

    # Save outputs
    summary = save_outputs(paradox, extreme, good_access)

    # Final summary
    print("\n" + "=" * 70)
    print("PARADOX STUDY COMPLETE")
    print("=" * 70)
    print(f"""
KEY FINDINGS:
- {len(paradox):,} tracts have good food access but poor health outcomes
- This represents {summary['paradox_rate']:.1f}% of non-LILA tracts
- Mean health burden in paradox tracts: {summary['mean_burden_paradox']:.2f}
- Most affected state: {summary['top_state']}

NEXT STEPS:
1. Deep dive into extreme cases
2. Correlate with additional variables (car ownership, walkability, etc.)
3. Compare urban vs rural paradox patterns
4. Investigate temporal stability (are these tracts consistently paradoxical?)
""")


if __name__ == "__main__":
    main()
