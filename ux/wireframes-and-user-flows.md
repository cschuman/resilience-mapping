# 📐 WIREFRAMES & USER FLOWS
## Health Resilience Mapping Platform

**Created**: January 31, 2025  
**Version**: 1.0  
**For**: Dev/Creative Team Implementation

---

## 🎯 SITE ARCHITECTURE OVERVIEW

### **Three-Site Strategy**
1. **stories.resilience-mapping.org** → Community-focused, narrative-driven
2. **research.resilience-mapping.org** → Data-focused, academic tools
3. **policy.resilience-mapping.org** → Brief-focused, action-oriented

### **Shared Navigation**
```
[ LOGO ] Stories | Research | Policy    [SEARCH] [LANGUAGE] [HELP]
```

---

## 📱 MOBILE-FIRST WIREFRAMES

### **STORIES SITE - Mobile Homepage**
```
┌─────────────────┐
│ [≡] STORIES [🔍]│
├─────────────────┤
│   🏠 Find Hope   │
│  in Communities  │
│   Like Yours     │
│                 │
│ [Search by zip] │
│ [    56789    ] │
│ [ Find Stories ]│
├─────────────────┤
│ 📍 Featured Today│
│ ┌─────┬────────┐│
│ │📸   │Detroit │ │
│ │     │Gardens │ │
│ │     │Success │ │
│ └─────┴────────┘│
├─────────────────┤
│ 🎯 Browse by     │
│ [ Rural ] [Urban]│
│ [Families][Elders]│
│ [ Success Stories]│
├─────────────────┤
│ 💬 Latest Updates│
│ "Birmingham adds │
│ new garden..." → │
└─────────────────┘
```

### **RESEARCH SITE - Mobile Homepage**
```
┌─────────────────┐
│ [≡] RESEARCH [🔍]│
├─────────────────┤
│ 📊 Data & Analysis│
│  on 1,059 Resilient│
│    Communities    │
│                  │
│ [Quick Search]   │
│ Demographics ▼   │
│ [Download Data]  │
├─────────────────┤
│ 📈 Key Findings  │
│ • 23% higher health│
│ • Rural outperform │
│ • See methodology →│
├─────────────────┤
│ 🔬 Research Tools │
│ [🗂 Browse Dataset]│
│ [📊 Create Charts] │
│ [📋 Export Data]   │
├─────────────────┤
│ 📚 Publications  │
│ "Food Access ≠   │
│ Health Outcomes" →│
└─────────────────┘
```

### **POLICY SITE - Mobile Homepage**
```
┌─────────────────┐
│ [≡] POLICY  [🔍]│
├─────────────────┤
│ 🏛 Evidence-Based │
│  Solutions for    │
│  Policymakers     │
│                  │
│ [Find by Issue]  │
│ Rural Health ▼   │
│ [Get Brief]      │
├─────────────────┤
│ ⚡ Quick Actions  │
│ [📄 4-Page Brief] │
│ [📞 Contact List] │
│ [🗣 Talking Points]│
├─────────────────┤
│ 🎯 Success Models │
│ Rural Kansas:    │
│ Mobile Markets → │
│                  │
│ Urban Detroit:   │
│ Corner Stores → │
├─────────────────┤
│ 📞 Get Help      │
│ Expert Consults  │
│ [Schedule Call]  │
└─────────────────┘
```

---

## 🖥 DESKTOP WIREFRAMES

