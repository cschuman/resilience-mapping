# Table Interaction Patterns for 68K Row Dataset
## Technical Specifications & UX Guidelines

**Date:** December 30, 2025
**Focus:** Performance, Accessibility, Mobile Optimization

---

## 1. Performance Architecture

### 1.1 Current State Analysis

```
Current Implementation:
├─ Server-side pagination: 100 rows per page
├─ Total pages: 681 pages
├─ Loading time: ~200ms per page
├─ Client-side rendering: Full table HTML
└─ No virtualization
```

**Performance Issues:**
- 681 pages is cognitively overwhelming
- Each navigation requires full server round-trip
- No progressive enhancement
- Mobile experience is identical to desktop (poor)

### 1.2 Recommended Architecture: Hybrid Virtualization

```
┌─────────────────────────────────────────────────────────────────┐
│ TIER 1: INITIAL LOAD (SSR)                                      │
├─────────────────────────────────────────────────────────────────┤
│ Server generates:                                                │
│ ├─ First 50 rows (HTML table)                                   │
│ ├─ Metadata (total count, distribution stats)                   │
│ ├─ Filter state (from URL params)                               │
│ └─ Skeleton for remaining rows                                  │
│                                                                  │
│ Benefits:                                                        │
│ ✓ Fast Time to First Paint (TTFP)                              │
│ ✓ SEO-friendly (content in HTML)                                │
│ ✓ Works without JavaScript (progressive enhancement)            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ TIER 2: CLIENT-SIDE HYDRATION                                   │
├─────────────────────────────────────────────────────────────────┤
│ JavaScript enhances to:                                          │
│ ├─ Virtualized scrolling (render only visible rows)             │
│ ├─ Infinite scroll (load next batch on demand)                  │
│ ├─ Client-side sort (for loaded data)                           │
│ └─ Instant filter preview (before server round-trip)            │
│                                                                  │
│ Technical stack:                                                 │
│ - @tanstack/svelte-virtual for virtualization                   │
│ - IntersectionObserver for infinite scroll trigger              │
│ - Optimistic UI updates for filters                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ TIER 3: PROGRESSIVE LOADING                                     │
├─────────────────────────────────────────────────────────────────┤
│ Load additional data:                                            │
│ ├─ When user scrolls to 80% of cached rows                      │
│ ├─ Fetch 200 rows at a time (balance: requests vs payload)     │
│ ├─ Cache in memory (LRU cache, max 1000 rows)                  │
│ └─ Show loading skeleton for new rows                           │
│                                                                  │
│ Edge cases:                                                      │
│ - Slow network: Show inline spinner, don't block UI             │
│ - Network error: Retry with exponential backoff                 │
│ - User scrolls too fast: Cancel pending requests, fetch current │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 API Design for Efficient Loading

```typescript
// Endpoint: GET /api/tracts

interface TractListRequest {
  // Pagination
  offset: number;        // Starting row (0-indexed)
  limit: number;         // Rows to return (default: 200, max: 500)

  // Sorting
  sort: string;          // Column name (e.g., "resilience_score")
  order: 'asc' | 'desc'; // Sort direction

  // Filtering
  state?: string;               // State abbreviation (e.g., "CA")
  county?: string;              // County name (partial match)
  score_min?: number;           // Minimum resilience score
  score_max?: number;           // Maximum resilience score
  pop_min?: number;             // Minimum population
  pop_max?: number;             // Maximum population
  lila_only?: boolean;          // Only LILA tracts
  percentile_tier?: string;     // "top_1", "top_5", "top_10"
  community_type?: string[];    // ["college", "military", "rural"]

  // Response format
  format: 'json' | 'csv' | 'geojson';
}

interface TractListResponse {
  data: Tract[];                // Array of tract objects
  metadata: {
    total: number;              // Total matching rows
    offset: number;             // Current offset
    limit: number;              // Current limit
    has_more: boolean;          // More rows available?
    filters_applied: string[];  // Active filters
    distribution: {             // Score distribution
      bins: number[];           // Histogram bins
      counts: number[];         // Count per bin
    };
  };
}

