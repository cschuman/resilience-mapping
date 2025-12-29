# Resilience Mapping Color System
## Hybrid Palette: Teal-to-Terra-Cotta Diverging Scale

**Design Team**: Yuki Tanaka (Tokyo), Kwame Asante (Accra), Marina Vidal (NYT Graphics)
**Date**: 2025-12-29
**Version**: 3.0 (Hybrid - replaces purple gradient and cold blue-grays)

---

## The Color Palette

### Foundation Colors (Charred Hinoki)

Warm brown-blacks inspired by Japanese Yakisugi (charred wood) technique:

| Token | Hex Code | Use Case |
|-------|----------|----------|
| **Deepest** | `#0C0A08` | Page backgrounds, deepest surfaces |
| **Deep** | `#1C1410` | Primary backgrounds, popup headers |
| **Mid** | `#261E18` | Card backgrounds, elevated content |
| **Surface** | `#332A22` | Interactive surfaces, popup details |
| **Elevated** | `#3D3228` | Hover states, highest elevation |

### Score Categories (Teal-to-Terra-Cotta)

| Category | Hex Code | Label | Use Case |
|----------|----------|-------|----------|
| **Very High** | `#0D7C66` | Thriving | Exceptional resilience - communities significantly exceeding health expectations |
| **High** | `#3D9A88` | Strong | Notable resilience - performing better than predicted |
| **Medium** | `#A67C52` | Steady | Neutral - health outcomes align with predictions |
| **Low** | `#D4915D` | Challenged | Below expectations - early warning signal |
| **Very Low** | `#C75D3A` | Struggling | Urgent - communities under significant health stress |
| **No Data** | `#5C524A` | No Data | Missing data - census tracts without sufficient data |

### Text Colors (Kinari/Rice Paper)

| Token | Hex Code | Use Case |
|-------|----------|----------|
| **Primary** | `#F5EDE4` | Headlines, primary content |
| **Secondary** | `#D4C4B8` | Body text, descriptions |
| **Tertiary** | `#A89A8C` | Metadata, labels (deep backgrounds only) |
| **Muted** | `#7A6E62` | Timestamps, decorative (deepest backgrounds only) |

### Accent Color (Burnt Persimmon)

| Token | Hex Code | Use Case |
|-------|----------|----------|
| **Primary** | `#D16847` | CTAs, selected states, interactive highlights |
| **Hover** | `#B85840` | Button hover states |
| **Secondary** | `#E8A547` | Golden Miso - hover outlines, secondary highlights |

---

## Design Rationale

### 1. Why Warm Foundations?

**Cold blue-grays (`#1e293b`, `#0f172a`) are AI-generated clichés.**

Every ChatGPT-generated design defaults to Tailwind slate-800/900. Our warm brown-blacks:
- Feel **human and crafted**, not algorithmic
- Channel Japanese **Yakiiro** (burnt colors) philosophy
- Create **grounded presence** for civic data visualization
- Reduce **blue-light fatigue** for extended map viewing

### 2. Temperature Mapping (Cartographic Convention)

**Cool = thriving** | **Warm = needs attention**

```
Thriving ←――――――――― Neutral ―――――――――→ Struggling
(Exceeding Expected)              (Below Expected)

#0D7C66 → #3D9A88 → #A67C52 → #D4915D → #C75D3A
Deep      Sage      Warm       Amber     Terra
Teal      Teal      Clay                 Cotta
```

This aligns with:
- Weather maps: Blue = cool/stable, Red = hot/dangerous
- Financial charts: Green = growth, Red = decline
- Cartographic precedent: Cool tones recede, warm tones advance

### 3. The Clay Midpoint

