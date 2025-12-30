"""
Data preparation for Community Health Trajectory Prediction

Loads and merges:
- CDC PLACES data (2020-2025)
- Census ACS 5-year estimates (2015-2023)
- USDA Food Access Research Atlas (2019)
- Spatial geometries (census tract boundaries)
"""

import pandas as pd
import geopandas as gpd
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
import logging
from .config import (
    RAW_DATA_DIR, INTERIM_DATA_DIR, PROCESSED_DATA_DIR,
    PLACES_YEARS, ACS_YEARS, CHBI_COMPONENTS
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_places_longitudinal(years: Optional[List[int]] = None) -> pd.DataFrame:
    """
    Load CDC PLACES data for multiple years

    Parameters
    ----------
    years : list of int, optional
        Years to load. If None, loads all available years from config.

    Returns
    -------
    pd.DataFrame
        Longitudinal PLACES data with columns:
        - LocationID: Census tract FIPS code
        - Year: Data year
        - MeasureId: Health outcome identifier
        - Data_Value: Prevalence estimate
        - Low_Confidence_Limit, High_Confidence_Limit: 95% CI
        - TotalPopulation: Tract population
    """
    if years is None:
        years = PLACES_YEARS

    logger.info(f"Loading PLACES data for years: {years}")

    dfs = []
    for year in years:
        # Adjust file path based on your data structure
        # Assuming files like: data/raw/places_tract_2023.csv
        file_path = RAW_DATA_DIR / f"places_tract_{year}.csv"

        if not file_path.exists():
            logger.warning(f"PLACES data for {year} not found at {file_path}")
            continue

        df = pd.read_csv(file_path)
        df['Year'] = year
        dfs.append(df)
        logger.info(f"  Loaded {len(df)} records for {year}")

    if not dfs:
        raise FileNotFoundError("No PLACES data files found. Check RAW_DATA_DIR.")

    # Concatenate all years
    places_long = pd.concat(dfs, ignore_index=True)

    # Standardize column names
    places_long = places_long.rename(columns={
        'LocationName': 'TractName',
        'StateAbbr': 'State',
        'StateDesc': 'StateName',
        'CountyFIPS': 'CountyFIPS',
        'CountyName': 'County',
        'TractFIPS': 'LocationID',  # Some files use different names
    })

    # Ensure LocationID is 11-digit FIPS code
    if 'LocationID' in places_long.columns:
        places_long['LocationID'] = places_long['LocationID'].astype(str).str.zfill(11)

    logger.info(f"Total PLACES records: {len(places_long)}")
    logger.info(f"Unique tracts: {places_long['LocationID'].nunique()}")
    logger.info(f"Unique measures: {places_long['MeasureId'].nunique()}")

    return places_long


def create_composite_health_burden_index(places_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create Composite Health Burden Index (CHBI) from PLACES outcomes

    Parameters
    ----------
    places_df : pd.DataFrame
        Longitudinal PLACES data from load_places_longitudinal()

    Returns
    -------
    pd.DataFrame
        Tract-year level data with CHBI scores
        Columns: LocationID, Year, CHBI, CHBI_zscore, [component outcomes]
    """
    logger.info("Creating Composite Health Burden Index (CHBI)")

    # Filter to CHBI component outcomes
    chbi_outcomes = list(CHBI_COMPONENTS.keys())
    places_chbi = places_df[places_df['MeasureId'].isin(chbi_outcomes)].copy()

    # Pivot to wide format (one row per tract-year, columns for each outcome)
    chbi_wide = places_chbi.pivot_table(
        index=['LocationID', 'Year'],
        columns='MeasureId',
        values='Data_Value',
        aggfunc='first'  # Should only be one value per tract-year-outcome
    ).reset_index()

    # Check for missing outcomes
    missing_outcomes = set(chbi_outcomes) - set(chbi_wide.columns)
    if missing_outcomes:
        logger.warning(f"Missing outcomes in data: {missing_outcomes}")

    # Calculate weighted CHBI
    chbi_wide['CHBI'] = 0
    for outcome, weight in CHBI_COMPONENTS.items():
        if outcome in chbi_wide.columns:
            # Replace NaN with median (conservative imputation)
            outcome_median = chbi_wide[outcome].median()
            chbi_wide[outcome] = chbi_wide[outcome].fillna(outcome_median)
            chbi_wide['CHBI'] += chbi_wide[outcome] * weight
        else:
            logger.warning(f"Outcome {outcome} not found, excluding from CHBI")

    # Standardize CHBI within each year (z-score)
    # This accounts for national trends and model updates
    chbi_wide['CHBI_zscore'] = chbi_wide.groupby('Year')['CHBI'].transform(
        lambda x: (x - x.mean()) / x.std()
    )

    logger.info(f"CHBI calculated for {len(chbi_wide)} tract-years")
    logger.info(f"CHBI range: {chbi_wide['CHBI'].min():.2f} to {chbi_wide['CHBI'].max():.2f}")
    logger.info(f"CHBI mean by year:\n{chbi_wide.groupby('Year')['CHBI'].mean()}")

    return chbi_wide


def load_census_acs(years: Optional[List[int]] = None) -> pd.DataFrame:
    """
    Load Census American Community Survey (ACS) 5-year estimates

    Parameters
    ----------
    years : list of int, optional
        Years to load (e.g., [2019, 2021] for 2015-2019 and 2017-2021 estimates)

    Returns
    -------
    pd.DataFrame
        Census tract-level social determinants of health indicators

    Notes
    -----
    Key variables to include:
    - B01003: Total population
    - B19013: Median household income
    - B17001: Poverty status
    - B15003: Educational attainment
    - B25064: Median gross rent
    - B25077: Median home value
    - B03002: Race/ethnicity
    - B08301: Means of transportation to work
    """
    if years is None:
        years = ACS_YEARS

    logger.info(f"Loading ACS data for years: {years}")

    # Placeholder - actual implementation depends on your data source
    # Options:
    # 1. Pre-downloaded CSV files from data.census.gov
    # 2. API calls to Census Bureau API
    # 3. IPUMS NHGIS extracts

    # Example structure (you'll need to customize):
    dfs = []
    for year in years:
        file_path = RAW_DATA_DIR / f"acs_{year}_tract.csv"
        if file_path.exists():
            df = pd.read_csv(file_path)
            df['Year'] = year
            dfs.append(df)

    if not dfs:
        logger.warning("No ACS data files found. Returning empty DataFrame.")
        return pd.DataFrame()

    acs_long = pd.concat(dfs, ignore_index=True)

    # Standardize FIPS codes
    acs_long['LocationID'] = acs_long['GEOID'].astype(str).str.zfill(11)

    logger.info(f"Loaded ACS data for {len(acs_long)} tract-years")

    return acs_long


def load_tract_geometries(year: int = 2020) -> gpd.GeoDataFrame:
    """
    Load census tract boundary geometries

    Parameters
    ----------
    year : int
        Census year for tract boundaries (2010 or 2020)

    Returns
    -------
    gpd.GeoDataFrame
        Tract geometries with FIPS codes
    """
    logger.info(f"Loading tract geometries for {year}")

    # Assuming you have a shapefile or GeoJSON of tract boundaries
    # Download from: https://www.census.gov/cgi-bin/geo/shapefiles/index.php

    file_path = RAW_DATA_DIR / f"census_tracts_{year}" / f"tl_{year}_*_tract.shp"

    # For now, return placeholder
    logger.warning("Tract geometry loading not yet implemented")
    return gpd.GeoDataFrame()


def merge_all_data(
    chbi_df: pd.DataFrame,
    acs_df: pd.DataFrame,
    geometry_df: Optional[gpd.GeoDataFrame] = None
) -> pd.DataFrame:
    """
    Merge CHBI, ACS, and geometry data into analysis-ready format

    Parameters
    ----------
    chbi_df : pd.DataFrame
        Output from create_composite_health_burden_index()
    acs_df : pd.DataFrame
        Output from load_census_acs()
    geometry_df : gpd.GeoDataFrame, optional
        Tract geometries

    Returns
    -------
    pd.DataFrame or gpd.GeoDataFrame
        Merged dataset ready for feature engineering
    """
    logger.info("Merging CHBI, ACS, and geometry data")

    # Start with CHBI
    merged = chbi_df.copy()

    # Merge ACS data
    if not acs_df.empty:
        merged = merged.merge(
            acs_df,
            on=['LocationID', 'Year'],
            how='left',
            suffixes=('', '_acs')
        )
        logger.info(f"Merged with ACS data: {len(merged)} rows")

    # Merge geometries (optional, for spatial analysis)
    if geometry_df is not None and not geometry_df.empty:
        merged = merged.merge(
            geometry_df[['LocationID', 'geometry']],
            on='LocationID',
            how='left'
        )
        merged = gpd.GeoDataFrame(merged, geometry='geometry')
        logger.info("Added tract geometries")

    # Sort by tract and year for time series operations
    merged = merged.sort_values(['LocationID', 'Year'])

    # Report missingness
    missing_pct = merged.isnull().sum() / len(merged) * 100
    high_missing = missing_pct[missing_pct > 10]
    if not high_missing.empty:
        logger.warning(f"Columns with >10% missing data:\n{high_missing}")

    return merged


def prepare_trajectory_data(save_path: Optional[Path] = None) -> pd.DataFrame:
    """
    End-to-end data preparation pipeline

    Parameters
    ----------
    save_path : Path, optional
        Where to save the prepared dataset

    Returns
    -------
    pd.DataFrame
        Analysis-ready dataset for trajectory prediction
    """
    logger.info("="*60)
    logger.info("PHASE 1: DATA PREPARATION")
    logger.info("="*60)

    # Step 1: Load PLACES data
    places = load_places_longitudinal()

    # Step 2: Create CHBI
    chbi = create_composite_health_burden_index(places)

    # Step 3: Load ACS data
    acs = load_census_acs()

    # Step 4: Load geometries (optional)
    # geometries = load_tract_geometries(year=2020)
    geometries = None  # Skip for now

    # Step 5: Merge all data
    merged = merge_all_data(chbi, acs, geometries)

    # Step 6: Save
    if save_path is None:
        save_path = PROCESSED_DATA_DIR / "trajectory_analysis_ready.parquet"

    merged.to_parquet(save_path, index=False)
    logger.info(f"Saved analysis-ready data to {save_path}")
    logger.info(f"Final dataset: {len(merged)} rows, {len(merged.columns)} columns")

    return merged


if __name__ == "__main__":
    # Run data preparation
    df = prepare_trajectory_data()
    print("\nData preparation complete!")
    print(f"Dataset shape: {df.shape}")
    print(f"\nColumns: {df.columns.tolist()}")
    print(f"\nFirst few rows:\n{df.head()}")