// Example request:
GET /api/tracts?offset=0&limit=200&sort=resilience_score&order=desc&state=CA&score_min=1.0

// Example response:
{
  "data": [
    {
      "fips": "06001400100",
      "state": "CA",
      "county": "Alameda",
      "resilience_score": 4.23,
      "percentile": 99.8,
      "population": 5234,
      "lila_status": true,
      // ... additional fields
    },
    // ... 199 more rows
  ],
  "metadata": {
    "total": 1234,
    "offset": 0,
    "limit": 200,
    "has_more": true,
    "filters_applied": ["state=CA", "score_min=1.0"],
    "distribution": {
      "bins": [-3, -2, -1, 0, 1, 2, 3, 4, 5],
      "counts": [5, 23, 156, 789, 178, 63, 15, 4, 1]
    }
  }
}
```

---

## 2. Table UI Components

### 2.1 Column Configuration

**Essential columns (always visible):**
```
┌────────────┬─────────────────────────┬───────────┬────────────┬──────────┐
│ State      │ Location                │ Score     │ Population │ Actions  │
│ (2 chars)  │ (County, tract)         │ (±X.XX)   │ (X,XXX)    │ (links)  │
├────────────┼─────────────────────────┼───────────┼────────────┼──────────┤
│ CA         │ Alameda County          │ +4.23     │ 5,234      │ View     │
│            │ Tract 400100            │ (Top 1%)  │            │ Compare  │
├────────────┼─────────────────────────┼───────────┼────────────┼──────────┤
│ TN         │ Rutherford County       │ +4.75     │ 6,891      │ View     │
│            │ Tract 041500            │ (Top 0.1%)│            │ Compare  │
└────────────┴─────────────────────────┴───────────┴────────────┴──────────┘

Width allocation:
- State: 80px (fixed)
- Location: 280px (flex)
- Score: 140px (fixed)
- Population: 120px (fixed)
- Actions: 120px (fixed)
Total minimum: 740px
```

**Optional columns (user can toggle):**
```
Available in column selector:
☐ FIPS Code (geoid)
☐ Median Income
☐ % Below Poverty
☐ LILA Status
☐ Food Access Score
☐ Predicted Health Score
☐ Actual Health Score
☐ Residual (raw)
☐ Urban/Rural
☐ Metro Area
☐ Congressional District (if added)
```

### 2.2 Column Customization UI

```
┌─────────────────────────────────────────────────────────────────┐
│ [🔽 Columns] ← Dropdown button in table header                  │
│                                                                  │
│ ┌─────────────────────────────────────┐                         │
│ │ Visible Columns                     │                         │
│ │ ─────────────────────────────────── │                         │
│ │ ☑ State                             │ ← Drag handle           │
│ │ ☑ Location                          │ ← Always required       │
│ │ ☑ Resilience Score                  │ ← Always required       │
│ │ ☑ Population                        │                         │
│ │ ☐ FIPS Code                         │                         │
│ │ ☐ Median Income                     │                         │
│ │ ☐ LILA Status                       │                         │
│ │ ☐ % Below Poverty                   │                         │
│ │                                     │                         │
│ │ [Reset to Default]  [Apply]         │                         │
│ └─────────────────────────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘

