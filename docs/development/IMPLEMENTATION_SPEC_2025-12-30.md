# Implementation Specification & Task Tracker
## Resilience Mapping Site Improvements
**Created:** December 30, 2025
**Timeline:** 10 weeks (Q1 2026)
**Status:** Planning Complete - Ready for Implementation

---

## Executive Summary

Following comprehensive review by product leadership, engineering workshop, and domain expert validation, we have a validated 10-week implementation plan with clear phases, dependencies, and acceptance criteria.

### Key Workshop Decisions

| Decision | Verdict | Rationale |
|----------|---------|-----------|
| Data Quality First | ✅ MANDATORY | Prison tracts flagged as "resilient" is blocking |
| Infrastructure Before UX | ✅ MANDATORY | No caching, no indexes = failure under load |
| Server-Side Pagination | ✅ APPROVED | Only scalable approach for 68K rows |
| Interactive Charts | ❌ DEFERRED to Q2 | Too complex, not core value |
| User Accounts | ❌ DEFERRED indefinitely | No use case identified |
| Trajectory Predictions UI | ❌ REJECTED | Research proves they don't work |

### Validation Summary (Expert Panel)

**Geospatial Analyst (Dr. Marcus Williams):**
- Confirmed geographic clustering patterns valid
- Identified 14/50 top tracts have zero population (data quality issue)
- Recommended: "Health Opportunity Zones" for priority intervention

**Epidemiologist (Dr. Sarah Chen):**
- Validated burden-resilience correlation (r = -0.72)
- 67 million Americans in above-average burden communities
- 28% of extreme tracts are unpopulated (artifact concern)

**Biostatistician (Dr. James Park):**
- **Grade: B+ (Strong with Reservations)**
- Extreme values are statistically valid (0.3% beyond 3σ matches theory)
- Critical concern: Construct independence unclear
- Recommendation: Population filters mandatory

---

## Phase 0: Data Quality Sprint (Weeks 1-2)
### BLOCKING - No other work proceeds until complete

#### Task 0.1: Identify and Flag Special Population Tracts
**Status:** `pending`
**Assignee:** TBD
**Acceptance Criteria:**
- [ ] Query identifies all tracts with resilience score > 2.0 AND population < 500
- [ ] Cross-reference with Census institutional population data
- [ ] Flag categories: prison, military, college, nursing home, zero-population
- [ ] Export list for manual review

**Technical Notes:**
```sql
-- Candidate query for special population identification
SELECT
  fips,
  resilience_score,
  population,
  CASE
    WHEN population = 0 THEN 'zero_population'
    WHEN name ILIKE '%correctional%' OR name ILIKE '%prison%' THEN 'prison'
    WHEN name ILIKE '%military%' OR name ILIKE '%base%' THEN 'military'
    WHEN name ILIKE '%university%' OR name ILIKE '%college%' THEN 'college'
    ELSE 'review_needed'
  END as tract_type
FROM tracts
WHERE resilience_score > 2.0 AND population < 500
ORDER BY resilience_score DESC;
```

#### Task 0.2: Create Exclusion/Flagging System
**Status:** `pending`
**Assignee:** TBD
**Acceptance Criteria:**
- [ ] Add `tract_type` enum column to tracts table
- [ ] Add `is_residential` boolean column
- [ ] Create migration script
- [ ] Update all affected tracts
- [ ] Add filtering to all public-facing queries

**Database Migration:**
```sql
ALTER TABLE tracts ADD COLUMN tract_type TEXT DEFAULT 'residential';
ALTER TABLE tracts ADD COLUMN is_residential BOOLEAN DEFAULT TRUE;
CREATE INDEX idx_tracts_residential ON tracts(is_residential) WHERE is_residential = TRUE;
```

#### Task 0.3: Validate "Top Resilient" List
**Status:** `pending`
**Assignee:** TBD
**Acceptance Criteria:**
- [ ] Manual review of top 100 resilient tracts
- [ ] Verify none are prisons, military bases, or unpopulated
- [ ] Document any edge cases (legitimate small-population resilient communities)
- [ ] Create test suite for data quality checks

