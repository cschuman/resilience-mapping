# Health Resilience Mapping - Development Roadmap

> **Last Updated**: December 30, 2025
> **Status**: POST-WORKSHOP REALIGNMENT
> **Reference**: `docs/development/LINEAR_TICKETS_2025-12-30.md` for detailed tickets

---

## Executive Summary: Workshop Outcomes

On December 30, 2025, the full 8-person core team conducted an all-day strategic workshop. Key findings:

### Critical Assessment
| Domain | Workshop Verdict | Action Required |
|--------|-----------------|-----------------|
| **Data Quality** | Prison tracts in top rankings | BLOCKING - Must fix before growth |
| **Performance** | 2.3MB bundle, fails 3G test | P1 - Excludes poor communities |
| **Accessibility** | Keyboard trap, SR broken | P1 - Excludes disabled users |
| **Infrastructure** | No backups, no monitoring | P0 - One incident from disaster |
| **Community** | Zero consent, zero CAB | P0 - Extraction not partnership |

### Strategic Shift
1. **Table-first, map-second** — Accessibility drives architecture
2. **Data quality before growth** — Pause promotion until data validated
3. **Community Advisory Board** — $2,500/month, non-negotiable
4. **Performance budget** — Nothing ships without device testing
5. **Consent protocol** — No stories without explicit agreement

---

## PHASE 0: CRITICAL FOUNDATION (Now - Jan 13)

**All other work is blocked until Phase 0 complete.**

### 0.1 Data Quality Sprint
**Owner**: Miguel Santos | **Status**: IN PROGRESS

- [ ] Filter institutional populations (>10% group quarters)
- [ ] Re-run regression with corrected state fixed effects
- [ ] Manually validate top 100 communities
- [ ] Document all changes publicly in DATA_CORRECTIONS.md
- [ ] Update live database with corrected scores

**Why Blocking**: Top "resilient" community is 98.8% prison population. Publishing this discredits entire project.

### 0.2 Infrastructure Safety
**Owner**: Aaliyah Muhammad | **Status**: CRITICAL

- [x] Database backups configured (MUST BE TODAY)
- [ ] Health monitoring and alerts
- [ ] Staging environment
- [ ] Disaster recovery runbook
- [ ] Incident response plan

**Why Blocking**: No backups = complete data loss risk. "Hope is not a strategy."

### 0.3 Community Advisory Board Formation
**Owner**: Rev. Dr. Keisha Williams | **Status**: IN PROGRESS

- [ ] Recruit 5 members from mapped communities
- [ ] Establish stipend payments ($500/month each)
- [ ] Schedule first meeting (target: Jan 13)
- [ ] Draft governance charter
- [ ] Define veto powers and decision rights

**Why Blocking**: "Nothing about us without us." We're building for communities not at the table.

---

## PHASE 1: ACCESSIBILITY & PERFORMANCE (Jan 13 - Jan 27)

### 1.1 Accessible Data Table (PRIMARY)
**Owner**: David Chen-Williams + Jordan Park + Yuki Nakamura-Jackson

Build fully accessible data table as the PRIMARY interface. Map becomes progressive enhancement.

- [ ] Searchable, sortable table with all tracts
- [ ] Full keyboard navigation
- [ ] Screen reader optimized (ARIA, announcements)
- [ ] WCAG AA minimum, target AAA
- [ ] Virtual scrolling for 68K rows
- [ ] Server-side pagination

**Philosophy**: "I don't see your interface. I experience its soul." — David

### 1.2 Map Accessibility Fixes
**Owner**: David Chen-Williams

- [ ] Fix keyboard trap (Escape exits focus)
- [ ] Add screen reader announcements for interactions
- [ ] Focus management on tract selection
- [ ] High contrast mode toggle
- [ ] Reduced motion option

### 1.3 Performance Optimization
**Owner**: Jordan Park

**Target**: 3-second load on 3G, works on 5-year-old phones

- [ ] Reduce bundle to <500KB initial load
- [ ] Lazy load MapLibre (only on /map)
- [ ] Progressive map loading (placeholder → outline → details)
- [ ] Service worker for offline core data
- [ ] Test on real devices, not emulators

