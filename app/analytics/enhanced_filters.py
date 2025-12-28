#!/usr/bin/env python3
"""
Enhanced Institutional Filters

The basic >10% group quarters filter misses:
1. Military family housing (not counted as group quarters)
2. Off-campus student apartments (not counted as group quarters)

This module adds additional filters based on demographic signatures.
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Dict


# Known military installation counties (partial list - major bases)
MILITARY_COUNTIES = {
    # Format: (State FIPS, County FIPS): "Base Name"
    ("22", "115"): "Fort Johnson (Vernon Parish, LA)",
    ("37", "133"): "Camp Lejeune (Onslow County, NC)",
    ("37", "049"): "MCAS Cherry Point (Craven County, NC)",
    ("45", "015"): "Naval Weapons Station Charleston (Berkeley County, SC)",
    ("45", "019"): "Fort Jackson (Charleston County, SC)",
    ("13", "051"): "Fort Benning (Chattahoochee County, GA)",
    ("48", "027"): "Fort Hood (Bell County, TX)",
    ("06", "073"): "Camp Pendleton (San Diego County, CA)",
    ("51", "153"): "Fort Belvoir (Prince William County, VA)",
    ("15", "003"): "Multiple bases (Honolulu County, HI)",
    ("32", "003"): "Nellis AFB (Clark County, NV)",
    ("12", "033"): "NAS Jacksonville (Duval County, FL)",
    ("47", "125"): "Fort Campbell (Montgomery County, TN)",
    ("35", "013"): "Cannon AFB (Curry County, NM)",
    # Added after validation round 2
    ("45", "013"): "MCAS Beaufort/Parris Island (Beaufort County, SC)",
    ("32", "001"): "NAS Fallon (Churchill County, NV)",
    ("28", "087"): "Columbus AFB (Lowndes County, MS)",
}

# Major university counties (with large student populations)
UNIVERSITY_COUNTIES = {
    ("39", "049"): "Ohio State University (Franklin County, OH)",
    ("01", "081"): "Auburn University (Lee County, AL)",
    ("42", "101"): "Multiple universities (Philadelphia County, PA)",
    ("26", "161"): "University of Michigan (Washtenaw County, MI)",
    ("17", "019"): "University of Illinois (Champaign County, IL)",
    ("48", "041"): "Texas A&M (Brazos County, TX)",
    ("13", "059"): "University of Georgia (Clarke County, GA)",
    ("21", "067"): "University of Kentucky (Fayette County, KY)",
    ("36", "109"): "Cornell University (Tompkins County, NY)",
    ("19", "103"): "University of Iowa (Johnson County, IA)",
    # Added after validation round 2
    ("19", "169"): "Iowa State University (Story County, IA)",
    ("54", "061"): "West Virginia University (Monongalia County, WV)",
    ("26", "065"): "Michigan State University (Ingham County, MI)",
    ("18", "157"): "Tippecanoe County (Purdue University, IN)",
}


def filter_low_population(
    df: pd.DataFrame,
    min_population: int = 500,
    pop_column: str = 'Pop2010'
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Filter tracts with population too low for meaningful analysis.

    Args:
        df: DataFrame with tract data
        min_population: Minimum population threshold
        pop_column: Name of population column

    Returns:
        (filtered_df, excluded_df)
    """
    if pop_column not in df.columns:
        print(f"WARNING: {pop_column} not found, skipping population filter")
        return df, pd.DataFrame()

    df[pop_column] = pd.to_numeric(df[pop_column], errors='coerce').fillna(0)

    excluded = df[df[pop_column] < min_population].copy()
    filtered = df[df[pop_column] >= min_population].copy()

    print(f"Population filter (min {min_population}):")
    print(f"  Excluded: {len(excluded):,} tracts")
    print(f"  Remaining: {len(filtered):,} tracts")

    return filtered, excluded


