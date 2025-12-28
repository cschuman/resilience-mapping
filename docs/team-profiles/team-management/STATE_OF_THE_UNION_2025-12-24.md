# State of the Union: Health Resilience Mapping Platform
## Leadership Team Deep Dive - December 24, 2025

**Status**: CRITICAL PIVOT REQUIRED
**Decision**: Unanimous consensus to fix data quality before platform launch
**Original Target**: March 31, 2025 (missed)
**Revised Target**: Tiered launch after data quality sprint

---

## Executive Summary

After comprehensive analysis by all 8 core leadership team members, we have identified **catastrophic data quality issues** that must be resolved before any public launch. The team unanimously agrees:

1. **Fix data first** - The state fixed effects bug invalidates all 68,170 resilience scores
2. **Archive Go backend** - Transition fully to approved Supabase/Vercel/Next.js stack
3. **Build community trust** - No community featured without explicit consent
4. **Tiered launch** - Research site first, Stories and Policy sites follow with consent

---

## Critical Data Issues Identified

### TIER 1: Launch Blocking (Must Fix Immediately)

| Issue | Severity | Location | Impact |
|-------|----------|----------|--------|
| State Fixed Effects Bug | CATASTROPHIC | `app/backend/expected.go:77-82` | ALL resilience scores wrong |
| Institutional Contamination | CRITICAL | 498 tracts | Prisons classified as "resilient communities" |
| Census Boundary Mismatch | HIGH | Data pipeline | Mixed 2010/2020 definitions, no crosswalk |

### TIER 2: Must Address Before Wide Release

| Issue | Severity | Impact |
|-------|----------|--------|
| Temporal Misalignment | HIGH | 4-year gap (FARA 2019 → PLACES 2023) spans COVID |
| Confidence Interval Width | MEDIUM | Wide CIs in small populations not weighted |
| Racial Disparity Pattern | SEVERE | 69% resilient=white, 61% vulnerable=Black |

---

## Leadership Perspectives Summary

### Amara Chen-Rodriguez (Product Lead, 35% Product Weight)
**Position**: Fix data before shipping. "Data without dignity is violence."

Key points:
- Cannot ship knowing our "resilient" tracts include prisons
- Two-week data sprint required before platform work
- Reframe from 1,059 communities to ~400 validated communities
- Legal and reputational risk of launching with known bugs is catastrophic

**Recommendation**: 2-week data quality sprint, then 6-week platform build

---

### Marcus Thompson (Technical Architect, 35% Architecture Weight)
**Position**: Archive Go backend, commit to approved stack, fix regression bug first.

Key points:
- State FE bug uses wrong index - loop variable `i` used for both stateList AND burdened array
- Go backend has zero deployment path, zero unit tests
- Supabase data import works - that's our foundation
- Port statistical model to Python where analytics suite lives

**Recommendation**: Fix bug (1 day), archive Go code, build fresh on Next.js/Supabase

---

### Miguel Santos (Data Infrastructure, 30% Data Weight)
**Position**: Five-alarm fire. Data quality issues invalidate core findings.

Key points:
- State FE bug: "ALL 68,170 resilience scores are potentially wrong"
- Institutional contamination: Top "resilient" tract is 98.8% prison
- Every bug systematically biases toward white communities
- 0/15 validation tests currently passing
- Estimated 40 working days to fully clean and validate

**Recommendation**: Cannot launch. Full data quality audit required.

---

### Aaliyah Muhammad (DevOps/SRE, 30% Launch Weight)
**Position**: Original March 31 was unrealistic. Zero infrastructure was deployed.