**The Jordan Test**: "On my grandma's phone, in Korea, on spotty 2G, with her glasses forgotten"

### 1.4 Performance Budget CI
**Owner**: Jordan Park + Aaliyah Muhammad

- [ ] Lighthouse CI in GitHub Actions
- [ ] Fail PR if performance budget exceeded
- [ ] Track metrics over time

**Budgets**:
- Performance score: >70
- First Contentful Paint: <2s
- Bundle size: <500KB gzipped

---

## PHASE 2: DESIGN SYSTEM & CONSENT (Jan 27 - Feb 10)

### 2.1 Community Consent Protocol
**Owner**: Keisha Williams + Amara Chen-Rodriguez + Legal

- [ ] Design consent flow (CAB review)
- [ ] Legal consent document
- [ ] Consent management in database
- [ ] Opt-out functionality
- [ ] Data deletion procedures

**The Keisha Test**: "Would I be proud to preach about this on Sunday?"

### 2.2 Design System V1
**Owner**: Yuki Nakamura-Jackson

Build accessible-first design system.

- [ ] Typography scale (min 16px body, proper hierarchy)
- [ ] Color system (all combinations pass WCAG AA)
- [ ] Spacing tokens
- [ ] Core components: Button, Card, Table, Form, Modal
- [ ] Storybook documentation with a11y audits

**Philosophy**: "Every gradient is political. Design is never neutral."

### 2.3 Stories Framework
**Owner**: Yuki + Keisha

- [ ] Story submission system (with consent)
- [ ] Community review workflow
- [ ] Photography guidelines (dignity, not poverty porn)
- [ ] Story display templates
- [ ] Moderation tools

**Requirement**: NO STORIES WITHOUT CONSENT. Empty page is better than extracted story.

---

## PHASE 3: LOCALIZATION & ADVOCACY (Feb 10 - Feb 24)

### 3.1 Spanish Localization
**Owner**: Yuki Nakamura-Jackson + Miguel Santos

- [ ] i18n framework setup (svelte-i18n)
- [ ] Extract all UI strings
- [ ] Professional translation
- [ ] Community review of translations
- [ ] Language switcher
- [ ] Persist preference

**Why**: 40% of food-insecure households speak Spanish primarily.

### 3.2 Advocacy Toolkit
**Owner**: Amara Chen-Rodriguez + Yuki

- [ ] Print-friendly tract reports (one-page PDF)
- [ ] Talking points generator
- [ ] Embeddable widgets
- [ ] Social share cards
- [ ] Citation generator

### 3.3 Policy Tracker
**Owner**: Amara Chen-Rodriguez

- [ ] Connect resilience data to policy outcomes
- [ ] Track legislation affecting mapped communities
- [ ] Success stories from advocacy

---

## PHASE 4: RESEARCH PLATFORM (Feb 24 - Mar 10)

### 4.1 Enhanced API
**Owner**: Marcus Thompson

- [ ] Rate limiting
- [ ] API keys for researchers
- [ ] Usage analytics
- [ ] Bulk data exports
- [ ] Attribution enforcement

### 4.2 Compare Tool
**Owner**: Jordan Park + Miguel Santos

- [ ] "Show me communities like mine"
- [ ] Multi-tract comparison view
- [ ] Demographic filtering
- [ ] Exportable comparisons

### 4.3 Overlay Layers
**Owner**: Miguel Santos

- [ ] Churches/faith institutions
- [ ] FQHCs and clinics
- [ ] Farmers markets
- [ ] Food banks
- [ ] Environmental justice data (EPA)

---

## PHASE 5: COMMUNITY OWNERSHIP (Mar 10 - Ongoing)

### 5.1 Community Data Dashboards
- [ ] Each consenting community gets own page
- [ ] Community-controlled content
- [ ] Local data they choose to share
- [ ] Their stories, their way

### 5.2 Ownership Transfer Framework
- [ ] Legal structure for community ownership
- [ ] Technical handoff documentation
- [ ] Sustainability plan
- [ ] Target: Community ownership by 2027

---

## Quality Gates

### Before Any Growth/Marketing
- [x] Platform deployed and accessible
- [ ] Data quality issues resolved (institutional filter)
- [ ] WCAG AA compliance verified
- [ ] Community Advisory Board operational
- [ ] Community consent obtained (min 10)
- [ ] Legal review completed
- [ ] Load testing passed (100x current traffic)

