"""
Feature engineering for Community Health Trajectory Prediction

Creates:
- Temporal features (trends, acceleration, volatility)
- Social determinant change features (income mobility, gentrification risk)
- Spatial features (lags, clustering, spillovers)
- Interaction features
- Target labels (DECLINE, STABLE, IMPROVE)
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import percentileofscore
from typing import Tuple, List, Optional
import logging
from .config import (
    TRAJECTORY_THRESHOLDS, TRAJECTORY_LABELS,
    PROCESSED_DATA_DIR
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_temporal_features(df: pd.DataFrame, target_col: str = 'CHBI_zscore') -> pd.DataFrame:
    """
    Calculate temporal trend features from time series data

    Parameters
    ----------
    df : pd.DataFrame
        Tract-year level data sorted by LocationID and Year
    target_col : str
        Column to calculate trends for (e.g., CHBI_zscore)

    Returns
    -------
    pd.DataFrame
        Original data with added temporal features
    """
    logger.info(f"Calculating temporal features for {target_col}")

    df = df.sort_values(['LocationID', 'Year'])

    # Group by tract
    grouped = df.groupby('LocationID')

    # 1. Linear trend slope (requires 3+ observations)
    def calculate_slope(group):
        if len(group) < 3:
            return np.nan
        years = group['Year'].values
        values = group[target_col].values
        # Remove NaN
        mask = ~np.isnan(values)
        if mask.sum() < 3:
            return np.nan
        slope, _, _, _, _ = stats.linregress(years[mask], values[mask])
        return slope

    df['trend_slope'] = grouped.apply(
        lambda g: pd.Series(calculate_slope(g), index=g.index)
    ).values

    # 2. Acceleration (2nd derivative)
    df['acceleration'] = grouped[target_col].apply(
        lambda x: x - 2 * x.shift(1) + x.shift(2)
    ).values

    # 3. Volatility (std of year-to-year changes)
    df['volatility'] = grouped[target_col].apply(
        lambda x: x.diff().rolling(window=3, min_periods=2).std()
    ).values

    # 4. Momentum (rate of change)
    df['momentum'] = grouped[target_col].apply(
        lambda x: (x - x.shift(1)) / x.shift(1).abs()
    ).values

    # 5. Percentile rank within year
    df['percentile_rank'] = df.groupby('Year')[target_col].rank(pct=True)

    # 6. Distance from high-risk threshold (95th percentile)
    high_risk_threshold = df.groupby('Year')[target_col].transform(lambda x: x.quantile(0.95))
    df['distance_to_high_risk'] = high_risk_threshold - df[target_col]

    # 7. Crossing events (did tract cross into high-risk zone?)
    df['crossed_into_high_risk'] = (
        (df['percentile_rank'] > 0.95) &
        (df.groupby('LocationID')['percentile_rank'].shift(1) <= 0.95)
    ).astype(int)

    logger.info(f"Added {6} temporal features")

    return df


def calculate_sdoh_change_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate social determinant of health change features

    Requires ACS variables:
    - median_income
    - poverty_rate
    - college_educated_pct
    - median_rent
    - white_pct (for gentrification analysis)
    - moved_in_last_year_pct (residential instability)

    Parameters
    ----------
    df : pd.DataFrame
        Merged data with ACS variables

    Returns
    -------
    pd.DataFrame
        Data with SDOH change features
    """
    logger.info("Calculating SDOH change features")

    df = df.sort_values(['LocationID', 'Year'])
    grouped = df.groupby('LocationID')

    # Check for required columns
    required_cols = ['median_income', 'poverty_rate']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        logger.warning(f"Missing required SDOH columns: {missing}")
        logger.warning("Creating placeholder features (implement ACS data loading first)")
        # Create dummy columns for now
        for col in missing:
            df[col] = np.nan

    # 1. Income trajectory (3-year change)
    df['income_trajectory'] = grouped['median_income'].apply(
        lambda x: (x - x.shift(3)) / x.shift(3)
    ).values

    # 2. Income acceleration
    df['income_acceleration'] = grouped['median_income'].apply(
        lambda x: x - 2 * x.shift(1) + x.shift(2)
    ).values

    # 3. Poverty rate velocity
    df['poverty_velocity'] = grouped['poverty_rate'].apply(
        lambda x: x - x.shift(1)
    ).values

    # 4. Gentrification risk score (simplified - enhance when ACS data available)
    if all(col in df.columns for col in ['college_educated_pct', 'median_rent', 'white_pct']):
        # Calculate component growth rates
        college_growth = grouped['college_educated_pct'].pct_change(periods=3)
        rent_growth = grouped['median_rent'].pct_change(periods=3)
        white_growth = grouped['white_pct'].diff(periods=3)

        # Gentrification risk = weighted combination
        df['gentrification_risk'] = (
            (college_growth > 0.1).astype(float) * 0.35 +
            (rent_growth > 0.15).astype(float) * 0.35 +
            (white_growth > 5).astype(float) * 0.30
        )
    else:
        logger.warning("Cannot calculate gentrification risk - missing ACS variables")
        df['gentrification_risk'] = 0

    # 5. Population churn (residential instability)
    if 'moved_in_last_year_pct' in df.columns:
        df['churn_rate'] = df['moved_in_last_year_pct']
        df['churn_acceleration'] = grouped['churn_rate'].apply(
            lambda x: x - x.shift(1)
        ).values
    else:
        df['churn_rate'] = np.nan
        df['churn_acceleration'] = np.nan

    logger.info("Added SDOH change features")

    return df


