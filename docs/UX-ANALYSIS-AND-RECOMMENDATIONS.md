# UX Analysis and Recommendations
## Community Resilience Mapping Platform

**Date:** December 30, 2025
**Analyst:** Senior UX Designer (Data Applications Specialist)
**Focus:** Information Architecture, User Flows, Interaction Patterns for 68K+ row dataset

---

## Executive Summary

This analysis evaluates the proposed restructuring of the Community Resilience Mapping platform from a user-centered design perspective. The platform serves diverse user groups with fundamentally different mental models and workflow requirements. The key tension is between "discovery-first" vs "data-first" approaches.

**Core Recommendation:** Reject the binary choice. Build parallel entry points tailored to distinct user journeys rather than forcing all users through a single funnel.

---

## 1. Information Architecture Analysis

### 1.1 Current Structure (Evaluated)

```
/                  → Homepage (discovery-oriented, featured tracts)
/map               → Interactive choropleth map
/data              → Basic paginated table (100 rows/page)
/about             → Methodology documentation
/stories           → Community stories (empty)
```

**Strengths:**
- Clear separation of concerns
- Discovery-oriented homepage reduces cognitive load for first-time visitors
- Map is isolated with dedicated layout (good for performance)

**Weaknesses:**
- No clear path for researchers to "skip to data"
- Stories page exists but unused
- Missing research findings visibility
- No advanced filtering or segmentation

### 1.2 Proposed Architecture (Recommended)

```
/                           → Multi-persona landing page (NEW)
  ├─ Hero: "What is this?" (30sec pitch)
  ├─ Three pathways: Explore | Analyze | Learn
  └─ Research highlights (teaser cards)

/explore                    → Discovery interface (current homepage content)
  ├─ Featured tracts
  ├─ Map preview
  └─ "Interesting findings" narratives

/data                       → PRIMARY data interface (enhanced)
  ├─ Advanced filters (NEW)
  ├─ Virtualized table (NEW - performance)
  ├─ Inline mini-maps (NEW)
  ├─ Download filtered subset (NEW)
  └─ Quick map toggle (NEW)

/map                        → Full-screen map (unchanged)

/research                   → Research findings hub (NEW)
  ├─ Published papers
  ├─ Analysis summaries
  ├─ Downloadable datasets
  ├─ Citation guidance
  └─ Methodology overview

/stories                    → Community narratives
  ├─ Case studies
  ├─ Stakeholder quotes
  ├─ Photo essays (future)
  └─ Submit a story (CTA)

/about                      → About the project
  ├─ Team
  ├─ Data sources
  ├─ API documentation
  └─ Contact

/use-cases (NEW)            → Persona-specific guides
  ├─ For Researchers
  ├─ For Journalists
  ├─ For Policymakers
  └─ For Community Orgs
```

**Rationale:**
- **Persona-driven IA:** Different users have different "jobs to be done"
- **Multiple entry points:** Researchers shouldn't wade through storytelling to find CSV downloads
- **Progressive disclosure:** Complexity hidden until needed
- **Research visibility:** Elevates academic credibility without overwhelming casual users

---

## 2. User Personas & Journey Analysis

### 2.1 Persona 1: Academic Researcher

**Primary Goal:** Extract clean data for peer-reviewed publication

**Mental Model:**
- "Show me the data, methodology, and citation format"
- Skeptical of derived metrics until proven
- Values reproducibility, temporal caveats, sample size

**Current Journey Problems:**
1. Homepage emphasizes "top tracts" (cherry-picking concern)
2. Must navigate to /data to understand full dataset
3. No quick way to filter by research criteria (e.g., "show me all tracts with N>5000 and score>2")
4. Methodology buried in /about

**Recommended Journey:**

