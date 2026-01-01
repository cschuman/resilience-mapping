#!/usr/bin/env python3
"""
Download ACS data for Black immigrant analysis and occupation data.

Tables:
1. B05003 - Sex by Age by Nativity by Citizenship (with race iterations)
   - B05003B: Black alone (foreign-born vs native-born)
   - B05003I: Hispanic (for comparison)
2. C24010 - Occupation by Sex (for union density proxy)

Uses Census API to get tract-level data.
"""

import requests
import pandas as pd
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "external"

STATE_FIPS = [
    '01', '02', '04', '05', '06', '08', '09', '10', '11', '12',
    '13', '15', '16', '17', '18', '19', '20', '21', '22', '23',
    '24', '25', '26', '27', '28', '29', '30', '31', '32', '33',
    '34', '35', '36', '37', '38', '39', '40', '41', '42', '44',
    '45', '46', '47', '48', '49', '50', '51', '53', '54', '55', '56'
]

BASE_URL = "https://api.census.gov/data/2022/acs/acs5"


def download_black_nativity():
    """
    Download B05003B: Black alone - Nativity by Citizenship

    Key variables:
    - B05003B_001E: Total Black population
    - B05003B_003E: Native-born Black (male)
    - B05003B_014E: Native-born Black (female)
    - B05003B_006E: Foreign-born Black (male, naturalized)
    - B05003B_009E: Foreign-born Black (male, not citizen)
    - B05003B_017E: Foreign-born Black (female, naturalized)
    - B05003B_020E: Foreign-born Black (female, not citizen)
    """
    print("=" * 60)
    print("Downloading B05003B: Black Nativity Data")
    print("=" * 60)

    # Simplified approach: get total and foreign-born totals
    # B05003B_001E = Total
    # B05003B_004E = Male native-born
    # B05003B_015E = Female native-born
    # (Total - native-born = foreign-born)

    variables = [
        "NAME",
        "B05003B_001E",  # Total Black population
        "B05003B_004E",  # Male: Native born
        "B05003B_015E",  # Female: Native born
    ]

    all_data = []

    for state in STATE_FIPS:
        url = f"{BASE_URL}?get={','.join(variables)}&for=tract:*&in=state:{state}"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            header = data[0]
            rows = data[1:]

            for row in rows:
                all_data.append(dict(zip(header, row)))

            print(f"  State {state}: {len(rows):,} tracts")

        except Exception as e:
            print(f"  State {state}: ERROR - {e}")

        time.sleep(0.1)

    df = pd.DataFrame(all_data)
    df['GEOID'] = df['state'] + df['county'] + df['tract']

    # Convert to numeric
    for col in ['B05003B_001E', 'B05003B_004E', 'B05003B_015E']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Calculate foreign-born
    df['black_total'] = df['B05003B_001E']
    df['black_native_born'] = df['B05003B_004E'] + df['B05003B_015E']
    df['black_foreign_born'] = df['black_total'] - df['black_native_born']
    df['pct_black_foreign_born'] = (df['black_foreign_born'] / df['black_total'] * 100).round(2)

    result = df[['GEOID', 'NAME', 'black_total', 'black_native_born', 'black_foreign_born', 'pct_black_foreign_born']]

    output_path = DATA_DIR / "acs_black_nativity_2022.csv"
    result.to_csv(output_path, index=False)
    print(f"\nSaved {len(result):,} tracts to {output_path}")

    # Summary
    valid = result[result['black_total'] > 100]  # Tracts with meaningful Black population
    print(f"\nSummary (tracts with Black pop > 100):")
    print(f"  N tracts: {len(valid):,}")
    print(f"  Mean % Black foreign-born: {valid['pct_black_foreign_born'].mean():.1f}%")
    print(f"  Median % Black foreign-born: {valid['pct_black_foreign_born'].median():.1f}%")
    print(f"  Max % Black foreign-born: {valid['pct_black_foreign_born'].max():.1f}%")

    return result