### **STORIES SITE - Desktop Layout**
```
┌────────────────────────────────────────────────────────────┐
│ STORIES    Research | Policy        [Search] [Lang] [Help] │
├────────────────────────────────────────────────────────────┤
│                                                            │
│        🏠 FIND HOPE IN COMMUNITIES LIKE YOURS              │
│                                                            │
│    [Search by location, demographics, or challenges]       │
│    [                                                ]      │
│                     [Find Communities]                     │
│                                                            │
├──────────────────────┬─────────────────────────────────────┤
│ 📍 FEATURED STORIES   │ 🎯 BROWSE BY CATEGORY              │
│                      │                                     │
│ ┌─────────────────┐  │ [🏘 Rural]     [🏙 Urban]          │
│ │     📸          │  │                                     │
│ │  Detroit        │  │ [👨‍👩‍👧‍👦 Families]  [👴 Seniors]       │
│ │  Community      │  │                                     │
│ │  Gardens        │  │ [💪 Success]   [🤝 Partnerships]    │
│ │                 │  │                                     │
│ │ "How one woman  │  │ [📖 All Stories]                   │
│ │ transformed..." │  │                                     │
│ └─────────────────┘  │                                     │
│                      │                                     │
│ ┌─────────────────┐  │ 💬 COMMUNITY UPDATES               │
│ │     📸          │  │                                     │
│ │  Birmingham     │  │ • New garden opens in Austin       │
│ │  Mobile Market  │  │ • Rural Kansas wins state award    │
│ │                 │  │ • Detroit program expands          │
│ │ "Weekly fresh   │  │                                     │
│ │ produce..."     │  │ [View All Updates]                 │
│ └─────────────────┘  │                                     │
└──────────────────────┴─────────────────────────────────────┘
```

### **RESEARCH SITE - Desktop Data Explorer**
```
┌────────────────────────────────────────────────────────────┐
│ RESEARCH   Stories | Policy           [Search] [Lang] [Help]│
├────────────────────────────────────────────────────────────┤
│ 📊 DATA EXPLORER: 1,059 Resilient Communities             │
├─────────────────┬──────────────────────────────────────────┤
│ 🔍 FILTERS      │ 🗺 MAP VIEW                             │
│                 │                                         │
│ Demographics    │ ┌─────────────────────────────────────┐ │
│ □ Rural         │ │                                     │ │
│ ✓ Urban         │ │        📍    📍                    │ │
│ □ Suburban      │ │              📍   📍              │ │
│                 │ │    📍                              │ │
│ Population      │ │         📍    📍    📍            │ │
│ [1000] - [50000]│ │                                     │ │
│                 │ │                                     │ │
│ Health Outcomes │ │    [Zoom In] [Satellite] [Data]    │ │
│ ✓ Low Diabetes  │ └─────────────────────────────────────┘ │
│ ✓ Heart Health  │                                         │
│                 │ 📊 QUICK STATS                          │
│ Food Access     │ • Average health improvement: 23%       │
│ □ No Grocery    │ • Rural communities: 67% of total      │
│ ✓ Limited SNAP  │ • Most common intervention: Gardens     │
│                 │                                         │
│ [Apply Filters] │ [📊 Create Chart] [📋 Export Data]     │
├─────────────────┼──────────────────────────────────────────┤
│ 📈 RESULTS      │ 📊 SELECTED COMMUNITY                  │
│ 247 communities │                                         │
│                 │ Detroit Census Tract 5339              │
│ ┌─────────────┐ │ Population: 3,247                      │
│ │ Detroit     │ │ Demographics: 67% Black, 23% Latino    │
│ │ CT-5339     │ │ Median Income: $31,200                 │
│ │ Pop: 3,247  │ │                                         │
│ └─────────────┘ │ 🎯 Key Success Factors:                │
│                 │ • Community gardens (5)                │
│ ┌─────────────┐ │ • Mobile farmer's market               │
│ │ Atlanta     │ │ • Health worker program                │
│ │ CT-1205     │ │                                         │
│ │ Pop: 2,891  │ │ [📞 Contact] [📖 Full Story]          │
│ └─────────────┘ │                                         │
└─────────────────┴──────────────────────────────────────────┘
```

---

## 🔄 USER FLOW DIAGRAMS

### **FLOW 1: Maria (CHW) Finding Resources**
```
Maria opens app on phone
         ↓
Homepage loads (stories site)
         ↓
Types "diabetes Birmingham" in search
         ↓
Results show 5 similar communities
         ↓
Taps "Detroit Gardens" story
         ↓
Reads 2-minute story + sees photos
         ↓
Taps "Save Offline" button
         ↓
Downloads resource list + contact info
         ↓
Shares with client via text message
         ↓
SUCCESS: Client feels hopeful
```

### **FLOW 2: Dr. James (Researcher) Getting Data**
```
Google search "resilient communities data"
         ↓
Finds research site in results
         ↓
Homepage explains methodology
         ↓
Clicks "Browse Dataset"
         ↓
Filters by rural + diabetes + South
         ↓
Previews data table (147 communities)
         ↓
Clicks "Download CSV"
         ↓
Fills out usage form (30 seconds)
         ↓
Downloads data + metadata + codebook
         ↓
SUCCESS: Runs analysis in R
```

