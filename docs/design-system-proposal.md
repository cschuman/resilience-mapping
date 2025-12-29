# Community Resilience Mapping - Visual Design System Proposal

**Version:** 1.0
**Date:** December 29, 2025
**Status:** Proposal for Review

---

## Executive Summary

This design system addresses critical visual hierarchy and consistency issues in the Community Resilience Mapping application. The current implementation suffers from:

1. **Unclear visual hierarchy** - competing elements on homepage, no clear focal point
2. **Inconsistent component patterns** - back buttons styled 3 different ways across pages
3. **Dense, overwhelming text** - 600-line About page with no progressive disclosure
4. **Disconnected experiences** - dark immersive map vs. content-heavy scrolling pages
5. **Poor wayfinding** - users can't orient themselves within the site

This proposal establishes a unified visual language that supports data visualization while improving readability, scannability, and user confidence.

---

## 1. Typography System

### Type Scale

#### Hierarchy Definitions

```
Display (Hero/Landing)
- Size: 48px (3rem)
- Weight: 700 (Bold)
- Line Height: 1.1
- Letter Spacing: -0.02em
- Usage: Homepage hero, major landing headlines
- Example: "Community Resilience Mapping"

Heading 1 (Page Title)
- Size: 40px (2.5rem)
- Weight: 700 (Bold)
- Line Height: 1.2
- Letter Spacing: -0.01em
- Usage: Page titles, primary headings
- Example: "About & Methodology"

Heading 2 (Section Title)
- Size: 24px (1.5rem)
- Weight: 600 (Semibold)
- Line Height: 1.3
- Letter Spacing: 0
- Usage: Major section divisions
- Example: "Methodology", "Research Question"

Heading 3 (Subsection)
- Size: 18px (1.125rem)
- Weight: 600 (Semibold)
- Line Height: 1.4
- Letter Spacing: 0
- Usage: Subsections within content
- Example: "Data Sources", "Statistical Model"

Heading 4 (Minor Heading)
- Size: 16px (1rem)
- Weight: 600 (Semibold)
- Line Height: 1.5
- Letter Spacing: 0
- Usage: Card titles, minor divisions
- Example: Story card titles

Body Large (Lead)
- Size: 18px (1.125rem)
- Weight: 400 (Regular)
- Line Height: 1.7
- Usage: Introductory paragraphs, emphasis
- Max Width: 65ch

Body (Standard)
- Size: 16px (1rem)
- Weight: 400 (Regular)
- Line Height: 1.7
- Usage: Default body text
- Max Width: 70ch

Body Small
- Size: 14px (0.875rem)
- Weight: 400 (Regular)
- Line Height: 1.6
- Usage: Secondary information, captions
- Max Width: 75ch

Caption
- Size: 13px (0.8125rem)
- Weight: 400 (Regular)
- Line Height: 1.5
- Usage: Figure captions, metadata, timestamps

Label
- Size: 12px (0.75rem)
- Weight: 600 (Semibold)
- Line Height: 1.4
- Letter Spacing: 0.05em
- Text Transform: Uppercase
- Usage: Category badges, form labels, stat labels

Code/Monospace
- Size: 14px (0.875rem)
- Weight: 400 (Regular)
- Line Height: 1.6
- Font Family: ui-monospace, 'SF Mono', Monaco, 'Cascadia Code', monospace
- Usage: FIPS codes, API endpoints, code blocks
```

### Font Stack

```css
/* Primary (UI) */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto',
             'Helvetica Neue', Arial, sans-serif;

/* Monospace (Data/Code) */
font-family: ui-monospace, 'SF Mono', Monaco, 'Cascadia Code',
             'Courier New', monospace;
```

### Typography Problems Solved

**BEFORE:**
- Homepage: 60px title competing with 20px subtitle competing with large buttons
- About page: No visual rhythm, all text feels same weight
- Unclear information hierarchy

**AFTER:**
- Clear 3-tier hierarchy: Display > Section > Body
- Scannable sections with predictable visual weight
- Readable line lengths (65-75ch) prevent eye strain

---

## 2. Color System

### Semantic Color Tokens

#### Surface Colors (Backgrounds)

```css
--surface-base: #0f172a          /* slate-900 - deepest background */
--surface-elevated: #1e293b      /* slate-800 - cards, panels */
--surface-overlay: #334155       /* slate-700 - modals, dropdowns */
--surface-subtle: rgba(51, 65, 85, 0.5)  /* transparent cards */
--surface-light: rgba(255, 255, 255, 0.95) /* light overlays (map legend) */
```

#### Text Colors

```css
--text-primary: #ffffff          /* white - primary headings, critical info */
--text-secondary: #e2e8f0        /* slate-200 - body text on dark */
--text-tertiary: #cbd5e1         /* slate-300 - less important text */
--text-muted: #94a3b8            /* slate-400 - metadata, captions */
--text-disabled: #64748b         /* slate-500 - disabled states */

/* Light surfaces (map legend) */
--text-dark-primary: #0f172a     /* slate-900 */
--text-dark-secondary: #1e293b   /* slate-800 */
--text-dark-tertiary: #475569    /* slate-600 */
```

