# Detailed User Flows by Persona
## Community Resilience Mapping Platform

**Date:** December 30, 2025

---

## Flow 1: Academic Researcher - First Visit

**Goal:** Evaluate dataset quality, download data, cite appropriately

**Entry Point:** Google search "census tract resilience health data"

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: ARRIVAL & CREDIBILITY ASSESSMENT (10 seconds)          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    LAND ON: Homepage
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ First Impression Scan:                                           │
│ ☑ Title includes "Research Dataset"                             │
│ ☑ Author/institution visible                                    │
│ ☑ Data source citations (CDC PLACES, USDA)                      │
│ ☑ Sample size (68,170 tracts)                                   │
│ ☑ Download CTA visible above fold                               │
│                                                                  │
│ Decision Point: Credible? → YES, continue                       │
│                          → NO, bounce (lost user)               │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: METHODOLOGY VALIDATION (2 minutes)                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
            Click: "Methodology" or "For Researchers"
                              ↓
                    ARRIVE: /research or /about
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ Scan for Red Flags:                                              │
│ ☑ Statistical method explained (regression residuals)           │
│ ☑ Limitations acknowledged (temporal gap, model estimates)      │
│ ☑ Sample size justification                                     │
│ ☑ Reproducibility (code on GitHub)                              │
│ ☐ Peer review status (future improvement)                       │
│                                                                  │
│ Decision Point: Methodology sound? → YES, proceed to download   │
│                                    → NO, explore more deeply    │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: DATA PREVIEW & FILTERING (5 minutes)                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    Click: "Browse Data"
                              ↓
                    ARRIVE: /data
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ Exploration Actions:                                             │
│ 1. Scan first 50 rows to understand variables                   │
│ 2. Sort by resilience_score (check distribution)                │
│ 3. Filter to own state (geographic relevance check)             │
│ 4. Check for missing data patterns                              │
│ 5. Expand row to see full variable list                         │
│                                                                  │
│ Questions Answered:                                              │
│ - What variables are included?                                  │
│ - Are there missing data issues?                                │
│ - What's the score distribution?                                │
│ - Can I filter to my region of interest?                        │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: DOWNLOAD DECISION (1 minute)                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
         Decision: Full dataset or filtered subset?
                              ↓
    ┌─────────────────────┬─────────────────────────┐
    ↓                     ↓                         ↓
Full Dataset         Filtered Subset          Specific Tracts
    │                     │                         │
    │                     │                         │
Click "Download CSV" Apply filters first      Select rows, export
    │                Set: state=CA
    │                score>1.0
    │                pop>5000
    │                     │                         │
    └─────────────────────┴─────────────────────────┘
                              ↓
                    DOWNLOAD INITIATED
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ File: resilience_data_2025-12-30.csv (2.5 MB)                   │
│ Contains: 68,170 rows × 25 columns                              │
│                                                                  │
│ Columns include:                                                 │
│ - GEOID (tract FIPS code)                                       │
│ - state_abbr, county_name                                       │
│ - resilience_score (Z-score)                                    │
│ - percentile_rank                                               │
│ - total_pop, median_income                                      │
│ - LILA status, food access metrics                             │
│ - CDC PLACES health outcomes (13 measures)                     │
│ - Predicted vs actual health scores                            │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: CITATION CAPTURE (30 seconds)                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
            Return to /research page
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ Citation Block (Copy to Clipboard):                             │
│                                                                  │
│ [APA] [MLA] [Chicago] [BibTeX]                                  │
│                                                                  │
│ Community Resilience Mapping Project (2025). Census tract-level │
│ health resilience scores: Identifying communities with better   │
│ health outcomes than predicted. https://resilience-mapping.fly.dev│
│                                                                  │
│ Data sources: CDC PLACES 2023, USDA Food Access Atlas 2019.    │
│                                                                  │
│ [Copy Citation] ← Click                                         │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ POST-VISIT ACTIONS                                              │
├─────────────────────────────────────────────────────────────────┤
│ ☑ Open CSV in R/Python for analysis                            │
│ ☑ Merge with own datasets (by GEOID)                           │
│ ☑ Run statistical tests                                        │
│ ☑ Cite in manuscript                                            │
│ ☐ Return to site for updated data (future)                     │
│ ☐ Star GitHub repo (if discovered)                             │
└─────────────────────────────────────────────────────────────────┘

