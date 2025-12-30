# Linear Tickets: Workshop Outcomes
## December 30, 2025 | All-Day Team Workshop

---

## Epic 1: Data Quality Sprint (BLOCKING)
**Owner**: Miguel Santos
**Priority**: P0 - Critical
**Deadline**: January 13, 2025

### RESIL-001: Filter Institutional Populations
**Type**: Bug | **Priority**: P0 | **Points**: 5

**Description**:
Top "resilient" communities include tracts with >20% institutional population (prisons, dorms). Tract 47149041500 is 98.8% prison population - currently ranked #1.

**Acceptance Criteria**:
- [ ] Add group quarters filter to data pipeline (>10% threshold)
- [ ] Identify and document all affected tracts
- [ ] Re-run regression without contaminated tracts
- [ ] Update database with corrected scores
- [ ] Document exclusion criteria in methodology

**Technical Details**:
- File: `app/analytics/analyze_resilience.py`
- Data source: ACS table B26001 (Group Quarters Population)
- Filter logic: Exclude where `gq_population / total_population > 0.10`

**Labels**: `data-quality`, `blocking`, `regression`

---

### RESIL-002: Validate Top 100 Communities
**Type**: Task | **Priority**: P0 | **Points**: 8

**Description**:
After institutional filter is applied, manually validate top 100 resilient communities to ensure no other systematic issues.

**Acceptance Criteria**:
- [ ] Pull ACS demographic data for top 100 tracts
- [ ] Verify population counts are reasonable (not 50 people)
- [ ] Check for boundary anomalies (tracts crossing major features)
- [ ] Confirm health data source matches tract boundaries
- [ ] Document any additional exclusion criteria discovered

**Dependencies**: RESIL-001

**Labels**: `data-quality`, `validation`, `manual-review`

---

### RESIL-003: Document Data Quality Changes
**Type**: Documentation | **Priority**: P1 | **Points**: 3

**Description**:
Create public changelog documenting all data corrections and their impact on findings.

**Acceptance Criteria**:
- [ ] Write DATA_CORRECTIONS.md with full history
- [ ] Update README with data version information
- [ ] Add disclaimer to website about ongoing validation
- [ ] Create comparison table: old scores vs new scores for top 20

**Dependencies**: RESIL-001, RESIL-002

**Labels**: `documentation`, `transparency`

---

## Epic 2: Infrastructure Safety
**Owner**: Aaliyah Muhammad
**Priority**: P0 - Critical
**Deadline**: TODAY (Dec 30) for backups, January 6 for full epic

### RESIL-004: Configure Database Backups
**Type**: Bug | **Priority**: P0 | **Points**: 2

**Description**:
NO DATABASE BACKUPS CONFIGURED. Complete data loss is one incident away.

**Acceptance Criteria**:
- [ ] Enable point-in-time recovery on Fly Postgres
- [ ] Configure daily automated backups
- [ ] Test restore process with documentation
- [ ] Set up backup monitoring/alerts

**Commands**:
```bash
fly postgres backup create -a resilience-mapping-db
fly postgres backup list -a resilience-mapping-db
```

**Labels**: `infrastructure`, `critical`, `same-day`

---

### RESIL-005: Add Production Monitoring
**Type**: Feature | **Priority**: P1 | **Points**: 5

**Description**:
No visibility into production errors or performance. Flying blind.

**Acceptance Criteria**:
- [ ] Set up error tracking (Sentry or similar)
- [ ] Add performance monitoring (response times, error rates)
- [ ] Create dashboard for key metrics
- [ ] Configure alerts for error spikes and downtime
- [ ] Document runbook for common alerts

**Labels**: `infrastructure`, `observability`

---

### RESIL-006: Create Staging Environment
**Type**: Feature | **Priority**: P1 | **Points**: 3

**Description**:
Currently testing in production. Dangerous for a data platform.

**Acceptance Criteria**:
- [ ] Create `resilience-mapping-staging` Fly app
- [ ] Set up staging database with anonymized data
- [ ] Configure staging deployment pipeline
- [ ] Document staging vs production differences

**Labels**: `infrastructure`, `devops`

---

### RESIL-007: Disaster Recovery Plan
**Type**: Documentation | **Priority**: P1 | **Points**: 3