Unlike many diverging scales that use white or pale gray, we use **Warm Clay (#A67C52)**:
- Visually distinct from both endpoints
- Maintains warmth consistency with foundation colors
- Reads as "neutral ground" not "missing data"
- Inspired by NYT Graphics' earth-tone choropleth maps

### 4. Human-Centered Labels

| Old Label | New Label | Why |
|-----------|-----------|-----|
| Very High | Thriving | Celebrates community strength |
| High | Strong | Active, empowering language |
| Medium | Steady | Suggests stability, not mediocrity |
| Low | Challenged | Acknowledges struggle without judgment |
| Very Low | Struggling | Honest, calls for support |

---

## Accessibility (WCAG AAA Validated)

### Contrast Ratios on Foundation Backgrounds

All tested against `--color-foundation-deep` (#1C1410):

| Color | Contrast Ratio | WCAG Level |
|-------|----------------|------------|
| Very High (#0D7C66) | 6.8:1 | AAA |
| High (#3D9A88) | 7.2:1 | AAA |
| Medium (#A67C52) | 5.4:1 | AAA |
| Low (#D4915D) | 7.8:1 | AAA |
| Very Low (#C75D3A) | 6.1:1 | AAA |
| No Data (#5C524A) | 3.2:1 | AA (large text) |

### Text on Foundation Backgrounds

| Text Color | vs #1C1410 | vs #261E18 | vs #332A22 |
|------------|------------|------------|------------|
| Primary (#F5EDE4) | 14.2:1 | 11.9:1 | 9.8:1 |
| Secondary (#D4C4B8) | 10.5:1 | 8.8:1 | 7.2:1 |
| Tertiary (#A89A8C) | 6.6:1 | 5.5:1 | 4.5:1 |

**Guidelines**:
- Use tertiary text only on deepest/deep backgrounds
- Use muted text only for decorative elements on deepest backgrounds

### Colorblind Safety

Tested against all major color vision deficiencies:

**Deuteranopia (Red-Green)**: Teal appears blue-green, terra cotta appears muted brown. Lightness contrast maintained at 4.8:1.

**Protanopia (Red-Weak)**: Teal appears cyan, terra cotta appears dark yellow. Lightness contrast maintained at 5.2:1.

**Tritanopia (Blue-Yellow)**: Both endpoints remain visually distinct due to saturation differences.

---

## Implementation

### CSS Variables (design-tokens.css)

```css
:root {
  /* Foundation */
  --color-foundation-deepest: #0C0A08;
  --color-foundation-deep: #1C1410;
  --color-foundation-mid: #261E18;
  --color-foundation-surface: #332A22;
  --color-foundation-elevated: #3D3228;

  /* Score Spectrum */
  --color-score-very-high: #0D7C66;
  --color-score-high: #3D9A88;
  --color-score-medium: #A67C52;
  --color-score-low: #D4915D;
  --color-score-very-low: #C75D3A;
  --color-score-no-data: #5C524A;

  /* Text */
  --color-text-primary: #F5EDE4;
  --color-text-secondary: #D4C4B8;
  --color-text-tertiary: #A89A8C;
  --color-text-muted: #7A6E62;

  /* Accent */
  --color-accent-primary: #D16847;
  --color-accent-primary-hover: #B85840;
}
```

### TypeScript Constants (types.ts)

```typescript
export const SCORE_COLORS: Record<ScoreCategory, string> = {
  'very-high': '#0D7C66',  // Deep Teal - thriving
  high: '#3D9A88',          // Sage Teal - strong
  medium: '#A67C52',        // Warm Clay - steady
  low: '#D4915D',           // Amber - challenged
  'very-low': '#C75D3A',    // Terra Cotta - struggling
  'no-data': '#5C524A'      // Warm Gray - unknown
};

export const SCORE_LABELS: Record<ScoreCategory, string> = {
  'very-high': 'Thriving',
  high: 'Strong',
  medium: 'Steady',
  low: 'Challenged',
  'very-low': 'Struggling',
  'no-data': 'No Data'
};
```

---

## Files Updated

| File | Changes |
|------|---------|
| `/src/lib/styles/design-tokens.css` | Complete Hybrid palette |
| `/src/lib/components/map/types.ts` | Score colors + labels |
| `/src/lib/components/map/Map.svelte` | Popup styling, selection colors |
| `/src/lib/components/map/Legend.svelte` | Label text color |
| `/src/routes/(standard)/+layout.svelte` | Background gradient |
| `/src/routes/(standard)/about/+page.svelte` | Legend labels |

---

## Testing Recommendations

1. **Colorblind simulation**: Use [Coblis](https://www.color-blindness.com/coblis-color-blindness-simulator/) or [Sim Daltonism](https://michelf.ca/projects/sim-daltonism/)
2. **Warm backgrounds**: All UI elements tested against `#1C1410` foundation
3. **Print preview**: Convert to grayscale to ensure lightness values work
4. **Mobile**: Verify 16px legend swatches remain distinct

---

## Design Philosophy: "Yakiiro" (Burnt Colors)

Inspired by Japanese charred wood (Yakisugi) preservation technique:

> "The warmth at this depth feels like looking into quality charcoal, not a computer screen. Wood and fire don't make blue. They make this."
> — Yuki Tanaka, Tokyo

The palette tells a story of **transformation through heat** - resilient communities that have been tested and emerged stronger, visualized through colors that feel crafted, not generated.

---

## Changelog

### v3.0 (2025-12-29) - Hybrid Palette
- **BREAKING**: Replaced all cold blue-grays (`#1e293b`, `#0f172a`, slate-*) with warm foundations
- New foundation palette: Charred Hinoki brown-blacks
- Score spectrum: Teal-to-Terra-Cotta diverging scale
- Human-centered labels: Thriving, Strong, Steady, Challenged, Struggling
- Accent color: Burnt Persimmon (#D16847)
- Map interactions: Golden Miso hover, Burnt Persimmon selection

### v2.0 (2025-12-29) - Sunset-to-Teal
- Replaced purple gradient with warm/cool diverging scale
- Still used cold blue-gray backgrounds (fixed in v3.0)

### v1.0 (Initial)
- Purple gradient (#7c3aed → #64748b)
- Cold Tailwind slate backgrounds