```
ENTRY: Homepage
  ↓
  Click "For Researchers" pathway
  ↓
ARRIVE: /research
  - Quick stats: 68,170 tracts, 2023 PLACES + 2019 FARA
  - Download full dataset (CSV, JSON, GeoJSON)
  - Methodology summary with caveats
  - Citation block (copy to clipboard)
  - Link to /data for filtering
  ↓
FILTER: /data
  - Filter by state, population, LILA status
  - Sort by resilience score
  - Preview inline statistics
  - Download filtered subset
  ↓
VALIDATE: /map (optional)
  - Visual QA of spatial patterns
  - Export map as PNG for publication
```

**Key Improvements:**
- Zero-click access to CSV from homepage
- Methodology visible before download
- Ability to download filtered subsets
- Clear temporal caveats (2019 vs 2023 data)

### 2.2 Persona 2: Journalist

**Primary Goal:** Find compelling human-interest stories with visual proof

**Mental Model:**
- "Where are the surprising findings?"
- Needs both data credibility AND narrative hooks
- Values geographic specificity, unusual patterns

**Current Journey Problems:**
1. Featured tracts lack narrative context (why are they resilient?)
2. No "story starters" or curated highlights
3. /stories page is empty
4. Map doesn't suggest "interesting clusters" to investigate

**Recommended Journey:**

```
ENTRY: Homepage
  ↓
  Click "Explore Stories" pathway
  ↓
ARRIVE: /explore
  - Featured finding cards (e.g., "Why is rural Tennessee outperforming?")
  - Map preview showing clusters
  - "Top surprising tracts" with one-sentence hooks
  ↓
INVESTIGATE: /map or /data
  - Click tract to see details
  - Compare to neighboring tracts
  - Download tract-specific data
  ↓
ENRICH: /stories
  - Read similar case studies
  - Contact info for community interviews
```

**Key Improvements:**
- Curated "story starters" on /explore
- Contextual narratives, not just numbers
- One-click export of tract details for fact-checking

### 2.3 Persona 3: Policymaker / Grant Writer

**Primary Goal:** Find proof points for funding proposals

**Mental Model:**
- "Show me what works, where, and why it matters"
- Needs digestible talking points
- Values benchmark comparisons (state, national)

**Current Journey Problems:**
1. No pre-made talking points or one-pagers
2. Difficult to compare across states
3. No "policy implications" section
4. Can't filter by policy-relevant segments (military bases, college towns)

**Recommended Journey:**

```
ENTRY: Homepage
  ↓
  Click "For Policymakers" pathway
  ↓
ARRIVE: /use-cases/policymakers
  - Key findings (3 bullet points)
  - State-level summary stats
  - Downloadable one-pager (PDF)
  - Link to full research
  ↓
FILTER: /data
  - Select state
  - Filter by community type (college town, military base, etc.)
  - Compare resilient vs non-resilient tracts
  ↓
EXPORT: Talking points + map screenshot
```

**Key Improvements:**
- Pre-made policy briefs
- State-level aggregations
- Community type filters
- Benchmark comparisons built-in

### 2.4 Persona 4: Community Organization

**Primary Goal:** Justify existing programs or identify expansion opportunities

**Mental Model:**
- "Is our community doing well? Who can we learn from?"
- Geographically focused (county or city level)
- Needs simple, shareable visuals

**Current Journey Problems:**
1. No geographic search beyond state filter
2. Can't easily compare multiple nearby tracts
3. No "share this tract" feature
4. Missing community resources or contact info

**Recommended Journey:**

```
ENTRY: Homepage
  ↓
  Search by ZIP or city name
  ↓
ARRIVE: /map (centered on location)
  - See local tracts color-coded
  - Click tract for details
  - Compare to county/state average
  ↓
SHARE: Generate shareable link
  - Short URL with tract pre-selected
  - Social media card preview
  ↓
LEARN: /stories
  - "Communities like yours that succeeded"
  - Contact info for peer learning
```

**Key Improvements:**
- Geographic search (ZIP, city, county)
- Comparison benchmarks
- Shareable links with social previews
- Peer learning resources

