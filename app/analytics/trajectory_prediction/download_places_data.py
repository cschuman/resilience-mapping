"""
Download historical CDC PLACES census tract data for trajectory prediction

Data sources:
- 2020 Release: https://data.cdc.gov/500-Cities-Places/PLACES-Local-Data-for-Better-Health-Census-Tract-D/4ai3-zynv
- 2021 Release: https://data.cdc.gov/500-Cities-Places/PLACES-Local-Data-for-Better-Health-Census-Tract-D/373s-ayzu
- 2022 Release: https://data.cdc.gov/500-Cities-Places/PLACES-Local-Data-for-Better-Health-Census-Tract-D/shc3-fzig
- 2023 Release: https://data.cdc.gov/500-Cities-Places/PLACES-Local-Data-for-Better-Health-Census-Tract-D/em5e-5hvn
- 2024 Release: https://data.cdc.gov/500-Cities-Places/PLACES-Local-Data-for-Better-Health-Census-Tract-D/yjkw-uj5s
- 2025 Release: https://data.cdc.gov/500-Cities-Places/PLACES-Local-Data-for-Better-Health-Census-Tract-D/cwsq-ngmh
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Optional
import urllib.request
import time

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# CDC PLACES data.cdc.gov dataset identifiers by year
# Format: {year: dataset_id} - These are used in the Socrata API
PLACES_DATASETS = {
    2020: "4ai3-zynv",   # First PLACES release
    2021: "373s-ayzu",   # 2021 release
    2022: "shc3-fzig",   # 2022 release (GIS friendly format also available)
    2023: "em5e-5hvn",   # 2023 release
    2024: "yjkw-uj5s",   # 2024 release (GIS friendly format)
    2025: "cwsq-ngmh",   # 2025 release (current)
}

# Column mappings may vary by year - we'll standardize during processing
COLUMN_MAPPINGS = {
    # Old column names -> Standard names
    "LocationID": "LocationID",
    "TractFIPS": "LocationID",
    "GEOID": "LocationID",
    "Census Tract FIPS": "LocationID",
}


def get_download_url(dataset_id: str, format: str = "csv", limit: int = 500000) -> str:
    """
    Construct Socrata API URL for downloading CDC data

    Parameters
    ----------
    dataset_id : str
        The 9-character Socrata dataset identifier
    format : str
        Download format (csv, json, geojson)
    limit : int
        Maximum number of rows (Socrata default is 1000)

    Returns
    -------
    str
        Full download URL
    """
    # Socrata Open Data API endpoint for data.cdc.gov
    base_url = f"https://data.cdc.gov/api/views/{dataset_id}/rows.{format}"
    params = f"?accessType=DOWNLOAD"

    return base_url + params


def download_places_year(year: int, dataset_id: str, output_dir: Path, overwrite: bool = False) -> Optional[Path]:
    """
    Download PLACES data for a specific year

    Parameters
    ----------
    year : int
        Release year
    dataset_id : str
        Socrata dataset identifier
    output_dir : Path
        Directory to save downloaded file
    overwrite : bool
        Whether to overwrite existing files

    Returns
    -------
    Path or None
        Path to downloaded file, or None if failed
    """
    output_file = output_dir / f"places_tract_{year}.csv"

    if output_file.exists() and not overwrite:
        logger.info(f"[{year}] File already exists: {output_file}")
        return output_file

    url = get_download_url(dataset_id)
    logger.info(f"[{year}] Downloading from: {url}")

    try:
        # Download with progress reporting
        def reporthook(blocknum, blocksize, totalsize):
            if totalsize > 0:
                pct = min(100, blocknum * blocksize * 100 / totalsize)
                sys.stdout.write(f"\r[{year}] Downloading: {pct:.1f}%")
                sys.stdout.flush()

        urllib.request.urlretrieve(url, output_file, reporthook)
        sys.stdout.write("\n")

        # Verify file was downloaded
        file_size = output_file.stat().st_size
        logger.info(f"[{year}] Downloaded: {output_file} ({file_size / 1_000_000:.1f} MB)")

        return output_file

    except Exception as e:
        logger.error(f"[{year}] Download failed: {e}")
        if output_file.exists():
            output_file.unlink()  # Remove partial file
        return None


def download_all_places_data(years: Optional[list] = None, overwrite: bool = False) -> Dict[int, Path]:
    """
    Download PLACES data for all specified years

    Parameters
    ----------
    years : list of int, optional
        Years to download. If None, downloads all available.
    overwrite : bool
        Whether to overwrite existing files

    Returns
    -------
    dict
        Mapping of year -> file path for successful downloads
    """
    if years is None:
        years = list(PLACES_DATASETS.keys())

    logger.info("="*60)
    logger.info("CDC PLACES Historical Data Download")
    logger.info("="*60)
    logger.info(f"Years to download: {years}")
    logger.info(f"Output directory: {RAW_DATA_DIR}")
    logger.info("")

    results = {}
    failed = []

    for year in sorted(years):
        if year not in PLACES_DATASETS:
            logger.warning(f"No dataset available for year {year}")
            continue

        dataset_id = PLACES_DATASETS[year]
        result = download_places_year(year, dataset_id, RAW_DATA_DIR, overwrite)

        if result:
            results[year] = result
        else:
            failed.append(year)

        # Rate limiting - be nice to the CDC servers
        time.sleep(2)

    # Summary
    logger.info("")
    logger.info("="*60)
    logger.info("DOWNLOAD SUMMARY")
    logger.info("="*60)
    logger.info(f"Successfully downloaded: {len(results)} years")
    for year, path in sorted(results.items()):
        size_mb = path.stat().st_size / 1_000_000
        logger.info(f"  {year}: {path.name} ({size_mb:.1f} MB)")

    if failed:
        logger.warning(f"Failed downloads: {failed}")

    return results


def verify_downloads(data_dir: Path = RAW_DATA_DIR) -> Dict[int, dict]:
    """
    Verify downloaded files and report basic statistics

    Parameters
    ----------
    data_dir : Path
        Directory containing downloaded files

    Returns
    -------
    dict
        Mapping of year -> file statistics
    """
    import csv

    stats = {}

    for year in PLACES_DATASETS.keys():
        file_path = data_dir / f"places_tract_{year}.csv"

        if not file_path.exists():
            logger.warning(f"[{year}] File not found: {file_path}")
            continue

        # Get basic file stats
        file_size = file_path.stat().st_size

        # Count rows and get column names
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            columns = next(reader)
            row_count = sum(1 for _ in reader)

        stats[year] = {
            'file': file_path,
            'size_mb': file_size / 1_000_000,
            'rows': row_count,
            'columns': len(columns),
            'column_names': columns[:10],  # First 10 columns
        }

        logger.info(f"[{year}] Rows: {row_count:,}, Columns: {len(columns)}, Size: {file_size/1_000_000:.1f} MB")

    return stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download CDC PLACES historical data")
    parser.add_argument('--years', type=int, nargs='+',
                       help='Specific years to download (default: all)')
    parser.add_argument('--overwrite', action='store_true',
                       help='Overwrite existing files')
    parser.add_argument('--verify', action='store_true',
                       help='Verify existing downloads instead of downloading')

    args = parser.parse_args()

    if args.verify:
        stats = verify_downloads()
        print(f"\nVerified {len(stats)} downloads")
    else:
        results = download_all_places_data(
            years=args.years,
            overwrite=args.overwrite
        )

        # Verify after download
        if results:
            print("\nVerifying downloads...")
            verify_downloads()