#### Brand Colors (Primary Actions)

```css
--brand-primary: #10b981         /* emerald-500 - primary actions, success */
--brand-primary-hover: #059669   /* emerald-600 - hover states */
--brand-primary-light: #34d399   /* emerald-400 - highlights */
--brand-primary-subtle: rgba(16, 185, 129, 0.1) /* backgrounds */
```

#### Accent Colors (Secondary Actions)

```css
--accent-violet: #8b5cf6         /* violet-500 - community/stories */
--accent-violet-hover: #7c3aed   /* violet-600 */
--accent-blue: #3b82f6           /* blue-500 - economic */
--accent-amber: #f59e0b          /* amber-500 - food access */
```

#### Data Visualization Scale (Resilience Scores)

```css
/* Choropleth map colors - sequential */
--data-very-high: #059669        /* emerald-600 - >= 2.0 */
--data-high: #10b981             /* emerald-500 - 1.0 to 2.0 */
--data-medium: #fbbf24           /* amber-400 - 0.0 to 1.0 */
--data-low: #f97316              /* orange-500 - -1.0 to 0.0 */
--data-very-low: #dc2626         /* red-600 - < -1.0 */
--data-no-data: #9ca3af          /* gray-400 - missing data */
```

#### UI State Colors

```css
--border-subtle: #334155         /* slate-700 - subtle dividers */
--border-moderate: #475569       /* slate-600 - cards, inputs */
--border-strong: #64748b         /* slate-500 - emphasized borders */

--focus-ring: #10b981            /* emerald-500 - focus indicators */
--error: #f87171                 /* red-400 - error states */
--warning: #fbbf24               /* amber-400 - warnings */
--info: #60a5fa                  /* blue-400 - informational */
```

### Color Accessibility Standards

All text/background combinations meet WCAG AA (4.5:1 for body text, 3:1 for large text):