---

## 3. Critical UX Concerns with Proposals

### 3.1 CONCERN: "Rewrite homepage to lead with discovery not data"

**Pushback:** This is a false dichotomy.

**Analysis:**
- Current homepage ALREADY leads with discovery (featured tracts, narrative framing)
- The problem isn't "discovery vs data" but "no clear persona pathways"
- Researchers don't want to "discover" — they want to validate and extract

**Recommendation:**
- Keep discovery-oriented content
- ADD prominent "I'm a researcher, skip to data" pathway
- Use hero section for multi-CTA approach: [Explore Map] [Browse Data] [Read Research]

**Evidence from user research:**
- Academic users abandon sites that don't signal credibility within 10 seconds
- Burying data access behind narrative increases bounce rate for technical users

### 3.2 CONCERN: "Make data table the PRIMARY interface"

**Pushback:** Primary for whom?

**Analysis:**
- For researchers: YES, table is primary
- For journalists: NO, map + stories are primary
- For policymakers: NO, curated findings are primary
- For community orgs: NO, geographic search is primary

**Current table limitations:**
- 100 rows/page × 681 pages = unusable for exploration
- No inline visualizations (sparklines, mini-maps)
- Limited filtering (only state)
- No saved filter sets
- No export of filtered results

**Recommendation:**
- Make table PRIMARY FOR RESEARCHERS specifically
- Design a researcher-optimized /data page
- Keep map-first experience for discovery users
- Don't force all users through table interface

### 3.3 CONCERN: "Add filters for college towns, military bases, vulnerable communities"

**STRONG SUPPORT with caveats**

**Analysis:**
- Excellent for segmentation and policy research
- Aligns with user mental models (policymakers think in these categories)
- Technical challenge: How are these defined?

**Data requirements:**
```
College towns → Requires tract-level enrollment data or proximity to universities
Military bases → Requires geocoding of military installations + radius buffer
Vulnerable communities → Requires composite index (already have LILA, but add median income, disability %, elderly %)
```

**Recommended filter taxonomy:**

```
GEOGRAPHIC
  ├─ State (dropdown)
  ├─ County (autocomplete)
  ├─ Metro vs Rural (toggle)
  └─ Region (multi-select: South, Midwest, etc.)

DEMOGRAPHIC
  ├─ Population size (range slider)
  ├─ Median income (range slider)
  ├─ % Below poverty (range slider)
  └─ Age distribution (checkboxes)

RESILIENCE
  ├─ Score range (slider: -3 to +5)
  ├─ Percentile tier (dropdown: Top 1%, 5%, 10%)
  └─ Outlier status (positive, negative, expected)

COMMUNITY TYPE (NEW)
  ├─ College town (checkbox)
  ├─ Military base proximity (checkbox)
  ├─ LILA status (checkbox - already have)
  ├─ Healthcare access (checkbox: FQHC present)
  └─ Faith infrastructure (checkbox: if data available)

COMPARISON (NEW)
  ├─ Better than state avg (toggle)
  ├─ Better than predicted (toggle)
  └─ Statistical significance (p < 0.05)
```

**UI Pattern Recommendation:**
- Progressive disclosure: Start with 3 most common filters visible
- "Advanced filters" accordion for power users
- "Save filter set" for researchers
- "Share filtered view" URL generation

### 3.4 CONCERN: "Show score distribution histogram"

**STRONG SUPPORT**

**Analysis:**
- Excellent for understanding data distribution
- Helps users contextualize individual scores
- Standard in data-heavy applications

**Recommended implementation:**

**Location 1: /data page (above table)**
```
[Histogram visualization]
- X-axis: Resilience score bins (-3 to +5)
- Y-axis: Count of tracts
- Vertical line: Current filter selection
- Tooltip: "X tracts in this range"
- Interaction: Click bar to filter to that range
```

