#!/usr/bin/env python3
"""
Community Health Trajectory Prediction - Training Pipeline
==========================================================

Production-ready training script for 3-class trajectory prediction.
Implements proper temporal cross-validation, handles class imbalance,
and generates comprehensive evaluation metrics.

Author: Dr. Sarah Kim
Date: 2025-12-30
"""

import sys
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import warnings

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    balanced_accuracy_score,
    f1_score,
    cohen_kappa_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    log_loss,
)
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns

# Import config
try:
    from config import (
        PROCESSED_DATA_DIR,
        MODELS_DIR,
        RESULTS_DIR,
        FIGURES_DIR,
        XGBOOST_PARAMS,
        CV_CONFIG,
        TRAJECTORY_LABELS,
        RANDOM_SEED,
    )
except ImportError:
    # Fallback if config import fails
    PROCESSED_DATA_DIR = Path("../../../data/processed")
    MODELS_DIR = Path("../../../models/trajectory_prediction")
    RESULTS_DIR = Path("../../../results")
    FIGURES_DIR = Path("../../../figures/trajectory")
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
        'random_state': 42,
        'tree_method': 'hist',
    }
    CV_CONFIG = {
        # 2025 data is identical to 2024 (not yet updated), so exclude
        'validation_years': [2023, 2024],
        'expanding_window': True,
    }
    TRAJECTORY_LABELS = {'DECLINE': 0, 'STABLE': 1, 'IMPROVE': 2}
    RANDOM_SEED = 42

warnings.filterwarnings('ignore', category=FutureWarning)
np.random.seed(RANDOM_SEED)


# =============================================================================
# LOGGING SETUP
# =============================================================================

