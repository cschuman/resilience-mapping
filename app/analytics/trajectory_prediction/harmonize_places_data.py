"""
Harmonize CDC PLACES data across years for trajectory prediction

Two formats exist:
1. Long format (2020, 2021, 2023, 2025): One row per tract-measure combination
2. Wide/GIS format (2022, 2024): One row per tract, measures as columns

This script converts all years to a consistent wide format.
"""

import os
import csv
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
INTERIM_DATA_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Key health measures for trajectory prediction (CHBI components)
CHBI_MEASURES = {
    'OBESITY': 'Obesity among adults',
    'DIABETES': 'Diagnosed diabetes among adults',
    'CHD': 'Coronary heart disease among adults',
    'BPHIGH': 'High blood pressure among adults',
    'LPA': 'Physical inactivity among adults',
    'MHLTH': 'Mental health not good for >=14 days',
    'PHLTH': 'Physical health not good for >=14 days',
}

# Additional useful measures
ADDITIONAL_MEASURES = {
    'CASTHMA': 'Current asthma among adults',
    'COPD': 'COPD among adults',
    'CANCER': 'Cancer (non-skin) among adults',
    'STROKE': 'Stroke among adults',
    'KIDNEY': 'Chronic kidney disease among adults',
    'CSMOKING': 'Current smoking among adults',
    'BINGE': 'Binge drinking among adults',
    'SLEEP': 'Sleeping less than 7 hours',
    'CHECKUP': 'Annual checkup among adults',
    'DENTAL': 'Dental visit among adults',
    'DEPRESSION': 'Depression among adults',
}

ALL_MEASURES = {**CHBI_MEASURES, **ADDITIONAL_MEASURES}