Persistence:
- Save preference to localStorage
- URL param: ?cols=state,location,score,pop,income
- Allow sharing of custom column views
```

### 2.3 Sorting Interaction

```
┌─────────────────────────────────────────────────────────────────┐
│ Column Header Interaction Pattern                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ DEFAULT STATE:                                                   │
│ ┌─────────────────────────┐                                     │
│ │ Resilience Score ↕      │ ← Neutral state (unsorted)          │
│ └─────────────────────────┘                                     │
│                                                                  │
│ FIRST CLICK (descending):                                        │
│ ┌─────────────────────────┐                                     │
│ │ Resilience Score ↓      │ ← Active sort (dark icon)           │
│ └─────────────────────────┘                                     │
│                                                                  │
│ SECOND CLICK (ascending):                                        │
│ ┌─────────────────────────┐                                     │
│ │ Resilience Score ↑      │ ← Active sort (dark icon)           │
│ └─────────────────────────┘                                     │
│                                                                  │
│ THIRD CLICK (clear):                                             │
│ ┌─────────────────────────┐                                     │
│ │ Resilience Score ↕      │ ← Back to neutral (default order)   │
│ └─────────────────────────┘                                     │
│                                                                  │
│ SHIFT + CLICK (multi-column sort):                               │
│ ┌─────────────────────────┐  ┌─────────────────────────┐        │
│ │ State ↓ ¹               │  │ Resilience Score ↓ ²    │        │
│ └─────────────────────────┘  └─────────────────────────┘        │
│ ← Primary sort               ← Secondary sort                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Keyboard support:
- Tab to column header
- Enter/Space to cycle sort
- Shift+Enter for multi-column sort

Screen reader:
- Announce: "Resilience Score, sortable column, currently sorted descending, activate to sort ascending"
```

### 2.4 Inline Row Expansion

```
┌─────────────────────────────────────────────────────────────────┐
│ COLLAPSED ROW (default)                                          │
├─────────────────────────────────────────────────────────────────┤
│ [>] CA   Alameda County, Tract 400100    +4.23   5,234   View   │
│     ↑                                    (Top 1%)                │
│     └─ Expansion toggle                                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓ (click to expand)
┌─────────────────────────────────────────────────────────────────┐
│ EXPANDED ROW                                                     │
├─────────────────────────────────────────────────────────────────┤
│ [v] CA   Alameda County, Tract 400100    +4.23   5,234   View   │
│     ↑                                    (Top 1%)                │
│     └─ Collapse toggle                                           │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ EXPANDED DETAILS                                            │ │
│ │                                                             │ │
│ │ ┌──────────────────────┐  ┌──────────────────────────────┐ │ │
│ │ │ Quick Stats          │  │ Mini Map Preview             │ │ │
│ │ ├──────────────────────┤  │                              │ │ │
│ │ │ FIPS: 06001400100    │  │  ┌────────────────────────┐  │ │ │
│ │ │ Population: 5,234    │  │  │    [Interactive map]   │  │ │ │
│ │ │ Median Inc: $72,000  │  │  │    showing this tract  │  │ │ │
│ │ │ Poverty: 8.2%        │  │  │    + neighbors         │  │ │ │
│ │ │ LILA: Yes            │  │  │                        │  │ │ │
│ │ │ Urban/Rural: Urban   │  │  └────────────────────────┘  │ │ │
│ │ │                      │  │  [Open in full map →]        │ │ │
│ │ └──────────────────────┘  └──────────────────────────────┘ │ │
│ │                                                             │ │
│ │ ┌───────────────────────────────────────────────────────┐  │ │
│ │ │ Health Outcomes vs. Predicted                         │  │ │
│ │ ├───────────────────────────────────────────────────────┤  │ │
│ │ │ Diabetes: 6.2% (predicted: 9.8%) ✓ Better            │  │ │
│ │ │ Obesity: 22.1% (predicted: 28.4%) ✓ Better           │  │ │
│ │ │ High BP: 28.3% (predicted: 31.7%) ✓ Better           │  │ │
│ │ └───────────────────────────────────────────────────────┘  │ │
│ │                                                             │ │
│ │ [Download Tract Data CSV] [Add to Comparison] [Share]      │ │
│ │                                                             │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

Interaction:
- Click anywhere in row to expand
- Click again to collapse
- Arrow keys to navigate between rows
- Expand/collapse with Enter/Space
- Only one row expanded at a time (optional: allow multiple)