**Description**:
No documented process for recovery from incidents.

**Acceptance Criteria**:
- [ ] Write incident response runbook
- [ ] Document on-call rotation (even if just one person)
- [ ] Create communication templates for outages
- [ ] Test disaster recovery with tabletop exercise
- [ ] Define RTO (Recovery Time Objective) and RPO (Recovery Point Objective)

**Labels**: `infrastructure`, `documentation`, `reliability`

---

## Epic 3: Community Advisory Board
**Owner**: Rev. Dr. Keisha Williams
**Priority**: P0 - Critical
**Deadline**: January 13, 2025 (first meeting)

### RESIL-008: Recruit Advisory Board Members
**Type**: Task | **Priority**: P0 | **Points**: 5

**Description**:
Form 5-person Community Advisory Board from mapped communities with real decision-making power.

**Acceptance Criteria**:
- [ ] Identify 10 candidates from resilient communities
- [ ] Conduct outreach calls with each candidate
- [ ] Confirm 5 members (target: 3 faith leaders, 1 CHW, 1 advocate)
- [ ] Set up monthly stipend payments ($500/month each)
- [ ] Schedule first meeting within 2 weeks

**Budget**: $2,500/month ongoing

**Labels**: `community`, `governance`, `critical`

---

### RESIL-009: Draft Community Governance Charter
**Type**: Documentation | **Priority**: P1 | **Points**: 5

**Description**:
Document the role, authority, and processes of the Community Advisory Board.

**Acceptance Criteria**:
- [ ] Define CAB voting rights and veto powers
- [ ] Document meeting cadence and format
- [ ] Create decision escalation process
- [ ] Define relationship to technical team
- [ ] Get legal review of governance structure

**Labels**: `community`, `governance`, `documentation`

---

### RESIL-010: Build Consent Protocol
**Type**: Feature | **Priority**: P1 | **Points**: 8

**Description**:
Create system for communities to consent to being featured, control their data representation.

**Acceptance Criteria**:
- [ ] Design consent flow (UI/UX)
- [ ] Create legal consent document (lawyer review)
- [ ] Build consent management in database
- [ ] Implement opt-out functionality
- [ ] Document data deletion procedures

**Dependencies**: RESIL-009 (CAB should review)

**Labels**: `community`, `legal`, `feature`

---

## Epic 4: Accessibility Remediation
**Owner**: David Chen-Williams
**Priority**: P1 - High
**Deadline**: January 20, 2025

### RESIL-011: Build Accessible Data Table
**Type**: Feature | **Priority**: P1 | **Points**: 8

**Description**:
Create fully accessible data table as PRIMARY interface. Map becomes progressive enhancement.

**Acceptance Criteria**:
- [ ] Searchable/sortable table with all 68K tracts
- [ ] Full keyboard navigation
- [ ] Screen reader optimized (ARIA labels, announcements)
- [ ] Pass WCAG AA for tables (target AAA)
- [ ] Pagination accessible
- [ ] Column headers sortable via keyboard

**Technical Notes**:
- Consider TanStack Table for accessibility primitives
- Virtual scrolling for performance with 68K rows
- Server-side pagination for initial load

**Labels**: `accessibility`, `feature`, `a11y-critical`

---

### RESIL-012: Fix Map Keyboard Trap
**Type**: Bug | **Priority**: P1 | **Points**: 3

**Description**:
Users get trapped in map component - can't tab out. Critical accessibility violation.

**Acceptance Criteria**:
- [ ] Escape key exits map focus
- [ ] Tab moves to next focusable element
- [ ] Focus indicator visible at all times
- [ ] Document keyboard shortcuts in UI

**Labels**: `accessibility`, `bug`, `a11y-critical`

---

### RESIL-013: Add Screen Reader Announcements
**Type**: Feature | **Priority**: P1 | **Points**: 5

**Description**:
Map interactions produce no screen reader output. Blind users can't use core feature.

**Acceptance Criteria**:
- [ ] Announce tract selection ("Selected: Tract 12345 in Miami-Dade County")
- [ ] Announce resilience score on selection
- [ ] Announce navigation state ("Zoomed in to Florida")
- [ ] Live region for dynamic content updates
- [ ] Test with NVDA, JAWS, and VoiceOver