def detect_format(file_path: Path) -> str:
    """
    Detect if file is in long or wide format

    Returns 'long' or 'wide'
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)

    # Wide format has measure-specific columns like OBESITY_CrudePrev
    if any('_CrudePrev' in col for col in headers):
        return 'wide'
    # Long format has MeasureId column
    elif 'MeasureId' in headers:
        return 'long'
    else:
        logger.warning(f"Unknown format for {file_path}")
        return 'unknown'


def process_long_format(file_path: Path, year: int) -> Dict[str, Dict[str, float]]:
    """
    Process long format file (one row per tract-measure)

    Returns dict: {tract_fips: {measure: value, ...}}
    """
    logger.info(f"Processing long format: {file_path}")

    tract_data = defaultdict(dict)
    row_count = 0

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            row_count += 1

            # Get tract ID and measure
            tract_id = row.get('LocationID', row.get('TractFIPS', ''))
            measure_id = row.get('MeasureId', '')
            value = row.get('Data_Value', '')

            if not tract_id or not measure_id:
                continue

            # Store tract metadata (first time only)
            if 'StateAbbr' not in tract_data[tract_id]:
                tract_data[tract_id]['StateAbbr'] = row.get('StateAbbr', '')
                tract_data[tract_id]['CountyFIPS'] = row.get('CountyFIPS', '')
                tract_data[tract_id]['TotalPopulation'] = row.get('TotalPopulation', '0')
                tract_data[tract_id]['Year'] = year

            # Store measure value
            try:
                tract_data[tract_id][f'{measure_id}_CrudePrev'] = float(value) if value else None
            except ValueError:
                tract_data[tract_id][f'{measure_id}_CrudePrev'] = None

            # Progress update every 500k rows
            if row_count % 500000 == 0:
                logger.info(f"  Processed {row_count:,} rows, {len(tract_data):,} unique tracts")

    logger.info(f"  Final: {row_count:,} rows -> {len(tract_data):,} tracts")
    return dict(tract_data)


def process_wide_format(file_path: Path, year: int) -> Dict[str, Dict[str, float]]:
    """
    Process wide format file (one row per tract)

    Returns dict: {tract_fips: {measure: value, ...}}
    """
    logger.info(f"Processing wide format: {file_path}")

    tract_data = {}

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            tract_id = row.get('TractFIPS', row.get('LocationID', ''))

            if not tract_id:
                continue

            tract_data[tract_id] = {
                'StateAbbr': row.get('StateAbbr', ''),
                'CountyFIPS': row.get('CountyFIPS', ''),
                'TotalPopulation': row.get('TotalPopulation', '0'),
                'Year': year,
            }

            # Copy all measure columns
            for col, val in row.items():
                if '_CrudePrev' in col or '_Crude95CI' in col:
                    try:
                        tract_data[tract_id][col] = float(val) if val else None
                    except ValueError:
                        tract_data[tract_id][col] = None

    logger.info(f"  Loaded {len(tract_data):,} tracts")
    return tract_data


def harmonize_all_years(years: Optional[List[int]] = None) -> None:
    """
    Process and harmonize all PLACES data files

    Outputs:
    - places_harmonized_YYYY.csv for each year
    - places_longitudinal.csv with all years combined
    """
    if years is None:
        years = [2020, 2021, 2022, 2023, 2024, 2025]

    logger.info("="*60)
    logger.info("PLACES Data Harmonization")
    logger.info("="*60)

    all_years_data = {}
    all_columns = set()

    for year in years:
        file_path = RAW_DATA_DIR / f"places_tract_{year}.csv"

        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            continue

        # Detect and process format
        format_type = detect_format(file_path)
        logger.info(f"[{year}] Format: {format_type}")

        if format_type == 'long':
            tract_data = process_long_format(file_path, year)
        elif format_type == 'wide':
            tract_data = process_wide_format(file_path, year)
        else:
            logger.error(f"Cannot process {file_path}")
            continue

        # Track all columns
        for tract_id, data in tract_data.items():
            all_columns.update(data.keys())

        # Save individual year
        output_path = INTERIM_DATA_DIR / f"places_harmonized_{year}.csv"
        save_harmonized(tract_data, output_path)

        all_years_data[year] = tract_data
        logger.info(f"[{year}] Saved to {output_path}")

    # Create longitudinal dataset
    logger.info("")
    logger.info("Creating longitudinal dataset...")
    create_longitudinal_dataset(all_years_data, all_columns)


def save_harmonized(tract_data: Dict, output_path: Path) -> None:
    """Save harmonized data to CSV"""
    if not tract_data:
        return

    # Get all columns
    all_cols = set()
    for data in tract_data.values():
        all_cols.update(data.keys())

    # Order columns: metadata first, then measures
    meta_cols = ['Year', 'StateAbbr', 'CountyFIPS', 'TotalPopulation']
    measure_cols = sorted([c for c in all_cols if c not in meta_cols])
    columns = ['TractFIPS'] + meta_cols + measure_cols

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()

        for tract_id, data in sorted(tract_data.items()):
            row = {'TractFIPS': tract_id}
            row.update(data)
            writer.writerow(row)


def create_longitudinal_dataset(all_years_data: Dict, all_columns: set) -> None:
    """
    Create a single longitudinal dataset with all years
    """
    output_path = INTERIM_DATA_DIR / "places_longitudinal.csv"

    # Order columns
    meta_cols = ['TractFIPS', 'Year', 'StateAbbr', 'CountyFIPS', 'TotalPopulation']
    measure_cols = sorted([c for c in all_columns if c not in meta_cols and c not in {'Year'}])
    columns = meta_cols + measure_cols

    total_rows = 0

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()

        for year in sorted(all_years_data.keys()):
            tract_data = all_years_data[year]

            for tract_id, data in sorted(tract_data.items()):
                row = {'TractFIPS': tract_id}
                row.update(data)
                writer.writerow(row)
                total_rows += 1

    logger.info(f"Created longitudinal dataset: {output_path}")
    logger.info(f"  Total rows: {total_rows:,}")
    logger.info(f"  Columns: {len(columns)}")


def create_trajectory_analysis_file() -> None:
    """
    Create analysis-ready file with CHBI components across years

    This creates a panel dataset with:
    - One row per tract-year
    - Only CHBI component measures
    - Calculated burden index
    """
    logger.info("")
    logger.info("Creating trajectory analysis file...")

    input_path = INTERIM_DATA_DIR / "places_longitudinal.csv"
    output_path = INTERIM_DATA_DIR / "places_trajectory_panel.csv"

    if not input_path.exists():
        logger.error(f"Longitudinal file not found: {input_path}")
        return

    # Output columns
    meta_cols = ['TractFIPS', 'Year', 'StateAbbr', 'CountyFIPS', 'TotalPopulation']
    chbi_cols = [f'{m}_CrudePrev' for m in CHBI_MEASURES.keys()]

    with open(input_path, 'r', encoding='utf-8') as fin, \
         open(output_path, 'w', encoding='utf-8', newline='') as fout:

        reader = csv.DictReader(fin)

        # Add CHBI column
        output_cols = meta_cols + chbi_cols + ['CHBI']
        writer = csv.DictWriter(fout, fieldnames=output_cols, extrasaction='ignore')
        writer.writeheader()

        rows_written = 0
        for row in reader:
            # Calculate CHBI (weighted average of components)
            chbi_values = []
            weights = []

            for measure, weight in [
                ('OBESITY', 0.20),
                ('DIABETES', 0.20),
                ('CHD', 0.15),
                ('BPHIGH', 0.10),
                ('LPA', 0.10),
                ('MHLTH', 0.15),
                ('PHLTH', 0.10),
            ]:
                col = f'{measure}_CrudePrev'
                val = row.get(col, '')
                if val and val != 'None':
                    try:
                        chbi_values.append(float(val))
                        weights.append(weight)
                    except ValueError:
                        pass

            # Calculate weighted average
            if chbi_values and sum(weights) > 0:
                chbi = sum(v * w for v, w in zip(chbi_values, weights)) / sum(weights)
                row['CHBI'] = f"{chbi:.2f}"
            else:
                row['CHBI'] = ''

            writer.writerow(row)
            rows_written += 1

        logger.info(f"Created trajectory panel: {output_path}")
        logger.info(f"  Rows: {rows_written:,}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Harmonize CDC PLACES data")
    parser.add_argument('--years', type=int, nargs='+',
                       help='Specific years to process (default: all)')
    parser.add_argument('--skip-trajectory', action='store_true',
                       help='Skip trajectory analysis file creation')

    args = parser.parse_args()

    # Harmonize all years
    harmonize_all_years(years=args.years)

    # Create trajectory analysis file
    if not args.skip_trajectory:
        create_trajectory_analysis_file()

    logger.info("")
    logger.info("Harmonization complete!")