Animation:
- Smooth height transition (300ms ease-out)
- Fade in details content (200ms delay)
- Mini map loads lazily (only when expanded)
```

---

## 3. Filtering System

### 3.1 Quick Filters (Above Table)

```
┌─────────────────────────────────────────────────────────────────┐
│ QUICK FILTERS BAR                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌────────────────────────────────────────────────────────────┐  │
│ │ 🔍 Search by location...                     [Clear] [X]   │  │
│ │    (county name, ZIP, city)                                │  │
│ └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│ │ State        │ │ Score        │ │ Population   │            │
│ │ All States ▼ │ │ Any      ▼   │ │ Any      ▼   │            │
│ └──────────────┘ └──────────────┘ └──────────────┘            │
│                                                                  │
│ [+ Advanced Filters]                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Behavior:
- Auto-apply on change (no "Apply" button needed)
- Debounce text search (300ms)
- Update URL params for shareability
- Show active filter count badge
```

### 3.2 Advanced Filters (Progressive Disclosure)

```
┌─────────────────────────────────────────────────────────────────┐
│ ADVANCED FILTERS PANEL (accordion/modal)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ▼ GEOGRAPHIC FILTERS                                            │
│ ├─ State: [Multi-select dropdown]                               │
│ │  ☐ California                                                 │
│ │  ☐ Texas                                                      │
│ │  ☑ Tennessee (1 selected)                                     │
│ │  ...                                                           │
│ ├─ Region: [Checkboxes]                                         │
│ │  ☐ Northeast  ☐ Southeast  ☑ Midwest  ☐ West                │
│ ├─ Metro Status: [Radio buttons]                                │
│ │  ○ Any  ○ Metro only  ○ Non-metro only                       │
│ └─ County: [Autocomplete text input]                            │
│                                                                  │
│ ▼ RESILIENCE FILTERS                                            │
│ ├─ Score Range: [Dual-handle slider]                            │
│ │  ─●────────────●─                                             │
│ │  -3.0       0.0       +5.0                                    │
│ │  Min: 0.0   Max: 5.0                                          │
│ ├─ Percentile Tier: [Dropdown]                                  │
│ │  ☐ Top 1%                                                     │
│ │  ☑ Top 5%                                                     │
│ │  ☐ Top 10%                                                    │
│ │  ☐ Above Average (>50th percentile)                          │
│ └─ Outlier Type: [Radio buttons]                                │
│    ○ Any  ○ Positive outliers  ○ Negative outliers             │
│                                                                  │
│ ▼ DEMOGRAPHIC FILTERS                                           │
│ ├─ Population: [Range inputs]                                   │
│ │  Min: [    1,000] Max: [  50,000]                            │
│ ├─ Median Income: [Range slider]                                │
│ │  ─●────────────●─                                             │
│ │  $0      $50k      $100k      $150k+                         │
│ ├─ % Below Poverty: [Range slider]                              │
│ │  ─●────────────●─                                             │
│ │  0%     10%     20%     30%+                                  │
│ └─ Age Distribution: [Checkboxes]                               │
│    ☐ High elderly (>20%)                                        │
│    ☐ High youth (>30% under 18)                                 │
│                                                                  │
│ ▼ COMMUNITY CHARACTERISTICS                                     │
│ ├─ LILA Status: [Checkbox]                                      │
│ │  ☑ Only show LILA tracts                                     │
│ ├─ Community Type: [Multi-select]                               │
│ │  ☐ College town                                               │
│ │  ☐ Military base proximity                                    │
│ │  ☐ Healthcare access (FQHC present)                          │
│ │  ☐ High faith infrastructure                                  │
│ └─ Urban/Rural: [Radio buttons]                                 │
│    ○ Any  ○ Urban  ○ Rural                                      │
│                                                                  │
│ ─────────────────────────────────────────────────────────────── │
│                                                                  │
│ Active Filters: Tennessee, Score 0-5, Top 5%                    │
│ Showing: 45 of 68,170 tracts                                    │
│                                                                  │
│ [Clear All] [Save Filter Set] [Share URL] [Apply Filters]       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Features:
- Collapsible sections (reduce visual overwhelm)
- Real-time count preview ("Showing X tracts")
- Save filter sets to localStorage
- Share filtered view via URL
- Export filtered data to CSV
```

### 3.3 Filter Presets (One-Click)

```
┌─────────────────────────────────────────────────────────────────┐
│ FILTER PRESETS (Quick access buttons)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Commonly Used:                                                   │
│ [Top Performers (>2σ)]                                          │
│ [LILA Tracts Only]                                              │
│ [High Population (>10K)]                                        │
│ [Positive Outliers]                                             │
│                                                                  │
│ Research-Focused:                                                │
│ [College Towns]                                                  │
│ [Rural High-Performers]                                          │
│ [Urban Low-Income]                                               │
│                                                                  │
│ Custom (if logged in):                                           │
│ [My Saved Filter 1]                                             │
│ [My Saved Filter 2]                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Implementation:
const FILTER_PRESETS = {
  top_performers: {
    score_min: 2.0,
    label: "Top Performers (>2σ)"
  },
  lila_only: {
    lila_status: true,
    label: "LILA Tracts Only"
  },
  high_pop: {
    pop_min: 10000,
    label: "High Population (>10K)"
  }
};
```

---

## 4. Bulk Operations

### 4.1 Row Selection

```
┌─────────────────────────────────────────────────────────────────┐
│ TABLE WITH SELECTION                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌─┬────────────────────────────────────────────────────────┐    │
│ │☑│ Select All (50 on this page) | Select All (1,234 filtered)│ │
│ └─┴────────────────────────────────────────────────────────┘    │
│                                                                  │
│ ┌─┬───┬─────────────────────────┬──────────┬──────────┬──────┐ │
│ │ │St │ Location                │ Score    │ Pop      │ View │ │
│ ├─┼───┼─────────────────────────┼──────────┼──────────┼──────┤ │
│ │☑│CA │ Alameda County          │ +4.23    │ 5,234    │ View │ │
│ │☑│TN │ Rutherford County       │ +4.75    │ 6,891    │ View │ │
│ │☐│SC │ Pickens County          │ +4.41    │ 3,812    │ View │ │
│ │☑│MI │ Mecosta County          │ +4.24    │ 4,156    │ View │ │
│ └─┴───┴─────────────────────────┴──────────┴──────────┴──────┘ │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────┐    │
│ │ 3 rows selected                                          │    │
│ │                                                          │    │
│ │ [Compare Selected] [Download Selected] [Add to Collection]│   │
│ └──────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Keyboard shortcuts:
- Shift+Click: Select range
- Cmd/Ctrl+Click: Toggle individual
- Cmd/Ctrl+A: Select all visible
- Escape: Clear selection