**Labels**: `accessibility`, `feature`

---

### RESIL-014: High Contrast Mode
**Type**: Feature | **Priority**: P2 | **Points**: 3

**Description**:
Low vision users struggle with current color scheme.

**Acceptance Criteria**:
- [ ] Add high contrast toggle in settings
- [ ] Persist preference in localStorage
- [ ] Respect prefers-contrast media query
- [ ] Test with color blindness simulators
- [ ] Ensure 7:1 contrast ratio in high contrast mode

**Labels**: `accessibility`, `feature`

---

### RESIL-015: WCAG Audit & Remediation
**Type**: Task | **Priority**: P1 | **Points**: 8

**Description**:
Full WCAG 2.1 AA audit with remediation of findings.

**Acceptance Criteria**:
- [ ] Run automated audit (axe-core, Lighthouse)
- [ ] Manual audit with screen reader
- [ ] Keyboard-only navigation test
- [ ] Document all findings
- [ ] Fix all Level A and AA issues
- [ ] Create accessibility statement page

**Labels**: `accessibility`, `audit`

---

## Epic 5: Performance Optimization
**Owner**: Jordan Park
**Priority**: P1 - High
**Deadline**: January 20, 2025

### RESIL-016: Reduce Initial Bundle Size
**Type**: Performance | **Priority**: P1 | **Points**: 5

**Description**:
Current bundle is 2.3MB uncompressed. Target: under 500KB initial load.

**Acceptance Criteria**:
- [ ] Analyze bundle with `rollup-plugin-visualizer`
- [ ] Lazy load MapLibre (only on /map route)
- [ ] Tree-shake unused code
- [ ] Implement route-based code splitting
- [ ] Target: <200KB first paint bundle

**Labels**: `performance`, `optimization`

---

### RESIL-017: Implement Progressive Map Loading
**Type**: Feature | **Priority**: P1 | **Points**: 5

**Description**:
Map shows nothing for 3+ seconds on slow connections. Need progressive experience.

**Acceptance Criteria**:
- [ ] Show placeholder/skeleton immediately
- [ ] Load US outline first (low-res)
- [ ] Load state boundaries second
- [ ] Load tract details on zoom
- [ ] Target: something visible in <500ms on 3G

**Labels**: `performance`, `ux`

---

### RESIL-018: Service Worker for Offline
**Type**: Feature | **Priority**: P2 | **Points**: 5

**Description**:
No offline capability. Communities with bad internet can't cache data.

**Acceptance Criteria**:
- [ ] Implement service worker with Workbox
- [ ] Cache static assets (CSS, JS)
- [ ] Cache API responses for viewed tracts
- [ ] Show offline indicator
- [ ] Allow offline viewing of previously loaded data

**Labels**: `performance`, `offline`, `feature`

---

### RESIL-019: Performance Budget CI
**Type**: DevOps | **Priority**: P2 | **Points**: 3

**Description**:
No automated checks for performance regressions.

**Acceptance Criteria**:
- [ ] Add Lighthouse CI to GitHub Actions
- [ ] Set performance budget thresholds
- [ ] Fail PR if budget exceeded
- [ ] Track performance over time

**Budgets**:
- Performance score: >70
- First Contentful Paint: <2s
- Time to Interactive: <4s
- Bundle size: <500KB

**Labels**: `performance`, `ci`, `devops`

---

## Epic 6: Design System Foundation
**Owner**: Yuki Nakamura-Jackson
**Priority**: P2 - Medium
**Deadline**: January 27, 2025

### RESIL-020: Typography System
**Type**: Design System | **Priority**: P2 | **Points**: 3

**Description**:
Create consistent typography scale with accessibility built in.

**Acceptance Criteria**:
- [ ] Define type scale (8-10 sizes)
- [ ] Set line heights for readability
- [ ] Ensure minimum 16px body text
- [ ] Create heading hierarchy components
- [ ] Document usage guidelines

**Labels**: `design-system`, `accessibility`

---

### RESIL-021: Color System
**Type**: Design System | **Priority**: P2 | **Points**: 5

**Description**:
Current colors are ad-hoc. Need system with contrast guarantees.

