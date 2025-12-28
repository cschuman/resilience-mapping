#!/usr/bin/env python3
"""
Corrected Resilience Model with State Fixed Effects

This module implements the OLS regression model for calculating resilience scores.
It ports the corrected Go implementation from app/backend/expected.go to Python.

BUG FIX (December 24, 2025):
    The original Go code had a critical bug where the inner loop variable 'i'
    shadowed the outer loop variable 'i', causing state fixed effects to be
    computed incorrectly. This Python implementation uses the corrected logic.

Model specification:
    burden ~ intercept + LILATracts_1And10 + low_income + rural + no_vehicle_far + State FE

Resilience score = -residual / std(residuals)
    Positive = doing better than expected (resilient)
    Negative = doing worse than expected (vulnerable)
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional, Dict, List
import statsmodels.api as sm
from dataclasses import dataclass


@dataclass
class OLSResult:
    """Results from OLS regression"""
    r_squared: float
    adj_r_squared: float
    coefficients: Dict[str, float]
    std_errors: Dict[str, float]
    n_observations: int
    n_states: int
    residual_std: float


def filter_institutional_populations(
    fara: pd.DataFrame,
    threshold: float = 0.10
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Filter out tracts with high institutional/group quarters populations.

    These include prisons, college dorms, military bases, etc. which have
    institutional food service rather than community-based food access.

    Args:
        fara: FARA dataset with tract-level food access data
        threshold: Maximum proportion of group quarters population (default 10%)

    Returns:
        Tuple of (filtered_fara, excluded_tracts)
    """
    # Check for GroupQuartersFlag or GroupQuarters column
    gq_cols = [col for col in fara.columns if 'group' in col.lower() or 'gq' in col.lower()]

    if 'GroupQuartersFlag' in fara.columns:
        gq_col = 'GroupQuartersFlag'
    elif 'GroupQuarters' in fara.columns:
        gq_col = 'GroupQuarters'
    elif 'GroupQuartersPop' in fara.columns and 'TotalPop' in fara.columns:
        # Calculate proportion if we have population data
        fara = fara.copy()
        fara['GQ_Proportion'] = fara['GroupQuartersPop'] / fara['TotalPop'].replace(0, np.nan)
        gq_col = 'GQ_Proportion'
    else:
        print(f"WARNING: No group quarters column found. Available columns with 'group': {gq_cols}")
        print("Returning unfiltered data. Manual review required.")
        return fara, pd.DataFrame()

    # Filter based on threshold
    if gq_col == 'GroupQuartersFlag':
        # Binary flag - exclude all flagged tracts
        excluded = fara[fara[gq_col] == 1]
        filtered = fara[fara[gq_col] != 1]
    else:
        # Proportion - use threshold
        excluded = fara[fara[gq_col] > threshold]
        filtered = fara[fara[gq_col] <= threshold]

    print(f"Institutional population filter applied:")
    print(f"  Threshold: {threshold * 100:.0f}%")
    print(f"  Excluded tracts: {len(excluded):,}")
    print(f"  Remaining tracts: {len(filtered):,}")

    return filtered, excluded


