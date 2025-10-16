#!/usr/bin/env python3
"""
Import Community Data to Supabase
Created: January 31, 2025
Purpose: Import 1,059 resilient communities into Supabase
"""

import pandas as pd
import json
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase credentials (you'll set these)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://YOUR_PROJECT.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY", "YOUR_ANON_KEY")

def init_supabase() -> Client:
    """Initialize Supabase client"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def import_communities(supabase: Client):
    """Import community data from CSV"""
    print("🏘️ Loading community data...")
    
    # Load the main resilient communities file from new location
    df = pd.read_csv('../../data/input/all_1059_resilient_with_cities_enhanced.csv')
    
    print(f"📊 Found {len(df)} communities to import")
    
    # Prepare data for Supabase
    communities = []
    for _, row in df.iterrows():
        # Extract tract_id from Census_Tract column
        census_tract = str(row.get('Census_Tract', ''))
        if not census_tract or census_tract == 'nan':
            continue  # Skip rows with no tract ID
            
        # Extract state code from tract (first 2 digits)
        state_code = census_tract[:2] if len(census_tract) >= 2 else '00'
        # Extract county code from tract (digits 3-5)
        county_code = census_tract[2:5] if len(census_tract) >= 5 else '000'
        
        # Build community name from available data
        community_name = f"{row.get('County', 'Unknown County')}, {row.get('State', 'Unknown State')}"
        if pd.notna(row.get('city_name')):
            community_name = f"{row.get('city_name')}, {row.get('State_Abbr', 'XX')}"
        
        community = {
            'tract_id': census_tract.zfill(11),
            'state': state_code,
            'county': county_code,
            'name': community_name,
            
            # Core metrics (using actual column names and normalizing)
            'population': int(row.get('Population_2010', 0)) if pd.notna(row.get('Population_2010')) else None,
            # Resilience score is already in right range (1-5), normalize to 0-1
            'resilience_score': float(row.get('Resilience_Score', 0)) / 5.0 if pd.notna(row.get('Resilience_Score')) else None,
            # Health burden might need normalization - check if it exists
            'health_outcome': float(row.get('Health_Burden', 0)) / 100.0 if pd.notna(row.get('Health_Burden')) else 0.5,
            # Food access - check if FARA_Score exists, otherwise use default
            'food_access': float(row.get('FARA_Score', 0)) / 100.0 if pd.notna(row.get('FARA_Score')) else 0.5,
            'unexpected_good': True,  # All 1,059 are unexpectedly good
            
            # Additional metrics (normalize percentages to decimals)
            'median_income': int(row.get('Median_Income', 0)) if pd.notna(row.get('Median_Income')) else None,
            # Poverty rate is 0-100, convert to 0-1
            'poverty_rate': float(row.get('Poverty_Rate', 0)) / 100.0 if pd.notna(row.get('Poverty_Rate')) else None,
            'life_expectancy': float(row.get('Life_Expectancy', 0)) if pd.notna(row.get('Life_Expectancy')) else 75.0,  # Default
            
            # Privacy settings (start conservative)
            'privacy_level': 'public',  # You can adjust based on criteria
            'community_approved': True,  # Set to False initially if you want approval workflow
            
            # Data quality
            'data_quality': 'verified'
        }
        
        # Skip geographic coordinates for now - we'll add them later
        # if pd.notna(row.get('longitude')) and pd.notna(row.get('latitude')):
        #     community['centroid'] = f"POINT({row['longitude']} {row['latitude']})"
        
        communities.append(community)
    
    # Insert communities in batches
    batch_size = 50
    successful = 0
    for i in range(0, len(communities), batch_size):
        batch = communities[i:i+batch_size]
        try:
            response = supabase.table('communities').insert(batch).execute()
            successful += len(batch)
            print(f"✅ Imported batch {i//batch_size + 1}/{(len(communities)-1)//batch_size + 1}")
        except Exception as e:
            print(f"❌ Error importing batch {i//batch_size + 1}: {e}")
            # Try inserting one by one to find the problematic record
            for j, community in enumerate(batch):
                try:
                    response = supabase.table('communities').insert(community).execute()
                    successful += 1
                except Exception as individual_error:
                    print(f"   ❌ Failed on record {i+j+1}: tract_id={community.get('tract_id')}, error={individual_error}")
                    # Continue with next record
    
    print(f"🎉 Successfully imported {successful} out of {len(communities)} communities!")

def create_sample_stories(supabase: Client):
    """Create a few sample stories for testing"""
    print("\n📝 Creating sample stories...")
    
    # Get a few community IDs
    response = supabase.table('communities').select('id, name').limit(3).execute()
    communities = response.data
    
    if not communities:
        print("⚠️ No communities found. Import communities first.")
        return
    
    sample_stories = [
        {
            'community_id': communities[0]['id'],
            'title': 'Our Garden Brings Us Together',
            'slug': 'our-garden-brings-us-together',
            'summary': 'How a community garden transformed our neighborhood and brought generations together.',
            'content': '''
                Three years ago, an empty lot sat at the corner of Main and Oak. Today, it's the heart of our community.
                
                What started as one family's idea to grow vegetables has become a place where our entire neighborhood 
                gathers. Children learn from elders about traditional farming methods. New immigrants share seeds and 
                recipes from their home countries. High school students earn service hours while learning about sustainability.
                
                The garden has given us more than fresh food. It's given us connection, purpose, and pride in our community.
                Every tomato planted is a vote of confidence in our neighborhood's future. Every harvest is a celebration 
                of what we can accomplish together.
                
                This is resilience. Not just surviving, but thriving together.
            ''',
            'story_type': 'community_strength',
            'category': 'resilience',
            'tags': ['garden', 'community', 'food', 'sustainability'],
            'storyteller_name': 'Maria Rodriguez',
            'status': 'published',
            'community_approved': True,
            'views': 150,
            'likes': 45
        },
        {
            'community_id': communities[0]['id'] if len(communities) > 0 else None,
            'title': 'When the Flood Came, We Were Ready',
            'slug': 'when-the-flood-came-we-were-ready',
            'summary': 'Our community\'s response to natural disaster showed our true strength.',
            'content': '''
                The weather alerts started on Tuesday. By Thursday, water was rising fast. But this time was different.
                
                After the flood five years ago, we didn't just rebuild - we prepared. Every block now has a flood captain.
                We have supplies stored at the community center. Most importantly, we have a plan that includes everyone,
                especially our elderly neighbors and families without transportation.
                
                When the water came this time, Mr. Johnson was already at Mrs. Chen's house, helping her to higher ground.
                The Patel family's store became a distribution center for emergency supplies. The high school opened as a
                shelter, staffed by volunteers who'd trained for this moment.
                
                We lost some things to the water. But we didn't lose anyone. And we didn't lose hope.
                
                Resilience isn't about avoiding hardship. It's about facing it together.
            ''',
            'story_type': 'crisis_response',
            'category': 'resilience',
            'tags': ['disaster', 'preparedness', 'community', 'mutual aid'],
            'storyteller_name': 'James Washington',
            'storyteller_anonymous': False,
            'status': 'published',
            'community_approved': True,
            'views': 230,
            'likes': 89
        }
    ]
    
    for story in sample_stories:
        try:
            response = supabase.table('stories').insert(story).execute()
            print(f"✅ Created story: {story['title']}")
        except Exception as e:
            print(f"❌ Error creating story: {e}")
    
    print("📚 Sample stories created!")

def verify_import(supabase: Client):
    """Verify the import worked"""
    print("\n🔍 Verifying import...")
    
    # Count communities
    response = supabase.table('communities').select('*', count='exact').execute()
    community_count = response.count
    
    # Count public communities
    response = supabase.table('communities').select('*', count='exact').eq('privacy_level', 'public').execute()
    public_count = response.count
    
    # Count stories
    response = supabase.table('stories').select('*', count='exact').execute()
    story_count = response.count
    
    print(f"""
    ✅ Import Summary:
    - Total communities: {community_count}
    - Public communities: {public_count}
    - Stories: {story_count}
    
    🎉 Your Supabase is ready! Communities are imported and ready to serve.
    """)

def main():
    """Main import function"""
    print("""
    ╔══════════════════════════════════════════════╗
    ║   Health Resilience Mapping Data Import     ║
    ║   Importing 1,059 Resilient Communities     ║
    ╚══════════════════════════════════════════════╝
    """)
    
    # Check if credentials are set
    if SUPABASE_URL == "https://YOUR_PROJECT.supabase.co":
        print("""
        ⚠️ Please set your Supabase credentials first!
        
        1. Create a .env file in this directory
        2. Add your Supabase URL and anon key:
           
           SUPABASE_URL=https://YOUR_PROJECT.supabase.co
           SUPABASE_ANON_KEY=YOUR_ANON_KEY
        
        You can find these in your Supabase project settings.
        """)
        return
    
    try:
        # Initialize Supabase
        supabase = init_supabase()
        print(f"✅ Connected to Supabase: {SUPABASE_URL}")
        
        # Import communities
        import_communities(supabase)
        
        # Create sample stories
        create_sample_stories(supabase)
        
        # Verify everything worked
        verify_import(supabase)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you've:")
        print("1. Run the schema.sql file in Supabase SQL editor")
        print("2. Set the correct credentials in .env")
        print("3. Have the data files in data/input/")

if __name__ == "__main__":
    main()