**Location 2: /research page (in stats overview)**
```
Distribution summary:
- Mean: 0.00 (by design)
- Median: -0.12
- SD: 1.00
- Skewness: +0.34 (right-tailed)
- Visual histogram
```

**Location 3: Tract detail popups (on map)**
```
"This tract: +2.4 (top 5%)"
[Mini histogram showing this tract's position]
```

**Accessibility considerations:**
- Provide text alternative: "Distribution: 5% very low, 20% low, 50% medium, 20% high, 5% very high"
- Ensure color contrast for bins
- Keyboard navigation for interactive histogram

---

## 4. Interaction Patterns for 68K Row Table

### 4.1 Performance Strategy

**Current approach:** Server-side pagination (100 rows/page)

**Problem:** 681 pages is cognitively overwhelming

**Recommended approach:** Hybrid virtualization + progressive loading

**Technical pattern:**

```
INITIAL LOAD:
- Fetch 200 rows + metadata (total count, distribution stats)
- Render first 50 rows in viewport
- Pre-cache next 150 rows in memory

USER SCROLLS:
- Virtualized rendering (only render visible rows + buffer)
- Infinite scroll triggers fetch when 80% through cached data
- Show loading skeleton for new data

USER FILTERS:
- Cancel pending requests
- Fetch filtered data (server-side)
- Reset scroll to top
- Update histogram to show filtered distribution

USER SORTS:
- Server-side sort (too large for client-side)
- Maintain scroll position if possible
```

**Libraries to consider:**
- TanStack Virtual (formerly react-virtual) for virtualization
- SvelteKit's streaming SSR for progressive hydration

### 4.2 Table Interaction Patterns

**Pattern 1: Sortable columns**
```
[Header]  Column Name ↕
- Click once: Sort descending
- Click twice: Sort ascending
- Click third: Clear sort (return to default)
- Shift+click: Multi-column sort
```

**Pattern 2: Inline expansion**
```
[Row] Tennessee, Rutherford County    +4.75    [>]
  ↓ (click to expand)
[Expanded Row]
  ├─ Population: 5,234
  ├─ Median income: $52,000
  ├─ LILA status: Yes
  ├─ [View on map] [Download tract data]
  └─ [Mini map preview]
```

**Pattern 3: Bulk actions**
```
[Checkbox] Select all (current page / all filtered results)
- Compare selected (up to 10 tracts)
- Download selected
- Add to collection (for logged-in users)
```

**Pattern 4: Column customization**
```
[Columns dropdown]
☑ State
☑ County
☑ Resilience Score
☐ Population
☐ Median Income
☐ % Below Poverty
☐ LILA Status
[Reset to default]
```

**Pattern 5: Quick filters (above table)**
```
[Search box: Filter by location name...]
[State: All ▼] [Score: Any ▼] [Population: Any ▼]
[+ Advanced filters]
```

### 4.3 Mobile Considerations

**Problem:** 68K row table on mobile is unusable in traditional format

**Recommended approach:** Switch to card-based layout on small screens

**Mobile pattern:**

```
DESKTOP (>768px):
[Full table with 8+ columns]

TABLET (480-768px):
[Table with 5 essential columns]
[Horizontal scroll for additional columns]

MOBILE (<480px):
[Card stack]
┌─────────────────────┐
│ Tennessee           │
│ Rutherford County   │
│                     │
│ Score: +4.75 (Top 1%)
│ Pop: 5,234          │
│ [View] [Compare]    │
└─────────────────────┘
```

**Mobile filters:**
```
[Filter button (floating action button)]
  ↓
[Bottom sheet with filters]
  - State
  - Score range
  - [Apply] [Clear]
```

---

## 5. Research Findings Integration

### 5.1 Current State

**Existing research assets:**
- docs/research-findings.md
- docs/COMPREHENSIVE-FINDINGS-REPORT.md
- docs/top-resilient-communities.md
- docs/policy-analysis.md
- docs/research-paper-draft.md

