#!/usr/bin/env python3
"""
Download Census Group Quarters Data by Type

Downloads tract-level group quarters population by type from the
2020 Census PL 94-171 Redistricting Data.

Variables (from P5 table - GROUP QUARTERS POPULATION BY MAJOR GROUP QUARTERS TYPE):
- P1_001N: Total population
- P5_001N: Total group quarters population
- P5_002N: Institutionalized population
- P5_003N: Correctional facilities for adults
- P5_004N: Juvenile facilities
- P5_005N: Nursing facilities
- P5_006N: Other institutional facilities
- P5_007N: Noninstitutionalized population
- P5_008N: College/university student housing
- P5_009N: Military quarters
- P5_010N: Other noninstitutional facilities

Source: https://api.census.gov/data/2020/dec/pl
"""

import requests
import pandas as pd
import os
import time

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_INPUT = os.path.join(PROJECT_ROOT, 'data', 'input')

# Census API base URL for 2020 PL 94-171 Redistricting Data
BASE_URL = "https://api.census.gov/data/2020/dec/pl"

# Variables to fetch
VARIABLES = [
    "P1_001N",      # Total population
    "P5_001N",      # Total group quarters population
    "P5_002N",      # Institutionalized population
    "P5_003N",      # Correctional facilities for adults
    "P5_004N",      # Juvenile facilities
    "P5_005N",      # Nursing facilities
    "P5_006N",      # Other institutional facilities
    "P5_007N",      # Noninstitutionalized population
    "P5_008N",      # College/university student housing
    "P5_009N",      # Military quarters
    "P5_010N",      # Other noninstitutional facilities
]

# All US states and territories FIPS codes
STATE_FIPS = [
    "01", "02", "04", "05", "06", "08", "09", "10", "11", "12",
    "13", "15", "16", "17", "18", "19", "20", "21", "22", "23",
    "24", "25", "26", "27", "28", "29", "30", "31", "32", "33",
    "34", "35", "36", "37", "38", "39", "40", "41", "42", "44",
    "45", "46", "47", "48", "49", "50", "51", "53", "54", "55",
    "56", "72"  # 50 states + DC + PR
]


def fetch_state_tracts(state_fips: str, variables: list) -> pd.DataFrame:
    """Fetch tract-level data for a single state."""
    var_string = ",".join(variables)

    url = f"{BASE_URL}?get={var_string}&for=tract:*&in=state:{state_fips}"

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        data = response.json()

        # First row is header
        header = data[0]
        rows = data[1:]

        df = pd.DataFrame(rows, columns=header)
        return df

    except requests.exceptions.RequestException as e:
        print(f"  Error fetching state {state_fips}: {e}")
        return pd.DataFrame()