### Before Community Story Launch
- [ ] Consent protocol approved by CAB
- [ ] Legal review of consent documents
- [ ] 5 pilot communities with signed consent
- [ ] Story moderation workflow tested
- [ ] Harm assessment process documented

---

## Decision Framework

Per team charter, decisions follow weighted voting:

### Technical Decisions
Marcus (35%) + Aaliyah (25%) + Miguel (15%) + Jordan (10%) + Others (15%)

### Design Decisions
Yuki (40%) + David (20%) + Jordan (15%) + Keisha (10%) + Amara (10%) + Marcus (5%)

### Community Decisions
**Keisha (60%) + VETO POWER** + Amara (10%) + David (10%) + Others (20%)

### Keisha's Veto
Rev. Dr. Keisha Williams holds absolute veto on any decision that could harm communities. This has never been exercised but is non-negotiable.

---

## Team Tensions (Healthy Conflict)

| Tension | Resolution Approach |
|---------|---------------------|
| Jordan (ship fast) ↔ Aaliyah (ship safe) | Feature flags + gradual rollouts |
| Amara (narrative window) ↔ Keisha (community timeline) | Community milestones in sprints |
| Yuki (visual beauty) ↔ David (universal access) | Co-design from start, user testing settles |
| Marcus (over-engineer) ↔ Jordan (under-test) | Clear SLAs and performance budgets |

---

## Success Metrics

### Technical Metrics
- [ ] Lighthouse Performance: >70 (currently 34)
- [ ] Lighthouse Accessibility: >90 (currently 67)
- [ ] P99 latency: <200ms
- [ ] Uptime: 99.9%
- [ ] Zero data loss incidents

### Community Metrics
- [ ] Advisory Board: 5 members, monthly meetings
- [ ] Consented communities: 10 by March
- [ ] Community feedback sessions: Monthly
- [ ] Harm reports: Zero

### Impact Metrics
- [ ] Policy citations: 5+
- [ ] Academic citations: 10+
- [ ] Journalist embeds: 20+
- [ ] Community advocacy uses: 50+

---

## Team Principles (Workshop Reaffirmed)

1. **"Downtime equals harm"** — System reliability is moral imperative
2. **"Data without dignity is violence"** — Respectful representation
3. **"Performance is justice"** — Slow sites exclude poor communities
4. **"Nothing about us without us"** — Community ownership of narratives
5. **"Every bug is someone's hungry night"** — Technical failures have human costs
6. **"Table-first, map-second"** — Accessibility drives architecture

---

## Calendar View

```
December 2025
├── Dec 30: Workshop complete, roadmap realigned
├── Dec 30: Database backups (AALIYAH - TODAY)
└── Dec 31: Data quality sprint begins

January 2025
├── Week 1 (Jan 1-5): Institutional filter + monitoring
├── Week 2 (Jan 6-12): Validation + CAB recruitment
├── Jan 13: CAB first meeting, Sprint 2 begins
├── Week 3-4 (Jan 13-26): Accessibility + performance sprint
└── Jan 27: Design system sprint begins

February 2025
├── Week 5-6 (Jan 27 - Feb 9): Design system + consent protocol
├── Feb 10: Localization sprint begins
├── Week 7-8 (Feb 10-23): Spanish + advocacy toolkit
└── Feb 24: Research platform sprint begins

March 2025
├── Week 9-10 (Feb 24 - Mar 9): API + compare + overlays
├── Mar 10: Community ownership phase begins
└── Mar 31: Original launch target (now: "ready when ready")
```

---

## Contributors Welcome

### Expertise Sought
- Spatial statisticians (validate methodology)
- Public health researchers (ground truth findings)
- Accessibility specialists (audit and improve)
- Community organizers (connect us to communities)
- Policy analysts (translate data to action)
- Translators (Spanish, other languages)

### How to Contribute
1. Read this roadmap
2. Check open issues on GitHub
3. Join community call (schedule TBD)
4. Propose changes via PR

---

*Last Updated: December 30, 2025*
*Previous Version: December 24, 2025*
*Workshop Transcript: Available on request*