Limits:
- Comparison: Max 10 tracts (prevents cognitive overload)
- Download: No limit
- Collection: Max 100 tracts (for performance)
```

### 4.2 Comparison View

```
┌─────────────────────────────────────────────────────────────────┐
│ COMPARISON VIEW (Modal or separate page)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Comparing 3 tracts:                                              │
│                                                                  │
│ ┌──────────────┬──────────────┬──────────────┬──────────────┐   │
│ │ Metric       │ CA Alameda   │ TN Rutherford│ MI Mecosta   │   │
│ ├──────────────┼──────────────┼──────────────┼──────────────┤   │
│ │ Score        │ +4.23 🥈     │ +4.75 🥇     │ +4.24 🥉     │   │
│ │ Percentile   │ 99.7%        │ 99.9%        │ 99.8%        │   │
│ │ Population   │ 5,234        │ 6,891        │ 4,156        │   │
│ │ Median Inc   │ $72,000      │ $58,000      │ $45,000      │   │
│ │ Poverty %    │ 8.2%         │ 12.4%        │ 18.7%        │   │
│ │ LILA         │ Yes          │ Yes          │ Yes          │   │
│ │ Urban/Rural  │ Urban        │ Suburban     │ Rural        │   │
│ ├──────────────┴──────────────┴──────────────┴──────────────┤   │
│ │ HEALTH OUTCOMES                                            │   │
│ ├──────────────┬──────────────┬──────────────┬──────────────┤   │
│ │ Diabetes     │ 6.2% ✓       │ 7.1% ✓       │ 8.9% ✓       │   │
│ │ Obesity      │ 22.1% ✓      │ 24.3% ✓      │ 28.1% ✓      │   │
│ │ High BP      │ 28.3% ✓      │ 29.7% ✓      │ 31.2% ✓      │   │
│ └──────────────┴──────────────┴──────────────┴──────────────┘   │
│                                                                  │
│ [Download Comparison CSV] [Share Comparison] [Close]            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Visual enhancements:
- Color code highest/lowest in each row
- Sparklines for distributions
- Radar chart for multi-metric comparison
- Export to PNG/PDF for presentations
```

---

## 5. Mobile Optimization

### 5.1 Responsive Breakpoints

```
DESKTOP (>1024px):
- Full table with all visible columns
- Inline expansion for details
- Advanced filters in sidebar