#### Task 0.4: Add Population Filters to API
**Status:** `pending`
**Assignee:** TBD
**Acceptance Criteria:**
- [ ] All API endpoints default to `is_residential=TRUE`
- [ ] Add optional `include_institutional=true` parameter for research use
- [ ] Update API documentation
- [ ] Add integration tests

**Files to Modify:**
- `src/routes/api/tracts/+server.ts`
- `src/routes/api/tracts/[fips]/+server.ts`
- `src/lib/server/db/queries.ts`

---

## Phase 1: Infrastructure Foundation (Weeks 3-5)

### Week 3: Database Performance

#### Task 1.1: Add Missing Indexes
**Status:** `pending`
**Priority:** CRITICAL
**Acceptance Criteria:**
- [ ] Create composite index on (state_abbr, resilience_score DESC)
- [ ] Create index on burden_score for filtering
- [ ] Create index on population for range queries
- [ ] Benchmark: Query time < 100ms for paginated results

```sql
-- Required indexes
CREATE INDEX CONCURRENTLY idx_tracts_state_score
  ON tracts(state_abbr, resilience_score DESC);
CREATE INDEX CONCURRENTLY idx_tracts_burden
  ON tracts(burden_score);
CREATE INDEX CONCURRENTLY idx_tracts_population
  ON tracts(population);
CREATE INDEX CONCURRENTLY idx_tracts_geom_gist
  ON tracts USING GIST(geom);
```

#### Task 1.2: Create Materialized Views for Aggregates
**Status:** `pending`
**Acceptance Criteria:**
- [ ] State-level aggregates (count, avg score, population sum)
- [ ] Score distribution histogram buckets
- [ ] Automatic refresh on data update
- [ ] Dashboard queries < 50ms

```sql
CREATE MATERIALIZED VIEW state_aggregates AS
SELECT
  state_abbr,
  COUNT(*) as tract_count,
  SUM(population) as total_population,
  AVG(resilience_score) as avg_resilience,
  AVG(burden_score) as avg_burden,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY resilience_score) as median_resilience
FROM tracts
WHERE is_residential = TRUE
GROUP BY state_abbr;

CREATE UNIQUE INDEX ON state_aggregates(state_abbr);
```

#### Task 1.3: Add Database Connection Pooling
**Status:** `pending`
**Acceptance Criteria:**
- [ ] Implement connection pooling in production
- [ ] Max connections: 20 (Fly.io limit)
- [ ] Idle timeout: 30 seconds
- [ ] Add connection pool monitoring

### Week 4: HTTP Caching Layer

#### Task 1.4: Implement Cache-Control Headers
**Status:** `pending`
**Acceptance Criteria:**
- [ ] Static assets: 1 year cache (immutable)
- [ ] API responses: 5 minute cache, stale-while-revalidate
- [ ] HTML: no-cache, must-revalidate
- [ ] Verify headers with curl/browser dev tools

**Implementation Pattern:**
```typescript
// src/hooks.server.ts
export const handle: Handle = async ({ event, resolve }) => {
  const response = await resolve(event);

  if (event.url.pathname.startsWith('/api/')) {
    response.headers.set('Cache-Control', 'public, max-age=300, stale-while-revalidate=60');
    response.headers.set('Vary', 'Accept-Encoding');
  }

  return response;
};
```

#### Task 1.5: Add ETag Support for API Responses
**Status:** `pending`
**Acceptance Criteria:**
- [ ] Generate ETags based on content hash
- [ ] Return 304 Not Modified when appropriate
- [ ] Reduce bandwidth for repeat visitors
- [ ] Test with conditional GET requests

#### Task 1.6: CDN Configuration Review
**Status:** `pending`
**Acceptance Criteria:**
- [ ] Verify Fly.io edge caching is active
- [ ] Test from multiple geographic locations
- [ ] Document cache hit/miss ratios
- [ ] Consider Cloudflare if Fly.io insufficient

