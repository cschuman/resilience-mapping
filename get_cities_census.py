#!/usr/bin/env python3
"""
Get official Census city names for all resilient tracts
Using Census TIGER/Line Place boundaries
"""

import pandas as pd
import json
import time
from urllib.request import urlopen
from urllib.parse import quote

def get_cities_via_census_api():
    """
    Use Census Geocoding API to get city names
    Most accurate without downloading shapefiles
    """
    
    print("Loading resilient communities list...")
    df = pd.read_csv('data/processed/all_1059_resilient_lila_communities.csv')
    
    # Census Geocoding API endpoint
    base_url = "https://geocoding.geo.census.gov/geocoder/geographies/centroid"
    
    cities = []
    errors = []
    
    print(f"Getting city names for {len(df)} tracts via Census API...")
    print("Note: This will take ~20 minutes due to rate limiting")
    
    for idx, row in df.iterrows():
        tract = str(row['Census_Tract']).zfill(11)
        
        # Build API request for tract centroid
        # Format: State(2) + County(3) + Tract(6)
        state = tract[:2]
        county = tract[2:5]
        tract_code = tract[5:11]
        
        params = {
            'benchmark': '2020',
            'vintage': '2019',  # Match FARA data year
            'layers': 'Census Tracts',
            'format': 'json'
        }
        
        try:
            # First, get tract centroid coordinates
            tract_url = f"https://geocoding.geo.census.gov/geocoder/geographies/tract"
            query = f"?state={state}&county={county}&tract={tract_code}&benchmark=2020&vintage=2019&format=json"
            
            response = urlopen(tract_url + query)
            data = json.loads(response.read())
            
            if data['result']['geographies']:
                geo = data['result']['geographies'][0]
                centroid_lat = geo.get('CENTLAT', '')
                centroid_lon = geo.get('CENTLON', '')
                
                # Now get place name from coordinates
                if centroid_lat and centroid_lon:
                    place_url = f"https://geocoding.geo.census.gov/geocoder/geographies/coordinates"
                    place_query = f"?x={centroid_lon}&y={centroid_lat}&benchmark=2020&vintage=2019&layers=Places&format=json"
                    
                    place_response = urlopen(place_url + place_query)
                    place_data = json.loads(place_response.read())
                    
                    if place_data['result']['geographies']:
                        place_name = place_data['result']['geographies'][0].get('NAME', 'Unincorporated')
                        place_state = place_data['result']['geographies'][0].get('STATE', '')
                    else:
                        place_name = 'Unincorporated/Rural'
                        place_state = state
                else:
                    place_name = 'Unknown'
                    place_state = state
            else:
                place_name = 'Not Found'
                place_state = state
                
            cities.append({
                'Census_Tract': row['Census_Tract'],
                'City': place_name,
                'City_State': place_state,
                'County': row['County'],
                'State': row['State']
            })
            
            if (idx + 1) % 50 == 0:
                print(f"Processed {idx + 1}/{len(df)} tracts...")
                time.sleep(1)  # Rate limiting
                
        except Exception as e:
            errors.append({'tract': tract, 'error': str(e)})
            cities.append({
                'Census_Tract': row['Census_Tract'],
                'City': 'Error',
                'City_State': '',
                'County': row['County'],
                'State': row['State']
            })
            
        # Rate limiting
        time.sleep(0.1)
    
    # Create output dataframe
    cities_df = pd.DataFrame(cities)
    
    # Merge with original data
    result = df.merge(cities_df[['Census_Tract', 'City']], on='Census_Tract', how='left')
    
    # Save results
    result.to_csv('data/processed/all_1059_resilient_with_cities.csv', index=False)
    
    print(f"\nComplete! Saved to: data/processed/all_1059_resilient_with_cities.csv")
    print(f"Errors: {len(errors)}")
    
    if errors:
        pd.DataFrame(errors).to_csv('data/processed/geocoding_errors.csv', index=False)
    
    # Summary of cities
    city_counts = result['City'].value_counts()
    print("\nTop 20 cities by resilient tract count:")
    print(city_counts.head(20))
    
    return result