SUCCESS METRICS:
✓ Time to download: <3 minutes from landing
✓ Citation captured: Yes
✓ Return likelihood: Medium (if data updates available)
```

---

## Flow 2: Journalist - Story Research

**Goal:** Find compelling human-interest angle with geographic specificity

**Entry Point:** Editor assignment: "Look into food deserts with good health outcomes"

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: INITIAL DISCOVERY (2 minutes)                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
            Google: "food desert good health outcomes"
                              ↓
                    LAND ON: Homepage
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ Journalist Scan Pattern:                                         │
│ 1. Skim headline: "Health Resilience Atlas" ✓                   │
│ 2. Look for numbers: "68,170 tracts" ✓                          │
│ 3. Look for surprising findings: "1,059 communities defy odds" ✓│
│ 4. Look for visuals: Map preview ✓                              │
│ 5. Look for stories: "Featured tracts" (but no narrative) ✗     │
│                                                                  │
│ Initial Reaction: "Interesting data, but where's the story?"    │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: GEOGRAPHIC EXPLORATION (5 minutes)                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    Click: "Explore Map"
                              ↓
                    ARRIVE: /map (full screen)
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ Map Exploration Actions:                                         │
│ 1. Pan to familiar region (e.g., own state)                     │
│ 2. Notice color-coded clusters                                  │
│ 3. Click on darkest green area (highest resilience)             │
│                                                                  │
│ Popup shows:                                                     │
│ ┌────────────────────────────────────┐                          │
│ │ Tennessee, Rutherford County       │                          │
│ │ FIPS: 47149041500                  │                          │
│ │ Resilience Score: +4.75 (Top 0.1%) │                          │
│ │ Population: 5,234                  │                          │
│ │ [View Details]                     │                          │
│ └────────────────────────────────────┘                          │
│                                                                  │
│ Journalist Reaction: "Why is this specific place doing so well?"│
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: STORY ANGLE DEVELOPMENT (10 minutes)                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
            Click: "View Details" or navigate to /data
                              ↓
            Filter: State = Tennessee, Top 1% scores
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ Research Questions:                                              │
│ 1. What makes Tennessee special? (cluster of high scores)       │
│ 2. Are there commonalities? (rural, college towns?)             │
│ 3. Who can I interview? (need local contacts)                   │
│ 4. What's the counter-narrative? (nearby struggling tracts)     │
│                                                                  │
│ Current Problem: No narrative context provided                  │
│                                                                  │
│ DESIRED (not yet built):                                        │
│ - "Story starters" section on tract detail page                 │
│ - "Communities like this one" comparisons                       │
│ - Local resource links (health dept, community orgs)            │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: DATA COLLECTION FOR FACT-CHECKING (5 minutes)           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        Actions needed for article:
                              ↓
    ┌─────────────────────┬─────────────────────────┬──────────────┐
    ↓                     ↓                         ↓              ↓
Screenshot map       Download tract data      Get exact stats  Find context
    │                     │                         │              │
Save as PNG          CSV with filtered          Copy score,    Navigate to
for article          Tennessee tracts           population,    /research for
graphic                                         percentile     methodology
    │                     │                         │              │
    └─────────────────────┴─────────────────────────┴──────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: EXTERNAL FOLLOW-UP                                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        Journalist leaves site to:
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ 1. Google "Rutherford County Tennessee health"                  │
│ 2. Find local health department contact                         │
│ 3. Search for community organizations                           │
│ 4. Look for local news archives                                 │
│ 5. Plan site visit / phone interviews                           │
│                                                                  │
│ OPPORTUNITY (future):                                           │
│ - Include local contact suggestions in tract details            │
│ - Link to /stories page with similar community profiles         │
│ - Provide quote-ready stats in shareable format                 │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 6: ARTICLE PRODUCTION & ATTRIBUTION                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        Article includes:
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ - Lead: "In a census tract in Rutherford County, Tennessee,    │
│   residents are defying the odds..."                            │
│                                                                  │
│ - Data point: "According to an analysis of 68,000+ census      │
│   tracts by the Community Resilience Mapping Project..."        │
│                                                                  │
│ - Visual: Embedded map screenshot showing regional pattern      │
│                                                                  │
│ - Attribution: Link to https://resilience-mapping.fly.dev       │
│                                                                  │
│ - Human angle: Interview with local resident or health official │
└──────────────────────────────────────────────────────────────────┘

SUCCESS METRICS:
✓ Time to find story angle: 15 minutes
✓ Data verification: Easy (direct download)
✓ Attribution: Included
✗ Local context: Required external research (improvement opportunity)
```

