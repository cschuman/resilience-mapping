"""
Temporal cross-validation framework for trajectory prediction

Implements expanding window CV to prevent data leakage:
- Train on years 2020-2021 → Validate on 2022
- Train on years 2020-2022 → Validate on 2023
- Train on years 2020-2023 → Validate on 2024
etc.

This mimics real-world deployment where we only have data up to time T
to predict T+1.
"""

import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, Generator
from sklearn.model_selection import BaseCrossValidator
import logging
from .config import CV_CONFIG, RANDOM_SEED

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TemporalCrossValidator(BaseCrossValidator):
    """
    Temporal cross-validation with expanding window

    Prevents data leakage by ensuring training data always precedes
    validation data chronologically.

    Parameters
    ----------
    validation_years : list of int
        Years to use as validation sets
    min_train_years : int
        Minimum number of years needed for training
    expanding_window : bool
        If True, use expanding window (train set grows over time)
        If False, use rolling window (train set size stays constant)

    Examples
    --------
    >>> cv = TemporalCrossValidator(
    ...     validation_years=[2022, 2023, 2024],
    ...     min_train_years=2
    ... )
    >>> for train_idx, val_idx in cv.split(df, year_col='Year'):
    ...     X_train, X_val = df.iloc[train_idx], df.iloc[val_idx]
    """

    def __init__(
        self,
        validation_years: List[int] = None,
        min_train_years: int = 2,
        expanding_window: bool = True
    ):
        if validation_years is None:
            validation_years = CV_CONFIG['validation_years']

        self.validation_years = sorted(validation_years)
        self.min_train_years = min_train_years
        self.expanding_window = expanding_window

        logger.info(f"TemporalCrossValidator initialized")
        logger.info(f"  Validation years: {self.validation_years}")
        logger.info(f"  Min train years: {self.min_train_years}")
        logger.info(f"  Window type: {'expanding' if expanding_window else 'rolling'}")

    def get_n_splits(self, X=None, y=None, groups=None):
        """Returns the number of splitting iterations"""
        return len(self.validation_years)

    def split(
        self,
        df: pd.DataFrame,
        year_col: str = 'Year'
    ) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        """
        Generate train/validation splits

        Parameters
        ----------
        df : pd.DataFrame
            Data to split, must contain year_col
        year_col : str
            Name of column containing year

        Yields
        ------
        train_idx : np.ndarray
            Indices of training samples
        val_idx : np.ndarray
            Indices of validation samples
        """
        if year_col not in df.columns:
            raise ValueError(f"Column '{year_col}' not found in dataframe")

        years_available = sorted(df[year_col].unique())
        min_year = min(years_available)

        logger.info(f"\nGenerating temporal CV splits from {len(years_available)} years of data")

        for i, val_year in enumerate(self.validation_years, 1):
            if val_year not in years_available:
                logger.warning(f"Validation year {val_year} not in data - skipping")
                continue

            # Determine training years
            if self.expanding_window:
                # Expanding: use all years before validation year
                train_years = [y for y in years_available if y < val_year]
            else:
                # Rolling: use fixed window of min_train_years
                train_years = [y for y in years_available
                              if val_year - self.min_train_years <= y < val_year]

            if len(train_years) < self.min_train_years:
                logger.warning(
                    f"Insufficient training years for validation year {val_year} "
                    f"({len(train_years)} < {self.min_train_years}) - skipping"
                )
                continue

            # Get indices
            train_idx = df[df[year_col].isin(train_years)].index.values
            val_idx = df[df[year_col] == val_year].index.values

            logger.info(
                f"Split {i}/{len(self.validation_years)}: "
                f"Train years={train_years} (n={len(train_idx)}), "
                f"Val year={val_year} (n={len(val_idx)})"
            )

            yield train_idx, val_idx


def filter_complete_cases(
    df: pd.DataFrame,
    feature_cols: List[str],
    target_col: str = 'trajectory_label'
) -> pd.DataFrame:
    """
    Filter to complete cases (no missing features or target)

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with features and target
    feature_cols : list of str
        Feature column names
    target_col : str
        Target column name

    Returns
    -------
    pd.DataFrame
        Filtered dataset with complete cases
    """
    logger.info("Filtering to complete cases")

    # Check for target availability
    if 'has_trajectory_label' in df.columns:
        df = df[df['has_trajectory_label'] == True].copy()
        logger.info(f"  Filtered to rows with trajectory labels: {len(df)}")

    # Remove rows with missing features
    before = len(df)
    df = df.dropna(subset=feature_cols + [target_col])
    after = len(df)

    if before > after:
        logger.info(f"  Removed {before - after} rows with missing values ({(before-after)/before*100:.1f}%)")

    logger.info(f"  Final sample size: {len(df)}")

    return df


