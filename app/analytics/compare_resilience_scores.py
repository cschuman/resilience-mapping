#!/usr/bin/env python3
"""
Compare Old vs New Resilience Scores

This script compares resilience scores before and after the bug fix to:
1. Quantify the impact of the state fixed effects bug
2. Identify tracts that changed classification
3. Generate a comprehensive comparison report

Usage:
    python compare_resilience_scores.py [old_scores.csv] [new_scores.csv]
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Optional
import matplotlib.pyplot as plt
import seaborn as sns


def load_scores(
    old_path: str = 'data/processed/model_table_with_residuals.csv',
    new_path: str = 'data/processed/model_table_corrected.csv'
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load old and new resilience score files.

    Args:
        old_path: Path to original (buggy) scores
        new_path: Path to corrected scores

    Returns:
        Tuple of (old_scores, new_scores)
    """
    print("Loading score files...")

    try:
        old_scores = pd.read_csv(old_path)
        print(f"  Old scores: {len(old_scores):,} tracts")
    except FileNotFoundError:
        print(f"  WARNING: Could not find {old_path}")
        old_scores = None

    try:
        new_scores = pd.read_csv(new_path)
        print(f"  New scores: {len(new_scores):,} tracts")
    except FileNotFoundError:
        print(f"  WARNING: Could not find {new_path}")
        new_scores = None

    return old_scores, new_scores


def classify_tracts(scores: pd.DataFrame, score_col: str = 'resilience_score') -> pd.Series:
    """
    Classify tracts as resilient, expected, or vulnerable.

    Args:
        scores: DataFrame with resilience scores
        score_col: Name of the score column

    Returns:
        Series with classifications
    """
    def classify(score):
        if score > 1.645:
            return 'resilient'
        elif score < -1.645:
            return 'vulnerable'
        else:
            return 'expected'

    return scores[score_col].apply(classify)


def compare_distributions(old: pd.DataFrame, new: pd.DataFrame) -> Dict:
    """
    Compare score distributions between old and new.

    Args:
        old: Old scores DataFrame
        new: New scores DataFrame

    Returns:
        Dictionary with comparison statistics
    """
    stats = {
        'old': {
            'mean': old['resilience_score'].mean(),
            'std': old['resilience_score'].std(),
            'min': old['resilience_score'].min(),
            'max': old['resilience_score'].max(),
            'n_resilient': (old['resilience_score'] > 1.645).sum(),
            'n_vulnerable': (old['resilience_score'] < -1.645).sum(),
        },
        'new': {
            'mean': new['resilience_score'].mean(),
            'std': new['resilience_score'].std(),
            'min': new['resilience_score'].min(),
            'max': new['resilience_score'].max(),
            'n_resilient': (new['resilience_score'] > 1.645).sum(),
            'n_vulnerable': (new['resilience_score'] < -1.645).sum(),
        }
    }

    # Calculate changes
    stats['change'] = {
        'mean_diff': stats['new']['mean'] - stats['old']['mean'],
        'std_diff': stats['new']['std'] - stats['old']['std'],
        'resilient_diff': stats['new']['n_resilient'] - stats['old']['n_resilient'],
        'vulnerable_diff': stats['new']['n_vulnerable'] - stats['old']['n_vulnerable'],
    }

    return stats


