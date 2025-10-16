#!/usr/bin/env python3
"""
Analyze the LEAST resilient LILA communities - those performing worse than expected
These are the true crisis areas needing immediate intervention
"""

import pandas as pd
import numpy as np

def analyze_least_resilient():
    """
    Identify and analyze the least resilient (most vulnerable) LILA tracts
    """
    print("="*60)
    print("ANALYZING LEAST RESILIENT FOOD DESERTS")
    print("="*60)
    
    # Load all data with coordinates
    df = pd.read_csv('data/processed/all_1059_resilient_FINAL_with_coordinates.csv')
    
    # Also load the full model results to get ALL tracts, not just resilient ones
    all_results = pd.read_csv('data/processed/model_table_with_residuals.csv')
    fara = pd.read_csv('data/interim/fara_2019.csv')
    
    # Prepare for merge
    fara['GEOID'] = fara['CensusTract'].astype(str).str.zfill(11)
    all_results['GEOID'] = all_results['GEOID'].astype(str).str.zfill(11)
    
    # Merge to identify ALL LILA tracts
    merged = all_results.merge(
        fara[['GEOID', 'LILATracts_1And10', 'County', 'State', 'PovertyRate', 
              'MedianFamilyIncome', 'Pop2010', 'Urban']], 
        on='GEOID', 
        how='left'
    )
    
    # Filter to LILA tracts only
    all_lila = merged[merged['LILATracts_1And10'] == 1].copy()
    
    print(f"\nTotal LILA tracts analyzed: {len(all_lila)}")
    
    # Get bottom 10% (least resilient)
    threshold_10 = all_lila['resilience_score'].quantile(0.10)
    least_resilient = all_lila[all_lila['resilience_score'] <= threshold_10].copy()
    
    print(f"Least resilient LILA tracts (bottom 10%): {len(least_resilient)}")
    
    # Sort by resilience score (ascending - worst first)
    least_resilient = least_resilient.sort_values('resilience_score')
    
    # Add coordinates from gazetteer
    gaz = pd.read_csv('data/census_gazetteer/2019_Gaz_tracts_national.txt', 
                      sep='\t', dtype={'GEOID': str})
    gaz.columns = gaz.columns.str.strip()
    gaz = gaz[['GEOID', 'INTPTLAT', 'INTPTLONG']]
    gaz.columns = ['GEOID', 'latitude', 'longitude']
    
    least_resilient = least_resilient.merge(gaz, on='GEOID', how='left')
    
    # Urban/Rural label
    least_resilient['Type'] = least_resilient['Urban'].apply(
        lambda x: 'Urban' if x == 1 else 'Rural'
    )
    
    print("\n" + "="*60)
    print("BOTTOM 20 LEAST RESILIENT (MOST VULNERABLE) FOOD DESERTS")
    print("="*60)
    print()
    
    for idx, row in least_resilient.head(20).iterrows():
        print(f"#{idx+1}. Tract {row['TractFIPS']} - {row['County']}, {row['State']}")
        print(f"   Resilience Score: {row['resilience_score']:.2f} (NEGATIVE = worse than expected)")
        print(f"   Health Burden: {row['burden']:.2f} (POSITIVE = poor health)")
        print(f"   Poverty Rate: {row['PovertyRate']:.1f}%")
        print(f"   Population: {row['Pop2010']:.0f} ({row['Type']})")
        if pd.notna(row['latitude']):
            print(f"   📍 Location: https://maps.google.com/?q={row['latitude']},{row['longitude']}")
        print()
    
    # Geographic analysis of least resilient
    print("="*60)
    print("GEOGRAPHIC DISTRIBUTION OF LEAST RESILIENT TRACTS")
    print("="*60)
    
    # By state
    state_counts = least_resilient.groupby('State').size().sort_values(ascending=False).head(15)
    print("\nStates with most vulnerable LILA tracts:")
    for state, count in state_counts.items():
        print(f"  {state}: {count} tracts")
    
    # By county
    county_counts = least_resilient.groupby(['County', 'State']).size().sort_values(ascending=False).head(15)
    print("\nCounties with most vulnerable LILA tracts:")
    for (county, state), count in county_counts.items():
        print(f"  {county}, {state}: {count} tracts")
    
    # Compare characteristics
    print("\n" + "="*60)
    print("COMPARING MOST vs LEAST RESILIENT")
    print("="*60)
    
    # Get most resilient for comparison
    most_resilient = all_lila.nlargest(len(least_resilient), 'resilience_score')
    
    comparison = pd.DataFrame({
        'Metric': ['Mean Resilience Score', 'Mean Health Burden', 'Mean Poverty Rate', 
                   'Median Income', 'Percent Urban', 'Mean Population'],
        'Least Resilient': [
            least_resilient['resilience_score'].mean(),
            least_resilient['burden'].mean(),
            least_resilient['PovertyRate'].mean(),
            least_resilient['MedianFamilyIncome'].median(),
            (least_resilient['Urban'] == 1).mean() * 100,
            least_resilient['Pop2010'].mean()
        ],
        'Most Resilient': [
            most_resilient['resilience_score'].mean(),
            most_resilient['burden'].mean(),
            most_resilient['PovertyRate'].mean(),
            most_resilient['MedianFamilyIncome'].median(),
            (most_resilient['Urban'] == 1).mean() * 100,
            most_resilient['Pop2010'].mean()
        ]
    })
    
    comparison['Difference'] = comparison['Most Resilient'] - comparison['Least Resilient']
    
    print("\nKey Differences:")
    for _, row in comparison.iterrows():
        if row['Metric'] in ['Mean Resilience Score', 'Mean Health Burden']:
            print(f"{row['Metric']}:")
            print(f"  Least Resilient: {row['Least Resilient']:.3f}")
            print(f"  Most Resilient: {row['Most Resilient']:.3f}")
            print(f"  Difference: {row['Difference']:.3f}")
        elif 'Percent' in row['Metric']:
            print(f"{row['Metric']}:")
            print(f"  Least Resilient: {row['Least Resilient']:.1f}%")
            print(f"  Most Resilient: {row['Most Resilient']:.1f}%")
        elif 'Income' in row['Metric']:
            print(f"{row['Metric']}:")
            print(f"  Least Resilient: ${row['Least Resilient']:,.0f}")
            print(f"  Most Resilient: ${row['Most Resilient']:,.0f}")
        else:
            print(f"{row['Metric']}:")
            print(f"  Least Resilient: {row['Least Resilient']:.0f}")
            print(f"  Most Resilient: {row['Most Resilient']:.0f}")
        print()
    
    # Save least resilient list
    least_resilient.to_csv('data/processed/least_resilient_lila_tracts.csv', index=False)
    print(f"Saved {len(least_resilient)} least resilient tracts to: data/processed/least_resilient_lila_tracts.csv")
    
    # Check for patterns in least resilient
    print("\n" + "="*60)
    print("PATTERNS IN LEAST RESILIENT COMMUNITIES")
    print("="*60)
    
    # Rural vs Urban
    rural_pct = (least_resilient['Urban'] == 0).mean() * 100
    print(f"\nRural tracts: {rural_pct:.1f}% (vs {100-rural_pct:.1f}% urban)")
    
    # High poverty
    high_poverty = (least_resilient['PovertyRate'] > 30).mean() * 100
    print(f"High poverty (>30%): {high_poverty:.1f}% of least resilient")
    
    # Regional patterns
    south_states = ['Texas', 'Louisiana', 'Mississippi', 'Alabama', 'Georgia', 
                   'Florida', 'South Carolina', 'North Carolina', 'Tennessee', 
                   'Kentucky', 'West Virginia', 'Virginia', 'Arkansas', 'Oklahoma']
    
    south_tracts = least_resilient[least_resilient['State'].isin(south_states)]
    south_pct = len(south_tracts) / len(least_resilient) * 100
    print(f"Southern states: {south_pct:.1f}% of least resilient")
    
    return least_resilient, comparison

if __name__ == "__main__":
    least_resilient, comparison = analyze_least_resilient()
    
    print("\n" + "="*60)
    print("KEY FINDINGS - CRISIS AREAS")
    print("="*60)
    print("\n🚨 These communities face BOTH:")
    print("   1. Limited food access (LILA status)")
    print("   2. Worse health than predicted by models")
    print("\nThese are priority areas for intervention!")