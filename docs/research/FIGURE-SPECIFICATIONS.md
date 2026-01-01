# Figure Specifications for Research Papers

This document provides specifications for all figures referenced in the research papers. These specifications can be used by designers to create static images for publication, or by developers to create interactive web visualizations.

---

## Paper 4B: Immigrant Health Advantage (Hispanic Paradox)

### Figure 1: Conceptual Model of Immigrant Health Advantage Pathways

**Type:** Flow diagram / conceptual model
**Purpose:** Illustrate the theoretical framework

**Elements:**
- Central box: "Community Health Resilience"
- Incoming arrows from:
  - "Immigrant Selection" (solid arrow, hypothesized causal)
  - "Structural Poverty" (solid arrow, negative effect)
  - "Ethnic Composition" (dashed arrow, indirect/confounded)
  - "State Policy Context" (dashed arrow, moderator)
- Alternative explanations shown as dashed boxes:
  - "Return Migration Bias"
  - "Aggregation Artifact"
  - "Selection into Tracts"

**Colors:**
- Solid arrows: Primary hypothesized effects
- Dashed arrows: Alternative explanations tested
- Green: Positive associations
- Red: Negative associations
- Gray: Null/confounded

---

### Figure 2: Forest Plot of Hispanic Origin Subgroup Correlations

**Type:** Forest plot
**Purpose:** Show heterogeneity across Hispanic origin groups

**Data:**
| Origin Group | r | 95% CI Lower | 95% CI Upper |
|--------------|------|--------------|--------------|
| South American | +0.147 | +0.13 | +0.16 |
| Central American | +0.060 | +0.05 | +0.07 |
| Cuban | -0.030 | -0.08 | +0.02 |
| Mexican | -0.029 | -0.04 | -0.02 |
| Puerto Rican | -0.017 | -0.03 | 0.00 |
| **Hispanic (aggregate)** | **+0.006** | **0.00** | **+0.01** |

**Design Notes:**
- Point estimates as squares (size proportional to N)
- Horizontal lines for 95% CI
- Vertical dashed line at x=0 (null effect)
- Color code: Green for positive, red for negative, gray for aggregate
- Highlight that aggregate obscures heterogeneity

**Web Version:**
- Interactive tooltip showing exact values
- Click to filter map to that origin group

---

### Figure 3: Texas Map - Resilience Among Mexican-Majority Tracts

**Type:** Choropleth map
**Purpose:** Visualize the Austin-Border divergence

**Geography:** Texas state, census tract level
**Filter:** Mexican-majority tracts only (>30% Mexican)
**Variable:** Resilience score

**Color Scale:**
- Diverging: Red (low) → White (neutral) → Blue (high)
- Range: -3 to +3 SD
- Border tracts will appear deep red (-1.08 mean)
- Austin tracts will appear deep blue (+1.53 mean)

**Annotations:**
- Label "Border Counties" with callout showing -1.08 SD
- Label "Austin (Travis Co.)" with callout showing +1.53 SD
- Inset showing statewide distribution

**Web Version:**
- Interactive pan/zoom
- Hover for tract-level details
- Toggle to show poverty rate or foreign-born %

---

### Figure 4: Scatter Plot - Foreign-Born vs Resilience by Race/Ethnicity

**Type:** Scatter plot with regression lines
**Purpose:** Show cross-ethnic immigrant advantage

**Data:**
- X-axis: Foreign-born percentage (0-100%)
- Y-axis: Resilience score (-3 to +3)
- Two series:
  - Black-majority tracts (>30% Black): Blue points
  - Hispanic-majority tracts (>30% Hispanic): Orange points

**Regression Lines:**
- Black-majority: Steeper positive slope (r = +0.221)
- Hispanic-majority: Shallower positive slope (r = +0.133)

**Design Notes:**
- Alpha/transparency for overlapping points
- Confidence bands around regression lines
- Legend showing r values and N

**Web Version:**
- Interactive brushing to select regions
- Tooltip with tract details
- Option to color by state

---

### Figure 5: Mean Resilience by Foreign-Born Quintile

**Type:** Bar chart with error bars
**Purpose:** Illustrate generational decay gradient

**Data:**
| Quintile | Mean FB% | Resilience | SE |
|----------|----------|------------|-----|
| Q1 (Lowest) | 7% | -0.23 | 0.02 |
| Q2 | 14% | -0.21 | 0.02 |
| Q3 | 22% | -0.21 | 0.02 |
| Q4 | 31% | -0.15 | 0.02 |
| Q5 (Highest) | 46% | +0.05 | 0.02 |

