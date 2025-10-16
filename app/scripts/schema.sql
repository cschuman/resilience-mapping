-- Health Resilience Mapping Platform
-- Supabase Schema
-- Created: January 31, 2025
-- Purpose: Simple, powerful database for 1,059+ resilient communities

-- Enable PostGIS for geographic queries
CREATE EXTENSION IF NOT EXISTS postgis;

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- COMMUNITIES TABLE
-- =====================================================
CREATE TABLE communities (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    tract_id VARCHAR(11) UNIQUE NOT NULL,
    state VARCHAR(2) NOT NULL,
    county VARCHAR(3) NOT NULL,
    name TEXT NOT NULL,
    
    -- Core resilience metrics
    population INTEGER,
    resilience_score DECIMAL(5,4),
    health_outcome DECIMAL(5,4),
    food_access DECIMAL(5,4),
    unexpected_good BOOLEAN DEFAULT false,
    
    -- Geographic data
    centroid GEOGRAPHY(POINT, 4326),
    boundary GEOGRAPHY(MULTIPOLYGON, 4326),
    
    -- Additional metrics
    median_income INTEGER,
    poverty_rate DECIMAL(5,4),
    life_expectancy DECIMAL(4,1),
    
    -- Privacy and consent
    privacy_level VARCHAR(20) DEFAULT 'private' CHECK (privacy_level IN ('public', 'restricted', 'private')),
    community_approved BOOLEAN DEFAULT false,
    consent_date TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    data_quality VARCHAR(20) DEFAULT 'provisional',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_communities_tract_id ON communities(tract_id);
CREATE INDEX idx_communities_state ON communities(state);
CREATE INDEX idx_communities_unexpected_good ON communities(unexpected_good);
CREATE INDEX idx_communities_privacy ON communities(privacy_level);
CREATE INDEX idx_communities_resilience ON communities(resilience_score DESC);
CREATE INDEX idx_communities_centroid ON communities USING GIST(centroid);

-- =====================================================
-- STORIES TABLE
-- =====================================================
CREATE TABLE stories (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    community_id UUID REFERENCES communities(id) ON DELETE CASCADE,
    
    -- Story content
    title TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    summary TEXT,
    content TEXT NOT NULL,
    
    -- Categorization
    story_type VARCHAR(50),
    category VARCHAR(50),
    tags TEXT[],
    
    -- Storyteller info (optional, respects privacy)
    storyteller_name TEXT,
    storyteller_anonymous BOOLEAN DEFAULT false,
    
    -- Media
    featured_image_url TEXT,
    media_urls TEXT[],
    
    -- Status and approval
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'pending_approval', 'published', 'archived')),
    community_approved BOOLEAN DEFAULT false,
    approved_by UUID,
    approved_at TIMESTAMP WITH TIME ZONE,
    published_at TIMESTAMP WITH TIME ZONE,
    
    -- Engagement metrics
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    
    -- Metadata
    created_by UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_stories_community ON stories(community_id);
CREATE INDEX idx_stories_slug ON stories(slug);
CREATE INDEX idx_stories_status ON stories(status);
CREATE INDEX idx_stories_published ON stories(published_at DESC);
CREATE INDEX idx_stories_category ON stories(category);

-- =====================================================
-- USERS TABLE (extends Supabase auth.users)
-- =====================================================
CREATE TABLE user_profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    
    -- Basic info
    username TEXT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    display_name TEXT,
    bio TEXT,
    avatar_url TEXT,
    
    -- User type and role
    user_type VARCHAR(30) DEFAULT 'community_member' 
        CHECK (user_type IN ('community_member', 'researcher', 'policy_maker', 'admin')),
    role VARCHAR(30) DEFAULT 'viewer',
    
    -- Community association
    community_id UUID REFERENCES communities(id),
    community_verified BOOLEAN DEFAULT false,
    community_role VARCHAR(50), -- e.g., 'representative', 'member'
    
    -- Professional info (for researchers/policy makers)
    organization TEXT,
    job_title TEXT,
    research_interests TEXT[],
    
    -- Privacy and consent
    privacy_settings JSONB DEFAULT '{"profile_public": false, "show_email": false}',
    consent_given BOOLEAN DEFAULT false,
    terms_accepted_at TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- COMMENTS TABLE
-- =====================================================
CREATE TABLE comments (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    story_id UUID REFERENCES stories(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    parent_id UUID REFERENCES comments(id) ON DELETE CASCADE,
    
    content TEXT NOT NULL,
    
    -- Moderation
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'flagged', 'removed')),
    moderated_by UUID,
    moderated_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_comments_story ON comments(story_id);
CREATE INDEX idx_comments_user ON comments(user_id);
CREATE INDEX idx_comments_parent ON comments(parent_id);
CREATE INDEX idx_comments_status ON comments(status);

-- =====================================================
-- LIKES TABLE (for stories)
-- =====================================================
CREATE TABLE likes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    story_id UUID REFERENCES stories(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(story_id, user_id)
);

