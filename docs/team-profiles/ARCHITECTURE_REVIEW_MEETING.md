# Architecture Review Meeting - January 31, 2025
## Health Resilience Mapping Platform Implementation

**Meeting Lead**: Marcus Thompson (35% weight)  
**Required Attendees**: Marcus, Aaliyah, Miguel  
**Full Team Present**: All 8 core members

---

## Opening - Marcus Thompson (Technical Architect)

**Marcus**: Alright team, we need to finalize our architecture. We have 1,059 communities in Supabase, the data import works, and now we need to build the platform. The question on the table: Vercel or Fly.io for deployment? But more importantly - what's our entire technical stack?

Let me start with my concerns: We're serving vulnerable communities on bad phones with spotty connections. Every architectural decision must pass the "3am on 3% battery on one bar of signal" test.

---

## The Great Deployment Debate

**Jordan Park (Frontend)**: I vote Vercel, hands down. Their edge network is unmatched for static site generation. We can pre-render community pages, serve them from 70+ edge locations globally. First contentful paint under 1.5 seconds even on 3G. Plus, Next.js is literally made by Vercel - the integration is seamless.

**Aaliyah Muhammad (DevOps)**: Hold up, Jordan. Fly.io gives us actual containers, not just serverless functions. We can run persistent connections for real-time updates, WebSockets for community notifications. And we control the entire stack - no vendor lock-in. Plus, Fly.io's anycast network rivals Vercel's edge performance.

**Marcus**: Both valid points. But here's my take - we use BOTH. Hear me out:
- **Vercel** for the frontend sites (stories, research, policy) - static generation, edge caching
- **Fly.io** for critical backend services - WebSocket server, background jobs, data processing
- **Supabase** remains our database and auth layer

**Aaliyah**: That's... actually brilliant. Separation of concerns. Frontend can fail without taking down data services. I can implement circuit breakers between them.

---

## Frontend Architecture Deep Dive

**Yuki Nakamura-Jackson (Design)**: Before we lock in Next.js, let's discuss the design system implementation. I need:
- Component-level code splitting for performance
- CSS-in-JS for dynamic theming (dark mode, high contrast)
- Animation capabilities for dignity through motion
- Server-side rendering for SEO

**Jordan**: Next.js 14 with App Router gives us all of that. Plus:
- React Server Components for zero client JS where possible
- Parallel routes for the three sites
- Built-in image optimization
- Incremental static regeneration for fresh content

**David Chen-Williams (Accessibility)**: I need guarantees on accessibility. Can Next.js handle:
- Focus management across route transitions?
- Announcements for screen readers?
- Keyboard navigation without JavaScript?

**Jordan**: Yes to all three. We'll use:
- `next/link` with focus restoration
- Live regions for dynamic content
- Progressive enhancement - works without JS

**Yuki**: Sold. But we're building a monorepo, right? Three sites, shared components?

**Marcus**: Absolutely. Turborepo structure:
```
/apps
  /stories    (Next.js app)
  /research   (Next.js app)
  /policy     (Next.js app)
/packages
  /ui         (shared components)
  /utils      (shared utilities)
  /types      (TypeScript definitions)
```

---

## Data Architecture with Miguel

**Miguel Santos (Data Infrastructure)**: Let's talk geography. Supabase uses PostGIS - perfect. But we need to discuss:

1. **Coordinate precision**: Store full precision, display rounded
2. **Boundary versioning**: Census boundaries change yearly
3. **Spatial indexes**: For proximity queries
4. **Map tile generation**: Vector tiles or raster?

Here's my proposal:
```sql
-- Geographic data structure
CREATE TABLE communities (
    id UUID PRIMARY KEY,
    tract_id VARCHAR(11) UNIQUE,
    -- Store as geography for accurate calculations
    boundary GEOGRAPHY(MULTIPOLYGON, 4326),
    -- Also store simplified geometry for fast display
    boundary_simplified GEOMETRY(MULTIPOLYGON, 4326),
    -- Centroid for quick distance calculations
    centroid GEOGRAPHY(POINT, 4326),
    -- Bounding box for initial filtering
    bbox BOX2D,
    -- Temporal versioning
    boundary_year INTEGER,
    boundary_source VARCHAR(50)
);

-- Spatial indexes for performance
CREATE INDEX idx_communities_boundary ON communities USING GIST(boundary);
CREATE INDEX idx_communities_centroid ON communities USING GIST(centroid);
CREATE INDEX idx_communities_bbox ON communities USING GIST(bbox);
```

**Marcus**: Excellent. How do we serve map data efficiently?

**Miguel**: Three-tier approach:
1. **Overview (zoom 0-8)**: Pre-generated raster tiles on CDN
2. **Regional (zoom 9-12)**: Vector tiles from Fly.io cache
3. **Detail (zoom 13+)**: Dynamic PostGIS queries

**Jordan**: I'll use MapboxGL for rendering. Progressive loading based on zoom level.

