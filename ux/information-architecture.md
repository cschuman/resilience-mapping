# 🏗 INFORMATION ARCHITECTURE
## Health Resilience Mapping Platform

**Created**: January 31, 2025  
**Version**: 1.0  
**For**: Dev/Creative Team Implementation

---

## 🎯 ARCHITECTURE OVERVIEW

### **Three-Domain Strategy**
```
stories.resilience-mapping.org     → Community narratives & inspiration
research.resilience-mapping.org    → Data analysis & methodology  
policy.resilience-mapping.org      → Implementation guides & briefs
```

### **Shared Core Domain**
```
resilience-mapping.org             → Landing page + unified search
api.resilience-mapping.org         → Unified data API
admin.resilience-mapping.org       → Content management system
```

---

## 📐 SITE STRUCTURE HIERARCHY

### **STORIES SITE** (`stories.resilience-mapping.org`)
```
/
├── /browse/
│   ├── /rural/
│   ├── /urban/
│   ├── /families/
│   ├── /seniors/
│   └── /success-types/
│       ├── /gardens/
│       ├── /markets/
│       ├── /partnerships/
│       └── /health-programs/
├── /communities/
│   └── /{state}/
│       └── /{community-slug}/
│           ├── /story/
│           ├── /people/
│           ├── /resources/
│           └── /data/
├── /featured/
├── /recent/
├── /map/
├── /search/
├── /saved/
├── /about/
└── /submit-story/
```

### **RESEARCH SITE** (`research.resilience-mapping.org`)
```
/
├── /explorer/
│   ├── /map/
│   ├── /data/
│   ├── /charts/
│   └── /compare/
├── /datasets/
│   ├── /communities/
│   ├── /demographics/
│   ├── /health-outcomes/
│   ├── /food-access/
│   └── /interventions/
├── /methodology/
├── /findings/
│   ├── /key-insights/
│   ├── /publications/
│   └── /peer-review/
├── /tools/
│   ├── /api/
│   ├── /downloads/
│   └── /visualizations/
├── /community/{community-id}/
│   ├── /data/
│   ├── /analysis/
│   └── /contacts/
└── /researchers/
    ├── /directory/
    ├── /collaboration/
    └── /publications/
```

### **POLICY SITE** (`policy.resilience-mapping.org`)
```
/
├── /solutions/
│   ├── /rural-health/
│   ├── /urban-planning/
│   ├── /food-access/
│   └── /community-development/
├── /briefs/
│   ├── /federal/
│   ├── /state/
│   ├── /local/
│   └── /nonprofit/
├── /implementation/
│   ├── /guides/
│   ├── /toolkits/
│   ├── /funding/
│   └── /partnerships/
├── /case-studies/
├── /experts/
│   ├── /directory/
│   ├── /consultations/
│   └── /testimonials/
├── /resources/
│   ├── /talking-points/
│   ├── /legislation/
│   └── /funding-sources/
└── /contact/
```

---

## 🔗 CROSS-SITE CONTENT RELATIONSHIPS

### **Unified Content Model**
```
COMMUNITY ENTITY (Core Object)
├── Story Content (stories.*)
│   ├── Narrative text
│   ├── Photos/videos
│   ├── Community testimonials
│   └── Success metrics
├── Research Data (research.*)
│   ├── Demographic data
│   ├── Health outcomes
│   ├── Statistical analysis
│   └── Methodology notes
└── Policy Applications (policy.*)
    ├── Implementation guides
    ├── Funding sources
    ├── Contact information
    └── Replication toolkit
```

### **Content Linking Strategy**
- **Stories** → link to related research data and policy briefs
- **Research** → link to community stories and policy applications
- **Policy** → link to evidence from research and success stories
- **All sites** → cross-reference similar communities

---

## 🏷 CONTENT TAXONOMY

### **Primary Categories**
```
GEOGRAPHY
├── Rural
├── Urban  
├── Suburban
└── Regional (by state/region)

DEMOGRAPHICS  
├── Age (Youth, Families, Seniors)
├── Race/Ethnicity (Community-defined)
├── Income Level
└── Population Size

HEALTH FOCUS
├── Diabetes Prevention
├── Heart Health
├── Mental Health
├── Maternal Health
└── Chronic Disease Management

INTERVENTION TYPE
├── Community Gardens
├── Mobile Markets
├── Corner Store Partnerships
├── Health Worker Programs
├── Policy Changes
└── Infrastructure Improvements

SUCCESS METRICS
├── Health Outcomes
├── Community Engagement
├── Economic Impact
├── Policy Influence
└── Replication Success
```

### **Tagging Strategy**
- **Primary tags**: 3-5 per content item (required)
- **Secondary tags**: Additional descriptors (optional)
- **Community tags**: Self-defined by communities
- **Researcher tags**: Academic categorization
- **Policy tags**: Implementation focus areas

---