**Problem:** All buried in GitHub repo, not surfaced in UI

### 5.2 Recommended Integration Strategy

**Create /research page with hierarchical information:**

```
/research
├─ Hero: "Peer-Reviewed Findings"
├─ Quick stats (68K tracts, 50 states, etc.)
├─ Publication status badge (e.g., "Manuscript in review")
├─ Key findings (3-5 bullets with data visualizations)
├─ Downloads section
│   ├─ Full dataset (CSV, 2.5MB)
│   ├─ GeoJSON (12MB)
│   ├─ Methodology (PDF)
│   └─ Research paper draft (PDF)
├─ Citation generator
│   ├─ APA
│   ├─ MLA
│   ├─ Chicago
│   └─ BibTeX
├─ Methodology overview (expandable accordions)
│   ├─ Data sources
│   ├─ Statistical approach
│   ├─ Limitations & caveats
│   └─ Future directions
└─ Related publications (if any)
```

**Surface findings on homepage:**

```
Homepage → "Recent Findings" section

[Card 1]
Title: "1,059 Resilient Communities Identified"
Stat: 1.6% of low-access tracts show exceptional health
CTA: Read the research →

[Card 2]
Title: "Southeast Shows Strongest Resilience"
Map: Choropleth preview of regional patterns
CTA: Explore the map →

[Card 3]
Title: "Social Capital as Protective Factor"
Chart: Correlation visualization
CTA: Read methodology →
```

### 5.3 Academic Credibility Signals

**Critical for researcher trust:**

1. **Author affiliations** (if applicable)
2. **Data provenance** (CDC PLACES 2023, USDA FARA 2019)
3. **Temporal caveats** (4-year gap warning)
4. **Sample size transparency** (68,170 tracts, 2.55M records)
5. **Statistical methods** (regression residuals, Z-scores)
6. **Limitations section** (ecological fallacy, model-based estimates)
7. **Replication materials** (full code on GitHub)
8. **Citation count** (if published)
9. **DOI** (when available)
10. **License** (MIT for code, CC-BY for content)

**Warning labels for data quality:**

```
⚠ Temporal Mismatch
Food access data (2019) predates health outcomes (2023) by 4 years.
Interpret causal relationships with caution.

⚠ Model-Based Estimates
CDC PLACES uses small area estimation, not direct measurements.
Confidence intervals available in full dataset.

⚠ Boundary Changes
Mixed 2010/2020 census tract definitions may affect
comparisons across years.
```

---

## 6. What I Would Push Back On

### 6.1 REJECT: "Make data table the PRIMARY interface for everyone"

**Reasoning:**
- Violates user-centered design principle: different users, different needs
- Forces non-technical users through high-friction interface
- Map is superior for geographic discovery and pattern recognition
- Table is superior for precise lookup and export

**Counter-proposal:**
- Make table primary for /data route (researcher-focused)
- Make map primary for /explore route (discovery-focused)
- Let users choose their preferred mode
- Provide quick toggle between table/map views

### 6.2 REJECT: "Rewrite homepage to eliminate discovery framing"

**Reasoning:**
- Discovery framing is critical for journalist and policymaker engagement
- First-time visitors need narrative context before diving into data
- "Featured tracts" provide social proof and interesting hooks
- Pure data dump alienates non-technical stakeholders

**Counter-proposal:**
- Keep discovery framing as ONE pathway
- Add prominent researcher pathway (skip to data)
- Use hero section for multi-persona CTAs
- A/B test different entry points for different referral sources

### 6.3 CAUTION: "Add complex filters without clear UI"

**Reasoning:**
- Filter complexity can overwhelm casual users
- "College town" requires external data enrichment (not in current dataset)
- "Military base proximity" requires geocoding infrastructure
- Too many filters create "paradox of choice"