---

## Flow 3: Policymaker - Grant Proposal Evidence

**Goal:** Find proof points for state health equity grant application

**Entry Point:** Colleague recommendation during grant planning meeting

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: RELEVANCE CHECK (1 minute)                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
            Email link from colleague: [Click]
                              ↓
                    LAND ON: Homepage
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ Policymaker Scan:                                                │
│ ✓ "Research Dataset" = credible source                          │
│ ✓ "68,170 tracts" = comprehensive                               │
│ ✓ "50 states" = includes my state                               │
│ ✓ "Health outcomes" = relevant to grant focus                   │
│ ? "How do I use this for my grant?" = unclear                   │
│                                                                  │
│ Decision: Promising but need specific talking points            │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: STATE-LEVEL DISCOVERY (3 minutes)                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
    Decision: Map or Data? → Choose Data (need numbers)
                              ↓
                    Navigate to: /data
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ Filter Actions:                                                  │
│ 1. State dropdown: Select "Indiana"                             │
│ 2. Sort by resilience_score (desc)                              │
│                                                                  │
│ Results show:                                                    │
│ - 1,234 tracts in Indiana                                       │
│ - Top scoring tract: Marion County, +3.2 (Top 2%)               │
│ - Distribution visible in histogram                             │
│                                                                  │
│ Key Insight: "Indiana has multiple high-performing tracts       │
│              despite food access challenges"                    │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: COMPARISON ANALYSIS (5 minutes)                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        Questions for grant proposal:
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ 1. How does Indiana rank nationally?                            │
│    → Need /research page with state rankings (NOT YET BUILT)    │
│                                                                  │
│ 2. What % of Indiana tracts are resilient?                      │
│    → Need calculated statistic: 45/1234 = 3.6% (manual calc)    │
│                                                                  │
│ 3. How do we compare to neighbors? (IL, OH, MI, KY)             │
│    → Need comparison tool (NOT YET BUILT)                       │
│                                                                  │
│ 4. What are protective factors?                                 │
│    → Navigate to /research or /about                            │
│                                                                  │
│ CURRENT FRICTION: Must manually calculate/compare               │
│ DESIRED: Pre-computed state-level summaries                     │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: METHODOLOGY VERIFICATION (3 minutes)                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
            Click: "About" or "Methodology"
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ Policymaker Needs:                                               │
│ ✓ Data sources credible (CDC, USDA) = federal sources           │
│ ✓ Recent data (2023) = timely                                   │
│ ✓ Large sample (68K tracts) = rigorous                          │
│ ⚠ Temporal gap (2019-2023) = note in grant footnote            │
│ ✓ Available for replication = transparent                       │
│                                                                  │
│ Decision: Credible enough to cite in state grant proposal       │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: EXTRACT GRANT PROPOSAL CONTENT (10 minutes)             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        Open Word document, begin writing:
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ Grant Proposal Section: "Need for Intervention"                 │
│                                                                  │
│ Drafted Text:                                                    │
│ "Analysis of 68,170 census tracts nationwide reveals that only  │
│  1.6% demonstrate health resilience despite limited food access │
│  (Community Resilience Mapping Project, 2025). In Indiana,      │
│  approximately 3.6% of tracts (45 of 1,234) show positive      │
│  resilience scores, suggesting protective factors beyond food   │
│  access. This proposal seeks to identify and replicate these    │
│  protective mechanisms..."                                      │
│                                                                  │
│ [Toggle back to website to verify stats]                        │
│ [Download CSV for appendix]                                     │
│ [Screenshot map of Indiana for visual]                          │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ CURRENT PAIN POINTS:                                             │
├─────────────────────────────────────────────────────────────────┤
│ ✗ No pre-made "policy brief" or one-pager                       │
│ ✗ Must manually calculate state percentages                     │
│ ✗ No state-to-state comparison tool                             │
│ ✗ No downloadable charts/graphs for inclusion                   │
│ ✗ No policy implications section                                │
│                                                                  │
│ DESIRED FEATURES:                                                │
│ ✓ One-page state summary (PDF download)                         │
│ ✓ Quote-ready statistics                                        │
│ ✓ Pre-made visualizations (PowerPoint-ready)                    │
│ ✓ Policy recommendations section                                │
│ ✓ Contact for technical assistance                              │
└──────────────────────────────────────────────────────────────────┘

