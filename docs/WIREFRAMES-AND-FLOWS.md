# Visual Wireframes & User Flows
## Community Resilience Mapping Platform

**Date:** December 30, 2025
**Purpose:** Visual reference for proposed UX improvements

---

## 1. Homepage Redesign: Multi-Persona Entry Points

### Current Homepage
```
┌─────────────────────────────────────────────────────────────────┐
│                     COMMUNITY RESILIENCE ATLAS                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│              "Open Research Dataset"                             │
│                                                                  │
│         Community Health Resilience Atlas                        │
│                                                                  │
│    Tract-level analysis identifying US communities with         │
│    better health outcomes than predicted                         │
│                                                                  │
│    [Download Dataset]  [Explore Map]  [Methodology]             │
│                                                                  │
│    68,170 tracts  |  51 states  |  264M+ people                 │
│                                                                  │
│ ┌────────────────────────────────────────────────────────────┐  │
│ │                                                            │  │
│ │              [Map Preview - MiniMap Component]             │  │
│ │                                                            │  │
│ └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│              HIGHEST RESILIENCE SCORES                           │
│                                                                  │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│ │Tennessee │ │S.Carolina│ │S.Carolina│ │ Michigan │            │
│ │Top 0.1% │ │Top 0.2% │ │Top 0.3% │ │Top 0.3% │            │
│ │5,234 pop │ │3,812 pop │ │4,156 pop │ │2,891 pop │            │
│ │[View]    │ │[View]    │ │[View]    │ │[View]    │            │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
│                                                                  │
│              USE THIS DATA                                       │
│    Free for research, journalism, and policy analysis           │
│    [Download CSV]  [API Documentation]                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

PROBLEMS:
✗ No clear persona pathways
✗ Researchers must hunt for methodology
✗ No research findings visibility
✗ Single linear flow
```

### Proposed Homepage: Multi-Entry
```
┌─────────────────────────────────────────────────────────────────┐
│                     COMMUNITY RESILIENCE ATLAS                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│         Finding Communities That Defy the Odds                   │
│                                                                  │
│    Analysis of 68,170 census tracts reveals which communities   │
│    achieve better health outcomes despite limited food access   │
│                                                                  │
│ ┌────────────────────┬────────────────────┬──────────────────┐  │
│ │  🗺️ EXPLORE        │  📊 ANALYZE        │  📚 LEARN       │  │
│ ├────────────────────┼────────────────────┼──────────────────┤  │
│ │ Interactive maps   │ Browse full data   │ Research findings│  │
│ │ & featured stories │ Advanced filters   │ & methodology    │  │
│ │                    │ Download datasets  │ Policy briefs    │  │
│ │ [Start Exploring]  │ [Browse Data]      │ [Read Research] │  │
│ │                    │                    │                  │  │
│ │ For: Journalists,  │ For: Researchers,  │ For: Academics,  │  │
│ │ policymakers,      │ data analysts,     │ policymakers,    │  │
│ │ general public     │ GIS specialists    │ grant writers    │  │
│ └────────────────────┴────────────────────┴──────────────────┘  │
│                                                                  │
│              RECENT RESEARCH HIGHLIGHTS                          │
│                                                                  │
│ ┌───────────────────────────────────────────────────────────┐   │
│ │ 📍 1,059 resilient communities identified (1.6% of LILA)  │   │
│ │    Communities achieving 0.6-4.7σ better health outcomes  │   │
│ │    → [View the map] [Download data]                       │   │
│ └───────────────────────────────────────────────────────────┘   │
│                                                                  │
│ ┌───────────────────────────────────────────────────────────┐   │
│ │ 🌎 Southeast shows strongest resilience clustering        │   │
│ │    Tennessee, South Carolina lead in high-performing      │   │
│ │    rural tracts. Social capital may be protective factor. │   │
│ │    → [Read full analysis] [Explore region]                │   │
│ └───────────────────────────────────────────────────────────┘   │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 🎓 New Working Paper: "Protective Factors in Food Deserts"  │ │
│ │    Faith-based infrastructure and community gardens may     │ │
│ │    buffer health impacts of limited food access.            │ │
│ │    → [Read paper draft] [Download citations]                │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│              QUICK ACCESS                                        │
│    [Download Full Dataset CSV]  [View API Docs]  [Contact Us]  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

IMPROVEMENTS:
✓ Three clear persona pathways
✓ Research findings surfaced prominently
✓ Multiple entry points for different user goals
✓ Recent discoveries create return-visit incentive
```

---

## 2. New /research Page

