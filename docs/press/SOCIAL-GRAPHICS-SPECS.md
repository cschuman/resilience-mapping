# Social Graphics & Open Graph Image Specifications

This document provides specifications for social media graphics and Open Graph images for the Community Resilience Mapping Project.

---

## General Specifications

### Dimensions

| Platform | Size | Aspect Ratio | Use Case |
|----------|------|--------------|----------|
| Open Graph (Twitter/LinkedIn) | 1200×630px | 1.91:1 | Link previews |
| Twitter Card | 1200×628px | 1.91:1 | Tweet embeds |
| Instagram/Facebook Square | 1080×1080px | 1:1 | Feed posts |
| Instagram Story | 1080×1920px | 9:16 | Stories |
| LinkedIn Article | 1200×627px | 1.91:1 | Article headers |

### Brand Colors

```css
/* Primary palette */
--color-positive: #22c55e;     /* Green - good outcomes */
--color-negative: #ef4444;     /* Red - poor outcomes */
--color-neutral: #6b7280;      /* Gray - neutral */
--color-accent: #3b82f6;       /* Blue - accent */
--color-background: #0f172a;   /* Dark navy - background */
--color-surface: #1e293b;      /* Slate - cards */
--color-text: #f8fafc;         /* White - text */
```

### Typography

- **Headlines:** Inter Bold, 48-72px
- **Subheadlines:** Inter SemiBold, 24-36px
- **Body:** Inter Regular, 18-24px
- **Data values:** JetBrains Mono Bold, 72-120px
- **Labels:** Inter Medium, 14-18px

---

## Finding #1: College vs Prison (4 SD Gap)

### Open Graph Image (1200×630)

**Layout:** Split comparison

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ┌─────────────────────┐    ┌─────────────────────┐        │
│  │                     │    │                     │        │
│  │      +2.95          │    │      -0.98          │        │
│  │   (large, green)    │    │    (large, red)     │        │
│  │                     │    │                     │        │
│  │   College Towns     │    │   Prison Towns      │        │
│  └─────────────────────┘    └─────────────────────┘        │
│                                                             │
│           "4 Standard Deviations Apart"                     │
│                                                             │
│                    odds.health                              │
└─────────────────────────────────────────────────────────────┘
```

**Text:**
- Headline: "College vs Prison: A 4 SD Health Divide"
- Left card: "+2.95" in green, "College Towns" below
- Right card: "-0.98" in red, "Prison Towns" below
- Subhead: "Same country. Same healthcare system. 4 standard deviations apart."
- Footer: odds.health logo

**Alt text:** "Comparison showing college towns at +2.95 resilience versus prison towns at -0.98, a 4 standard deviation gap"

### Twitter Thread Graphics (1080×1080 each)

**Card 1 - Hook:**
- Large text: "4 SD"
- Subtext: "The health gap between college and prison towns"

**Card 2 - College:**
- "+2.95" in green
- "College Towns"
- "Among the healthiest communities in America"

**Card 3 - Prison:**
- "-0.98" in red
- "Prison Towns"
- "Among the least healthy communities in America"

**Card 4 - CTA:**
- "Explore the data"
- odds.health/research/special-populations

---

## Finding #2: Hispanic Paradox

### Open Graph Image (1200×630)

**Layout:** Data reveal

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│     The "Hispanic Paradox" Is an Aggregation Artifact       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  South American    ████████████████  +0.147         │   │
│  │  Central American  ████████          +0.060         │   │
│  │  Cuban             ██                -0.030         │   │
│  │  Mexican           ██                -0.029         │   │
│  │  Puerto Rican      ███               -0.017         │   │
│  │  ─────────────────────────────────────────────      │   │
│  │  Aggregate         │                 +0.006         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│                    odds.health                              │
└─────────────────────────────────────────────────────────────┘
```

**Text:**
- Headline: "The 'Hispanic Paradox' Is an Aggregation Artifact"
- Horizontal bar chart showing origin group correlations
- Highlight: The aggregate (+0.006) obscures the heterogeneity
- Footer: odds.health logo

**Alt text:** "Bar chart showing Hispanic origin group correlations with resilience ranging from +0.147 (South American) to -0.030 (Cuban), with aggregate at near-zero +0.006"