def filter_military_counties(
    df: pd.DataFrame,
    tract_column: str = 'CensusTract'
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Filter tracts in counties with major military installations.

    Military family housing doesn't count as group quarters but
    exhibits similar non-transferable resilience patterns.

    Args:
        df: DataFrame with tract data
        tract_column: Name of tract ID column

    Returns:
        (filtered_df, excluded_df)
    """
    df = df.copy()

    # Extract state and county FIPS from tract ID
    df['_tract_str'] = df[tract_column].astype(str).str.zfill(11)
    df['_state_fips'] = df['_tract_str'].str[:2]
    df['_county_fips'] = df['_tract_str'].str[2:5]

    # Check if in military county
    def is_military_county(row):
        key = (row['_state_fips'], row['_county_fips'])
        return key in MILITARY_COUNTIES

    df['_is_military'] = df.apply(is_military_county, axis=1)

    excluded = df[df['_is_military']].copy()
    filtered = df[~df['_is_military']].copy()

    # Clean up temp columns
    for col in ['_tract_str', '_state_fips', '_county_fips', '_is_military']:
        filtered = filtered.drop(columns=[col], errors='ignore')
        excluded = excluded.drop(columns=[col], errors='ignore')

    print(f"Military county filter:")
    print(f"  Excluded: {len(excluded):,} tracts")
    print(f"  Remaining: {len(filtered):,} tracts")

    if len(excluded) > 0:
        # Show which bases
        excluded['_tract_str'] = excluded[tract_column].astype(str).str.zfill(11)
        excluded['_state_fips'] = excluded['_tract_str'].str[:2]
        excluded['_county_fips'] = excluded['_tract_str'].str[2:5]
        bases_found = set()
        for _, row in excluded.iterrows():
            key = (row['_state_fips'], row['_county_fips'])
            if key in MILITARY_COUNTIES:
                bases_found.add(MILITARY_COUNTIES[key])
        print(f"  Bases excluded: {', '.join(sorted(bases_found))}")

    return filtered, excluded


def filter_student_signature(
    df: pd.DataFrame,
    median_age_col: str = None,
    poverty_rate_col: str = 'PovertyRate',
    age_threshold: float = 25.0,
    poverty_threshold: float = 40.0
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Filter tracts with student housing demographic signature.

    Student housing signature: young median age + high poverty rate
    (Students are counted as impoverished due to low/no income)

    Args:
        df: DataFrame with tract data
        median_age_col: Column with median age (if available)
        poverty_rate_col: Column with poverty rate
        age_threshold: Maximum median age for student signature
        poverty_threshold: Minimum poverty rate for student signature

    Returns:
        (filtered_df, excluded_df)
    """
    # If we don't have median age, we can't apply this filter
    if median_age_col is None or median_age_col not in df.columns:
        print("Student signature filter: skipped (no median age data)")
        return df, pd.DataFrame()

    if poverty_rate_col not in df.columns:
        print("Student signature filter: skipped (no poverty rate data)")
        return df, pd.DataFrame()

    df = df.copy()
    df[median_age_col] = pd.to_numeric(df[median_age_col], errors='coerce')
    df[poverty_rate_col] = pd.to_numeric(df[poverty_rate_col], errors='coerce')

    # Student signature: young + high poverty
    is_student = (df[median_age_col] < age_threshold) & (df[poverty_rate_col] > poverty_threshold)

    excluded = df[is_student].copy()
    filtered = df[~is_student].copy()

    print(f"Student signature filter (age < {age_threshold} AND poverty > {poverty_threshold}%):")
    print(f"  Excluded: {len(excluded):,} tracts")
    print(f"  Remaining: {len(filtered):,} tracts")

    return filtered, excluded


def filter_high_renter_mobility(
    df: pd.DataFrame,
    renter_threshold: float = 95.0,
    exclude_high_renter: bool = True
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Filter tracts with extremely high renter rates.

    >95% renter occupancy often indicates:
    - Military housing
    - Student apartments
    - Transitional housing

    Args:
        df: DataFrame with tract data
        renter_threshold: Percentage threshold for renter occupancy
        exclude_high_renter: Whether to exclude high-renter tracts

    Returns:
        (filtered_df, excluded_df)
    """
    # This would require additional Census data we may not have
    # Placeholder for future implementation
    print("High renter filter: skipped (data not available in FARA)")
    return df, pd.DataFrame()


def apply_all_enhanced_filters(
    df: pd.DataFrame,
    min_population: int = 500,
    filter_military: bool = True,
    tract_column: str = 'CensusTract'
) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Apply all enhanced filters to the dataset.

    Args:
        df: DataFrame with tract data
        min_population: Minimum population threshold
        filter_military: Whether to filter military counties
        tract_column: Name of tract ID column

    Returns:
        (filtered_df, dict of excluded DataFrames by reason)
    """
    print("=" * 60)
    print("APPLYING ENHANCED INSTITUTIONAL FILTERS")
    print("=" * 60)

    excluded = {}
    current_df = df.copy()

    # 1. Population filter
    current_df, exc = filter_low_population(current_df, min_population)
    if len(exc) > 0:
        excluded['low_population'] = exc

    # 2. Military county filter
    if filter_military:
        current_df, exc = filter_military_counties(current_df, tract_column)
        if len(exc) > 0:
            excluded['military_county'] = exc

    # Summary
    total_excluded = sum(len(e) for e in excluded.values())
    print(f"\n--- Enhanced Filter Summary ---")
    print(f"Original tracts: {len(df):,}")
    print(f"Total excluded: {total_excluded:,}")
    print(f"Remaining: {len(current_df):,}")

    return current_df, excluded


if __name__ == "__main__":
    # Test with sample data
    print("Enhanced filters module loaded successfully")
    print(f"Known military counties: {len(MILITARY_COUNTIES)}")
    print(f"Known university counties: {len(UNIVERSITY_COUNTIES)}")