```
┌─────────────────────────────────────────────────────────────────┐
│ [← Home]              RESEARCH FINDINGS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                  Peer-Reviewed Research                          │
│            Community Health Resilience Analysis                  │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────┐    │
│ │ 📊 DATASET OVERVIEW                                      │    │
│ ├──────────────────────────────────────────────────────────┤    │
│ │ • 68,170 census tracts across all 50 US states + DC     │    │
│ │ • CDC PLACES 2023 health outcomes (2.55M records)       │    │
│ │ • USDA Food Access Atlas 2019 (72,531 tracts)           │    │
│ │ • Regression residual analysis (Z-score methodology)    │    │
│ │                                                          │    │
│ │ ⚠️ IMPORTANT CAVEATS:                                    │    │
│ │ • 4-year temporal gap (2019 food data vs 2023 health)   │    │
│ │ • Model-based estimates, not direct measurements        │    │
│ │ • Ecological inference limitations                      │    │
│ │                                                          │    │
│ │ Status: 📝 Working Paper (Not Yet Peer Reviewed)        │    │
│ │                                                          │    │
│ │ [Download Dataset ↓] [View Methodology →]               │    │
│ └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────┐    │
│ │ 🔍 KEY FINDINGS                                          │    │
│ ├──────────────────────────────────────────────────────────┤    │
│ │                                                          │    │
│ │ Finding 1: Resilience in Adversity                      │    │
│ │ ─────────────────────────────────────────────────────   │    │
│ │ 1,059 census tracts (1.6% of LILA areas) demonstrate   │    │
│ │ health outcomes 0.6-4.7 standard deviations better     │    │
│ │ than predicted by food access metrics.                 │    │
│ │                                                          │    │
│ │ [View these tracts on map →]                            │    │
│ │                                                          │    │
│ │ ─────────────────────────────────────────────────────   │    │
│ │                                                          │    │
│ │ Finding 2: Geographic Clustering                        │    │
│ │ ─────────────────────────────────────────────────────   │    │
│ │ Strong Southeast clustering (TN, SC, GA, KY) suggests  │    │
│ │ regional protective factors. State-level leaders:       │    │
│ │ • Tennessee: 187 resilient tracts                       │    │
│ │ • South Carolina: 142 resilient tracts                  │    │
│ │ • Indiana: 98 resilient tracts                          │    │
│ │                                                          │    │
│ │ [View regional analysis →]                              │    │
│ │                                                          │    │
│ │ ─────────────────────────────────────────────────────   │    │
│ │                                                          │    │
│ │ Finding 3: Potential Protective Factors                │    │
│ │ ─────────────────────────────────────────────────────   │    │
│ │ Qualitative analysis suggests:                         │    │
│ │ • Strong social capital and community networks         │    │
│ │ • Faith-based infrastructure (churches, food pantries) │    │
│ │ • Alternative food systems (gardens, farmers markets)  │    │
│ │ • Healthcare access (FQHCs, mobile clinics)            │    │
│ │                                                          │    │
│ │ ⚠️ These are hypotheses requiring validation           │    │
│ │                                                          │    │
│ │ [Read full analysis →]                                  │    │
│ │                                                          │    │
│ └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────┐    │
│ │ 📥 DOWNLOADS                                             │    │
│ ├──────────────────────────────────────────────────────────┤    │
│ │ Full Dataset                                             │    │
│ │ └─ [CSV (2.5 MB)] [GeoJSON (12 MB)] [JSON API]          │    │
│ │                                                          │    │
│ │ Documentation                                            │    │
│ │ └─ [Methodology PDF] [Data Dictionary] [Codebook]       │    │
│ │                                                          │    │
│ │ Publications                                             │    │
│ │ └─ [Working Paper Draft] [Policy Brief] [Infographic]   │    │
│ │                                                          │    │
│ │ Supplementary Materials                                  │    │
│ │ └─ [Statistical Tables] [Figures] [GitHub Repository]   │    │
│ └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────┐    │
│ │ 📖 CITATION                                              │    │
│ ├──────────────────────────────────────────────────────────┤    │
│ │                                                          │    │
│ │ [APA] [MLA] [Chicago] [BibTeX]                          │    │
│ │                                                          │    │
│ │ ┌────────────────────────────────────────────────────┐  │    │
│ │ │ Community Resilience Mapping Project (2025).       │  │    │
│ │ │ Census tract-level health resilience scores:       │  │    │
│ │ │ Identifying communities with better health         │  │    │
│ │ │ outcomes than predicted.                           │  │    │
│ │ │ https://resilience-mapping.fly.dev                 │  │    │
│ │ │                                                     │  │    │
│ │ │ Data sources: CDC PLACES 2023, USDA Food Access    │  │    │
│ │ │ Research Atlas 2019.                               │  │    │
│ │ │                                                     │  │    │
│ │ │ [📋 Copy Citation]                                 │  │    │
│ │ └────────────────────────────────────────────────────┘  │    │
│ └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────┐    │
│ │ 🔬 METHODOLOGY                                           │    │
│ ├──────────────────────────────────────────────────────────┤    │
│ │                                                          │    │
│ │ [▼] Data Sources & Preparation                          │    │
│ │ [▶] Statistical Approach                                │    │
│ │ [▶] Resilience Score Calculation                        │    │
│ │ [▶] Limitations & Caveats                               │    │
│ │ [▶] Future Directions                                   │    │
│ │                                                          │    │
│ │ [View full methodology document →]                      │    │
│ └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────┐    │
│ │ 📬 CONTACT                                               │    │
│ ├──────────────────────────────────────────────────────────┤    │
│ │ Questions about the data or methodology?                │    │
│ │ Interested in collaboration?                            │    │
│ │                                                          │    │
│ │ [Open GitHub Issue] [Email Researchers]                 │    │
│ └──────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Enhanced /data Page: Table-First Interface

### Current Data Page
```
┌─────────────────────────────────────────────────────────────────┐
│ [← Back]           DATA EXPLORER                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Browse Dataset                                                   │
│ 68,170 census tracts with resilience scores                     │
│                                                    [Download CSV]│
│                                                                  │
│ State: [All States ▼]                                           │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────┐    │
│ │ Location ↕    Score ↕    Population ↕    Actions        │    │
│ ├──────────────────────────────────────────────────────────┤    │
│ │ TN County     +4.75      5,234          View             │    │
│ │ SC County     +4.41      3,812          View             │    │
│ │ ...           ...        ...            ...              │    │
│ │ (100 rows)                                               │    │
│ └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│ Page 1 of 681          [Previous] [Next]                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