TABLET (768px - 1024px):
- Reduced column count (hide optional columns)
- Horizontal scroll for additional columns
- Filters in modal overlay

MOBILE (<768px):
- Switch to card-based layout (NO TABLE)
- Vertical stacking of information
- Bottom sheet for filters
```

### 5.2 Mobile Card Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ MOBILE VIEW (<768px)                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌─ Filters ──────────────────────────────────────┐              │
│ │ [State: All ▼] [Score: Any ▼] [🔍]             │              │
│ └────────────────────────────────────────────────┘              │
│                                                                  │
│ Showing 1,234 tracts                                             │
│                                                                  │
│ ┌────────────────────────────────────────────────┐              │
│ │ CALIFORNIA                                     │              │
│ │ Alameda County, Tract 400100                   │              │
│ │                                                │              │
│ │ Resilience Score: +4.23                        │              │
│ │ ████████████░░░░░░░░ Top 1%                   │              │
│ │                                                │              │
│ │ Population: 5,234                              │              │
│ │ Median Income: $72,000                         │              │
│ │                                                │              │
│ │ [View on Map] [Compare] [More ▼]              │              │
│ └────────────────────────────────────────────────┘              │
│                                                                  │
│ ┌────────────────────────────────────────────────┐              │
│ │ TENNESSEE                                      │              │
│ │ Rutherford County, Tract 041500                │              │
│ │                                                │              │
│ │ Resilience Score: +4.75                        │              │
│ │ ████████████████░░░░ Top 0.1%                 │              │
│ │                                                │              │
│ │ Population: 6,891                              │              │
│ │ Median Income: $58,000                         │              │
│ │                                                │              │
│ │ [View on Map] [Compare] [More ▼]              │              │
│ └────────────────────────────────────────────────┘              │
│                                                                  │
│ [Load More ↓]                                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Interaction:
- Swipe to dismiss card (optional)
- Tap card to expand for full details
- Sticky filter bar at top
- Infinite scroll for loading more
- Pull-to-refresh for new data
```

### 5.3 Mobile Filter Bottom Sheet

```
┌─────────────────────────────────────────────────────────────────┐
│ MOBILE FILTER SHEET (slides up from bottom)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌────────────────────────────────────────────────┐              │
│ │         ━━━━ (drag handle)                     │              │
│ │                                                │              │
│ │ Filters                                [Clear] │              │
│ │                                                │              │
│ │ State                                          │              │
│ │ [All States               ▼]                  │              │
│ │                                                │              │
│ │ Resilience Score                               │              │
│ │ ─●────────────●─                               │              │
│ │ Any score to +5.0                              │              │
│ │                                                │              │
│ │ Population                                     │              │
│ │ [Any size                 ▼]                  │              │
│ │                                                │              │
│ │ [▼ Advanced Filters]                           │              │
│ │                                                │              │
│ │ ─────────────────────────────────────────      │              │
│ │                                                │              │
│ │ Showing 1,234 results                          │              │
│ │                                                │              │
│ │ [Apply Filters]                                │              │
│ │                                                │              │
│ └────────────────────────────────────────────────┘              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Behavior:
- Swipe down or tap backdrop to close
- Auto-apply filters on interaction (no need for "Apply" button)
- Show result count in real-time
- Haptic feedback on filter change (iOS/Android)
```