---

## Security & Privacy Architecture

**Keisha Williams (Community Trust)**: Stop. Before we go further - how are we protecting communities? I need guarantees on:
- No tracking pixels
- No third-party analytics
- Community-controlled data deletion
- Encrypted personally identifiable information

**Marcus**: Here's the security architecture:
```typescript
// Row Level Security in Supabase
communities
  - public_view (anyone)
  - authenticated_view (registered users)
  - community_admin (community members only)
  - sensitive_data (encrypted, key per community)

// Encryption at rest
- Database: AES-256
- File storage: Client-side encryption for uploads
- Backups: Encrypted with separate keys

// No tracking
- First-party analytics only (self-hosted Plausible)
- No Google Analytics, no Facebook Pixel
- Cookie-less, GDPR/CCPA compliant
```

**Aaliyah**: Adding to that - defense in depth:
```yaml
Security Layers:
  1. Cloudflare: DDoS protection, rate limiting
  2. Vercel: Edge authentication checks
  3. Fly.io: Application firewall
  4. Supabase: Row-level security
  5. Encryption: Field-level for PII
```

**Keisha**: What about community consent management?

**Amara Chen-Rodriguez (Product)**: Built into the schema:
```typescript
interface CommunityConsent {
  dataSharing: 'public' | 'researchers' | 'private'
  storySharing: boolean
  contactSharing: 'none' | 'verified' | 'all'
  updateNotifications: boolean
  withdrawConsent: () => Promise<void> // Instant deletion
}
```

---

## Performance Requirements Deep Dive

**Jordan**: Based on the wireframes, here are my performance targets:
```javascript
const performanceTargets = {
  mobile: {
    FCP: 1500,  // First Contentful Paint
    LCP: 2500,  // Largest Contentful Paint
    CLS: 0.1,   // Cumulative Layout Shift
    FID: 100,   // First Input Delay
    bundleSize: 100 * 1024, // 100KB initial JS
  },
  desktop: {
    FCP: 1000,
    LCP: 2000,
    CLS: 0.05,
    FID: 50,
    bundleSize: 200 * 1024,
  }
}
```

**Aaliyah**: To achieve that, we need aggressive optimization:
```yaml
Optimization Strategy:
  Build Time:
    - Tree shaking everything
    - Route-based code splitting
    - Preact for production (smaller than React)
    - WebP/AVIF images with fallbacks
  
  Runtime:
    - Service worker for offline
    - Resource hints (prefetch, preconnect)
    - HTTP/3 with 0-RTT
    - Brotli compression
  
  Edge:
    - Static generation for all community pages
    - ISR (Incremental Static Regeneration) every hour
    - Edge middleware for personalization
    - Stale-while-revalidate caching
```

---

## The Three-Site Architecture

**Amara**: Let's clarify the three-site strategy from a product perspective:
- **stories.*** - Community-facing, emotion-driven, beautiful
- **research.*** - Data-facing, analysis-driven, comprehensive  
- **policy.*** - Action-facing, urgency-driven, practical

**Marcus**: Technically, they share:
```typescript
// Shared infrastructure
const sharedServices = {
  database: 'Supabase PostgreSQL',
  auth: 'Supabase Auth',
  storage: 'Supabase Storage',
  search: 'Typesense on Fly.io',
  email: 'Resend',
  monitoring: 'Sentry + Prometheus',
}

// But separate:
const siteSpecific = {
  stories: {
    cms: 'Sanity.io',
    media: 'Cloudinary',
    analytics: 'Plausible',
  },
  research: {
    notebooks: 'Observable embeds',
    compute: 'Fly.io workers',
    exports: 'Scheduled jobs',
  },
  policy: {
    documents: 'PDF generation',
    briefing: 'Markdown to PDF',
    scheduling: 'Cal.com embed',
  }
}
```

**Yuki**: Design-wise, they share components but have distinct themes:
```css
/* Shared design tokens */
--color-primary: #2563EB;
--font-body: 'Inter', sans-serif;
--spacing-unit: 8px;

/* Site-specific */
stories { --emotion: warm; --imagery: full; }
research { --emotion: neutral; --imagery: charts; }
policy { --emotion: urgent; --imagery: minimal; }
```

---

## Critical Infrastructure Decisions

**Aaliyah**: We need to decide on critical infrastructure:

### Option A: Maximum Resilience (My recommendation)
```yaml
Primary Region: us-east-1
  - Vercel deployment
  - Supabase database
  - Fly.io services

Failover Region: us-west-2  
  - Standby database replica
  - Cached static content
  - Degraded mode operations

Disaster Recovery:
  - 15-minute RPO
  - 1-hour RTO
  - Automated failover
```

### Option B: Cost-Optimized (But still reliable)
```yaml
Single Region: us-central
  - All services co-located
  - Daily backups to different region
  - Manual failover process
  - 4-hour RTO acceptable
```