def get_feature_columns(df: pd.DataFrame, exclude_patterns: List[str] = None) -> List[str]:
    """
    Automatically identify feature columns

    Parameters
    ----------
    df : pd.DataFrame
        Dataset
    exclude_patterns : list of str
        Column name patterns to exclude

    Returns
    -------
    list of str
        Feature column names
    """
    if exclude_patterns is None:
        exclude_patterns = [
            'LocationID', 'Year', 'TractName', 'State', 'County',
            'geometry', 'trajectory_label', 'has_trajectory_label',
            'future_chbi', 'CHBI', 'chbi_change',  # Don't use raw CHBI or future values
        ]

    # All numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Exclude metadata and target
    feature_cols = [
        col for col in numeric_cols
        if not any(pattern in col for pattern in exclude_patterns)
    ]

    logger.info(f"Identified {len(feature_cols)} feature columns")

    return feature_cols


def create_cv_splits_summary(
    df: pd.DataFrame,
    cv: TemporalCrossValidator,
    year_col: str = 'Year',
    target_col: str = 'trajectory_label'
) -> pd.DataFrame:
    """
    Create summary table of CV splits

    Parameters
    ----------
    df : pd.DataFrame
        Dataset
    cv : TemporalCrossValidator
        Cross-validator
    year_col : str
        Year column name
    target_col : str
        Target column name

    Returns
    -------
    pd.DataFrame
        Summary table with split statistics
    """
    summaries = []

    for i, (train_idx, val_idx) in enumerate(cv.split(df, year_col=year_col), 1):
        train_df = df.iloc[train_idx]
        val_df = df.iloc[val_idx]

        # Calculate class distribution
        train_dist = train_df[target_col].value_counts(normalize=True).to_dict()
        val_dist = val_df[target_col].value_counts(normalize=True).to_dict()

        summary = {
            'split': i,
            'train_years': str(sorted(train_df[year_col].unique())),
            'val_year': val_df[year_col].iloc[0],
            'train_n': len(train_df),
            'val_n': len(val_df),
            'train_decline_pct': train_dist.get(0, 0) * 100,
            'train_stable_pct': train_dist.get(1, 0) * 100,
            'train_improve_pct': train_dist.get(2, 0) * 100,
            'val_decline_pct': val_dist.get(0, 0) * 100,
            'val_stable_pct': val_dist.get(1, 0) * 100,
            'val_improve_pct': val_dist.get(2, 0) * 100,
        }
        summaries.append(summary)

    summary_df = pd.DataFrame(summaries)

    logger.info("\nCross-validation splits summary:")
    logger.info(f"\n{summary_df.to_string(index=False)}")

    return summary_df


if __name__ == "__main__":
    # Example usage
    from .config import PROCESSED_DATA_DIR

    # Load featured data
    data_path = PROCESSED_DATA_DIR / "features_and_targets.parquet"
    if not data_path.exists():
        logger.error(f"Data not found: {data_path}")
        logger.info("Run feature_engineering.py first")
        exit(1)

    df = pd.read_parquet(data_path)
    logger.info(f"Loaded data: {df.shape}")

    # Initialize CV
    cv = TemporalCrossValidator(
        validation_years=[2022, 2023, 2024],
        min_train_years=2,
        expanding_window=True
    )

    # Get feature columns
    feature_cols = get_feature_columns(df)
    logger.info(f"Features: {feature_cols[:10]}... ({len(feature_cols)} total)")

    # Filter to complete cases
    df_clean = filter_complete_cases(df, feature_cols, target_col='trajectory_label')

    # Create splits summary
    summary = create_cv_splits_summary(df_clean, cv)

    # Example: iterate through splits
    for i, (train_idx, val_idx) in enumerate(cv.split(df_clean), 1):
        X_train = df_clean.iloc[train_idx][feature_cols]
        y_train = df_clean.iloc[train_idx]['trajectory_label']
        X_val = df_clean.iloc[val_idx][feature_cols]
        y_val = df_clean.iloc[val_idx]['trajectory_label']

        logger.info(f"\nSplit {i}:")
        logger.info(f"  X_train shape: {X_train.shape}")
        logger.info(f"  y_train dist: {y_train.value_counts().to_dict()}")
        logger.info(f"  X_val shape: {X_val.shape}")
        logger.info(f"  y_val dist: {y_val.value_counts().to_dict()}")