### **FLOW 3: Councilwoman Sarah (Policymaker) Finding Solutions**
```
Colleague emails policy site link
         ↓
Opens policy homepage
         ↓
Clicks "Rural Health" from dropdown
         ↓
Sees 4-page brief with key findings
         ↓
Downloads "Implementation Guide"
         ↓
Clicks "Contact Successful Communities"
         ↓
Gets list of 3 rural success stories
         ↓
Calls Kansas community leader
         ↓
SUCCESS: Plans mobile market program
```

### **FLOW 4: Keisha (Resident) Discovering Her Community**
```
Neighbor mentions "we're on a website"
         ↓
Googles "Detroit resilient communities"
         ↓
Finds stories site in results
         ↓
Searches for her zip code
         ↓
Sees her community featured!
         ↓
Reads story about her neighborhood
         ↓
Shares on Facebook with pride
         ↓
Friends comment + share more
         ↓
SUCCESS: Neighborhood pride increases
```

---

## 📝 DETAILED WIREFRAMES BY PAGE TYPE

### **Community Story Page (Stories Site)**
```
┌─────────────────────────┐
│ [≡] ←  DETROIT GARDENS  │
├─────────────────────────┤
│                         │
│    📸 Hero Image        │
│   (Community garden)    │
│                         │
├─────────────────────────┤
│ 📍 Detroit, Michigan    │
│ Population: 3,247       │
│ 67% Black, 23% Latino   │
│ Median Income: $31,200  │
├─────────────────────────┤
│ 🎯 THE SUCCESS STORY    │
│                         │
│ "Five years ago, this   │
│ neighborhood had no     │
│ grocery store and the   │
│ highest diabetes rates  │
│ in the city..."         │
│                         │
│ [Read Full Story]       │
├─────────────────────────┤
│ 📊 BY THE NUMBERS       │
│ • Diabetes: ↓23%        │
│ • Gardens: 5 built      │
│ • Families: 89 involved │
├─────────────────────────┤
│ 🤝 KEY PEOPLE           │
│ ┌───────┬─────────────┐ │
│ │ 📸    │ Maria Lopez │ │
│ │       │ Garden Lead │ │
│ │       │ [Contact]   │ │
│ └───────┴─────────────┘ │
├─────────────────────────┤
│ 📚 RESOURCES            │
│ • Garden Planning Guide │
│ • Funding Sources List  │
│ • Volunteer Toolkit     │
│ [Download All] [Save]   │
├─────────────────────────┤
│ 🔗 SIMILAR COMMUNITIES  │
│ • Birmingham Gardens    │
│ • Atlanta Urban Farms   │
│ • Phoenix Co-ops        │
└─────────────────────────┘
```

### **Data Explorer Page (Research Site)**
```
┌─────────────────────────┐
│ 📊 DATA EXPLORER        │
├─────────────────────────┤
│ 🔍 Search & Filter      │
│ [Location] [Demographics]│
│ [Health] [Food Access]  │
├─────────────────────────┤
│ 📈 Current Selection    │
│ 247 communities match   │
│ your criteria           │
├─────────────────────────┤
│ 🗺 Map View             │
│ ┌─────────────────────┐ │
│ │    📍  📍  📍      │ │
│ │  📍        📍      │ │
│ │      📍    📍      │ │
│ │ [Zoom] [Layers]    │ │
│ └─────────────────────┘ │
├─────────────────────────┤
│ 📊 Results List         │
│ ┌─────────────────────┐ │
│ │ Detroit CT-5339     │ │
│ │ Pop: 3,247 | Rural  │ │
│ │ Health Score: 8.2   │ │
│ │ [View] [Add to Set] │ │
│ └─────────────────────┘ │
├─────────────────────────┤
│ 🔧 Analysis Tools       │
│ [📊 Create Chart]       │
│ [📋 Export Data]        │
│ [📧 Save Search]        │
└─────────────────────────┘
```