def calculate_spatial_features(df: pd.DataFrame, geometry_col: Optional[str] = 'geometry') -> pd.DataFrame:
    """
    Calculate spatial features (requires geometries)

    Features:
    - Spatial lag (average of neighbors)
    - Local Moran's I (clustering statistic)
    - Distance to nearest declining tract

    Parameters
    ----------
    df : pd.DataFrame or gpd.GeoDataFrame
        Data with geometries
    geometry_col : str
        Name of geometry column

    Returns
    -------
    pd.DataFrame
        Data with spatial features
    """
    logger.info("Calculating spatial features")

    if geometry_col not in df.columns:
        logger.warning(f"No {geometry_col} column found - skipping spatial features")
        df['spatial_lag_CHBI'] = np.nan
        df['local_morans_I'] = np.nan
        df['cluster_type'] = 'NA'
        return df

    # Spatial features require libpysal
    try:
        from libpysal.weights import Queen
        from esda.moran import Moran_Local
    except ImportError:
        logger.error("libpysal not installed - cannot calculate spatial features")
        logger.info("Install with: pip install libpysal esda")
        df['spatial_lag_CHBI'] = np.nan
        df['local_morans_I'] = np.nan
        df['cluster_type'] = 'NA'
        return df

    import geopandas as gpd

    # Convert to GeoDataFrame if not already
    if not isinstance(df, gpd.GeoDataFrame):
        df = gpd.GeoDataFrame(df, geometry=geometry_col)

    # Calculate spatial weights (queen contiguity)
    # Do this for each year separately (in case boundaries change)
    for year in df['Year'].unique():
        year_mask = df['Year'] == year
        gdf_year = df[year_mask].copy()

        if len(gdf_year) < 10:
            continue

        # Build spatial weights matrix
        w = Queen.from_dataframe(gdf_year)

        # Spatial lag of CHBI
        chbi_values = gdf_year['CHBI_zscore'].values
        spatial_lag = w.sparse.dot(chbi_values) / w.cardinalities

        df.loc[year_mask, 'spatial_lag_CHBI'] = spatial_lag

        # Local Moran's I
        try:
            moran_loc = Moran_Local(chbi_values, w)
            df.loc[year_mask, 'local_morans_I'] = moran_loc.Is
            df.loc[year_mask, 'cluster_type'] = moran_loc.q  # 1=HH, 2=LH, 3=LL, 4=HL
        except Exception as e:
            logger.warning(f"Could not calculate Local Moran's I for {year}: {e}")

    logger.info("Added spatial features")

    return df


