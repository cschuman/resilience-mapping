#!/usr/bin/env python3
"""
Fetch ACS 5-Year Demographic Data for Paper 4: Health Equity Analysis

This script fetches tract-level demographic data from the Census API:
- Racial composition
- Hispanic/Latino origin
- Median household income
- Poverty rate
- Employment/unemployment
- Housing tenure (rent vs own)
- Educational attainment

Output: data/external/acs_demographics_2022.csv
"""

import requests
import pandas as pd
from pathlib import Path
import time
import sys

# Census API base URL
BASE_URL = "https://api.census.gov/data/2022/acs/acs5"

# Variables to fetch (ACS 5-Year 2022)
# See: https://api.census.gov/data/2022/acs/acs5/variables.html
VARIABLES = {
    # Total population
    "B01003_001E": "total_population",

    # Race (B02001)
    "B02001_001E": "race_total",
    "B02001_002E": "race_white_alone",
    "B02001_003E": "race_black_alone",
    "B02001_004E": "race_aian_alone",  # American Indian/Alaska Native
    "B02001_005E": "race_asian_alone",
    "B02001_006E": "race_nhpi_alone",  # Native Hawaiian/Pacific Islander
    "B02001_007E": "race_other_alone",
    "B02001_008E": "race_two_or_more",

    # Hispanic/Latino (B03003)
    "B03003_001E": "hispanic_total",
    "B03003_003E": "hispanic_yes",

    # Median household income (B19013)
    "B19013_001E": "median_hh_income",

    # Poverty status (B17001)
    "B17001_001E": "poverty_total",
    "B17001_002E": "poverty_below",

    # Employment status (B23025) - Population 16+
    "B23025_001E": "employ_total",
    "B23025_002E": "employ_in_labor_force",
    "B23025_005E": "employ_unemployed",

    # Housing tenure (B25003)
    "B25003_001E": "tenure_total",
    "B25003_002E": "tenure_owner",
    "B25003_003E": "tenure_renter",

    # Educational attainment 25+ (B15003)
    "B15003_001E": "edu_total",
    "B15003_017E": "edu_hs_diploma",
    "B15003_018E": "edu_ged",
    "B15003_021E": "edu_associates",
    "B15003_022E": "edu_bachelors",
    "B15003_023E": "edu_masters",
    "B15003_024E": "edu_professional",
    "B15003_025E": "edu_doctorate",
}

# All US states and DC FIPS codes
STATE_FIPS = [
    "01", "02", "04", "05", "06", "08", "09", "10", "11", "12",
    "13", "15", "16", "17", "18", "19", "20", "21", "22", "23",
    "24", "25", "26", "27", "28", "29", "30", "31", "32", "33",
    "34", "35", "36", "37", "38", "39", "40", "41", "42", "44",
    "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"
]