**Acceptance Criteria**:
- [ ] Define semantic color tokens (primary, secondary, success, warning, error)
- [ ] Define surface colors (backgrounds, cards)
- [ ] Ensure all combinations pass WCAG AA
- [ ] Document color usage in Storybook
- [ ] Create dark mode tokens (future)

**Labels**: `design-system`, `accessibility`

---

### RESIL-022: Component Library Foundation
**Type**: Design System | **Priority**: P2 | **Points**: 8

**Description**:
Build core component library with Storybook documentation.

**Acceptance Criteria**:
- [ ] Button component (variants, states, sizes)
- [ ] Card component
- [ ] Table component (accessible)
- [ ] Form inputs
- [ ] Modal/Dialog
- [ ] All components in Storybook with a11y checks

**Labels**: `design-system`, `components`

---

## Epic 7: Localization
**Owner**: Yuki Nakamura-Jackson + Miguel Santos
**Priority**: P2 - Medium
**Deadline**: February 10, 2025

### RESIL-023: Spanish Translation
**Type**: i18n | **Priority**: P2 | **Points**: 8

**Description**:
40% of food-insecure households speak Spanish primarily. We're excluding them.

**Acceptance Criteria**:
- [ ] Set up i18n framework (svelte-i18n or similar)
- [ ] Extract all UI strings
- [ ] Professional translation of all strings
- [ ] Community review of translations
- [ ] Language switcher in UI
- [ ] Persist language preference

**Labels**: `i18n`, `accessibility`, `equity`

---

## Epic 8: Export & Advocacy Tools
**Owner**: Amara Chen-Rodriguez + Yuki Nakamura-Jackson
**Priority**: P2 - Medium
**Deadline**: February 17, 2025

### RESIL-024: Print-Friendly Tract Reports
**Type**: Feature | **Priority**: P2 | **Points**: 5

**Description**:
Community organizers need printable reports for meetings.

**Acceptance Criteria**:
- [ ] One-page PDF report per tract
- [ ] Include key metrics, map snippet, context
- [ ] Print-optimized CSS
- [ ] Download button on tract detail page

**Labels**: `feature`, `advocacy`

---

### RESIL-025: Embeddable Widget
**Type**: Feature | **Priority**: P3 | **Points**: 8

**Description**:
Allow journalists and researchers to embed our map.

**Acceptance Criteria**:
- [ ] iframe embed code generator
- [ ] Configurable: state filter, zoom level, theme
- [ ] Track embeds for impact measurement
- [ ] Clear attribution requirements

**Labels**: `feature`, `distribution`

---

## Summary: Sprint Planning

### Sprint 1 (Dec 30 - Jan 13): Foundation
**Focus**: Data Quality + Infrastructure + CAB Formation

| Ticket | Owner | Points | Priority |
|--------|-------|--------|----------|
| RESIL-001 | Miguel | 5 | P0 |
| RESIL-002 | Miguel | 8 | P0 |
| RESIL-004 | Aaliyah | 2 | P0 |
| RESIL-005 | Aaliyah | 5 | P1 |
| RESIL-008 | Keisha | 5 | P0 |
| **Total** | | **25** | |

### Sprint 2 (Jan 13 - Jan 27): Accessibility + Performance
**Focus**: Make it work for everyone

| Ticket | Owner | Points | Priority |
|--------|-------|--------|----------|
| RESIL-011 | David + Jordan | 8 | P1 |
| RESIL-012 | David | 3 | P1 |
| RESIL-016 | Jordan | 5 | P1 |
| RESIL-017 | Jordan | 5 | P1 |
| RESIL-009 | Keisha | 5 | P1 |
| **Total** | | **26** | |

### Sprint 3 (Jan 27 - Feb 10): Design System + Consent
**Focus**: Foundation for scale

| Ticket | Owner | Points | Priority |
|--------|-------|--------|----------|
| RESIL-010 | Keisha + Legal | 8 | P1 |
| RESIL-020 | Yuki | 3 | P2 |
| RESIL-021 | Yuki | 5 | P2 |
| RESIL-022 | Yuki + Jordan | 8 | P2 |
| **Total** | | **24** | |

---

*Generated from All-Day Team Workshop, December 30, 2025*
