#!/usr/bin/env python3
"""
Build Rich Feature Set for Community Health Trajectory Prediction

This script creates 50+ features from the available PLACES longitudinal data:
1. Component-level trajectories (7 health measures)
2. Temporal features (trends, acceleration, momentum)
3. Relative positioning features (within-year percentiles)
4. Component interaction features
5. Volatility and stability measures

Author: Enhanced feature engineering pipeline
Date: 2025-12-30
"""

import csv
import math
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from statistics import mean, stdev, median

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# CHBI component weights (from harmonize script)
CHBI_COMPONENTS = {
    'OBESITY': 0.20,
    'DIABETES': 0.20,
    'CHD': 0.15,
    'BPHIGH': 0.10,
    'LPA': 0.10,
    'MHLTH': 0.15,
    'PHLTH': 0.10,
}

# Trajectory classification thresholds
DECLINE_THRESHOLD = 0.3
IMPROVE_THRESHOLD = -0.3


def load_trajectory_panel() -> Dict[str, Dict[int, Dict]]:
    """Load trajectory panel and organize by tract and year."""
    input_path = INTERIM_DATA_DIR / "places_trajectory_panel.csv"
    logger.info(f"Loading trajectory panel from {input_path}")

    tract_years = defaultdict(dict)

    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            tract_id = row['TractFIPS']
            year = int(row['Year'])

            data = {
                'StateAbbr': row['StateAbbr'],
                'CountyFIPS': row['CountyFIPS'],
                'Population': int(float(row['TotalPopulation'])) if row['TotalPopulation'] else 0,
            }

            # Parse CHBI and all component values
            try:
                data['CHBI'] = float(row['CHBI']) if row['CHBI'] else None
            except ValueError:
                data['CHBI'] = None

            for component in CHBI_COMPONENTS.keys():
                col = f'{component}_CrudePrev'
                try:
                    data[component] = float(row[col]) if row.get(col) else None
                except (ValueError, KeyError):
                    data[component] = None

            tract_years[tract_id][year] = data

    logger.info(f"Loaded {len(tract_years):,} tracts")
    return dict(tract_years)