PROBLEMS:
✗ 681 pages is overwhelming
✗ Only state filter available
✗ No score distribution context
✗ No advanced filtering
✗ Can't download filtered subset
```

### Proposed Enhanced Data Page
```
┌─────────────────────────────────────────────────────────────────┐
│ [← Home]              DATA EXPLORER                      [? Help]│
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Browse & Filter 68,170 Census Tracts                            │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 🔍 Search by location, FIPS, or county...              [X] │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ Quick Filters:                                                   │
│ [State: All ▼] [Score: Any ▼] [Population: Any ▼]              │
│ [+ Advanced Filters]                       Active: 0 filters    │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ SCORE DISTRIBUTION                                          │ │
│ │                                                             │ │
│ │       ▂                                                     │ │
│ │     ▂ █                                                     │ │
│ │   ▅ █ █ ▅                                                   │ │
│ │ ▂ █ █ █ █ ▂ ▂ ▂                                             │ │
│ │ █████████████████                                           │ │
│ │ -3  -2  -1   0   1   2   3   4   5                          │ │
│ │                                                             │ │
│ │ Click a bar to filter to that range                        │ │
│ │ Showing all 68,170 tracts                                  │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ Results: 68,170 tracts                                           │
│ [⬇ Download Visible] [⚙️ Columns] [🔗 Share View]               │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │┌─┬──┬─────────────────────────┬────────────┬─────────┬────┐│ │
│ ││☐│St│ Location ↓              │ Score ↓    │ Pop ↕   │    ││ │
│ │├─┼──┼─────────────────────────┼────────────┼─────────┼────┤│ │
│ ││☐│TN│ Rutherford County       │ +4.75      │ 6,891   │[>] ││ │
│ ││ │  │ Tract 041500            │ Top 0.1%   │         │View││ │
│ │├─┼──┼─────────────────────────┼────────────┼─────────┼────┤│ │
│ ││☐│SC│ Pickens County          │ +4.41      │ 3,812   │[>] ││ │
│ ││ │  │ Tract 011202            │ Top 0.2%   │         │View││ │
│ │├─┼──┼─────────────────────────┼────────────┼─────────┼────┤│ │
│ ││☐│SC│ Beaufort County         │ +4.32      │ 4,156   │[>] ││ │
│ ││ │  │ Tract 001000            │ Top 0.3%   │         │View││ │
│ │├─┼──┼─────────────────────────┼────────────┼─────────┼────┤│ │
│ ││☐│MI│ Mecosta County          │ +4.24      │ 2,891   │[>] ││ │
│ ││ │  │ Tract 981300            │ Top 0.3%   │         │View││ │
│ │└─┴──┴─────────────────────────┴────────────┴─────────┴────┘│ │
│ │                                                             │ │
│ │ [Scroll for more... infinite scroll active]                │ │
│ │                                                             │ │
│ │ 3 tracts selected    [Compare] [Download Selected]         │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ [⇄ Toggle Map View]                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