Key points:
- No Vercel deployment, no Fly.io services, no monitoring at time of analysis
- 1 test file with 8 skeleton tests (doesn't compile)
- Architecture "approved" ≠ architecture "deployed"

**Recommendation**: Phased launch after data quality resolved

---

### Keisha Williams (Community Trust, 60% Community Weight, VETO Power)
**Position**: Immediate pause. No communities have consented.

Key points:
- Zero of 1,059 communities know they're being featured
- Prison data as "resilient communities" is deeply problematic
- Racial disparity pattern could perpetuate harm
- "I would not be able to preach about this project with a clear conscience"

**Recommendation**: PAUSE. Form Community Advisory Board. Pilot with 5 communities before any launch.

**Veto Status**: RESERVED - will exercise if data quality and consent conditions not met

---

## Strategic Direction: Unanimous Consensus

### What We're Doing

```
PHASE 0: DATA QUALITY (Weeks 1-2) ← BLOCKING
├── Fix state fixed effects bug (Day 1)
├── Filter institutional populations (Days 2-3)
├── Re-run analysis with clean data (Days 4-7)
├── Validate top 100 communities (Week 2)
└── Get research team sign-off

PHASE 1: COMMUNITY TRUST (Weeks 1-6) ← PARALLEL
├── Form Community Advisory Board (Week 2)
├── Pilot engagement with 5 communities (Weeks 3-5)
├── Develop consent protocols (Week 4)
└── Legal review of consent framework (Week 5)

PHASE 2: TECHNICAL BUILD (Weeks 3-10)
├── Archive Go backend as reference
├── Build on Next.js/Supabase/Vercel stack
├── Three-site MVP
└── Performance/Accessibility/Security audits

PHASE 3: TIERED LAUNCH
├── Research site (aggregate data only)
├── Stories site (consented communities)
└── Policy site (full platform)
```

### What We're NOT Doing

- ❌ Keeping Go backend "just in case"
- ❌ Building dual systems
- ❌ Launching with known data bugs
- ❌ Featuring communities without consent
- ❌ Rushing launch with broken data

---

## The State Fixed Effects Bug

### Location
`/Users/corey/Projects/resilience-mapping-go/app/backend/expected.go` lines 77-82

### The Problem
```go
// BUGGY CODE:
for i:=1; i<len(stateList); i++ {
    if burdened[i][bh("StateAbbr")] == stateList[i] {  // BUG: uses i for BOTH
        x = append(x, 1.0)
    } else {
        x = append(x, 0.0)
    }
}
```

The loop variable `i` is used for two different purposes:
1. Index into `stateList` (correct)
2. Index into `burdened` array (WRONG - should be outer loop's row index)

### Impact
- Assigns state fixed effects incorrectly
- Corrupts OLS regression coefficients
- ALL resilience scores based on wrong predictions
- We're identifying the wrong communities as outliers

### Fix Required
Port to Python or fix the Go code to use the correct row index for the burdened array.

---

## Institutional Population Contamination

### The Numbers
- 498 LILA tracts have >20% group quarters population
- Top "resilient" tract: Mecosta County, MI - 98.8% group quarters (prison)
- Multiple 100% institutional tracts in dataset

### Why This Matters
- Prisons have controlled institutional food service - not "community resilience"
- College dorms have mandatory meal plans - not food desert survival
- Military bases have institutional food provision - not community health

### Fix Required
Filter tracts with >10% group quarters population from "community" analysis.

---

## Revised Timeline

| Phase | Duration | Deliverable | Owner |
|-------|----------|-------------|-------|
| Data Quality Sprint | 2 weeks | Clean, validated community list | Miguel |
| Community Trust Building | 6 weeks | 10 consenting communities | Keisha |
| Technical Foundation | 4 weeks | Monorepo, infrastructure, core features | Marcus |
| Platform MVP | 4 weeks | Three functional sites | Jordan |
| Testing & Hardening | 2 weeks | Audits passed, load tested | Aaliyah |
| **Research Site Launch** | TBD | Aggregate data, methodology | Amara |
| **Stories Site Launch** | TBD+2wks | Consented community stories | Keisha |
| **Policy Site Launch** | TBD+4wks | Full platform | Amara |

---

## Success Criteria

### Before ANY Launch
- [ ] State fixed effects bug fixed and validated
- [ ] Institutional populations filtered (<10% group quarters)
- [ ] Top 100 resilient communities manually validated
- [ ] Racial disparity analysis documented and addressed
- [ ] At least 10 communities with explicit consent
- [ ] Community Advisory Board operational
- [ ] Legal review completed

### Quality Gates
- [ ] 80% test coverage on statistical model
- [ ] WCAG AA accessibility compliance (AAA target)
- [ ] 3-second load time on 3G
- [ ] Security audit passed
- [ ] Disaster recovery tested

---

## Decision Accountability

| Decision Area | Primary Owner | Veto Power |
|--------------|---------------|------------|
| Architecture | Marcus (35%) | Aaliyah (reliability) |
| Product | Amara (35%) | - |
| Data | Miguel (30%) | Keisha (if harmful) |
| Community | Keisha (60%) | Always |
| Launch | Aaliyah (30%) | Keisha (community harm) |

---

## Files Referenced

- `app/backend/expected.go` - State fixed effects bug location
- `app/analytics/investigate_anomalies.py` - Data quality investigation
- `docs/development/ROADMAP.md` - Technical roadmap (needs update)
- `docs/IMPLEMENTATION_PLAN.md` - Timeline (needs update)
- `docs/team-profiles/team-management/ARCHITECTURE_REVIEW_MEETING.md` - Approved architecture
- `docs/team-profiles/team-management/DECISION_FRAMEWORK.md` - Voting weights

---

## Next Actions

### Immediate (This Week)
1. **Fix state FE bug** - Port to Python or correct Go code
2. **Filter institutional populations** - Add >10% group quarters filter
3. **Re-run analysis** - Generate new resilience scores
4. **Compare results** - Document changes from original findings
5. **Begin community outreach** - Keisha initiates conversations

### This document approved by:
- [ ] Amara Chen-Rodriguez (Product)
- [ ] Marcus Thompson (Architecture)
- [ ] Keisha Williams (Community)
- [ ] Aaliyah Muhammad (DevOps)
- [ ] Miguel Santos (Data)

---

*"Every millisecond matters. Every pixel has purpose. Every query protects privacy."*

*Document created: December 24, 2025*
*Next review: January 7, 2026*
