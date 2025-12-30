#!/usr/bin/env python3
"""
Generate Trajectory Predictions for All Tracts

Loads the trained ensemble model and generates predictions for all tracts
to be stored in the database for fast API access.

Output: CSV file with tract_fips, predicted_class, and probabilities
"""

import json
import logging
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import xgboost as xgb
import lightgbm as lgb
from sklearn.preprocessing import StandardScaler

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models" / "trajectory_prediction"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def load_ensemble_model():
    """Load the trained ensemble model from native formats."""
    # Load metadata
    metadata_path = MODELS_DIR / "ensemble_latest.json"
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    logger.info(f"Loading ensemble from {metadata['timestamp']}")

    # Load XGBoost
    xgb_path = MODELS_DIR / metadata['xgboost_path']
    xgb_model = xgb.Booster()
    xgb_model.load_model(str(xgb_path))
    logger.info(f"Loaded XGBoost from {xgb_path}")

    # Load LightGBM
    lgb_path = MODELS_DIR / metadata['lightgbm_path']
    lgb_model = lgb.Booster(model_file=str(lgb_path))
    logger.info(f"Loaded LightGBM from {lgb_path}")

    # Load scaler
    scaler_path = MODELS_DIR / metadata['scaler_path']
    with open(scaler_path, 'r') as f:
        scaler_params = json.load(f)

    scaler = StandardScaler()
    scaler.mean_ = np.array(scaler_params['mean'])
    scaler.scale_ = np.array(scaler_params['scale'])
    scaler.var_ = np.array(scaler_params['var'])

    return {
        'xgboost': xgb_model,
        'lightgbm': lgb_model,
        'scaler': scaler,
        'weights': metadata['ensemble_weights'],
        'feature_names': metadata['feature_names'],
        'class_names': metadata['class_names'],
    }


def ensemble_predict(model_data, X):
    """Generate ensemble predictions."""
    # Scale features
    X_scaled = model_data['scaler'].transform(X)

    # XGBoost predictions
    dmatrix = xgb.DMatrix(X_scaled)
    xgb_proba = model_data['xgboost'].predict(dmatrix)

    # LightGBM predictions
    lgb_proba = model_data['lightgbm'].predict(X_scaled)

    # Weighted ensemble
    weights = model_data['weights']
    ensemble_proba = weights[0] * xgb_proba + weights[1] * lgb_proba

    # Get predictions
    predictions = np.argmax(ensemble_proba, axis=1)
    class_names = model_data['class_names']
    predicted_classes = [class_names[p] for p in predictions]

    return predicted_classes, ensemble_proba


def main():
    logger.info("=" * 70)
    logger.info("GENERATING TRAJECTORY PREDICTIONS")
    logger.info("=" * 70)

    # Load model
    model_data = load_ensemble_model()

    # Load the latest prediction dataset (use 2024 data as "current")
    data_path = PROCESSED_DATA_DIR / "prediction_dataset_spatial.csv"
    df = pd.read_csv(data_path)

    # Filter to most recent prediction year (2024)
    df_current = df[df['PredictionYear'] == 2024].copy()
    logger.info(f"Generating predictions for {len(df_current):,} tracts (2024 data)")

    # Prepare features
    exclude_cols = ['TractFIPS', 'PredictionYear', 'StateAbbr', 'CountyFIPS',
                    'target_change', 'target_class']
    feature_cols = [c for c in df.columns if c not in exclude_cols]

    # Handle missing values
    for col in feature_cols:
        if df_current[col].isna().any():
            df_current[col] = df_current[col].fillna(df_current[col].median())

    X = df_current[feature_cols].values

    # Generate predictions
    logger.info("Generating ensemble predictions...")
    predicted_classes, probabilities = ensemble_predict(model_data, X)

    # Create output dataframe
    output = pd.DataFrame({
        'tract_fips': df_current['TractFIPS'].values,
        'state_abbr': df_current['StateAbbr'].values,
        'predicted_trajectory': predicted_classes,
        'prob_decline': probabilities[:, 0],
        'prob_improve': probabilities[:, 1],
        'prob_stable': probabilities[:, 2],
        'confidence': probabilities.max(axis=1),
    })

    # Add prediction metadata
    output['prediction_date'] = datetime.now().strftime('%Y-%m-%d')
    output['model_version'] = 'ensemble_v1'

    # Save to CSV
    output_path = PROCESSED_DATA_DIR / "tract_predictions.csv"
    output.to_csv(output_path, index=False)
    logger.info(f"Saved predictions to {output_path}")

    # Summary statistics
    logger.info("\n" + "=" * 70)
    logger.info("PREDICTION SUMMARY")
    logger.info("=" * 70)

    trajectory_counts = output['predicted_trajectory'].value_counts()
    logger.info(f"\nTrajectory Distribution:")
    for traj, count in trajectory_counts.items():
        pct = 100 * count / len(output)
        logger.info(f"  {traj}: {count:,} ({pct:.1f}%)")

    logger.info(f"\nConfidence Statistics:")
    logger.info(f"  Mean: {output['confidence'].mean():.3f}")
    logger.info(f"  Median: {output['confidence'].median():.3f}")
    logger.info(f"  Min: {output['confidence'].min():.3f}")
    logger.info(f"  Max: {output['confidence'].max():.3f}")

    # High confidence predictions
    high_conf = output[output['confidence'] >= 0.6]
    logger.info(f"\nHigh Confidence Predictions (>=60%): {len(high_conf):,} ({100*len(high_conf)/len(output):.1f}%)")

    logger.info("\n" + "=" * 70)
    logger.info("DONE")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