IMPROVEMENTS:
✓ Score distribution histogram for context
✓ Quick filters for common use cases
✓ Advanced filters for power users
✓ Infinite scroll (no pagination)
✓ Row selection for bulk operations
✓ Download filtered data
✓ Shareable filter URLs
✓ Column customization
✓ Quick map toggle
```

---

## 4. Advanced Filters Panel

```
┌─────────────────────────────────────────────────────────────────┐
│ ADVANCED FILTERS                                        [Close X]│
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ▼ GEOGRAPHIC FILTERS                                            │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ State (multi-select)                                        │ │
│ │ ┌───────────────────────────────────────────────────────┐   │ │
│ │ │ 🔍 Search states...                                   │   │ │
│ │ │ ☑ California (1,234 tracts)                           │   │ │
│ │ │ ☐ Texas (2,456 tracts)                                │   │ │
│ │ │ ☑ Tennessee (987 tracts)                              │   │ │
│ │ │ ☐ New York (1,876 tracts)                             │   │ │
│ │ │ ... (scroll for more)                                 │   │ │
│ │ └───────────────────────────────────────────────────────┘   │ │
│ │                                                             │ │
│ │ Region                                                      │ │
│ │ ☐ Northeast  ☑ Southeast  ☐ Midwest  ☐ West  ☐ Southwest  │ │
│ │                                                             │ │
│ │ Metro Status                                                │ │
│ │ ○ Any  ○ Metro only  ○ Non-metro only                      │ │
│ │                                                             │ │
│ │ County (autocomplete)                                       │ │
│ │ [Type county name...                               ] 🔍    │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ ▼ RESILIENCE FILTERS                                            │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Score Range                                                 │ │
│ │ ─●────────────────────●─                                    │ │
│ │ -3.0     -1.0     0.0     1.0     3.0     5.0               │ │
│ │ Min: 1.0            Max: 5.0                                │ │
│ │                                                             │ │
│ │ Percentile Tier                                             │ │
│ │ ☑ Top 1% (682 tracts)                                      │ │
│ │ ☑ Top 5% (3,409 tracts)                                    │ │
│ │ ☐ Top 10% (6,817 tracts)                                   │ │
│ │ ☐ Above Average (>50th %ile)                               │ │
│ │                                                             │ │
│ │ Outlier Status                                              │ │
│ │ ○ Any  ● Positive outliers only  ○ Negative outliers only │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ ▶ DEMOGRAPHIC FILTERS (click to expand)                         │
│                                                                  │
│ ▶ COMMUNITY CHARACTERISTICS (click to expand)                   │
│                                                                  │
│ ─────────────────────────────────────────────────────────────── │
│                                                                  │
│ Active Filters: California, Tennessee, Score 1.0-5.0, Top 5%    │
│ Results: 234 tracts match these criteria                        │
│                                                                  │
│ [Clear All] [Save as Preset] [Share URL] [Apply Filters]        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

INTERACTION:
- Real-time result count preview
- Collapsible sections to reduce overwhelm
- Progressive disclosure pattern
- Save custom filter presets
- Share filtered view via URL
```

---

## 5. Row Expansion: Inline Details

```
┌─────────────────────────────────────────────────────────────────┐
│ COLLAPSED ROW (default state)                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌─┬──┬─────────────────────────┬────────────┬─────────┬────┐   │
│ │☐│TN│ Rutherford County       │ +4.75      │ 6,891   │[>] │   │
│ │ │  │ Tract 041500            │ Top 0.1%   │         │View│   │
│ └─┴──┴─────────────────────────┴────────────┴─────────┴────┘   │
│      ↑ Click anywhere to expand                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

                    [Click to expand ↓]