- White on `--surface-base` (#fff on #0f172a): 16.1:1
- `--text-secondary` on `--surface-base` (#e2e8f0 on #0f172a): 13.5:1
- `--text-tertiary` on `--surface-base` (#cbd5e1 on #0f172a): 11.2:1
- `--text-muted` on `--surface-base` (#94a3b8 on #0f172a): 7.4:1
- `--brand-primary` on `--surface-base` (#10b981 on #0f172a): 5.8:1 (use only for large text/icons)

### Color Problems Solved

**BEFORE:**
- Emerald-400, emerald-500, emerald-600 used inconsistently
- Violet-600 only on homepage stories button (feels random)
- No clear distinction between interactive vs. decorative color

**AFTER:**
- Emerald reserved for primary actions + positive data
- Accent colors have clear semantic meaning (violet=community, amber=food, blue=economic)
- Data visualization colors separate from UI colors

---

## 3. Component Library

### 3.1 Navigation Components

#### Persistent Header (NEW)

**Purpose:** Site-wide navigation, consistent wayfinding across all pages

```
Visual Description:
┌─────────────────────────────────────────────────────────────┐
│ [Logo/Icon] Community Resilience Mapping    [Map][Stories][About] │
└─────────────────────────────────────────────────────────────┘

- Height: 64px (fixed)
- Background: --surface-elevated with 1px bottom border (--border-subtle)
- Left: Logo/wordmark (18px semibold, --text-primary)
- Right: Horizontal nav links (14px medium, --text-muted)
- Sticky position on scroll
```

**Variants:**
- **Default:** Logo left, nav right (desktop)
- **Mobile:** Hamburger menu icon, logo center
- **Map Page:** Transparent background, overlays map

#### Breadcrumbs (NEW)

**Purpose:** Show location within site hierarchy

```
Visual:
Home > About > Methodology

- Size: 14px (--caption)
- Color: --text-muted
- Separator: chevron or / character
- Hover: --text-secondary
- Current page: --text-primary, not linked
```

#### Back Link (STANDARDIZED)

**Purpose:** Return to previous context

```css
/* Unified back link style */
.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-muted);
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  transition: all 0.15s ease;
}

.back-link:hover {
  color: var(--brand-primary);
  background: rgba(16, 185, 129, 0.1);
}

/* Icon: 20px Heroicon arrow-left */
```

**Problem Solved:** Currently 3 different implementations:
1. About page: inline-flex, no background
2. Stories page: inline-flex, different spacing
3. Map page: 36px button with slate background

**After:** One consistent pattern, always recognizable

### 3.2 Buttons

#### Primary Button

```css
.btn-primary {
  background: var(--brand-primary);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-primary:hover {
  background: var(--brand-primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-primary:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}

/* Icon variant: includes 20px icon + 8px gap */
```

**Usage:** Primary CTAs ("Explore the Map", "Submit a Story")

#### Secondary Button

```css
.btn-secondary {
  background: var(--surface-overlay);
  color: var(--text-primary);
  /* Same dimensions/states as primary */
}

.btn-secondary:hover {
  background: var(--border-strong);
}
```

**Usage:** Secondary actions ("Learn About Methodology", API links)

#### Accent Button (Violet)

```css
.btn-accent {
  background: var(--accent-violet);
  color: white;
  /* Same dimensions/states as primary */
}

.btn-accent:hover {
  background: var(--accent-violet-hover);
}
```

**Usage:** Community-specific actions ("Community Stories")

#### Ghost Button

```css
.btn-ghost {
  background: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border-subtle);
  /* Same dimensions */
}

.btn-ghost:hover {
  color: var(--text-primary);
  border-color: var(--border-moderate);
  background: rgba(255, 255, 255, 0.05);
}
```

**Usage:** Tertiary actions, filter buttons

#### Icon Button

```css
.btn-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: transparent;
  color: var(--text-muted);
  border: none;
  cursor: pointer;
}

.btn-icon:hover {
  background: var(--surface-overlay);
  color: var(--text-primary);
}

/* Mobile: min 44px tap target */
```

**Usage:** Legend toggle, close buttons

### 3.3 Cards

#### Stat Card

```
Visual Description:
┌──────────────────────┐
│   64,419            │  <- Value (2.5rem bold, --brand-primary)
│   Census Tracts     │  <- Label (0.8125rem, --text-muted)
└──────────────────────┘

- Background: --surface-subtle
- Padding: 1.5rem
- Border-radius: 12px
- Text-align: center
- Optional: subtle border (1px --border-subtle)
```

**Current Issue:** Homepage uses 4xl text (36px) which feels too large for dense stat grids

**Improvement:** Reduce to 2xl (24px) for better balance, use 3xl (30px) for hero stats

#### Story Card

```
┌───────────────────────────────────────┐
│ [HEALTH]              Detroit, MI     │ <- Header (category badge + location)
│                                        │
│ Urban Garden Network Transforms       │ <- Title (H4, 1.25rem semibold)
│ Food Desert                           │
│                                        │
│ A coalition of neighborhood...        │ <- Summary (0.875rem, --text-tertiary)
│ creating a model for other low-       │
│ income areas.                         │
│                                        │
│ ────────────────────────────────────  │ <- Border separator
│ View on map →                         │ <- Action link
└───────────────────────────────────────┘

- Background: --surface-elevated (1e293b80)
- Border: 1px --border-subtle
- Border-radius: 12px
- Padding: 1.5rem
- Hover: lift 4px, brighten border
```

#### Data Card (NEW - for dense methodology content)

```
┌───────────────────────────────────────┐
│ Statistical Model                     │ <- H3 with colored left border
│                                        │
│ We use OLS regression with state      │ <- Body text
│ fixed effects to predict health...    │
│                                        │
│ ┌──────────────────────────────────┐  │
│ │ Health ~ Poverty + Education     │  │ <- Code block (inset)
│ │        + Insurance + ...         │  │
│ └──────────────────────────────────┘  │
└───────────────────────────────────────┘

- Left border: 3px solid --brand-primary
- Background: --surface-subtle
- Padding: 1.5rem
- Margin-bottom: 1.5rem
```

**Purpose:** Break up long text sections, create visual anchors for scanning

### 3.4 Tables

#### Data Table (Homepage "Top Resilient Communities")

**Current Issues:**
- Row height too compressed (appears dense)
- Score badges good, but inconsistent with other badges
- Hover state too subtle

**Improved Design:**

```css
.data-table {
  width: 100%;
  background: var(--surface-elevated);
  border-radius: 12px;
  overflow: hidden;
}

.data-table thead {
  background: var(--surface-base);
  border-bottom: 1px solid var(--border-subtle);
}

.data-table th {
  padding: 1rem 1.25rem;
  font-size: 0.8125rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--text-muted);
  text-align: left;
}

.data-table td {
  padding: 1rem 1.25rem;  /* Increased from 0.75rem */
  font-size: 0.875rem;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-subtle);
}

.data-table tr:hover {
  background: rgba(16, 185, 129, 0.05);  /* Subtle emerald tint */
}

.data-table tr:last-child td {
  border-bottom: none;
}

/* FIPS codes */
.data-table .fips {
  font-family: var(--font-mono);
  color: var(--text-muted);
}

/* Score badge */
.score-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.8125rem;
  background: var(--brand-primary-subtle);
  color: var(--brand-primary);
}
```

### 3.5 Badges & Pills

#### Category Badge (Stories)

```css
.badge-category {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  /* Color set dynamically based on category */
}

/* Variants */
.badge-health {
  background: rgba(16, 185, 129, 0.2);
  color: var(--brand-primary);
}

.badge-food {
  background: rgba(245, 158, 11, 0.2);
  color: var(--accent-amber);
}

.badge-community {
  background: rgba(139, 92, 246, 0.2);
  color: var(--accent-violet);
}

.badge-economic {
  background: rgba(59, 130, 246, 0.2);
  color: var(--accent-blue);
}
```

### 3.6 Progressive Disclosure Components (NEW)

#### Accordion

**Purpose:** Collapse dense methodology sections for easier scanning

```
Visual:
┌────────────────────────────────────────────────────────┐
│ [+] Data Sources                                       │
└────────────────────────────────────────────────────────┘

When expanded:
┌────────────────────────────────────────────────────────┐
│ [-] Data Sources                                       │
│                                                        │
│ • CDC PLACES 2023 - Census tract-level health...      │
│ • USDA Food Access Research Atlas 2019 - Low-         │
│   income, low-access classification...                │
│ • Census ACS 2020 - Demographic and socio...          │
└────────────────────────────────────────────────────────┘

- Header: 1.125rem semibold, clickable, full-width
- Icon: 20px chevron (rotates on expand)
- Padding: 1rem header, 1rem 1.5rem content
- Border: 1px solid --border-subtle
- Border-radius: 8px
- Animation: 200ms ease height transition
```

#### Tabs (NEW - for API Documentation)

```
Visual:
┌─────────┬─────────┬─────────┬─────────┐
│ /stats  │ /tracts │ /fips   │ /geocode│  <- Active has bottom border
└─────────┴─────────┴─────────┴─────────┘
─────────────────────────────────────────
GET /api/stats
Returns aggregate statistics...

- Tab button: 0.875rem medium, padding 0.75rem 1.25rem
- Active: border-bottom 2px --brand-primary, color --text-primary
- Inactive: color --text-muted
- Content panel: padding 1.5rem, min-height 200px
```

#### Details/Summary (Lightweight alternative)

```html
<details class="disclosure">
  <summary>Show technical details</summary>
  <p>The regression model controls for...</p>
</details>
```

**Styling:**
- Summary: 0.875rem medium, cursor pointer, --text-muted
- Marker: Custom emerald triangle
- Padding: 0.5rem left margin for content

---

## 4. Layout System

### 4.1 Grid System

#### Responsive Breakpoints

```css
/* Mobile first */
--breakpoint-sm: 640px   /* Large phones */
--breakpoint-md: 768px   /* Tablets */
--breakpoint-lg: 1024px  /* Small laptops */
--breakpoint-xl: 1280px  /* Desktops */
--breakpoint-2xl: 1536px /* Large screens */
```

#### Container Widths

```css
.container {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
}

/* Max widths by content type */
.container-prose {
  max-width: 65ch;  /* ~800px - optimal for reading */
}

.container-standard {
  max-width: 1200px;  /* Homepage, Stories */
}

.container-wide {
  max-width: 1400px;  /* Data-heavy tables */
}

.container-full {
  max-width: 100%;  /* Map page */
}

@media (min-width: 640px) {
  .container {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
}

@media (min-width: 1024px) {
  .container {
    padding-left: 2rem;
    padding-right: 2rem;
  }
}
```

#### Grid Patterns

**Stat Grid (Homepage)**
```css
.stat-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;
}

@media (min-width: 640px) {
  .stat-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .stat-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
  }
}
```

**Story Grid**
```css
.story-grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: 1fr;
}

@media (min-width: 640px) {
  .story-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .story-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### 4.2 Page Layout Templates

#### Content Page (About, Methodology)

**Current Problem:** 600 lines of text, no breaks, overwhelming

**Proposed Structure:**

```
┌──────────────────────────────────────────────────────┐
│ [Header Nav - Persistent]                           │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ← Back                                             │  <- Breadcrumb (optional)
│                                                      │
│  About & Methodology                                │  <- H1
│  Understanding how community resilience scores      │  <- Subtitle
│  are calculated...                                  │
│                                                      │
│  ┌──────┬──────┬──────┬──────┐                     │
│  │ 64K  │  50  │ 330M │ 1059 │                     │  <- Stat grid
│  │Tracts│States│People│LILA  │                     │
│  └──────┴──────┴──────┴──────┘                     │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │ Research Question                           │   │  <- Section
│  │                                             │   │
│  │ Which communities demonstrate better...    │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │ [+] Methodology                             │   │  <- Accordion (collapsed)
│  └─────────────────────────────────────────────┘   │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │ [-] Score Categories                        │   │  <- Accordion (expanded)
│  │                                             │   │
│  │ ■ Very High  ≥2.0  Exceptionally better    │   │
│  │ ■ High  1.0-2.0  Notably better            │   │
│  │ ■ Medium  0-1.0  Slightly better           │   │
│  │ ■ Low  -1.0-0  Slightly worse              │   │
│  │ ■ Very Low  <-1.0  Notably worse           │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
│  ─────────────────────────────────────────────      │  <- Footer
│  Home | Map | API                                   │
│                                                      │
└──────────────────────────────────────────────────────┘

Max-width: 800px (65ch)
Padding: 2rem top/bottom, 1.5rem sides
```

**Key Changes:**
1. Persistent header for navigation (no need to scroll back up)
2. Stat grid at top (visual anchor, key info upfront)
3. Accordions for dense sections (scan headlines, expand as needed)
4. Consistent left-aligned layout (no centering except stats)

#### Data-Heavy Page (Homepage)

**Current Problem:** Competing CTAs, unclear what to do first

**Proposed Structure:**

```
┌─────────────────────────────────────────────────────────┐
│ [Header Nav]                                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│          Community Resilience Mapping                   │  <- H1 (centered)
│                                                         │
│     Identifying communities with strong social ties    │  <- Subtitle
│     and shared experiences that aren't captured by     │
│     traditional demographic metrics.                   │
│                                                         │
│     [Explore the Map →]                                │  <- Primary CTA (emerald)
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────┬──────┬──────┬──────┐                        │
│  │ 64K  │  50  │ 0.02 │ 330M │                        │  <- Stats (reduced size)
│  │Tracts│States│ Avg  │People│                        │
│  └──────┴──────┴──────┴──────┘                        │
│                                                         │
│  ┌───────────────────────────────────────────────┐    │
│  │ Top Resilient Communities                     │    │  <- Table section
│  │                                               │    │
│  │ [Table with improved row heights, hover]     │    │
│  └───────────────────────────────────────────────┘    │
│                                                         │
│  ┌───────────────────────────────────────────────┐    │
│  │ Community Stories                             │    │  <- Story preview
│  │                                               │    │
│  │ [2x2 grid of story cards]                    │    │
│  │                                               │    │
│  │         [View All Stories →]                  │    │
│  └───────────────────────────────────────────────┘    │
│                                                         │
│  ┌───────────────────────────────────────────────┐    │
│  │ API Access                                    │    │  <- Secondary actions
│  │                                               │    │
│  │ [GET /api/stats] [GET /api/tracts] [Docs →]  │    │
│  └───────────────────────────────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘

Max-width: 1200px
Hero: Full-width gradient
Content: Sections with clear vertical rhythm (3rem spacing)
```

**Key Changes:**
1. Single primary CTA (map) - violet "Stories" moved to preview section
2. Story preview section (show 4, link to full page)
3. Clearer visual sections with background cards
4. Vertical flow guides eye: Hero → Stats → Data → Stories → API

#### Immersive Page (Map)

**Current State:** Good - dark, full-screen, minimal chrome

**Minor Improvements:**

```
┌─────────────────────────────────────────────────────────┐
│ [←] Community Resilience Map    [Search...]  [≡][About]│  <- Fixed header
├─────────────────────────────────────────────────────────┤
│                                                         │
│                                                         │
│    [MAP FILLS ENTIRE VIEWPORT]                         │
│                                                         │
│                                                         │
│  ┌──────────────┐                                      │
│  │ Resilience   │ <- Legend (bottom-left)              │
│  │ ■ Very High  │                                      │
│  │ ■ High       │                                      │
│  │ ■ Medium     │                                      │
│  └──────────────┘                                      │
└─────────────────────────────────────────────────────────┘

Header: 56px tall (compact)
Background: Transparent with backdrop-blur
Legend: Semi-transparent white card
No footer (full immersion)
```

**Key Changes:**
1. Search moved to header (always accessible)
2. Header transparency (doesn't compete with map)
3. Persistent header even on scroll (access nav anytime)

---

## 5. Spacing System

### Spatial Scale

```css
--space-1: 0.25rem   /* 4px  - tight gaps */
--space-2: 0.5rem    /* 8px  - small gaps, icon spacing */
--space-3: 0.75rem   /* 12px - default component padding */
--space-4: 1rem      /* 16px - standard spacing */
--space-5: 1.25rem   /* 20px - list item spacing */
--space-6: 1.5rem    /* 24px - card padding, section spacing */
--space-8: 2rem      /* 32px - large section spacing */
--space-10: 2.5rem   /* 40px - page section dividers */
--space-12: 3rem     /* 48px - major section spacing */
--space-16: 4rem     /* 64px - page sections */
--space-20: 5rem     /* 80px - hero spacing */
```

### Spacing Guidelines

**Component Internal Spacing:**
- Buttons: 0.75rem vertical, 1.5rem horizontal
- Cards: 1.5rem all sides
- Tables: 1rem cell padding
- Form inputs: 0.75rem vertical, 1rem horizontal

**Layout Spacing:**
- Between sections: 3rem (mobile), 4rem (desktop)
- Between related elements: 1rem
- Between cards in grid: 1.5rem
- Page margin: 1rem (mobile), 2rem (desktop)

**Typography Spacing:**
- H1 margin-bottom: 1rem
- H2 margin-bottom: 1.25rem, margin-top: 3rem
- H3 margin-bottom: 0.75rem, margin-top: 1.5rem
- Paragraph margin-bottom: 1rem
- List item margin-bottom: 0.5rem

---

## 6. Interactive States & Animations

### Hover States

```css
/* Buttons */
button:hover {
  transform: translateY(-1px);
  transition: all 0.15s ease;
}

/* Cards */
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
}

/* Links */
a:hover {
  color: var(--brand-primary);
  transition: color 0.15s ease;
}

/* Table rows */
tr:hover {
  background: rgba(16, 185, 129, 0.05);
  transition: background 0.1s ease;
}
```

### Focus States

```css
/* All interactive elements */
:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}

/* Inputs */
input:focus, textarea:focus, select:focus {
  border-color: var(--brand-primary);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}
```

### Loading States

```css
/* Spinner */
.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(255, 255, 255, 0.2);
  border-top-color: var(--brand-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Skeleton screens */
.skeleton {
  background: linear-gradient(
    90deg,
    var(--surface-elevated) 0%,
    var(--surface-overlay) 50%,
    var(--surface-elevated) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
```

### Micro-interactions

```css
/* Accordion expand */
.accordion-content {
  overflow: hidden;
  transition: height 0.2s ease;
}

/* Tab switch */
.tab-panel {
  opacity: 0;
  animation: fadeIn 0.15s ease forwards;
}

@keyframes fadeIn {
  to { opacity: 1; }
}

/* Score badge pulse (on data update) */
.score-badge.updated {
  animation: pulse 0.5s ease;
}

@keyframes pulse {
  50% { transform: scale(1.05); }
}
```

---

## 7. Before/After Visual Scenarios

### Scenario 1: Homepage Hero

**BEFORE:**
```
Problem: Three competing CTAs at same visual weight
- "Explore the Map" (emerald)
- "Community Stories" (violet)
- "Learn About Methodology" (slate)

User confusion: Which should I click first?
```

**AFTER:**
```
Solution: Clear visual hierarchy
1. "Explore the Map" - Large emerald button (primary action)
   - 18px font, 16px vertical padding
   - Positioned center, isolated with whitespace

2. "Community Stories" - Separate section below with preview cards
   - Secondary importance established through position

3. "Learn About Methodology" - Text link in header nav
   - Accessible but not competing for attention

Result: User knows primary path is map exploration
```

### Scenario 2: About Page Dense Text

**BEFORE:**
```
Problem: 600 lines of continuous text
- User scrolls endlessly
- Can't find specific section
- Feels overwhelming
```

**AFTER:**
```
Solution: Accordion-based progressive disclosure

Collapsed view (initial load):
├─ [+] Data Sources
├─ [+] Health Burden Index
├─ [+] Statistical Model
├─ [+] Exclusion Criteria
├─ [-] Score Categories (expanded by default)
│   └─ [Color scale shown]
├─ [+] Limitations
├─ [+] Appropriate Uses
└─ [+] API Access

Benefits:
- See all sections at once (scannable)
- Expand only what you need
- Reduced cognitive load
- Faster navigation to relevant info
```

### Scenario 3: Back Navigation Inconsistency

**BEFORE:**
```
About page:
  <a> with arrow icon, gray text, no background

Stories page:
  <a> with arrow icon, different spacing, inline-flex

Map page:
  <button> 36px square, slate background, centered icon

Problem: Users don't recognize it as same pattern
```

**AFTER:**
```
Unified pattern (all pages):

┌────────────┐
│ ← Back    │  - 14px medium weight
└────────────┘  - 8px gap between icon and text
                - 12px horizontal padding, 8px vertical
                - Rounded 6px corners
                - Transparent background
                - Emerald tint on hover

Visual consistency = instant recognition
```

### Scenario 4: Story Cards Category System

**BEFORE:**
```
Problem: Violet only appears on homepage CTA
- No visual connection to "community" theme
- Category badges feel arbitrary
```

**AFTER:**
```
Solution: Semantic color system

HEALTH category:     Emerald (#10b981) - aligns with primary brand
FOOD ACCESS category: Amber (#f59e0b) - warm, approachable
COMMUNITY category:   Violet (#8b5cf6) - connects to homepage CTA
ECONOMIC category:    Blue (#3b82f6) - trust, stability

Each color has meaning:
- Violet on homepage "Community Stories" button
- Violet on story cards with "Community" category
- Visual thread connects homepage → stories page
```

### Scenario 5: Map Legend Contrast

**BEFORE:**
```
White legend on dark map:
- Text: slate-800 on white background
- Good contrast (12.6:1)
- But... choropleth colors hard to distinguish

Map colors:
- Very High: #059669
- High: #10b981
- Medium: #fbbf24
- Low: #f97316
- Very Low: #dc2626
```

**AFTER:**
```
No change needed - already accessible!

Verification:
- All text meets WCAG AA
- Color scale uses sufficient steps
- Not relying on color alone (legend has labels)

Recommendation: Add pattern overlays for colorblind users
(future enhancement)
```

---

## 8. Mobile Adaptations

### Touch Target Sizing

All interactive elements minimum 44x44px tap target:

```css
/* Mobile overrides */
@media (max-width: 640px) {
  .btn-icon {
    width: 44px;
    height: 44px;
  }

  .back-link {
    padding: 0.625rem 0.875rem; /* Ensures 44px height */
  }

  .nav-link {
    min-height: 44px;
    padding: 0.625rem 1rem;
  }
}
```

### Mobile Navigation

**Header collapse:**
```
Desktop:
[Logo] Community Resilience Mapping          [Map][Stories][About]

Mobile:
[☰] Community Resilience
                                    [Map][≡]

Expanded menu:
┌────────────────────────┐
│ [×] Menu              │
│                        │
│ → Explore Map         │
│ → Community Stories   │
│ → About              │
│ → API Docs           │
└────────────────────────┘
```

### Typography Scaling

```css
/* Mobile font size adjustments */
@media (max-width: 640px) {
  h1 { font-size: 2rem; }      /* 40px → 32px */
  h2 { font-size: 1.25rem; }   /* 24px → 20px */
  h3 { font-size: 1rem; }      /* 18px → 16px */

  .hero-title { font-size: 2.25rem; } /* 48px → 36px */

  body { font-size: 0.875rem; } /* 16px → 14px */
}
```

### Mobile Grid Adjustments

```css
/* Stack all grids on mobile */
@media (max-width: 640px) {
  .stat-grid,
  .story-grid,
  .use-grid {
    grid-template-columns: 1fr;
  }

  /* Exception: Stats can stay 2x2 */
  .stat-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }
}
```

---

## 9. Accessibility Checklist

### Color Contrast

- [ ] All text meets WCAG AA (4.5:1 body, 3:1 large text)
- [ ] Focus indicators meet 3:1 contrast against background
- [ ] Data visualizations not relying on color alone

### Keyboard Navigation

- [ ] All interactive elements focusable via Tab
- [ ] Skip link to main content (already implemented)
- [ ] Focus visible on all elements (outline: 2px solid --focus-ring)
- [ ] Modal/accordion keyboard controls (Escape to close, Arrow keys to navigate)

### Screen Readers

- [ ] Semantic HTML (header, nav, main, section, article)
- [ ] ARIA labels for icon-only buttons
- [ ] ARIA live regions for dynamic content (map updates, loading states)
- [ ] Alt text for decorative images (empty alt="")
- [ ] Descriptive link text (not "click here")

### Motion & Animation

- [ ] Respect `prefers-reduced-motion`

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 10. Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
**Priority: Critical visual hierarchy issues**

1. Implement design tokens (CSS custom properties)
   - Color system
   - Typography scale
   - Spacing system

2. Standardize navigation components
   - Unified back link pattern
   - Persistent header component
   - Breadcrumb component

3. Button system refinement
   - Consolidate to 4 variants (primary, secondary, accent, ghost)
   - Standardize sizing/padding
   - Update all instances

**Deliverables:**
- `design-tokens.css` file
- `Navigation.svelte` component
- `Button.svelte` component with variants

### Phase 2: Content Pages (Week 3)
**Priority: Improve About page scannability**

1. Implement accordion component
   - Methodology sections
   - API documentation
   - Limitations

2. Implement data card pattern
   - Visual section breaks
   - Colored left borders for scanning

3. Update About page layout
   - Add stat grid at top
   - Convert to accordion sections
   - Improve spacing/rhythm

**Deliverables:**
- `Accordion.svelte` component
- `DataCard.svelte` component
- Refactored `about/+page.svelte`

### Phase 3: Homepage Refinement (Week 4)
**Priority: Clear primary CTA, reduce competition**

1. Hero restructure
   - Single primary CTA (Explore Map)
   - Remove competing buttons

2. Story preview section
   - Show 4 cards
   - "View All Stories" link
   - Move violet branding here

3. Table improvements
   - Increase row padding
   - Better hover states
   - Improve score badge consistency

**Deliverables:**
- Refactored `+page.svelte` (homepage)
- `StoryPreview.svelte` component

### Phase 4: Polish & Mobile (Week 5)
**Priority: Responsive refinement**

1. Mobile navigation
   - Hamburger menu
   - Stacked layouts
   - Touch target sizing

2. Micro-interactions
   - Hover states
   - Focus states
   - Loading states

3. Accessibility audit
   - Keyboard navigation test
   - Screen reader test
   - Color contrast verification

**Deliverables:**
- Mobile-responsive CSS
- Accessibility audit report
- Animation/transition refinements

---

## 11. Success Metrics

### Quantitative Metrics

1. **Task Completion Rate**
   - Users can find methodology section: Target 95%
   - Users can navigate to map from any page: Target 100%

2. **Time to First Interaction**
   - Reduce time to click primary CTA by 30%

3. **Scroll Depth**
   - About page: Increase to 60% (from ~30% due to density)
   - Homepage: Maintain 80%+

4. **Accessibility Score**
   - Lighthouse Accessibility: 100/100
   - WAVE errors: 0
   - Keyboard navigation success: 100%

### Qualitative Metrics

1. **Visual Clarity**
   - 5-second test: "What is the primary action on this page?"
   - Target: 90% correctly identify "Explore Map"

2. **Navigation Confidence**
   - User interviews: "Did you always know where you were in the site?"
   - Target: 85% "yes" or "mostly yes"

3. **Information Findability**
   - Task: "Find the definition of resilience score categories"
   - Target: <30 seconds average time

---

## 12. Design System Maintenance

### Documentation

- Maintain living styleguide (Storybook or similar)
- Component usage examples
- Do's and Don'ts for each pattern

### Governance

- Design tokens as single source of truth
- PR reviews check for token usage (not hardcoded values)
- Quarterly design system review meeting

### Versioning

- Semantic versioning for major/minor/patch changes
- Changelog for each release
- Migration guides for breaking changes

---

## Appendix A: Current Color Audit

### Colors Found in Codebase

**Backgrounds:**
- `#0f172a` (slate-900) - base background
- `#1e293b` (slate-800) - elevated surfaces
- `#334155` (slate-700) - overlays, buttons
- `rgba(51, 65, 85, 0.5)` - transparent cards
- `rgba(30, 41, 59, 0.8)` - story cards

**Text:**
- `#ffffff` - white (headings)
- `#e2e8f0` (slate-200) - body text
- `#cbd5e1` (slate-300) - secondary text
- `#94a3b8` (slate-400) - muted text
- `#64748b` (slate-500) - disabled/tertiary

**Brand:**
- `#10b981` (emerald-500) - primary actions, positive data
- `#059669` (emerald-600) - hover states, very-high scores
- `#34d399` (emerald-400) - highlights, high scores
- `#8b5cf6` (violet-500) - community accent
- `#7c3aed` (violet-600) - violet hover

**Data Visualization:**
- `#059669` - very high (≥2.0)
- `#10b981` - high (1.0-2.0)
- `#fbbf24` (amber-400) - medium (0-1.0)
- `#f97316` (orange-500) - low (-1.0-0)
- `#dc2626` (red-600) - very low (<-1.0)
- `#9ca3af` (gray-400) - no data

**Borders:**
- `#334155` (slate-700) - subtle borders
- `#475569` (slate-600) - moderate borders

### Consolidation Recommendations

**Keep:**
- All slate scale (good neutral system)
- Emerald scale (brand)
- Data viz colors (scientifically chosen for distinction)

**Add:**
- Violet scale (currently only 2 values)
- Amber accent (for food category)
- Blue accent (for economic category)

**Remove:**
- Random one-off colors
- Hardcoded rgba values (use CSS custom properties instead)

---

## Appendix B: Typography Audit

### Current Font Sizes Found

**Headings:**
- 60px (3.75rem) - homepage title (TOO LARGE)
- 48px (3rem) - unused
- 40px (2.5rem) - about page H1
- 36px (2.25rem) - unused
- 32px (2rem) - unused
- 24px (1.5rem) - H2
- 20px (1.25rem) - story card titles
- 18px (1.125rem) - H3, lead text

**Body:**
- 16px (1rem) - standard body
- 14px (0.875rem) - small text, captions
- 13px (0.8125rem) - category labels, legends
- 12px (0.75rem) - labels, badges
- 11px (0.6875rem) - legend notes (TOO SMALL)

**Stats:**
- 56px (3.5rem) - homepage stat values (TOO LARGE)
- 28px (1.75rem) - about page stat values

### Consolidation Recommendations

**Reduce scale to 8 sizes:**
1. Display: 48px (hero only)
2. H1: 40px
3. H2: 24px
4. H3: 18px
5. H4: 16px
6. Body: 16px
7. Small: 14px
8. Caption: 13px

**Eliminate:**
- 60px display (too large)
- 56px stats (reduce to 40px)
- 11px text (increase to 13px minimum for accessibility)

---

## Appendix C: Component Inventory

### Existing Components (to be standardized)

1. **Buttons**
   - Primary (emerald)
   - Secondary (slate)
   - Accent (violet)
   - Icon buttons
   - Back links (3 different implementations!)

2. **Cards**
   - Stat cards
   - Story cards
   - Data cards (need)

3. **Tables**
   - Data table (homepage)

4. **Navigation**
   - Back links
   - Footer nav
   - Header (map page only)

5. **Map Components**
   - Legend
   - Search
   - Hover tooltip
   - Info panel

6. **Forms**
   - Search input (address search)

### Missing Components (to be created)

1. **Navigation**
   - Persistent header
   - Breadcrumbs
   - Mobile menu

2. **Progressive Disclosure**
   - Accordion
   - Tabs
   - Details/summary

3. **Feedback**
   - Toast notifications
   - Error states
   - Loading states (spinner exists, need skeleton screens)

4. **Data Display**
   - Score scale visual
   - Category legend
   - Stat comparison

---

## Conclusion

This design system proposal addresses the core visual hierarchy and consistency issues in the Community Resilience Mapping application. By implementing:

1. **Clear typography hierarchy** - Users can scan and understand content structure
2. **Semantic color system** - Colors have meaning and guide action
3. **Consistent components** - Patterns are recognizable across pages
4. **Progressive disclosure** - Dense content becomes manageable
5. **Unified navigation** - Users always know where they are

The application will transform from a data-dense academic tool into an accessible, scannable, and confidence-inspiring public resource.

The phased implementation roadmap prioritizes critical visual hierarchy issues first, then progressively refines the experience with mobile optimization and polish. Success metrics ensure improvements are measurable and aligned with user needs.

---

**Next Steps:**

1. Review this proposal with stakeholders
2. Prioritize Phase 1 foundation work
3. Create component library in Storybook (optional but recommended)
4. Begin implementation following roadmap

**Questions for Discussion:**

1. Should accordions be open or closed by default on About page?
2. Do we need a formal design review process for new components?
3. What analytics can we add to measure navigation patterns?
4. Should we conduct user testing before/after Phase 2?
