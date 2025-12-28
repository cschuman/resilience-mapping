#!/usr/bin/env python3
"""
Run Enhanced Analysis with Improved Filters

This script applies the enhanced institutional filters to find
ACTUAL resilient communities (not military or student housing).
"""

import pandas as pd
import numpy as np
import os
import sys

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_INPUT = os.path.join(PROJECT_ROOT, 'data', 'input')
DATA_PROCESSED = os.path.join(PROJECT_ROOT, 'data', 'processed')

from enhanced_filters import (
    filter_low_population,
    filter_military_counties,
    MILITARY_COUNTIES,
    UNIVERSITY_COUNTIES
)


def load_corrected_results():
    """Load the corrected model results."""
    path = os.path.join(DATA_PROCESSED, 'model_table_corrected.csv')
    df = pd.read_csv(path)
    print(f"Loaded {len(df):,} tracts from corrected model")
    return df


def load_fara_data():
    """Load FARA data for additional filtering."""
    path = os.path.join(DATA_INPUT, 'fara_2019.csv')
    df = pd.read_csv(path, low_memory=False)
    print(f"Loaded {len(df):,} tracts from FARA")
    return df


def apply_enhanced_filters(results, fara):
    """Apply enhanced filters to find valid resilient communities."""
    print("\n" + "=" * 60)
    print("APPLYING ENHANCED INSTITUTIONAL FILTERS")
    print("=" * 60)

    # Merge results with FARA for additional data
    results['TractFIPS'] = results['TractFIPS'].astype(str).str.zfill(11)
    fara['GEOID'] = fara['CensusTract'].astype(str).str.zfill(11)

    merged = results.merge(
        fara[['GEOID', 'Pop2010', 'State', 'County', 'PCTGQTRS']],
        left_on='TractFIPS',
        right_on='GEOID',
        how='left'
    )

    original_count = len(merged)
    print(f"\nStarting tracts: {original_count:,}")

    # 1. Filter low population
    merged, exc_pop = filter_low_population(merged, min_population=500, pop_column='Pop2010')

    # 2. Filter military counties
    merged, exc_mil = filter_military_counties(merged, tract_column='TractFIPS')

    # 3. Filter known university counties
    print("\nUniversity county filter:")
    merged['_tract_str'] = merged['TractFIPS'].astype(str).str.zfill(11)
    merged['_state_fips'] = merged['_tract_str'].str[:2]
    merged['_county_fips'] = merged['_tract_str'].str[2:5]

    def is_university_county(row):
        key = (row['_state_fips'], row['_county_fips'])
        return key in UNIVERSITY_COUNTIES

    merged['_is_university'] = merged.apply(is_university_county, axis=1)
    exc_uni = merged[merged['_is_university']].copy()
    merged = merged[~merged['_is_university']].copy()

    print(f"  Excluded: {len(exc_uni):,} tracts")
    print(f"  Remaining: {len(merged):,} tracts")

    # Clean up temp columns
    for col in ['_tract_str', '_state_fips', '_county_fips', '_is_university']:
        merged = merged.drop(columns=[col], errors='ignore')

    # Summary
    total_excluded = original_count - len(merged)
    print(f"\n--- Enhanced Filter Summary ---")
    print(f"Original: {original_count:,}")
    print(f"Excluded (low pop): {len(exc_pop):,}")
    print(f"Excluded (military): {len(exc_mil):,}")
    print(f"Excluded (university): {len(exc_uni):,}")
    print(f"Total excluded: {total_excluded:,}")
    print(f"Remaining: {len(merged):,}")

    return merged


def identify_valid_resilient(df, top_n=100):
    """Identify the top N valid resilient communities."""
    print("\n" + "=" * 60)
    print("TOP VALID RESILIENT COMMUNITIES")
    print("=" * 60)

    # Get top resilient after filters
    top = df.nlargest(top_n, 'resilience_score').copy()

    print(f"\nTop {top_n} Resilient Tracts (after enhanced filters):")
    print(f"  Mean score: {top['resilience_score'].mean():.3f}")
    print(f"  Min score: {top['resilience_score'].min():.3f}")
    print(f"  States represented: {top['StateAbbr'].nunique()}")

    # Display top 20
    print(f"\n--- TOP 20 FOR VALIDATION ---")
    display_cols = ['TractFIPS', 'StateAbbr', 'County', 'resilience_score', 'burden', 'Pop2010']
    available_cols = [c for c in display_cols if c in top.columns]
    print(top.head(20)[available_cols].to_string())

    # Save
    output_path = os.path.join(DATA_PROCESSED, 'top_100_valid_resilient.csv')
    top.to_csv(output_path, index=False)
    print(f"\nSaved: {output_path}")

    return top


def compare_before_after(original_top, filtered_top):
    """Compare top tracts before and after enhanced filters."""
    print("\n" + "=" * 60)
    print("COMPARISON: BEFORE vs AFTER ENHANCED FILTERS")
    print("=" * 60)

    # How many of original top 20 survived?
    original_ids = set(original_top.head(20)['TractFIPS'].astype(str))
    filtered_ids = set(filtered_top.head(100)['TractFIPS'].astype(str))

    survived = original_ids & filtered_ids
    excluded = original_ids - filtered_ids

    print(f"\nOf original top 20:")
    print(f"  Survived filters: {len(survived)}")
    print(f"  Excluded: {len(excluded)}")

    if excluded:
        print(f"\n  Excluded tracts: {', '.join(sorted(excluded)[:5])}...")


def main():
    print("=" * 60)
    print("ENHANCED RESILIENCE ANALYSIS")
    print("Finding VALID Resilient Communities")
    print("=" * 60)

    # Load data
    results = load_corrected_results()
    fara = load_fara_data()

    # Load original top 100 for comparison
    original_top_path = os.path.join(DATA_PROCESSED, 'top_100_resilient_corrected.csv')
    if os.path.exists(original_top_path):
        original_top = pd.read_csv(original_top_path)
    else:
        original_top = results.nlargest(100, 'resilience_score')

    # Apply enhanced filters
    filtered = apply_enhanced_filters(results, fara)

    # Identify valid resilient communities
    valid_top = identify_valid_resilient(filtered)

    # Compare
    compare_before_after(original_top, valid_top)

    # Final summary
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"\nFiles generated:")
    print(f"  - {DATA_PROCESSED}/top_100_valid_resilient.csv")

    return valid_top


if __name__ == "__main__":
    valid_top = main()