┌─────────────────────────────────────────────────────────────────┐
│ EXPANDED ROW                                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌─┬──┬─────────────────────────┬────────────┬─────────┬────┐   │
│ │☑│TN│ Rutherford County       │ +4.75      │ 6,891   │[v] │   │
│ │ │  │ Tract 041500            │ Top 0.1%   │         │Hide│   │
│ └─┴──┴─────────────────────────┴────────────┴─────────┴────┘   │
│                                                                  │
│ ┌───────────────────────────────────────────────────────────┐   │
│ │ EXPANDED CONTENT                                          │   │
│ │                                                           │   │
│ │ ┌────────────────────┐  ┌──────────────────────────────┐ │   │
│ │ │ TRACT DETAILS      │  │ LOCATION PREVIEW             │ │   │
│ │ │                    │  │                              │ │   │
│ │ │ FIPS: 47149041500  │  │ ┌────────────────────────┐   │ │   │
│ │ │ State: Tennessee   │  │ │  [Mini interactive     │   │ │   │
│ │ │ County: Rutherford │  │ │   map showing this     │   │ │   │
│ │ │ Population: 6,891  │  │ │   tract highlighted    │   │ │   │
│ │ │                    │  │ │   + neighboring tracts]│   │ │   │
│ │ │ Median Inc: $58K   │  │ │                        │   │ │   │
│ │ │ % Poverty: 12.4%   │  │ │  Click to open in      │   │ │   │
│ │ │ LILA: Yes          │  │ │  full map view         │   │ │   │
│ │ │ Urban/Rural: Mixed │  │ └────────────────────────┘   │ │   │
│ │ │                    │  │                              │ │   │
│ │ │ [📍 View on Map]   │  │ [🗺️ Open Full Map]         │ │   │
│ │ └────────────────────┘  └──────────────────────────────┘ │   │
│ │                                                           │   │
│ │ ┌───────────────────────────────────────────────────────┐ │   │
│ │ │ HEALTH OUTCOMES vs. PREDICTED                         │ │   │
│ │ │                                                        │ │   │
│ │ │ Metric           Actual    Predicted    Difference    │ │   │
│ │ │ ─────────────────────────────────────────────────────│ │   │
│ │ │ Diabetes         6.2%      9.8%        -3.6% ✓       │ │   │
│ │ │ Obesity          22.1%     28.4%       -6.3% ✓       │ │   │
│ │ │ High BP          28.3%     31.7%       -3.4% ✓       │ │   │
│ │ │ Poor MH Days     2.8       4.2         -1.4 ✓        │ │   │
│ │ │                                                        │ │   │
│ │ │ ✓ = Better than predicted                            │ │   │
│ │ └───────────────────────────────────────────────────────┘ │   │
│ │                                                           │   │
│ │ ┌───────────────────────────────────────────────────────┐ │   │
│ │ │ CONTEXTUAL POSITION                                   │ │   │
│ │ │                                                        │ │   │
│ │ │ This tract's score: +4.75                             │ │   │
│ │ │                                                        │ │   │
│ │ │ Distribution:                                          │ │   │
│ │ │         ▂                                              │ │   │
│ │ │       ▂ █                                              │ │   │
│ │ │     ▅ █ █ ▅              ▲ You are here (99.9%ile)   │ │   │
│ │ │   ▂ █ █ █ █ ▂ ▂ ▂        │                            │ │   │
│ │ │   -3  -1   1   3   5 ────┘                            │ │   │
│ │ │                                                        │ │   │
│ │ │ Comparison:                                            │ │   │
│ │ │ • Better than 99.9% of all tracts                     │ │   │
│ │ │ • Better than 98.2% of Tennessee tracts               │ │   │
│ │ │ • #1 in Rutherford County                             │ │   │
│ │ └───────────────────────────────────────────────────────┘ │   │
│ │                                                           │   │
│ │ ACTIONS:                                                  │   │
│ │ [📥 Download Tract Data] [➕ Add to Comparison]          │   │
│ │ [🔗 Share Link] [📊 View Nearby Tracts]                  │   │
│ │                                                           │   │
│ └───────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

