"""
Calculate community health burden trajectories for prediction

This script:
1. Calculates year-over-year CHBI changes
2. Standardizes CHBI within each year (z-scores)
3. Calculates trajectory slopes and acceleration
4. Classifies tracts as DECLINE, STABLE, or IMPROVE
5. Creates features for trajectory prediction
"""

import csv
import math
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from statistics import mean, stdev

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

# Trajectory classification thresholds (in z-score standard deviations)
DECLINE_THRESHOLD = 0.3   # CHBI increased by >0.3 SD
IMPROVE_THRESHOLD = -0.3  # CHBI decreased by >0.3 SD


def load_trajectory_panel() -> Dict[str, Dict[int, Dict]]:
    """
    Load trajectory panel and organize by tract and year

    Returns
    -------
    dict
        {tract_fips: {year: {CHBI: value, ...}}}
    """
    input_path = INTERIM_DATA_DIR / "places_trajectory_panel.csv"
    logger.info(f"Loading trajectory panel from {input_path}")

    tract_years = defaultdict(dict)

    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            tract_id = row['TractFIPS']
            year = int(row['Year'])

            try:
                chbi = float(row['CHBI']) if row['CHBI'] else None
                pop = int(float(row['TotalPopulation'])) if row['TotalPopulation'] else 0
            except ValueError:
                chbi = None
                pop = 0

            tract_years[tract_id][year] = {
                'CHBI': chbi,
                'Population': pop,
                'StateAbbr': row['StateAbbr'],
                'CountyFIPS': row['CountyFIPS'],
            }

    logger.info(f"Loaded {len(tract_years):,} tracts across years")
    return dict(tract_years)


def calculate_yearly_statistics(tract_years: Dict) -> Dict[int, Dict]:
    """
    Calculate mean and std dev of CHBI for each year (for z-score standardization)

    Returns
    -------
    dict
        {year: {'mean': value, 'std': value, 'count': n}}
    """
    logger.info("Calculating yearly CHBI statistics...")

    yearly_values = defaultdict(list)

    for tract_id, years in tract_years.items():
        for year, data in years.items():
            if data['CHBI'] is not None:
                yearly_values[year].append(data['CHBI'])

    stats = {}
    for year, values in sorted(yearly_values.items()):
        stats[year] = {
            'mean': mean(values),
            'std': stdev(values) if len(values) > 1 else 1.0,
            'count': len(values),
            'min': min(values),
            'max': max(values),
        }
        logger.info(f"  {year}: n={stats[year]['count']:,}, mean={stats[year]['mean']:.2f}, std={stats[year]['std']:.2f}")

    return stats


def calculate_trajectories(tract_years: Dict, yearly_stats: Dict) -> Dict[str, Dict]:
    """
    Calculate trajectory features for each tract

    Features:
    - CHBI_zscore_current: Current year z-score
    - CHBI_change_1yr: 1-year change in z-score
    - CHBI_change_3yr: 3-year change in z-score
    - CHBI_slope: Linear trend slope (z-score per year)
    - CHBI_acceleration: Change in slope (2nd derivative)
    - trajectory_class: DECLINE, STABLE, or IMPROVE

    Returns
    -------
    dict
        {tract_fips: {feature: value, ...}}
    """
    logger.info("Calculating tract trajectories...")

    trajectories = {}
    decline_count = stable_count = improve_count = 0

    for tract_id, years in tract_years.items():
        # Get available years sorted
        available_years = sorted([y for y, d in years.items() if d['CHBI'] is not None])

        if len(available_years) < 2:
            continue  # Need at least 2 years for trajectory

        # Calculate z-scores for each year
        zscores = {}
        for year in available_years:
            chbi = years[year]['CHBI']
            if chbi is not None and year in yearly_stats:
                zscores[year] = (chbi - yearly_stats[year]['mean']) / yearly_stats[year]['std']

        if not zscores:
            continue

        # Get most recent year
        current_year = max(zscores.keys())
        current_zscore = zscores[current_year]

        # 1-year change
        prev_year = current_year - 1
        change_1yr = None
        if prev_year in zscores:
            change_1yr = current_zscore - zscores[prev_year]

        # 3-year change
        prev_year_3 = current_year - 3
        change_3yr = None
        if prev_year_3 in zscores:
            change_3yr = current_zscore - zscores[prev_year_3]

        # Linear slope (simple linear regression)
        years_list = sorted(zscores.keys())
        if len(years_list) >= 2:
            n = len(years_list)
            sum_x = sum(years_list)
            sum_y = sum(zscores[y] for y in years_list)
            sum_xy = sum(y * zscores[y] for y in years_list)
            sum_x2 = sum(y * y for y in years_list)

            denominator = n * sum_x2 - sum_x * sum_x
            if denominator != 0:
                slope = (n * sum_xy - sum_x * sum_y) / denominator
            else:
                slope = 0
        else:
            slope = 0

        # Acceleration (2nd derivative estimate)
        if len(years_list) >= 3:
            # Simple: change in change
            changes = []
            for i in range(1, len(years_list)):
                changes.append(zscores[years_list[i]] - zscores[years_list[i-1]])
            if len(changes) >= 2:
                acceleration = changes[-1] - changes[0]
            else:
                acceleration = 0
        else:
            acceleration = 0

        # Classify trajectory based on 1-year change
        if change_1yr is not None:
            if change_1yr > DECLINE_THRESHOLD:
                trajectory_class = 'DECLINE'
                decline_count += 1
            elif change_1yr < IMPROVE_THRESHOLD:
                trajectory_class = 'IMPROVE'
                improve_count += 1
            else:
                trajectory_class = 'STABLE'
                stable_count += 1
        else:
            trajectory_class = 'UNKNOWN'

        # Store trajectory data
        trajectories[tract_id] = {
            'TractFIPS': tract_id,
            'CurrentYear': current_year,
            'StateAbbr': years[current_year]['StateAbbr'],
            'CountyFIPS': years[current_year]['CountyFIPS'],
            'Population': years[current_year]['Population'],
            'CHBI_current': years[current_year]['CHBI'],
            'CHBI_zscore_current': current_zscore,
            'CHBI_change_1yr': change_1yr,
            'CHBI_change_3yr': change_3yr,
            'CHBI_slope': slope,
            'CHBI_acceleration': acceleration,
            'years_observed': len(available_years),
            'trajectory_class': trajectory_class,
        }

    logger.info(f"Calculated trajectories for {len(trajectories):,} tracts")
    logger.info(f"  DECLINE: {decline_count:,} ({100*decline_count/len(trajectories):.1f}%)")
    logger.info(f"  STABLE:  {stable_count:,} ({100*stable_count/len(trajectories):.1f}%)")
    logger.info(f"  IMPROVE: {improve_count:,} ({100*improve_count/len(trajectories):.1f}%)")

    return trajectories


