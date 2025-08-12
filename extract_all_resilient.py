#!/usr/bin/env python3
"""
Extract all 1,059 resilient LILA communities with full location details
"""

import pandas as pd
import numpy as np

def get_all_resilient_communities():
    """Extract all resilient LILA tracts with location details"""
    
    print("Loading data...")
    # Load results and FARA data
    results = pd.read_csv('data/processed/model_table_with_residuals.csv')
    fara = pd.read_csv('data/interim/fara_2019.csv')
    
    # Prepare for merge
    fara['GEOID'] = fara['CensusTract'].astype(str).str.zfill(11)
    results['GEOID'] = results['GEOID'].astype(str).str.zfill(11)
    
    # Get the 90th percentile threshold for resilience
    threshold_90 = results['resilience_score'].quantile(0.9)
    print(f"90th percentile resilience threshold: {threshold_90:.3f}")
    
    # Merge to get full location data
    merged = results.merge(
        fara[['GEOID', 'County', 'State', 'LILATracts_1And10', 
              'Urban', 'Pop2010', 'PovertyRate', 'MedianFamilyIncome']], 
        on='GEOID', 
        how='left'
    )
    
    # Filter to resilient LILA tracts
    resilient_lila = merged[
        (merged['LILATracts_1And10'] == 1) & 
        (merged['resilience_score'] > threshold_90)
    ].copy()
    
    print(f"\nTotal resilient LILA communities: {len(resilient_lila)}")
    
    # Add urban/rural label
    resilient_lila['Type'] = resilient_lila['Urban'].apply(lambda x: 'Urban' if x == 1 else 'Rural')
    
    # Sort by resilience score
    resilient_lila = resilient_lila.sort_values('resilience_score', ascending=False)
    
    # Select and rename columns for output
    output_df = resilient_lila[[
        'TractFIPS', 'County', 'State', 'StateAbbr',
        'resilience_score', 'burden', 'Type', 
        'Pop2010', 'PovertyRate', 'MedianFamilyIncome'
    ]].copy()
    
    output_df.columns = [
        'Census_Tract', 'County', 'State', 'State_Abbr',
        'Resilience_Score', 'Health_Burden', 'Urban_Rural', 
        'Population_2010', 'Poverty_Rate', 'Median_Income'
    ]
    
    # Round numeric columns
    output_df['Resilience_Score'] = output_df['Resilience_Score'].round(3)
    output_df['Health_Burden'] = output_df['Health_Burden'].round(3)
    output_df['Poverty_Rate'] = output_df['Poverty_Rate'].round(1)
    
    # Save full list
    output_df.to_csv('data/processed/all_1059_resilient_lila_communities.csv', index=False)
    print(f"Saved full list to: data/processed/all_1059_resilient_lila_communities.csv")
    
    # Create summary by state
    print("\n" + "="*60)
    print("SUMMARY BY STATE")
    print("="*60)
    state_summary = output_df.groupby(['State', 'State_Abbr']).agg({
        'Census_Tract': 'count',
        'Resilience_Score': 'mean',
        'Urban_Rural': lambda x: (x == 'Urban').sum()
    }).rename(columns={
        'Census_Tract': 'Count',
        'Resilience_Score': 'Mean_Resilience',
        'Urban_Rural': 'Urban_Count'
    })
    
    state_summary['Rural_Count'] = state_summary['Count'] - state_summary['Urban_Count']
    state_summary = state_summary.sort_values('Count', ascending=False)
    
    print("\nTop 15 states by count of resilient LILA communities:")
    print(state_summary.head(15))
    
    # Create summary by county (top 30)
    print("\n" + "="*60)
    print("TOP 30 COUNTIES")
    print("="*60)
    county_summary = output_df.groupby(['County', 'State']).agg({
        'Census_Tract': 'count',
        'Resilience_Score': 'mean',
        'Population_2010': 'sum'
    }).rename(columns={
        'Census_Tract': 'Tract_Count',
        'Resilience_Score': 'Mean_Resilience',
        'Population_2010': 'Total_Population'
    })
    
    county_summary = county_summary.sort_values('Tract_Count', ascending=False).head(30)
    print(county_summary)
    
    # Save county summary
    county_summary.to_csv('data/processed/top_counties_resilient_lila.csv')
    
    # Look for patterns - check for common city names in county field
    print("\n" + "="*60)
    print("POTENTIAL COLLEGE TOWNS / MILITARY BASES")
    print("="*60)
    
    # Keywords that might indicate special populations
    college_keywords = ['University', 'College', 'State', 'Campus']
    military_keywords = ['Fort', 'Base', 'Naval', 'Air Force', 'Marine', 'Army']
    
    # Check county names for patterns
    potential_college = []
    potential_military = []
    
    for _, row in output_df.iterrows():
        county_upper = row['County'].upper() if pd.notna(row['County']) else ''
        
        # Check specific known college counties
        college_counties = {
            'Washtenaw': 'University of Michigan',
            'Centre': 'Penn State',
            'Story': 'Iowa State',
            'Tippecanoe': 'Purdue',
            'Clarke': 'University of Georgia',
            'Orange': 'UNC Chapel Hill',
            'Alachua': 'University of Florida',
            'Dane': 'UW Madison',
            'Boulder': 'CU Boulder',
            'Tompkins': 'Cornell',
            'Lafayette': 'Ole Miss',
            'Riley': 'Kansas State',
            'Oktibbeha': 'Mississippi State',
            'Lee': 'Auburn',
            'Brazos': 'Texas A&M'
        }
        
        military_counties = {
            'El Paso': 'Fort Bliss',
            'Bell': 'Fort Hood',
            'Cumberland': 'Fort Bragg',
            'Hardin': 'Fort Knox',
            'Christian': 'Fort Campbell',
            'Comanche': 'Fort Sill',
            'Muscogee': 'Fort Benning',
            'Liberty': 'Fort Stewart',
            'Onslow': 'Camp Lejeune',
            'San Diego': 'Multiple bases',
            'Norfolk': 'Naval Station Norfolk',
            'Pierce': 'Joint Base Lewis-McChord'
        }
        
        for county_key, institution in college_counties.items():
            if county_key in row['County']:
                potential_college.append({
                    'Tract': row['Census_Tract'],
                    'County': row['County'],
                    'State': row['State'],
                    'Institution': institution,
                    'Resilience': row['Resilience_Score']
                })
                break
                
        for county_key, base in military_counties.items():
            if county_key in row['County']:
                potential_military.append({
                    'Tract': row['Census_Tract'],
                    'County': row['County'],
                    'State': row['State'],
                    'Base': base,
                    'Resilience': row['Resilience_Score']
                })
                break
    
    if potential_college:
        college_df = pd.DataFrame(potential_college)
        print(f"\nFound {len(college_df)} potential college town tracts:")
        print(college_df.head(10))
        college_df.to_csv('data/processed/potential_college_resilient_tracts.csv', index=False)
    
    if potential_military:
        military_df = pd.DataFrame(potential_military)
        print(f"\nFound {len(military_df)} potential military base tracts:")
        print(military_df.head(10))
        military_df.to_csv('data/processed/potential_military_resilient_tracts.csv', index=False)
    
    # Get a sample for manual review
    print("\n" + "="*60)
    print("RANDOM SAMPLE FOR VERIFICATION (20 tracts)")
    print("="*60)
    sample = output_df.sample(n=min(20, len(output_df)), random_state=42)
    for _, row in sample.iterrows():
        print(f"{row['Census_Tract']} - {row['County']}, {row['State_Abbr']} "
              f"(Score: {row['Resilience_Score']:.2f}, {row['Urban_Rural']})")
    
    return output_df, state_summary, county_summary