FEATURES:
✓ Quick stats at a glance
✓ Mini map for geographic context
✓ Health outcome comparisons
✓ Distribution context (where this tract falls)
✓ Benchmarking (county, state, national)
✓ Action buttons for common tasks
```

---

## 6. Comparison View: Side-by-Side Analysis

```
┌─────────────────────────────────────────────────────────────────┐
│ TRACT COMPARISON                                        [Close X]│
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Comparing 3 selected tracts                                      │
│                                                                  │
│ ┌───────────────┬────────────────┬────────────────┬───────────┐ │
│ │ Metric        │ TN Rutherford  │ SC Pickens     │ MI Mecosta│ │
│ │               │ 47149041500    │ 45077011202    │ 26107981300│ │
│ ├───────────────┼────────────────┼────────────────┼───────────┤ │
│ │ RESILIENCE    │                │                │           │ │
│ ├───────────────┼────────────────┼────────────────┼───────────┤ │
│ │ Score         │ +4.75 🥇       │ +4.41 🥈       │ +4.24 🥉  │ │
│ │ Percentile    │ 99.9%          │ 99.7%          │ 99.6%     │ │
│ │ Rank (of 68K) │ #1             │ #2             │ #4        │ │
│ ├───────────────┼────────────────┼────────────────┼───────────┤ │
│ │ DEMOGRAPHICS  │                │                │           │ │
│ ├───────────────┼────────────────┼────────────────┼───────────┤ │
│ │ Population    │ 6,891          │ 3,812          │ 2,891     │ │
│ │ Median Income │ $58,000        │ $52,000        │ $45,000   │ │
│ │ % Poverty     │ 12.4%          │ 15.2%          │ 18.7%     │ │
│ │ % Elderly     │ 14.2%          │ 18.3%          │ 16.7%     │ │
│ ├───────────────┼────────────────┼────────────────┼───────────┤ │
│ │ LOCATION      │                │                │           │ │
│ ├───────────────┼────────────────┼────────────────┼───────────┤ │
│ │ State         │ Tennessee      │ S. Carolina    │ Michigan  │ │
│ │ Metro Status  │ Suburban       │ Rural          │ Rural     │ │
│ │ LILA          │ Yes            │ Yes            │ Yes       │ │
│ ├───────────────┼────────────────┼────────────────┼───────────┤ │
│ │ HEALTH        │                │                │           │ │
│ ├───────────────┼────────────────┼────────────────┼───────────┤ │
│ │ Diabetes      │ 6.2% ✓         │ 7.1% ✓         │ 8.9% ✓    │ │
│ │ Obesity       │ 22.1% ✓        │ 24.3% ✓        │ 28.1% ✓   │ │
│ │ High BP       │ 28.3% ✓        │ 29.7% ✓        │ 31.2% ✓   │ │
│ │ Poor MH Days  │ 2.8 ✓          │ 3.2 ✓          │ 3.8 ✓     │ │
│ └───────────────┴────────────────┴────────────────┴───────────┘ │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ MULTI-METRIC COMPARISON (Radar Chart)                       │ │
│ │                                                             │ │
│ │           Resilience                                        │ │
│ │                •                                            │ │
│ │               /│\                                           │ │
│ │              / │ \                                          │ │
│ │   Income •─────+─────• Health                              │ │
│ │             \  │  /                                         │ │
│ │              \ │ /                                          │ │
│ │               \│/                                           │ │
│ │                •                                            │ │
│ │           Population                                        │ │
│ │                                                             │ │
│ │ ─── TN Rutherford   ─── SC Pickens   ─── MI Mecosta       │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ KEY INSIGHTS                                                │ │
│ │                                                             │ │
│ │ • All three tracts are in top 1% for resilience            │ │
│ │ • Tennessee tract has highest population but best health   │ │
│ │ • South Carolina tract most rural but still high-performing│ │
│ │ • Income levels vary widely (not primary driver?)          │ │
│ │                                                             │ │
│ │ [📥 Download Comparison] [🔗 Share] [➕ Add More Tracts]   │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

FEATURES:
✓ Side-by-side metric comparison
✓ Visual ranking (medals for top performers)
✓ Radar chart for multi-dimensional view
✓ Automatic insights generation
✓ Export for presentations
```

---

## 7. Mobile-Optimized Card Layout

```
┌──────────────────────────┐
│ MOBILE VIEW (<768px)     │
├──────────────────────────┤
│                          │
│ ┌──── Filters ────────┐  │
│ │ [State ▼] [Score ▼] │  │
│ │ [🔍]                │  │
│ └─────────────────────┘  │
│                          │
│ Showing 1,234 tracts     │
│                          │
│ ┌──────────────────────┐ │
│ │ TENNESSEE            │ │
│ │ Rutherford County    │ │
│ │ Tract 041500         │ │
│ │                      │ │
│ │ Score: +4.75         │ │
│ │ ████████████░░░░     │ │
│ │ Top 0.1%             │ │
│ │                      │ │
│ │ Pop: 6,891           │ │
│ │ Income: $58,000      │ │
│ │ LILA: Yes            │ │
│ │                      │ │
│ │ [View Map] [Compare] │ │
│ │                      │ │
│ │ [Tap for details ▼]  │ │
│ └──────────────────────┘ │
│                          │
│ ┌──────────────────────┐ │
│ │ SOUTH CAROLINA       │ │
│ │ Pickens County       │ │
│ │ Tract 011202         │ │
│ │                      │ │
│ │ Score: +4.41         │ │
│ │ ████████████░░░░     │ │
│ │ Top 0.2%             │ │
│ │                      │ │
│ │ Pop: 3,812           │ │
│ │ Income: $52,000      │ │
│ │ LILA: Yes            │ │
│ │                      │ │
│ │ [View Map] [Compare] │ │
│ │                      │ │
│ │ [Tap for details ▼]  │ │
│ └──────────────────────┘ │
│                          │
│ [Load More ↓]            │
│                          │
│ [🔍 Filters ↑]           │
│ ← Floating button        │
│                          │
└──────────────────────────┘