## 🔍 SEARCH ARCHITECTURE

### **Unified Search System**
```
SEARCH SCOPE OPTIONS
├── All Sites (default)
├── Stories Only
├── Research Only
└── Policy Only

SEARCH TYPES
├── Quick Search (homepage)
├── Advanced Filters (explorer pages)  
├── Geographic Search (map-based)
└── Similar Community Search (AI-powered)

SEARCH FEATURES
├── Autocomplete suggestions
├── Spell correction
├── Synonym handling
├── Related searches
└── Search result saving
```

### **Search Result Ranking**
1. **Exact matches** (title, location)
2. **Community self-identification** tags
3. **Similarity algorithms** (demographics + outcomes)
4. **Content freshness** (recent updates prioritized)
5. **Community approval ratings** (quality signal)
6. **User engagement metrics** (time on page, shares)

### **Search Personalization**
- **Location-based** suggestions (if permitted)
- **Previous search** history
- **Saved communities** quick access
- **Role-based** results (CHW vs. researcher vs. policymaker)

---

## 🗂 URL STRUCTURE & NAMING

### **URL Patterns**

#### Stories Site URLs
```
/                                  → Homepage
/browse/{category}                 → Browse by category
/browse/{category}/{subcategory}   → Subcategory browse  
/community/{state}/{slug}          → Individual community
/community/{state}/{slug}/story    → Full story page
/community/{state}/{slug}/people   → Key contacts
/community/{state}/{slug}/resources→ Implementation resources
/search?q={query}&filters={params} → Search results
/map?filters={params}              → Map view with filters
/featured                          → Editorial selections
/recent                           → Recently updated
```

#### Research Site URLs  
```
/                                  → Research homepage
/explorer                          → Interactive data explorer
/explorer/map                      → Map-based exploration
/explorer/data                     → Tabular data view
/community/{id}                    → Research profile
/community/{id}/data               → Raw data download
/dataset/{type}                    → Dataset landing pages
/methodology                       → Research methods
/findings/{topic}                  → Key findings by topic
/tools/api                         → API documentation
```

#### Policy Site URLs
```
/                                  → Policy homepage
/solutions/{issue}                 → Solution categories
/briefs/{level}                    → Policy briefs by gov level
/implementation/{type}             → Implementation guides
/case-studies                      → Successful implementations
/experts                           → Expert directory
/contact                          → Get consultation
```

### **URL Best Practices**
- **Readable slugs**: `detroit-community-gardens` not `DET001`
- **Consistent structure**: Same pattern across sites
- **SEO-friendly**: Include primary keywords
- **Stable URLs**: Permanent redirects for changes
- **Clean parameters**: Readable query strings

---

## 🧭 NAVIGATION DESIGN

### **Global Navigation**
```
Primary Nav (All Sites):
[LOGO] Stories | Research | Policy    [SEARCH] [LANGUAGE] [HELP]

Secondary Nav (Context-sensitive):
Stories: Browse | Featured | Map | Recent | Saved
Research: Explorer | Data | Findings | Tools | API  
Policy: Solutions | Briefs | Experts | Resources | Contact
```

### **Breadcrumb Patterns**
```
Stories: Home > Browse > Rural > Texas > Amarillo Community Gardens
Research: Home > Explorer > Community > TX-4567 > Demographics  
Policy: Home > Solutions > Rural Health > Mobile Markets > Implementation
```

### **Footer Navigation**
```
CONTENT                    TOOLS                     HELP
├── Stories                ├── Search                ├── About Us
├── Research               ├── Map Explorer          ├── How It Works  
├── Policy Briefs          ├── Data Downloads        ├── Contact
└── Featured Communities   └── API Access            ├── Privacy Policy
                                                     ├── Terms of Service
CONNECT                    FOR PROFESSIONALS        └── Accessibility
├── Newsletter             ├── Researchers           
├── Social Media           ├── Policymakers          
├── Community Updates      ├── Journalists           
└── Submit Story           └── Community Leaders     
```

---

## 📱 RESPONSIVE NAVIGATION PATTERNS

### **Mobile Navigation**
```
COLLAPSED STATE:
[≡] [LOGO] [🔍]

EXPANDED STATE:
[×] Stories
    ├── Browse Communities
    ├── Featured Stories  
    ├── Map View
    └── Recent Updates
    Research
    ├── Data Explorer
    ├── Findings
    └── Downloads
    Policy  
    ├── Solution Briefs
    ├── Implementation
    └── Expert Directory
    ────────────────
    [🔍] Search
    [🌐] Language: EN ▼
    [?] Help & About
```

### **Tablet Navigation**
- **Horizontal tabs** for primary navigation
- **Dropdown menus** for secondary navigation  
- **Sidebar filters** on explorer pages
- **Sticky navigation** on scroll

### **Desktop Navigation**
- **Full horizontal menu** always visible
- **Mega menus** for complex categories
- **Contextual sidebars** for related content
- **Keyboard shortcuts** for power users