def download_all_states():
    """Download group quarters data for all states."""
    print("=" * 60)
    print("DOWNLOADING CENSUS GROUP QUARTERS DATA")
    print("2020 Census PL 94-171 Redistricting Data")
    print("=" * 60)
    print(f"\nVariables: {len(VARIABLES)}")
    print(f"States to fetch: {len(STATE_FIPS)}")

    all_data = []

    for i, state in enumerate(STATE_FIPS, 1):
        print(f"\rFetching state {state} ({i}/{len(STATE_FIPS)})...", end="", flush=True)

        df = fetch_state_tracts(state, VARIABLES)
        if not df.empty:
            all_data.append(df)

        # Be nice to the API
        time.sleep(0.2)

    print("\n")

    if not all_data:
        print("ERROR: No data retrieved!")
        return None

    # Combine all states
    combined = pd.concat(all_data, ignore_index=True)

    # Create tract FIPS (11 digits: state + county + tract)
    combined['TractFIPS'] = (
        combined['state'].str.zfill(2) +
        combined['county'].str.zfill(3) +
        combined['tract'].str.zfill(6)
    )

    # Convert numeric columns
    for var in VARIABLES:
        combined[var] = pd.to_numeric(combined[var], errors='coerce').fillna(0).astype(int)

    # Rename columns for clarity
    combined = combined.rename(columns={
        'P1_001N': 'total_pop',
        'P5_001N': 'gq_total',
        'P5_002N': 'gq_institutional',
        'P5_003N': 'gq_correctional',
        'P5_004N': 'gq_juvenile',
        'P5_005N': 'gq_nursing',
        'P5_006N': 'gq_other_inst',
        'P5_007N': 'gq_noninstitutional',
        'P5_008N': 'gq_college',
        'P5_009N': 'gq_military',
        'P5_010N': 'gq_other_noninst',
    })

    # Calculate percentages (handle division by zero)
    for col in ['gq_total', 'gq_college', 'gq_military', 'gq_correctional', 'gq_nursing']:
        pct_col = f'pct_{col}'
        combined[pct_col] = combined.apply(
            lambda row: round(row[col] / row['total_pop'] * 100, 2) if row['total_pop'] > 0 else 0,
            axis=1
        )

    # Select and order columns
    output_cols = [
        'TractFIPS', 'state', 'county', 'tract',
        'total_pop', 'gq_total', 'gq_institutional', 'gq_noninstitutional',
        'gq_college', 'gq_military', 'gq_correctional', 'gq_nursing',
        'gq_juvenile', 'gq_other_inst', 'gq_other_noninst',
        'pct_gq_total', 'pct_gq_college', 'pct_gq_military',
        'pct_gq_correctional', 'pct_gq_nursing'
    ]
    combined = combined[output_cols]

    print(f"Total tracts retrieved: {len(combined):,}")

    # Summary stats
    print("\n--- Group Quarters Summary ---")
    print(f"Tracts with college housing: {(combined['gq_college'] > 0).sum():,}")
    print(f"Tracts with military quarters: {(combined['gq_military'] > 0).sum():,}")
    print(f"Tracts with correctional: {(combined['gq_correctional'] > 0).sum():,}")
    print(f"Tracts with nursing: {(combined['gq_nursing'] > 0).sum():,}")

    # High concentration tracts
    print("\n--- High Concentration Tracts ---")
    print(f"College housing >25%: {(combined['pct_gq_college'] > 25).sum():,}")
    print(f"Military >25%: {(combined['pct_gq_military'] > 25).sum():,}")
    print(f"Correctional >25%: {(combined['pct_gq_correctional'] > 25).sum():,}")
    print(f"Nursing >25%: {(combined['pct_gq_nursing'] > 25).sum():,}")

    # Tracts that would be filtered at various thresholds
    print("\n--- Filter Impact at Various Thresholds ---")
    for threshold in [10, 15, 20, 25]:
        college_filter = (combined['pct_gq_college'] > threshold).sum()
        military_filter = (combined['pct_gq_military'] > threshold).sum()
        correctional_filter = (combined['pct_gq_correctional'] > threshold).sum()
        any_filter = (
            (combined['pct_gq_college'] > threshold) |
            (combined['pct_gq_military'] > threshold) |
            (combined['pct_gq_correctional'] > threshold)
        ).sum()
        print(f"  >{threshold}%: College={college_filter:,}, Military={military_filter:,}, Correctional={correctional_filter:,}, Any={any_filter:,}")

    # Save
    output_path = os.path.join(DATA_INPUT, 'census_gq_by_type_2020.csv')
    combined.to_csv(output_path, index=False)
    print(f"\nSaved: {output_path}")

    return combined


if __name__ == "__main__":
    df = download_all_states()

    if df is not None:
        # Show sample of high-college tracts
        print("\n--- Sample: Highest College Housing % ---")
        top_college = df.nlargest(10, 'pct_gq_college')[
            ['TractFIPS', 'total_pop', 'gq_college', 'pct_gq_college']
        ]
        print(top_college.to_string(index=False))

        print("\n--- Sample: Highest Military % ---")
        top_military = df.nlargest(10, 'pct_gq_military')[
            ['TractFIPS', 'total_pop', 'gq_military', 'pct_gq_military']
        ]
        print(top_military.to_string(index=False))