def download_occupation_data():
    """
    Download occupation data for union density proxy.

    Key categories (proxy for union jobs):
    - Production, transportation, material moving
    - Government/public administration

    Using C24010: Sex by Occupation for the Civilian Employed Population 16+
    """
    print("\n" + "=" * 60)
    print("Downloading C24010: Occupation Data")
    print("=" * 60)

    # Key occupation variables
    # C24010_001E: Total civilian employed 16+
    # C24010_006E: Management, business, science, arts (male)
    # C24010_042E: Management, business, science, arts (female)
    # C24010_030E: Production, transportation, material moving (male)
    # C24010_066E: Production, transportation, material moving (female)
    # C24010_027E: Service occupations (male)
    # C24010_063E: Service occupations (female)

    variables = [
        "NAME",
        "C24010_001E",  # Total employed
        "C24010_006E",  # Male: Management, business, science, arts
        "C24010_042E",  # Female: Management, business, science, arts
        "C24010_030E",  # Male: Production, transportation, material moving
        "C24010_066E",  # Female: Production, transportation, material moving
        "C24010_027E",  # Male: Natural resources, construction, maintenance
        "C24010_063E",  # Female: Natural resources, construction, maintenance
    ]

    all_data = []

    for state in STATE_FIPS:
        url = f"{BASE_URL}?get={','.join(variables)}&for=tract:*&in=state:{state}"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            header = data[0]
            rows = data[1:]

            for row in rows:
                all_data.append(dict(zip(header, row)))

            print(f"  State {state}: {len(rows):,} tracts")

        except Exception as e:
            print(f"  State {state}: ERROR - {e}")

        time.sleep(0.1)

    df = pd.DataFrame(all_data)
    df['GEOID'] = df['state'] + df['county'] + df['tract']

    # Convert to numeric
    for col in df.columns:
        if col.startswith('C24010'):
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Calculate occupation percentages
    df['total_employed'] = df['C24010_001E']
    df['professional_mgmt'] = df['C24010_006E'] + df['C24010_042E']
    df['production_transport'] = df['C24010_030E'] + df['C24010_066E']
    df['construction_maintenance'] = df['C24010_027E'] + df['C24010_063E']

    # Blue collar (production + construction) - proxy for union jobs
    df['blue_collar'] = df['production_transport'] + df['construction_maintenance']

    df['pct_professional'] = (df['professional_mgmt'] / df['total_employed'] * 100).round(2)
    df['pct_blue_collar'] = (df['blue_collar'] / df['total_employed'] * 100).round(2)
    df['pct_production'] = (df['production_transport'] / df['total_employed'] * 100).round(2)

    result = df[['GEOID', 'NAME', 'total_employed', 'professional_mgmt', 'blue_collar',
                 'production_transport', 'pct_professional', 'pct_blue_collar', 'pct_production']]

    output_path = DATA_DIR / "acs_occupation_2022.csv"
    result.to_csv(output_path, index=False)
    print(f"\nSaved {len(result):,} tracts to {output_path}")

    # Summary
    print(f"\nSummary:")
    print(f"  Mean % professional/management: {result['pct_professional'].mean():.1f}%")
    print(f"  Mean % blue collar: {result['pct_blue_collar'].mean():.1f}%")
    print(f"  Mean % production/transport: {result['pct_production'].mean():.1f}%")

    return result


def main():
    print("=" * 60)
    print("DOWNLOADING ADDITIONAL ACS DATA FOR PAPER 4B")
    print("=" * 60)
    print()

    black_nativity = download_black_nativity()
    occupation = download_occupation_data()

    print("\n" + "=" * 60)
    print("DOWNLOAD COMPLETE")
    print("=" * 60)
    print(f"\nFiles saved to: {DATA_DIR}")
    print("  - acs_black_nativity_2022.csv")
    print("  - acs_occupation_2022.csv")

    return black_nativity, occupation


if __name__ == "__main__":
    black_nativity, occupation = main()