def prepare_design_matrix(
    burdened: pd.DataFrame,
    fara: pd.DataFrame,
    include_no_vehicle: bool = True,
    state_fixed_effects: bool = True
) -> Tuple[pd.DataFrame, pd.Series, List[str], List[str]]:
    """
    Prepare the design matrix X and response vector y for OLS.

    Args:
        burdened: DataFrame with TractFIPS, StateAbbr, burden columns
        fara: FARA DataFrame with food access variables
        include_no_vehicle: Whether to include LA1and10_NoVehicle variable
        state_fixed_effects: Whether to include state dummy variables

    Returns:
        Tuple of (X, y, feature_names, state_list)
    """
    # Standardize GEOID format
    burdened = burdened.copy()
    fara = fara.copy()

    # Handle different GEOID column names
    if 'GEOID' not in fara.columns and 'CensusTract' in fara.columns:
        fara['GEOID'] = fara['CensusTract'].astype(str).str.zfill(11)
    elif 'GEOID' in fara.columns:
        fara['GEOID'] = fara['GEOID'].astype(str).str.zfill(11)

    burdened['TractFIPS'] = burdened['TractFIPS'].astype(str).str.zfill(11)

    # Merge datasets
    merged = burdened.merge(fara, left_on='TractFIPS', right_on='GEOID', how='inner')

    # Get sorted list of states (drop first for reference category)
    state_list = sorted(merged['StateAbbr'].unique())

    # Build feature columns
    feature_names = ['intercept', 'LILATracts_1And10', 'LI', 'rural']

    # Convert LILA and LI to numeric
    merged['LILATracts_1And10'] = pd.to_numeric(merged['LILATracts_1And10'], errors='coerce').fillna(0)
    merged['LI'] = pd.to_numeric(merged['LI'], errors='coerce').fillna(0)

    # Create rural indicator (1 - Urban)
    merged['Urban'] = pd.to_numeric(merged['Urban'], errors='coerce').fillna(0)
    merged['rural'] = 1 - merged['Urban']

    # Build X matrix
    X = pd.DataFrame()
    X['intercept'] = 1
    X['LILATracts_1And10'] = merged['LILATracts_1And10'].values
    X['LI'] = merged['LI'].values
    X['rural'] = merged['rural'].values

    if include_no_vehicle:
        if 'LA1and10_NoVehicle' in merged.columns:
            merged['LA1and10_NoVehicle'] = pd.to_numeric(
                merged['LA1and10_NoVehicle'], errors='coerce'
            ).fillna(0)
            X['LA1and10_NoVehicle'] = merged['LA1and10_NoVehicle'].values
            feature_names.append('LA1and10_NoVehicle')
        else:
            print("WARNING: LA1and10_NoVehicle column not found in FARA data")

    # CORRECTED STATE FIXED EFFECTS
    # This is the critical fix - we create dummy variables correctly
    if state_fixed_effects:
        # Drop first state (reference category) to avoid perfect multicollinearity
        for state in state_list[1:]:
            col_name = f'state_{state}'
            # CORRECT: Compare each row's state to the current state in the loop
            X[col_name] = (merged['StateAbbr'] == state).astype(float)
            feature_names.append(col_name)

    # Response variable
    y = merged['burden'].values

    # Store tract info for output
    X['_TractFIPS'] = merged['TractFIPS'].values
    X['_StateAbbr'] = merged['StateAbbr'].values
    X['_GEOID'] = merged['GEOID'].values if 'GEOID' in merged.columns else merged['TractFIPS'].values

    print(f"Design matrix prepared:")
    print(f"  Observations: {len(X):,}")
    print(f"  Features: {len(feature_names)}")
    print(f"  States: {len(state_list)} (reference: {state_list[0]})")

    return X, pd.Series(y), feature_names, state_list


def fit_ols_model(
    X: pd.DataFrame,
    y: pd.Series,
    feature_names: List[str]
) -> Tuple[sm.regression.linear_model.RegressionResultsWrapper, np.ndarray]:
    """
    Fit OLS regression model.

    Args:
        X: Design matrix with features
        y: Response vector (burden)
        feature_names: List of feature names

    Returns:
        Tuple of (model_results, residuals)
    """
    # Extract feature columns only (exclude metadata columns starting with _)
    X_features = X[[col for col in X.columns if not col.startswith('_')]]

    # Fit model using statsmodels
    model = sm.OLS(y, X_features)
    results = model.fit()

    # Calculate residuals
    residuals = y - results.fittedvalues

    return results, residuals


