# Community Health Mapping Research Paper Series

## Overview

A series of 4 papers derived from the CDC PLACES-based Community Health Trajectory Prediction system. Each paper addresses a distinct question while contributing to a coherent research program.

---

## Paper 1: Spatial Synchrony, Not Contagion ✅ COMPLETE

**Title:** "Spatial Synchrony, Not Contagion: A Methodological Correction in Community Health Trajectory Prediction"

**Status:** Peer-reviewed and accepted (simulated panel review)

**File:** `docs/research/SPATIAL-CONTAGION-PAPER-REVISED.md`

**Key Finding:** The apparent "spatial contagion" in community health trajectories was an artifact of temporal data leakage. When spatial features are properly lagged, they add nothing to prediction. Communities exhibit spatial synchrony (changing together at the same time) but not predictive contagion (prior neighbor change predicting future focal change).

**Contribution:** Methodological correction demonstrating the importance of proper temporal alignment in spatial feature construction.

---

## Paper 2: The Unpredictability of Community Health Trajectories 📊 ANALYSIS COMPLETE

**Title:** "Mean Reversion, Not Momentum: Why Community Health Trajectories Resist Prediction"

**Status:** Scope complete, initial analysis complete

**Files:**
- `docs/research/PAPER-2-UNPREDICTABILITY-SCOPE.md`
- `app/analytics/trajectory_prediction/unpredictability_analysis.py`

**Key Findings (from initial analysis):**
1. **Strong mean reversion** (r = -0.40 to -0.58 between adjacent year changes)
2. **Levels are 99.7% persistent** - healthy tracts stay healthy
3. **Changes exhibit mean reversion** - improvements followed by declines
4. **Geography explains 28% of variance** in change magnitude
5. **Classification is inherently unstable** due to mean reversion

**Primary Insight:** The F1=0.26 performance reflects mean reversion dynamics, not noise. Communities oscillate around stable equilibria rather than following persistent trajectories.

**Policy Implications:**
- Don't label communities as "improving" or "declining"
- Focus on current burden levels (stable, actionable)
- Use multi-year averages for trend assessment
- Target high-burden tracts, not "declining" ones

**Next Steps:** Write full paper manuscript (~5,000 words)

---

## Paper 3: Validating the Composite Health Burden Index 📋 SCOPED

**Title:** "Development and Validation of a Composite Health Burden Index for U.S. Census Tracts"

**Status:** Scope complete

**File:** `docs/research/PAPER-3-CHBI-VALIDATION-SCOPE.md`

**Research Questions:**
1. Does CHBI correlate with external measures (mortality, life expectancy)?
2. Do domain experts agree with the weighting scheme?
3. How robust is CHBI to alternative specifications?
4. Does higher CHBI predict worse outcomes?

**Validation Framework:**
- Construct validity (external correlates)
- Face validity (expert survey)
- Sensitivity analysis (alternative weights)
- Predictive validity (future outcomes)

**Data Needs:**
- CDC WONDER mortality data
- USALEEP life expectancy
- Expert survey (20-50 respondents)

**Next Steps:** Obtain external validation data, design expert survey

---

## Paper 4: Structural Determinants of Community Health Burden 📋 SCOPED

**Title:** "Racial Residential Segregation and Community Health Burden: A Tract-Level Analysis"

**Status:** Scope complete

**File:** `docs/research/PAPER-4-HEALTH-EQUITY-SCOPE.md`

**Research Questions:**
1. Association between racial composition and CHBI
2. How much is "explained" by socioeconomic factors?
3. Are trajectories equitably distributed?
4. Does our model perform equitably across community types?

**Analyses:**
- Descriptive epidemiology of burden distribution
- Hierarchical regression (race → SES → place → healthcare)
- Trajectory equity analysis
- Model equity audit

**Data Needs:**
- ACS demographics (race, income, poverty, housing)
- County-level segregation indices
- FQHC and hospital locations

**Next Steps:** Obtain ACS data, run equity analyses

---

## Paper Dependencies

```
Paper 1 (Spatial Synchrony)
    └── Establishes that spatial features don't help prediction

Paper 2 (Unpredictability)
    └── Explains WHY prediction fails (mean reversion)
    └── Builds on Paper 1's null finding

Paper 3 (CHBI Validation)
    └── Independent of Papers 1-2
    └── Validates the metric used in all papers

Paper 4 (Equity)
    └── Uses Paper 1's predictions for equity audit
    └── Uses Paper 2's findings to contextualize trajectories
```

---

## Publication Strategy

**Order of Submission:**

1. **Paper 1** (Spatial Synchrony) → Epidemiology / IJE
   - Ready for submission
   - Methodological correction, high value

2. **Paper 2** (Unpredictability) → Epidemiology / Milbank Quarterly
   - Needs manuscript writing
   - Novel finding (mean reversion), high policy value

3. **Paper 3** (CHBI Validation) → Health Services Research / Medical Care
   - Needs external data + expert survey
   - Can be written in parallel with Paper 2

4. **Paper 4** (Equity) → AJPH / J Health Disparities
   - Needs ACS data merge
   - Most policy-relevant, but needs foundation from earlier papers

---

## Code Assets

| Paper | Analysis Script | Status |
|-------|-----------------|--------|
| Paper 1 | `peer_review_fixes.py`, `round2_fixes.py` | Complete |
| Paper 2 | `unpredictability_analysis.py` | Complete |
| Paper 3 | Not yet created | Needed |
| Paper 4 | Not yet created | Needed |

---

## Timeline Estimate

| Paper | Analysis | Writing | Review | Total |
|-------|----------|---------|--------|-------|
| Paper 1 | Complete | Complete | Complete | **Ready** |
| Paper 2 | Complete | 1 week | 1 week | **2-3 weeks** |
| Paper 3 | 1 week | 1 week | 1 week | **3-4 weeks** |
| Paper 4 | 1 week | 1 week | 1 week | **3-4 weeks** |

Papers 3 and 4 can be developed in parallel.

---

## Summary

This research program transforms a failed prediction system into four valuable contributions:

1. **Methodological warning** about temporal leakage in spatial features
2. **Theoretical insight** about mean reversion in community health
3. **Validated metric** for measuring community health burden
4. **Equity analysis** of burden distribution and prediction fairness

The finding that prediction fails is itself valuable—it prevents investment in systems that cannot work and redirects attention to current burden levels rather than unstable trajectory classifications.
