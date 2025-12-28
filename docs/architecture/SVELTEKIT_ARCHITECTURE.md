# Technical Architecture: SvelteKit Edition
## Health Resilience Mapping Platform

**Updated**: December 26, 2025
**Version**: 2.0 (SvelteKit Migration)
**Status**: APPROVED

---

## Decision: SvelteKit over Next.js

### Why SvelteKit?

| Factor | SvelteKit | Next.js |
|--------|-----------|---------|
| **Bundle Size** | Smaller (no virtual DOM) | Larger React runtime |
| **Performance** | Compiled to vanilla JS | Runtime reconciliation |
| **Learning Curve** | Simpler reactivity model | Complex hooks/effects |
| **DX** | Less boilerplate | More configuration |
| **SSR/SSG** | Built-in, flexible | Built-in, opinionated |

### Trade-offs Accepted
- Smaller ecosystem than React
- Fewer pre-built component libraries
- Less enterprise adoption (but growing)

---

## System Overview

```
┌─────────────────────── USER LAYER ───────────────────────┐
│                                                           │
│  stories.*    research.*    policy.*    landing.*        │
│  (SvelteKit)  (SvelteKit)  (SvelteKit)  (SvelteKit)     │
│                                                           │
└─────────────────────── ▼ HTTPS ▼ ───────────────────────┘

┌─────────────────────── CDN LAYER ────────────────────────┐
│                                                           │
│              Cloudflare / Vercel Edge Network            │
│              • Static Assets  • Image Optimization       │
│              • Edge Caching   • DDoS Protection         │
│                                                           │
└─────────────────────── ▼ HTTPS ▼ ───────────────────────┘

┌─────────────────── APPLICATION LAYER ────────────────────┐
│                                                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │
│  │   SvelteKit  │ │   Supabase   │ │   Python     │     │
│  │   App        │ │   Backend    │ │   Analytics  │     │
│  │              │ │              │ │              │     │
│  │ • SSR/SSG    │ │ • PostgreSQL │ │ • Data ETL   │     │
│  │ • API Routes │ │ • Auth       │ │ • Model runs │     │
│  │ • Edge Funcs │ │ • Realtime   │ │ • Reports    │     │
│  └──────────────┘ └──────────────┘ └──────────────┘     │
│                                                           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────── DATA LAYER ───────────────────────┐
│                                                           │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐         │
│ │  Supabase   │ │  Supabase   │ │  Supabase   │         │
│ │  PostgreSQL │ │  Storage    │ │  Edge Funcs │         │
│ │  + PostGIS  │ │             │ │             │         │
│ │             │ │ • GeoJSON   │ │ • Search    │         │
│ │ • Tracts    │ │ • Images    │ │ • Aggregate │         │
│ │ • Scores    │ │ • Documents │ │ • Transform │         │
│ │ • Stories   │ │             │ │             │         │
│ └─────────────┘ └─────────────┘ └─────────────┘         │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend
| Layer | Technology | Purpose |
|-------|------------|---------|
| Framework | **SvelteKit 2.x** | SSR, routing, API routes |
| Styling | **Tailwind CSS** | Utility-first styling |
| Components | **Skeleton UI** or **shadcn-svelte** | Component library |
| Maps | **MapLibre GL** | Interactive mapping |
| Charts | **LayerChart** or **Pancake** | Data visualization |
| Forms | **Superforms** | Form handling + validation |

### Backend
| Layer | Technology | Purpose |
|-------|------------|---------|
| Database | **Supabase (PostgreSQL + PostGIS)** | Primary data store |
| Auth | **Supabase Auth** | Authentication |
| Storage | **Supabase Storage** | File uploads |
| API | **SvelteKit API Routes** | Server endpoints |
| Analytics | **Python (existing)** | Statistical analysis |

### Infrastructure
| Layer | Technology | Purpose |
|-------|------------|---------|
| Hosting | **Vercel** or **Cloudflare Pages** | Edge deployment |
| CDN | **Cloudflare** | Asset delivery |
| Monitoring | **Sentry** | Error tracking |
| Analytics | **Plausible** or **Umami** | Privacy-first analytics |

---

## Project Structure

```
app/
├── web/                          # SvelteKit application
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/       # Shared components
│   │   │   │   ├── ui/           # Base UI components
│   │   │   │   ├── map/          # Map components
│   │   │   │   ├── charts/       # Chart components
│   │   │   │   └── community/    # Community-specific
│   │   │   ├── stores/           # Svelte stores
│   │   │   ├── utils/            # Utility functions
│   │   │   └── server/           # Server-only code
│   │   ├── routes/
│   │   │   ├── (marketing)/      # Landing pages
│   │   │   ├── (research)/       # Research site
│   │   │   ├── (stories)/        # Stories site
│   │   │   ├── (policy)/         # Policy site
│   │   │   └── api/              # API endpoints
│   │   ├── app.html
│   │   ├── app.css
│   │   └── hooks.server.ts
│   ├── static/
│   ├── svelte.config.js
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── package.json
├── analytics/                    # Python analytics (existing)
│   ├── resilience_model.py
│   ├── enhanced_filters.py
│   └── ...
└── backend/                      # Go backend (archived/reference)
    └── ...
