#!/usr/bin/env python3
"""
Build Spatial Features for Community Health Trajectory Prediction

This script computes neighbor-based spatial features:
1. Neighbor average CHBI (spatial lag)
2. Spatial autocorrelation indicators
3. Hot spot / cold spot classification
4. Neighborhood health context

Uses tract geometries to identify contiguous neighbors.

Author: Spatial feature engineering pipeline
Date: 2025-12-30
"""

import json
import csv
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
from statistics import mean, stdev
from shapely.geometry import shape
from shapely import STRtree

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
INTERIM_DATA_DIR = DATA_DIR / "interim"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_tract_geometries() -> Dict[str, any]:
    """Load tract geometries from GeoJSON file."""
    geojson_path = PROCESSED_DATA_DIR / "tracts_enriched.geojson"
    logger.info(f"Loading tract geometries from {geojson_path}")

    with open(geojson_path, 'r') as f:
        data = json.load(f)

    tracts = {}
    for feature in data['features']:
        geoid = feature['properties']['GEOID']
        geom = shape(feature['geometry'])
        tracts[geoid] = {
            'geometry': geom,
            'state': feature['properties'].get('STATEFP'),
            'county': feature['properties'].get('COUNTYFP'),
        }

    logger.info(f"Loaded {len(tracts):,} tract geometries")
    return tracts


def build_neighbor_graph(tracts: Dict) -> Dict[str, Set[str]]:
    """
    Build adjacency graph using spatial index for efficiency.
    Two tracts are neighbors if they touch (share boundary or point).
    """
    logger.info("Building neighbor adjacency graph...")

    # Create list of (geoid, geometry) for indexing
    geoids = list(tracts.keys())
    geometries = [tracts[g]['geometry'] for g in geoids]

    # Build spatial index
    tree = STRtree(geometries)

    # Find neighbors for each tract
    neighbors = defaultdict(set)

    for i, geoid in enumerate(geoids):
        geom = geometries[i]

        # Query spatial index for potential neighbors
        # Using touches or intersects (shared boundary)
        candidate_indices = tree.query(geom)

        for j in candidate_indices:
            if i != j:  # Don't include self
                other_geoid = geoids[j]
                other_geom = geometries[j]

                # Check if they actually touch (share boundary)
                if geom.touches(other_geom) or geom.intersects(other_geom):
                    neighbors[geoid].add(other_geoid)
                    neighbors[other_geoid].add(geoid)

        if (i + 1) % 10000 == 0:
            logger.info(f"  Processed {i + 1:,} / {len(geoids):,} tracts")

    # Stats
    n_neighbors = [len(v) for v in neighbors.values()]
    avg_neighbors = mean(n_neighbors) if n_neighbors else 0
    logger.info(f"Average neighbors per tract: {avg_neighbors:.1f}")
    logger.info(f"Tracts with 0 neighbors (islands): {sum(1 for n in n_neighbors if n == 0):,}")

    return dict(neighbors)


def load_trajectory_panel() -> Dict[str, Dict[int, Dict]]:
    """Load trajectory panel data organized by tract and year."""
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
            except ValueError:
                chbi = None

            tract_years[tract_id][year] = {
                'CHBI': chbi,
            }

    logger.info(f"Loaded trajectory data for {len(tract_years):,} tracts")
    return dict(tract_years)


def compute_spatial_features(
    tract_id: str,
    year: int,
    neighbors: Dict[str, Set[str]],
    tract_years: Dict[str, Dict[int, Dict]],
    yearly_stats: Dict[int, Dict]
) -> Dict[str, float]:
    """
    Compute spatial features for a tract in a given year.

    Features:
    - n_neighbors: Number of contiguous neighbors
    - neighbor_avg_chbi: Average CHBI of neighbors
    - neighbor_std_chbi: Std dev of neighbor CHBI values
    - spatial_lag: Tract CHBI - neighbor average (positive = worse than neighbors)
    - spatial_lag_zscore: Standardized spatial lag
    - is_local_hotspot: 1 if tract CHBI > neighbor avg by 0.5 SD
    - is_local_coldspot: 1 if tract CHBI < neighbor avg by 0.5 SD
    - neighbor_improving_pct: % of neighbors that improved last year
    - neighbor_declining_pct: % of neighbors that declined last year
    """
    features = {
        'n_neighbors': 0,
        'neighbor_avg_chbi': None,
        'neighbor_std_chbi': None,
        'spatial_lag': None,
        'spatial_lag_zscore': None,
        'is_local_hotspot': 0,
        'is_local_coldspot': 0,
        'neighbor_improving_pct': None,
        'neighbor_declining_pct': None,
        'neighbor_avg_change': None,
    }

    # Get tract's own CHBI (use T-1, the prior year, to avoid temporal leakage)
    tract_data = tract_years.get(tract_id, {}).get(year - 1, {})
    tract_chbi = tract_data.get('CHBI')

    # Get neighbors
    tract_neighbors = neighbors.get(tract_id, set())
    features['n_neighbors'] = len(tract_neighbors)

    if not tract_neighbors:
        return features

    # Collect neighbor CHBI values
    neighbor_chbis = []
    neighbor_changes = []
    n_improving = 0
    n_declining = 0

    for neighbor_id in tract_neighbors:
        neighbor_data = tract_years.get(neighbor_id, {})
        # FIX: Use LAGGED data for neighbor change
        # For prediction year T, use neighbor's CHBI from year T-1 (not T)
        # and neighbor's change from T-2 to T-1 (not T-1 to T)
        prev = neighbor_data.get(year - 1, {}).get('CHBI')  # Neighbor CHBI at T-1
        prev2 = neighbor_data.get(year - 2, {}).get('CHBI')  # Neighbor CHBI at T-2

        if prev is not None:
            neighbor_chbis.append(prev)  # Use T-1 CHBI, not T

        # CRITICAL FIX: Compute LAGGED change (T-2 to T-1), not contemporaneous (T-1 to T)
        if prev is not None and prev2 is not None:
            change = prev - prev2  # Change from T-2 to T-1 (properly lagged)
            neighbor_changes.append(change)
            if change < -0.1:  # Improved (CHBI decreased)
                n_improving += 1
            elif change > 0.1:  # Declined (CHBI increased)
                n_declining += 1

    if neighbor_chbis:
        features['neighbor_avg_chbi'] = mean(neighbor_chbis)
        if len(neighbor_chbis) > 1:
            features['neighbor_std_chbi'] = stdev(neighbor_chbis)
        else:
            features['neighbor_std_chbi'] = 0.0

        # Spatial lag
        if tract_chbi is not None:
            features['spatial_lag'] = tract_chbi - features['neighbor_avg_chbi']

            # Standardize spatial lag using yearly stats
            if year in yearly_stats and yearly_stats[year]['std'] > 0:
                features['spatial_lag_zscore'] = features['spatial_lag'] / yearly_stats[year]['std']

            # Hot/cold spot detection
            threshold = 0.5 * (features['neighbor_std_chbi'] or yearly_stats.get(year, {}).get('std', 1))
            if features['spatial_lag'] > threshold:
                features['is_local_hotspot'] = 1
            elif features['spatial_lag'] < -threshold:
                features['is_local_coldspot'] = 1

    if neighbor_changes:
        features['neighbor_avg_change'] = mean(neighbor_changes)
        features['neighbor_improving_pct'] = n_improving / len(tract_neighbors)
        features['neighbor_declining_pct'] = n_declining / len(tract_neighbors)

    return features


