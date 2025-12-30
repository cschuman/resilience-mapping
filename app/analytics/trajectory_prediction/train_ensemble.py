#!/usr/bin/env python3
"""
Ensemble Model Training for Community Health Trajectory Prediction
===================================================================

Combines XGBoost and LightGBM using soft voting to improve robustness
and prediction quality.

Author: Ensemble model pipeline
Date: 2025-12-30
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import (
    balanced_accuracy_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
import xgboost as xgb
import lightgbm as lgb
import matplotlib.pyplot as plt
import seaborn as sns

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models" / "trajectory_prediction"
RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = PROJECT_ROOT / "figures" / "trajectory"

for d in [MODELS_DIR, RESULTS_DIR, FIGURES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42

# XGBoost parameters
XGBOOST_PARAMS = {
    'n_estimators': 500,
    'max_depth': 6,
    'learning_rate': 0.05,
    'min_child_weight': 5,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'objective': 'multi:softprob',
    'num_class': 3,
    'eval_metric': 'mlogloss',
    'random_state': RANDOM_SEED,
    'tree_method': 'hist',
}

# LightGBM parameters
LIGHTGBM_PARAMS = {
    'n_estimators': 500,
    'max_depth': 6,
    'learning_rate': 0.05,
    'min_child_samples': 20,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'objective': 'multiclass',
    'num_class': 3,
    'metric': 'multi_logloss',
    'random_state': RANDOM_SEED,
    'verbosity': -1,
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def load_data(data_path: Path) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray, List[str]]:
    """Load and prepare data for training."""
    logger.info(f"Loading data from: {data_path}")
    df = pd.read_csv(data_path)
    logger.info(f"Loaded {len(df):,} records with {len(df.columns)} columns")

    # Exclude non-feature columns
    exclude_cols = ['TractFIPS', 'PredictionYear', 'StateAbbr', 'CountyFIPS',
                    'target_change', 'target_class']
    feature_cols = [c for c in df.columns if c not in exclude_cols]

    # Handle missing values
    for col in feature_cols:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())

    X = df[feature_cols].values
    feature_names = feature_cols

    # Encode target
    le = LabelEncoder()
    y = le.fit_transform(df['target_class'])
    class_names = list(le.classes_)

    logger.info(f"Features: {len(feature_names)}")
    logger.info(f"Classes: {class_names}")
    logger.info(f"Class distribution: {np.bincount(y).tolist()}")

    return df, X, y, feature_names


def train_xgboost(X_train, y_train, X_val, y_val, weights=None):
    """Train XGBoost model."""
    logger.info("Training XGBoost...")
    model = xgb.XGBClassifier(**XGBOOST_PARAMS, early_stopping_rounds=50)
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        sample_weight=weights,
        verbose=False
    )
    logger.info(f"XGBoost best iteration: {model.best_iteration}")
    return model


def train_lightgbm(X_train, y_train, X_val, y_val, weights=None):
    """Train LightGBM model."""
    logger.info("Training LightGBM...")
    model = lgb.LGBMClassifier(**LIGHTGBM_PARAMS)

    callbacks = [lgb.early_stopping(stopping_rounds=50, verbose=False)]

    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        sample_weight=weights,
        callbacks=callbacks
    )
    logger.info(f"LightGBM best iteration: {model.best_iteration_}")
    return model


def ensemble_predict_proba(models: List, X: np.ndarray, weights: List[float] = None):
    """Soft voting ensemble prediction."""
    if weights is None:
        weights = [1.0 / len(models)] * len(models)

    probas = np.zeros((X.shape[0], 3))
    for model, weight in zip(models, weights):
        probas += weight * model.predict_proba(X)

    return probas


def evaluate_model(y_true, y_pred, y_proba, name="Model"):
    """Evaluate model performance."""
    metrics = {
        'balanced_accuracy': balanced_accuracy_score(y_true, y_pred),
        'f1_macro': f1_score(y_true, y_pred, average='macro'),
        'f1_weighted': f1_score(y_true, y_pred, average='weighted'),
        'roc_auc': roc_auc_score(y_true, y_proba, multi_class='ovr'),
    }

    logger.info(f"\n{name} Performance:")
    logger.info(f"  Balanced Accuracy: {metrics['balanced_accuracy']:.4f}")
    logger.info(f"  F1 (macro):        {metrics['f1_macro']:.4f}")
    logger.info(f"  F1 (weighted):     {metrics['f1_weighted']:.4f}")
    logger.info(f"  ROC AUC:           {metrics['roc_auc']:.4f}")

    return metrics


def save_models(xgb_model, lgb_model, scaler, feature_names, class_names, weights, timestamp):
    """Save models using native formats (no pickle)."""
    # Save XGBoost model (native JSON format via booster)
    xgb_path = MODELS_DIR / f"xgboost_{timestamp}.json"
    xgb_model.get_booster().save_model(str(xgb_path))
    logger.info(f"Saved XGBoost model to: {xgb_path}")

    # Save LightGBM model (native text format)
    lgb_path = MODELS_DIR / f"lightgbm_{timestamp}.txt"
    lgb_model.booster_.save_model(str(lgb_path))
    logger.info(f"Saved LightGBM model to: {lgb_path}")

    # Save scaler parameters as JSON
    scaler_params = {
        'mean': scaler.mean_.tolist(),
        'scale': scaler.scale_.tolist(),
        'var': scaler.var_.tolist(),
    }
    scaler_path = MODELS_DIR / f"scaler_{timestamp}.json"
    with open(scaler_path, 'w') as f:
        json.dump(scaler_params, f, indent=2)
    logger.info(f"Saved scaler to: {scaler_path}")

    # Save ensemble metadata
    metadata = {
        'timestamp': timestamp,
        'feature_names': feature_names,
        'class_names': class_names,
        'ensemble_weights': weights,
        'xgboost_path': xgb_path.name,
        'lightgbm_path': lgb_path.name,
        'scaler_path': scaler_path.name,
    }
    metadata_path = MODELS_DIR / f"ensemble_metadata_{timestamp}.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"Saved metadata to: {metadata_path}")

    # Save latest reference
    latest_metadata = MODELS_DIR / "ensemble_latest.json"
    with open(latest_metadata, 'w') as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"Saved latest reference to: {latest_metadata}")


def main():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    logger.info("=" * 70)
    logger.info("ENSEMBLE MODEL TRAINING")
    logger.info("=" * 70)

    # Load data
    data_path = PROCESSED_DATA_DIR / "prediction_dataset_spatial.csv"
    df, X, y, feature_names = load_data(data_path)

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Temporal split: train on years < 2024, validate on 2024
    train_mask = df['PredictionYear'] < 2024
    val_mask = df['PredictionYear'] == 2024

    X_train = X_scaled[train_mask]
    y_train = y[train_mask]
    X_val = X_scaled[val_mask]
    y_val = y[val_mask]

    logger.info(f"Training samples: {len(y_train):,}")
    logger.info(f"Validation samples: {len(y_val):,}")

    # Compute sample weights for class imbalance
    class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
    sample_weights = np.array([class_weights[label] for label in y_train])

    # Train individual models
    logger.info("\n" + "=" * 70)
    logger.info("TRAINING INDIVIDUAL MODELS")
    logger.info("=" * 70)

    xgb_model = train_xgboost(X_train, y_train, X_val, y_val, sample_weights)
    lgb_model = train_lightgbm(X_train, y_train, X_val, y_val, sample_weights)

    # Evaluate individual models
    logger.info("\n" + "=" * 70)
    logger.info("INDIVIDUAL MODEL PERFORMANCE (Validation Set)")
    logger.info("=" * 70)

    xgb_pred = xgb_model.predict(X_val)
    xgb_proba = xgb_model.predict_proba(X_val)
    xgb_metrics = evaluate_model(y_val, xgb_pred, xgb_proba, "XGBoost")

    lgb_pred = lgb_model.predict(X_val)
    lgb_proba = lgb_model.predict_proba(X_val)
    lgb_metrics = evaluate_model(y_val, lgb_pred, lgb_proba, "LightGBM")

    # Create ensemble
    logger.info("\n" + "=" * 70)
    logger.info("ENSEMBLE MODEL PERFORMANCE")
    logger.info("=" * 70)

    # Equal weight ensemble
    models = [xgb_model, lgb_model]
    ensemble_proba = ensemble_predict_proba(models, X_val)
    ensemble_pred = np.argmax(ensemble_proba, axis=1)
    ensemble_metrics = evaluate_model(y_val, ensemble_pred, ensemble_proba, "Ensemble (50/50)")

    # Optimized weights based on individual F1 scores
    total_f1 = xgb_metrics['f1_macro'] + lgb_metrics['f1_macro']
    opt_weights = [
        xgb_metrics['f1_macro'] / total_f1,
        lgb_metrics['f1_macro'] / total_f1
    ]
    opt_ensemble_proba = ensemble_predict_proba(models, X_val, opt_weights)
    opt_ensemble_pred = np.argmax(opt_ensemble_proba, axis=1)
    opt_metrics = evaluate_model(y_val, opt_ensemble_pred, opt_ensemble_proba,
                                  f"Ensemble ({opt_weights[0]:.2f}/{opt_weights[1]:.2f})")

    # Classification report for best ensemble
    best_weights = opt_weights if opt_metrics['f1_macro'] > ensemble_metrics['f1_macro'] else [0.5, 0.5]
    best_proba = ensemble_predict_proba(models, X_val, best_weights)
    best_pred = np.argmax(best_proba, axis=1)

    class_names = ['DECLINE', 'IMPROVE', 'STABLE']
    logger.info("\nBest Ensemble Classification Report:")
    report = classification_report(y_val, best_pred, target_names=class_names)
    logger.info(f"\n{report}")

    # Confusion matrix
    cm = confusion_matrix(y_val, best_pred)
    logger.info(f"\nConfusion Matrix:\n{cm}")

    # Train final models on training data (not all data, to avoid data leakage)
    logger.info("\n" + "=" * 70)
    logger.info("TRAINING FINAL MODELS")
    logger.info("=" * 70)

    # Use the training data with validation for early stopping
    final_xgb = train_xgboost(X_train, y_train, X_val, y_val, sample_weights)
    final_lgb = train_lightgbm(X_train, y_train, X_val, y_val, sample_weights)

    # Final ensemble evaluation on validation set
    final_models = [final_xgb, final_lgb]
    final_proba = ensemble_predict_proba(final_models, X_val, best_weights)
    final_pred = np.argmax(final_proba, axis=1)
    final_metrics = evaluate_model(y_val, final_pred, final_proba, "Final Ensemble (Validation)")

    logger.info(f"\nFinal Ensemble Classification Report:")
    report = classification_report(y_val, final_pred, target_names=class_names)
    logger.info(f"\n{report}")

    # Save models using native formats
    save_models(final_xgb, final_lgb, scaler, feature_names, class_names, best_weights, timestamp)

    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Ensemble Model Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    cm_path = FIGURES_DIR / f"ensemble_confusion_matrix_{timestamp}.png"
    plt.savefig(cm_path, dpi=150)
    plt.close()
    logger.info(f"Saved confusion matrix to: {cm_path}")

    # Feature importance (averaged from both models)
    xgb_importance = final_xgb.feature_importances_
    lgb_importance = final_lgb.feature_importances_
    avg_importance = (xgb_importance + lgb_importance) / 2

    importance_df = pd.DataFrame({
        'feature': feature_names,
        'xgb_importance': xgb_importance,
        'lgb_importance': lgb_importance,
        'avg_importance': avg_importance
    }).sort_values('avg_importance', ascending=False)

    importance_path = RESULTS_DIR / f"ensemble_feature_importance_{timestamp}.csv"
    importance_df.to_csv(importance_path, index=False)
    logger.info(f"Saved feature importance to: {importance_path}")

    # Plot feature importance
    plt.figure(figsize=(10, 8))
    top_n = 20
    top_features = importance_df.head(top_n)
    plt.barh(range(top_n), top_features['avg_importance'].values[::-1])
    plt.yticks(range(top_n), top_features['feature'].values[::-1])
    plt.xlabel('Average Importance')
    plt.title(f'Top {top_n} Features (Ensemble Average)')
    plt.tight_layout()
    fi_path = FIGURES_DIR / f"ensemble_feature_importance_{timestamp}.png"
    plt.savefig(fi_path, dpi=150)
    plt.close()
    logger.info(f"Saved feature importance plot to: {fi_path}")

    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("TRAINING SUMMARY")
    logger.info("=" * 70)
    logger.info(f"Dataset: {data_path}")
    logger.info(f"Total samples: {len(y):,}")
    logger.info(f"Features: {len(feature_names)}")
    logger.info(f"Ensemble weights: XGBoost={best_weights[0]:.2f}, LightGBM={best_weights[1]:.2f}")
    logger.info("")
    logger.info("Validation Performance (2024 holdout):")
    logger.info(f"  XGBoost:   F1={xgb_metrics['f1_macro']:.4f}, Acc={xgb_metrics['balanced_accuracy']:.4f}")
    logger.info(f"  LightGBM:  F1={lgb_metrics['f1_macro']:.4f}, Acc={lgb_metrics['balanced_accuracy']:.4f}")
    logger.info(f"  Ensemble:  F1={opt_metrics['f1_macro']:.4f}, Acc={opt_metrics['balanced_accuracy']:.4f}")
    logger.info("")
    logger.info("Top 5 Features:")
    for _, row in importance_df.head(5).iterrows():
        logger.info(f"  {row['feature']}: {row['avg_importance']:.4f}")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