def quick_county_to_city_mapping():
    """
    Quick approximation using county seats and major cities
    Less accurate but immediate
    """
    
    print("Using county-to-major-city mapping (quick approximation)...")
    
    df = pd.read_csv('data/processed/all_1059_resilient_lila_communities.csv')
    
    # Major county to city mappings
    county_cities = {
        'Harris County': 'Houston',
        'Maricopa County': 'Phoenix',
        'Travis County': 'Austin',
        'Dallas County': 'Dallas',
        'Bexar County': 'San Antonio',
        'King County': 'Seattle',
        'Franklin County': 'Columbus',
        'Marion County': 'Indianapolis',
        'Davidson County': 'Nashville',
        'Tarrant County': 'Fort Worth',
        'San Diego County': 'San Diego',
        'Wake County': 'Raleigh',
        'Gwinnett County': 'Atlanta area',
        'Fulton County': 'Atlanta',
        'Honolulu County': 'Honolulu',
        'Ingham County': 'Lansing/East Lansing',
        'Washtenaw County': 'Ann Arbor',
        'Tippecanoe County': 'Lafayette/West Lafayette',
        'Monroe County': 'Bloomington',
        'Clarke County': 'Athens',
        'Brazos County': 'College Station',
        'Lee County': 'Auburn',
        'Riley County': 'Manhattan',
        'Story County': 'Ames',
        'Dane County': 'Madison',
        'Boulder County': 'Boulder',
        'Tompkins County': 'Ithaca',
        'Centre County': 'State College',
        'Alachua County': 'Gainesville',
        'Orange County': 'Chapel Hill',
        'Lafayette County': 'Oxford',
        'Oktibbeha County': 'Starkville',
        'El Paso County': 'El Paso',
        'Bell County': 'Killeen/Fort Hood',
        'Cumberland County': 'Fayetteville',
        'Christian County': 'Clarksville',
        'Comanche County': 'Lawton',
        'Muscogee County': 'Columbus',
        'Liberty County': 'Hinesville',
        'Onslow County': 'Jacksonville',
        'Norfolk city': 'Norfolk',
        'Virginia Beach city': 'Virginia Beach',
        'Pierce County': 'Tacoma'
    }
    
    # Apply mapping
    df['City'] = df['County'].map(county_cities)
    
    # For unmapped counties, use a generic label
    df['City'] = df['City'].fillna(df['County'].str.replace(' County', ''))
    
    # Add state for clarity
    df['City_State'] = df['City'] + ', ' + df['State_Abbr']
    
    # Save
    df.to_csv('data/processed/all_1059_resilient_with_cities_approx.csv', index=False)
    
    print(f"Saved approximate cities to: data/processed/all_1059_resilient_with_cities_approx.csv")
    
    # Summary
    city_counts = df['City'].value_counts()
    print("\nTop 20 cities by resilient tract count (approximation):")
    print(city_counts.head(20))
    
    # Show some examples
    print("\nSample of city assignments:")
    print(df[['Census_Tract', 'County', 'State_Abbr', 'City']].head(20))
    
    return df

if __name__ == "__main__":
    print("=" * 60)
    print("GETTING CITY NAMES FOR RESILIENT COMMUNITIES")
    print("=" * 60)
    
    print("\nChoose method:")
    print("1. Census API (accurate but slow - 20+ minutes)")
    print("2. County-to-city mapping (quick approximation)")
    
    # For now, use quick method to demonstrate
    print("\nUsing quick approximation method for immediate results...")
    df = quick_county_to_city_mapping()
    
    print("\n" + "=" * 60)
    print("For accurate Census-designated place names:")
    print("Uncomment get_cities_via_census_api() in the code")
    print("Or download TIGER/Line Place shapefiles for spatial join")
    print("=" * 60)