### Week 5: Rate Limiting & Monitoring

#### Task 1.7: Implement Rate Limiting
**Status:** `pending`
**Priority:** CRITICAL (before public launch)
**Acceptance Criteria:**
- [ ] 100 requests/minute per IP for API
- [ ] 1000 requests/minute for static assets
- [ ] Graceful 429 response with Retry-After header
- [ ] Whitelist known research partners

**Implementation:**
```typescript
// Using @upstash/ratelimit or similar
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(100, '1 m'),
  analytics: true,
});
```

#### Task 1.8: Add Application Monitoring
**Status:** `pending`
**Acceptance Criteria:**
- [ ] Error tracking (Sentry or similar)
- [ ] Performance monitoring (Core Web Vitals)
- [ ] Database query logging (slow queries > 100ms)
- [ ] Uptime monitoring with alerting

#### Task 1.9: Load Testing
**Status:** `pending`
**Acceptance Criteria:**
- [ ] Simulate 1000 concurrent users
- [ ] Response time P95 < 500ms
- [ ] No errors under load
- [ ] Database connections stay under limit
- [ ] Document capacity limits

**Load Test Script:**
```bash
# Using k6 or similar
k6 run --vus 1000 --duration 5m load-test.js
```

---

## Phase 2: Core UX Implementation (Weeks 6-9)

### Week 6: Homepage & Navigation

#### Task 2.1: Update Homepage Messaging
**Status:** `pending`
**Acceptance Criteria:**
- [ ] New headline: "Discover Communities Defying Health Expectations"
- [ ] Three clear CTAs: Explore Map, Download Data, Read Research
- [ ] Audience segmentation: Researchers, Journalists, Policymakers, Community Orgs
- [ ] Key statistics prominent (68,170 tracts, 330M population)

**Copy Source:** `docs/development/SITE_IMPROVEMENTS_2025-12-30.md` Section 1

#### Task 2.2: Create /research Route
**Status:** `pending`
**Priority:** HIGH (credibility + differentiation)
**Acceptance Criteria:**
- [ ] Route renders at `/research`
- [ ] Lists Paper 1 and Paper 2 with status badges
- [ ] Surfaces 5 key findings from Paper 2 (with visualizations)
- [ ] "What We Got Wrong" section (transparency)
- [ ] Links to GitHub, data download, methodology

**Component Structure:**
```
src/routes/(standard)/research/
├── +page.svelte
├── +page.server.ts
└── components/
    ├── PaperCard.svelte
    ├── FindingCard.svelte
    └── MethodologySection.svelte
```

#### Task 2.3: Add Research Findings to Homepage
**Status:** `pending`
**Acceptance Criteria:**
- [ ] 3 key findings as cards/callouts
- [ ] Each links to /research for detail
- [ ] Finding 1: "Health Levels Are 99.7% Stable"
- [ ] Finding 2: "Annual Changes Are Mostly Noise"
- [ ] Finding 3: "Geography Explains 28% of Variance"

### Week 7: Accessible Data Table (Foundation)

#### Task 2.4: Server-Side Pagination Infrastructure
**Status:** `pending`
**Priority:** CRITICAL
**Acceptance Criteria:**
- [ ] URL-based state: `?page=1&sort=score&order=desc&state=CA`
- [ ] Works without JavaScript
- [ ] 100 rows per page (configurable)
- [ ] Total count shown
- [ ] Page navigation (prev/next + jump to page)