def create_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create interaction features between key predictors

    Parameters
    ----------
    df : pd.DataFrame
        Data with engineered features

    Returns
    -------
    pd.DataFrame
        Data with interaction features
    """
    logger.info("Creating interaction features")

    # Critical interactions for health trajectory prediction

    # 1. Gentrification × Low Income (displacement vulnerability)
    if 'gentrification_risk' in df.columns and 'poverty_rate' in df.columns:
        df['displacement_risk'] = df['gentrification_risk'] * df['poverty_rate']

    # 2. Spatial lag decline × Residential instability (contagion risk)
    if 'spatial_lag_CHBI' in df.columns and 'churn_rate' in df.columns:
        df['contagion_risk'] = df['spatial_lag_CHBI'] * df['churn_rate']

    # 3. Poverty acceleration × Healthcare access (barrier to care)
    # Note: Requires healthcare access variable from ACS or other source
    if 'poverty_velocity' in df.columns:
        # Placeholder - enhance when healthcare access data available
        df['healthcare_barrier_risk'] = df['poverty_velocity']

    # 4. Trend slope × Volatility (unstable trajectories)
    if 'trend_slope' in df.columns and 'volatility' in df.columns:
        df['trajectory_instability'] = df['trend_slope'] * df['volatility']

    logger.info("Added interaction features")

    return df


def create_trajectory_labels(
    df: pd.DataFrame,
    target_col: str = 'CHBI_zscore',
    horizon_years: int = 1,
    decline_threshold: float = None,
    improve_threshold: float = None
) -> pd.DataFrame:
    """
    Create trajectory classification labels (DECLINE, STABLE, IMPROVE)

    Parameters
    ----------
    df : pd.DataFrame
        Data sorted by LocationID and Year
    target_col : str
        Column to calculate trajectory from
    horizon_years : int
        How many years ahead to predict (1 = 12 months, 2 = 24 months)
    decline_threshold : float
        Z-score threshold for DECLINE class (default from config)
    improve_threshold : float
        Z-score threshold for IMPROVE class (default from config)

    Returns
    -------
    pd.DataFrame
        Data with trajectory_label column
    """
    logger.info(f"Creating trajectory labels with {horizon_years}-year horizon")

    if decline_threshold is None:
        decline_threshold = TRAJECTORY_THRESHOLDS['decline_threshold']
    if improve_threshold is None:
        improve_threshold = TRAJECTORY_THRESHOLDS['improve_threshold']

    df = df.sort_values(['LocationID', 'Year'])

    # Calculate change over horizon
    df['future_chbi'] = df.groupby('LocationID')[target_col].shift(-horizon_years)
    df['chbi_change'] = df['future_chbi'] - df[target_col]

    # Classify trajectory
    conditions = [
        df['chbi_change'] > decline_threshold,     # DECLINE (health burden increasing)
        df['chbi_change'] < improve_threshold,     # IMPROVE (health burden decreasing)
    ]
    choices = [
        TRAJECTORY_LABELS['DECLINE'],
        TRAJECTORY_LABELS['IMPROVE']
    ]
    df['trajectory_label'] = np.select(conditions, choices, default=TRAJECTORY_LABELS['STABLE'])

    # Remove rows where we don't have future data (last year(s) of dataset)
    df['has_trajectory_label'] = df['future_chbi'].notna()

    # Statistics
    label_dist = df[df['has_trajectory_label']]['trajectory_label'].value_counts()
    label_pct = label_dist / label_dist.sum() * 100

    logger.info(f"\nTrajectory label distribution:")
    for label_name, label_value in TRAJECTORY_LABELS.items():
        count = label_dist.get(label_value, 0)
        pct = label_pct.get(label_value, 0)
        logger.info(f"  {label_name}: {count} ({pct:.1f}%)")

    return df


def engineer_features(
    df: pd.DataFrame,
    include_spatial: bool = True,
    horizon_years: int = 1
) -> pd.DataFrame:
    """
    End-to-end feature engineering pipeline

    Parameters
    ----------
    df : pd.DataFrame
        Analysis-ready data from data_preparation
    include_spatial : bool
        Whether to calculate spatial features (requires geometries)
    horizon_years : int
        Prediction horizon for trajectory labels

    Returns
    -------
    pd.DataFrame
        Fully featured dataset ready for modeling
    """
    logger.info("="*60)
    logger.info("PHASE 2: FEATURE ENGINEERING")
    logger.info("="*60)

    # Make a copy to avoid modifying original
    df = df.copy()

    # 1. Temporal features
    df = calculate_temporal_features(df, target_col='CHBI_zscore')

    # 2. SDOH change features
    df = calculate_sdoh_change_features(df)

    # 3. Spatial features (optional)
    if include_spatial:
        df = calculate_spatial_features(df)

    # 4. Interaction features
    df = create_interaction_features(df)

    # 5. Create target labels
    df = create_trajectory_labels(df, horizon_years=horizon_years)

    # Report feature summary
    feature_cols = [col for col in df.columns if col not in [
        'LocationID', 'Year', 'TractName', 'State', 'County',
        'geometry', 'future_chbi', 'has_trajectory_label'
    ]]
    logger.info(f"\nTotal features created: {len(feature_cols)}")
    logger.info(f"Features with >50% missing: {(df[feature_cols].isnull().sum() > len(df)*0.5).sum()}")

    return df


if __name__ == "__main__":
    # Example usage
    logger.info("Loading analysis-ready data...")

    # Load prepared data
    data_path = PROCESSED_DATA_DIR / "trajectory_analysis_ready.parquet"
    if not data_path.exists():
        logger.error(f"Data file not found: {data_path}")
        logger.info("Run data_preparation.py first")
        exit(1)

    df = pd.read_parquet(data_path)

    # Engineer features
    df_featured = engineer_features(df, include_spatial=False, horizon_years=1)

    # Save
    output_path = PROCESSED_DATA_DIR / "features_and_targets.parquet"
    df_featured.to_parquet(output_path, index=False)

    logger.info(f"\nFeature engineering complete!")
    logger.info(f"Saved to: {output_path}")
    logger.info(f"Shape: {df_featured.shape}")