def calculate_resilience_scores(
    X: pd.DataFrame,
    y: pd.Series,
    residuals: np.ndarray
) -> pd.DataFrame:
    """
    Calculate resilience scores from model residuals.

    Resilience score = -residual / std(residuals)

    Interpretation:
        - Positive score: tract is doing better than expected (resilient)
        - Negative score: tract is doing worse than expected (vulnerable)
        - Score > 1.645: statistically significant positive outlier (p < 0.05, one-tailed)

    Args:
        X: Design matrix (with metadata columns)
        y: Observed burden values
        residuals: Model residuals

    Returns:
        DataFrame with tract info and resilience scores
    """
    # Calculate z-scores
    residual_std = np.std(residuals)
    resilience_scores = -residuals / (residual_std + 1e-9)

    # Build output DataFrame
    output = pd.DataFrame({
        'TractFIPS': X['_TractFIPS'].values,
        'StateAbbr': X['_StateAbbr'].values,
        'GEOID': X['_GEOID'].values,
        'burden': y.values,
        'resid': residuals,
        'resilience_score': resilience_scores
    })

    # Classify tracts
    output['classification'] = pd.cut(
        output['resilience_score'],
        bins=[-np.inf, -1.645, 1.645, np.inf],
        labels=['vulnerable', 'expected', 'resilient']
    )

    return output


def expected_burden(
    burdened: pd.DataFrame,
    fara: pd.DataFrame,
    include_no_vehicle: bool = True,
    state_fixed_effects: bool = True,
    filter_institutional: bool = True,
    institutional_threshold: float = 0.10
) -> Tuple[pd.DataFrame, OLSResult]:
    """
    Main function to compute expected burden and resilience scores.

    This is the Python equivalent of ExpectedBurden in app/backend/expected.go,
    with the state fixed effects bug CORRECTED.

    Args:
        burdened: DataFrame with columns [TractFIPS, StateAbbr, burden]
        fara: FARA DataFrame with food access variables
        include_no_vehicle: Include LA1and10_NoVehicle variable
        state_fixed_effects: Include state dummy variables
        filter_institutional: Filter out high group quarters tracts
        institutional_threshold: Threshold for institutional population filter

    Returns:
        Tuple of (model_table, ols_result)
    """
    # Filter institutional populations if requested
    if filter_institutional:
        fara, excluded = filter_institutional_populations(fara, institutional_threshold)
        if len(excluded) > 0:
            excluded.to_csv('data/processed/excluded_institutional_tracts.csv', index=False)
            print(f"  Saved excluded tracts to data/processed/excluded_institutional_tracts.csv")

    # Prepare design matrix
    X, y, feature_names, state_list = prepare_design_matrix(
        burdened, fara, include_no_vehicle, state_fixed_effects
    )

    # Fit model
    results, residuals = fit_ols_model(X, y, feature_names)

    # Calculate resilience scores
    model_table = calculate_resilience_scores(X, y, residuals)

    # Build OLS result summary
    ols_result = OLSResult(
        r_squared=results.rsquared,
        adj_r_squared=results.rsquared_adj,
        coefficients={name: coef for name, coef in zip(feature_names, results.params)},
        std_errors={name: se for name, se in zip(feature_names, results.bse)},
        n_observations=len(y),
        n_states=len(state_list),
        residual_std=np.std(residuals)
    )

    # Print summary
    print(f"\nOLS Regression Results:")
    print(f"  R-squared: {ols_result.r_squared:.4f}")
    print(f"  Adjusted R-squared: {ols_result.adj_r_squared:.4f}")
    print(f"  N observations: {ols_result.n_observations:,}")
    print(f"  Residual std: {ols_result.residual_std:.4f}")

    print(f"\nCoefficients:")
    for name in ['intercept', 'LILATracts_1And10', 'LI', 'rural']:
        if name in ols_result.coefficients:
            coef = ols_result.coefficients[name]
            se = ols_result.std_errors[name]
            print(f"  {name}: {coef:.4f} (SE: {se:.4f})")

    # Resilience summary
    resilient_count = (model_table['resilience_score'] > 1.645).sum()
    vulnerable_count = (model_table['resilience_score'] < -1.645).sum()

    print(f"\nResilience Classification:")
    print(f"  Resilient (score > 1.645): {resilient_count:,} tracts")
    print(f"  Vulnerable (score < -1.645): {vulnerable_count:,} tracts")
    print(f"  Expected: {len(model_table) - resilient_count - vulnerable_count:,} tracts")

    return model_table, ols_result


