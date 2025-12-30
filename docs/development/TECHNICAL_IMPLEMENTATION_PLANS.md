# Technical Implementation Plans
## Post-Workshop Technical Specifications
### December 30, 2025

---

## Table of Contents
1. [Data Quality Sprint](#1-data-quality-sprint)
2. [Accessible Data Table](#2-accessible-data-table)
3. [Performance Optimization](#3-performance-optimization)
4. [Infrastructure Safety](#4-infrastructure-safety)
5. [Design System Foundation](#5-design-system-foundation)

---

## 1. Data Quality Sprint

### Owner: Miguel Santos
### Timeline: Dec 30 - Jan 13

### 1.1 Institutional Population Filter

**Problem**: Census tracts with high institutional populations (prisons, college dorms, military barracks) contaminate health outcome analysis. Currently, Tract 47149041500 (98.8% prison) is ranked #1 for resilience.

**Solution**: Filter tracts where institutional population exceeds 10% of total.

**Data Source**: ACS Table B26001 (Group Quarters Population by Group Quarters Type)

**Implementation**:

```python
# app/analytics/filters/institutional.py

import pandas as pd
from typing import Tuple

# ACS B26001 columns
GQ_COLUMNS = {
    'B26001_001E': 'total_gq',           # Total group quarters population
    'B26001_002E': 'institutionalized',   # Institutionalized population
    'B26001_003E': 'correctional',        # Correctional facilities
    'B26001_004E': 'juvenile',            # Juvenile facilities
    'B26001_005E': 'nursing',             # Nursing facilities
    'B26001_006E': 'other_institutional', # Other institutional
}

def calculate_institutional_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate institutional population ratio for each tract.

    Args:
        df: DataFrame with ACS group quarters data

    Returns:
        DataFrame with institutional_ratio column added
    """
    df['institutional_ratio'] = (
        df['institutionalized'] / df['total_population']
    ).fillna(0)

    return df

def filter_institutional_tracts(
    df: pd.DataFrame,
    threshold: float = 0.10
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Filter out tracts with high institutional populations.

    Args:
        df: DataFrame with tract data including institutional_ratio
        threshold: Maximum allowed institutional ratio (default 10%)

    Returns:
        Tuple of (filtered_df, excluded_df)
    """
    mask = df['institutional_ratio'] <= threshold

    filtered = df[mask].copy()
    excluded = df[~mask].copy()

    print(f"Filtered {len(excluded)} tracts with institutional ratio > {threshold:.0%}")
    print(f"Remaining: {len(filtered)} tracts")

    return filtered, excluded

def document_exclusions(excluded: pd.DataFrame, output_path: str) -> None:
    """
    Document all excluded tracts for transparency.
    """
    report = excluded[[
        'tract_fips', 'state_abbr', 'county_name',
        'total_population', 'institutionalized', 'institutional_ratio',
        'original_resilience_score'
    ]].sort_values('institutional_ratio', ascending=False)

    report.to_csv(output_path, index=False)
    print(f"Exclusion report saved to {output_path}")
```

**Database Migration**:

```sql
-- migrations/003_add_institutional_filter.sql

-- Add institutional columns
ALTER TABLE tracts ADD COLUMN IF NOT EXISTS
    institutional_population INTEGER DEFAULT 0;
ALTER TABLE tracts ADD COLUMN IF NOT EXISTS
    institutional_ratio DECIMAL(5,4) DEFAULT 0;
ALTER TABLE tracts ADD COLUMN IF NOT EXISTS
    excluded_institutional BOOLEAN DEFAULT FALSE;

-- Create index for filtering
CREATE INDEX CONCURRENTLY idx_tracts_institutional
    ON tracts(excluded_institutional)
    WHERE excluded_institutional = FALSE;

-- Update API views to exclude
CREATE OR REPLACE VIEW public_tracts AS
SELECT * FROM tracts
WHERE excluded_institutional = FALSE;
```

**Validation Checklist**:
- [ ] Download ACS B26001 for all tracts
- [ ] Join with existing tract data
- [ ] Calculate ratios
- [ ] Apply 10% threshold
- [ ] Document all exclusions
- [ ] Re-run regression
- [ ] Compare old vs new top 100
- [ ] Manual review of new top 20
- [ ] Update production database

---

### 1.2 State Fixed Effects Verification

**Problem**: Previously identified bug in `expected.go` where inner loop variable shadowed outer loop, causing incorrect state-level adjustments.

**Fix Applied**: December 24, 2025 - renamed `i` to `si` in inner loop

**Verification Steps**:

```python
# app/analytics/verification/state_effects.py

def verify_state_fixed_effects(df: pd.DataFrame) -> bool:
    """
    Verify state fixed effects are correctly applied.

    For each state, the mean residual should be approximately 0
    (within-state variation only).
    """
    state_means = df.groupby('state_abbr')['residual'].mean()

    # All state means should be close to 0 (within tolerance)
    tolerance = 0.01
    violations = state_means[abs(state_means) > tolerance]

    if len(violations) > 0:
        print("WARNING: State fixed effects may not be correctly applied:")
        print(violations)
        return False

    print("State fixed effects verified: all state means within tolerance")
    return True
```

---

## 2. Accessible Data Table

### Owner: David Chen-Williams + Jordan Park + Yuki Nakamura-Jackson
### Timeline: Jan 13 - Jan 27

### 2.1 Architecture Decision

**Decision**: Table-first, map-second

The data table is the PRIMARY interface. Map is progressive enhancement.

**Rationale** (David):
> "I can't experience your map. But I can navigate a well-structured table. When you design for screen readers first, everyone benefits."

### 2.2 Component Specification

```typescript
// src/lib/components/data/TractTable.svelte

/*
 * TractTable - Accessible data table for 68,000+ census tracts
 *
 * Accessibility Requirements:
 * - Full keyboard navigation (Tab, Arrow keys, Enter, Escape)
 * - Screen reader announcements for all interactions
 * - Sort state announced on column headers
 * - Row selection announced
 * - Pagination controls accessible
 * - Column visibility controls accessible
 *
 * Performance Requirements:
 * - Virtual scrolling for 68K rows
 * - Server-side pagination
 * - Debounced search
 * - <100ms interaction response
 */

interface TractTableProps {
  // Data
  initialData?: Tract[];

  // Pagination
  pageSize?: number;        // Default: 25
  serverPagination?: boolean; // Default: true

  // Accessibility
  caption: string;          // Required for screen readers
  ariaLabel?: string;
  announceChanges?: boolean; // Default: true

  // Features
  sortable?: boolean;       // Default: true
  searchable?: boolean;     // Default: true
  selectable?: boolean;     // Default: true
  exportable?: boolean;     // Default: true
}

interface TractTableColumn {
  id: string;
  header: string;
  accessibleHeader?: string; // Longer description for SR
  sortable?: boolean;
  width?: string;
  align?: 'left' | 'center' | 'right';
  format?: (value: any) => string;
}
```

### 2.3 Keyboard Navigation Spec

```typescript
// Keyboard shortcuts following WAI-ARIA Grid Pattern

const KEYBOARD_BINDINGS = {
  // Navigation
  'ArrowDown': 'Move to next row',
  'ArrowUp': 'Move to previous row',
  'ArrowRight': 'Move to next cell',
  'ArrowLeft': 'Move to previous cell',
  'Home': 'Move to first cell in row',
  'End': 'Move to last cell in row',
  'Ctrl+Home': 'Move to first cell in table',
  'Ctrl+End': 'Move to last cell in table',
  'PageDown': 'Move down one page',
  'PageUp': 'Move up one page',

  // Actions
  'Enter': 'Select/activate current row',
  'Space': 'Toggle row selection',
  'Escape': 'Clear selection / exit focus',

  // Sorting
  'Ctrl+ArrowUp': 'Sort column ascending',
  'Ctrl+ArrowDown': 'Sort column descending',

  // Search
  '/': 'Focus search input',
  'Ctrl+F': 'Focus search input',
};
```

### 2.4 Screen Reader Announcements

```typescript
// src/lib/utils/announcements.ts

export function announceTableSort(column: string, direction: 'asc' | 'desc') {
  announce(`Table sorted by ${column}, ${direction === 'asc' ? 'ascending' : 'descending'}`);
}

export function announceRowSelection(tractId: string, county: string, state: string) {
  announce(`Selected tract ${tractId} in ${county}, ${state}`);
}

export function announceSearchResults(count: number, query: string) {
  announce(`${count} results found for "${query}"`);
}

export function announcePageChange(page: number, total: number) {
  announce(`Page ${page} of ${total}`);
}

export function announceSortableColumn(column: string, currentSort?: 'asc' | 'desc') {
  const sortState = currentSort
    ? `Currently sorted ${currentSort === 'asc' ? 'ascending' : 'descending'}`
    : 'Not sorted';
  announce(`${column}, sortable column. ${sortState}. Press Enter to sort.`);
}

function announce(message: string, priority: 'polite' | 'assertive' = 'polite') {
  const region = document.getElementById('aria-live-region');
  if (region) {
    region.setAttribute('aria-live', priority);
    region.textContent = message;
  }
}
```

### 2.5 Virtual Scrolling Implementation

```typescript
// Using TanStack Virtual for 68K row performance

import { createVirtualizer } from '@tanstack/svelte-virtual';

// In component
const virtualizer = createVirtualizer({
  count: $filteredData.length,
  getScrollElement: () => tableContainer,
  estimateSize: () => 48, // Row height in pixels
  overscan: 10, // Extra rows to render
});

// Only render visible rows + overscan
$: visibleRows = $virtualizer.getVirtualItems();
```

### 2.6 Server-Side Pagination API

```typescript
// src/routes/api/tracts/+server.ts

import { z } from 'zod';

const PaginationSchema = z.object({
  page: z.coerce.number().min(1).default(1),
  pageSize: z.coerce.number().min(10).max(100).default(25),
  sortBy: z.string().optional(),
  sortOrder: z.enum(['asc', 'desc']).default('desc'),
  search: z.string().optional(),
  state: z.string().length(2).optional(),
  minScore: z.coerce.number().optional(),
  maxScore: z.coerce.number().optional(),
});

export async function GET({ url }) {
  const params = PaginationSchema.parse(Object.fromEntries(url.searchParams));

  const { data, total, page, pageSize } = await queryTracts(params);

  return json({
    data,
    pagination: {
      page,
      pageSize,
      total,
      totalPages: Math.ceil(total / pageSize),
    },
  });
}
```

---

## 3. Performance Optimization

### Owner: Jordan Park
### Timeline: Jan 13 - Jan 27

### 3.1 Bundle Analysis

**Current State** (December 30, 2025):
```
Total: ~2.3MB uncompressed
├── maplibre-gl: 1.4MB (60%)
├── pmtiles: 180KB (8%)
├── d3 (unused portions): 300KB (13%)
├── zod: 50KB (2%)
└── app code: 370KB (17%)
```

**Target State**:
```
Initial Load: <200KB
├── core app: 100KB
├── critical CSS: 20KB
└── minimal JS: 80KB

Lazy Loaded (on /map route):
├── maplibre-gl: 400KB (tree-shaken)
├── pmtiles: 50KB
└── map components: 50KB
```

### 3.2 Code Splitting Strategy

```typescript
// vite.config.ts

export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Core - always loaded
          'vendor-core': ['svelte', '@sveltejs/kit'],

          // Map - lazy loaded on /map route
          'vendor-map': ['maplibre-gl', 'pmtiles'],

          // Data viz - lazy loaded
          'vendor-charts': ['d3-scale', 'd3-array'],

          // Validation - only on forms
          'vendor-validation': ['zod'],
        },
      },
    },
  },
});
```

### 3.3 Progressive Map Loading

```svelte
<!-- src/lib/components/map/ProgressiveMap.svelte -->

<script lang="ts">
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';

  let stage: 'skeleton' | 'outline' | 'states' | 'tracts' = 'skeleton';
  let MapComponent: any;

  onMount(async () => {
    // Stage 1: Show skeleton immediately
    stage = 'skeleton';

    // Stage 2: Load US outline (tiny GeoJSON)
    const outline = await fetch('/data/us-outline.json');
    stage = 'outline';

    // Stage 3: Lazy load full map library
    const { default: Map } = await import('./Map.svelte');
    MapComponent = Map;
    stage = 'states';

    // Stage 4: Load tract details on zoom
    // (handled within Map component)
  });
</script>

{#if stage === 'skeleton'}
  <div class="map-skeleton" aria-label="Loading map...">
    <div class="skeleton-pulse"></div>
  </div>
{:else if stage === 'outline'}
  <svg class="us-outline" aria-label="United States outline">
    <!-- Simple SVG outline -->
  </svg>
{:else if MapComponent}
  <svelte:component this={MapComponent} />
{/if}

<style>
  .map-skeleton {
    background: var(--color-surface-secondary);
    aspect-ratio: 16/9;
    border-radius: var(--radius-lg);
  }

  .skeleton-pulse {
    animation: pulse 1.5s ease-in-out infinite;
  }
</style>
```

### 3.4 Service Worker Strategy

```typescript
// src/service-worker.ts

import { build, files, version } from '$service-worker';

const CACHE_NAME = `resilience-map-${version}`;

// Assets to cache immediately
const PRECACHE = [
  '/',
  '/data',
  '/about',
  '/offline',
];

// Cache strategies
const STRATEGIES = {
  // Static assets: Cache first, network fallback
  static: /\.(js|css|woff2|png|svg)$/,

  // API responses: Network first, cache fallback
  api: /\/api\//,

  // Tiles: Cache with expiration
  tiles: /\.pmtiles$/,
};

self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  if (STRATEGIES.static.test(url.pathname)) {
    event.respondWith(cacheFirst(request));
  } else if (STRATEGIES.api.test(url.pathname)) {
    event.respondWith(networkFirst(request));
  } else if (STRATEGIES.tiles.test(url.pathname)) {
    event.respondWith(cacheWithExpiration(request, 24 * 60 * 60)); // 24 hours
  }
});

async function cacheFirst(request: Request): Promise<Response> {
  const cached = await caches.match(request);
  if (cached) return cached;

  const response = await fetch(request);
  const cache = await caches.open(CACHE_NAME);
  cache.put(request, response.clone());
  return response;
}

async function networkFirst(request: Request): Promise<Response> {
  try {
    const response = await fetch(request);
    const cache = await caches.open(CACHE_NAME);
    cache.put(request, response.clone());
    return response;
  } catch {
    const cached = await caches.match(request);
    if (cached) return cached;
    return new Response('Offline', { status: 503 });
  }
}
```

### 3.5 Performance Budget CI

```yaml
# .github/workflows/lighthouse.yml

name: Lighthouse CI

on: [push, pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 22

      - name: Install and Build
        run: |
          cd app/web
          npm ci
          npm run build

      - name: Run Lighthouse
        uses: treosh/lighthouse-ci-action@v10
        with:
          configPath: ./lighthouserc.json
          uploadArtifacts: true
          temporaryPublicStorage: true

# lighthouserc.json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:performance": ["error", {"minScore": 0.7}],
        "categories:accessibility": ["error", {"minScore": 0.9}],
        "categories:best-practices": ["warn", {"minScore": 0.9}],
        "first-contentful-paint": ["error", {"maxNumericValue": 2000}],
        "interactive": ["error", {"maxNumericValue": 4000}],
        "total-byte-weight": ["error", {"maxNumericValue": 500000}]
      }
    }
  }
}
```

---

## 4. Infrastructure Safety

### Owner: Aaliyah Muhammad
### Timeline: Dec 30 (backups TODAY) - Jan 13

### 4.1 Database Backup Configuration

```bash
# IMMEDIATE - Run today (Dec 30)

# Enable point-in-time recovery
fly postgres config update -a resilience-mapping-db \
  --wal-level logical

# Create initial backup
fly postgres backup create -a resilience-mapping-db

# Verify backup
fly postgres backup list -a resilience-mapping-db

# Test restore (to new instance)
fly postgres backup restore -a resilience-mapping-db \
  --backup-id <backup-id> \
  --app-name resilience-mapping-db-test
```

### 4.2 Monitoring Setup

```typescript
// src/lib/server/monitoring.ts

import { logger } from './logger';

interface HealthMetrics {
  database: {
    connected: boolean;
    latencyMs: number;
    poolSize: number;
    activeConnections: number;
  };
  memory: {
    heapUsedMB: number;
    heapTotalMB: number;
    externalMB: number;
  };
  uptime: number;
}

export async function collectMetrics(): Promise<HealthMetrics> {
  const dbStart = Date.now();
  const dbResult = await db.query('SELECT 1');
  const dbLatency = Date.now() - dbStart;

  const memUsage = process.memoryUsage();

  return {
    database: {
      connected: !!dbResult,
      latencyMs: dbLatency,
      poolSize: db.pool.totalCount,
      activeConnections: db.pool.idleCount,
    },
    memory: {
      heapUsedMB: Math.round(memUsage.heapUsed / 1024 / 1024),
      heapTotalMB: Math.round(memUsage.heapTotal / 1024 / 1024),
      externalMB: Math.round(memUsage.external / 1024 / 1024),
    },
    uptime: process.uptime(),
  };
}

// Health check endpoint
// src/routes/health/+server.ts

export async function GET() {
  try {
    const metrics = await collectMetrics();

    // Alert thresholds
    if (metrics.database.latencyMs > 100) {
      logger.warn('Database latency elevated', { latencyMs: metrics.database.latencyMs });
    }

    if (metrics.memory.heapUsedMB > 400) {
      logger.warn('Memory usage elevated', { heapUsedMB: metrics.memory.heapUsedMB });
    }

    return json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      metrics,
    });
  } catch (error) {
    logger.error('Health check failed', { error });
    return json({ status: 'unhealthy', error: error.message }, { status: 503 });
  }
}
```

### 4.3 Staging Environment

```toml
# fly.staging.toml

app = "resilience-mapping-staging"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[env]
  NODE_ENV = "staging"
  LOG_LEVEL = "debug"
  DATABASE_URL = "from secret"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512  # Smaller than prod
```

```bash
# Deploy to staging
fly deploy -c fly.staging.toml

# Staging vs Production differences:
# - Smaller VM (512MB vs 1GB)
# - Auto-stop when idle
# - Debug logging
# - Anonymized data subset
```

### 4.4 Incident Response Runbook

```markdown
# Incident Response Runbook
## Health Resilience Mapping Platform

### Severity Levels

| Level | Description | Response Time | Examples |
|-------|-------------|---------------|----------|
| SEV1 | Complete outage | 15 min | Site down, data loss |
| SEV2 | Degraded service | 1 hour | Slow responses, partial features broken |
| SEV3 | Minor issue | 4 hours | Non-critical bug, UI glitch |

### On-Call Rotation

**Current**: Aaliyah Muhammad (primary), Marcus Thompson (backup)
**Contact**: [Signal group / phone numbers]

### SEV1 Response

1. **ACKNOWLEDGE** (within 5 min)
   - Join incident Slack channel #incidents
   - Claim incident: "IC: [your name]"

2. **ASSESS** (within 15 min)
   - Check: `fly status -a resilience-mapping`
   - Check: `fly logs -a resilience-mapping`
   - Check: `/health` endpoint
   - Check database: `fly postgres connect -a resilience-mapping-db`

3. **MITIGATE**
   - If app crash: `fly machines restart`
   - If database: Check connection pool, restart if needed
   - If deployment: `fly releases list` then `fly deploy --image <previous>`

4. **COMMUNICATE**
   - Update status page (if exists)
   - Notify stakeholders in #incidents
   - Hourly updates until resolved

5. **RESOLVE & DOCUMENT**
   - Confirm service restored
   - Create post-mortem document
   - Schedule blameless review meeting

### Common Issues

#### App Won't Start
```bash
fly logs -a resilience-mapping | head -100
fly ssh console -a resilience-mapping
# Check: disk space, memory, env vars
```

#### Database Connection Failed
```bash
fly postgres connect -a resilience-mapping-db
# If can't connect, check:
fly machines list -a resilience-mapping-db
fly machines restart <machine-id> -a resilience-mapping-db
```

#### High Memory Usage
```bash
fly ssh console -a resilience-mapping
# Inside container:
top -o %MEM
# If needed, increase memory in fly.toml and redeploy
```
```

---

## 5. Design System Foundation

### Owner: Yuki Nakamura-Jackson
### Timeline: Jan 27 - Feb 10

### 5.1 Design Tokens

```css
/* src/lib/styles/tokens.css */

:root {
  /* ===== Typography ===== */
  --font-family-base: 'Inter', system-ui, sans-serif;
  --font-family-mono: 'JetBrains Mono', monospace;

  /* Type Scale (1.25 ratio) */
  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px - minimum for body */
  --font-size-lg: 1.25rem;    /* 20px */
  --font-size-xl: 1.5rem;     /* 24px */
  --font-size-2xl: 1.875rem;  /* 30px */
  --font-size-3xl: 2.25rem;   /* 36px */
  --font-size-4xl: 3rem;      /* 48px */

  /* Line Heights */
  --line-height-tight: 1.25;
  --line-height-base: 1.5;
  --line-height-relaxed: 1.75;

  /* Font Weights */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* ===== Colors ===== */
  /* All combinations tested for WCAG AA (4.5:1 for text, 3:1 for UI) */

  /* Semantic */
  --color-primary: #1e40af;         /* Blue 800 */
  --color-primary-hover: #1e3a8a;   /* Blue 900 */
  --color-secondary: #475569;       /* Slate 600 */
  --color-accent: #0891b2;          /* Cyan 600 */

  /* Feedback */
  --color-success: #15803d;         /* Green 700 */
  --color-warning: #a16207;         /* Yellow 700 */
  --color-error: #b91c1c;           /* Red 700 */
  --color-info: #0369a1;            /* Sky 700 */

  /* Surfaces */
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f8fafc;    /* Slate 50 */
  --color-bg-tertiary: #f1f5f9;     /* Slate 100 */
  --color-bg-elevated: #ffffff;

  /* Text */
  --color-text-primary: #0f172a;    /* Slate 900 */
  --color-text-secondary: #475569;  /* Slate 600 */
  --color-text-tertiary: #64748b;   /* Slate 500 */
  --color-text-inverse: #ffffff;

  /* Borders */
  --color-border-default: #e2e8f0;  /* Slate 200 */
  --color-border-strong: #cbd5e1;   /* Slate 300 */
  --color-border-focus: #3b82f6;    /* Blue 500 */

  /* ===== Spacing ===== */
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */

  /* ===== Radii ===== */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-full: 9999px;

  /* ===== Shadows ===== */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-focus: 0 0 0 3px rgb(59 130 246 / 0.5);

  /* ===== Transitions ===== */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;

  /* ===== Focus ===== */
  --focus-ring: 2px solid var(--color-border-focus);
  --focus-ring-offset: 2px;
}

/* High Contrast Mode */
@media (prefers-contrast: more) {
  :root {
    --color-text-primary: #000000;
    --color-text-secondary: #000000;
    --color-border-default: #000000;
    --color-border-strong: #000000;
  }
}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  :root {
    --transition-fast: 0ms;
    --transition-base: 0ms;
    --transition-slow: 0ms;
  }
}
```

### 5.2 Button Component

```svelte
<!-- src/lib/components/ui/Button.svelte -->

<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let variant: 'primary' | 'secondary' | 'ghost' | 'danger' = 'primary';
  export let size: 'sm' | 'md' | 'lg' = 'md';
  export let disabled = false;
  export let loading = false;
  export let type: 'button' | 'submit' | 'reset' = 'button';
  export let href: string | undefined = undefined;
  export let ariaLabel: string | undefined = undefined;

  const dispatch = createEventDispatcher();

  function handleClick(event: MouseEvent) {
    if (disabled || loading) {
      event.preventDefault();
      return;
    }
    dispatch('click', event);
  }

  $: tag = href ? 'a' : 'button';
  $: attrs = href
    ? { href, role: 'button' }
    : { type, disabled: disabled || loading };
</script>

<svelte:element
  this={tag}
  {...attrs}
  class="btn btn-{variant} btn-{size}"
  class:loading
  aria-label={ariaLabel}
  aria-busy={loading}
  aria-disabled={disabled}
  on:click={handleClick}
>
  {#if loading}
    <span class="spinner" aria-hidden="true"></span>
    <span class="sr-only">Loading...</span>
  {/if}
  <span class="btn-content" class:invisible={loading}>
    <slot />
  </span>
</svelte:element>

<style>
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-2);
    font-weight: var(--font-weight-medium);
    border-radius: var(--radius-md);
    transition: all var(--transition-fast);
    cursor: pointer;
    position: relative;
  }

  .btn:focus-visible {
    outline: var(--focus-ring);
    outline-offset: var(--focus-ring-offset);
  }

  /* Sizes */
  .btn-sm {
    padding: var(--space-1) var(--space-3);
    font-size: var(--font-size-sm);
    min-height: 32px;
  }

  .btn-md {
    padding: var(--space-2) var(--space-4);
    font-size: var(--font-size-base);
    min-height: 40px;
  }

  .btn-lg {
    padding: var(--space-3) var(--space-6);
    font-size: var(--font-size-lg);
    min-height: 48px;
  }

  /* Variants */
  .btn-primary {
    background: var(--color-primary);
    color: var(--color-text-inverse);
    border: none;
  }

  .btn-primary:hover:not(:disabled) {
    background: var(--color-primary-hover);
  }

  .btn-secondary {
    background: transparent;
    color: var(--color-text-primary);
    border: 1px solid var(--color-border-strong);
  }

  .btn-secondary:hover:not(:disabled) {
    background: var(--color-bg-secondary);
  }

  .btn-ghost {
    background: transparent;
    color: var(--color-text-primary);
    border: none;
  }

  .btn-ghost:hover:not(:disabled) {
    background: var(--color-bg-secondary);
  }

  .btn-danger {
    background: var(--color-error);
    color: var(--color-text-inverse);
    border: none;
  }

  /* States */
  .btn:disabled,
  .btn[aria-disabled="true"] {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .loading {
    cursor: wait;
  }

  .spinner {
    position: absolute;
    width: 1em;
    height: 1em;
    border: 2px solid currentColor;
    border-right-color: transparent;
    border-radius: var(--radius-full);
    animation: spin 0.75s linear infinite;
  }

  .invisible {
    visibility: hidden;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
  }
</style>
```

---

## Summary: Implementation Priorities

| Priority | Initiative | Owner | Target |
|----------|------------|-------|--------|
| P0 | Database backups | Aaliyah | TODAY |
| P0 | Institutional filter | Miguel | Jan 6 |
| P0 | Data validation | Miguel | Jan 13 |
| P1 | Accessible table | David + Jordan | Jan 27 |
| P1 | Performance <500KB | Jordan | Jan 27 |
| P1 | Monitoring | Aaliyah | Jan 13 |
| P2 | Design system | Yuki | Feb 10 |

---

*Document created: December 30, 2025*
*Post-Workshop Technical Specifications*