def setup_logging(log_file: Optional[Path] = None) -> logging.Logger:
    """Configure logging with both file and console handlers."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setLevel(logging.INFO)
        file_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger


# =============================================================================
# DATA LOADING AND PREPROCESSING
# =============================================================================

def load_prediction_dataset(data_path: Path, logger: logging.Logger) -> pd.DataFrame:
    """Load and perform initial validation of prediction dataset."""
    logger.info(f"Loading data from: {data_path}")

    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found: {data_path}")

    df = pd.read_csv(data_path)
    logger.info(f"Loaded {len(df):,} records")
    logger.info(f"Columns: {list(df.columns)}")

    # Validate required columns
    required_cols = ['TractFIPS', 'PredictionYear', 'target_class']
    missing_cols = set(required_cols) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Check for missing values
    missing_summary = df.isnull().sum()
    if missing_summary.sum() > 0:
        logger.warning("Missing values detected:")
        for col, count in missing_summary[missing_summary > 0].items():
            logger.warning(f"  {col}: {count} ({count/len(df)*100:.2f}%)")

    return df


def prepare_features_and_targets(
    df: pd.DataFrame,
    logger: logging.Logger
) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
    """
    Prepare feature matrix and target variable.

    Returns:
        X: Feature matrix
        y: Target labels (encoded as integers)
        feature_names: List of feature column names
    """
    logger.info("Preparing features and targets...")

    # Identify feature columns (exclude metadata and target)
    metadata_cols = ['TractFIPS', 'PredictionYear', 'StateAbbr', 'CountyFIPS',
                     'target_change', 'target_class']
    feature_cols = [col for col in df.columns if col not in metadata_cols]

    X = df[feature_cols].copy()

    # Handle missing values (simple imputation with median)
    if X.isnull().any().any():
        logger.info("Imputing missing values with median...")
        X = X.fillna(X.median())

    # Encode target labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df['target_class'])

    logger.info(f"Features: {len(feature_cols)} columns")
    logger.info(f"Feature names: {feature_cols}")
    logger.info(f"Target classes: {label_encoder.classes_}")
    logger.info(f"Target distribution:\n{pd.Series(y).value_counts().sort_index()}")

    return X, pd.Series(y), feature_cols


# =============================================================================
# TEMPORAL CROSS-VALIDATION
# =============================================================================

def create_temporal_cv_splits(
    df: pd.DataFrame,
    validation_years: List[int],
    expanding_window: bool = True,
    logger: Optional[logging.Logger] = None
) -> List[Tuple[np.ndarray, np.ndarray]]:
    """
    Create temporal cross-validation splits.

    CRITICAL: This ensures no data leakage by only using past data
    to predict future trajectories.

    Args:
        df: DataFrame with 'PredictionYear' column
        validation_years: List of years to validate on
        expanding_window: If True, training set grows over time

    Returns:
        List of (train_idx, val_idx) tuples
    """
    if logger:
        logger.info("Creating temporal CV splits...")
        logger.info(f"Validation years: {validation_years}")
        logger.info(f"Expanding window: {expanding_window}")

    splits = []
    all_years = sorted(df['PredictionYear'].unique())

    for val_year in validation_years:
        # Validation set: current year
        val_idx = df[df['PredictionYear'] == val_year].index.to_numpy()

        # Training set: all years before validation year
        if expanding_window:
            train_idx = df[df['PredictionYear'] < val_year].index.to_numpy()
        else:
            # Rolling window: use only previous year
            train_idx = df[df['PredictionYear'] == val_year - 1].index.to_numpy()

        if len(train_idx) > 0 and len(val_idx) > 0:
            splits.append((train_idx, val_idx))

            if logger:
                train_years = df.iloc[train_idx]['PredictionYear'].unique()
                logger.info(f"  Split {len(splits)}: Train on {sorted(train_years)} → "
                           f"Validate on {val_year} "
                           f"(n_train={len(train_idx)}, n_val={len(val_idx)})")

    return splits


# =============================================================================
# MODEL TRAINING
# =============================================================================

def compute_sample_weights(y: np.ndarray, method: str = 'balanced') -> np.ndarray:
    """
    Compute sample weights to handle class imbalance.

    Args:
        y: Target labels
        method: 'balanced' for inverse frequency weighting

    Returns:
        Array of sample weights
    """
    class_weights = compute_class_weight(
        class_weight=method,
        classes=np.unique(y),
        y=y
    )

    # Map class weights to samples
    sample_weights = np.array([class_weights[label] for label in y])

    return sample_weights


def train_xgboost_model(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    params: Dict,
    logger: logging.Logger,
    use_sample_weights: bool = True
) -> xgb.XGBClassifier:
    """
    Train XGBoost classifier with early stopping.

    Args:
        X_train, y_train: Training data
        X_val, y_val: Validation data for early stopping
        params: XGBoost hyperparameters
        use_sample_weights: Whether to apply class weights

    Returns:
        Trained XGBoost model
    """
    logger.info("Training XGBoost model...")

    # Compute sample weights if requested
    sample_weights = None
    if use_sample_weights:
        sample_weights = compute_sample_weights(y_train)
        logger.info("Applied balanced class weights")

    # Initialize model with early stopping
    model = xgb.XGBClassifier(**params, early_stopping_rounds=50)

    # Train with early stopping
    model.fit(
        X_train,
        y_train,
        sample_weight=sample_weights,
        eval_set=[(X_val, y_val)],
        verbose=False
    )

    # Get best iteration if early stopping was triggered
    try:
        best_iteration = model.best_iteration
        best_score = model.best_score
        logger.info(f"Best iteration: {best_iteration}, Best score: {best_score:.4f}")
    except AttributeError:
        logger.info(f"Training completed without early stopping")

    return model


# =============================================================================
# MODEL EVALUATION
# =============================================================================

def evaluate_model(
    model: xgb.XGBClassifier,
    X: np.ndarray,
    y_true: np.ndarray,
    class_names: List[str],
    logger: logging.Logger
) -> Dict[str, float]:
    """
    Comprehensive model evaluation.

    Returns:
        Dictionary of evaluation metrics
    """
    # Predictions
    y_pred = model.predict(X)
    y_pred_proba = model.predict_proba(X)

    # Compute metrics
    metrics = {}

    # Balanced accuracy (accounts for class imbalance)
    metrics['balanced_accuracy'] = balanced_accuracy_score(y_true, y_pred)

    # F1 scores
    metrics['f1_macro'] = f1_score(y_true, y_pred, average='macro', zero_division=0)
    metrics['f1_weighted'] = f1_score(y_true, y_pred, average='weighted', zero_division=0)

    # Per-class F1 scores (handle missing classes)
    f1_per_class = f1_score(y_true, y_pred, average=None, labels=[0, 1, 2], zero_division=0)
    for idx, class_name in enumerate(class_names):
        metrics[f'f1_{class_name.lower()}'] = f1_per_class[idx]

    # Cohen's kappa
    metrics['cohen_kappa'] = cohen_kappa_score(y_true, y_pred)

    # ROC AUC (one-vs-rest for multiclass)
    try:
        metrics['roc_auc_ovr'] = roc_auc_score(
            y_true, y_pred_proba, multi_class='ovr', average='weighted'
        )
    except Exception as e:
        logger.warning(f"Could not compute ROC AUC: {e}")
        metrics['roc_auc_ovr'] = np.nan

    # Log loss (with labels to handle missing classes)
    try:
        metrics['log_loss'] = log_loss(
            y_true, y_pred_proba, labels=[0, 1, 2]
        )
    except Exception as e:
        logger.warning(f"Could not compute log loss: {e}")
        metrics['log_loss'] = np.nan

    # Log metrics
    logger.info("Evaluation metrics:")
    logger.info(f"  Balanced Accuracy: {metrics['balanced_accuracy']:.4f}")
    logger.info(f"  F1 (macro):        {metrics['f1_macro']:.4f}")
    logger.info(f"  F1 (weighted):     {metrics['f1_weighted']:.4f}")
    logger.info(f"  Cohen's Kappa:     {metrics['cohen_kappa']:.4f}")
    logger.info(f"  ROC AUC (OvR):     {metrics['roc_auc_ovr']:.4f}")
    logger.info(f"  Log Loss:          {metrics['log_loss']:.4f}")

    # Per-class F1
    logger.info("Per-class F1 scores:")
    for class_name in class_names:
        f1 = metrics[f'f1_{class_name.lower()}']
        logger.info(f"  {class_name}: {f1:.4f}")

    # Classification report
    logger.info("\nClassification Report:")
    report = classification_report(
        y_true, y_pred, target_names=class_names, labels=[0, 1, 2], zero_division=0
    )
    logger.info("\n" + report)

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    logger.info("\nConfusion Matrix:")
    logger.info(f"\n{cm}")

    return metrics, cm


def plot_confusion_matrix(
    cm: np.ndarray,
    class_names: List[str],
    save_path: Path,
    title: str = "Confusion Matrix"
) -> None:
    """Plot and save confusion matrix."""
    plt.figure(figsize=(10, 8))

    # Normalize confusion matrix
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    # Plot
    sns.heatmap(
        cm_normalized,
        annot=True,
        fmt='.2%',
        cmap='Blues',
        xticklabels=class_names,
        yticklabels=class_names,
        cbar_kws={'label': 'Proportion'}
    )

    plt.title(title, fontsize=16, pad=20)
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.tight_layout()

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_feature_importance(
    model: xgb.XGBClassifier,
    feature_names: List[str],
    save_path: Path,
    top_n: int = 20
) -> pd.DataFrame:
    """Plot and return feature importance."""
    # Get feature importance
    importance = model.feature_importances_

    # Create DataFrame
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importance
    }).sort_values('importance', ascending=False)

    # Plot top N features
    top_features = importance_df.head(top_n)

    plt.figure(figsize=(12, 8))
    plt.barh(range(len(top_features)), top_features['importance'])
    plt.yticks(range(len(top_features)), top_features['feature'])
    plt.xlabel('Importance', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.title(f'Top {top_n} Most Important Features', fontsize=16, pad=20)
    plt.gca().invert_yaxis()
    plt.tight_layout()

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

    return importance_df


# =============================================================================
# MAIN TRAINING PIPELINE
# =============================================================================

def main():
    """Main training pipeline."""

    # Setup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = RESULTS_DIR / f"training_log_{timestamp}.txt"
    logger = setup_logging(log_file)

    logger.info("=" * 80)
    logger.info("COMMUNITY HEALTH TRAJECTORY PREDICTION - TRAINING PIPELINE")
    logger.info("=" * 80)
    logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Random seed: {RANDOM_SEED}")

    # Create output directories
    for directory in [MODELS_DIR, RESULTS_DIR, FIGURES_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory: {directory}")

    # Load data (use rich feature set)
    data_path = PROCESSED_DATA_DIR / "prediction_dataset_rich.csv"
    df = load_prediction_dataset(data_path, logger)

    # Prepare features and targets
    X, y, feature_names = prepare_features_and_targets(df, logger)

    # Get class names (must match LabelEncoder alphabetical order)
    class_names = ['DECLINE', 'IMPROVE', 'STABLE']

    # Create temporal CV splits
    cv_splits = create_temporal_cv_splits(
        df,
        validation_years=CV_CONFIG['validation_years'],
        expanding_window=CV_CONFIG['expanding_window'],
        logger=logger
    )

    logger.info(f"\nCreated {len(cv_splits)} temporal CV splits")

    # Cross-validation results storage
    cv_results = []
    cv_confusion_matrices = []
    trained_models = []

    # Train and evaluate on each split
    logger.info("\n" + "=" * 80)
    logger.info("TEMPORAL CROSS-VALIDATION")
    logger.info("=" * 80)

    for split_idx, (train_idx, val_idx) in enumerate(cv_splits, 1):
        logger.info(f"\n{'=' * 80}")
        logger.info(f"FOLD {split_idx}/{len(cv_splits)}")
        logger.info(f"{'=' * 80}")

        # Split data
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        # Log split info
        train_year = df.iloc[train_idx]['PredictionYear'].unique()
        val_year = df.iloc[val_idx]['PredictionYear'].unique()
        logger.info(f"Training years: {sorted(train_year)}")
        logger.info(f"Validation year: {val_year[0]}")
        logger.info(f"Training samples: {len(X_train)}")
        logger.info(f"Validation samples: {len(X_val)}")

        # Feature scaling (fit on train, transform both)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)

        # Train model
        model = train_xgboost_model(
            X_train_scaled,
            y_train.values,
            X_val_scaled,
            y_val.values,
            XGBOOST_PARAMS,
            logger,
            use_sample_weights=True
        )

        # Evaluate on validation set
        logger.info("\n--- Validation Set Performance ---")
        metrics, cm = evaluate_model(
            model,
            X_val_scaled,
            y_val.values,
            class_names,
            logger
        )

        # Store results
        metrics['split'] = split_idx
        metrics['validation_year'] = val_year[0]
        metrics['n_train'] = len(X_train)
        metrics['n_val'] = len(X_val)
        cv_results.append(metrics)
        cv_confusion_matrices.append(cm)
        trained_models.append({
            'model': model,
            'scaler': scaler,
            'split': split_idx,
            'validation_year': val_year[0]
        })

    # Aggregate CV results
    logger.info("\n" + "=" * 80)
    logger.info("CROSS-VALIDATION SUMMARY")
    logger.info("=" * 80)

    cv_results_df = pd.DataFrame(cv_results)

    # Mean and std of key metrics
    key_metrics = ['balanced_accuracy', 'f1_macro', 'f1_weighted', 'cohen_kappa', 'roc_auc_ovr']
    logger.info("\nMean ± Std across folds:")
    for metric in key_metrics:
        mean = cv_results_df[metric].mean()
        std = cv_results_df[metric].std()
        logger.info(f"  {metric:20s}: {mean:.4f} ± {std:.4f}")

    # Per-class F1 scores
    logger.info("\nPer-class F1 scores (mean ± std):")
    for class_name in class_names:
        col = f'f1_{class_name.lower()}'
        mean = cv_results_df[col].mean()
        std = cv_results_df[col].std()
        logger.info(f"  {class_name:10s}: {mean:.4f} ± {std:.4f}")

    # Save CV results
    cv_results_path = RESULTS_DIR / f"cv_results_{timestamp}.csv"
    cv_results_df.to_csv(cv_results_path, index=False)
    logger.info(f"\nSaved CV results to: {cv_results_path}")

    # Train final model on all data
    logger.info("\n" + "=" * 80)
    logger.info("TRAINING FINAL MODEL ON ALL DATA")
    logger.info("=" * 80)

    # Use all available data
    scaler_final = StandardScaler()
    X_scaled_final = scaler_final.fit_transform(X)

    # Split into train/val for early stopping (use last year as validation)
    last_year = df['PredictionYear'].max()
    train_mask = df['PredictionYear'] < last_year
    val_mask = df['PredictionYear'] == last_year

    X_train_final = X_scaled_final[train_mask]
    y_train_final = y[train_mask].values
    X_val_final = X_scaled_final[val_mask]
    y_val_final = y[val_mask].values

    logger.info(f"Training on years < {last_year} (n={len(X_train_final)})")
    logger.info(f"Validation on year {last_year} (n={len(X_val_final)})")

    final_model = train_xgboost_model(
        X_train_final,
        y_train_final,
        X_val_final,
        y_val_final,
        XGBOOST_PARAMS,
        logger,
        use_sample_weights=True
    )

    # Evaluate final model
    logger.info("\n--- Final Model Performance (All Data) ---")
    final_metrics, final_cm = evaluate_model(
        final_model,
        X_scaled_final,
        y.values,
        class_names,
        logger
    )

    # Plot confusion matrix for final model
    cm_path = FIGURES_DIR / f"confusion_matrix_final_{timestamp}.png"
    plot_confusion_matrix(final_cm, class_names, cm_path, "Final Model - Confusion Matrix")
    logger.info(f"Saved confusion matrix to: {cm_path}")

    # Feature importance
    logger.info("\n" + "=" * 80)
    logger.info("FEATURE IMPORTANCE ANALYSIS")
    logger.info("=" * 80)

    importance_path = FIGURES_DIR / f"feature_importance_{timestamp}.png"
    importance_df = plot_feature_importance(
        final_model,
        feature_names,
        importance_path,
        top_n=20
    )
    logger.info(f"Saved feature importance plot to: {importance_path}")

    # Save feature importance table
    importance_csv_path = RESULTS_DIR / f"feature_importance_{timestamp}.csv"
    importance_df.to_csv(importance_csv_path, index=False)
    logger.info(f"Saved feature importance table to: {importance_csv_path}")

    # Display top features
    logger.info("\nTop 10 Most Important Features:")
    for idx, row in importance_df.head(10).iterrows():
        logger.info(f"  {row['feature']:30s}: {row['importance']:.6f}")

    # Save final model and scaler
    import joblib

    # Save model using joblib (more reliable for sklearn interface)
    model_path = MODELS_DIR / f"xgboost_final_{timestamp}.pkl"
    joblib.dump(final_model, model_path)
    logger.info(f"\nSaved final model to: {model_path}")

    # Save scaler
    scaler_path = MODELS_DIR / f"scaler_final_{timestamp}.pkl"
    joblib.dump(scaler_final, scaler_path)
    logger.info(f"Saved scaler to: {scaler_path}")

    # Also save feature names for later use
    feature_names_path = MODELS_DIR / f"feature_names_{timestamp}.pkl"
    joblib.dump(feature_names, feature_names_path)
    logger.info(f"Saved feature names to: {feature_names_path}")

    # Generate summary report
    logger.info("\n" + "=" * 80)
    logger.info("TRAINING SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Dataset: {data_path}")
    logger.info(f"Total samples: {len(df):,}")
    logger.info(f"Features: {len(feature_names)}")
    logger.info(f"Classes: {class_names}")
    logger.info(f"CV folds: {len(cv_splits)}")
    logger.info(f"\nMean CV Performance:")
    logger.info(f"  Balanced Accuracy: {cv_results_df['balanced_accuracy'].mean():.4f}")
    logger.info(f"  F1 (macro):        {cv_results_df['f1_macro'].mean():.4f}")
    logger.info(f"  F1 (weighted):     {cv_results_df['f1_weighted'].mean():.4f}")
    logger.info(f"\nFinal Model Performance:")
    logger.info(f"  Balanced Accuracy: {final_metrics['balanced_accuracy']:.4f}")
    logger.info(f"  F1 (macro):        {final_metrics['f1_macro']:.4f}")
    logger.info(f"  F1 (weighted):     {final_metrics['f1_weighted']:.4f}")
    logger.info(f"\nOutputs saved to:")
    logger.info(f"  Models: {MODELS_DIR}")
    logger.info(f"  Results: {RESULTS_DIR}")
    logger.info(f"  Figures: {FIGURES_DIR}")
    logger.info(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    logger.info("TRAINING COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