-- =====================================================
-- RESEARCH_ACCESS TABLE
-- =====================================================
CREATE TABLE research_access (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Access details
    access_level VARCHAR(30) CHECK (access_level IN ('basic', 'full', 'admin')),
    data_use_agreement_signed BOOLEAN DEFAULT false,
    irb_approval_number TEXT,
    institution TEXT,
    research_purpose TEXT,
    
    -- Access period
    approved_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    
    -- Audit trail
    approved_by UUID,
    access_log JSONB DEFAULT '[]',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- ROW LEVEL SECURITY POLICIES
-- =====================================================

-- Enable RLS on all tables
ALTER TABLE communities ENABLE ROW LEVEL SECURITY;
ALTER TABLE stories ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE likes ENABLE ROW LEVEL SECURITY;
ALTER TABLE research_access ENABLE ROW LEVEL SECURITY;

-- Communities: Public can view public communities
CREATE POLICY "Public communities are viewable by everyone" ON communities
    FOR SELECT USING (privacy_level = 'public' AND community_approved = true);

-- Communities: Authenticated users can view restricted communities
CREATE POLICY "Restricted communities viewable by authenticated" ON communities
    FOR SELECT TO authenticated
    USING (privacy_level IN ('public', 'restricted'));

-- Communities: Community members can view their own community
CREATE POLICY "Community members can view their community" ON communities
    FOR SELECT TO authenticated
    USING (
        id IN (
            SELECT community_id FROM user_profiles 
            WHERE id = auth.uid() AND community_verified = true
        )
    );

-- Stories: Public can view published stories from public communities
CREATE POLICY "Published stories are viewable by everyone" ON stories
    FOR SELECT USING (
        status = 'published' 
        AND community_id IN (
            SELECT id FROM communities 
            WHERE privacy_level = 'public' AND community_approved = true
        )
    );

-- Stories: Authors can manage their own stories
CREATE POLICY "Authors can manage their stories" ON stories
    FOR ALL TO authenticated
    USING (created_by = auth.uid());

-- User profiles: Users can view their own profile
CREATE POLICY "Users can view own profile" ON user_profiles
    FOR SELECT TO authenticated
    USING (id = auth.uid());

-- User profiles: Users can update their own profile
CREATE POLICY "Users can update own profile" ON user_profiles
    FOR UPDATE TO authenticated
    USING (id = auth.uid());

-- Comments: Anyone can view approved comments
CREATE POLICY "Approved comments are public" ON comments
    FOR SELECT USING (status = 'approved');

-- Comments: Users can create comments
CREATE POLICY "Authenticated users can comment" ON comments
    FOR INSERT TO authenticated
    WITH CHECK (user_id = auth.uid());

-- Likes: Users can manage their own likes
CREATE POLICY "Users can manage their likes" ON likes
    FOR ALL TO authenticated
    USING (user_id = auth.uid());

-- =====================================================
-- FUNCTIONS AND TRIGGERS
-- =====================================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at trigger to all tables
CREATE TRIGGER update_communities_updated_at BEFORE UPDATE ON communities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_stories_updated_at BEFORE UPDATE ON stories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to increment story views
CREATE OR REPLACE FUNCTION increment_story_views(story_uuid UUID)
RETURNS void AS $$
BEGIN
    UPDATE stories 
    SET views = views + 1 
    WHERE id = story_uuid;
END;
$$ language 'plpgsql';

-- Function to get nearby communities
CREATE OR REPLACE FUNCTION get_nearby_communities(
    lat FLOAT, 
    lng FLOAT, 
    radius_km FLOAT DEFAULT 50
)
RETURNS TABLE(
    id UUID,
    tract_id VARCHAR,
    name TEXT,
    distance_km FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.tract_id,
        c.name,
        ST_Distance(c.centroid, ST_MakePoint(lng, lat)::geography) / 1000 as distance_km
    FROM communities c
    WHERE 
        c.privacy_level = 'public'
        AND c.community_approved = true
        AND ST_DWithin(c.centroid, ST_MakePoint(lng, lat)::geography, radius_km * 1000)
    ORDER BY distance_km;
END;
$$ language 'plpgsql';

-- =====================================================
-- SAMPLE DATA (Remove in production)
-- =====================================================

-- Sample community (you'll import real data)
INSERT INTO communities (
    tract_id, state, county, name,
    population, resilience_score, health_outcome, food_access,
    unexpected_good, privacy_level, community_approved,
    centroid
) VALUES (
    '01001020100', '01', '001', 'Sample Resilient Community',
    2500, 0.82, 0.75, 0.45,
    true, 'public', true,
    ST_MakePoint(-86.7911, 33.3865)
);

-- Success message
DO $$ 
BEGIN 
    RAISE NOTICE 'Schema created successfully! Ready to import 1,059 resilient communities.';
END $$;