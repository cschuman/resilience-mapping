# Community Resilience Mapping - UX Redesign Proposal

**Date:** December 29, 2025
**Prepared by:** UX Design Team
**Version:** 1.0

---

## Executive Summary

This document proposes a comprehensive UX redesign for the Community Resilience Mapping application to address critical navigation issues, improve content discoverability, and create cohesive user journeys across all personas. The redesign maintains all valuable content while establishing clear information architecture and intuitive navigation patterns.

**Key Problems Addressed:**
- No persistent navigation causing user disorientation
- Homepage overload with competing calls-to-action
- About page content overwhelming users (600+ lines with no navigation)
- Disconnected experiences between Map, Stories, and Data sections
- No clear discovery path for exploratory users
- API documentation buried and difficult to find for developers

---

## Table of Contents

1. [User Research & Personas](#1-user-research--personas)
2. [Proposed Information Architecture](#2-proposed-information-architecture)
3. [Global Navigation System](#3-global-navigation-system)
4. [Page-by-Page Redesign](#4-page-by-page-redesign)
5. [User Journey Flows](#5-user-journey-flows)
6. [Wireframe Descriptions](#6-wireframe-descriptions)
7. [Progressive Disclosure Strategy](#7-progressive-disclosure-strategy)
8. [Implementation Priority](#8-implementation-priority)
9. [Success Metrics](#9-success-metrics)

---

## 1. User Research & Personas

### Primary Personas

#### 1.1 The Community Organizer (Maya)
**Goals:**
- Understand resilience in her neighborhood
- Identify strengths to leverage for community programs
- Find similar communities for best practice sharing

**Pain Points:**
- Gets lost without persistent navigation
- Overwhelmed by technical methodology
- Can't easily share specific areas with stakeholders

**Needs:**
- Quick access to local data via address search
- Stories that provide context and inspiration
- Simple sharing capabilities (links, screenshots)

#### 1.2 The Academic Researcher (Dr. Chen)
**Goals:**
- Understand statistical methodology in depth
- Access raw data for secondary analysis
- Cite the project in academic work

**Pain Points:**
- About page lacks table of contents
- Can't quickly jump to specific methodology sections
- API documentation not prominent enough

**Needs:**
- Scannable methodology with clear sections
- Direct access to API documentation
- Citation information readily available

#### 1.3 The Data Journalist (Sam)
**Goals:**
- Find compelling stories in the data
- Create visualizations for articles
- Verify data sources and limitations

**Pain Points:**
- No way to filter/sort top resilient communities
- Stories and data feel disconnected
- Can't easily explore patterns (e.g., "high resilience food deserts")

**Needs:**
- Advanced filtering on the map
- Connection between quantitative data and qualitative stories
- Clear data provenance and limitations

#### 1.4 The Developer (Alex)
**Goals:**
- Integrate resilience data into other applications
- Understand API rate limits and capabilities
- Test endpoints quickly

**Pain Points:**
- API documentation buried at bottom of homepage
- No interactive API explorer
- Unclear what query parameters are available

**Needs:**
- Dedicated API documentation page
- Code examples in multiple languages
- Clear rate limiting and error handling docs

#### 1.5 The Casual Explorer (Jordan)
**Goals:**
- Learn what "community resilience" means
- Check their own neighborhood out of curiosity
- Understand if this matters to them

**Pain Points:**
- Homepage is data-heavy, not welcoming
- Unclear where to start
- Gets lost in methodology jargon

**Needs:**
- Simple, jargon-free introduction
- Immediate gratification (search their address first, learn later)
- Clear "why this matters" messaging

---

## 2. Proposed Information Architecture

### 2.1 Site Structure (Sitemap)

```
Community Resilience Mapping
│
├── Home (/)
│   ├── Hero Section (What is this? Why it matters)
│   ├── Quick Start (Address search OR Browse map OR Explore stories)
│   ├── Key Insights (3-4 data highlights)
│   └── For Different Users (Links to deep content)
│
├── Explore (/explore)
│   ├── Interactive Map (default view)
│   ├── Filter Panel (left sidebar, collapsible)
│   ├── Results Panel (right sidebar, shows selected tract OR list)
│   └── Share/Export tools
│
├── Stories (/stories)
│   ├── Featured Stories Grid
│   ├── Filter by Category (health, food, community, economic)
│   ├── Submit Story CTA
│   └── Related Tracts (Map integration)
│
├── Learn (/learn)
│   ├── Overview Tab
│   │   ├── Research Question
│   │   ├── Key Findings
│   │   ├── Quick Stats
│   │   └── Visual Explainer
│   │
│   ├── Methodology Tab
│   │   ├── Table of Contents (sticky)
│   │   ├── Data Sources
│   │   ├── Statistical Model
│   │   ├── Score Categories
│   │   └── Validation Approach
│   │
│   ├── Limitations Tab
│   │   ├── Temporal Gaps
│   │   ├── Model Limitations
│   │   ├── Appropriate Use Cases
│   │   └── Inappropriate Use Cases
│   │
│   └── FAQ Tab
│       ├── General Questions
│       ├── Technical Questions
│       └── Data Questions
│
├── For Developers (/developers)
│   ├── Getting Started
│   ├── API Reference
│   │   ├── Authentication (if applicable)
│   │   ├── Endpoints
│   │   │   ├── GET /api/stats
│   │   │   ├── GET /api/tracts
│   │   │   ├── GET /api/tracts/:fips
│   │   │   └── GET /api/geocode
│   │   ├── Rate Limits
│   │   └── Error Handling
│   ├── Code Examples
│   │   ├── JavaScript/TypeScript
│   │   ├── Python
│   │   ├── R
│   │   └── cURL
│   ├── Data Schema
│   └── Changelog
│
└── About (/about)
    ├── Project Background
    ├── Team
    ├── Citation
    ├── Contact
    └── Terms of Use
```

### 2.2 Information Architecture Principles

1. **Separation of Concerns:** Split dense "About" page into "/learn" (methodology) and "/about" (project info)
2. **Task-Based Organization:** Primary actions (Explore, Stories, Learn) in main nav
3. **Progressive Disclosure:** Start simple (home), add complexity on demand (explore filters)
4. **Developer-First API Docs:** Dedicated section, not buried in general content
5. **Content Chunking:** Use tabs within pages to reduce vertical scrolling

---

## 3. Global Navigation System

### 3.1 Desktop Navigation

**Primary Navigation Bar (Persistent across all pages)**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  [Logo] Community Resilience Mapping                                    │
│                                                                          │
│  Explore   Stories   Learn   For Developers   About   [Search Icon]    │
└─────────────────────────────────────────────────────────────────────────┘
```

**Specifications:**
- **Position:** Fixed at top, dark gradient background (#0f172a to #1e293b)
- **Height:** 64px
- **Logo:** Left-aligned, links to home
- **Primary Links:** Center-aligned, 16px font, emerald hover (#10b981)
- **Search Icon:** Right-aligned, opens global address search modal
- **Active State:** Bottom border (3px solid emerald) + text color emerald
- **Accessibility:** Skip link, keyboard navigation, ARIA labels

**Secondary Navigation (Contextual)**
- Appears below primary nav on specific pages
- Example: Explore page shows "Map | Data Table | Statistics" toggle
- Example: Learn page shows "Overview | Methodology | Limitations | FAQ" tabs

### 3.2 Mobile Navigation

**Hamburger Menu (< 768px)**

```
┌────────────────────────────────────┐
│  ☰  CRM        [Search Icon]       │
└────────────────────────────────────┘

[Tap ☰ reveals full-screen menu]

┌────────────────────────────────────┐
│  ✕  Menu                           │
├────────────────────────────────────┤
│                                    │
│  🗺️  Explore                       │
│  📖  Stories                       │
│  🎓  Learn                         │
│  💻  For Developers                │
│  ℹ️  About                         │
│                                    │
│  ───────────────────────              │
│                                    │
│  🔍  Search by Address             │
│                                    │
└────────────────────────────────────┘
```

**Specifications:**
- **Hamburger Position:** Top-left, 44px touch target
- **Menu Style:** Full-screen overlay, slide-in from left
- **Close Button:** Top-right ✕, 44px touch target
- **Menu Items:** 20px font, 56px tall touch targets
- **Search:** Promoted to bottom of menu for quick access

### 3.3 Breadcrumb Navigation

Used on deep pages to show context:

```
Home > Explore > Census Tract 26163523900
Home > Learn > Methodology > Statistical Model
Home > Stories > Health > Detroit Urban Gardens
```

**Specifications:**
- **Position:** Below header, above page title
- **Style:** 14px font, slate-400 color, emerald on hover
- **Separator:** > or / character
- **Last Item:** Not a link (current page)

### 3.4 Footer Navigation

**Desktop Footer (3 columns)**

```
┌─────────────────────────────────────────────────────────────────┐
│  EXPLORE              LEARN                CONNECT              │
│  Map                  Methodology          About the Project    │
│  Data Table           Limitations          Team                 │
│  Statistics           FAQ                  Contact              │
│  API Docs             Citation             GitHub               │
│                                                                  │
│  ────────────────────────────────────────────────────────────   │
│                                                                  │
│  © 2025 Community Resilience Mapping | Terms | Privacy          │
└─────────────────────────────────────────────────────────────────┘
```

**Specifications:**
- **Background:** Darker slate (#0f172a)
- **Links:** Small (14px), muted color, organized by task
- **Social Links:** If applicable, icon-only with labels

---

## 4. Page-by-Page Redesign

### 4.1 Homepage (/) - The Welcome Gateway

**Current Problems:**
- Too much data upfront (stats, top tracts table, API links)
- Three CTAs compete for attention
- No clear value proposition for casual visitors

**Redesign Strategy:**
Focus on clarity, quick value, and directing users to the right path.

#### Layout Structure:

**Hero Section (Full viewport height)**
```
┌──────────────────────────────────────────────────────────────────┐
│                         NAVIGATION BAR                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│                  Community Resilience Mapping                    │
│                                                                  │
│         Discovering the hidden strengths in communities          │
│          that help them thrive against the odds                  │
│                                                                  │
│                  ┌──────────────────────────┐                   │
│                  │  Enter your address...   │  [Search]         │
│                  └──────────────────────────┘                   │
│                                                                  │
│         or  [Browse the Map]  [Read Stories]                    │
│                                                                  │
│                         ↓ Scroll to learn more                  │
└──────────────────────────────────────────────────────────────────┘
```

**What This Is Section**
```
┌──────────────────────────────────────────────────────────────────┐
│  What is Community Resilience?                                   │
│                                                                  │
│  [Icon] Some communities have better health outcomes than       │
│         their circumstances predict. We map these communities   │
│         to understand what makes them resilient.                │
│                                                                  │
│  [Visual: Simple before/after diagram or infographic]           │
│                                                                  │
│  64,419 census tracts • 50 states + DC • 330M+ people           │
└──────────────────────────────────────────────────────────────────┘
```

**Three Key Findings (Insight Cards)**
```
┌──────────────────────────────────────────────────────────────────┐
│  Key Insights from the Data                                      │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  1,059      │  │  Rural &    │  │  Community  │            │
│  │  resilient  │  │  Urban both │  │  networks   │            │
│  │  food       │  │  show high  │  │  matter     │            │
│  │  deserts    │  │  resilience │  │  more than  │            │
│  │             │  │             │  │  income     │            │
│  │  [Explore→] │  │  [Explore→] │  │  [Learn→]   │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└──────────────────────────────────────────────────────────────────┘
```

**Pathways Section (For Different Users)**
```
┌──────────────────────────────────────────────────────────────────┐
│  Find Your Path                                                  │
│                                                                  │
│  ┌──────────────────────┐  ┌──────────────────────┐            │
│  │ 🗺️ I want to explore │  │ 📖 I want to read    │            │
│  │   my community        │  │   success stories    │            │
│  │                       │  │                       │            │
│  │ Search by address or  │  │ Real examples from   │            │
│  │ browse the map        │  │ resilient communities│            │
│  │                       │  │                       │            │
│  │ [Go to Map →]        │  │ [Read Stories →]     │            │
│  └──────────────────────┘  └──────────────────────┘            │
│                                                                  │
│  ┌──────────────────────┐  ┌──────────────────────┐            │
│  │ 🎓 I want to learn   │  │ 💻 I want to use     │            │
│  │   the methodology     │  │   the data/API       │            │
│  │                       │  │                       │            │
│  │ Statistical approach  │  │ REST API endpoints   │            │
│  │ and data sources      │  │ and code examples    │            │
│  │                       │  │                       │            │
│  │ [Learn More →]       │  │ [API Docs →]         │            │
│  └──────────────────────┘  └──────────────────────┘            │
└──────────────────────────────────────────────────────────────────┘
```

**Featured Story Teaser**
```
┌──────────────────────────────────────────────────────────────────┐
│  Featured Story                                                  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  [Image]  Urban Garden Network Transforms Food Desert       ││
│  │                                                              ││
│  │           A coalition in Detroit converted vacant lots...   ││
│  │                                                              ││
│  │           [Read Story →]  [View on Map →]                   ││
│  └─────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────┘
```

**Quick Stats Footer**
```
┌──────────────────────────────────────────────────────────────────┐
│  Dataset at a Glance                                             │
│                                                                  │
│  64,419 tracts  |  51 states  |  5.7 avg score  |  330M+ people │
└──────────────────────────────────────────────────────────────────┘
```

#### Key Changes:
- Remove top tracts table (move to Explore page with filtering)
- Remove API links from homepage (dedicated page)
- Add search bar to hero for immediate engagement
- Use insight cards instead of raw stats
- Provide clear pathways for different user types

---

### 4.2 Explore Page (/explore) - Unified Data Experience

**Current Problems:**
- Map is full-screen with minimal context
- No way to filter or search for patterns
- Selected tract info only shows in popup, not persistent
- Can't see data table view as alternative to map

**Redesign Strategy:**
Create a powerful exploration interface with map, filters, and data views.

#### Layout Structure:

**Desktop (3-column layout)**
```
┌─────────────────────────────────────────────────────────────────────────┐
│                         NAVIGATION BAR                                  │
├─────┬───────────────────────────────────────────────────────────┬───────┤
│     │                                                            │       │
│  F  │                  INTERACTIVE MAP                          │   I   │
│  I  │                                                            │   N   │
│  L  │                                                            │   F   │
│  T  │   (Map visualization with legend,                         │   O   │
│  E  │    search bar overlay at top,                             │       │
│  R  │    zoom controls, fullscreen toggle)                      │   P   │
│  S  │                                                            │   A   │
│     │                                                            │   N   │
│     │                                                            │   E   │
│  280│                                                            │  320  │
│  px │                                                            │  px   │
│     │                                                            │       │
├─────┴───────────────────────────────────────────────────────────┴───────┤
│                              FOOTER                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

**Left Sidebar - Filters Panel (Collapsible)**
```
┌────────────────────────┐
│  [≡] Filters           │
│  ────────────────────  │
│                        │
│  Resilience Score      │
│  ○ All                 │
│  ○ Very High (≥2.0)    │
│  ○ High (1.0-2.0)      │
│  ○ Medium (0-1.0)      │
│  ○ Low (-1.0-0)        │
│  ○ Very Low (<-1.0)    │
│                        │
│  ────────────────────  │
│                        │
│  Geographic            │
│  [State dropdown ▼]    │
│  [County dropdown ▼]   │
│                        │
│  ────────────────────  │
│                        │
│  Community Type        │
│  ☑ Urban               │
│  ☑ Rural               │
│  ☐ High Group Quarters │
│                        │
│  ────────────────────  │
│                        │
│  Special Interest      │
│  ☐ Food Deserts (LILA) │
│  ☐ Top 100 Resilient   │
│  ☐ Featured in Stories │
│                        │
│  ────────────────────  │
│                        │
│  [Reset] [Apply]       │
└────────────────────────┘
```

**Right Sidebar - Info Panel (Dynamic)**

*No Selection State:*
```
┌──────────────────────────┐
│  About This Map          │
│  ──────────────────────  │
│                          │
│  Click on any census     │
│  tract to see detailed   │
│  resilience data.        │
│                          │
│  Or search by address    │
│  in the bar above.       │
│                          │
│  [View Data Table]       │
└──────────────────────────┘
```

*Tract Selected State:*
```
┌──────────────────────────┐
│  Census Tract 26163523900│
│  ──────────────────────  │
│  Detroit, MI             │
│  Wayne County            │
│                          │
│  Resilience Score        │
│  +2.34                   │
│  Very High Resilience    │
│  ████████ 95th percentile│
│                          │
│  Health Burden: 0.42     │
│  Population: 5,234       │
│                          │
│  ──────────────────────  │
│  Why is this high?       │
│  • Better health outcomes│
│    than predicted        │
│  • Strong community      │
│    networks likely       │
│                          │
│  ──────────────────────  │
│  Related Stories         │
│  • Urban Garden Network  │
│    Transforms Food Desert│
│    [Read →]              │
│                          │
│  ──────────────────────  │
│  [Share Link]            │
│  [Export Data]           │
│  [Close ✕]               │
└──────────────────────────┘
```

**Mobile Layout (Stacked)**
```
┌──────────────────────────────┐
│  [≡ Filters]  [ℹ Info]      │  ← Tabs toggle panels
├──────────────────────────────┤
│                              │
│       MAP (Full width)       │
│                              │
│  [Search bar overlay]        │
│                              │
└──────────────────────────────┘
[Tapping Filters or Info opens bottom sheet]
```

**View Toggle (Below nav, above map)**
```
Map View  |  Data Table  |  Statistics
   ●            ○              ○
```

**Data Table View:**
- Sortable columns: FIPS, State, County, Population, Score, Category
- Pagination (50 per page)
- Export to CSV option
- Click row to select on map

**Statistics View:**
- Distribution charts (histogram of scores)
- Top 20 resilient tracts table
- State-by-state comparison
- Correlation visualizations

#### Key Changes:
- Add persistent filter panel for exploration
- Add info panel that stays visible (not just popup)
- Add view toggle (Map | Table | Stats)
- Collapse sidebars on mobile, use tabs/bottom sheets
- Add "Related Stories" link when tract has associated story

---

### 4.3 Stories Page (/stories) - Narrative Connection

**Current Problems:**
- Stories feel disconnected from data
- No filtering by category
- Limited context about why these tracts are resilient
- Can't submit community stories easily

**Redesign Strategy:**
Create rich story experience with clear connection to map data.

#### Layout Structure:

**Hero Section**
```
┌──────────────────────────────────────────────────────────────────┐
│  Community Stories                                               │
│                                                                  │
│  Real examples of resilience from communities across America.   │
│  These stories highlight innovative solutions that improve       │
│  health, food access, and quality of life.                      │
│                                                                  │
│  [Submit Your Story]                                             │
└──────────────────────────────────────────────────────────────────┘
```

**Filter Tabs**
```
All Stories  |  Health  |  Food Access  |  Community  |  Economic
     ●            ○           ○              ○             ○
```

**Story Cards (Grid, 2-col on desktop, 1-col mobile)**
```
┌──────────────────────────────────────────────────────────────────┐
│  ┌──────────────────────────┐  ┌──────────────────────────┐     │
│  │ [Image or illustration]  │  │ [Image]                  │     │
│  │                          │  │                          │     │
│  │ [HEALTH] Detroit, MI     │  │ [FOOD ACCESS] El Paso, TX│     │
│  │                          │  │                          │     │
│  │ Urban Garden Network     │  │ Community Health Workers │     │
│  │ Transforms Food Desert   │  │ Bridge the Gap          │     │
│  │                          │  │                          │     │
│  │ A coalition of neighbor- │  │ Promotoras reduced      │     │
│  │ hood associations...     │  │ diabetes...             │     │
│  │                          │  │                          │     │
│  │ Census Tract: 26163523900│  │ Census Tract: 48141003701│    │
│  │ Resilience Score: +2.34  │  │ Resilience Score: +1.89  │     │
│  │                          │  │                          │     │
│  │ [Read Full Story →]      │  │ [Read Full Story →]      │     │
│  │ [View on Map →]          │  │ [View on Map →]          │     │
│  └──────────────────────────┘  └──────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

**Individual Story Page (/stories/[id])**
```
┌──────────────────────────────────────────────────────────────────┐
│  ← Back to Stories                                               │
│                                                                  │
│  Urban Garden Network Transforms Food Desert                     │
│  Detroit, MI • Wayne County • Census Tract 26163523900           │
│                                                                  │
│  [FOOD ACCESS]  Resilience Score: +2.34 (Very High)             │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │         [Hero Image or Photo Gallery]                      │ │
│  │                                                             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [Full story content in readable typography]                    │
│                                                                  │
│  A coalition of neighborhood associations converted vacant      │
│  lots into productive community gardens, increasing fresh       │
│  produce access for over 5,000 residents...                     │
│                                                                  │
│  ────────────────────────────────────────────────────────────   │
│                                                                  │
│  The Data Behind the Story                                      │
│                                                                  │
│  This census tract shows significantly better health outcomes   │
│  than its socioeconomic profile would predict:                  │
│                                                                  │
│  • Resilience Score: +2.34 (95th percentile)                    │
│  • Health Burden: 0.42 (lower than expected)                    │
│  • Food Access: Low-income, low-access (food desert)            │
│  • Population: 5,234                                             │
│                                                                  │
│  [View This Tract on the Map →]                                 │
│  [Explore Similar Communities →]                                │
│                                                                  │
│  ────────────────────────────────────────────────────────────   │
│                                                                  │
│  More Stories Like This                                          │
│  [Related story cards...]                                        │
└──────────────────────────────────────────────────────────────────┘
```

**Submit Story CTA (Prominent)**
```
┌──────────────────────────────────────────────────────────────────┐
│  Share Your Community's Story                                    │
│                                                                  │
│  Does your community have a resilience success story? We'd      │
│  love to hear about initiatives making a difference.            │
│                                                                  │
│  [Submit a Story →]                                              │
│                                                                  │
│  (Links to form or email with template)                         │
└──────────────────────────────────────────────────────────────────┘
```

#### Key Changes:
- Add category filtering
- Expand to full story pages (not just cards)
- Add "Data Behind the Story" section linking to map
- Add "Similar Communities" discovery
- Make submit CTA more prominent
- Add images/illustrations for visual appeal

---

### 4.4 Learn Page (/learn) - Methodology Hub

**Current Problems:**
- 600+ lines of dense content with no navigation
- Can't jump to specific sections
- Researchers and casual users mixed together
- No visual explanations

**Redesign Strategy:**
Use tabbed interface with sticky table of contents for scanability.

#### Layout Structure:

**Tab Navigation (Sticky below header)**
```
┌──────────────────────────────────────────────────────────────────┐
│  Overview  |  Methodology  |  Limitations  |  FAQ               │
│     ●             ○              ○           ○                   │
└──────────────────────────────────────────────────────────────────┘
```

**OVERVIEW TAB (For casual learners)**
```
┌──────────────────────────────────────────────────────────────────┐
│  Understanding Community Resilience                              │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  What We're Measuring                                       │ │
│  │                                                             │ │
│  │  [Visual diagram showing:]                                  │ │
│  │  Socioeconomic Factors → Predicted Health → Actual Health  │ │
│  │                                ↑                            │ │
│  │                        Resilience Gap                       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  The Research Question                                           │
│  Which communities have better health outcomes than their       │
│  material circumstances predict?                                │
│                                                                  │
│  [Expandable sections with visual aids]                         │
│  ▼ How We Define Resilience                                     │
│  ▼ What the Scores Mean                                         │
│  ▼ Where the Data Comes From                                    │
│  ▼ Why This Matters                                             │
│                                                                  │
│  ────────────────────────────────────────────────────────────   │
│  Key Findings                                                    │
│  • 1,059 food deserts show high resilience                      │
│  • Geographic diversity in top performers                       │
│  • Social factors matter beyond income                          │
│                                                                  │
│  [Want the details? → Go to Methodology tab]                    │
└──────────────────────────────────────────────────────────────────┘
```

**METHODOLOGY TAB (For researchers)**

*Desktop: 2-column layout with sticky TOC*
```
┌─────────┬────────────────────────────────────────────────────────┐
│  TOC    │  Content                                               │
│ (Sticky)│                                                        │
│         │  Methodology                                           │
│ • Data  │                                                        │
│   Sources│  ────────────────────────────────────────────────   │
│ • Health│                                                        │
│   Burden│  Data Sources                                         │
│   Index │                                                        │
│ • Model │  We combine data from three primary sources:          │
│ • Excl- │                                                        │
│   usions│  CDC PLACES 2023                                      │
│ • Score │  Census tract-level health outcomes including         │
│   Calc. │  diabetes, obesity, mental health...                  │
│         │                                                        │
│ [Jump   │  [Detailed content continues...]                      │
│  to     │                                                        │
│  section│  ────────────────────────────────────────────────     │
│  on     │  Health Burden Index                                  │
│  click] │  ...                                                   │
│         │                                                        │
│ 200px   │  (Scrollable, TOC highlights current section)         │
└─────────┴────────────────────────────────────────────────────────┘
```

*Mobile: Dropdown TOC*
```
┌──────────────────────────────────┐
│  [▼ Jump to Section...]          │
├──────────────────────────────────┤
│                                  │
│  Methodology                     │
│                                  │
│  Data Sources                    │
│  ...                             │
└──────────────────────────────────┘
```

**Content Organization:**

1. Data Sources (expandable cards)
   - CDC PLACES 2023 (with link)
   - USDA Food Access Research Atlas 2019 (with link)
   - Census ACS 2020 (with link)

2. Health Burden Index
   - What it measures (bullet list)
   - How it's calculated (formula in plain language)
   - Visual: bar chart showing components

3. Statistical Model
   - Regression equation (formatted nicely)
   - What each variable means (glossary)
   - Visual: regression plot example

4. Score Calculation
   - Residual explanation (plain language)
   - Z-score transformation (visual)
   - Interpretation guide

5. Exclusion Criteria
   - Group quarters threshold
   - Why this matters

**LIMITATIONS TAB**
```
┌──────────────────────────────────────────────────────────────────┐
│  Understanding the Limitations                                   │
│                                                                  │
│  [Important: Read before using this data]                       │
│                                                                  │
│  ▼ Temporal Gaps                                                │
│     Health (2023) vs Food Access (2019) vs Census (2020)       │
│     Impact: Changes may not reflect current conditions          │
│                                                                  │
│  ▼ Model-Based Estimates                                        │
│     CDC PLACES uses statistical modeling, not direct measures   │
│     Impact: Some tract estimates have high uncertainty          │
│                                                                  │
│  ▼ Ecological Fallacy                                           │
│     Tract patterns ≠ individual outcomes                        │
│     Impact: Cannot predict individual health                    │
│                                                                  │
│  [Continue for all limitations...]                              │
│                                                                  │
│  ────────────────────────────────────────────────────────────   │
│                                                                  │
│  Appropriate vs Inappropriate Uses                              │
│                                                                  │
│  ✓ DO use for:                    ✗ DO NOT use for:            │
│  • Exploratory research           • Justifying disinvestment   │
│  • Identifying communities        • Individual predictions      │
│  • Asset-based planning           • Punitive comparisons       │
│  ...                              ...                           │
└──────────────────────────────────────────────────────────────────┘
```

**FAQ TAB**
```
┌──────────────────────────────────────────────────────────────────┐
│  Frequently Asked Questions                                      │
│                                                                  │
│  [Search FAQs...]                                                │
│                                                                  │
│  General Questions                                               │
│  ────────────────────                                            │
│  ▼ What is a census tract?                                      │
│  ▼ How often is this data updated?                              │
│  ▼ Can I use this for my community?                             │
│                                                                  │
│  Technical Questions                                             │
│  ────────────────────                                            │
│  ▼ Why use OLS regression instead of other methods?             │
│  ▼ How do you handle missing data?                              │
│  ▼ What is a "standardized residual"?                           │
│                                                                  │
│  Data Questions                                                  │
│  ────────────────────                                            │
│  ▼ Where can I download the raw data?                           │
│  ▼ How do I cite this project?                                  │
│  ▼ Is there an API?                                             │
│     Yes! See our [API Documentation →]                          │
│                                                                  │
│  [Didn't find your answer? Contact us →]                        │
└──────────────────────────────────────────────────────────────────┘
```

#### Key Changes:
- Split into 4 tabs (Overview, Methodology, Limitations, FAQ)
- Add sticky TOC to Methodology tab
- Use expandable sections to reduce overwhelming walls of text
- Add visual diagrams to Overview
- Create dedicated FAQ section
- Make citation info easy to find

---

### 4.5 For Developers Page (/developers) - API Documentation

**Current Problems:**
- API endpoints buried at bottom of homepage
- No code examples
- No information about rate limits, errors, parameters

**Redesign Strategy:**
Create dedicated, developer-friendly API docs with interactive examples.

#### Layout Structure:

**Hero Section**
```
┌──────────────────────────────────────────────────────────────────┐
│  API Documentation                                               │
│                                                                  │
│  Access community resilience data programmatically via our      │
│  REST API. All endpoints return JSON.                           │
│                                                                  │
│  Base URL: https://resilience-mapping.fly.dev                   │
│  Rate Limit: 100 requests/minute                                │
│  Authentication: None required (public data)                     │
└──────────────────────────────────────────────────────────────────┘
```

**Tab Navigation**
```
Quick Start  |  Endpoints  |  Code Examples  |  Data Schema
      ●            ○              ○                 ○
```

**QUICK START TAB**
```
┌──────────────────────────────────────────────────────────────────┐
│  Getting Started                                                 │
│                                                                  │
│  1. Try Your First Request                                       │
│                                                                  │
│  curl https://resilience-mapping.fly.dev/api/stats              │
│                                                                  │
│  [Copy]  [Try it →]                                              │
│                                                                  │
│  2. Explore Census Tracts                                        │
│                                                                  │
│  curl "https://resilience-mapping.fly.dev/api/tracts?limit=10"  │
│                                                                  │
│  [Copy]  [Try it →]                                              │
│                                                                  │
│  3. Geocode an Address                                           │
│                                                                  │
│  curl "https://resilience-mapping.fly.dev/api/geocode?\          │
│        address=1600+Pennsylvania+Ave+NW+Washington+DC"           │
│                                                                  │
│  [Copy]  [Try it →]                                              │
│                                                                  │
│  ────────────────────────────────────────────────────────────   │
│  Rate Limiting                                                   │
│  • 100 requests per minute per IP                               │
│  • 429 status returned if exceeded                              │
│  • X-RateLimit-* headers included in responses                  │
│                                                                  │
│  Error Handling                                                  │
│  All errors return { "success": false, "error": "message" }     │
└──────────────────────────────────────────────────────────────────┘
```

**ENDPOINTS TAB (Accordion style)**
```
┌──────────────────────────────────────────────────────────────────┐
│  ▼ GET /api/stats                                                │
│     Get aggregate statistics for the dataset                     │
│                                                                  │
│     No parameters required                                       │
│                                                                  │
│     Response:                                                    │
│     {                                                            │
│       "success": true,                                           │
│       "data": {                                                  │
│         "totalTracts": 64419,                                    │
│         "stateCount": 51,                                        │
│         "avgResilience": 5.7,                                    │
│         "totalPopulation": 331893745                             │
│       }                                                          │
│     }                                                            │
│                                                                  │
│     [Try it in the API Explorer →]                              │
│                                                                  │
│  ────────────────────────────────────────────────────────────   │
│                                                                  │
│  ▼ GET /api/tracts                                               │
│     Get paginated list of census tracts with resilience scores  │
│                                                                  │
│     Query Parameters:                                            │
│     • limit (integer, default 100, max 1000)                    │
│     • offset (integer, default 0)                               │
│     • state (string, 2-letter code, optional)                   │
│     • minScore (float, optional)                                │
│     • maxScore (float, optional)                                │
│     • sortBy (string, optional: score|population|fips)          │
│     • order (string, optional: asc|desc)                        │
│                                                                  │
│     Example:                                                     │
│     /api/tracts?limit=50&state=CA&minScore=1.0&sortBy=score    │
│                                                                  │
│     Response:                                                    │
│     {                                                            │
│       "success": true,                                           │
│       "data": [...],                                             │
│       "pagination": {                                            │
│         "limit": 50,                                             │
│         "offset": 0,                                             │
│         "total": 8057                                            │
│       }                                                          │
│     }                                                            │
│                                                                  │
│  ────────────────────────────────────────────────────────────   │
│                                                                  │
│  [Continue for all endpoints...]                                │
└──────────────────────────────────────────────────────────────────┘
```

**CODE EXAMPLES TAB**

*Language Selector*
```
JavaScript  |  Python  |  R  |  cURL
     ●          ○        ○      ○
```

*Example for /api/tracts (JavaScript)*
```javascript
// Fetch top 10 resilient tracts in California
const response = await fetch(
  'https://resilience-mapping.fly.dev/api/tracts?' +
  new URLSearchParams({
    state: 'CA',
    minScore: 2.0,
    limit: 10,
    sortBy: 'score',
    order: 'desc'
  })
);

const data = await response.json();

if (data.success) {
  data.data.forEach(tract => {
    console.log(`${tract.fips}: ${tract.resilience_score}`);
  });
}

[Copy Code]  [Run in CodeSandbox →]
```

*Example for /api/geocode (Python)*
```python
import requests

# Geocode an address and get resilience data
response = requests.get(
    'https://resilience-mapping.fly.dev/api/geocode',
    params={'address': '1600 Pennsylvania Ave NW, Washington, DC'}
)

data = response.json()

if data['success'] and data['results']:
    result = data['results'][0]
    print(f"Tract: {result['tractFips']}")
    print(f"Score: {result['resilienceScore']}")

[Copy Code]  [Download Notebook →]
```

**DATA SCHEMA TAB**
```
┌──────────────────────────────────────────────────────────────────┐
│  Tract Object Schema                                             │
│                                                                  │
│  {                                                               │
│    "fips": "string (11 digits)",                                │
│    "state": "string (2 letters)",                               │
│    "state_name": "string",                                       │
│    "county": "string (3 digits)",                               │
│    "tract": "string (6 digits)",                                │
│    "population": "integer",                                      │
│    "resilience_score": "float | null",                          │
│    "score_category": "enum (very-high|high|medium|low|...)",    │
│    "burden": "float | null",                                     │
│    "is_lila": "boolean",                                         │
│    "group_quarters_pct": "float",                               │
│    "percentile": "integer (0-100) | null"                       │
│  }                                                               │
│                                                                  │
│  Score Category Values:                                          │
│  • "very-high": ≥ 2.0                                           │
│  • "high": 1.0 to 2.0                                           │
│  • "medium": 0.0 to 1.0                                         │
│  • "low": -1.0 to 0.0                                           │
│  • "very-low": < -1.0                                           │
│  • "no-data": null resilience_score                             │
│                                                                  │
│  [Download Full Schema (JSON Schema) →]                         │
└──────────────────────────────────────────────────────────────────┘
```

**API Explorer (Interactive, optional enhancement)**
```
┌──────────────────────────────────────────────────────────────────┐
│  Interactive API Explorer                                        │
│                                                                  │
│  Endpoint: [/api/tracts ▼]                                       │
│                                                                  │
│  Parameters:                                                     │
│  limit:  [100        ]                                           │
│  offset: [0          ]                                           │
│  state:  [CA         ]                                           │
│  minScore: [1.0      ]                                           │
│                                                                  │
│  [Execute Request]                                               │
│                                                                  │
│  Response:                                                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ {                                                           │ │
│  │   "success": true,                                          │ │
│  │   "data": [...]                                             │ │
│  │ }                                                           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [Copy cURL]  [Copy JavaScript]  [Copy Python]                  │
└──────────────────────────────────────────────────────────────────┘
```

#### Key Changes:
- Dedicated page (not buried on homepage)
- Tabbed organization (Quick Start, Endpoints, Examples, Schema)
- Code examples in multiple languages
- Interactive API explorer
- Clear documentation of parameters, responses, errors
- Rate limit information upfront

---

### 4.6 About Page (/about) - Project Information

**Current Problem:**
- Currently mixed with methodology (creating 600+ line page)

**Redesign Strategy:**
Focus on project background, team, contact, terms - NOT methodology.

#### Layout Structure:

```
┌──────────────────────────────────────────────────────────────────┐
│  About This Project                                              │
│                                                                  │
│  Background                                                      │
│  Community Resilience Mapping is a data-driven exploration      │
│  of communities that thrive despite challenging circumstances.  │
│  [2-3 paragraphs about project origins and goals]               │
│                                                                  │
│  ────────────────────────────────────────────────────────────   │
│                                                                  │
│  The Team                                                        │
│  [Team member cards with photos, roles, links]                  │
│                                                                  │
│  ────────────────────────────────────────────────────────────   │
│                                                                  │
│  Citation                                                        │
│  If you use this data in research or reporting, please cite:    │
│                                                                  │
│  [Citation box with copy button]                                │
│                                                                  │
│  ────────────────────────────────────────────────────────────   │
│                                                                  │
│  Contact                                                         │
│  • General inquiries: hello@resilience-mapping.org              │
│  • Story submissions: stories@resilience-mapping.org            │
│  • Technical support: support@resilience-mapping.org            │
│  • GitHub: [link]                                               │
│                                                                  │
│  ────────────────────────────────────────────────────────────   │
│                                                                  │
│  Terms of Use                                                    │
│  This data is provided for public benefit under [License].      │
│  [Expandable legal terms]                                       │
│                                                                  │
│  Privacy Policy                                                  │
│  [Expandable privacy info]                                      │
└──────────────────────────────────────────────────────────────────┘
```

---

## 5. User Journey Flows

### 5.1 Community Organizer Journey (Maya)

**Goal:** Understand resilience in her Detroit neighborhood

```
Entry Point: Homepage
    ↓
    Types address in hero search bar
    ↓
Lands on: Explore page with her tract selected
    ↓
    Views resilience score in right sidebar
    ↓
    Clicks "Related Stories"
    ↓
Lands on: Urban Garden Network story
    ↓
    Reads full story
    ↓
    Clicks "View Similar Communities"
    ↓
Back to: Explore page with filter applied (high resilience + food deserts)
    ↓
    Clicks "Share Link"
    ↓
    Copies URL to share with community board
```

**Key Improvements:**
- Address search available immediately on homepage
- Related stories linked from tract details
- Sharing functionality built-in
- Can discover similar communities

### 5.2 Academic Researcher Journey (Dr. Chen)

**Goal:** Understand methodology and cite the project

```
Entry Point: Homepage
    ↓
    Clicks "I want to learn the methodology"
    ↓
Lands on: Learn page > Methodology tab
    ↓
    Uses sticky TOC to jump to "Statistical Model"
    ↓
    Reads model details
    ↓
    Clicks "Limitations" tab to understand constraints
    ↓
    Reviews appropriate uses
    ↓
    Clicks "FAQ" tab
    ↓
    Searches "How do I cite"
    ↓
    Clicks citation link in FAQ
    ↓
Lands on: About page > Citation section
    ↓
    Copies citation to clipboard
```

**Key Improvements:**
- Methodology separated into Learn page
- Sticky TOC allows quick navigation
- Tabs prevent overwhelming single page
- Citation easy to find via FAQ or About page

### 5.3 Data Journalist Journey (Sam)

**Goal:** Find story about resilient food deserts

```
Entry Point: Homepage
    ↓
    Sees "1,059 resilient food deserts" insight card
    ↓
    Clicks "Explore →"
    ↓
Lands on: Explore page with filter pre-applied
    ↓
    Uses left sidebar filters to refine:
    ☑ Food Deserts (LILA)
    ○ Very High (≥2.0)
    ↓
    Map updates to show matching tracts
    ↓
    Clicks tract in Detroit
    ↓
    Right sidebar shows:
    - Score details
    - Related story link
    ↓
    Clicks "Urban Garden Network" story
    ↓
Lands on: Full story page
    ↓
    Reads "Data Behind the Story" section
    ↓
    Clicks "Explore Similar Communities"
    ↓
Back to: Explore page with new filter
    ↓
    Switches to "Data Table" view
    ↓
    Exports to CSV for analysis
```

**Key Improvements:**
- Insight cards on homepage provide story hooks
- Powerful filters enable pattern discovery
- Stories and data are explicitly linked
- Multiple views (map, table, export) support different work styles

### 5.4 Developer Journey (Alex)

**Goal:** Integrate resilience data into existing app

```
Entry Point: Homepage
    ↓
    Clicks "I want to use the data/API"
    ↓
Lands on: For Developers page > Quick Start tab
    ↓
    Copies curl example
    ↓
    Tests in terminal
    ↓
    Clicks "Endpoints" tab
    ↓
    Expands GET /api/tracts
    ↓
    Reviews query parameters
    ↓
    Clicks "Code Examples" tab
    ↓
    Selects "Python"
    ↓
    Copies Python code
    ↓
    Clicks "Data Schema" tab
    ↓
    Reviews tract object structure
    ↓
    Downloads JSON Schema file
    ↓
    Implements integration
```

**Key Improvements:**
- Dedicated API page (not buried)
- Progressive learning path (Quick Start → Details → Examples → Schema)
- Code examples in multiple languages
- Downloadable schema for validation

### 5.5 Casual Explorer Journey (Jordan)

**Goal:** Learn what this is and check out their neighborhood

```
Entry Point: Homepage via social media
    ↓
    Reads hero: "Discovering hidden strengths in communities"
    ↓
    Intrigued, types their address in search
    ↓
Lands on: Explore page with their tract
    ↓
    Sees score: +0.34 (Medium Resilience)
    ↓
    Wonders "what does this mean?"
    ↓
    Clicks "Learn More" link in sidebar
    ↓
Lands on: Learn page > Overview tab
    ↓
    Sees visual diagram of resilience concept
    ↓
    Expands "What the Scores Mean"
    ↓
    Understands their community is "slightly better than predicted"
    ↓
    Curious about success stories
    ↓
    Clicks "Stories" in main nav
    ↓
Lands on: Stories page
    ↓
    Browses inspiring examples
    ↓
    Shares Detroit story on social media
```

**Key Improvements:**
- Clear value proposition in hero
- Immediate engagement via search
- "Learn More" contextually available when viewing results
- Overview tab provides accessible entry point to methodology
- Easy path to inspiring stories

---

## 6. Wireframe Descriptions

### 6.1 Global Header (All Pages)

**Desktop (1200px+)**
```
┌───────────────────────────────────────────────────────────────┐
│  [Logo Icon] Community Resilience Mapping                     │
│                                                                │
│         Explore    Stories    Learn    For Developers    About│
│                                                       [Search]│
└───────────────────────────────────────────────────────────────┘
Height: 64px
Background: Linear gradient #0f172a → #1e293b
Logo: 32px icon + text
Nav links: 16px, 24px spacing, emerald (#10b981) on hover
Search icon: Opens modal overlay with address search
Active page: 3px emerald bottom border
```

**Tablet (768px - 1199px)**
```
┌───────────────────────────────────────┐
│  [Logo] CRM                  [Search] │
│                                       │
│  Explore  Stories  Learn  Dev   About │
└───────────────────────────────────────┘
Height: 56px
Logo: Abbreviated "CRM"
Nav links: 14px, compressed spacing
```

**Mobile (< 768px)**
```
┌───────────────────────────────────────┐
│  ☰  CRM                     [Search]  │
└───────────────────────────────────────┘
Height: 56px
Hamburger: Left side, opens full-screen menu
Search: Right side, opens full-screen search
```

### 6.2 Homepage Hero Section

**Desktop**
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                                                                 │
│              Community Resilience Mapping                       │
│              ─────────────────────────                          │
│                                                                 │
│     Discovering the hidden strengths in communities            │
│          that help them thrive against the odds                │
│                                                                 │
│                                                                 │
│      ┌────────────────────────────────────────┐               │
│      │  Enter your address or zip code...     │  [Search]     │
│      └────────────────────────────────────────┘               │
│                                                                 │
│                                                                 │
│              or  [Browse the Map]  [Read Stories]              │
│                                                                 │
│                                                                 │
│                            ↓                                    │
│                    Scroll to learn more                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
Viewport height: 100vh
Typography: H1 48px bold, subtitle 20px light
Search bar: 500px wide, 56px tall, emerald focus state
CTAs: Outlined buttons, 48px tall
Background: Subtle gradient with abstract map pattern (low opacity)
```

### 6.3 Explore Page - 3 Column Layout (Desktop)

**Full Layout**
```
┌────┬──────────────────────────────────────────────────┬─────────┐
│ F  │                                                   │   I    │
│ I  │                                                   │   N    │
│ L  │                                                   │   F    │
│ T  │              INTERACTIVE MAP                      │   O    │
│ E  │                                                   │        │
│ R  │   ┌─────────────────────┐                        │   P    │
│ S  │   │ [Address search]    │                        │   A    │
│    │   └─────────────────────┘                        │   N    │
│    │                                                   │   E    │
│ 280│                                                   │   L    │
│ px │   [Legend]        [Zoom controls]                │        │
│    │   [bottom-left]   [top-right]                    │  320px │
│    │                                                   │        │
│    │                                                   │        │
│    │                                                   │        │
│    │                                                   │        │
└────┴──────────────────────────────────────────────────┴─────────┘

Left Panel (Filters):
- Collapsible sections
- Checkboxes, radio buttons, dropdowns
- Apply/Reset buttons at bottom
- Collapses to 40px icon bar when closed

Center (Map):
- Full-bleed map canvas
- Overlay controls (search, legend, zoom)
- Touch/mouse interactions
- Tract selection with visual highlight

Right Panel (Info):
- Dynamic content based on selection
- Sticky header with tract ID
- Scrollable details section
- Action buttons at bottom
- Collapses to icon when no selection
```

### 6.4 Learn Page - Tabbed Interface

**Tab Bar (Sticky)**
```
┌──────────────────────────────────────────────────────────────┐
│  Overview  |  Methodology  |  Limitations  |  FAQ            │
│     ●             ○              ○           ○               │
└──────────────────────────────────────────────────────────────┘
Position: Sticky, 8px below header
Height: 48px
Active tab: Emerald indicator, bold font
Background: White with bottom shadow
```

**Methodology Tab with TOC (Desktop)**
```
┌─────────────┬───────────────────────────────────────────────┐
│ • Data      │  Methodology                                  │
│   Sources   │                                               │
│             │  Data Sources                                 │
│ • Health    │  ═════════════                                │
│   Burden    │                                               │
│   Index     │  We combine data from three primary sources:  │
│             │                                               │
│ • Statistical│  [CDC PLACES 2023 expandable card]          │
│   Model     │  [USDA Food Access expandable card]          │
│             │  [Census ACS 2020 expandable card]           │
│ • Exclusion │                                               │
│   Criteria  │                                               │
│             │  Health Burden Index                          │
│ • Score     │  ════════════════════                         │
│   Calc.     │                                               │
│             │  We construct a composite index (0-1) from:  │
│   200px     │  • Chronic disease prevalence...             │
│   sticky    │  • Mental health indicators...               │
│             │                                               │
│  [Active    │  [Visual: bar chart of components]           │
│   section   │                                               │
│   highlight]│  ...                                          │
│             │                                               │
└─────────────┴───────────────────────────────────────────────┘

TOC (Left):
- Sticky position as user scrolls
- Active section highlighted
- Smooth scroll on click
- Collapses to dropdown on mobile

Content (Right):
- Max width 800px for readability
- Expandable cards for data sources
- Visual aids (charts, diagrams)
- Code blocks with syntax highlighting
- Liberal use of white space
```

### 6.5 For Developers Page - Code Examples

**Code Block Pattern**
```
┌──────────────────────────────────────────────────────────────┐
│  Fetch Top Resilient Tracts in California                   │
│  ────────────────────────────────────────────────────────   │
│                                                              │
│  JavaScript  |  Python  |  R  |  cURL                       │
│      ●           ○        ○      ○                          │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  1  // Fetch top 10 resilient tracts in California    │ │
│  │  2  const response = await fetch(                     │ │
│  │  3    'https://resilience-mapping.fly.dev/api/tracts?'│ │
│  │  4    + new URLSearchParams({                         │ │
│  │  5      state: 'CA',                                  │ │
│  │  6      minScore: 2.0,                                │ │
│  │  7      limit: 10,                                    │ │
│  │  8      sortBy: 'score',                              │ │
│  │  9      order: 'desc'                                 │ │
│  │ 10    })                                              │ │
│  │ 11  );                                                │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  [Copy Code]  [Open in CodeSandbox]                         │
└──────────────────────────────────────────────────────────────┘

Code Block Specs:
- Syntax highlighting (VS Code Dark+ theme)
- Line numbers
- Copy button (top-right)
- Optional "Try it" integration
- Monospace font: Fira Code or SF Mono
- Background: #1e1e1e (dark) or #f6f8fa (light mode)
```

### 6.6 Mobile-Specific Patterns

**Bottom Sheet for Filters (Explore page mobile)**
```
┌──────────────────────────────┐
│                              │
│         MAP AREA             │
│                              │
│  [Tap to expand filters ↑]   │
└──────────────────────────────┘
          ↓ Tap
┌──────────────────────────────┐
│  [Drag handle]               │
│  Filters                  [✕]│
│  ─────────────────────────   │
│                              │
│  Resilience Score            │
│  ○ All                       │
│  ○ Very High                 │
│  ...                         │
│                              │
│  [Apply Filters]             │
└──────────────────────────────┘

Sheet Behavior:
- Slides up from bottom
- Drag handle for gesture control
- 3 states: collapsed (showing tab), half (showing filters), full (all options)
- Backdrop dim when expanded
- Swipe down to close
```

**Mobile Navigation Menu**
```
[Trigger: Tap ☰]
┌──────────────────────────────┐
│  ✕  Menu                     │  ← Slide in from left
├──────────────────────────────┤
│                              │
│  🗺️  Explore                 │  ← 56px tall touch targets
│  ─────────────────────────   │
│  📖  Stories                 │
│  ─────────────────────────   │
│  🎓  Learn                   │
│  ─────────────────────────   │
│  💻  For Developers          │
│  ─────────────────────────   │
│  ℹ️  About                   │
│                              │
│  ═════════════════════════   │
│                              │
│  🔍  Search by Address       │  ← Full-width search at bottom
│      [Search...]             │
│                              │
└──────────────────────────────┘

Menu Specs:
- Full-screen overlay
- Slide-in animation (300ms ease-out)
- Backdrop: 70% opacity black
- Tap outside to close
- Icons for visual hierarchy
- Search promoted for quick access
```

---

## 7. Progressive Disclosure Strategy

### 7.1 Progressive Disclosure Principles

**Level 1 - Essential (Homepage, Overview tab)**
- What is this?
- Why does it matter?
- How do I start?
- No jargon, simple language

**Level 2 - Intermediate (Explore page, Stories)**
- How do scores work?
- What makes a community resilient?
- Examples and patterns
- Some technical terms with definitions

**Level 3 - Advanced (Methodology tab, API docs)**
- Statistical methods
- Data sources and processing
- Limitations and caveats
- Technical implementation details

### 7.2 Specific Disclosure Patterns

**Expandable Sections**
```
▼ What is a census tract?
  A census tract is a small geographic area containing
  2,500-8,000 people, designed for statistical purposes.
  [Link to Census.gov for more details]

▼ How do you calculate the resilience score?
  [Brief explanation in plain language]
  [Link to Methodology tab for full details]
```

**Tooltips for Technical Terms**
```
The resilience score [ℹ] is calculated as a standardized residual.

[Hover/tap ℹ shows:]
"Standardized residual: The difference between actual and
predicted health, expressed in standard deviations (z-score)"
```

**Stepped Learning Paths**
```
Homepage:
  "Communities that thrive against the odds"

Overview Tab:
  "Resilience is when a community has better health
   outcomes than predicted by income, education, etc."

Methodology Tab:
  "We use OLS regression with state fixed effects to
   model health burden as a function of socioeconomic
   factors, then calculate standardized residuals..."
```

**Contextual "Learn More" Links**
```
[On Explore page, when tract is selected:]

Resilience Score: +2.34 (Very High)
[What does this mean? →]

[Links to Learn > Overview > "What the Scores Mean"]
```

**Layered Visualizations**
```
Level 1: Simple icon or diagram
  "Predicted health ← → Actual health = Resilience"

Level 2: Annotated chart
  [Bar chart showing components of health burden index]

Level 3: Interactive visualization
  [Regression plot with adjustable parameters]
```

### 7.3 Mobile-Specific Disclosure

**Accordion Menus**
- All sections collapsed by default on mobile
- Only one section open at a time to reduce scrolling
- Clear visual indicators (▶ closed, ▼ open)

**"Show More" Links**
```
Community Resilience Mapping identifies census tracts
with better health outcomes than predicted... [Show More]

[Expands to:]
...based on socioeconomic factors like income, education,
and healthcare access. We use statistical regression to
find communities that outperform expectations.
```

**Bottom Sheets for Details**
```
[On mobile map, tap tract]
┌──────────────────────────────┐
│  Tract 26163523900           │
│  Score: +2.34                │
│                              │
│  [View Full Details ↑]       │
└──────────────────────────────┘

[Tap to expand bottom sheet with complete info]
```

---

## 8. Implementation Priority

### Phase 1 - Critical Foundation (Weeks 1-3)

**Priority: Highest - Address core navigation issues**

1. **Global Navigation Component**
   - Create persistent header with nav links
   - Implement mobile hamburger menu
   - Add global search functionality
   - Estimated effort: 3 days

2. **Homepage Redesign**
   - Restructure to hero + pathways layout
   - Remove top tracts table (move to Explore)
   - Add address search to hero
   - Simplify CTAs
   - Estimated effort: 4 days

3. **Learn Page (Split from About)**
   - Create new /learn route
   - Implement tab navigation (Overview, Methodology, Limitations, FAQ)
   - Add sticky TOC to Methodology tab
   - Migrate content from current About page
   - Estimated effort: 5 days

4. **Basic Footer Navigation**
   - Create footer component with sitemap
   - Add to all pages
   - Estimated effort: 2 days

**Phase 1 Total: 14 days (3 weeks)**

**Success Criteria:**
- Users can navigate between pages without getting lost
- Methodology content is scannable with TOC
- Homepage clearly directs users to appropriate sections

---

### Phase 2 - Enhanced Explore Experience (Weeks 4-6)

**Priority: High - Enable discovery and exploration**

5. **Explore Page Redesign**
   - Implement 3-column layout (filters | map | info)
   - Create collapsible filter panel
   - Build persistent info panel (not just popup)
   - Add view toggle (Map | Table | Stats)
   - Estimated effort: 7 days

6. **Advanced Filtering**
   - Score range filters
   - Geographic filters (state, county)
   - Special interest filters (LILA, top 100, etc.)
   - Filter persistence in URL params
   - Estimated effort: 4 days

7. **Data Table View**
   - Sortable columns
   - Pagination
   - CSV export
   - Click row to select on map
   - Estimated effort: 3 days

**Phase 2 Total: 14 days (3 weeks)**

**Success Criteria:**
- Users can filter and explore patterns in the data
- Table view provides alternative to map
- Filters are intuitive and responsive

---

### Phase 3 - Stories & Connections (Weeks 7-8)

**Priority: Medium-High - Connect data to narrative**

8. **Enhanced Stories Page**
   - Add category filtering
   - Create full story page template
   - Add "Data Behind the Story" section
   - Link stories to map tracts
   - Estimated effort: 5 days

9. **Cross-Page Integration**
   - "Related Stories" in Explore info panel
   - "View on Map" from story pages
   - "Explore Similar Communities" links
   - Estimated effort: 3 days

**Phase 3 Total: 8 days (2 weeks)**

**Success Criteria:**
- Stories and data feel connected, not siloed
- Users can move fluidly between qualitative and quantitative
- Discovery paths lead between sections

---

### Phase 4 - Developer Experience (Weeks 9-10)

**Priority: Medium - Serve developer audience**

10. **For Developers Page**
    - Create /developers route
    - Implement Quick Start tab
    - Document all endpoints with parameters
    - Add code examples (JS, Python, R, cURL)
    - Create data schema documentation
    - Estimated effort: 6 days

11. **API Enhancements**
    - Add filtering query params to /api/tracts
    - Add rate limit headers
    - Improve error responses
    - Add CORS headers if needed
    - Estimated effort: 3 days

**Phase 4 Total: 9 days (2 weeks)**

**Success Criteria:**
- Developers can find API docs easily
- Code examples work copy-paste
- All endpoints thoroughly documented

---

### Phase 5 - Polish & Optimization (Weeks 11-12)

**Priority: Medium - Improve UX refinement**

12. **Mobile Optimization**
    - Bottom sheets for filters/info on mobile
    - Touch-optimized map controls
    - Mobile-specific navigation patterns
    - Performance testing on devices
    - Estimated effort: 4 days

13. **Accessibility Audit**
    - Keyboard navigation testing
    - Screen reader testing
    - ARIA label refinement
    - Color contrast validation
    - Focus management
    - Estimated effort: 3 days

14. **Performance Optimization**
    - Lazy loading optimizations
    - Image optimization
    - Bundle size reduction
    - Cache strategy refinement
    - Estimated effort: 2 days

**Phase 5 Total: 9 days (2 weeks)**

**Success Criteria:**
- Works well on mobile devices
- WCAG AA compliant
- Fast load times (<3s)

---

### Phase 6 - Advanced Features (Weeks 13-14)

**Priority: Low - Nice to have**

15. **Interactive API Explorer**
    - Build playground with parameter inputs
    - Live response preview
    - Code generation
    - Estimated effort: 4 days

16. **Advanced Visualizations**
    - Distribution charts on Statistics view
    - Correlation visualizations
    - Time series if data available
    - Estimated effort: 4 days

17. **Social Sharing**
    - Share specific tracts with metadata
    - Social media cards (Open Graph)
    - Direct link to filtered views
    - Estimated effort: 2 days

**Phase 6 Total: 10 days (2 weeks)**

**Success Criteria:**
- Enhanced engagement through sharing
- Developers can test API in browser
- Richer data exploration

---

### Implementation Timeline Summary

```
Phase 1: Weeks 1-3   (Critical Foundation)         ████████████░░░░░░░░░░░░
Phase 2: Weeks 4-6   (Enhanced Explore)            ░░░░░░░░░░░░████████████
Phase 3: Weeks 7-8   (Stories & Connections)       ░░░░░░░░░░░░░░░░░░░░████
Phase 4: Weeks 9-10  (Developer Experience)        ░░░░░░░░░░░░░░░░░░░░░░░░████
Phase 5: Weeks 11-12 (Polish & Optimization)       ░░░░░░░░░░░░░░░░░░░░░░░░░░░░████
Phase 6: Weeks 13-14 (Advanced Features)           ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████

Total: 14 weeks (3.5 months) for complete redesign
```

**Minimum Viable Redesign (MVP):**
Phases 1-3 (8 weeks) address all critical UX issues and provide significant improvement.

---

## 9. Success Metrics

### 9.1 User Engagement Metrics

**Navigation Effectiveness**
- Bounce rate from pages other than home (Target: <40%)
- Average pages per session (Target: >3.5)
- Users who navigate to 2+ sections (Target: >60%)

**Task Completion**
- Address searches completed (Target: >70% of initiated)
- Stories read to completion (Target: >50%)
- API docs visited by repeat users (Target: >30%)

**Content Discoverability**
- % users who find Methodology tab when on Learn page (Target: >80%)
- % users who filter on Explore page (Target: >40%)
- Story-to-map navigation rate (Target: >25%)

### 9.2 Usability Metrics

**Navigation**
- Time to find Methodology from homepage (Target: <15 seconds)
- Time to find API documentation (Target: <10 seconds)
- Navigation errors (dead ends, back button reliance) (Target: <10% of sessions)

**Mobile Experience**
- Mobile bounce rate compared to desktop (Target: <15% difference)
- Mobile task completion rate (Target: >85% of desktop rate)
- Touch target errors (Target: <5% of interactions)

**Accessibility**
- Keyboard-only navigation success rate (Target: 100%)
- Screen reader error rate (Target: <5%)
- Color contrast compliance (Target: 100% WCAG AA)

### 9.3 Persona-Specific Metrics

**Community Organizer (Maya)**
- Address search to tract details time (Target: <10 seconds)
- Tract link sharing rate (Target: >15%)
- Related story click-through (Target: >30%)

**Academic Researcher (Dr. Chen)**
- Methodology page time-on-page (Target: >3 minutes)
- TOC usage rate (Target: >60%)
- Citation copy rate (Target: >40% of Learn page visitors)

**Data Journalist (Sam)**
- Filter application rate (Target: >50%)
- Data table view usage (Target: >25%)
- CSV export rate (Target: >10%)

**Developer (Alex)**
- API doc bounce rate (Target: <20%)
- Code example copy rate (Target: >60%)
- Repeat API doc visits (Target: >40%)

**Casual Explorer (Jordan)**
- Homepage to immediate action (search/explore/stories) (Target: >70%)
- Overview tab comprehension (survey) (Target: >80% understand concept)
- Share/social engagement (Target: >5%)

### 9.4 Technical Performance Metrics

**Load Times**
- Homepage First Contentful Paint (Target: <1.5s)
- Explore page Time to Interactive (Target: <3.5s)
- Map tiles load time (Target: <2s)

**Core Web Vitals**
- Largest Contentful Paint (Target: <2.5s)
- First Input Delay (Target: <100ms)
- Cumulative Layout Shift (Target: <0.1)

**Bundle Size**
- JavaScript bundle (Target: <250KB gzipped)
- CSS bundle (Target: <50KB gzipped)
- Image optimization (Target: all images <200KB)

### 9.5 Data Collection Methods

**Analytics Setup**
```
Google Analytics 4 (or privacy-focused alternative like Plausible)
- Page views and session duration
- Navigation paths (Funnel analysis)
- Event tracking:
  - address_search_initiated
  - address_search_completed
  - tract_selected
  - filter_applied
  - story_read
  - api_doc_code_copied
  - share_link_clicked
  - tab_switched (Learn page)
  - toc_item_clicked (Methodology)
```

**User Testing**
- 5 users per persona (25 total) for usability testing
- Task success rate measurement
- Think-aloud protocol
- Post-task satisfaction surveys (SUS score)

**A/B Testing Opportunities**
- Homepage hero CTA variations
- Filter panel default state (open vs closed)
- Story card layouts
- API doc code example language preference

**Heatmaps & Session Recordings**
- Hotjar or Microsoft Clarity
- Rage click detection
- Scroll depth analysis
- Form abandonment tracking

---

## 10. Appendix

### 10.1 Design System Tokens

**Colors**
```
Primary:
  emerald-400: #34d399 (hover states)
  emerald-500: #10b981 (primary actions, active states)
  emerald-600: #059669 (pressed states)

Neutrals:
  slate-900: #0f172a (darkest backgrounds)
  slate-800: #1e293b (dark backgrounds, cards)
  slate-700: #334155 (borders, dividers on dark)
  slate-600: #475569 (muted text on dark)
  slate-400: #94a3b8 (secondary text on dark)
  slate-300: #cbd5e1 (body text on dark)
  white: #ffffff (headings on dark)

Resilience Score Colors:
  very-high: #059669 (emerald-600)
  high: #34d399 (emerald-400)
  medium: #fbbf24 (amber-400)
  low: #f97316 (orange-500)
  very-low: #dc2626 (red-600)
  no-data: #6b7280 (gray-500)

Semantic:
  error: #f87171 (red-400)
  warning: #fbbf24 (amber-400)
  success: #10b981 (emerald-500)
  info: #3b82f6 (blue-500)
```

**Typography**
```
Font Family:
  sans: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif
  mono: ui-monospace, "SF Mono", "Fira Code", Consolas, monospace

Font Sizes:
  xs: 12px / 0.75rem
  sm: 14px / 0.875rem
  base: 16px / 1rem
  lg: 18px / 1.125rem
  xl: 20px / 1.25rem
  2xl: 24px / 1.5rem
  3xl: 30px / 1.875rem
  4xl: 36px / 2.25rem
  5xl: 48px / 3rem

Line Heights:
  tight: 1.25
  normal: 1.5
  relaxed: 1.625
  loose: 2

Font Weights:
  normal: 400
  medium: 500
  semibold: 600
  bold: 700
```

**Spacing Scale**
```
0.5: 8px
1: 16px
1.5: 24px
2: 32px
3: 48px
4: 64px
6: 96px
8: 128px
```

**Border Radius**
```
sm: 4px (small elements, tags)
base: 8px (buttons, inputs, cards)
lg: 12px (large cards)
xl: 16px (modals, prominent sections)
full: 9999px (pills, badges)
```

**Shadows**
```
sm: 0 1px 2px rgba(0,0,0,0.05)
base: 0 4px 6px rgba(0,0,0,0.1)
md: 0 6px 12px rgba(0,0,0,0.15)
lg: 0 10px 25px rgba(0,0,0,0.2)
xl: 0 20px 40px rgba(0,0,0,0.25)
```

### 10.2 Responsive Breakpoints

```
Mobile: 0 - 639px
Tablet: 640px - 1023px
Desktop: 1024px - 1439px
Wide: 1440px+

Key breakpoints:
  sm: 640px
  md: 768px
  lg: 1024px
  xl: 1280px
  2xl: 1536px
```

### 10.3 Component Library Reference

**To Build:**
- Button (primary, secondary, ghost variants)
- Card (default, interactive, elevated)
- Input (text, search, select, checkbox, radio)
- Modal (dialog, bottom sheet)
- Tabs (horizontal, vertical)
- Accordion
- Table (sortable, paginated)
- Badge (status, category)
- Tooltip
- Breadcrumb
- Toast (notifications)
- Dropdown menu
- Loading spinner
- Empty state
- Error state

### 10.4 Accessibility Checklist

**Keyboard Navigation**
- [ ] All interactive elements reachable via Tab
- [ ] Tab order follows visual order
- [ ] Skip links provided
- [ ] No keyboard traps
- [ ] Focus indicators visible (2px outline)
- [ ] Escape key closes modals/dropdowns

**Screen Readers**
- [ ] Semantic HTML (header, nav, main, article, aside, footer)
- [ ] ARIA labels where needed
- [ ] ARIA live regions for dynamic content
- [ ] Alternative text for images
- [ ] Form labels associated with inputs
- [ ] Error messages announced

**Color & Contrast**
- [ ] Text contrast ≥ 4.5:1 (WCAG AA)
- [ ] Large text contrast ≥ 3:1
- [ ] Color not sole indicator of meaning
- [ ] Focus indicators have ≥ 3:1 contrast

**Touch Targets**
- [ ] Minimum 44x44px on mobile
- [ ] Adequate spacing between targets
- [ ] No fine motor skill requirements

**Content**
- [ ] Plain language option for technical content
- [ ] Captions for video/audio
- [ ] Transcripts available
- [ ] Language attribute set (lang="en")

### 10.5 Content Writing Guidelines

**Voice & Tone**
- Informative but approachable
- Avoid academic jargon in public-facing content
- Use active voice
- Be specific (not "data" but "64,419 census tracts")
- Assume curiosity, not expertise

**Terminology**
- Prefer "resilience score" over "standardized residual"
- Define technical terms on first use
- Use consistent terms throughout
- Link to glossary for complex concepts

**Microcopy Examples**
- Button: "Explore the Map" not "View Map"
- Empty state: "No tracts match your filters. Try adjusting your criteria." not "0 results"
- Error: "We couldn't find that address. Try a different format." not "Geocode failed"
- Loading: "Loading census tract data..." not "Loading..."

---

## Conclusion

This UX redesign addresses all critical issues identified in the current Community Resilience Mapping application:

1. **Navigation**: Persistent global nav and contextual breadcrumbs eliminate disorientation
2. **Information Architecture**: Clear separation of Explore, Stories, Learn, and For Developers
3. **Content Discoverability**: Tabbed interfaces and sticky TOCs make dense content scannable
4. **User Journeys**: Optimized paths for 5 distinct personas
5. **Mobile Experience**: Bottom sheets, optimized touch targets, and responsive layouts
6. **Progressive Disclosure**: Layered complexity from homepage through methodology

**Estimated Timeline**: 14 weeks for full implementation
**Minimum Viable Redesign**: 8 weeks (Phases 1-3)

**Next Steps**:
1. Stakeholder review and approval
2. Design mockups in Figma (based on wireframes)
3. User testing with prototype
4. Phased implementation following priority order
5. Analytics setup and baseline measurement
6. Iterative refinement based on user feedback

---

**Document Prepared By:** UX Design Team
**Date:** December 29, 2025
**Version:** 1.0
**Status:** For Review