**Marcus**: Given our user base, I vote Option A. Communities depend on us.

**Amara**: Agreed. The extra cost is worth zero downtime.

---

## Development Workflow

**Marcus**: Let's define our development workflow:
```bash
# Local development
1. Supabase local (Docker)
2. Next.js dev server (pnpm)
3. Fly.io local (Docker)

# Branch strategy
main → production
staging → staging environment
feature/* → preview deployments

# CI/CD Pipeline (GitHub Actions)
1. Type checking (TypeScript)
2. Linting (ESLint + Prettier)
3. Unit tests (Vitest)
4. Integration tests (Playwright)
5. Accessibility tests (axe-core)
6. Performance tests (Lighthouse CI)
7. Security scan (Snyk)
8. Deploy preview (Vercel)
9. E2E tests against preview
10. Merge to main = auto-deploy
```

**Jordan**: For local development, we need:
```json
{
  "scripts": {
    "dev": "turbo run dev",
    "dev:stories": "pnpm --filter stories dev",
    "dev:research": "pnpm --filter research dev",
    "dev:policy": "pnpm --filter policy dev",
    "test": "turbo run test",
    "test:a11y": "turbo run test:a11y",
    "test:e2e": "playwright test",
    "build": "turbo run build",
    "deploy": "turbo run deploy"
  }
}
```

---

## Implementation Timeline

**Amara**: Based on this architecture, what's our timeline?

**Marcus**: Here's my proposal:

### Week 1-2: Foundation
- [ ] Monorepo setup with Turborepo
- [ ] Shared component library
- [ ] Design system implementation
- [ ] Supabase schema finalization
- [ ] CI/CD pipeline

### Week 3-4: Core Features
- [ ] Authentication flow
- [ ] Community pages (static generation)
- [ ] Search implementation
- [ ] Map integration
- [ ] Story submission

### Week 5-6: Three Sites
- [ ] Stories site MVP
- [ ] Research site MVP
- [ ] Policy site MVP
- [ ] Cross-site navigation
- [ ] Content management

### Week 7-8: Production Readiness
- [ ] Performance optimization
- [ ] Security audit
- [ ] Accessibility audit
- [ ] Load testing
- [ ] Documentation

---

## Final Architecture Decision

**Marcus**: Let me summarize our architecture:

```yaml
Frontend:
  Framework: Next.js 14 (App Router)
  Deployment: Vercel (Edge Network)
  Structure: Monorepo (Turborepo)
  Styling: Tailwind + CSS Modules
  Components: Radix UI + Custom
  State: Zustand
  Maps: MapboxGL

Backend:
  Database: Supabase (PostgreSQL + PostGIS)
  Auth: Supabase Auth
  Realtime: Supabase Realtime + Fly.io WebSockets
  Storage: Supabase Storage
  Search: Typesense on Fly.io
  Workers: Fly.io (Scheduled jobs)
  Email: Resend

Infrastructure:
  CDN: Vercel Edge Network
  DNS: Cloudflare
  Monitoring: Sentry + Prometheus
  Analytics: Plausible (self-hosted)
  CI/CD: GitHub Actions
  Containers: Fly.io (for services)

Security:
  WAF: Cloudflare
  Secrets: GitHub Secrets + Vercel Env
  Encryption: At-rest + In-transit
  Auth: JWT + Row Level Security
  Audit: Every data access logged
```

**All team members**: Approved! ✅

---

## Keisha's Final Checkpoint

**Keisha**: Before we proceed, I need confirmation:
1. Communities can delete their data instantly? **Marcus**: Yes, hard delete with audit log.
2. No surveillance capabilities? **Aaliyah**: None. No tracking, no analytics without consent.
3. Beautiful and dignified? **Yuki**: Every pixel designed with respect.
4. Works on old phones? **Jordan**: Tested on 5-year-old Android devices.
5. Accessible to all? **David**: WCAG AAA compliance guaranteed.

**Keisha**: Then I give my blessing. Build it.

---

## Action Items

1. **Marcus**: Set up monorepo structure, create base architecture (TODAY)
2. **Jordan**: Initialize Next.js apps with shared components (TODAY)
3. **Miguel**: Finalize PostGIS schema and spatial indexes (TODAY)
4. **Aaliyah**: Configure Vercel + Fly.io deployments (TODAY)
5. **Yuki**: Create design system package (TOMORROW)
6. **David**: Set up accessibility testing pipeline (TOMORROW)
7. **Amara**: Document product requirements based on architecture (TOMORROW)
8. **Keisha**: Review and approve community consent flows (THIS WEEK)

---

## Meeting Closed

**Marcus**: We have our architecture. It's bulletproof, scalable, and respects our communities. Let's build.

**Team Motto**: *"Every millisecond matters. Every pixel has purpose. Every query protects privacy."*

---

*Meeting Duration: 2 hours*  
*Decision: APPROVED by all members*  
*Next Review: Week 2 Progress Check*