MOBILE INTERACTIONS:
- Tap card to expand details
- Swipe card left for quick actions
- Pull to refresh data
- Infinite scroll for loading
- Bottom sheet for filters
- Sticky filter button
```

---

## 8. User Flow: Researcher Path

```
RESEARCHER JOURNEY MAP
════════════════════════════════════════════════════════════════════

ENTRY POINT: Google → "census tract health resilience data"
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ HOMEPAGE                                          Time: 0:00     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│         Finding Communities That Defy the Odds                   │
│                                                                  │
│ ┌──────────────┬──────────────┬──────────────┐                  │
│ │ 🗺️ EXPLORE  │ 📊 ANALYZE  │ 📚 LEARN     │ ← CLICK THIS      │
│ │             │             │              │                    │
│ │ [Start]     │ [Browse]    │ [Research]   │                    │
│ └──────────────┴──────────────┴──────────────┘                  │
│                                                                  │
│ Decision: "I want the data" → Click [Read Research]             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ /research PAGE                                    Time: 0:05     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ RESEARCH FINDINGS                                                │
│                                                                  │
│ ✓ Scan dataset overview (68K tracts, CDC + USDA)               │
│ ✓ Check methodology (regression residuals, Z-scores)           │
│ ✓ Note caveats (temporal gap, model estimates)                 │
│ ✓ Verify not peer-reviewed yet (working paper)                 │
│                                                                  │
│ Decision: "Methodology sound, proceed to data"                  │
│                                                                  │
│ Action: Click [Download Dataset ↓]                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ DOWNLOAD INITIATED                                Time: 0:10     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ resilience_data_2025-12-30.csv (2.5 MB)                         │
│                                                                  │
│ ✓ Downloaded to ~/Downloads                                    │
│                                                                  │
│ Meanwhile, also:                                                 │
│ - Copy citation to clipboard                                    │
│ - Bookmark methodology page                                     │
│ - Star GitHub repo (if discovered)                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ OPTIONAL: DATA PREVIEW                            Time: 0:12     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Click: [Browse Data] to preview before opening in R/Python      │
│                                                                  │
│ /data page:                                                      │
│ - Filter to own state (California)                              │
│ - Sort by resilience score (desc)                               │
│ - Expand top row to see variables                               │
│ - Confirm data structure matches expectations                   │
│                                                                  │
│ Decision: "Looks good, ready for analysis"                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ LOCAL ANALYSIS (outside website)                  Time: 0:15+    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Open R/Python:                                                   │
│ > df <- read.csv("resilience_data_2025-12-30.csv")             │
│ > summary(df$resilience_score)                                  │
│ > ggplot(df, aes(x=resilience_score)) + geom_histogram()       │
│                                                                  │
│ Begin research analysis...                                       │
│                                                                  │
│ Citation in manuscript:                                          │
│ "Community Resilience Mapping Project (2025)..."                │
└─────────────────────────────────────────────────────────────────┘

TOTAL TIME: ~15 minutes from landing to productive analysis
SUCCESS: ✓ Found data, ✓ Verified methodology, ✓ Downloaded, ✓ Cited
```

---

## 9. User Flow: Journalist Path

```
JOURNALIST JOURNEY MAP
════════════════════════════════════════════════════════════════════

ENTRY POINT: Editor email → "Check out this resilience mapping tool"
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ HOMEPAGE                                          Time: 0:00     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌──────────────┬──────────────┬──────────────┐                  │
│ │ 🗺️ EXPLORE  │ 📊 ANALYZE  │ 📚 LEARN     │ ← CLICK THIS      │
│ │             │             │              │                    │
│ │ [Start]     │ [Browse]    │ [Research]   │                    │
│ └──────────────┴──────────────┴──────────────┘                  │
│                                                                  │
│ RECENT RESEARCH HIGHLIGHTS:                                      │
│ "1,059 resilient communities..."  ← Skim this                   │
│ "Southeast clustering..."          ← Interesting!               │
│                                                                  │
│ Decision: "I want to see the map" → Click [Start Exploring]    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ /explore PAGE (new discovery-focused page)        Time: 0:02     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ DISCOVER RESILIENT COMMUNITIES                                   │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ [Interactive map preview]                                   │ │
│ │ (showing Southeast cluster highlighted)                     │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ FEATURED STORIES:                                                │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 🏞️ "Rural Tennessee Defies the Odds"                        │ │
│ │ Rutherford County tract shows health outcomes 4.7σ better   │ │
│ │ than predicted despite being classified as food desert.     │ │
│ │ Population: 6,891 | Median income: $58K | Top 0.1%          │ │
│ │ [View on map →] [Read story →]                              │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ Decision: "This is my story!" → Click [View on map]            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ /map PAGE (tract pre-selected)                    Time: 0:05     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ [Map centered on Rutherford County, TN]                         │
│ [Tract 47149041500 highlighted with popup open]                 │
│                                                                  │
│ Popup shows:                                                     │
│ - Score: +4.75 (Top 0.1%)                                       │
│ - Population: 6,891                                             │
│ - Health metrics                                                │
│ - [Download tract data] [Compare nearby]                        │
│                                                                  │
│ Journalist actions:                                              │
│ ✓ Screenshot map for article                                    │
│ ✓ Note exact statistics                                         │
│ ✓ Click nearby tracts to compare                                │
│ ✓ Download tract-specific CSV for fact-checking                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ EXTERNAL FOLLOW-UP                                Time: 0:15+    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Leave website to:                                                │
│ - Google "Rutherford County Tennessee health department"        │
│ - Find local community organizations                            │
│ - Plan phone interviews                                         │
│ - Draft article with data points                                │
│                                                                  │
│ Article includes:                                                │
│ - Map screenshot from website                                   │
│ - Attribution: "Community Resilience Mapping Project"           │
│ - Link to website in online version                             │
│ - Human-interest angle from local interviews                    │
└─────────────────────────────────────────────────────────────────┘