def identify_changed_tracts(
    old: pd.DataFrame,
    new: pd.DataFrame,
    tract_col: str = 'TractFIPS'
) -> Tuple[pd.DataFrame, Dict]:
    """
    Identify tracts that changed classification.

    Args:
        old: Old scores DataFrame
        new: New scores DataFrame
        tract_col: Column name for tract identifier

    Returns:
        Tuple of (merged_df, change_summary)
    """
    # Standardize tract IDs
    old = old.copy()
    new = new.copy()
    old[tract_col] = old[tract_col].astype(str).str.zfill(11)
    new[tract_col] = new[tract_col].astype(str).str.zfill(11)

    # Add classifications
    old['old_class'] = classify_tracts(old)
    new['new_class'] = classify_tracts(new)

    # Merge
    merged = old[[tract_col, 'StateAbbr', 'burden', 'resilience_score', 'old_class']].merge(
        new[[tract_col, 'resilience_score', 'new_class']],
        on=tract_col,
        how='inner',
        suffixes=('_old', '_new')
    )

    # Calculate score change
    merged['score_change'] = merged['resilience_score_new'] - merged['resilience_score_old']
    merged['abs_change'] = merged['score_change'].abs()

    # Identify classification changes
    merged['class_changed'] = merged['old_class'] != merged['new_class']

    # Specific transitions
    merged['became_resilient'] = (merged['old_class'] != 'resilient') & (merged['new_class'] == 'resilient')
    merged['lost_resilient'] = (merged['old_class'] == 'resilient') & (merged['new_class'] != 'resilient')
    merged['became_vulnerable'] = (merged['old_class'] != 'vulnerable') & (merged['new_class'] == 'vulnerable')
    merged['lost_vulnerable'] = (merged['old_class'] == 'vulnerable') & (merged['new_class'] != 'vulnerable')

    # Summary
    change_summary = {
        'total_tracts': len(merged),
        'tracts_matched': len(merged),
        'classification_changed': merged['class_changed'].sum(),
        'became_resilient': merged['became_resilient'].sum(),
        'lost_resilient': merged['lost_resilient'].sum(),
        'became_vulnerable': merged['became_vulnerable'].sum(),
        'lost_vulnerable': merged['lost_vulnerable'].sum(),
        'mean_score_change': merged['score_change'].mean(),
        'median_score_change': merged['score_change'].median(),
        'max_increase': merged['score_change'].max(),
        'max_decrease': merged['score_change'].min(),
        'correlation': merged['resilience_score_old'].corr(merged['resilience_score_new']),
    }

    return merged, change_summary


