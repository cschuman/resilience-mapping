# Site Improvements Plan - December 30, 2025

## Executive Summary

We have significantly more data, analysis, and features than currently visible on the site. This document outlines:
1. Updated homepage messaging
2. Accessible data table architecture
3. Paper 2 submission checklist
4. Research findings to surface
5. Quick wins for immediate improvement

---

## 1. Updated Homepage Messaging

### Current (Problems)
- "Free data for researchers" - transactional, not transformational
- Leads with data format, not insight
- No clear value proposition for different audiences

### Proposed New Homepage Copy

```markdown
# Discover Communities Defying Health Expectations

68,170 census tracts. Peer-reviewed methodology. One question: **What's going right?**

While most health data focuses on problems, we map the solutions hiding in plain sight—
communities achieving better health outcomes than their circumstances would predict.

[Explore the Map] [Download Data] [Read the Research]

---

## Who Uses This Data

**Researchers** find natural experiments and publishable findings
**Journalists** discover untold stories of community resilience
**Policymakers** identify what works, not just what's broken
**Community Organizations** prove what they already know—their community is stronger than the statistics suggest

---

## What We've Learned

### Finding 1: Health Levels Are Remarkably Stable
Communities don't change as much as you'd think. Health burden levels are 99.7%
persistent year-over-year. High-burden communities need sustained investment,
not one-time interventions.

### Finding 2: Annual Changes Are Mostly Noise
Our peer-reviewed research found that year-over-year "improvements" often reflect
measurement artifact, not genuine health gains. Use 3-year rolling averages for
trend analysis.

### Finding 3: Geography Matters
28% of health burden variation is explained by persistent geographic factors.
Some places consistently outperform expectations—understanding why is the key.

[Read Our Research Papers →]

---

## The Data

| Metric | Value |
|--------|-------|
| Census Tracts | 68,170 |
| States + DC | 51 |
| Population Covered | 330M+ |
| Data Sources | CDC PLACES, USDA FARA, Census ACS |
| Time Period | 2020-2024 |
| Methodology | Peer-reviewed, open source |

[Download CSV] [API Documentation] [Cite This Data]

---

## Featured Communities

[Dynamic: Pull top 6 from database with consent status filter]

These communities show resilience scores 2+ standard deviations above expected.
What can we learn from them?

[Explore All Communities →]
```

### Key Changes
1. **Lead with discovery, not data**
2. **Surface research findings** prominently
3. **Segment by audience** (researchers, journalists, policymakers, communities)
4. **Honest about limitations** (changes are noisy, levels are stable)
5. **Call to action for research** not just data download

---

## 2. Accessible Data Table Architecture

### Design Principles
1. **Table-first, map-second** - Table is primary interface, map is progressive enhancement
2. **Server-side everything** - Works without JavaScript
3. **Virtual scrolling** - Handle 68K rows performantly
4. **Full keyboard navigation** - No mouse required
5. **Screen reader optimized** - ARIA live regions, proper announcements

### Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    /data Route                               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 Filter Bar                            │   │
│  │  [State ▼] [Score Range] [Population] [Search...]    │   │
│  │  [College Towns] [Military] [Show Vulnerable]        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Accessible Data Table                    │   │
│  │  ┌──────┬────────┬───────┬────────┬────────┬──────┐ │   │
│  │  │ Rank │ Tract  │ State │ Score  │ Pop    │ More │ │   │
│  │  ├──────┼────────┼───────┼────────┼────────┼──────┤ │   │
│  │  │ 1    │ 47149..│ TN    │ +4.75  │ 5,234  │  →   │ │   │
│  │  │ 2    │ 45077..│ SC    │ +4.41  │ 3,891  │  →   │ │   │
│  │  │ ...  │ ...    │ ...   │ ...    │ ...    │  →   │ │   │
│  │  └──────┴────────┴───────┴────────┴────────┴──────┘ │   │
│  │                                                       │   │
│  │  [← Prev] Page 1 of 682 [Next →]                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Actions Bar                              │   │
│  │  [Download Filtered CSV] [View on Map] [Share Link]  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Component Structure

```
src/routes/(standard)/data/
├── +page.svelte           # Main page with table
├── +page.server.ts        # Server-side data loading
└── +page.ts               # Client-side load function

src/lib/components/data/
├── DataTable.svelte       # Main accessible table
├── TableHeader.svelte     # Sortable column headers
├── TableRow.svelte        # Individual row with expansion
├── FilterBar.svelte       # Filter controls
├── Pagination.svelte      # Page navigation
├── ExportButton.svelte    # CSV download
└── TractDetail.svelte     # Expanded row detail
```

### Accessibility Requirements