def run_model_on_data(
    places_path: str = 'data/raw/places_tract.csv',
    fara_path: str = 'data/interim/fara_2019.csv',
    output_path: str = 'data/processed/model_table_corrected.csv'
) -> Tuple[pd.DataFrame, OLSResult]:
    """
    Run the complete model pipeline on data files.

    Args:
        places_path: Path to PLACES data
        fara_path: Path to FARA data
        output_path: Path for output CSV

    Returns:
        Tuple of (model_table, ols_result)
    """
    print("=" * 60)
    print("CORRECTED RESILIENCE MODEL")
    print("State Fixed Effects Bug Fix Applied")
    print("=" * 60)

    # Load data
    print("\nLoading data...")

    try:
        places = pd.read_csv(places_path)
        print(f"  PLACES data: {len(places):,} records")
    except FileNotFoundError:
        print(f"  ERROR: Could not find {places_path}")
        return None, None

    try:
        fara = pd.read_csv(fara_path)
        print(f"  FARA data: {len(fara):,} tracts")
    except FileNotFoundError:
        print(f"  ERROR: Could not find {fara_path}")
        return None, None

    # Calculate burden from PLACES
    print("\nCalculating health burden...")
    burdened = calculate_burden_from_places(places)
    print(f"  Burden calculated for {len(burdened):,} tracts")

    # Run model
    model_table, ols_result = expected_burden(burdened, fara)

    # Save results
    model_table.to_csv(output_path, index=False)
    print(f"\nSaved: {output_path}")

    return model_table, ols_result


def calculate_burden_from_places(places: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate composite health burden from PLACES outcomes.

    Uses z-score averaging of key health outcomes:
    - OBESITY: Obesity among adults
    - DIABETES: Diabetes among adults
    - CHD: Coronary heart disease among adults
    - BPHIGH: High blood pressure among adults
    - LPA: Lack of physical activity among adults

    Args:
        places: PLACES DataFrame in long format

    Returns:
        DataFrame with TractFIPS, StateAbbr, burden
    """
    target_outcomes = ['OBESITY', 'DIABETES', 'CHD', 'BPHIGH', 'LPA']

    # Filter to target outcomes
    places_filtered = places[places['MeasureId'].isin(target_outcomes)].copy()

    # Pivot to wide format
    places_wide = places_filtered.pivot_table(
        index=['LocationID', 'StateAbbr'],
        columns='MeasureId',
        values='Data_Value',
        aggfunc='mean'
    ).reset_index()

    # Z-score normalize each outcome
    from sklearn.preprocessing import StandardScaler

    available_outcomes = [col for col in target_outcomes if col in places_wide.columns]
    scaler = StandardScaler()
    z_scores = scaler.fit_transform(places_wide[available_outcomes].fillna(0))

    # Calculate mean burden
    places_wide['burden'] = z_scores.mean(axis=1)

    # Rename for output
    places_wide = places_wide.rename(columns={'LocationID': 'TractFIPS'})

    return places_wide[['TractFIPS', 'StateAbbr', 'burden']]


if __name__ == "__main__":
    import sys

    # Allow custom paths from command line
    places_path = sys.argv[1] if len(sys.argv) > 1 else 'data/raw/places_tract.csv'
    fara_path = sys.argv[2] if len(sys.argv) > 2 else 'data/interim/fara_2019.csv'
    output_path = sys.argv[3] if len(sys.argv) > 3 else 'data/processed/model_table_corrected.csv'

    model_table, ols_result = run_model_on_data(places_path, fara_path, output_path)

    if model_table is not None:
        print("\n" + "=" * 60)
        print("TOP 20 RESILIENT TRACTS (CORRECTED)")
        print("=" * 60)
        top_20 = model_table.nlargest(20, 'resilience_score')
        print(top_20[['TractFIPS', 'StateAbbr', 'burden', 'resilience_score']].to_string())