def identify_top_changes(
    merged: pd.DataFrame,
    n: int = 50
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Identify tracts with largest score changes.

    Args:
        merged: Merged comparison DataFrame
        n: Number of top tracts to return

    Returns:
        Tuple of (top_increases, top_decreases, new_resilient, lost_resilient)
    """
    # Sort by change magnitude
    top_increases = merged.nlargest(n, 'score_change')
    top_decreases = merged.nsmallest(n, 'score_change')

    # Tracts that became resilient
    new_resilient = merged[merged['became_resilient']].nlargest(n, 'resilience_score_new')

    # Tracts that lost resilient status
    lost_resilient = merged[merged['lost_resilient']].nlargest(n, 'resilience_score_old')

    return top_increases, top_decreases, new_resilient, lost_resilient


def analyze_state_patterns(merged: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze how score changes vary by state.

    Args:
        merged: Merged comparison DataFrame

    Returns:
        DataFrame with state-level summary
    """
    state_summary = merged.groupby('StateAbbr').agg({
        'score_change': ['mean', 'std', 'min', 'max'],
        'class_changed': 'sum',
        'became_resilient': 'sum',
        'lost_resilient': 'sum',
        'resilience_score_old': 'count'
    }).round(4)

    state_summary.columns = [
        'mean_change', 'std_change', 'min_change', 'max_change',
        'n_class_changed', 'n_became_resilient', 'n_lost_resilient', 'n_tracts'
    ]

    # Calculate percent changed
    state_summary['pct_changed'] = (
        state_summary['n_class_changed'] / state_summary['n_tracts'] * 100
    ).round(1)

    return state_summary.sort_values('mean_change', ascending=False)


def create_comparison_visualizations(
    merged: pd.DataFrame,
    output_dir: str = 'figures'
) -> None:
    """
    Create visualization comparing old and new scores.

    Args:
        merged: Merged comparison DataFrame
        output_dir: Directory for output figures
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 1. Scatter plot: old vs new scores
    ax1 = axes[0, 0]
    colors = merged['class_changed'].map({True: 'red', False: 'blue'})
    ax1.scatter(
        merged['resilience_score_old'],
        merged['resilience_score_new'],
        c=colors, alpha=0.3, s=5
    )
    ax1.plot([-5, 5], [-5, 5], 'k--', linewidth=1, label='No change')
    ax1.axhline(1.645, color='green', linestyle=':', alpha=0.7, label='Resilient threshold')
    ax1.axhline(-1.645, color='orange', linestyle=':', alpha=0.7, label='Vulnerable threshold')
    ax1.axvline(1.645, color='green', linestyle=':', alpha=0.7)
    ax1.axvline(-1.645, color='orange', linestyle=':', alpha=0.7)
    ax1.set_xlabel('Old Resilience Score (Buggy)')
    ax1.set_ylabel('New Resilience Score (Corrected)')
    ax1.set_title('Old vs New Resilience Scores\n(Red = Changed Classification)')
    ax1.legend(loc='upper left')
    ax1.set_xlim(-5, 5)
    ax1.set_ylim(-5, 5)

    # 2. Distribution of score changes
    ax2 = axes[0, 1]
    ax2.hist(merged['score_change'], bins=100, edgecolor='black', alpha=0.7)
    ax2.axvline(0, color='red', linestyle='--', linewidth=2, label='No change')
    ax2.axvline(merged['score_change'].mean(), color='green', linestyle='-',
                linewidth=2, label=f'Mean: {merged["score_change"].mean():.3f}')
    ax2.set_xlabel('Score Change (New - Old)')
    ax2.set_ylabel('Number of Tracts')
    ax2.set_title('Distribution of Score Changes')
    ax2.legend()

    # 3. Classification transition matrix
    ax3 = axes[1, 0]
    transition_matrix = pd.crosstab(
        merged['old_class'],
        merged['new_class'],
        margins=True
    )
    # Reorder for logical display
    order = ['vulnerable', 'expected', 'resilient', 'All']
    transition_matrix = transition_matrix.reindex(
        index=[x for x in order if x in transition_matrix.index],
        columns=[x for x in order if x in transition_matrix.columns]
    )
    sns.heatmap(
        transition_matrix,
        annot=True, fmt='d', cmap='Blues', ax=ax3
    )
    ax3.set_xlabel('New Classification')
    ax3.set_ylabel('Old Classification')
    ax3.set_title('Classification Transition Matrix')

    # 4. State-level mean changes
    ax4 = axes[1, 1]
    state_means = merged.groupby('StateAbbr')['score_change'].mean().sort_values()
    top_states = pd.concat([state_means.head(10), state_means.tail(10)])
    colors = ['red' if x < 0 else 'green' for x in top_states.values]
    ax4.barh(range(len(top_states)), top_states.values, color=colors, alpha=0.7)
    ax4.set_yticks(range(len(top_states)))
    ax4.set_yticklabels(top_states.index)
    ax4.axvline(0, color='black', linewidth=1)
    ax4.set_xlabel('Mean Score Change')
    ax4.set_title('States with Largest Score Changes\n(Top/Bottom 10)')

    plt.tight_layout()
    output_path = f'{output_dir}/score_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_path}")

    plt.close()


def generate_comparison_report(
    old: pd.DataFrame,
    new: pd.DataFrame,
    output_path: str = 'data/processed/comparison_report.md'
) -> str:
    """
    Generate a comprehensive Markdown comparison report.

    Args:
        old: Old scores DataFrame
        new: New scores DataFrame
        output_path: Path for output report

    Returns:
        Report content as string
    """
    # Get comparison data
    dist_stats = compare_distributions(old, new)
    merged, change_summary = identify_changed_tracts(old, new)
    top_increases, top_decreases, new_resilient, lost_resilient = identify_top_changes(merged)
    state_patterns = analyze_state_patterns(merged)

    report = f"""# Resilience Score Comparison Report
## State Fixed Effects Bug Fix Analysis

**Generated**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

---

## Executive Summary

The state fixed effects bug in `app/backend/expected.go` caused systematic errors in resilience score calculations. This report quantifies the impact of the bug fix.

### Key Findings

| Metric | Old (Buggy) | New (Corrected) | Change |
|--------|-------------|-----------------|--------|
| Mean Score | {dist_stats['old']['mean']:.4f} | {dist_stats['new']['mean']:.4f} | {dist_stats['change']['mean_diff']:+.4f} |
| Std Dev | {dist_stats['old']['std']:.4f} | {dist_stats['new']['std']:.4f} | {dist_stats['change']['std_diff']:+.4f} |
| Resilient Tracts | {dist_stats['old']['n_resilient']:,} | {dist_stats['new']['n_resilient']:,} | {dist_stats['change']['resilient_diff']:+,} |
| Vulnerable Tracts | {dist_stats['old']['n_vulnerable']:,} | {dist_stats['new']['n_vulnerable']:,} | {dist_stats['change']['vulnerable_diff']:+,} |

### Classification Changes

- **Total tracts analyzed**: {change_summary['total_tracts']:,}
- **Tracts that changed classification**: {change_summary['classification_changed']:,} ({change_summary['classification_changed']/change_summary['total_tracts']*100:.1f}%)
- **Correlation between old and new scores**: {change_summary['correlation']:.4f}

### Classification Transitions

| Transition | Count |
|------------|-------|
| Became Resilient | {change_summary['became_resilient']:,} |
| Lost Resilient Status | {change_summary['lost_resilient']:,} |
| Became Vulnerable | {change_summary['became_vulnerable']:,} |
| Lost Vulnerable Status | {change_summary['lost_vulnerable']:,} |

---

## Detailed Analysis

### Score Change Distribution

- **Mean change**: {change_summary['mean_score_change']:.4f}
- **Median change**: {change_summary['median_score_change']:.4f}
- **Maximum increase**: {change_summary['max_increase']:.4f}
- **Maximum decrease**: {change_summary['max_decrease']:.4f}

### Top 10 Tracts with Largest Score INCREASES

| Tract | State | Old Score | New Score | Change |
|-------|-------|-----------|-----------|--------|
"""

    for _, row in top_increases.head(10).iterrows():
        report += f"| {row['TractFIPS']} | {row['StateAbbr']} | {row['resilience_score_old']:.3f} | {row['resilience_score_new']:.3f} | {row['score_change']:+.3f} |\n"

    report += """
### Top 10 Tracts with Largest Score DECREASES

| Tract | State | Old Score | New Score | Change |
|-------|-------|-----------|-----------|--------|
"""

    for _, row in top_decreases.head(10).iterrows():
        report += f"| {row['TractFIPS']} | {row['StateAbbr']} | {row['resilience_score_old']:.3f} | {row['resilience_score_new']:.3f} | {row['score_change']:+.3f} |\n"

    report += """
### Newly Classified as Resilient (Top 10)

| Tract | State | Old Classification | New Score |
|-------|-------|-------------------|-----------|
"""

    for _, row in new_resilient.head(10).iterrows():
        report += f"| {row['TractFIPS']} | {row['StateAbbr']} | {row['old_class']} | {row['resilience_score_new']:.3f} |\n"

    report += """
### Lost Resilient Status (Top 10)

| Tract | State | Old Score | New Classification |
|-------|-------|-----------|-------------------|
"""

    for _, row in lost_resilient.head(10).iterrows():
        report += f"| {row['TractFIPS']} | {row['StateAbbr']} | {row['resilience_score_old']:.3f} | {row['new_class']} |\n"

    report += """
---

## State-Level Analysis

### States with Largest Mean Score Changes

| State | Mean Change | Std Change | % Tracts Changed | N Tracts |
|-------|-------------|------------|------------------|----------|
"""

    for state, row in state_patterns.head(10).iterrows():
        report += f"| {state} | {row['mean_change']:+.4f} | {row['std_change']:.4f} | {row['pct_changed']:.1f}% | {row['n_tracts']:,} |\n"

    report += f"""
---

## Implications

1. **The bug systematically affected state-level comparisons**: States with larger absolute mean changes had more systematic bias in the original analysis.

2. **{change_summary['classification_changed']:,} tracts changed classification**: This represents {change_summary['classification_changed']/change_summary['total_tracts']*100:.1f}% of all tracts.

3. **{change_summary['lost_resilient']:,} tracts lost "resilient" status**: These communities were incorrectly classified in the original analysis.

4. **{change_summary['became_resilient']:,} tracts gained "resilient" status**: These communities were previously overlooked.

---

## Recommendations

1. **Re-validate top communities**: Manually review the top 100 resilient tracts in the new analysis.
2. **Update all derived analyses**: Any downstream analysis using the old scores must be re-run.
3. **Document methodology change**: All publications must note the correction.

---

*Report generated by compare_resilience_scores.py*
*Bug fix applied: December 24, 2025*
"""

    # Save report
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(report)
    print(f"Saved: {output_path}")

    return report


def main(
    old_path: str = 'data/processed/model_table_with_residuals.csv',
    new_path: str = 'data/processed/model_table_corrected.csv'
):
    """
    Run complete comparison analysis.

    Args:
        old_path: Path to original (buggy) scores
        new_path: Path to corrected scores
    """
    print("=" * 60)
    print("RESILIENCE SCORE COMPARISON")
    print("State Fixed Effects Bug Fix Analysis")
    print("=" * 60)

    # Load data
    old, new = load_scores(old_path, new_path)

    if old is None or new is None:
        print("\nERROR: Could not load score files. Please ensure both files exist.")
        print("Run the corrected model first: python resilience_model.py")
        return

    # Compare distributions
    print("\n" + "=" * 40)
    print("DISTRIBUTION COMPARISON")
    print("=" * 40)
    dist_stats = compare_distributions(old, new)

    print(f"\nOld (Buggy) Statistics:")
    for key, value in dist_stats['old'].items():
        print(f"  {key}: {value:,.4f}" if isinstance(value, float) else f"  {key}: {value:,}")

    print(f"\nNew (Corrected) Statistics:")
    for key, value in dist_stats['new'].items():
        print(f"  {key}: {value:,.4f}" if isinstance(value, float) else f"  {key}: {value:,}")

    # Identify changes
    print("\n" + "=" * 40)
    print("CLASSIFICATION CHANGES")
    print("=" * 40)
    merged, change_summary = identify_changed_tracts(old, new)

    print(f"\nChange Summary:")
    for key, value in change_summary.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value:,}")

    # Save merged comparison
    merged.to_csv('data/processed/score_comparison.csv', index=False)
    print("\nSaved: data/processed/score_comparison.csv")

    # State analysis
    print("\n" + "=" * 40)
    print("STATE-LEVEL PATTERNS")
    print("=" * 40)
    state_patterns = analyze_state_patterns(merged)
    print("\nTop 10 states by mean score change:")
    print(state_patterns.head(10)[['mean_change', 'n_class_changed', 'pct_changed', 'n_tracts']])

    state_patterns.to_csv('data/processed/state_change_analysis.csv')
    print("\nSaved: data/processed/state_change_analysis.csv")

    # Create visualizations
    print("\n" + "=" * 40)
    print("CREATING VISUALIZATIONS")
    print("=" * 40)
    try:
        create_comparison_visualizations(merged)
    except Exception as e:
        print(f"  WARNING: Could not create visualizations: {e}")

    # Generate report
    print("\n" + "=" * 40)
    print("GENERATING REPORT")
    print("=" * 40)
    generate_comparison_report(old, new)

    print("\n" + "=" * 60)
    print("COMPARISON COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    import sys

    old_path = sys.argv[1] if len(sys.argv) > 1 else 'data/processed/model_table_with_residuals.csv'
    new_path = sys.argv[2] if len(sys.argv) > 2 else 'data/processed/model_table_corrected.csv'

    main(old_path, new_path)
