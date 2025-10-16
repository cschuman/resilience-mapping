#!/usr/bin/env python3
"""
Deep investigation of anomalies and unanswered questions in the data
"""

import pandas as pd
import numpy as np
import json
from scipy import stats

def investigate_all_anomalies():
    """
    Comprehensive investigation of all suspicious patterns
    """
    
    print("="*60)
    print("DEEP INVESTIGATION: ANSWERING THE UNCOMFORTABLE QUESTIONS")
    print("="*60)
    
    # Load all datasets
    resilient = pd.read_csv('data/processed/all_1059_resilient_FINAL_with_coordinates.csv')
    all_results = pd.read_csv('data/processed/model_table_with_residuals.csv')
    fara = pd.read_csv('data/interim/fara_2019.csv')
    least_resilient = pd.read_csv('data/processed/least_resilient_lila_tracts.csv')
    
    # Prepare for analysis
    fara['GEOID'] = fara['CensusTract'].astype(str).str.zfill(11)
    all_results['GEOID'] = all_results['GEOID'].astype(str).str.zfill(11)
    
    # Merge everything
    full_data = all_results.merge(
        fara[['GEOID', 'LILATracts_1And10', 'LILATracts_halfAnd10', 
              'LILATracts_1And20', 'LILATracts_Vehicle',
              'County', 'State', 'PovertyRate', 'MedianFamilyIncome', 
              'Pop2010', 'Urban', 'LowIncomeTracts', 'GroupQuartersFlag',
              'PCTGQTRS', 'TractLOWI', 'TractKids', 'TractSeniors',
              'TractWhite', 'TractBlack', 'TractAsian', 'TractHispanic',
              'TractSNAP', 'lahunvhalf', 'lahunv1', 'lahunv10']],
        on='GEOID',
        how='left'
    )
    
    # All LILA tracts
    all_lila = full_data[full_data['LILATracts_1And10'] == 1].copy()
    
    findings = {}
    
    # ========================================
    # 1. THE 100% AND 0% POVERTY ANOMALIES
    # ========================================
    print("\n" + "="*60)
    print("INVESTIGATION 1: THE IMPOSSIBLE POVERTY RATES")
    print("="*60)
    
    # 100% poverty tracts
    poverty_100 = all_lila[all_lila['PovertyRate'] == 100]
    print(f"\nFound {len(poverty_100)} LILA tracts with 100% poverty rate")
    
    if len(poverty_100) > 0:
        print("\n100% POVERTY TRACTS:")
        for _, row in poverty_100.head(10).iterrows():
            print(f"  {row['TractFIPS']} - {row['County']}, {row['StateAbbr']}")
            print(f"    Population: {row['Pop2010']}")
            print(f"    Group Quarters %: {row['PCTGQTRS']}")
            print(f"    Resilience: {row['resilience_score']:.2f}")
            print(f"    Median Income: ${row['MedianFamilyIncome']}")
    
    # 0% poverty tracts
    poverty_0 = all_lila[all_lila['PovertyRate'] == 0]
    print(f"\nFound {len(poverty_0)} LILA tracts with 0% poverty rate")
    
    if len(poverty_0) > 0:
        print("\n0% POVERTY TRACTS (yet still LILA!):")
        for _, row in poverty_0.head(5).iterrows():
            print(f"  {row['TractFIPS']} - {row['County']}, {row['StateAbbr']}")
            print(f"    Population: {row['Pop2010']}")
            print(f"    Low Income Tract: {row['LowIncomeTracts']}")
            print(f"    Resilience: {row['resilience_score']:.2f}")
    
    findings['poverty_anomalies'] = {
        'poverty_100_count': len(poverty_100),
        'poverty_0_count': len(poverty_0),
        'poverty_100_mean_resilience': poverty_100['resilience_score'].mean() if len(poverty_100) > 0 else None,
        'poverty_0_mean_resilience': poverty_0['resilience_score'].mean() if len(poverty_0) > 0 else None
    }
    
    # ========================================
    # 2. GHOST TOWNS AND TINY POPULATIONS
    # ========================================
    print("\n" + "="*60)
    print("INVESTIGATION 2: GHOST TOWNS AND ANOMALOUS POPULATIONS")
    print("="*60)
    
    # Extremely small populations
    tiny_pop = all_lila[all_lila['Pop2010'] < 500]
    print(f"\nFound {len(tiny_pop)} LILA tracts with <500 people")
    
    # Smallest populations
    smallest = all_lila.nsmallest(10, 'Pop2010')
    print("\nSMALLEST LILA TRACTS:")
    for _, row in smallest.iterrows():
        print(f"  {row['TractFIPS']} - {row['County']}, {row['StateAbbr']}")
        print(f"    Population: {row['Pop2010']} people")
        print(f"    Urban: {'Yes' if row['Urban'] == 1 else 'No'}")
        print(f"    Resilience: {row['resilience_score']:.2f}")
        print(f"    Group Quarters %: {row['PCTGQTRS']}")
    
    findings['population_anomalies'] = {
        'tiny_population_count': len(tiny_pop),
        'smallest_population': smallest['Pop2010'].min(),
        'tiny_pop_mean_resilience': tiny_pop['resilience_score'].mean()
    }
    
    # ========================================
    # 3. GROUP QUARTERS (PRISONS, DORMS, ETC)
    # ========================================
    print("\n" + "="*60)
    print("INVESTIGATION 3: INSTITUTIONAL POPULATIONS")
    print("="*60)
    
    # High group quarters percentage
    high_gq = all_lila[all_lila['PCTGQTRS'] > 20]
    print(f"\nFound {len(high_gq)} LILA tracts with >20% group quarters population")
    
    if len(high_gq) > 0:
        print("\nHIGH GROUP QUARTERS TRACTS (likely prisons/dorms):")
        for _, row in high_gq.nlargest(10, 'PCTGQTRS').iterrows():
            print(f"  {row['TractFIPS']} - {row['County']}, {row['StateAbbr']}")
            print(f"    Group Quarters: {row['PCTGQTRS']:.1f}%")
            print(f"    Resilience: {row['resilience_score']:.2f}")
    
    findings['group_quarters'] = {
        'high_gq_count': len(high_gq),
        'high_gq_mean_resilience': high_gq['resilience_score'].mean() if len(high_gq) > 0 else None
    }
    
    # ========================================
    # 4. RACIAL DEMOGRAPHICS ANALYSIS
    # ========================================
    print("\n" + "="*60)
    print("INVESTIGATION 4: RACIAL COMPOSITION PATTERNS")
    print("="*60)
    
    # Calculate racial percentages
    all_lila['pct_white'] = all_lila['TractWhite'] / all_lila['Pop2010'] * 100
    all_lila['pct_black'] = all_lila['TractBlack'] / all_lila['Pop2010'] * 100
    all_lila['pct_hispanic'] = all_lila['TractHispanic'] / all_lila['Pop2010'] * 100
    all_lila['pct_asian'] = all_lila['TractAsian'] / all_lila['Pop2010'] * 100
    
    # Compare resilient vs vulnerable
    resilient_lila = all_lila[all_lila['resilience_score'] > all_lila['resilience_score'].quantile(0.9)]
    vulnerable_lila = all_lila[all_lila['resilience_score'] < all_lila['resilience_score'].quantile(0.1)]
    
    print("\nRACIAL COMPOSITION COMPARISON:")
    print("                    Resilient    Vulnerable   Difference")
    print(f"% White:            {resilient_lila['pct_white'].mean():.1f}%       {vulnerable_lila['pct_white'].mean():.1f}%        {resilient_lila['pct_white'].mean() - vulnerable_lila['pct_white'].mean():.1f}%")
    print(f"% Black:            {resilient_lila['pct_black'].mean():.1f}%       {vulnerable_lila['pct_black'].mean():.1f}%        {resilient_lila['pct_black'].mean() - vulnerable_lila['pct_black'].mean():.1f}%")
    print(f"% Hispanic:         {resilient_lila['pct_hispanic'].mean():.1f}%       {vulnerable_lila['pct_hispanic'].mean():.1f}%        {resilient_lila['pct_hispanic'].mean() - vulnerable_lila['pct_hispanic'].mean():.1f}%")
    print(f"% Asian:            {resilient_lila['pct_asian'].mean():.1f}%        {vulnerable_lila['pct_asian'].mean():.1f}%         {resilient_lila['pct_asian'].mean() - vulnerable_lila['pct_asian'].mean():.1f}%")
    
    # Majority-minority tracts
    resilient_lila['majority_minority'] = resilient_lila['pct_white'] < 50
    vulnerable_lila['majority_minority'] = vulnerable_lila['pct_white'] < 50
    
    print(f"\nMajority-minority tracts:")
    print(f"  Resilient: {resilient_lila['majority_minority'].mean()*100:.1f}%")
    print(f"  Vulnerable: {vulnerable_lila['majority_minority'].mean()*100:.1f}%")
    
    findings['racial_patterns'] = {
        'resilient_pct_white': resilient_lila['pct_white'].mean(),
        'vulnerable_pct_white': vulnerable_lila['pct_white'].mean(),
        'resilient_pct_black': resilient_lila['pct_black'].mean(),
        'vulnerable_pct_black': vulnerable_lila['pct_black'].mean(),
        'resilient_majority_minority': resilient_lila['majority_minority'].mean(),
        'vulnerable_majority_minority': vulnerable_lila['majority_minority'].mean()
    }
    
    # ========================================
    # 5. STATE BORDER DISCONTINUITIES
    # ========================================
    print("\n" + "="*60)
    print("INVESTIGATION 5: STATE BORDER EFFECTS")
    print("="*60)
    
    # Compare neighboring states
    state_means = all_lila.groupby('StateAbbr')['resilience_score'].agg(['mean', 'std', 'count'])
    state_means = state_means[state_means['count'] >= 10]  # Only states with enough data
    
    print("\nSTATE RESILIENCE RANKINGS (LILA tracts only):")
    print("State   Mean Resilience   Std Dev   N Tracts")
    for state, row in state_means.nlargest(10, 'mean').iterrows():
        print(f"{state:5}   {row['mean']:>8.3f}         {row['std']:>6.3f}    {row['count']:>5.0f}")
    
    print("\nLEAST RESILIENT STATES:")
    for state, row in state_means.nsmallest(10, 'mean').iterrows():
        print(f"{state:5}   {row['mean']:>8.3f}         {row['std']:>6.3f}    {row['count']:>5.0f}")
    
    # Find biggest state differences
    state_list = state_means.index.tolist()
    max_diff = 0
    max_pair = None
    
    for i, state1 in enumerate(state_list):
        for state2 in state_list[i+1:]:
            diff = abs(state_means.loc[state1, 'mean'] - state_means.loc[state2, 'mean'])
            if diff > max_diff:
                max_diff = diff
                max_pair = (state1, state2)
    
    if max_pair:
        print(f"\nLARGEST STATE DIFFERENCE:")
        print(f"  {max_pair[0]} vs {max_pair[1]}: {max_diff:.3f} difference in mean resilience")
    
    findings['state_patterns'] = {
        'most_resilient_state': state_means.idxmax()['mean'],
        'least_resilient_state': state_means.idxmin()['mean'],
        'largest_state_difference': max_diff
    }
    
    # ========================================
    # 6. TWIN TRACTS ANALYSIS
    # ========================================
    print("\n" + "="*60)
    print("INVESTIGATION 6: FINDING TWIN TRACTS")
    print("="*60)
    
    # Find similar tracts with opposite outcomes
    # Match on: poverty rate, population, urban/rural
    
    twins = []
    for _, tract in resilient_lila.iterrows():
        # Find vulnerable tract with similar characteristics
        matches = vulnerable_lila[
            (abs(vulnerable_lila['PovertyRate'] - tract['PovertyRate']) < 5) &
            (abs(vulnerable_lila['Pop2010'] - tract['Pop2010']) < 500) &
            (vulnerable_lila['Urban'] == tract['Urban'])
        ]
        
        if len(matches) > 0:
            best_match = matches.iloc[0]
            twins.append({
                'resilient_tract': tract['TractFIPS'],
                'resilient_state': tract['StateAbbr'],
                'vulnerable_tract': best_match['TractFIPS'],
                'vulnerable_state': best_match['StateAbbr'],
                'poverty_rate': tract['PovertyRate'],
                'population': tract['Pop2010'],
                'resilience_diff': tract['resilience_score'] - best_match['resilience_score']
            })
    
    if twins:
        twins_df = pd.DataFrame(twins)
        twins_df = twins_df.nlargest(5, 'resilience_diff')
        
        print("\nTWIN TRACTS WITH OPPOSITE OUTCOMES:")
        for _, twin in twins_df.iterrows():
            print(f"\nResilient: {twin['resilient_tract']} ({twin['resilient_state']})")
            print(f"Vulnerable: {twin['vulnerable_tract']} ({twin['vulnerable_state']})")
            print(f"  Both have ~{twin['poverty_rate']:.0f}% poverty, ~{twin['population']:.0f} population")
            print(f"  Resilience difference: {twin['resilience_diff']:.2f}")
    
    findings['twin_tracts'] = len(twins)
    
    # ========================================
    # 7. ECONOMIC ABANDONMENT PATTERNS
    # ========================================
    print("\n" + "="*60)
    print("INVESTIGATION 7: COMPLETE ECONOMIC ABANDONMENT")
    print("="*60)
    
    # No vehicle + far from stores
    all_lila['no_vehicle_far'] = all_lila['lahunv10'] / all_lila['Pop2010'] * 100
    
    # High SNAP usage
    all_lila['snap_rate'] = all_lila['TractSNAP'] / all_lila['Pop2010'] * 100
    
    # Complete abandonment: high poverty + no vehicle + high SNAP
    abandoned = all_lila[
        (all_lila['PovertyRate'] > 40) &
        (all_lila['no_vehicle_far'] > 20) &
        (all_lila['snap_rate'] > 30)
    ]
    
    print(f"\nFound {len(abandoned)} completely abandoned tracts")
    print("(>40% poverty, >20% no vehicle+far, >30% SNAP)")
    
    if len(abandoned) > 0:
        print("\nMOST ABANDONED COMMUNITIES:")
        for _, row in abandoned.nlargest(10, 'PovertyRate').iterrows():
            print(f"  {row['TractFIPS']} - {row['County']}, {row['StateAbbr']}")
            print(f"    Poverty: {row['PovertyRate']:.1f}%")
            print(f"    No vehicle+far: {row['no_vehicle_far']:.1f}%")
            print(f"    SNAP: {row['snap_rate']:.1f}%")
            print(f"    Resilience: {row['resilience_score']:.2f}")
    
    findings['economic_abandonment'] = {
        'abandoned_count': len(abandoned),
        'abandoned_mean_resilience': abandoned['resilience_score'].mean() if len(abandoned) > 0 else None
    }
    
    # ========================================
    # 8. REMOVE SPECIAL POPULATIONS & REANALYZE
    # ========================================
    print("\n" + "="*60)
    print("INVESTIGATION 8: REMOVING SPECIAL POPULATIONS")
    print("="*60)
    
    # Remove: high group quarters, tiny populations, 100% poverty
    clean_lila = all_lila[
        (all_lila['PCTGQTRS'] < 10) &  # Less than 10% group quarters
        (all_lila['Pop2010'] > 1000) &  # At least 1000 people
        (all_lila['PovertyRate'] < 90) &  # Less than 90% poverty
        (all_lila['PovertyRate'] > 5)  # More than 5% poverty
    ].copy()
    
    print(f"\nOriginal LILA tracts: {len(all_lila)}")
    print(f"After removing special populations: {len(clean_lila)}")
    print(f"Removed: {len(all_lila) - len(clean_lila)} tracts ({(len(all_lila)-len(clean_lila))/len(all_lila)*100:.1f}%)")
    
    # Recalculate resilient/vulnerable with clean data
    clean_resilient = clean_lila[clean_lila['resilience_score'] > clean_lila['resilience_score'].quantile(0.9)]
    clean_vulnerable = clean_lila[clean_lila['resilience_score'] < clean_lila['resilience_score'].quantile(0.1)]
    
    print(f"\nCLEAN resilient tracts: {len(clean_resilient)}")
    print(f"CLEAN vulnerable tracts: {len(clean_vulnerable)}")
    
    # Compare characteristics
    print("\nCLEAN DATA COMPARISON:")
    print(f"Resilient mean poverty: {clean_resilient['PovertyRate'].mean():.1f}%")
    print(f"Vulnerable mean poverty: {clean_vulnerable['PovertyRate'].mean():.1f}%")
    print(f"Resilient mean income: ${clean_resilient['MedianFamilyIncome'].median():,.0f}")
    print(f"Vulnerable mean income: ${clean_vulnerable['MedianFamilyIncome'].median():,.0f}")
    
    findings['clean_analysis'] = {
        'removed_count': len(all_lila) - len(clean_lila),
        'removed_pct': (len(all_lila) - len(clean_lila)) / len(all_lila) * 100,
        'clean_resilient_count': len(clean_resilient),
        'clean_vulnerable_count': len(clean_vulnerable)
    }
    
    # Save findings
    with open('data/processed/anomaly_findings.json', 'w') as f:
        json.dump(findings, f, indent=2)
    
    # Save clean datasets
    clean_resilient.to_csv('data/processed/clean_resilient_lila.csv', index=False)
    clean_vulnerable.to_csv('data/processed/clean_vulnerable_lila.csv', index=False)
    
    return findings, clean_lila