---

## 6. Accessibility (WCAG 2.1 AA Compliance)

### 6.1 Keyboard Navigation

```
TAB SEQUENCE:
1. Quick filter: Search input
2. Quick filter: State dropdown
3. Quick filter: Score dropdown
4. Quick filter: Population dropdown
5. Advanced filters button
6. Column header: State (sortable)
7. Column header: Location (sortable)
8. Column header: Score (sortable)
9. Column header: Population (sortable)
10. Table row 1 (focusable container)
11. Table row 1: Actions (View link)
12. Table row 2 (focusable container)
13. ...continue through visible rows
14. Pagination: Previous button
15. Pagination: Next button

KEYBOARD SHORTCUTS:
- Tab/Shift+Tab: Navigate between focusable elements
- Enter/Space: Activate buttons, toggle expansion
- Arrow keys: Navigate between table rows (when row focused)
- Home/End: Jump to first/last visible row
- Cmd/Ctrl+F: Focus search filter
- Escape: Close filters, clear selection
- Shift+Click: Select range of rows
```

### 6.2 Screen Reader Support

```html
<!-- Table semantic structure -->
<table role="table" aria-label="Census tract resilience data">
  <thead>
    <tr>
      <th scope="col">
        <button
          aria-label="Sort by state, currently unsorted"
          aria-sort="none"
        >
          State ↕
        </button>
      </th>
      <th scope="col">
        <button
          aria-label="Sort by resilience score, currently sorted descending"
          aria-sort="descending"
        >
          Resilience Score ↓
        </button>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr aria-expanded="false">
      <td>CA</td>
      <td>
        <span aria-label="Resilience score plus 4.23, top 1 percent">
          +4.23 (Top 1%)
        </span>
      </td>
    </tr>
  </tbody>
</table>

<!-- Filter announcements -->
<div aria-live="polite" aria-atomic="true" class="sr-only">
  Filters updated. Showing 1,234 of 68,170 tracts.
</div>

<!-- Loading state -->
<div aria-live="polite" aria-busy="true" class="sr-only">
  Loading more results...
</div>
```

### 6.3 Visual Accessibility

```
COLOR CONTRAST:
- Text on background: 4.5:1 minimum (WCAG AA)
- Interactive elements: 3:1 minimum
- Score colors: Don't rely on color alone (use icons + text)

FOCUS INDICATORS:
- 2px solid outline
- High contrast color (#005FCC or theme-dependent)
- Offset from element by 2px
- Visible on all interactive elements

FONT SIZES:
- Minimum body text: 14px (0.875rem)
- Minimum interactive element: 16px (1rem)
- Table headers: 12px (0.75rem) uppercase with wider letter-spacing
- Mobile: Increase base size to 16px (prevents zoom on focus)

TOUCH TARGETS (mobile):
- Minimum: 44×44px (iOS/Android guidelines)
- Spacing between targets: 8px minimum
- Expandable click area for small elements
```

### 6.4 Reduced Motion Support

```css
/* Respect prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }

  /* Disable smooth scroll */
  html {
    scroll-behavior: auto;
  }

  /* Disable row expansion animation */
  .table-row[aria-expanded="true"] {
    transition: none;
  }
}
```

---

## 7. Performance Benchmarks

### 7.1 Loading Performance

```
TARGET METRICS:

First Contentful Paint (FCP):
- Desktop: <1.0s
- Mobile: <1.5s

Largest Contentful Paint (LCP):
- Desktop: <2.0s
- Mobile: <2.5s

Time to Interactive (TTI):
- Desktop: <2.5s
- Mobile: <3.5s

Initial table render (50 rows):
- Desktop: <200ms
- Mobile: <300ms

Filter application:
- Client-side (cached data): <50ms
- Server-side (new data): <300ms

Infinite scroll next batch:
- Fetch: <200ms
- Render: <100ms
```

### 7.2 Runtime Performance