**Implementation:**
```typescript
// src/routes/(standard)/data/+page.server.ts
export const load: PageServerLoad = async ({ url }) => {
  const page = parseInt(url.searchParams.get('page') || '1');
  const limit = 100;
  const offset = (page - 1) * limit;
  const state = url.searchParams.get('state');
  const sort = url.searchParams.get('sort') || 'resilience_score';
  const order = url.searchParams.get('order') || 'desc';

  const [tracts, countResult] = await Promise.all([
    db.query(`
      SELECT * FROM tracts
      WHERE is_residential = TRUE
      ${state ? `AND state_abbr = $1` : ''}
      ORDER BY ${sort} ${order}
      LIMIT ${limit} OFFSET ${offset}
    `, state ? [state] : []),
    db.query('SELECT COUNT(*) FROM tracts WHERE is_residential = TRUE')
  ]);

  return {
    tracts: tracts.rows,
    total: parseInt(countResult.rows[0].count),
    page,
    totalPages: Math.ceil(countResult.rows[0].count / limit),
    filters: { state, sort, order }
  };
};
```

#### Task 2.5: Create DataTable Component
**Status:** `pending`
**Acceptance Criteria:**
- [ ] Proper `<table>` with `role="grid"`
- [ ] Sortable column headers with `aria-sort`
- [ ] Row count announced to screen readers
- [ ] `aria-rowcount` and `aria-rowindex` attributes
- [ ] Caption describing current filter/sort state

**Accessibility Requirements:**
```svelte
<table
  role="grid"
  aria-label="Community health resilience data"
  aria-rowcount={totalRows}
>
  <caption class="sr-only">
    Showing {filteredCount} communities, sorted by {sortColumn} {sortDirection}
  </caption>
  <!-- ... -->
</table>
```

#### Task 2.6: Keyboard Navigation
**Status:** `pending`
**Priority:** CRITICAL for accessibility
**Acceptance Criteria:**
- [ ] Arrow keys navigate between cells
- [ ] Enter expands row detail
- [ ] Tab moves between interactive elements
- [ ] Home/End jump to first/last row
- [ ] No keyboard traps
- [ ] Focus indicator visible

**Key Bindings:**
| Key | Action |
|-----|--------|
| ↑/↓ | Move between rows |
| ←/→ | Move between cells |
| Enter | Expand row / activate link |
| Space | Toggle selection |
| Home/End | First/last row |
| Page Up/Down | Jump 10 rows |
| Escape | Close expanded detail |

### Week 8: Data Table Polish & Filters

#### Task 2.7: Filter Bar Implementation
**Status:** `pending`
**Acceptance Criteria:**
- [ ] State dropdown (51 options + "All States")
- [ ] Score range slider (or min/max inputs)
- [ ] Population filter (min/max)
- [ ] All filters update URL (shareable)
- [ ] "Reset Filters" button

#### Task 2.8: Live Region for Announcements
**Status:** `pending`
**Acceptance Criteria:**
- [ ] `aria-live="polite"` region for status updates
- [ ] Announce when filters change: "Showing 245 communities in California"
- [ ] Announce when page changes: "Page 5 of 27"
- [ ] Announce when sort changes

```svelte
<div aria-live="polite" aria-atomic="true" class="sr-only">
  {announcement}
</div>
```

#### Task 2.9: CSV Export with Filters
**Status:** `pending`
**Acceptance Criteria:**
- [ ] "Download CSV" button respects current filters
- [ ] Filename includes filter state: `resilience_CA_2024.csv`
- [ ] Includes all columns with headers
- [ ] Streaming download for large datasets
- [ ] Works without JavaScript

### Week 9: Map Improvements & Integration

#### Task 2.10: Improved Map Popups
**Status:** `pending`
**Acceptance Criteria:**
- [ ] Show percentile rank ("Top 5% nationally")
- [ ] Show state rank ("12 of 1,842 in California")
- [ ] Link to full tract detail in data table
- [ ] Population and key metrics
- [ ] Accessible close button

#### Task 2.11: Map-Table Integration
**Status:** `pending`
**Acceptance Criteria:**
- [ ] "View on Map" button in data table focuses map on tract
- [ ] Map click updates selected row in table (if visible)
- [ ] URL includes both map position and selected tract
- [ ] Bidirectional sync is smooth