def identify_prediction_targets(tract_years: Dict, yearly_stats: Dict) -> List[Dict]:
    """
    Create prediction dataset: use T-1 features to predict T trajectory

    For each prediction year (2022, 2023, 2024, 2025):
    - Features: CHBI and changes up to year T-1
    - Target: Trajectory class in year T

    Returns
    -------
    list of dict
        Each dict is one training example
    """
    logger.info("Creating prediction dataset...")

    prediction_years = [2022, 2023, 2024, 2025]
    examples = []

    for tract_id, years in tract_years.items():
        for target_year in prediction_years:
            prev_year = target_year - 1
            prev_year_2 = target_year - 2

            # Need at least 2 years prior to target
            if prev_year not in years or prev_year_2 not in years:
                continue
            if years[prev_year]['CHBI'] is None or years[prev_year_2]['CHBI'] is None:
                continue
            if target_year not in years or years[target_year]['CHBI'] is None:
                continue

            # Calculate features (at T-1)
            chbi_prev = years[prev_year]['CHBI']
            chbi_prev_2 = years[prev_year_2]['CHBI']

            zscore_prev = (chbi_prev - yearly_stats[prev_year]['mean']) / yearly_stats[prev_year]['std']
            zscore_prev_2 = (chbi_prev_2 - yearly_stats[prev_year_2]['mean']) / yearly_stats[prev_year_2]['std']

            change_1yr = zscore_prev - zscore_prev_2

            # Calculate target (trajectory at T)
            chbi_target = years[target_year]['CHBI']
            zscore_target = (chbi_target - yearly_stats[target_year]['mean']) / yearly_stats[target_year]['std']
            target_change = zscore_target - zscore_prev

            if target_change > DECLINE_THRESHOLD:
                target_class = 'DECLINE'
            elif target_change < IMPROVE_THRESHOLD:
                target_class = 'IMPROVE'
            else:
                target_class = 'STABLE'

            examples.append({
                'TractFIPS': tract_id,
                'PredictionYear': target_year,
                'StateAbbr': years[prev_year]['StateAbbr'],
                'CountyFIPS': years[prev_year]['CountyFIPS'],
                'Population': years[prev_year]['Population'],
                # Features (at T-1)
                'CHBI_prev': chbi_prev,
                'CHBI_zscore_prev': zscore_prev,
                'CHBI_change_1yr': change_1yr,
                # Target (at T)
                'target_change': target_change,
                'target_class': target_class,
            })

    logger.info(f"Created {len(examples):,} prediction examples")

    # Distribution by year and class
    for year in prediction_years:
        year_examples = [e for e in examples if e['PredictionYear'] == year]
        logger.info(f"  {year}: {len(year_examples):,} examples")
        for cls in ['DECLINE', 'STABLE', 'IMPROVE']:
            count = len([e for e in year_examples if e['target_class'] == cls])
            pct = 100 * count / len(year_examples) if year_examples else 0
            logger.info(f"    {cls}: {count:,} ({pct:.1f}%)")

    return examples


def save_trajectories(trajectories: Dict, output_path: Path) -> None:
    """Save trajectory data to CSV"""
    if not trajectories:
        return

    first_key = next(iter(trajectories))
    columns = list(trajectories[first_key].keys())

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for tract_id, data in sorted(trajectories.items()):
            writer.writerow(data)

    logger.info(f"Saved trajectories to {output_path}")