```
TARGET METRICS:

Scroll performance:
- 60 FPS minimum (16.67ms per frame)
- No janky scrolling
- Virtualization keeps DOM size <500 nodes

Sort performance:
- Client-side (1000 rows): <100ms
- Server-side request: <300ms

Filter debounce:
- Text input: 300ms
- Dropdown: Immediate (no debounce)
- Range slider: 150ms

Memory usage:
- Initial load: <50MB
- After 1000 rows cached: <100MB
- Memory leak prevention: Clear cache on route change
```

---

## 8. Implementation Checklist

### Phase 1: Foundation (Week 1-2)
- [ ] API endpoint for paginated data (/api/tracts)
- [ ] Server-side filtering and sorting
- [ ] Basic table component with SSR
- [ ] URL parameter sync for shareability
- [ ] CSV download for full dataset

### Phase 2: Enhanced Interactions (Week 3-4)
- [ ] Client-side virtualization (TanStack Virtual)
- [ ] Infinite scroll implementation
- [ ] Inline row expansion
- [ ] Column customization
- [ ] Multi-column sorting

### Phase 3: Advanced Filtering (Week 5-6)
- [ ] Quick filters UI (state, score, population)
- [ ] Advanced filters panel (progressive disclosure)
- [ ] Filter presets
- [ ] Save/share filter sets
- [ ] Download filtered data

### Phase 4: Mobile Optimization (Week 7)
- [ ] Card-based layout for mobile
- [ ] Bottom sheet filters
- [ ] Touch-optimized interactions
- [ ] Responsive breakpoints

### Phase 5: Accessibility (Week 8)
- [ ] Keyboard navigation
- [ ] Screen reader support
- [ ] ARIA labels and live regions
- [ ] Focus management
- [ ] Color contrast audit
- [ ] Reduced motion support

### Phase 6: Polish (Week 9-10)
- [ ] Bulk operations (selection, comparison, download)
- [ ] Loading skeletons
- [ ] Error states
- [ ] Empty states
- [ ] Performance optimization
- [ ] Analytics instrumentation

---

## 9. Success Metrics

### Quantitative Metrics

**Engagement:**
- Average session duration on /data page: >3 minutes
- Filter usage rate: >40% of visitors
- Download rate: >15% of visitors
- Return visitor rate: >20%

**Performance:**
- Bounce rate: <30%
- Time to first interaction: <2 seconds
- Filter application time: <300ms
- Error rate: <1%

**Accessibility:**
- Keyboard task completion: >95%
- Screen reader task completion: >90%
- Mobile usability score: >90

### Qualitative Metrics

**User Feedback:**
- "Easy to filter data": >4/5 rating
- "Table performance is good": >4/5 rating
- "Found what I needed": >85% yes rate

**Task Completion:**
- Can researcher find and download California tracts with score >2.0 in <2 minutes? >90% success
- Can journalist identify top 5 tracts in their state in <1 minute? >85% success
- Can policymaker filter by state and export in <30 seconds? >95% success

---

## 10. Future Enhancements

### Advanced Features (Post-MVP)

1. **Saved Collections**
   - User accounts
   - Save favorite tracts
   - Share collections with collaborators
   - Email alerts for data updates

2. **Advanced Analytics**
   - Correlation analysis (within UI)
   - Cluster detection visualization
   - Trend analysis (if multi-year data available)
   - Export to statistical software (SPSS, Stata)

3. **Collaboration Features**
   - Commenting on tracts
   - Community ratings/reviews
   - Expert annotations
   - Research paper citations tracking

4. **API Enhancements**
   - GraphQL endpoint for flexible queries
   - Webhook support for data updates
   - Rate limiting and authentication
   - Comprehensive API documentation (Swagger/OpenAPI)

5. **Visualization Upgrades**
   - Interactive charts within table
   - Small multiples for comparisons
   - Export to presentation formats (PowerPoint, Google Slides)
   - Animated transitions for data updates

---

**Document Version:** 1.0
**Last Updated:** 2025-12-30
**Owner:** UX Design Team
**Review Cycle:** Quarterly or after major feature releases