**Design Notes:**
- Bars colored on gradient (red → blue as quintile increases)
- Error bars showing 95% CI
- Annotation: "+0.28 SD gradient from Q1 to Q5"
- Secondary axis or annotation showing poverty rates are similar (16-17%)

**Web Version:**
- Hover for detailed statistics
- Click to see tract distribution within quintile

---

### Figure 6: Heatmap - Resilience by Income × Foreign-Born

**Type:** 2D heatmap
**Purpose:** Show interaction between income and immigrant composition

**Axes:**
- X-axis: Foreign-born quartile (Q1-Q4)
- Y-axis: Median income quartile (Q1-Q4)

**Data:** 4×4 grid of mean resilience values

**Color Scale:**
- Diverging: Red (low) → White (neutral) → Blue (high)

**Expected Pattern:**
- Highest resilience: Medium-high income + high foreign-born (upper right)
- Lowest resilience: Low income regardless of foreign-born (bottom row)
- Shows that income moderates immigrant advantage

**Web Version:**
- Interactive cell selection
- Show N and CI for each cell
- Filter to specific states

---

## Paper 4: Health Equity / Structural Correlates

### Figure 1: State-Level Resilience Gap Distribution

**Type:** Diverging bar chart / lollipop chart
**Purpose:** Show range of state-level majority-minority gaps

**Data:** 43+ states with gap values
**Sort:** By gap value (ascending)

**Highlight States:**
- DC: +1.87 SD (highest)
- California: +0.15 SD (reversed)
- Washington: -0.42 SD (reversed, though small N)
- Mississippi: -0.89 SD (lowest)
- Louisiana: -0.78 SD

**Design Notes:**
- Vertical line at x=0
- Color: Green for positive (minority advantage), red for negative (minority disadvantage)
- Asterisk or marker for states that survived Bonferroni correction

---

### Figure 2: Correlation Matrix of Structural Correlates

**Type:** Correlation heatmap
**Purpose:** Show relationships between resilience and potential correlates

**Variables:**
- Resilience score
- % Black population
- % Hispanic population
- % Bachelor's degree+
- Median household income
- Poverty rate
- % Foreign-born
- Urban/rural

**Color Scale:**
- Blue-white-red diverging for correlations

---

### Figure 3: Bottom 10% Tract Composition

**Type:** Pie chart or stacked bar
**Purpose:** Show disproportionate burden on minority communities

**Data:**
- Low-resilience tracts (bottom 10%): 56.2% majority-minority
- National average: 26.4% majority-minority

**Design Notes:**
- Side-by-side comparison
- Clear labeling of disparity

---

## Shared / Site-Wide Figures

### College vs Prison: 4 SD Gap

**Type:** Comparison graphic
**Purpose:** Headline finding visualization

**Data:**
- College towns: +2.95 SD
- Prison towns: -0.98 SD
- Gap: ~4 SD

**Design:**
- Two large numbers with icons
- Arrow or gap indicator showing 4 SD
- Brief context text

---

### Ohio Bifurcation Map

**Type:** State map with tract-level choropleth
**Purpose:** Show Columbus/Cleveland divergence

**Annotations:**
- Columbus: 4 of top 10 nationally
- Cleveland: 3 of bottom 10 nationally
- Distance: ~60 miles

---

## Technical Specifications

### Color Palette
- **Positive/Good:** #22c55e (green-500)
- **Negative/Bad:** #ef4444 (red-500)
- **Neutral:** #6b7280 (gray-500)
- **Accent:** #3b82f6 (blue-500)

### Typography
- **Titles:** Inter Bold, 16-24px
- **Labels:** Inter Medium, 12-14px
- **Annotations:** Inter Regular Italic, 11-12px
- **Data values:** JetBrains Mono, 12-14px

### Export Formats
- **Print:** SVG or PDF, 300 DPI minimum
- **Web:** SVG preferred, PNG fallback at 2x resolution
- **Social:** 1200×630px for Open Graph

### Accessibility
- All figures must pass WCAG 2.1 AA contrast requirements
- Color should not be the only means of conveying information
- Provide alt text descriptions for all figures

---

## Implementation Priority

1. **Immediate (for paper pages):**
   - Figure 2 (Forest plot) - key finding
   - Figure 3 (Texas map) - signature visualization
   - Figure 4 (Scatter plot) - cross-ethnic test

2. **Secondary (enhance understanding):**
   - Figure 5 (Quintile bars)
   - Figure 6 (Heatmap)
   - Figure 1 (Conceptual model)

3. **Site-wide:**
   - College vs Prison graphic
   - Ohio map
   - State-level gap chart

---

*Specifications prepared for design/development handoff*
*Last updated: 2025-01-01*