```

---

## Component Architecture

### Shared Components (lib/components/)

```svelte
<!-- Example: CommunityCard.svelte -->
<script lang="ts">
  import type { Community } from '$lib/types';

  export let community: Community;
  export let variant: 'compact' | 'full' = 'compact';
</script>

<article class="community-card" class:full={variant === 'full'}>
  <header>
    <h3>{community.name}</h3>
    <span class="score">{community.resilience_score.toFixed(2)}</span>
  </header>
  <p>{community.county}, {community.state}</p>
  <slot name="actions" />
</article>
```

### State Management (lib/stores/)

```typescript
// lib/stores/communities.ts
import { writable, derived } from 'svelte/store';
import type { Community } from '$lib/types';

export const communities = writable<Community[]>([]);
export const selectedCommunity = writable<Community | null>(null);

export const resilientCommunities = derived(
  communities,
  $communities => $communities.filter(c => c.resilience_score > 1.645)
);
```

### Server Functions (lib/server/)

```typescript
// lib/server/db.ts
import { createClient } from '@supabase/supabase-js';
import { SUPABASE_URL, SUPABASE_SERVICE_KEY } from '$env/static/private';

export const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

export async function getCommunities(limit = 100) {
  const { data, error } = await supabase
    .from('communities')
    .select('*')
    .order('resilience_score', { ascending: false })
    .limit(limit);

  if (error) throw error;
  return data;
}
```

---

## Routing Structure

### Route Groups

```
routes/
├── (marketing)/                  # Public landing pages
│   ├── +page.svelte              # Homepage
│   ├── about/+page.svelte
│   └── methodology/+page.svelte
├── (research)/                   # Research portal
│   ├── +layout.svelte            # Research layout
│   ├── +page.svelte              # Research dashboard
│   ├── data/+page.svelte         # Data explorer
│   └── methodology/+page.svelte
├── (stories)/                    # Community stories
│   ├── +layout.svelte            # Stories layout
│   ├── +page.svelte              # Stories browse
│   └── [community]/+page.svelte  # Individual story
├── (policy)/                     # Policy portal
│   ├── +layout.svelte
│   ├── +page.svelte
│   └── briefs/+page.svelte
└── api/                          # API routes
    ├── communities/+server.ts
    ├── search/+server.ts
    └── export/+server.ts
```

---

## Data Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Python    │────▶│  Supabase   │────▶│  SvelteKit  │
│  Analytics  │     │  PostgreSQL │     │   Frontend  │
│             │     │             │     │             │
│ • Run model │     │ • Store     │     │ • SSR pages │
│ • Generate  │     │ • Query     │     │ • API calls │
│   scores    │     │ • PostGIS   │     │ • Realtime  │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Data Pipeline

1. **Python Analytics** → Generates resilience scores
2. **Import to Supabase** → Existing `import_to_supabase.py`
3. **SvelteKit SSR** → Server-side data fetching
4. **Client Hydration** → Interactive maps/charts

---

## Deployment

### Vercel (Recommended)

```bash
# Install adapter
npm install -D @sveltejs/adapter-vercel

# svelte.config.js
import adapter from '@sveltejs/adapter-vercel';

export default {
  kit: {
    adapter: adapter({
      runtime: 'edge', // or 'nodejs18.x'
    })
  }
};
```

### Cloudflare Pages (Alternative)

```bash
# Install adapter
npm install -D @sveltejs/adapter-cloudflare

# svelte.config.js
import adapter from '@sveltejs/adapter-cloudflare';

export default {
  kit: {
    adapter: adapter()
  }
};
```

---

## Migration from Next.js Plan

Since no Next.js code exists yet, this is a clean start:

1. **Phase 1**: Set up SvelteKit monorepo structure
2. **Phase 2**: Implement design system components
3. **Phase 3**: Build research site (data-only)
4. **Phase 4**: Build stories site (with consent)
5. **Phase 5**: Build policy site

---

## Environment Variables

```bash
# .env
PUBLIC_SUPABASE_URL=https://xxx.supabase.co
PUBLIC_SUPABASE_ANON_KEY=xxx

# Private (server-only)
SUPABASE_SERVICE_KEY=xxx
```

---

## Performance Targets

| Metric | Target |
|--------|--------|
| Lighthouse Score | > 95 |
| First Contentful Paint | < 1.2s |
| Time to Interactive | < 2.5s |
| Bundle Size (JS) | < 100KB gzipped |
| Core Web Vitals | All green |

---

*Document approved by: Project Lead*
*Last updated: December 26, 2025*