def calculate_yearly_chbi_stats(tract_years: Dict) -> Dict[int, Dict]:
    """Calculate mean and std of CHBI for each year."""
    yearly_values = defaultdict(list)

    for tract_id, years in tract_years.items():
        for year, data in years.items():
            if data.get('CHBI') is not None:
                yearly_values[year].append(data['CHBI'])

    stats = {}
    for year, values in yearly_values.items():
        if values:
            stats[year] = {
                'mean': mean(values),
                'std': stdev(values) if len(values) > 1 else 1.0
            }

    return stats


def save_neighbor_graph(neighbors: Dict[str, Set[str]], output_path: Path):
    """Save neighbor graph to JSON for reuse."""
    # Convert sets to lists for JSON serialization
    serializable = {k: list(v) for k, v in neighbors.items()}
    with open(output_path, 'w') as f:
        json.dump(serializable, f)
    logger.info(f"Saved neighbor graph to {output_path}")


def load_neighbor_graph(input_path: Path) -> Optional[Dict[str, Set[str]]]:
    """Load pre-computed neighbor graph if it exists."""
    if not input_path.exists():
        return None

    logger.info(f"Loading cached neighbor graph from {input_path}")
    with open(input_path, 'r') as f:
        data = json.load(f)

    return {k: set(v) for k, v in data.items()}


def merge_with_rich_features():
    """
    Merge spatial features with the rich features dataset.
    """
    rich_features_path = PROCESSED_DATA_DIR / "prediction_dataset_rich.csv"
    output_path = PROCESSED_DATA_DIR / "prediction_dataset_spatial.csv"
    neighbor_cache_path = PROCESSED_DATA_DIR / "tract_neighbors.json"

    # Load or build neighbor graph
    neighbors = load_neighbor_graph(neighbor_cache_path)
    if neighbors is None:
        tracts = load_tract_geometries()
        neighbors = build_neighbor_graph(tracts)
        save_neighbor_graph(neighbors, neighbor_cache_path)

    # Load trajectory panel for CHBI values
    tract_years = load_trajectory_panel()
    yearly_stats = calculate_yearly_chbi_stats(tract_years)

    # Read rich features and add spatial features
    logger.info(f"Reading rich features from {rich_features_path}")

    rows = []
    spatial_feature_names = [
        'n_neighbors', 'neighbor_avg_chbi', 'neighbor_std_chbi',
        'spatial_lag', 'spatial_lag_zscore', 'is_local_hotspot',
        'is_local_coldspot', 'neighbor_improving_pct', 'neighbor_declining_pct',
        'neighbor_avg_change'
    ]

    with open(rich_features_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        original_fields = reader.fieldnames

        for row in reader:
            tract_id = row['TractFIPS']
            year = int(row['PredictionYear'])

            # Compute spatial features
            spatial_feats = compute_spatial_features(
                tract_id, year, neighbors, tract_years, yearly_stats
            )

            # Add to row
            for feat_name in spatial_feature_names:
                val = spatial_feats[feat_name]
                row[feat_name] = '' if val is None else val

            rows.append(row)

    # Write output
    output_fields = original_fields + spatial_feature_names

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=output_fields)
        writer.writeheader()
        writer.writerows(rows)

    logger.info(f"Wrote {len(rows):,} rows to {output_path}")

    # Print stats
    n_with_neighbors = sum(1 for r in rows if r.get('n_neighbors') and int(r['n_neighbors']) > 0)
    logger.info(f"Tracts with neighbors: {n_with_neighbors:,} ({100*n_with_neighbors/len(rows):.1f}%)")

    hotspots = sum(1 for r in rows if r.get('is_local_hotspot') == 1)
    coldspots = sum(1 for r in rows if r.get('is_local_coldspot') == 1)
    logger.info(f"Local hotspots: {hotspots:,}, Local coldspots: {coldspots:,}")


if __name__ == '__main__':
    merge_with_rich_features()
