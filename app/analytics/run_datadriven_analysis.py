#!/usr/bin/env python3
"""
Run Analysis with Data-Driven Filters

Uses actual Census group quarters data instead of hardcoded county lists.
This is the scalable, production-ready approach.
"""

import pandas as pd
import numpy as np
import os

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PROCESSED = os.path.join(PROJECT_ROOT, 'data', 'processed')

from data_driven_filters import apply_data_driven_filters


def load_corrected_results():
    """Load the corrected model results."""
    path = os.path.join(DATA_PROCESSED, 'model_table_corrected.csv')
    df = pd.read_csv(path, dtype={'TractFIPS': str})
    df['TractFIPS'] = df['TractFIPS'].str.zfill(11)
    print(f"Loaded {len(df):,} tracts from corrected model")
    return df


def identify_valid_resilient(df, top_n=100):
    """Identify the top N valid resilient communities."""
    print("\n" + "=" * 60)
    print("TOP VALID RESILIENT COMMUNITIES")
    print("=" * 60)

    # Get top resilient after filters
    top = df.nlargest(top_n, 'resilience_score').copy()

    print(f"\nTop {top_n} Resilient Tracts (after data-driven filters):")
    print(f"  Mean score: {top['resilience_score'].mean():.3f}")
    print(f"  Min score: {top['resilience_score'].min():.3f}")
    print(f"  Max score: {top['resilience_score'].max():.3f}")
    print(f"  States represented: {top['StateAbbr'].nunique()}")

    # Display top 20
    print(f"\n--- TOP 20 FOR VALIDATION ---")
    display_cols = ['TractFIPS', 'StateAbbr', 'resilience_score', 'burden',
                    'pct_gq_college', 'pct_gq_military', 'total_pop']
    available_cols = [c for c in display_cols if c in top.columns]
    print(top.head(20)[available_cols].to_string())

    # Save
    output_path = os.path.join(DATA_PROCESSED, 'top_100_valid_datadriven.csv')
    top.to_csv(output_path, index=False)
    print(f"\nSaved: {output_path}")

    return top


def compare_with_hardcoded(datadriven_top, hardcoded_path):
    """Compare data-driven results with hardcoded filter results."""
    if not os.path.exists(hardcoded_path):
        return

    print("\n" + "=" * 60)
    print("COMPARISON: DATA-DRIVEN vs HARDCODED FILTERS")
    print("=" * 60)

    hardcoded_top = pd.read_csv(hardcoded_path, dtype={'TractFIPS': str})

    dd_ids = set(datadriven_top.head(20)['TractFIPS'].astype(str))
    hc_ids = set(hardcoded_top.head(20)['TractFIPS'].astype(str))

    overlap = dd_ids & hc_ids
    only_dd = dd_ids - hc_ids
    only_hc = hc_ids - dd_ids

    print(f"\nTop 20 comparison:")
    print(f"  Overlap: {len(overlap)} tracts")
    print(f"  Only in data-driven: {len(only_dd)}")
    print(f"  Only in hardcoded: {len(only_hc)}")


def main():
    print("=" * 60)
    print("DATA-DRIVEN RESILIENCE ANALYSIS")
    print("Using Census 2020 Group Quarters Data")
    print("=" * 60)

    # Load model results
    results = load_corrected_results()

    # Apply data-driven filters
    filtered, excluded = apply_data_driven_filters(
        results,
        tract_column='TractFIPS',
        min_population=500,
        college_threshold=15.0,    # >15% in college housing
        military_threshold=10.0,   # >10% in military quarters
        correctional_threshold=10.0,  # >10% in correctional facilities
        nursing_threshold=50.0,    # >50% in nursing (high threshold)
    )

    # Identify valid resilient communities
    valid_top = identify_valid_resilient(filtered)

    # Compare with hardcoded results
    hardcoded_path = os.path.join(DATA_PROCESSED, 'top_100_valid_resilient.csv')
    compare_with_hardcoded(valid_top, hardcoded_path)

    # Final summary
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"\nFiles generated:")
    print(f"  - {DATA_PROCESSED}/top_100_valid_datadriven.csv")

    # Key insight
    print("\n" + "=" * 60)
    print("KEY IMPROVEMENT")
    print("=" * 60)
    print("""
This analysis uses REAL Census data:
- College housing: Actual % in dorms/student housing
- Military quarters: Actual % in on-base housing
- Correctional: Actual % in prisons/jails

NO hardcoded county lists needed. Scales to entire US automatically.
    """)

    return valid_top


if __name__ == "__main__":
    valid_top = main()