def fetch_state_data(state_fips: str, variables: dict) -> pd.DataFrame:
    """Fetch ACS data for all tracts in a state."""

    var_list = ",".join(variables.keys())

    params = {
        "get": f"NAME,{var_list}",
        "for": "tract:*",
        "in": f"state:{state_fips}",
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        print(f"  Error fetching state {state_fips}: {response.status_code}")
        return pd.DataFrame()

    data = response.json()

    if len(data) < 2:
        print(f"  No data for state {state_fips}")
        return pd.DataFrame()

    # First row is headers
    headers = data[0]
    rows = data[1:]

    df = pd.DataFrame(rows, columns=headers)

    # Create GEOID (state + county + tract)
    df["GEOID"] = df["state"] + df["county"] + df["tract"]

    return df


def compute_derived_variables(df: pd.DataFrame, variables: dict) -> pd.DataFrame:
    """Compute percentage and derived variables."""

    # Rename columns
    rename_map = {k: v for k, v in variables.items() if k in df.columns}
    df = df.rename(columns=rename_map)

    # Convert to numeric
    numeric_cols = list(variables.values())
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Compute percentages

    # Race percentages
    if "race_total" in df.columns and df["race_total"].notna().any():
        df["pct_white"] = (df["race_white_alone"] / df["race_total"] * 100).round(2)
        df["pct_black"] = (df["race_black_alone"] / df["race_total"] * 100).round(2)
        df["pct_asian"] = (df["race_asian_alone"] / df["race_total"] * 100).round(2)
        df["pct_aian"] = (df["race_aian_alone"] / df["race_total"] * 100).round(2)
        df["pct_nhpi"] = (df["race_nhpi_alone"] / df["race_total"] * 100).round(2)
        df["pct_other_race"] = (df["race_other_alone"] / df["race_total"] * 100).round(2)
        df["pct_two_or_more_races"] = (df["race_two_or_more"] / df["race_total"] * 100).round(2)

    # Hispanic percentage
    if "hispanic_total" in df.columns and df["hispanic_total"].notna().any():
        df["pct_hispanic"] = (df["hispanic_yes"] / df["hispanic_total"] * 100).round(2)

    # Poverty rate
    if "poverty_total" in df.columns and df["poverty_total"].notna().any():
        df["poverty_rate"] = (df["poverty_below"] / df["poverty_total"] * 100).round(2)

    # Unemployment rate
    if "employ_in_labor_force" in df.columns and df["employ_in_labor_force"].notna().any():
        df["unemployment_rate"] = (df["employ_unemployed"] / df["employ_in_labor_force"] * 100).round(2)

    # Renter percentage
    if "tenure_total" in df.columns and df["tenure_total"].notna().any():
        df["pct_renter"] = (df["tenure_renter"] / df["tenure_total"] * 100).round(2)

    # Educational attainment (% with bachelor's or higher)
    if "edu_total" in df.columns and df["edu_total"].notna().any():
        bachelors_plus = (
            df["edu_bachelors"].fillna(0) +
            df["edu_masters"].fillna(0) +
            df["edu_professional"].fillna(0) +
            df["edu_doctorate"].fillna(0)
        )
        df["pct_bachelors_plus"] = (bachelors_plus / df["edu_total"] * 100).round(2)

        hs_plus = (
            df["edu_hs_diploma"].fillna(0) +
            df["edu_ged"].fillna(0) +
            df["edu_associates"].fillna(0) +
            bachelors_plus
        )
        df["pct_hs_plus"] = (hs_plus / df["edu_total"] * 100).round(2)

    return df


def main():
    """Fetch ACS data for all states and save to CSV."""

    output_dir = Path("data/external")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "acs_demographics_2022.csv"

    print("Fetching ACS 5-Year 2022 Demographic Data")
    print("=" * 50)

    all_data = []

    for i, state in enumerate(STATE_FIPS):
        print(f"Fetching state {state} ({i+1}/{len(STATE_FIPS)})...", end=" ")

        df = fetch_state_data(state, VARIABLES)

        if not df.empty:
            print(f"{len(df)} tracts")
            all_data.append(df)
        else:
            print("skipped")

        # Rate limiting
        time.sleep(0.1)

    print("\nCombining data...")
    combined = pd.concat(all_data, ignore_index=True)

    print("Computing derived variables...")
    combined = compute_derived_variables(combined, VARIABLES)

    # Select final columns
    final_cols = [
        "GEOID", "NAME",
        "total_population",
        "pct_white", "pct_black", "pct_asian", "pct_aian", "pct_nhpi",
        "pct_other_race", "pct_two_or_more_races", "pct_hispanic",
        "median_hh_income",
        "poverty_rate",
        "unemployment_rate",
        "pct_renter",
        "pct_bachelors_plus", "pct_hs_plus",
    ]

    # Only keep columns that exist
    final_cols = [c for c in final_cols if c in combined.columns]
    combined = combined[final_cols]

    print(f"Saving {len(combined)} tracts to {output_file}...")
    combined.to_csv(output_file, index=False)

    print("\nSummary:")
    print(f"  Total tracts: {len(combined):,}")
    print(f"  Columns: {', '.join(final_cols)}")
    print("\nSample:")
    print(combined.head(10).to_string())

    print(f"\nDone! Output saved to {output_file}")


if __name__ == "__main__":
    main()