SUCCESS METRICS:
✓ Found credible evidence: Yes
✓ Cited in grant proposal: Yes
✗ Time efficiency: 20+ minutes (could be 5 with state summaries)
? Return likelihood: Low (one-time use unless data updates)
```

---

## Flow 4: Community Organization - Local Assessment

**Goal:** Determine if our county's programs are working

**Entry Point:** Board meeting discussion about program effectiveness

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: GEOGRAPHIC SEARCH (30 seconds)                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        User intent: "Is Pickens County, SC doing well?"
                              ↓
                    LAND ON: Homepage
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ User Action: Look for search box                                │
│                                                                  │
│ CURRENT PROBLEM: No geographic search on homepage!              │
│                                                                  │
│ User must choose:                                                │
│ [Explore Map] ← Choose this (most intuitive)                    │
│ [Browse Data]                                                    │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: MANUAL MAP NAVIGATION (2-5 minutes)                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    ARRIVE: /map
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ Navigation Actions:                                              │
│ 1. Pan to Southeast (general area)                              │
│ 2. Zoom to South Carolina                                       │
│ 3. Locate Pickens County (northwest corner)                     │
│ 4. Click on tract                                                │
│                                                                  │
│ CURRENT FRICTION: Requires geographic knowledge                 │
│ DESIRED: Search "Pickens County SC" → zoom directly             │
│                                                                  │
│ Popup shows:                                                     │
│ ┌────────────────────────────────────────┐                      │
│ │ South Carolina, Pickens County         │                      │
│ │ FIPS: 45077011202                      │                      │
│ │ Resilience Score: +4.41 (Top 0.2%)     │                      │
│ │ Population: 3,812                      │                      │
│ │ [View Details]                         │                      │
│ └────────────────────────────────────────┘                      │
│                                                                  │
│ User Reaction: "Wow! We're in the top 0.2% nationally!"         │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: CONTEXT & INTERPRETATION (3 minutes)                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        Questions that arise:
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ 1. "What does +4.41 mean?" → Need explanation                   │
│ 2. "How do we compare to nearby counties?" → Need comparison    │
│ 3. "Why are we doing well?" → Need protective factors           │
│ 4. "How can we share this success?" → Need shareable content    │
│                                                                  │
│ User navigates to /about to understand score                    │
│                                                                  │
│ Reads: "Score represents standard deviations better than        │
│         predicted health outcomes. +4.41 means 4.41 SDs above   │
│         expected, placing this tract in top 0.2%."              │
│                                                                  │
│ CURRENT: Technical explanation (requires stats knowledge)       │
│ DESIRED: Plain language: "Your community's health is much       │
│          better than expected given food access challenges."    │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: ORGANIZATIONAL USE (Board Meeting Prep)                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        User needs for board presentation:
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ ☑ Screenshot of map showing high score (done)                   │
│ ☑ Copy exact statistics (score, percentile, population)         │
│ ☐ Comparison to county average (NOT AVAILABLE)                  │
│ ☐ Comparison to state average (NOT AVAILABLE)                   │
│ ☐ Trend over time (NOT AVAILABLE - single snapshot)             │
│ ☐ Suggested protective factors for this tract (NOT AVAILABLE)   │
│                                                                  │
│ WORKAROUND: Download CSV, manually find other Pickens tracts    │
│                                                                  │
│ Navigate to /data                                                │
│ Filter: State = South Carolina                                  │
│ Manual search for other Pickens County FIPS codes               │
│ (Requires knowing FIPS code format: 45077XXXXXX)                │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: SHARING SUCCESS WITH STAKEHOLDERS                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        Board meeting presentation:
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ "I found this national dataset that shows our community is      │
│  performing exceptionally well - top 0.2% of census tracts in   │
│  health resilience despite food access challenges."             │
│                                                                  │
│ [Show map screenshot]                                            │
│                                                                  │
│ Board questions:                                                 │
│ - "What are we doing right?" (User can't answer from site)      │
│ - "How do other parts of the county compare?" (Hard to find)    │
│ - "Can we use this for grant proposals?" (Yes, but need citation)│
│ - "Should we contact other high-performing communities?" (No directory)│
│                                                                  │
│ OUTCOME: Useful proof point, but limited actionable insights    │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ DESIRED FEATURES (NOT YET BUILT):                                │
├─────────────────────────────────────────────────────────────────┤
│ 1. Geographic search (ZIP, city, county name)                   │
│ 2. Tract-level "plain language" summary                         │
│ 3. Automatic county/state comparisons                           │
│ 4. "Communities like yours" peer learning section               │
│ 5. Shareable social media cards                                 │
│ 6. Contact info for similar high-performing communities         │
│ 7. Downloadable one-page summary for board meetings             │
│ 8. Email alert when new data available for your area            │
└─────────────────────────────────────────────────────────────────┘

SUCCESS METRICS:
✓ Found local data: Yes (but with friction)
✓ Understood score meaning: Partially
✗ Comparative context: Difficult to obtain
✗ Actionable insights: Limited
? Return likelihood: Low (unless data updates or peer network develops)
```