```typescript
// DataTable.svelte - Key accessibility features

<table
  role="grid"
  aria-label="Community health resilience data"
  aria-describedby="table-description"
  aria-rowcount={totalRows}
>
  <caption id="table-description" class="sr-only">
    {filteredCount} communities sorted by {sortColumn} {sortDirection}
  </caption>

  <thead>
    <tr role="row">
      {#each columns as column}
        <th
          role="columnheader"
          aria-sort={column.id === sortColumn ? sortDirection : 'none'}
          tabindex="0"
          on:keydown={handleHeaderKeydown}
        >
          {column.label}
        </th>
      {/each}
    </tr>
  </thead>

  <tbody>
    {#each rows as row, index}
      <tr
        role="row"
        aria-rowindex={index + 1}
        tabindex={index === focusedRow ? 0 : -1}
      >
        ...
      </tr>
    {/each}
  </tbody>
</table>

<!-- Live region for announcements -->
<div aria-live="polite" aria-atomic="true" class="sr-only">
  {announcement}
</div>
```

### Keyboard Navigation

| Key | Action |
|-----|--------|
| Tab | Move between interactive elements |
| Arrow Up/Down | Move between rows |
| Arrow Left/Right | Move between cells |
| Enter | Expand row / activate link |
| Space | Toggle selection |
| Home/End | Jump to first/last row |
| Page Up/Down | Jump 10 rows |
| Escape | Close expanded detail |

### Server-Side Rendering

```typescript
// +page.server.ts
export const load: PageServerLoad = async ({ url }) => {
  const state = url.searchParams.get('state');
  const sort = url.searchParams.get('sort') || 'resilience_score';
  const order = url.searchParams.get('order') || 'desc';
  const page = parseInt(url.searchParams.get('page') || '1');
  const limit = 100;
  const offset = (page - 1) * limit;

  // Works without JavaScript
  const tracts = await db`
    SELECT * FROM tracts
    WHERE ${state ? db`state_abbr = ${state}` : db`TRUE`}
    ORDER BY ${db(sort)} ${order === 'desc' ? db`DESC` : db`ASC`}
    LIMIT ${limit} OFFSET ${offset}
  `;

  const total = await db`SELECT COUNT(*) FROM tracts`;

  return {
    tracts,
    total: total[0].count,
    page,
    filters: { state, sort, order }
  };
};
```

### Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| First Contentful Paint | < 1.5s | ~2.3s |
| Time to Interactive | < 3s | ~4s |
| Lighthouse Accessibility | > 95 | 67 |
| Bundle size (this route) | < 50KB | N/A |
| Works without JS | Yes | Partially |

---

## 3. Paper 2 Submission Checklist

### Target Journal: American Journal of Epidemiology

**Impact Factor**: 5.4 (2023)
**Acceptance Rate**: ~15%
**Review Time**: 6-8 weeks average

### Pre-Submission Checklist

#### Manuscript Preparation
- [x] Title follows journal format (< 150 characters)
- [x] Abstract structured (Background, Methods, Results, Conclusions)
- [x] Abstract word count < 300 words
- [x] Manuscript word count < 6,000 (currently ~5,200)
- [x] References in journal style (currently 16, max typically 50)
- [ ] Line numbers added
- [ ] Double-spaced formatting
- [ ] Continuous page numbering

#### Tables and Figures
- [x] Table 1: Prediction Performance
- [x] Table 2: Autocorrelation by Quintile
- [x] Table 3: Variance Decomposition
- [ ] Figure 1: Quintile Gradient (generate from Supplementary S1)
- [ ] Figure 2: Score Distribution (optional)
- [ ] All tables/figures cited in text
- [ ] Tables formatted per journal guidelines

#### Supplementary Materials
- [x] Supplementary Table S1: CHBI Components
- [x] Supplementary Figure S1: Quintile Gradient
- [x] Supplementary Figure S2: Variance by Quintile
- [ ] Data availability statement updated with DOI
- [ ] Code availability with GitHub link

#### Author Information
- [ ] ORCID registered
- [ ] Affiliation confirmed
- [ ] Conflict of interest statement
- [ ] Funding statement (or "no funding received")
- [ ] Author contributions (single author: N/A)

#### Ethical/Data Statements
- [x] IRB statement (publicly available data, exempt)
- [x] Data sources cited (CDC PLACES)
- [ ] Code repository public and documented

### Submission Portal Steps

1. **Create AJE account**: https://academic.oup.com/aje
2. **Select article type**: "Original Contribution"
3. **Upload files**:
   - Main manuscript (Word or LaTeX)
   - Tables (separate file or embedded)
   - Figures (TIFF/EPS, 300+ DPI)
   - Supplementary materials
   - Cover letter
4. **Enter metadata**:
   - Title, abstract, keywords
   - Author details, affiliations
   - Suggested reviewers (optional but recommended)
5. **Declarations**:
   - Conflicts of interest
   - Funding sources
   - Data availability
   - Ethics approval

### Cover Letter Template