def create_city_lookup():
    """Create a file to help identify major cities"""
    
    # Load the full resilient list
    df = pd.read_csv('data/processed/all_1059_resilient_lila_communities.csv')
    
    # Group by county to identify clusters
    county_clusters = df.groupby(['County', 'State']).size().sort_values(ascending=False)
    
    print("\n" + "="*60)
    print("COUNTIES WITH MULTIPLE RESILIENT TRACTS (potential cities)")
    print("="*60)
    
    # Counties with 3+ resilient tracts likely contain cities
    multi_tract_counties = county_clusters[county_clusters >= 3]
    print(f"\n{len(multi_tract_counties)} counties have 3+ resilient LILA tracts:")
    print(multi_tract_counties.head(20))
    
    # These need manual city identification
    print("\n" + "="*60)
    print("ACTION NEEDED: City Identification")
    print("="*60)
    print("To identify specific cities for all 1,059 tracts, we need to:")
    print("1. Use Census geocoding API to get lat/lon for each tract")
    print("2. Reverse geocode to get city names")
    print("3. OR use Census Place boundaries to match tracts to cities")
    print("4. OR manually look up major counties in Census data")
    
    return multi_tract_counties

if __name__ == "__main__":
    print("="*60)
    print("EXTRACTING ALL 1,059 RESILIENT LILA COMMUNITIES")
    print("="*60)
    
    # Extract all communities
    all_resilient, state_summary, county_summary = get_all_resilient_communities()
    
    # Identify cities
    multi_tract_counties = create_city_lookup()
    
    print("\n" + "="*60)
    print("EXTRACTION COMPLETE")
    print("="*60)
    print("\nFiles created:")
    print("  - data/processed/all_1059_resilient_lila_communities.csv (FULL LIST)")
    print("  - data/processed/top_counties_resilient_lila.csv")
    print("  - data/processed/potential_college_resilient_tracts.csv")
    print("  - data/processed/potential_military_resilient_tracts.csv")
    
    print("\n🔍 To get specific CITIES for all tracts, we need to either:")
    print("   1. Use Census Geocoding API (free but rate-limited)")
    print("   2. Download Census Place boundary files and do spatial join")
    print("   3. Purchase city append service (~$100-500)")
    print("   4. Use Google Maps Geocoding API ($5 per 1000 requests)")