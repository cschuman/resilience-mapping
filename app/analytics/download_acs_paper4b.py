#!/usr/bin/env python3
"""
Download ACS data for Paper 4B: Hispanic Paradox Investigation

Tables needed:
1. B05002 - Place of Birth by Nativity and Citizenship Status (foreign-born %)
2. B03001 - Hispanic or Latino Origin by Specific Origin (Mexican, Puerto Rican, Cuban, etc.)

Uses Census API to get tract-level data for all states.
"""

import requests
import pandas as pd
import time
from pathlib import Path

# Output directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "external"

# State FIPS codes (all 50 states + DC)
STATE_FIPS = [
    '01', '02', '04', '05', '06', '08', '09', '10', '11', '12',
    '13', '15', '16', '17', '18', '19', '20', '21', '22', '23',
    '24', '25', '26', '27', '28', '29', '30', '31', '32', '33',
    '34', '35', '36', '37', '38', '39', '40', '41', '42', '44',
    '45', '46', '47', '48', '49', '50', '51', '53', '54', '55', '56'
]

# Census API base URL
BASE_URL = "https://api.census.gov/data/2022/acs/acs5"


def download_nativity_data():
    """
    Download B05002: Place of Birth by Nativity and Citizenship Status

    Key variables:
    - B05002_001E: Total population
    - B05002_013E: Foreign born
    """
    print("=" * 60)
    print("Downloading B05002: Nativity Data")
    print("=" * 60)

    variables = [
        "NAME",
        "B05002_001E",  # Total
        "B05002_013E",  # Foreign born
    ]

    all_data = []

    for state in STATE_FIPS:
        url = f"{BASE_URL}?get={','.join(variables)}&for=tract:*&in=state:{state}"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            # First row is header
            header = data[0]
            rows = data[1:]

            for row in rows:
                all_data.append(dict(zip(header, row)))

            print(f"  State {state}: {len(rows):,} tracts")

        except Exception as e:
            print(f"  State {state}: ERROR - {e}")

        time.sleep(0.1)  # Rate limiting

    # Convert to DataFrame
    df = pd.DataFrame(all_data)

    # Create GEOID
    df['GEOID'] = df['state'] + df['county'] + df['tract']

    # Convert to numeric
    df['total_pop'] = pd.to_numeric(df['B05002_001E'], errors='coerce')
    df['foreign_born'] = pd.to_numeric(df['B05002_013E'], errors='coerce')

    # Calculate percentage
    df['pct_foreign_born'] = (df['foreign_born'] / df['total_pop'] * 100).round(2)

    # Select final columns
    result = df[['GEOID', 'NAME', 'total_pop', 'foreign_born', 'pct_foreign_born']]

    # Save
    output_path = DATA_DIR / "acs_nativity_2022.csv"
    result.to_csv(output_path, index=False)
    print(f"\nSaved {len(result):,} tracts to {output_path}")

    # Summary stats
    print(f"\nSummary:")
    print(f"  Mean % foreign-born: {result['pct_foreign_born'].mean():.1f}%")
    print(f"  Median % foreign-born: {result['pct_foreign_born'].median():.1f}%")
    print(f"  Max % foreign-born: {result['pct_foreign_born'].max():.1f}%")

    return result


