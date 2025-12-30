"""
Community Health Trajectory Prediction System

An early warning system that predicts which census tracts will experience
health burden DECLINE or IMPROVEMENT 12-24 months in advance.

Key Components:
- data_preparation: Load and merge CDC PLACES + Census data
- feature_engineering: Create temporal, spatial, and SDOH features
- models: XGBoost, LSTM, SAR, and ensemble implementations
- validation: Temporal cross-validation framework
- interpretation: SHAP analysis and feature importance
"""

__version__ = "0.1.0"
__author__ = "Resilience Mapping Project"

from . import config
from .data_preparation import load_places_longitudinal, load_census_acs
from .feature_engineering import create_composite_health_burden_index, engineer_features
from .validation import TemporalCrossValidator

__all__ = [
    'config',
    'load_places_longitudinal',
    'load_census_acs',
    'create_composite_health_burden_index',
    'engineer_features',
    'TemporalCrossValidator',
]