#### Task 2.12: Fix Keyboard Accessibility on Map
**Status:** `pending`
**Priority:** CRITICAL (current keyboard trap)
**Acceptance Criteria:**
- [ ] Tab does not trap focus in map
- [ ] Skip link available to bypass map
- [ ] Basic keyboard navigation for map controls
- [ ] Screen reader can access legend and attribution

---

## Phase 3: Integration & Launch Prep (Week 10)

#### Task 3.1: Accessibility Audit
**Status:** `pending`
**Acceptance Criteria:**
- [ ] Lighthouse Accessibility score > 90
- [ ] axe DevTools shows 0 critical/serious issues
- [ ] WAVE tool shows 0 errors
- [ ] Manual keyboard navigation test passes
- [ ] Screen reader (VoiceOver/NVDA) test passes

**Current Baseline:** Lighthouse Accessibility = 67

#### Task 3.2: Performance Audit
**Status:** `pending`
**Acceptance Criteria:**
- [ ] Lighthouse Performance score > 90
- [ ] First Contentful Paint < 1.5s
- [ ] Time to Interactive < 3s
- [ ] Largest Contentful Paint < 2.5s
- [ ] Total Blocking Time < 200ms

**Current Baseline:** FCP ~2.3s, TTI ~4s

#### Task 3.3: Cross-Browser Testing
**Status:** `pending`
**Acceptance Criteria:**
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] iOS Safari
- [ ] Chrome Android
- [ ] Data table works without JavaScript

#### Task 3.4: Documentation Update
**Status:** `pending`
**Acceptance Criteria:**
- [ ] API documentation reflects new endpoints
- [ ] README updated with new features
- [ ] CHANGELOG entry for release
- [ ] Methodology documentation current

#### Task 3.5: Staging Deployment & QA
**Status:** `pending`
**Acceptance Criteria:**
- [ ] Deploy to staging environment
- [ ] Full regression test suite passes
- [ ] Load test on staging
- [ ] Stakeholder review signoff
- [ ] No P0/P1 bugs outstanding

#### Task 3.6: Production Deployment
**Status:** `pending`
**Acceptance Criteria:**
- [ ] Deploy during low-traffic window
- [ ] Verify all features work in production
- [ ] Monitor error rates for 24 hours
- [ ] Rollback plan documented and tested

---

## Deferred to Q2 2026

| Feature | Reason for Deferral | Estimated Effort |
|---------|---------------------|------------------|
| Interactive Visualizations | Complexity, not core value | 2 weeks |
| Advanced API Documentation | Need to stabilize API first | 1 week |
| User Accounts | No use case identified | 3 weeks |
| Community Stories | No consent infrastructure | 4 weeks |
| Prediction Alerts | Based on invalid methodology | N/A (cancelled) |
| State-Level Percentiles | Nice-to-have after national launch | 1 week |

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Data quality issues more extensive than expected | Medium | High | Week 1-2 buffer, manual review process |
| Database performance insufficient | Low | High | Connection pooling, indexes, caching |
| Accessibility target (90) not achievable | Medium | Medium | Hire accessibility consultant if needed |
| Scope creep from stakeholders | High | Medium | Frozen scope after Week 1 |
| Key team member unavailable | Low | High | Document all decisions, pair programming |

---

## Success Metrics

### Phase 0: Data Quality
- [ ] 0 prison/military tracts in top 100 resilient
- [ ] <5% of displayed tracts have population < 100

### Phase 1: Infrastructure
- [ ] API response time P95 < 200ms
- [ ] Zero downtime under 1000 concurrent users
- [ ] Cache hit rate > 80%

### Phase 2: UX
- [ ] Lighthouse Accessibility > 90
- [ ] Time to Interactive < 3s
- [ ] Data table works without JavaScript
- [ ] 0 keyboard traps

### Phase 3: Launch
- [ ] Error rate < 0.1%
- [ ] Uptime > 99.9%
- [ ] User feedback: "I can find what I need"

---

## Weekly Milestone Schedule