### **Policy Brief Page (Policy Site)**
```
┌─────────────────────────┐
│ 🏛 RURAL HEALTH BRIEF   │
├─────────────────────────┤
│ ⚡ EXECUTIVE SUMMARY     │
│                         │
│ Rural communities can   │
│ achieve better health   │
│ outcomes despite food   │
│ access challenges       │
│ through three proven    │
│ interventions...        │
├─────────────────────────┤
│ 📊 KEY FINDINGS         │
│ • 23% health improvement│
│ • $2.3M cost savings    │
│ • 67% community support │
├─────────────────────────┤
│ 🎯 PROVEN SOLUTIONS     │
│                         │
│ 1. Mobile Markets       │
│ Cost: $150K annually    │
│ Impact: 500 families    │
│ ROI: 3:1                │
│                         │
│ 2. Community Gardens    │
│ Cost: $25K setup        │
│ Impact: 100 families    │
│ ROI: 8:1                │
├─────────────────────────┤
│ 🚀 IMPLEMENTATION       │
│ [📋 Action Checklist]   │
│ [💰 Funding Sources]    │
│ [📞 Expert Contacts]    │
├─────────────────────────┤
│ 📚 ADDITIONAL RESOURCES │
│ [📄 Full Research]      │
│ [🎥 Video Examples]     │
│ [📧 Email Brief]        │
└─────────────────────────┘
```

---

## 🎯 INTERACTION PATTERNS

### **Search Functionality**
- **Autocomplete** as user types
- **Visual filters** with preview counts
- **Sort options**: Similarity, Success Level, Population
- **Save searches** for returning users
- **Recent searches** quick access

### **Story Navigation**
- **Swipe/Arrow** between similar communities
- **Progress indicator** for long stories
- **Quick facts** sidebar always visible
- **Share buttons** for social media
- **Print-friendly** single-page version

### **Data Visualization**
- **Interactive maps** with zoom/pan
- **Hover details** on data points
- **Toggle layers** (demographics, health, etc.)
- **Export options** (PNG, PDF, SVG)
- **Responsive charts** for mobile

### **Community Control**
- **Flag content** button on every page
- **Contact form** for corrections
- **Privacy controls** for personal stories
- **Opt-out mechanisms** clearly marked
- **Status updates** on requests

---

## 🎯 RESPONSIVE BREAKPOINTS

### **Mobile First** (320px+)
- Single column layout
- Touch-friendly buttons (44px min)
- Simplified navigation
- Essential content only

### **Tablet** (768px+)
- Two-column where appropriate
- Enhanced filtering options
- Sidebar navigation
- More detailed previews

### **Desktop** (1024px+)
- Multi-column layouts
- Advanced data tools
- Keyboard shortcuts
- Rich interactions

### **Large Desktop** (1440px+)
- Dashboard-style layouts
- Multiple simultaneous views
- Advanced analytics
- Professional tools

---

## 🎯 ACCESSIBILITY WIREFRAME NOTES

### **Screen Reader Flow**
1. **Skip navigation** link first
2. **Main landmark** clearly defined
3. **Heading hierarchy** logical (h1→h2→h3)
4. **Alt text** for all images
5. **Button purpose** clear from text

### **Keyboard Navigation**
- **Tab order** follows visual flow
- **Focus indicators** highly visible
- **Keyboard shortcuts** for power users
- **Modal traps** focus properly
- **Custom controls** follow ARIA patterns

### **Color & Contrast**
- **High contrast** mode available
- **Color never** sole information method
- **Text alternatives** for color-coding
- **Pattern/texture** supplements color
- **User preference** respect for reduced motion

---

## 🎯 WIREFRAME VALIDATION CHECKLIST

### **Before Development Starts**
- [ ] All user stories mapped to wireframes
- [ ] Mobile-first approach confirmed
- [ ] Accessibility requirements included
- [ ] Performance considerations noted
- [ ] Community control mechanisms visible
- [ ] Three-site navigation clear
- [ ] Search functionality detailed
- [ ] Data export flows defined
- [ ] Story sharing flows mapped
- [ ] Error states designed

### **Ready for Design System**
- [ ] Component inventory complete
- [ ] Interaction patterns defined
- [ ] Content strategy aligned
- [ ] Technical feasibility confirmed
- [ ] Community feedback incorporated

---

**Next Steps**: Create content strategy and copy framework based on these wireframes.

**Review Date**: February 3, 2025 (after design system creation)