**Counter-proposal:**
- Start with 3-5 essential filters (state, score range, population)
- Add "Advanced filters" progressive disclosure
- Build community type filters ONLY after data enrichment
- Provide filter presets: "High resilience, low income" (one click)

### 6.4 CAUTION: "Surface research findings without peer review"

**Reasoning:**
- Academic credibility requires peer review
- "Research findings" page should distinguish:
  - Peer-reviewed publications (high credibility)
  - Working papers (medium credibility)
  - Exploratory analysis (low credibility)
- Overstating findings damages trust

**Counter-proposal:**
- Label clearly: "Working Paper (Not Peer Reviewed)"
- Include limitations and caveats prominently
- Link to GitHub for methodology transparency
- Update with peer-review status when available

### 6.5 REJECT: "Eliminate /map as standalone page"

**Reasoning:**
- Map is the ONLY interface for spatial pattern recognition
- Critical for journalists finding geographic clusters
- Essential for community orgs locating their area
- Performance benefits of dedicated map layout

**Counter-proposal:**
- Keep /map as full-screen dedicated experience
- Add inline mini-maps in table rows (best of both worlds)
- Provide "View in map" quick action from table
- Let map link to table (bidirectional navigation)

---

## 7. Prioritized Recommendations

### 7.1 IMMEDIATE (Ship in next 2 weeks)

**P0: Multi-persona homepage**
- Add three clear pathways: Explore | Analyze | Learn
- Keep discovery content, add researcher skip-link
- Effort: 2 days design, 3 days development

**P0: Enhanced data table filters**
- Add score range slider
- Add population filter
- Add county autocomplete
- Effort: 1 day design, 4 days development

**P0: Research findings page**
- Create /research route
- Surface existing markdown docs
- Add citation block
- Effort: 1 day design, 2 days development

**P0: Download filtered data**
- Allow CSV export of current filter state
- Add "Download visible rows" button
- Effort: 3 days development

### 7.2 SHORT-TERM (Ship in next 6 weeks)

**P1: Table virtualization**
- Implement infinite scroll with virtualization
- Improve from 100 rows/page to smooth scrolling
- Effort: 1 day design, 5 days development

**P1: Score distribution histogram**
- Add to /data page above table
- Interactive filtering by clicking bins
- Effort: 2 days design, 3 days development

**P1: Inline mini-maps in table**
- Show small map preview in expanded row
- "View in full map" quick action
- Effort: 3 days design, 4 days development

**P1: Advanced filter panel**
- Progressive disclosure design
- Save filter sets (localStorage)
- Share filtered URL
- Effort: 3 days design, 5 days development

**P1: Geographic search**
- ZIP code, city, county search
- Auto-center map on result
- Effort: 2 days design, 6 days development (geocoding API)

### 7.3 MEDIUM-TERM (Ship in 3 months)

**P2: Community type filters**
- Enrich data with college town classification
- Add military base proximity (geocoding)
- Add FQHC presence (data enrichment)
- Effort: 2 weeks data engineering, 1 week UI

**P2: Comparison mode**
- Select up to 5 tracts for side-by-side comparison
- Radar charts for multi-metric comparison
- Effort: 3 days design, 1 week development

**P2: Stories content**
- Commission 5-10 community case studies
- Photo essays and interviews
- Effort: 4 weeks content creation, 1 week development

**P2: Use-case specific landing pages**
- /use-cases/researchers
- /use-cases/journalists
- /use-cases/policymakers
- Effort: 1 week design, 1 week development

### 7.4 LONG-TERM (Ship in 6+ months)

**P3: User accounts & saved collections**
- Save favorite tracts
- Create custom collections
- Share collections with collaborators
- Effort: 2 weeks design, 4 weeks development

