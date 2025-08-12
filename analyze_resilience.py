#!/usr/bin/env python3
"""
Comprehensive resilience analysis for research paper
Implements missing components from original vision
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Set style for publication-quality figures
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_data():
    """Load PLACES and FARA data"""
    print("Loading data...")
    
    # Load FARA data
    fara = pd.read_csv('data/interim/fara_2019.csv')
    print(f"FARA data: {fara.shape[0]} tracts")
    
    # Load PLACES data
    places = pd.read_csv('data/raw/places_tract.csv')
    print(f"PLACES data: {places.shape[0]} records")
    
    # Load model results
    results = pd.read_csv('data/processed/model_table_with_residuals.csv')
    print(f"Model results: {results.shape[0]} tracts")
    
    return fara, places, results

def analyze_places_outcomes(places):
    """Analyze which health outcomes are included"""
    print("\n=== PLACES Health Outcomes Analysis ===")
    
    # Key outcomes from original vision
    target_outcomes = ['OBESITY', 'DIABETES', 'CHD', 'BPHIGH', 'LPA']
    
    # Check available outcomes
    outcome_counts = places.groupby('MeasureId').size().sort_values(ascending=False)
    print(f"\nTop 10 health outcomes by frequency:")
    print(outcome_counts.head(10))
    
    # Check for target outcomes
    print("\nTarget outcomes availability:")
    for outcome in target_outcomes:
        if outcome in outcome_counts.index:
            print(f"  {outcome}: {outcome_counts[outcome]} records")
        else:
            print(f"  {outcome}: NOT FOUND")
    
    return outcome_counts

def analyze_confidence_intervals(places):
    """Analyze confidence intervals in PLACES data"""
    print("\n=== Confidence Interval Analysis ===")
    
    # Filter to key outcomes
    key_outcomes = ['OBESITY', 'DIABETES', 'CHD']
    places_key = places[places['MeasureId'].isin(key_outcomes)].copy()
    
    # Calculate CI width
    places_key['CI_width'] = places_key['High_Confidence_Limit'] - places_key['Low_Confidence_Limit']
    
    # Summary statistics
    print("\nCI width statistics by outcome:")
    ci_stats = places_key.groupby('MeasureId')['CI_width'].describe()
    print(ci_stats)
    
    # Identify high uncertainty tracts
    high_uncertainty = places_key[places_key['CI_width'] > places_key['CI_width'].quantile(0.9)]
    print(f"\nTracts with high uncertainty (top 10%): {high_uncertainty['LocationID'].nunique()}")
    
    return places_key

def analyze_lila_thresholds(fara):
    """Analyze different LILA threshold definitions"""
    print("\n=== LILA Threshold Analysis ===")
    
    # LILA columns
    lila_cols = ['LILATracts_1And10', 'LILATracts_halfAnd10', 'LILATracts_1And20', 'LILATracts_Vehicle']
    
    # Convert to numeric (handle NULL values)
    for col in lila_cols:
        fara[col] = pd.to_numeric(fara[col], errors='coerce')
    
    # Summary statistics
    print("\nLILA prevalence by threshold:")
    for col in lila_cols:
        prevalence = fara[col].mean() * 100
        count = fara[col].sum()
        print(f"  {col}: {prevalence:.1f}% ({int(count)} tracts)")
    
    # Overlap analysis
    print("\nOverlap between LILA definitions:")
    overlap_matrix = pd.DataFrame(index=lila_cols, columns=lila_cols)
    for i, col1 in enumerate(lila_cols):
        for j, col2 in enumerate(lila_cols):
            if i <= j:
                overlap = ((fara[col1] == 1) & (fara[col2] == 1)).sum()
                overlap_matrix.loc[col1, col2] = overlap
    print(overlap_matrix)
    
    return lila_cols

def perform_sensitivity_analysis(fara, results):
    """Run sensitivity analysis across LILA thresholds"""
    print("\n=== Sensitivity Analysis Across LILA Thresholds ===")
    
    # Merge data - ensure both GEOIDs are strings
    fara['GEOID'] = fara['CensusTract'].astype(str).str.zfill(11)
    results['GEOID'] = results['GEOID'].astype(str).str.zfill(11)
    merged = results.merge(fara[['GEOID', 'LILATracts_1And10', 'LILATracts_halfAnd10', 
                                  'LILATracts_1And20', 'LILATracts_Vehicle']], 
                           on='GEOID', how='left')
    
    # Analyze resilience by LILA status
    lila_cols = ['LILATracts_1And10', 'LILATracts_halfAnd10', 'LILATracts_1And20']
    
    sensitivity_results = []
    for col in lila_cols:
        # Filter to LILA tracts
        lila_tracts = merged[merged[col] == 1]
        
        # Identify resilient (top 10%)
        threshold = lila_tracts['resilience_score'].quantile(0.9)
        resilient = lila_tracts[lila_tracts['resilience_score'] > threshold]
        
        sensitivity_results.append({
            'threshold': col,
            'n_lila': len(lila_tracts),
            'n_resilient': len(resilient),
            'pct_resilient': len(resilient) / len(lila_tracts) * 100,
            'mean_resilience': lila_tracts['resilience_score'].mean(),
            'std_resilience': lila_tracts['resilience_score'].std()
        })
    
    sensitivity_df = pd.DataFrame(sensitivity_results)
    print("\nResilience by LILA threshold:")
    print(sensitivity_df)
    
    return merged, sensitivity_df

def generate_descriptive_statistics(fara, places, results):
    """Generate comprehensive descriptive statistics for paper"""
    print("\n=== Descriptive Statistics for Paper ===")
    
    # Overall sample
    print(f"\nTotal census tracts analyzed: {len(results):,}")
    
    # Geographic coverage
    state_coverage = results['StateAbbr'].nunique()
    print(f"States covered: {state_coverage}")
    
    # Health burden distribution
    print("\nHealth burden distribution:")
    burden_stats = results['burden'].describe()
    print(burden_stats)
    
    # Resilience score distribution
    print("\nResilience score distribution:")
    resilience_stats = results['resilience_score'].describe()
    print(resilience_stats)
    
    # Top resilient tracts
    top_resilient = results.nlargest(30, 'resilience_score')
    print(f"\nTop 30 resilient tracts:")
    print(top_resilient[['TractFIPS', 'StateAbbr', 'burden', 'resilience_score']].head(10))
    
    # State distribution of resilient tracts
    print("\nResilience by state (top 10):")
    state_resilience = top_resilient.groupby('StateAbbr').size().sort_values(ascending=False).head(10)
    print(state_resilience)
    
    return burden_stats, resilience_stats, top_resilient

def create_visualizations(merged, results):
    """Create missing visualizations for paper"""
    print("\n=== Creating Visualizations ===")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Scatter plot: Food access vs health burden with LOESS
    ax1 = axes[0, 0]
    lila_status = merged['LILATracts_1And10'].fillna(0)
    colors = ['blue' if x == 0 else 'red' for x in lila_status]
    ax1.scatter(merged['burden'], merged['resilience_score'], 
                c=colors, alpha=0.3, s=10)
    
    # Add LOESS smoothing
    from scipy.signal import savgol_filter
    sorted_idx = np.argsort(merged['burden'].dropna())
    burden_sorted = merged['burden'].dropna().iloc[sorted_idx]
    resilience_sorted = merged['resilience_score'].dropna().iloc[sorted_idx]
    
    # Simple moving average as LOESS approximation
    window = 100
    smooth_resilience = pd.Series(resilience_sorted.values).rolling(window, center=True).mean()
    ax1.plot(burden_sorted, smooth_resilience, 'green', linewidth=2, label='Smoothed trend')
    
    ax1.set_xlabel('Health Burden (z-score)')
    ax1.set_ylabel('Resilience Score')
    ax1.set_title('Health Burden vs Resilience\n(Red = LILA tracts, Blue = Non-LILA)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Distribution of resilience scores
    ax2 = axes[0, 1]
    ax2.hist(results['resilience_score'], bins=50, edgecolor='black', alpha=0.7)
    ax2.axvline(results['resilience_score'].quantile(0.9), color='red', 
                linestyle='--', label='90th percentile')
    ax2.axvline(results['resilience_score'].quantile(0.1), color='blue', 
                linestyle='--', label='10th percentile')
    ax2.set_xlabel('Resilience Score')
    ax2.set_ylabel('Number of Tracts')
    ax2.set_title('Distribution of Resilience Scores')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Residual Q-Q plot for model diagnostics
    ax3 = axes[1, 0]
    stats.probplot(results['resid'], dist="norm", plot=ax3)
    ax3.set_title('Q-Q Plot of Model Residuals')
    ax3.grid(True, alpha=0.3)
    
    # 4. Top resilient tracts bar chart
    ax4 = axes[1, 1]
    top_10 = results.nlargest(10, 'resilience_score')
    tract_labels = [f"{row['StateAbbr']}-{str(row['TractFIPS'])[-4:]}" 
                   for _, row in top_10.iterrows()]
    y_pos = np.arange(len(tract_labels))
    ax4.barh(y_pos, top_10['resilience_score'].values, color='green', alpha=0.7)
    ax4.set_yticks(y_pos)
    ax4.set_yticklabels(tract_labels)
    ax4.set_xlabel('Resilience Score')
    ax4.set_title('Top 10 Resilient Census Tracts')
    ax4.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('figures/resilience_analysis.png', dpi=300, bbox_inches='tight')
    print("Saved: figures/resilience_analysis.png")
    
    return fig

def create_bivariate_map_data(merged):
    """Prepare data for bivariate choropleth map"""
    print("\n=== Preparing Bivariate Map Data ===")
    
    # Create quintiles for both variables
    merged['lila_intensity'] = pd.qcut(merged['LILATracts_1And10'].fillna(0), 
                                       q=3, labels=['Low', 'Medium', 'High'])
    merged['resilience_category'] = pd.qcut(merged['resilience_score'], 
                                            q=3, labels=['Low', 'Medium', 'High'])
    
    # Create bivariate categories
    bivariate_map = {
        ('Low', 'Low'): 1, ('Low', 'Medium'): 2, ('Low', 'High'): 3,
        ('Medium', 'Low'): 4, ('Medium', 'Medium'): 5, ('Medium', 'High'): 6,
        ('High', 'Low'): 7, ('High', 'Medium'): 8, ('High', 'High'): 9
    }
    
    merged['bivariate_class'] = merged.apply(
        lambda x: bivariate_map.get((x['lila_intensity'], x['resilience_category']), 0)
        if pd.notna(x['lila_intensity']) and pd.notna(x['resilience_category']) else 0,
        axis=1
    )
    
    # Summary
    print("\nBivariate classification distribution:")
    print(merged['bivariate_class'].value_counts().sort_index())
    
    # Key finding: High LILA + High Resilience
    high_lila_high_resilience = merged[
        (merged['lila_intensity'] == 'High') & 
        (merged['resilience_category'] == 'High')
    ]
    print(f"\nTracts with High LILA + High Resilience: {len(high_lila_high_resilience)}")
    print("Top 5 examples:")
    print(high_lila_high_resilience.nlargest(5, 'resilience_score')[
        ['TractFIPS', 'StateAbbr', 'burden', 'resilience_score']
    ])
    
    # Save for mapping
    merged[['GEOID', 'bivariate_class', 'lila_intensity', 'resilience_category',
            'burden', 'resilience_score']].to_csv(
        'data/processed/bivariate_map_data.csv', index=False
    )
    print("Saved: data/processed/bivariate_map_data.csv")
    
    return merged

def identify_case_studies(merged):
    """Identify top resilient tracts for case studies"""
    print("\n=== Case Study Candidates ===")
    
    # Focus on LILA tracts with high resilience
    lila_resilient = merged[
        (merged['LILATracts_1And10'] == 1) & 
        (merged['resilience_score'] > merged['resilience_score'].quantile(0.9))
    ].copy()
    
    # Group by state and city (approximation using state)
    top_cases = lila_resilient.nlargest(20, 'resilience_score')
    
    print(f"\nTop 20 LILA tracts with highest resilience:")
    print(top_cases[['TractFIPS', 'StateAbbr', 'burden', 'resilience_score', 
                     'LILATracts_1And10', 'LILATracts_Vehicle']])
    
    # Geographic diversity
    print(f"\nGeographic distribution:")
    print(top_cases['StateAbbr'].value_counts())
    
    # Save for further investigation
    top_cases.to_csv('data/processed/case_study_candidates.csv', index=False)
    print("\nSaved: data/processed/case_study_candidates.csv")
    
    return top_cases

def main():
    """Run comprehensive analysis"""
    print("=" * 60)
    print("RESILIENCE MAPPING: COMPREHENSIVE DATA ANALYSIS")
    print("=" * 60)
    
    # Load data
    fara, places, results = load_data()
    
    # 1. Analyze PLACES outcomes
    outcome_counts = analyze_places_outcomes(places)
    
    # 2. Analyze confidence intervals
    places_with_ci = analyze_confidence_intervals(places)
    
    # 3. Analyze LILA thresholds
    lila_cols = analyze_lila_thresholds(fara)
    
    # 4. Sensitivity analysis
    merged, sensitivity_df = perform_sensitivity_analysis(fara, results)
    
    # 5. Descriptive statistics
    burden_stats, resilience_stats, top_resilient = generate_descriptive_statistics(
        fara, places, results
    )
    
    # 6. Create visualizations
    fig = create_visualizations(merged, results)
    
    # 7. Prepare bivariate map data
    merged_bivariate = create_bivariate_map_data(merged)
    
    # 8. Identify case studies
    case_studies = identify_case_studies(merged)
    
    # Save summary report
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print("\nKey outputs generated:")
    print("  - figures/resilience_analysis.png: 4-panel visualization")
    print("  - data/processed/bivariate_map_data.csv: For bivariate choropleth")
    print("  - data/processed/case_study_candidates.csv: Top resilient LILA tracts")
    print("\nKey findings:")
    print(f"  - Total tracts analyzed: {len(results):,}")
    print(f"  - Mean resilience score: {results['resilience_score'].mean():.3f}")
    print(f"  - Resilient tracts (>90th percentile): {(results['resilience_score'] > results['resilience_score'].quantile(0.9)).sum()}")
    print(f"  - LILA tracts with high resilience: {len(case_studies)}")

if __name__ == "__main__":
    main()