def download_hispanic_origin_data():
    """
    Download B03001: Hispanic or Latino Origin by Specific Origin

    Key variables:
    - B03001_001E: Total population
    - B03001_002E: Not Hispanic or Latino
    - B03001_003E: Hispanic or Latino (total)
    - B03001_004E: Mexican
    - B03001_005E: Puerto Rican
    - B03001_006E: Cuban
    - B03001_007E: Dominican
    - B03001_008E: Central American (total)
    - B03001_016E: South American (total)
    """
    print("\n" + "=" * 60)
    print("Downloading B03001: Hispanic Origin Data")
    print("=" * 60)

    variables = [
        "NAME",
        "B03001_001E",  # Total population
        "B03001_002E",  # Not Hispanic
        "B03001_003E",  # Hispanic or Latino (total)
        "B03001_004E",  # Mexican
        "B03001_005E",  # Puerto Rican
        "B03001_006E",  # Cuban
        "B03001_007E",  # Dominican
        "B03001_008E",  # Central American (total)
        "B03001_016E",  # South American (total)
    ]

    all_data = []

    for state in STATE_FIPS:
        url = f"{BASE_URL}?get={','.join(variables)}&for=tract:*&in=state:{state}"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            # First row is header
            header = data[0]
            rows = data[1:]

            for row in rows:
                all_data.append(dict(zip(header, row)))

            print(f"  State {state}: {len(rows):,} tracts")

        except Exception as e:
            print(f"  State {state}: ERROR - {e}")

        time.sleep(0.1)  # Rate limiting

    # Convert to DataFrame
    df = pd.DataFrame(all_data)

    # Create GEOID
    df['GEOID'] = df['state'] + df['county'] + df['tract']

    # Convert to numeric
    numeric_cols = ['B03001_001E', 'B03001_002E', 'B03001_003E', 'B03001_004E',
                    'B03001_005E', 'B03001_006E', 'B03001_007E', 'B03001_008E', 'B03001_016E']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Rename and calculate - CORRECTED variable mapping
    df['total_pop'] = df['B03001_001E']
    df['not_hispanic'] = df['B03001_002E']
    df['hispanic_total_direct'] = df['B03001_003E']  # Total Hispanic (direct from Census)
    df['hispanic_mexican'] = df['B03001_004E']
    df['hispanic_puerto_rican'] = df['B03001_005E']
    df['hispanic_cuban'] = df['B03001_006E']
    df['hispanic_dominican'] = df['B03001_007E']
    df['hispanic_central_american'] = df['B03001_008E']
    df['hispanic_south_american'] = df['B03001_016E']

    # Total Hispanic
    df['hispanic_total'] = df['total_pop'] - df['not_hispanic']

    # Percentages of total population
    df['pct_hispanic'] = (df['hispanic_total'] / df['total_pop'] * 100).round(2)
    df['pct_mexican'] = (df['hispanic_mexican'] / df['total_pop'] * 100).round(2)
    df['pct_puerto_rican'] = (df['hispanic_puerto_rican'] / df['total_pop'] * 100).round(2)
    df['pct_cuban'] = (df['hispanic_cuban'] / df['total_pop'] * 100).round(2)
    df['pct_dominican'] = (df['hispanic_dominican'] / df['total_pop'] * 100).round(2)
    df['pct_central_american'] = (df['hispanic_central_american'] / df['total_pop'] * 100).round(2)
    df['pct_south_american'] = (df['hispanic_south_american'] / df['total_pop'] * 100).round(2)

    # Percentages of Hispanic population (among Hispanics)
    df['pct_mexican_of_hispanic'] = (df['hispanic_mexican'] / df['hispanic_total'] * 100).round(2)
    df['pct_puerto_rican_of_hispanic'] = (df['hispanic_puerto_rican'] / df['hispanic_total'] * 100).round(2)
    df['pct_cuban_of_hispanic'] = (df['hispanic_cuban'] / df['hispanic_total'] * 100).round(2)

    # Dominant Hispanic origin
    origin_cols = ['hispanic_mexican', 'hispanic_puerto_rican', 'hispanic_cuban',
                   'hispanic_dominican', 'hispanic_central_american', 'hispanic_south_american']
    df['dominant_hispanic_origin'] = df[origin_cols].idxmax(axis=1)
    df['dominant_hispanic_origin'] = df['dominant_hispanic_origin'].str.replace('hispanic_', '')

    # Select final columns
    result = df[[
        'GEOID', 'NAME', 'total_pop', 'hispanic_total',
        'hispanic_mexican', 'hispanic_puerto_rican', 'hispanic_cuban',
        'hispanic_dominican', 'hispanic_central_american', 'hispanic_south_american',
        'pct_hispanic', 'pct_mexican', 'pct_puerto_rican', 'pct_cuban',
        'pct_dominican', 'pct_central_american', 'pct_south_american',
        'pct_mexican_of_hispanic', 'pct_puerto_rican_of_hispanic', 'pct_cuban_of_hispanic',
        'dominant_hispanic_origin'
    ]]

    # Save
    output_path = DATA_DIR / "acs_hispanic_origin_2022.csv"
    result.to_csv(output_path, index=False)
    print(f"\nSaved {len(result):,} tracts to {output_path}")

    # Summary stats
    print(f"\nHispanic Origin Distribution (among all tracts):")
    print(f"  Mean % Mexican: {result['pct_mexican'].mean():.1f}%")
    print(f"  Mean % Puerto Rican: {result['pct_puerto_rican'].mean():.1f}%")
    print(f"  Mean % Cuban: {result['pct_cuban'].mean():.1f}%")
    print(f"  Mean % Central American: {result['pct_central_american'].mean():.1f}%")
    print(f"  Mean % South American: {result['pct_south_american'].mean():.1f}%")

    # Dominant origin distribution
    print(f"\nDominant Hispanic Origin (tract counts):")
    print(result['dominant_hispanic_origin'].value_counts().to_string())

    return result


def main():
    print("=" * 60)
    print("DOWNLOADING ACS DATA FOR PAPER 4B")
    print("=" * 60)
    print()

    # Download nativity data
    nativity = download_nativity_data()

    # Download Hispanic origin data
    hispanic = download_hispanic_origin_data()

    # Summary
    print("\n" + "=" * 60)
    print("DOWNLOAD COMPLETE")
    print("=" * 60)
    print(f"\nFiles saved to: {DATA_DIR}")
    print("  - acs_nativity_2022.csv")
    print("  - acs_hispanic_origin_2022.csv")

    # Quick merge check
    merged = nativity.merge(hispanic[['GEOID', 'pct_mexican', 'pct_puerto_rican']], on='GEOID', how='inner')
    print(f"\nMerge check: {len(merged):,} tracts with both datasets")

    return nativity, hispanic


if __name__ == "__main__":
    nativity, hispanic = main()