def save_prediction_dataset(examples: List[Dict], output_path: Path) -> None:
    """Save prediction dataset to CSV"""
    if not examples:
        return

    columns = list(examples[0].keys())

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for example in examples:
            writer.writerow(example)

    logger.info(f"Saved prediction dataset to {output_path}")


def identify_top_declining_improving(trajectories: Dict, n: int = 100) -> Tuple[List, List]:
    """
    Identify the tracts with largest decline and improvement

    Returns
    -------
    tuple
        (top_declining, top_improving) lists of tract data
    """
    # Filter to tracts with 1-year change data
    with_change = [t for t in trajectories.values() if t['CHBI_change_1yr'] is not None]

    # Sort by change
    declining = sorted(with_change, key=lambda x: -x['CHBI_change_1yr'])[:n]
    improving = sorted(with_change, key=lambda x: x['CHBI_change_1yr'])[:n]

    return declining, improving


def print_summary_report(trajectories: Dict, declining: List, improving: List) -> None:
    """Print summary report of trajectory patterns"""
    print("\n" + "="*70)
    print("COMMUNITY HEALTH TRAJECTORY ANALYSIS")
    print("="*70)

    # Overall statistics
    valid = [t for t in trajectories.values() if t['trajectory_class'] != 'UNKNOWN']
    print(f"\nTotal tracts analyzed: {len(valid):,}")

    by_class = defaultdict(list)
    for t in valid:
        by_class[t['trajectory_class']].append(t)

    print("\nTrajectory Distribution:")
    for cls, tracts in sorted(by_class.items()):
        total_pop = sum(t['Population'] for t in tracts)
        print(f"  {cls}: {len(tracts):,} tracts ({total_pop/1_000_000:.1f}M people)")

    # Regional patterns
    print("\n" + "-"*50)
    print("REGIONAL TRAJECTORY PATTERNS")
    print("-"*50)

    # By state
    by_state = defaultdict(lambda: {'DECLINE': 0, 'STABLE': 0, 'IMPROVE': 0, 'total': 0})
    for t in valid:
        state = t['StateAbbr']
        by_state[state][t['trajectory_class']] += 1
        by_state[state]['total'] += 1

    # States with highest decline rates
    state_decline_rates = []
    for state, counts in by_state.items():
        if counts['total'] >= 50:  # Minimum tracts for meaningful rate
            decline_rate = counts['DECLINE'] / counts['total']
            state_decline_rates.append((state, decline_rate, counts['total']))

    state_decline_rates.sort(key=lambda x: -x[1])

    print("\nStates with Highest Decline Rates:")
    for state, rate, total in state_decline_rates[:10]:
        print(f"  {state}: {100*rate:.1f}% declining ({total} tracts)")

    print("\nStates with Highest Improvement Rates:")
    state_improve_rates = [(s, by_state[s]['IMPROVE']/by_state[s]['total'], by_state[s]['total'])
                          for s in by_state if by_state[s]['total'] >= 50]
    state_improve_rates.sort(key=lambda x: -x[1])
    for state, rate, total in state_improve_rates[:10]:
        print(f"  {state}: {100*rate:.1f}% improving ({total} tracts)")

    # Top declining communities
    print("\n" + "-"*50)
    print("TOP 10 DECLINING COMMUNITIES (Highest CHBI Increase)")
    print("-"*50)
    for i, t in enumerate(declining[:10], 1):
        print(f"{i:2}. {t['TractFIPS']} ({t['StateAbbr']})")
        print(f"    CHBI change: +{t['CHBI_change_1yr']:.3f} SD, Pop: {t['Population']:,}")

    # Top improving communities
    print("\n" + "-"*50)
    print("TOP 10 IMPROVING COMMUNITIES (Largest CHBI Decrease)")
    print("-"*50)
    for i, t in enumerate(improving[:10], 1):
        print(f"{i:2}. {t['TractFIPS']} ({t['StateAbbr']})")
        print(f"    CHBI change: {t['CHBI_change_1yr']:.3f} SD, Pop: {t['Population']:,}")


if __name__ == "__main__":
    logger.info("="*60)
    logger.info("COMMUNITY HEALTH TRAJECTORY CALCULATION")
    logger.info("="*60)

    # Load data
    tract_years = load_trajectory_panel()
    yearly_stats = calculate_yearly_statistics(tract_years)

    # Calculate trajectories
    trajectories = calculate_trajectories(tract_years, yearly_stats)

    # Save trajectories
    save_trajectories(trajectories, PROCESSED_DATA_DIR / "tract_trajectories.csv")

    # Create prediction dataset
    prediction_examples = identify_prediction_targets(tract_years, yearly_stats)
    save_prediction_dataset(prediction_examples, PROCESSED_DATA_DIR / "prediction_dataset.csv")

    # Identify extremes
    declining, improving = identify_top_declining_improving(trajectories)

    # Print summary report
    print_summary_report(trajectories, declining, improving)

    logger.info("")
    logger.info("Trajectory calculation complete!")
