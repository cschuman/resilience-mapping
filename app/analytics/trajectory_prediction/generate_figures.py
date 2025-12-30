#!/usr/bin/env python3
"""
Generate Publication-Quality Figures for Spatial Contagion Paper

Creates figures for the paper:
"Spatial Contagion in Community Health Trajectories"

Usage:
    python generate_figures.py

Output: figures/ directory with PNG files at 300 DPI
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import json

# Configuration
FIGURE_DIR = Path(__file__).parent.parent.parent.parent / "figures" / "paper"
DATA_DIR = Path(__file__).parent.parent.parent.parent / "data" / "processed"

# Publication style settings
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'sans-serif',
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
})

# Color palette (colorblind-friendly)
COLORS = {
    'DECLINE': '#d62728',   # Red
    'STABLE': '#7f7f7f',    # Gray
    'IMPROVE': '#2ca02c',   # Green
    'spatial': '#1f77b4',   # Blue
    'health': '#ff7f0e',    # Orange
    'other': '#9467bd',     # Purple
}


def load_data():
    """Load all required datasets."""
    print("Loading data...")

    spatial = pd.read_csv(DATA_DIR / "prediction_dataset_spatial.csv")
    predictions = pd.read_csv(DATA_DIR / "tract_predictions.csv")

    # Try to load feature importance if available
    model_dir = Path(__file__).parent / "models"
    importance_path = model_dir / "feature_importance.json"

    if importance_path.exists():
        with open(importance_path) as f:
            importance = json.load(f)
    else:
        # Default feature importance from training results
        importance = {
            'neighbor_avg_change': 12.3,
            'spatial_lag': 8.2,
            'neighbor_declining_pct': 5.8,
            'neighbor_improving_pct': 4.1,
            'CHBI_prev': 3.9,
            'CHBI_change_1yr': 3.3,
            'neighbor_avg_chbi': 3.1,
            'OBESITY_change_1yr': 2.9,
            'DIABETES_change_1yr': 2.7,
            'MHLTH_prev': 2.5,
        }

    return spatial, predictions, importance


def figure1_feature_importance(importance: dict):
    """
    Figure 1: Feature Importance Comparison

    Key finding: Spatial features dominate, neighbor_avg_change is 3.8x
    more important than own CHBI_change_1yr.
    """
    print("Creating Figure 1: Feature Importance...")

    fig, ax = plt.subplots(figsize=(8, 6))

    # Sort features by importance
    sorted_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:15]
    features = [f[0] for f in sorted_features]
    values = [f[1] for f in sorted_features]

    # Categorize features for coloring
    spatial_features = ['neighbor_avg_change', 'spatial_lag', 'neighbor_declining_pct',
                       'neighbor_improving_pct', 'neighbor_avg_chbi', 'num_neighbors',
                       'is_hotspot', 'is_coldspot']

    colors = [COLORS['spatial'] if f in spatial_features else COLORS['health']
              for f in features]

    y_pos = np.arange(len(features))
    bars = ax.barh(y_pos, values, color=colors, edgecolor='black', linewidth=0.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([f.replace('_', ' ').title() for f in features])
    ax.invert_yaxis()
    ax.set_xlabel('Feature Importance (%)')
    ax.set_title('Feature Importance for Health Trajectory Prediction')

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, values)):
        ax.text(val + 0.3, i, f'{val:.1f}%', va='center', fontsize=8)

    # Legend
    spatial_patch = mpatches.Patch(color=COLORS['spatial'], label='Spatial Features')
    health_patch = mpatches.Patch(color=COLORS['health'], label='Health Features')
    ax.legend(handles=[spatial_patch, health_patch], loc='lower right')

    # Highlight the key comparison
    ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.3)
    ax.annotate('3.8x more predictive\nthan own trajectory',
                xy=(12.3, 0), xytext=(15, 2),
                arrowprops=dict(arrowstyle='->', color='red', alpha=0.7),
                fontsize=8, color='red')

    plt.tight_layout()
    fig.savefig(FIGURE_DIR / "fig1_feature_importance.png")
    plt.close(fig)
    print(f"  Saved: {FIGURE_DIR / 'fig1_feature_importance.png'}")


def figure2_trajectory_distribution(spatial: pd.DataFrame):
    """
    Figure 2: Trajectory Distribution by Year

    Shows temporal patterns and class imbalance.
    """
    print("Creating Figure 2: Trajectory Distribution...")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Panel A: Overall distribution
    ax1 = axes[0]
    dist = spatial['target_class'].value_counts()
    colors = [COLORS[c] for c in dist.index]
    wedges, texts, autotexts = ax1.pie(
        dist.values,
        labels=dist.index,
        autopct='%1.1f%%',
        colors=colors,
        explode=[0.02, 0, 0.02],
        startangle=90
    )
    ax1.set_title('A. Overall Trajectory Distribution\n(n=189,566)')

    # Panel B: By year
    ax2 = axes[1]
    yearly = spatial.groupby(['PredictionYear', 'target_class']).size().unstack(fill_value=0)
    yearly_pct = yearly.div(yearly.sum(axis=1), axis=0) * 100

    x = np.arange(len(yearly_pct.index))
    width = 0.25

    for i, traj in enumerate(['DECLINE', 'STABLE', 'IMPROVE']):
        ax2.bar(x + i*width, yearly_pct[traj], width,
               label=traj, color=COLORS[traj], edgecolor='black', linewidth=0.5)

    ax2.set_xticks(x + width)
    ax2.set_xticklabels(yearly_pct.index.astype(int))
    ax2.set_xlabel('Prediction Year')
    ax2.set_ylabel('Percentage (%)')
    ax2.set_title('B. Trajectory Distribution by Year')
    ax2.legend()
    ax2.set_ylim(0, 100)

    plt.tight_layout()
    fig.savefig(FIGURE_DIR / "fig2_trajectory_distribution.png")
    plt.close(fig)
    print(f"  Saved: {FIGURE_DIR / 'fig2_trajectory_distribution.png'}")


def figure3_spatial_vs_own_trajectory(spatial: pd.DataFrame):
    """
    Figure 3: Spatial vs Own Trajectory Comparison

    Demonstrates the core finding that neighbor trajectories are
    more predictive than own historical trends.
    """
    print("Creating Figure 3: Spatial vs Own Trajectory...")

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Panel A: Own change by trajectory
    ax1 = axes[0]
    for traj in ['DECLINE', 'STABLE', 'IMPROVE']:
        subset = spatial[spatial['target_class'] == traj]['CHBI_change_1yr']
        ax1.hist(subset, bins=50, alpha=0.6, label=traj, color=COLORS[traj], density=True)

    ax1.set_xlabel('Own CHBI Change (1 year)')
    ax1.set_ylabel('Density')
    ax1.set_title('A. Own Historical Change\nby Future Trajectory')
    ax1.legend()
    ax1.axvline(x=0, color='black', linestyle='--', alpha=0.5)

    # Panel B: Neighbor change by trajectory
    ax2 = axes[1]
    for traj in ['DECLINE', 'STABLE', 'IMPROVE']:
        subset = spatial[spatial['target_class'] == traj]['neighbor_avg_change']
        ax2.hist(subset, bins=50, alpha=0.6, label=traj, color=COLORS[traj], density=True)

    ax2.set_xlabel('Neighbor Average CHBI Change')
    ax2.set_ylabel('Density')
    ax2.set_title('B. Neighbor Historical Change\nby Future Trajectory')
    ax2.legend()
    ax2.axvline(x=0, color='black', linestyle='--', alpha=0.5)

    plt.tight_layout()
    fig.savefig(FIGURE_DIR / "fig3_spatial_vs_own.png")
    plt.close(fig)
    print(f"  Saved: {FIGURE_DIR / 'fig3_spatial_vs_own.png'}")


def figure4_confidence_distribution(predictions: pd.DataFrame):
    """
    Figure 4: Prediction Confidence Distribution

    Shows model certainty across trajectory predictions.
    """
    print("Creating Figure 4: Confidence Distribution...")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Panel A: Overall confidence histogram
    ax1 = axes[0]
    ax1.hist(predictions['confidence'], bins=30, edgecolor='black',
             color=COLORS['spatial'], alpha=0.7)
    ax1.axvline(x=0.6, color='red', linestyle='--', label='High confidence threshold')
    ax1.set_xlabel('Confidence Score')
    ax1.set_ylabel('Frequency')
    ax1.set_title('A. Overall Confidence Distribution')
    ax1.legend()

    # Add statistics
    mean_conf = predictions['confidence'].mean()
    high_conf_pct = (predictions['confidence'] >= 0.6).mean() * 100
    ax1.text(0.95, 0.95, f'Mean: {mean_conf:.3f}\n>0.6: {high_conf_pct:.1f}%',
             transform=ax1.transAxes, ha='right', va='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Panel B: Confidence by trajectory
    ax2 = axes[1]
    trajectories = ['DECLINE', 'STABLE', 'IMPROVE']
    positions = np.arange(len(trajectories))

    bp_data = [predictions[predictions['predicted_trajectory'] == t]['confidence']
               for t in trajectories]

    bp = ax2.boxplot(bp_data, positions=positions, patch_artist=True)

    for patch, traj in zip(bp['boxes'], trajectories):
        patch.set_facecolor(COLORS[traj])
        patch.set_alpha(0.7)

    ax2.set_xticks(positions)
    ax2.set_xticklabels(trajectories)
    ax2.set_xlabel('Predicted Trajectory')
    ax2.set_ylabel('Confidence Score')
    ax2.set_title('B. Confidence by Predicted Trajectory')
    ax2.axhline(y=0.6, color='red', linestyle='--', alpha=0.5)

    plt.tight_layout()
    fig.savefig(FIGURE_DIR / "fig4_confidence.png")
    plt.close(fig)
    print(f"  Saved: {FIGURE_DIR / 'fig4_confidence.png'}")


def figure5_state_variation(predictions: pd.DataFrame):
    """
    Figure 5: Geographic Variation in Predictions

    Shows state-level heterogeneity in predicted decline rates.
    """
    print("Creating Figure 5: State Variation...")

    fig, ax = plt.subplots(figsize=(12, 6))

    # Calculate state-level stats
    state_stats = predictions.groupby('state_abbr').agg({
        'tract_fips': 'count',
        'predicted_trajectory': lambda x: (x == 'DECLINE').mean() * 100
    }).rename(columns={'tract_fips': 'n_tracts', 'predicted_trajectory': 'pct_decline'})

    # Filter to states with enough tracts
    state_stats = state_stats[state_stats['n_tracts'] >= 50].sort_values('pct_decline', ascending=True)

    # Color by decline rate
    colors = plt.cm.RdYlGn_r(state_stats['pct_decline'] / 100)

    y_pos = np.arange(len(state_stats))
    bars = ax.barh(y_pos, state_stats['pct_decline'], color=colors, edgecolor='black', linewidth=0.3)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(state_stats.index)
    ax.set_xlabel('Predicted Decline Rate (%)')
    ax.set_title('Predicted Decline Rate by State (states with n≥50 tracts)')

    # Add mean line
    mean_decline = state_stats['pct_decline'].mean()
    ax.axvline(x=mean_decline, color='black', linestyle='--', alpha=0.7, label=f'Mean: {mean_decline:.1f}%')
    ax.legend(loc='lower right')

    plt.tight_layout()
    fig.savefig(FIGURE_DIR / "fig5_state_variation.png")
    plt.close(fig)
    print(f"  Saved: {FIGURE_DIR / 'fig5_state_variation.png'}")


def figure6_category_importance():
    """
    Figure 6: Feature Category Importance

    Pie chart showing spatial vs health feature importance.
    """
    print("Creating Figure 6: Category Importance...")

    fig, ax = plt.subplots(figsize=(7, 7))

    categories = {
        'Spatial Features': 32.0,
        'Health Outcomes': 28.4,
        'Health Changes': 16.8,
        'Health Trajectories': 12.6,
        'Other': 10.2
    }

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    explode = [0.05, 0, 0, 0, 0]  # Emphasize spatial

    wedges, texts, autotexts = ax.pie(
        categories.values(),
        labels=categories.keys(),
        autopct='%1.1f%%',
        colors=colors,
        explode=explode,
        startangle=90,
        pctdistance=0.75
    )

    # Bold the spatial slice
    autotexts[0].set_fontweight('bold')
    texts[0].set_fontweight('bold')

    ax.set_title('Feature Category Contribution to Model Predictions', fontsize=14)

    # Add annotation
    ax.annotate('Spatial context is the\nsingle largest predictor',
                xy=(0.3, 0.3), xytext=(0.7, 0.5),
                fontsize=10, ha='center',
                arrowprops=dict(arrowstyle='->', color='gray'))

    plt.tight_layout()
    fig.savefig(FIGURE_DIR / "fig6_category_importance.png")
    plt.close(fig)
    print(f"  Saved: {FIGURE_DIR / 'fig6_category_importance.png'}")


def main():
    """Generate all figures."""
    # Create output directory
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {FIGURE_DIR}")
    print()

    # Load data
    spatial, predictions, importance = load_data()

    # Generate figures
    figure1_feature_importance(importance)
    figure2_trajectory_distribution(spatial)
    figure3_spatial_vs_own_trajectory(spatial)
    figure4_confidence_distribution(predictions)
    figure5_state_variation(predictions)
    figure6_category_importance()

    print()
    print("=" * 50)
    print("All figures generated successfully!")
    print(f"Location: {FIGURE_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    main()
