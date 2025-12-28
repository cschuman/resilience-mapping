#!/usr/bin/env python3
"""
Data-Driven Institutional Filters

Uses actual Census 2020 group quarters data by type to filter tracts
with high institutional populations. NO hardcoded county lists.

Data source: Census PL 94-171 Table P5 (Group Quarters by Major Type)
"""

import pandas as pd
import numpy as np
import os
from typing import Tuple, Dict

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_INPUT = os.path.join(PROJECT_ROOT, 'data', 'input')


def load_gq_data() -> pd.DataFrame:
    """Load Census group quarters data by type."""
    path = os.path.join(DATA_INPUT, 'census_gq_by_type_2020.csv')

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Census GQ data not found at {path}\n"
            "Run download_gq_data.py first to fetch from Census API."
        )

    df = pd.read_csv(path, dtype={'TractFIPS': str})
    df['TractFIPS'] = df['TractFIPS'].str.zfill(11)
    print(f"Loaded Census GQ data: {len(df):,} tracts")
    return df


def apply_data_driven_filters(
    results: pd.DataFrame,
    tract_column: str = 'TractFIPS',
    min_population: int = 500,
    college_threshold: float = 15.0,
    military_threshold: float = 10.0,
    correctional_threshold: float = 10.0,
    nursing_threshold: float = 25.0,
) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Apply data-driven filters using actual Census group quarters data.

    Args:
        results: DataFrame with model results
        tract_column: Column containing tract FIPS
        min_population: Minimum total population
        college_threshold: Max % in college housing
        military_threshold: Max % in military quarters
        correctional_threshold: Max % in correctional facilities
        nursing_threshold: Max % in nursing facilities

    Returns:
        (filtered_df, dict of excluded DataFrames by reason)
    """
    print("=" * 60)
    print("APPLYING DATA-DRIVEN INSTITUTIONAL FILTERS")
    print("Using Census 2020 Group Quarters Data")
    print("=" * 60)

    # Load GQ data
    gq_data = load_gq_data()

    # Normalize tract IDs
    results = results.copy()
    results[tract_column] = results[tract_column].astype(str).str.zfill(11)

    # Select GQ columns to merge
    gq_cols = ['TractFIPS', 'total_pop', 'gq_college', 'gq_military',
               'gq_correctional', 'gq_nursing', 'pct_gq_college',
               'pct_gq_military', 'pct_gq_correctional', 'pct_gq_nursing']

    # Create indicator for matched tracts
    gq_subset = gq_data[gq_cols].copy()
    gq_subset['_matched'] = True

    # Merge with GQ data
    merged = results.merge(
        gq_subset,
        left_on=tract_column,
        right_on='TractFIPS',
        how='left',
        suffixes=('', '_gq')
    )

    # Fill missing GQ data with 0 (tracts not in Census 2020)
    for col in ['total_pop', 'gq_college', 'gq_military', 'gq_correctional',
                'gq_nursing', 'pct_gq_college', 'pct_gq_military',
                'pct_gq_correctional', 'pct_gq_nursing']:
        if col in merged.columns:
            merged[col] = merged[col].fillna(0)

    matched_count = merged['_matched'].fillna(False).sum()
    original_count = len(merged)
    print(f"\nStarting tracts: {original_count:,}")
    print(f"Matched with Census GQ data: {matched_count:,}")

    excluded = {}

    # 1. Low population filter
    print(f"\n1. Population filter (min {min_population:,}):")
    low_pop_mask = merged['total_pop'] < min_population
    excluded['low_population'] = merged[low_pop_mask].copy()
    merged = merged[~low_pop_mask]
    print(f"   Excluded: {len(excluded['low_population']):,} tracts")

    # 2. College housing filter
    print(f"\n2. College housing filter (>{college_threshold}%):")
    college_mask = merged['pct_gq_college'] > college_threshold
    excluded['college_housing'] = merged[college_mask].copy()
    merged = merged[~college_mask]
    print(f"   Excluded: {len(excluded['college_housing']):,} tracts")
    if len(excluded['college_housing']) > 0:
        top_college = excluded['college_housing'].nlargest(5, 'pct_gq_college')
        for _, row in top_college.iterrows():
            print(f"      - {row[tract_column]}: {row['pct_gq_college']:.1f}% college ({int(row['gq_college']):,}/{int(row['total_pop']):,})")

    # 3. Military quarters filter
    print(f"\n3. Military quarters filter (>{military_threshold}%):")
    military_mask = merged['pct_gq_military'] > military_threshold
    excluded['military_quarters'] = merged[military_mask].copy()
    merged = merged[~military_mask]
    print(f"   Excluded: {len(excluded['military_quarters']):,} tracts")
    if len(excluded['military_quarters']) > 0:
        top_military = excluded['military_quarters'].nlargest(5, 'pct_gq_military')
        for _, row in top_military.iterrows():
            print(f"      - {row[tract_column]}: {row['pct_gq_military']:.1f}% military ({int(row['gq_military']):,}/{int(row['total_pop']):,})")

    # 4. Correctional facilities filter
    print(f"\n4. Correctional facilities filter (>{correctional_threshold}%):")
    correctional_mask = merged['pct_gq_correctional'] > correctional_threshold
    excluded['correctional'] = merged[correctional_mask].copy()
    merged = merged[~correctional_mask]
    print(f"   Excluded: {len(excluded['correctional']):,} tracts")

    # 5. Nursing facilities filter (optional, higher threshold)
    print(f"\n5. Nursing facilities filter (>{nursing_threshold}%):")
    nursing_mask = merged['pct_gq_nursing'] > nursing_threshold
    excluded['nursing'] = merged[nursing_mask].copy()
    merged = merged[~nursing_mask]
    print(f"   Excluded: {len(excluded['nursing']):,} tracts")

    # Summary
    total_excluded = sum(len(e) for e in excluded.values())
    print(f"\n{'=' * 60}")
    print("FILTER SUMMARY")
    print("=" * 60)
    print(f"Original tracts:          {original_count:,}")
    print(f"Excluded (low pop):       {len(excluded.get('low_population', [])):,}")
    print(f"Excluded (college):       {len(excluded.get('college_housing', [])):,}")
    print(f"Excluded (military):      {len(excluded.get('military_quarters', [])):,}")
    print(f"Excluded (correctional):  {len(excluded.get('correctional', [])):,}")
    print(f"Excluded (nursing):       {len(excluded.get('nursing', [])):,}")
    print(f"Total excluded:           {total_excluded:,}")
    print(f"Remaining:                {len(merged):,}")

    # Clean up merge columns
    drop_cols = ['TractFIPS_gq', '_matched']
    for col in drop_cols:
        if col in merged.columns:
            merged = merged.drop(columns=[col])

    return merged, excluded


if __name__ == "__main__":
    # Test with sample data
    print("Data-driven filters module loaded successfully")

    # Check if GQ data exists
    try:
        gq = load_gq_data()
        print(f"\nSample tracts with high college %:")
        print(gq.nlargest(5, 'pct_gq_college')[
            ['TractFIPS', 'total_pop', 'gq_college', 'pct_gq_college']
        ].to_string(index=False))
    except FileNotFoundError as e:
        print(f"\n{e}")