---

## Flow 5: Power User - Advanced Analysis

**Goal:** Identify spatial clusters of resilience for academic paper

**Entry Point:** Twitter/Reddit link from colleague

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: RAPID ASSESSMENT (30 seconds)                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
            Social media link: [Click]
                              ↓
                    LAND ON: Homepage or /map
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ Power User Scan:                                                 │
│ ✓ 68K rows = substantial dataset                                │
│ ✓ CSV download visible = good                                   │
│ ✓ GitHub link visible = excellent (reproducibility)             │
│ ? API available? (scan for /api docs)                           │
│ ? GeoJSON download? (for GIS analysis)                          │
│ ? Spatial weights matrix? (for Moran's I)                       │
│                                                                  │
│ Decision: Worth deep dive                                       │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: DATA ACQUISITION (2 minutes)                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        Download strategy:
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ 1. Download CSV (full dataset)                                  │
│ 2. Check for GeoJSON (for spatial analysis)                     │
│    → /api/tracts?format=geojson (if exists)                     │
│ 3. Clone GitHub repo (for reproducibility)                      │
│    → git clone [repo URL]                                       │
│ 4. Check for API documentation                                  │
│    → /about#api or /api/docs                                    │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: EXPLORATORY ANALYSIS IN R/PYTHON (30 minutes)           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        Local analysis workflow:
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ library(sf)                                                      │
│ library(spdep)                                                   │
│                                                                  │
│ # Load data                                                      │
│ resilience <- read_csv("resilience_data.csv")                   │
│ geo <- st_read("resilience.geojson")                            │
│                                                                  │
│ # Spatial autocorrelation                                       │
│ neighbors <- poly2nb(geo)                                        │
│ weights <- nb2listw(neighbors)                                  │
│ moran.test(geo$resilience_score, weights)                       │
│                                                                  │
│ # Hot spot analysis                                              │
│ local_moran <- localmoran(geo$resilience_score, weights)        │
│                                                                  │
│ # Cluster detection                                              │
│ clusters <- identify_clusters(geo, threshold = 0.05)            │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: RETURN TO SITE FOR VALIDATION                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        After finding clusters in data:
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ Return to /map to visually validate findings                    │
│                                                                  │
│ Analysis found:                                                  │
│ - Southeast cluster (TN, SC, GA)                                │
│ - Upper Midwest cluster (IN, MI)                                │
│ - Isolated high performers in West                              │
│                                                                  │
│ Visual validation on map:                                        │
│ ✓ Southeast cluster visible (dark green concentration)          │
│ ✓ Midwest cluster visible                                       │
│ ✓ Matches statistical findings                                  │
│                                                                  │
│ DESIRED (NOT YET BUILT):                                         │
│ - Ability to overlay custom analysis results on map             │
│ - Export map with cluster boundaries                            │
│ - Share custom map views (with URL parameters)                  │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: ADVANCED FILTERING FOR HYPOTHESIS TESTING               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        Hypothesis: College towns drive resilience
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ CURRENT LIMITATION: No "college town" filter in UI              │
│                                                                  │
│ WORKAROUND:                                                      │
│ 1. Manually create list of university ZIP codes                 │
│ 2. Join with census tract boundaries                            │
│ 3. Create "college_town" flag in local analysis                 │
│ 4. Run regression: resilience ~ college_town + controls         │
│                                                                  │
│ DESIRED:                                                         │
│ - Pre-computed "college_town" variable in dataset               │
│ - UI filter: "Community type: College town"                     │
│ - API parameter: /api/tracts?community_type=college             │
│ - Download filtered: "Download college town tracts only"        │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 6: MANUSCRIPT PREPARATION                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        Writing paper, need from website:
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ ✓ Citation (available)                                           │
│ ✓ Methodology description (available)                           │
│ ✓ Sample size (available)                                       │
│ ✓ Data sources (available)                                      │
│ ✓ Limitations (available)                                       │
│ ? DOI (not yet - recommend getting one)                         │
│ ? Version number (not visible - important for reproducibility)  │
│ ? Download timestamp (not included in CSV - add metadata)       │
│                                                                  │
│ RECOMMENDATION: Add data versioning & DOI                       │
└──────────────────────────────────────────────────────────────────┘

SUCCESS METRICS:
✓ Complete analysis possible: Yes
✓ Reproducible: Yes (GitHub + downloads)
✓ Return likelihood: High (will check for updates)
? Contribution likelihood: Medium (if GitHub issues/PRs welcomed)
```

---

## Key Insights from Flow Analysis

### Universal Pain Points

1. **No geographic search** - All non-technical users struggled to find specific locations
2. **Limited context** - Raw scores need plain-language interpretation
3. **No comparisons** - Users want benchmarks (county, state, national)
4. **Missing narratives** - Data without stories limits engagement
5. **One-time use** - No reason to return unless data updates or community features added

### Persona-Specific Needs

| Persona | Primary Need | Missing Feature |
|---------|--------------|-----------------|
| Researcher | Clean data + methodology | State-level summaries, version control |
| Journalist | Story angles + visuals | Narrative hooks, local contacts |
| Policymaker | Talking points + proof | Pre-made briefs, policy implications |
| Community Org | Local validation + peers | Geographic search, peer network |
| Power User | Advanced analysis tools | API, spatial weights, versioning |

### Recommended Flow Improvements

1. **Add geographic search** to homepage and /map
2. **Create /research landing page** for academic users
3. **Build comparison tools** (county, state, national benchmarks)
4. **Add plain-language summaries** for non-technical users
5. **Provide shareable social cards** for community orgs
6. **Implement data versioning** for reproducibility
7. **Create peer network** for community learning

---

**Next Steps:**
- Validate flows with actual users (usability testing)
- Prioritize missing features based on user volume
- Instrument analytics to measure flow completion rates
- A/B test different entry points on homepage