| Week | Phase | Key Deliverables | Exit Criteria |
|------|-------|------------------|---------------|
| 1 | Data Quality | Tract classification complete | Special populations identified |
| 2 | Data Quality | Filters deployed | API returns only residential tracts |
| 3 | Infrastructure | Database optimized | Queries < 100ms |
| 4 | Infrastructure | Caching active | Cache hit rate measurable |
| 5 | Infrastructure | Rate limiting + monitoring | Load test passes |
| 6 | Core UX | Homepage + /research | Research findings visible |
| 7 | Core UX | Data table foundation | SSR pagination works |
| 8 | Core UX | Filters + accessibility | Keyboard nav complete |
| 9 | Core UX | Map integration | Bidirectional sync works |
| 10 | Launch Prep | Audits + deployment | Production live |

---

## Appendix A: File Change Manifest

### New Files to Create
```
src/routes/(standard)/research/+page.svelte
src/routes/(standard)/research/+page.server.ts
src/routes/(standard)/data/+page.svelte
src/routes/(standard)/data/+page.server.ts
src/lib/components/data/DataTable.svelte
src/lib/components/data/FilterBar.svelte
src/lib/components/data/Pagination.svelte
src/lib/components/research/PaperCard.svelte
src/lib/components/research/FindingCard.svelte
src/lib/server/middleware/ratelimit.ts
src/lib/server/middleware/cache.ts
migrations/20250130_add_tract_type.sql
migrations/20250130_add_indexes.sql
migrations/20250130_create_state_aggregates.sql
```

### Existing Files to Modify
```
src/routes/(standard)/+page.svelte          # Homepage messaging
src/routes/api/tracts/+server.ts            # Add filtering
src/routes/api/tracts/[fips]/+server.ts     # Add filtering
src/lib/server/db/queries.ts                # New query functions
src/lib/components/Map.svelte               # Popup improvements
src/hooks.server.ts                         # Caching headers
src/app.html                                # Skip links
```

---

## Appendix B: Database Schema Changes

```sql
-- Migration 001: Add tract classification
ALTER TABLE tracts ADD COLUMN tract_type TEXT DEFAULT 'residential';
ALTER TABLE tracts ADD COLUMN is_residential BOOLEAN DEFAULT TRUE;

-- Migration 002: Add performance indexes
CREATE INDEX CONCURRENTLY idx_tracts_state_score ON tracts(state_abbr, resilience_score DESC);
CREATE INDEX CONCURRENTLY idx_tracts_burden ON tracts(burden_score);
CREATE INDEX CONCURRENTLY idx_tracts_population ON tracts(population);
CREATE INDEX CONCURRENTLY idx_tracts_residential ON tracts(is_residential) WHERE is_residential = TRUE;

-- Migration 003: State aggregates materialized view
CREATE MATERIALIZED VIEW state_aggregates AS
SELECT
  state_abbr,
  COUNT(*) as tract_count,
  SUM(population) as total_population,
  AVG(resilience_score) as avg_resilience,
  AVG(burden_score) as avg_burden,
  STDDEV(resilience_score) as std_resilience,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY resilience_score) as median_resilience,
  MIN(resilience_score) as min_resilience,
  MAX(resilience_score) as max_resilience
FROM tracts
WHERE is_residential = TRUE
GROUP BY state_abbr;

CREATE UNIQUE INDEX ON state_aggregates(state_abbr);

-- Migration 004: Score histogram buckets
CREATE MATERIALIZED VIEW score_distribution AS
SELECT
  WIDTH_BUCKET(resilience_score, -7, 6, 26) as bucket,
  COUNT(*) as count,
  SUM(population) as population
FROM tracts
WHERE is_residential = TRUE
GROUP BY bucket
ORDER BY bucket;
```

---

## Approval & Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Project Lead | | | |
| Engineering Lead | | | |
| Design Lead | | | |
| Accessibility Lead | | | |
| Stakeholder | | | |

---

**Document Version:** 1.0
**Last Updated:** December 30, 2025
**Next Review:** Week 2 (Phase 0 completion)