def calculate_yearly_statistics(tract_years: Dict) -> Dict[int, Dict]:
    """Calculate mean and std dev for CHBI and all components for each year."""
    logger.info("Calculating yearly statistics for standardization...")

    # Collect values by year for each measure
    yearly_values = defaultdict(lambda: defaultdict(list))

    for tract_id, years in tract_years.items():
        for year, data in years.items():
            if data['CHBI'] is not None:
                yearly_values[year]['CHBI'].append(data['CHBI'])

            for component in CHBI_COMPONENTS.keys():
                if data.get(component) is not None:
                    yearly_values[year][component].append(data[component])

    # Calculate stats
    stats = {}
    for year in sorted(yearly_values.keys()):
        stats[year] = {}
        for measure in ['CHBI'] + list(CHBI_COMPONENTS.keys()):
            values = yearly_values[year].get(measure, [])
            if len(values) > 1:
                stats[year][measure] = {
                    'mean': mean(values),
                    'std': stdev(values),
                    'median': median(values),
                    'min': min(values),
                    'max': max(values),
                    'p25': sorted(values)[len(values)//4],
                    'p75': sorted(values)[3*len(values)//4],
                }
            else:
                stats[year][measure] = {
                    'mean': values[0] if values else 0,
                    'std': 1.0,
                    'median': values[0] if values else 0,
                    'min': values[0] if values else 0,
                    'max': values[0] if values else 0,
                    'p25': values[0] if values else 0,
                    'p75': values[0] if values else 0,
                }

    logger.info(f"  Calculated statistics for {len(stats)} years")
    return stats


def calculate_zscore(value: float, year_stats: Dict) -> Optional[float]:
    """Calculate z-score for a value."""
    if value is None or year_stats['std'] == 0:
        return None
    return (value - year_stats['mean']) / year_stats['std']


def calculate_percentile(value: float, year_stats: Dict) -> Optional[float]:
    """Calculate approximate percentile position (0-1)."""
    if value is None:
        return None
    # Use min/max to estimate percentile
    range_val = year_stats['max'] - year_stats['min']
    if range_val == 0:
        return 0.5
    return (value - year_stats['min']) / range_val


def linear_regression_slope(x_vals: List, y_vals: List) -> Optional[float]:
    """Calculate simple linear regression slope."""
    if len(x_vals) < 2 or len(y_vals) < 2:
        return None

    n = len(x_vals)
    sum_x = sum(x_vals)
    sum_y = sum(y_vals)
    sum_xy = sum(x * y for x, y in zip(x_vals, y_vals))
    sum_x2 = sum(x * x for x in x_vals)

    denominator = n * sum_x2 - sum_x * sum_x
    if denominator == 0:
        return 0

    return (n * sum_xy - sum_x * sum_y) / denominator


def build_prediction_dataset(tract_years: Dict, yearly_stats: Dict) -> List[Dict]:
    """
    Build prediction dataset with 50+ features.

    For each prediction year (2022-2025):
    - Features use data from years prior to prediction year
    - Target is the trajectory in the prediction year
    """
    logger.info("Building rich prediction dataset...")

    # Note: 2025 PLACES data is identical to 2024 (not yet updated), so exclude it
    prediction_years = [2022, 2023, 2024]
    examples = []

    for tract_id, years in tract_years.items():
        available_years = sorted(years.keys())

        for target_year in prediction_years:
            prev_year = target_year - 1
            prev_year_2 = target_year - 2
            prev_year_3 = target_year - 3

            # Need at least 2 years prior to target
            if prev_year not in years or prev_year_2 not in years:
                continue
            if years[prev_year]['CHBI'] is None or years[prev_year_2]['CHBI'] is None:
                continue
            if target_year not in years or years[target_year]['CHBI'] is None:
                continue

            # Get data
            curr = years[prev_year]  # Most recent available data
            prev = years[prev_year_2]
            prev3 = years.get(prev_year_3, {})
            target_data = years[target_year]

            # Get yearly stats
            curr_stats = yearly_stats.get(prev_year, {})
            prev_stats = yearly_stats.get(prev_year_2, {})
            target_stats = yearly_stats.get(target_year, {})

            # Initialize feature dict
            features = {
                'TractFIPS': tract_id,
                'PredictionYear': target_year,
                'StateAbbr': curr['StateAbbr'],
                'CountyFIPS': curr['CountyFIPS'],
                'Population': curr['Population'],
            }

            # =================================================================
            # FEATURE GROUP 1: CHBI Features (Primary)
            # =================================================================

            # Raw values
            features['CHBI_prev'] = curr['CHBI']
            features['CHBI_prev2'] = prev['CHBI']

            # Z-scores (standardized within year)
            chbi_zscore_curr = calculate_zscore(curr['CHBI'], curr_stats.get('CHBI', {'mean': 20, 'std': 5}))
            chbi_zscore_prev = calculate_zscore(prev['CHBI'], prev_stats.get('CHBI', {'mean': 20, 'std': 5}))
            features['CHBI_zscore_prev'] = chbi_zscore_curr
            features['CHBI_zscore_prev2'] = chbi_zscore_prev

            # 1-year change in z-score
            if chbi_zscore_curr is not None and chbi_zscore_prev is not None:
                features['CHBI_change_1yr'] = chbi_zscore_curr - chbi_zscore_prev
            else:
                features['CHBI_change_1yr'] = 0

            # 2-year change if available
            if prev_year_3 in years and prev3.get('CHBI') is not None:
                prev3_stats = yearly_stats.get(prev_year_3, {})
                chbi_zscore_prev3 = calculate_zscore(prev3['CHBI'], prev3_stats.get('CHBI', {'mean': 20, 'std': 5}))
                if chbi_zscore_curr is not None and chbi_zscore_prev3 is not None:
                    features['CHBI_change_2yr'] = chbi_zscore_curr - chbi_zscore_prev3
                else:
                    features['CHBI_change_2yr'] = 0
            else:
                features['CHBI_change_2yr'] = features['CHBI_change_1yr']  # Fallback

            # Percentile position
            features['CHBI_percentile'] = calculate_percentile(curr['CHBI'], curr_stats.get('CHBI', {'min': 10, 'max': 40}))

            # Distance from danger zone (high CHBI = bad)
            if 'CHBI' in curr_stats:
                features['CHBI_distance_from_p75'] = curr_stats['CHBI']['p75'] - curr['CHBI']
            else:
                features['CHBI_distance_from_p75'] = 0

            # =================================================================
            # FEATURE GROUP 2: Component-Level Features (7 measures x 5+ features)
            # =================================================================

            for component in CHBI_COMPONENTS.keys():
                comp_curr = curr.get(component)
                comp_prev = prev.get(component)
                comp_prev3 = prev3.get(component) if prev3 else None

                # Raw value
                features[f'{component}_prev'] = comp_curr if comp_curr is not None else 0

                # Z-score
                if comp_curr is not None and component in curr_stats:
                    features[f'{component}_zscore'] = calculate_zscore(
                        comp_curr, curr_stats[component]
                    )
                else:
                    features[f'{component}_zscore'] = 0

                # 1-year change
                if comp_curr is not None and comp_prev is not None:
                    # Calculate as change in raw value (percentage point change)
                    features[f'{component}_change_1yr'] = comp_curr - comp_prev

                    # Also as z-score change
                    if component in curr_stats and component in prev_stats:
                        z_curr = calculate_zscore(comp_curr, curr_stats[component])
                        z_prev = calculate_zscore(comp_prev, prev_stats[component])
                        if z_curr is not None and z_prev is not None:
                            features[f'{component}_zchange_1yr'] = z_curr - z_prev
                        else:
                            features[f'{component}_zchange_1yr'] = 0
                    else:
                        features[f'{component}_zchange_1yr'] = 0
                else:
                    features[f'{component}_change_1yr'] = 0
                    features[f'{component}_zchange_1yr'] = 0

                # Percentile
                if comp_curr is not None and component in curr_stats:
                    features[f'{component}_percentile'] = calculate_percentile(
                        comp_curr, curr_stats[component]
                    )
                else:
                    features[f'{component}_percentile'] = 0.5

            # =================================================================
            # FEATURE GROUP 3: Temporal Pattern Features
            # =================================================================

            # Calculate CHBI slope if we have 3+ years
            history_years = [y for y in [prev_year_3, prev_year_2, prev_year] if y in years]
            if len(history_years) >= 2:
                chbi_values = []
                for y in history_years:
                    if years[y]['CHBI'] is not None:
                        y_stats = yearly_stats.get(y, {})
                        z = calculate_zscore(years[y]['CHBI'], y_stats.get('CHBI', {'mean': 20, 'std': 5}))
                        if z is not None:
                            chbi_values.append((y, z))

                if len(chbi_values) >= 2:
                    years_list = [v[0] for v in chbi_values]
                    zscores_list = [v[1] for v in chbi_values]
                    features['CHBI_trend_slope'] = linear_regression_slope(years_list, zscores_list)
                else:
                    features['CHBI_trend_slope'] = features['CHBI_change_1yr']
            else:
                features['CHBI_trend_slope'] = features['CHBI_change_1yr']

            # Momentum (is change accelerating or decelerating?)
            if len(history_years) >= 3 and prev_year_3 in years:
                chbi_prev3 = years[prev_year_3]['CHBI']
                if chbi_prev3 is not None and prev['CHBI'] is not None and curr['CHBI'] is not None:
                    change_recent = curr['CHBI'] - prev['CHBI']
                    change_older = prev['CHBI'] - chbi_prev3
                    features['CHBI_acceleration'] = change_recent - change_older
                else:
                    features['CHBI_acceleration'] = 0
            else:
                features['CHBI_acceleration'] = 0

            # =================================================================
            # FEATURE GROUP 4: Component Divergence Features
            # =================================================================

            # Which components are improving vs worsening?
            component_changes = []
            for component in CHBI_COMPONENTS.keys():
                change = features.get(f'{component}_zchange_1yr', 0)
                if change is not None:
                    component_changes.append((component, change))

            if component_changes:
                # Count components improving/worsening
                features['n_components_improving'] = sum(1 for c, v in component_changes if v < -0.1)
                features['n_components_worsening'] = sum(1 for c, v in component_changes if v > 0.1)
                features['n_components_stable'] = sum(1 for c, v in component_changes if -0.1 <= v <= 0.1)

                # Max/min component changes
                features['max_component_improvement'] = min(v for c, v in component_changes)
                features['max_component_decline'] = max(v for c, v in component_changes)

                # Component change volatility
                changes = [v for c, v in component_changes if v is not None]
                if len(changes) > 1:
                    features['component_change_volatility'] = stdev(changes)
                else:
                    features['component_change_volatility'] = 0
            else:
                features['n_components_improving'] = 0
                features['n_components_worsening'] = 0
                features['n_components_stable'] = 7
                features['max_component_improvement'] = 0
                features['max_component_decline'] = 0
                features['component_change_volatility'] = 0

            # =================================================================
            # FEATURE GROUP 5: Risk Profile Features
            # =================================================================

            # High-risk component exposure
            high_risk_components = 0
            for component in CHBI_COMPONENTS.keys():
                pct = features.get(f'{component}_percentile', 0.5)
                if pct is not None and pct > 0.75:
                    high_risk_components += 1
            features['n_high_risk_components'] = high_risk_components

            # Concentrated vs diffuse burden
            component_zscores = [
                features.get(f'{component}_zscore', 0)
                for component in CHBI_COMPONENTS.keys()
            ]
            if component_zscores:
                valid_zscores = [z for z in component_zscores if z is not None]
                if len(valid_zscores) > 1:
                    features['burden_concentration'] = max(valid_zscores) - min(valid_zscores)
                else:
                    features['burden_concentration'] = 0
            else:
                features['burden_concentration'] = 0

            # Mental health specific risk (MHLTH is strong predictor)
            features['mental_health_risk'] = features.get('MHLTH_zscore', 0)
            features['mental_health_trajectory'] = features.get('MHLTH_zchange_1yr', 0)

            # Physical health risk (PHLTH)
            features['physical_health_risk'] = features.get('PHLTH_zscore', 0)
            features['physical_health_trajectory'] = features.get('PHLTH_zchange_1yr', 0)

            # =================================================================
            # FEATURE GROUP 6: Population Features
            # =================================================================

            features['log_population'] = math.log(curr['Population'] + 1)

            # Population change if available
            if prev['Population'] and prev['Population'] > 0:
                features['population_change_pct'] = (
                    (curr['Population'] - prev['Population']) / prev['Population']
                )
            else:
                features['population_change_pct'] = 0

            # =================================================================
            # TARGET CALCULATION
            # =================================================================

            # Calculate target z-score change
            target_zscore = calculate_zscore(
                target_data['CHBI'],
                target_stats.get('CHBI', {'mean': 20, 'std': 5})
            )

            if chbi_zscore_curr is not None and target_zscore is not None:
                target_change = target_zscore - chbi_zscore_curr

                if target_change > DECLINE_THRESHOLD:
                    target_class = 'DECLINE'
                elif target_change < IMPROVE_THRESHOLD:
                    target_class = 'IMPROVE'
                else:
                    target_class = 'STABLE'

                features['target_change'] = target_change
                features['target_class'] = target_class

                examples.append(features)

    logger.info(f"Created {len(examples):,} prediction examples")
    return examples


def analyze_features(examples: List[Dict]) -> None:
    """Print summary statistics for the feature set."""
    if not examples:
        return

    # Count features
    feature_cols = [k for k in examples[0].keys()
                    if k not in ['TractFIPS', 'PredictionYear', 'StateAbbr',
                                'CountyFIPS', 'target_change', 'target_class']]

    logger.info(f"\n{'='*60}")
    logger.info(f"FEATURE SET SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"Total features: {len(feature_cols)}")
    logger.info(f"Total examples: {len(examples):,}")

    # Feature categories
    categories = {
        'CHBI': [f for f in feature_cols if f.startswith('CHBI_') or f == 'Population'],
        'OBESITY': [f for f in feature_cols if 'OBESITY' in f],
        'DIABETES': [f for f in feature_cols if 'DIABETES' in f],
        'CHD': [f for f in feature_cols if 'CHD' in f],
        'BPHIGH': [f for f in feature_cols if 'BPHIGH' in f],
        'LPA': [f for f in feature_cols if 'LPA' in f],
        'MHLTH': [f for f in feature_cols if 'MHLTH' in f],
        'PHLTH': [f for f in feature_cols if 'PHLTH' in f],
        'Component Aggregate': [f for f in feature_cols if 'n_components' in f or 'component' in f.lower()],
        'Risk Profile': [f for f in feature_cols if 'risk' in f.lower() or 'burden' in f.lower()],
        'Temporal': [f for f in feature_cols if 'trend' in f or 'acceleration' in f or 'momentum' in f],
    }

    logger.info("\nFeature categories:")
    for cat, features in categories.items():
        if features:
            logger.info(f"  {cat}: {len(features)} features")

    # Target distribution
    class_counts = defaultdict(int)
    for ex in examples:
        class_counts[ex['target_class']] += 1

    logger.info("\nTarget distribution:")
    for cls in ['DECLINE', 'STABLE', 'IMPROVE']:
        count = class_counts[cls]
        pct = 100 * count / len(examples)
        logger.info(f"  {cls}: {count:,} ({pct:.1f}%)")

    # By year
    logger.info("\nExamples by prediction year:")
    year_counts = defaultdict(int)
    for ex in examples:
        year_counts[ex['PredictionYear']] += 1
    for year in sorted(year_counts.keys()):
        logger.info(f"  {year}: {year_counts[year]:,}")


def save_dataset(examples: List[Dict], output_path: Path) -> None:
    """Save dataset to CSV."""
    if not examples:
        return

    # Ensure consistent column order
    columns = list(examples[0].keys())

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for example in examples:
            writer.writerow(example)

    logger.info(f"Saved dataset to {output_path}")


if __name__ == "__main__":
    logger.info("="*60)
    logger.info("BUILDING RICH FEATURE SET FOR TRAJECTORY PREDICTION")
    logger.info("="*60)

    # Load data
    tract_years = load_trajectory_panel()
    yearly_stats = calculate_yearly_statistics(tract_years)

    # Build prediction dataset with rich features
    examples = build_prediction_dataset(tract_years, yearly_stats)

    # Analyze features
    analyze_features(examples)

    # Save
    output_path = PROCESSED_DATA_DIR / "prediction_dataset_rich.csv"
    save_dataset(examples, output_path)

    logger.info("")
    logger.info("Feature engineering complete!")