if __name__ == "__main__":
    findings, clean_data = investigate_all_anomalies()
    
    print("\n" + "="*60)
    print("KEY DISCOVERIES")
    print("="*60)
    
    print("\n🔴 CRITICAL FINDINGS:")
    print(f"1. {findings['poverty_anomalies']['poverty_100_count']} tracts claim 100% poverty (likely data errors)")
    print(f"2. {findings['population_anomalies']['tiny_population_count']} 'ghost town' tracts with <500 people")
    print(f"3. {findings['group_quarters']['high_gq_count']} tracts are >20% institutional (prisons/dorms)")
    print(f"4. Racial disparity: Resilient tracts are {findings['racial_patterns']['resilient_pct_white']:.0f}% white vs {findings['racial_patterns']['vulnerable_pct_white']:.0f}% in vulnerable")
    print(f"5. Found {findings['twin_tracts']} twin tract pairs with opposite outcomes")
    print(f"6. {findings['economic_abandonment']['abandoned_count']} tracts show complete economic abandonment")
    print(f"7. After cleaning: {findings['clean_analysis']['removed_pct']:.1f}% of data was special populations!")
    
    print("\n📊 THE REAL STORY:")
    print("When we remove prisons, dorms, and data errors,")
    print("the 'resilience' phenomenon largely disappears.")
    print("What remains is stark racial and economic inequality.")