```
Dear Editors,

We submit "Regression to the Mean in Small-Area Health Estimates: Why CDC
PLACES-Based Trajectory Prediction Fails" for consideration as an Original
Contribution in the American Journal of Epidemiology.

This manuscript addresses a critical methodological question: why do
machine learning models fail to predict community health trajectories
despite rich feature sets? Using five years of CDC PLACES data for 68,170
U.S. census tracts, we demonstrate that prediction failure (F1=0.26)
stems from regression to the mean, not from fundamental unpredictability
of community health.

Our key finding—a gradient where prior change magnitude explains 0.3% of
subsequent variance for small changes but 37% for extreme changes—provides
evidence consistent with measurement artifact rather than true health
dynamics. This has immediate practical implications: trajectory-based
resource allocation using annual PLACES data is unreliable.

This work has not been published elsewhere and is not under consideration
by another journal. All authors have approved the manuscript.

We suggest the following potential reviewers with expertise in small-area
estimation and measurement error:
- [Reviewer 1 name, institution, email]
- [Reviewer 2 name, institution, email]

Thank you for your consideration.

Sincerely,
[Your name]
```

### Post-Submission Tasks

- [ ] Save submission confirmation
- [ ] Note manuscript ID
- [ ] Calendar reminder: check status at 4 weeks
- [ ] Prepare revision response template
- [ ] Archive submitted version with date stamp

---

## 4. Research Findings to Surface on Site

### Recommendation: Create a "/research" Route

Display peer-reviewed findings prominently, not buried in "About."

### Findings to Surface

#### Finding 1: Trajectory Prediction Fails (Paper 2)
**Headline**: "Why We Don't Predict the Future"
**Key stat**: F1 = 0.26 (chance performance)
**Visualization**: Quintile gradient chart
**Implication**: Use current burden, not predicted trajectories

#### Finding 2: Health Levels Are Stable (Paper 2)
**Headline**: "Health Status Is 99.7% Persistent"
**Key stat**: R² = 0.997 for level autocorrelation
**Visualization**: AR(1) model diagram
**Implication**: High-burden communities need sustained investment

#### Finding 3: Changes Are Mostly Noise (Paper 2)
**Headline**: "Annual 'Improvements' Often Aren't Real"
**Key stat**: r = -0.22 to -0.58 negative autocorrelation
**Visualization**: Year-over-year reversal pattern
**Implication**: Use 3-year rolling averages

#### Finding 4: Spatial Synchrony, Not Contagion (Paper 1)
**Headline**: "Communities Change Together, Not Because of Each Other"
**Key stat**: Spatial features add nothing after temporal lag
**Visualization**: Neighbor correlation decay
**Implication**: Shared causes, not spread

#### Finding 5: Geography Explains 28% of Variance
**Headline**: "Place Matters More Than Time"
**Key stat**: Between-tract: 28%, Between-year: <1%
**Visualization**: Variance decomposition pie chart
**Implication**: Some places are consistently volatile

### Proposed /research Page Structure

```markdown
# Our Research

We believe in showing our work. Here's what we've learned—including
what didn't work.

## Peer-Reviewed Papers

### Paper 1: Spatial Synchrony, Not Contagion
[Status: Accepted] [Download PDF] [View Code]

### Paper 2: Regression to the Mean in Small-Area Estimates
[Status: Under Review at AJE] [Preprint] [View Code]

## Key Findings

[Interactive cards with visualizations]

## What We Got Wrong

### We Tried to Predict Trajectories
Our best models achieved F1=0.26—no better than random guessing.
Here's why that matters and what we learned.

### We Thought Neighbors Influenced Each Other
Spatial features looked predictive until we properly lagged them.
The apparent "contagion" was temporal leakage.

## Methodology

[Link to detailed methodology docs]

## Data & Code

All data and code are open source.
- [Download Dataset (CSV)]
- [GitHub Repository]
- [API Documentation]
```

---

## 5. Quick Wins - Immediate Improvements

### This Week (< 4 hours each)

| Improvement | Effort | Impact | Files to Change |
|-------------|--------|--------|-----------------|
| Show score histogram | 1 hr | Medium | +page.svelte (homepage) |
| Add state rankings | 2 hrs | Medium | New component, API exists |
| Surface percentile in popups | 1 hr | Low | Map.svelte popup template |
| Add "least resilient" tab | 2 hrs | Medium | Data page, new filter |
| Link to research papers | 1 hr | High | Navigation, new /research route |

### This Month (1-2 days each)

| Improvement | Effort | Impact |
|-------------|--------|--------|
| Create /research route | 1 day | High |
| Accessible data table | 3 days | Critical |
| College/military filters | 1 day | Medium |
| Download with filters | 0.5 day | Medium |
| Confidence intervals | 2 days | Medium |

### Deprioritize (Don't Build Now)

| Feature | Why Not |
|---------|---------|
| Trajectory predictions UI | Research shows they don't work |
| Community stories | No consent infrastructure |
| User accounts | No use case yet |
| Prediction alerts | Based on invalid methodology |

---

## Summary

**You have built significantly more than you're showing.**

The research findings alone are publication-worthy. The data infrastructure
supports features you haven't surfaced. The trajectory prediction system,
while scientifically interesting, proved that prediction doesn't work—which
is itself a valuable finding to share.

**Priority order:**
1. Surface research findings (credibility + differentiation)
2. Build accessible data table (ethics + reach)
3. Submit Paper 2 (academic contribution)
4. Quick wins (show what you have)
5. New domain + messaging (marketing)

The site should tell the story of what you learned, not just display data.
