"""
Configuration for Community Health Trajectory Prediction System
"""

from pathlib import Path
import os

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "output"
MODELS_DIR = PROJECT_ROOT / "models" / "trajectory_prediction"
RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = PROJECT_ROOT / "figures" / "trajectory"

# Create directories if they don't exist
for dir_path in [PROCESSED_DATA_DIR, MODELS_DIR, RESULTS_DIR, FIGURES_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Data sources
PLACES_YEARS = [2020, 2021, 2022, 2023, 2024, 2025]
ACS_YEARS = list(range(2015, 2024))  # 5-year estimates

# Composite Health Burden Index (CHBI) components
CHBI_COMPONENTS = {
    'OBESITY': 0.20,      # Weight by mortality burden and prevention amenability
    'DIABETES': 0.20,
    'CHD': 0.15,          # Coronary heart disease
    'BPHIGH': 0.10,       # High blood pressure
    'LPA': 0.10,          # Physical inactivity
    'MHLTH': 0.15,        # Mental health (poor mental health days)
    'PHLTH': 0.10,        # Physical health (poor physical health days)
}

# Trajectory classification thresholds
TRAJECTORY_THRESHOLDS = {
    'decline_threshold': 0.5,    # Standard deviations
    'improve_threshold': -0.5,   # Standard deviations
    'prediction_horizon_months': 12,  # Primary prediction target
}

# Feature engineering parameters
SPATIAL_PARAMS = {
    'spatial_weights_type': 'queen',  # Queen contiguity for adjacency
    'k_nearest': 5,                    # For k-nearest neighbors spatial weights
    'distance_band_km': 10,            # For distance-based weights
}

# Model hyperparameters (initial values, will be tuned)
XGBOOST_PARAMS = {
    'n_estimators': 500,
    'max_depth': 6,
    'learning_rate': 0.05,
    'min_child_weight': 5,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'objective': 'multi:softprob',  # 3-class classification
    'num_class': 3,
    'eval_metric': 'mlogloss',
    'random_state': 42,
    'tree_method': 'hist',  # Faster for large datasets
}

LSTM_PARAMS = {
    'input_dim': 50,  # Will be set dynamically based on features
    'hidden_dim': 64,
    'num_layers': 2,
    'dropout': 0.3,
    'num_classes': 3,
    'sequence_length': 4,  # Use 4 years of history
    'batch_size': 256,
    'learning_rate': 0.001,
    'epochs': 100,
    'early_stopping_patience': 10,
}

RANDOM_FOREST_PARAMS = {
    'n_estimators': 500,
    'max_features': 'sqrt',
    'min_samples_split': 10,
    'min_samples_leaf': 5,
    'random_state': 42,
    'n_jobs': -1,
}

# Temporal cross-validation
CV_CONFIG = {
    'min_train_years': 2,     # Minimum years needed for training
    'validation_years': [2022, 2023, 2024, 2025],  # Years to validate on
    'expanding_window': True,  # Use expanding vs rolling window
}

# Evaluation metrics
METRICS = [
    'balanced_accuracy',
    'f1_macro',
    'f1_weighted',
    'cohen_kappa',
    'roc_auc_ovr',  # One-vs-rest for multi-class
]

# Feature importance
SHAP_PARAMS = {
    'max_display': 20,        # Top N features to display
    'check_additivity': False,  # Speed up for large datasets
    'approximate': True,      # Use TreeExplainer approximation for speed
}

# Plotting
PLOT_PARAMS = {
    'figure_size': (12, 8),
    'dpi': 300,
    'style': 'seaborn-v0_8-darkgrid',
    'palette': 'husl',
    'save_format': 'png',
}

# Target variable encoding
TRAJECTORY_LABELS = {
    'DECLINE': 0,
    'STABLE': 1,
    'IMPROVE': 2,
}

# Random seed for reproducibility
RANDOM_SEED = 42

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = RESULTS_DIR / 'trajectory_prediction.log'