TOTAL TIME: ~15 minutes on site + external follow-up
SUCCESS: ✓ Found story, ✓ Got visuals, ✓ Verified data, ✓ Attributed
```

---

## 10. Key UX Principles Summary

```
┌─────────────────────────────────────────────────────────────────┐
│ CORE UX DESIGN PRINCIPLES FOR THIS PLATFORM                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ 1. MULTI-PERSONA DESIGN                                         │
│    ────────────────────────────────────────────────────────     │
│    Don't force all users through single funnel.                 │
│    Provide parallel pathways for different goals:               │
│    • Exploration (map-first)                                    │
│    • Analysis (data-first)                                      │
│    • Research (findings-first)                                  │
│                                                                  │
│ 2. PROGRESSIVE DISCLOSURE                                       │
│    ────────────────────────────────────────────────────────     │
│    Start simple, reveal complexity on demand:                   │
│    • Quick filters → Advanced filters                           │
│    • Collapsed rows → Expanded details                          │
│    • Summary stats → Full methodology                           │
│                                                                  │
│ 3. CONTEXT OVER RAW DATA                                        │
│    ────────────────────────────────────────────────────────     │
│    Help users interpret numbers:                                │
│    • "+4.75" → "Top 0.1% (better than 99.9%)"                  │
│    • Show distribution histogram                                │
│    • Provide benchmarks (county, state, national)               │
│                                                                  │
│ 4. MOBILE-FIRST INTERACTIONS                                    │
│    ────────────────────────────────────────────────────────     │
│    Adapt to device capabilities:                                │
│    • Desktop: Table with inline expansion                       │
│    • Tablet: Hybrid table/cards                                 │
│    • Mobile: Card stack with bottom sheet filters               │
│                                                                  │
│ 5. ACCESSIBILITY AS DEFAULT                                     │
│    ────────────────────────────────────────────────────────     │
│    Not an afterthought:                                          │
│    • Keyboard navigation for all features                       │
│    • Screen reader support (ARIA labels)                        │
│    • High contrast, readable fonts                              │
│    • Respect prefers-reduced-motion                             │
│                                                                  │
│ 6. PERFORMANCE MATTERS                                          │
│    ────────────────────────────────────────────────────────     │
│    Large datasets require optimization:                         │
│    • Virtualized rendering (DOM size <500 nodes)                │
│    • Infinite scroll over pagination                            │
│    • Debounced filters (300ms)                                  │
│    • Lazy loading of heavy components                           │
│                                                                  │
│ 7. SHAREABILITY & REPRODUCIBILITY                               │
│    ────────────────────────────────────────────────────────     │
│    Science requires transparency:                                │
│    • URL params for all filter states                           │
│    • Shareable filtered views                                   │
│    • Download filtered subsets                                  │
│    • Clear version/timestamp on exports                         │
│                                                                  │
│ 8. TRUST THROUGH TRANSPARENCY                                   │
│    ────────────────────────────────────────────────────────     │
│    Academic credibility requires honesty:                        │
│    • Limitations prominently displayed                          │
│    • Data sources clearly cited                                 │
│    • Methodology fully documented                               │
│    • Peer review status labeled                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

**Document Version:** 1.0
**Last Updated:** 2025-12-30
**Purpose:** Visual reference for UX proposals
**Next Steps:** User testing, stakeholder review, implementation planning