### Texas Comparison Graphic (1080×1080)

**Layout:** Map with callouts

```
┌─────────────────────────────────────────┐
│                                         │
│         Same State. 2.6 SD Apart.       │
│                                         │
│     ┌───────────────────────────┐       │
│     │                           │       │
│     │    [Texas Map Outline]    │       │
│     │                           │       │
│     │   Austin ●───────● Border │       │
│     │   +1.53          -1.08    │       │
│     │                           │       │
│     └───────────────────────────┘       │
│                                         │
│    Mexican-majority communities         │
│    Radically different outcomes         │
│                                         │
│              odds.health                │
└─────────────────────────────────────────┘
```

---

## Finding #3: Ohio Bifurcation

### Open Graph Image (1200×630)

**Layout:** Geographic comparison

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              Ohio's Health Divide                           │
│                                                             │
│  ┌─────────────────────┐    ┌─────────────────────┐        │
│  │     COLUMBUS        │    │     CLEVELAND       │        │
│  │                     │    │                     │        │
│  │   4 of top 10       │    │   3 of bottom 10    │        │
│  │   nationally        │    │   nationally        │        │
│  │     (green)         │    │      (red)          │        │
│  └─────────────────────┘    └─────────────────────┘        │
│                                                             │
│           140 miles apart. 10+ SD difference.               │
│                                                             │
│                    odds.health                              │
└─────────────────────────────────────────────────────────────┘
```

**Text:**
- Headline: "Ohio's Health Divide"
- Left: "COLUMBUS - 4 of top 10 nationally"
- Right: "CLEVELAND - 3 of bottom 10 nationally"
- Subhead: "Same state. 140 miles apart. 10+ standard deviations."

**Alt text:** "Comparison showing Columbus with 4 of top 10 healthiest tracts nationally versus Cleveland with 3 of bottom 10, same state, 140 miles apart"

---

## Page-Specific OG Images

### Homepage (odds.health)

**File:** `/static/og-home.png`

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                      odds.health                            │
│                                                             │
│         Where You Live Explains 28% of Your Health          │
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                     │
│  │ 54,560  │  │   51    │  │  220M+  │                     │
│  │ Tracts  │  │ States  │  │ People  │                     │
│  └─────────┘  └─────────┘  └─────────┘                     │
│                                                             │
│         Community Health Resilience Mapping                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Research Page (odds.health/research)

**File:** `/static/og-research.png`

- Feature the 4 SD gap prominently
- Include "5 Research Papers" badge
- Show key finding numbers

### Paper-Specific OG Images

Each paper should have its own OG image:

| Paper | OG Image | Key Visual |
|-------|----------|------------|
| Immigrant Health Advantage | `/static/og-paper-immigrant.png` | Origin group forest plot |
| Health Equity | `/static/og-paper-equity.png` | State variation bar chart |
| Special Populations | `/static/og-paper-populations.png` | College vs Prison comparison |
| Spatial Synchrony | `/static/og-paper-spatial.png` | Abstract network graphic |

---

## Implementation Checklist

### Phase 1: Critical (Immediate)

- [ ] Homepage OG image (`/static/og-home.png`)
- [ ] College vs Prison OG image (`/static/og-college-prison.png`)
- [ ] Update `<meta property="og:image">` tags in relevant pages

### Phase 2: Paper Pages

- [ ] Immigrant Health Advantage OG image
- [ ] Health Equity OG image
- [ ] Special Populations OG image

### Phase 3: Social Campaign

- [ ] Twitter thread graphics for College vs Prison
- [ ] Twitter thread graphics for Hispanic Paradox
- [ ] LinkedIn article headers
- [ ] Instagram story templates

---

## File Naming Convention

```
/static/og-[page].png           # Page-level OG images
/static/social/[finding]-[n].png # Social thread graphics
/static/social/story-[finding].png # Instagram stories
```

---

## Accessibility Requirements

All graphics must include:
- High contrast text (WCAG AA minimum)
- Alt text in HTML implementation
- No text smaller than 14px equivalent
- Color not as sole indicator (use labels)

---

*Specifications prepared for design handoff*
*Last updated: January 2025*