**P3: Advanced spatial analysis**
- Cluster detection (Moran's I)
- Hot spot analysis
- Export to GIS formats (Shapefile, GeoPackage)
- Effort: 3 weeks development

**P3: Temporal analysis (if multi-year data available)**
- Year-over-year trends
- Animated map showing changes
- Effort: 4 weeks development (depends on data availability)

---

## 8. Key Metrics for Success

### 8.1 User Engagement Metrics

**Discovery users (journalists, general public):**
- Time on /explore page
- Map interactions per session
- Story page views
- Social shares

**Research users (academics):**
- CSV download rate
- /research page visits
- Average session depth
- Return visitor rate

**Data users (all technical users):**
- Filter usage rate
- Average rows per filtered view
- Export frequency
- Advanced filter adoption

### 8.2 Usability Metrics

**Task completion rates:**
- Can researchers find and download CSV in <30 seconds? (Target: 95%)
- Can journalists find compelling story in <2 minutes? (Target: 80%)
- Can community orgs find their tract in <1 minute? (Target: 90%)

**Error rates:**
- Filter combination that returns 0 results (Target: <5%)
- Pagination errors or timeouts (Target: <1%)
- Mobile usability issues (Target: <2%)

**Accessibility:**
- WCAG 2.1 AA compliance (Target: 100% of pages)
- Keyboard navigation support (Target: 100% of features)
- Screen reader compatibility (Target: Zero major issues)

### 8.3 Leading Indicators of Success

**Early signals (Week 1-4):**
- CSV download rate increases 50%+
- Average session duration increases
- Bounce rate decreases on homepage
- Filter usage >30% of data page visitors

**Mid-term signals (Month 2-3):**
- Return visitor rate >20%
- Share rate for specific tracts increases
- Inbound links from academic papers
- Media citations with correct attribution

**Long-term signals (Month 6+):**
- Peer-reviewed publication using this data
- GitHub stars and forks increase
- Speaking invitations / conference presentations
- Grant proposals citing this work

---

## 9. Final Recommendations Summary

### DO THIS:
1. **Build multiple entry points** for different personas (not one-size-fits-all)
2. **Enhance data table** with virtualization, advanced filters, and exports
3. **Create /research page** to surface existing analysis and build credibility
4. **Add score distribution histogram** for context
5. **Implement geographic search** for community org use case
6. **Keep map as standalone page** (critical for spatial discovery)
7. **Add progressive disclosure** for complex filters (don't overwhelm)

### DON'T DO THIS:
1. **Don't force all users through data table** (map is better for some workflows)
2. **Don't eliminate discovery framing** (critical for engagement)
3. **Don't add community type filters** until data enrichment is complete
4. **Don't claim peer-review status** without actual peer review
5. **Don't hide methodology** (transparency builds trust)
6. **Don't ignore mobile users** (30-40% of traffic on many data sites)

### DEBATE THIS:
1. **Should table or map be PRIMARY?** → FALSE DICHOTOMY. Build both well.
2. **Should homepage lead with discovery or data?** → BOTH via multi-CTA hero
3. **Are advanced filters worth complexity?** → YES, with progressive disclosure
4. **Is research page necessary?** → CRITICAL for academic credibility

---

## 10. Conclusion

The proposed changes reflect real user needs, but implementation matters enormously. The key insight is that **there is no single "primary interface" for a multi-persona platform**. Instead:

- **Researchers want clean data, fast** → Build excellent /data page with exports
- **Journalists want stories and visuals** → Build excellent /explore + /stories pages
- **Policymakers want proof points** → Build excellent /research + use-case pages
- **Community orgs want local insights** → Build excellent geographic search + sharing

The homepage should be a **router**, not a funnel. Let users self-select their pathway based on their goals, rather than forcing everyone through a single interaction model.

**Final recommendation:** Ship the multi-persona homepage and enhanced data table first (P0), then iterate based on usage analytics. Let user behavior tell you which pathways matter most.

---

**Prepared by:** Senior UX Designer
**Review requested from:** Product Manager, Lead Engineer, Data Science Lead
**Next steps:** Stakeholder review, technical feasibility assessment, roadmap prioritization