---

## 🎯 CONTENT DISCOVERY PATTERNS

### **Homepage Strategy**
- **Hero search** prominent on all homepages
- **Featured content** editorially curated
- **Browse by category** visual tiles
- **Recent updates** fresh content discovery
- **Popular communities** social proof

### **Related Content Algorithm**
```
SIMILARITY FACTORS (weighted):
├── Geographic proximity (30%)
├── Demographic similarity (25%)  
├── Intervention type (20%)
├── Health outcomes (15%)
└── Community size (10%)

CONTENT RELATIONSHIP TYPES:
├── "Similar Communities"
├── "Also in [State/Region]"  
├── "Communities with [Intervention]"
├── "Research about [Topic]"
└── "Implementation guide for [Solution]"
```

### **Personalization Features**
- **Recently viewed** communities
- **Saved for later** collections
- **Recommended based on** browsing history
- **Communities near you** (opt-in location)
- **Following updates** from specific communities

---

## 📊 ANALYTICS & TRACKING ARCHITECTURE

### **Content Performance Metrics**
- **Page views** and unique visitors
- **Time on page** and bounce rate
- **Search queries** and result clicks
- **Content sharing** across platforms
- **Download rates** for resources
- **Contact form** submissions

### **User Journey Tracking**
- **Cross-site navigation** patterns
- **Content type preferences** by persona
- **Search-to-action** conversion rates
- **Mobile vs desktop** usage patterns
- **Geographic usage** patterns

### **Community Impact Metrics**
- **Story view counts** by community
- **Resource downloads** per community
- **Contact requests** generated
- **Policy brief** usage
- **Researcher engagement** with community data

---

## 🔐 ACCESS CONTROL & PERMISSIONS

### **Public Content** (No authentication required)
- All community stories (with consent)
- Aggregate research findings
- Policy briefs and implementation guides
- Basic search and exploration tools

### **Researcher Access** (Registration required)
- Raw dataset downloads
- Advanced analytics tools
- Community contact information
- Methodology documentation
- Citation tracking

### **Community Admin** (Community-controlled)
- Edit community story content
- Manage resource lists
- Approve/deny research requests
- Update contact information
- View usage analytics for their community

### **Platform Admin** (Staff only)
- Content management system
- User management
- Analytics dashboard
- System monitoring
- Content moderation tools

---

## 🎯 SEO & FINDABILITY STRATEGY

### **URL Structure for SEO**
- **Primary keywords** in URLs
- **Readable slugs** vs numeric IDs
- **Logical hierarchy** reflected in URLs
- **Canonical URLs** to prevent duplication
- **Mobile-friendly** URL patterns

### **Content SEO Strategy**
- **Title tags**: Community name + intervention + outcome
- **Meta descriptions**: Story summary + call to action
- **Header structure**: Logical H1 → H2 → H3 hierarchy
- **Alt text**: Descriptive text for all images
- **Internal linking**: Strong cross-site link network

### **Schema Markup**
```
STRUCTURED DATA TYPES:
├── LocalBusiness (for communities)
├── NewsArticle (for stories)  
├── Dataset (for research data)
├── GovernmentService (for policy content)
└── ContactPoint (for expert directory)
```

---

## 🎯 INFORMATION ARCHITECTURE VALIDATION

### **Card Sorting Results** (Simulated based on personas)
- **Maria (CHW)**: Grouped by intervention type and outcome
- **Dr. James (Researcher)**: Grouped by methodology and data type
- **Sarah (Policymaker)**: Grouped by implementation level and cost
- **Keisha (Resident)**: Grouped by location and family relevance

### **Tree Testing Priorities**
1. **Find similar community** to yours (all personas)
2. **Download implementation guide** (professionals)  
3. **Contact successful community** (practitioners)
4. **Access raw data** (researchers)
5. **Submit your story** (community members)

### **First-Click Testing Focus**
- Homepage → Community story (85% success target)
- Research → Data download (70% success target)  
- Policy → Implementation guide (80% success target)
- Any page → Search function (95% success target)

---

## 🎯 CONTENT MAINTENANCE ARCHITECTURE

### **Content Lifecycle Management**
```
CREATION WORKFLOW:
Community Outreach → Story Collection → Fact Checking → 
Community Approval → Publication → Ongoing Updates

UPDATE TRIGGERS:
├── Annual community check-ins
├── New data releases  
├── Policy changes
├── Community requests
└── Link rot detection
```

### **Content Governance Structure**
- **Community liaisons**: Manage community relationships
- **Content editors**: Ensure quality and consistency
- **Data stewards**: Maintain research integrity
- **Technical writers**: Keep documentation current
- **Community managers**: Handle feedback and requests

---

**Next Steps**: Create technical architecture diagram based on this information architecture.

**Review Date**: February 5, 2025 (after technical implementation begins)