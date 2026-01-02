# Community Health Mapping Research Paper Series

## Overview

A series of 5 papers derived from the CDC PLACES-based Community Health Trajectory Prediction system. Each paper addresses a distinct question while contributing to a coherent research program.

---

## Paper 1: Spatial Synchrony, Not Contagion ✅ COMPLETE

**Title:** "Spatial Synchrony, Not Contagion: A Methodological Correction in Community Health Trajectory Prediction"

**Status:** Peer-reviewed and accepted (simulated panel review)

**File:** `docs/research/SPATIAL-CONTAGION-PAPER-REVISED.md`

**Key Finding:** The apparent "spatial contagion" in community health trajectories was an artifact of temporal data leakage. When spatial features are properly lagged, they add nothing to prediction. Communities exhibit spatial synchrony (changing together at the same time) but not predictive contagion (prior neighbor change predicting future focal change).

**Contribution:** Methodological correction demonstrating the importance of proper temporal alignment in spatial feature construction.

---

## Paper 2: Regression to the Mean in Small-Area Health Estimates ✅ PEER REVIEWED

**Title:** "Regression to the Mean in Small-Area Health Estimates: Why CDC PLACES-Based Trajectory Prediction Fails"

**Status:** Peer-reviewed and accepted (3 rounds, 4/4 reviewers Accept)

**Target Journal:** American Journal of Epidemiology

**Files:**
- `docs/research/PAPER-2-UNPREDICTABILITY-SCOPE.md`
- `app/analytics/trajectory_prediction/unpredictability_analysis_v2.py`

**Key Findings (validated through peer review):**
1. **Quintile gradient diagnostic of RTM**: Q1 r=-0.05 → Q5 r=-0.61 (12x stronger for extreme changes)
2. **Variance gradient confirms RTM**: Q1 var=0.020 → Q5 var=0.041 (doubles with extremity)
3. **Levels are 99.7% persistent** - healthy tracts stay healthy
4. **Classification is inherently unstable** - training on extreme changes = training on noise
5. **Geography explains 28% of variance** in change magnitude

**Primary Insight:** The F1=0.26 performance is caused by regression to the mean, not health dynamics. The quintile gradient (12x stronger reversion for extreme vs. moderate changes) is the diagnostic signature of RTM - true biological mean reversion would show uniform reversion regardless of magnitude.

**Policy Implications:**
- Avoid annual trajectory-based resource allocation (classify noise as signal)
- Use 3-5 year rolling averages for trend assessment
- Prioritize current burden levels over trajectory classifications
- Invest in reducing measurement error before building prediction systems

**Next Steps:** Write full manuscript for journal submission

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

## Paper 5: The Grocery Store Paradox ✅ DRAFT COMPLETE

**Title:** "The Grocery Store Paradox: Why Food Access Alone Cannot Heal Structurally Harmed Communities"

**Status:** Draft complete (January 2026)

**Target Journal:** American Journal of Public Health / Health Affairs

**File:** `docs/research/PAPER-5-PARADOX-STUDY.md`

**Key Findings:**
1. **7,102 paradox tracts identified**: Communities with good food access but poor health outcomes (>1 SD worse than predicted)
2. **Racial composition is strongest predictor**: 26.9% majority-Black vs. 3.7% in non-paradox (Cohen's d = 0.76)
3. **Historical redlining persists**: Paradox tracts 1.65x more likely to be in redlined areas (p < 0.0001)
4. **Social vulnerability concentrated**: 46.5% in highest SVI quartile (vs. 25% expected)
5. **Geographic clustering**: Chicago, Detroit, Cleveland, Philadelphia, Baltimore—cities with documented segregation histories

**Primary Insight:** The "paradox" is not paradoxical. These are communities that were systematically harmed by policy (redlining, disinvestment) and remain structurally disadvantaged. A grocery store cannot undo 90 years of cumulative harm.

**Policy Implications:**
- Food access is necessary but not sufficient
- Investment must be proportional to historical harm
- Single-factor interventions cannot address cumulative disadvantage
- Reparative frameworks may be more appropriate than ameliorative ones

**Data Sources Used:**
- CDC PLACES 2023
- USDA Food Access Research Atlas 2019
- American Community Survey 2022
- CDC Social Vulnerability Index 2022
- HOLC Redlining Maps (digitized)

**Limitations:**
- Cross-sectional design
- EPA EJSCREEN not available (environmental hazards not analyzed)
- 76% of within-paradox variance unexplained

**Next Steps:** Internal review, community input, journal submission

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

Paper 5 (Paradox Study) ← NEW
    └── Inverts the resilience question
    └── Uses same model infrastructure as Papers 1-4
    └── Connects to Paper 4's equity framing
    └── Strongest policy implications
```

---

## Publication Strategy

**Order of Submission:**

1. **Paper 1** (Spatial Synchrony) → Epidemiology / IJE
   - Ready for submission
   - Methodological correction, high value

2. **Paper 2** (RTM in Small-Area Estimates) → American Journal of Epidemiology
   - Ready for submission (passed 3 rounds peer review)
   - Novel finding: quintile gradient diagnostic of RTM

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
| Paper 2 | `unpredictability_analysis_v2.py` | Complete (peer-reviewed) |
| Paper 3 | Not yet created | Needed |
| Paper 4 | Not yet created | Needed |
| Paper 5 | `paradox_study.py`, `paradox_structural_analysis.py`, `paradox_svi_analysis.py`, `paradox_holc_analysis.py` | Complete |

---

## Timeline Estimate

| Paper | Analysis | Writing | Review | Total |
|-------|----------|---------|--------|-------|
| Paper 1 | Complete | Complete | Complete | **Ready** |
| Paper 2 | Complete | Complete | Complete | **Ready** |
| Paper 3 | 1 week | 1 week | 1 week | **3-4 weeks** |
| Paper 4 | 1 week | 1 week | 1 week | **3-4 weeks** |
| Paper 5 | Complete | Complete | Pending | **Draft Ready** |

Papers 3 and 4 can be developed in parallel. Paper 5 is ready for internal review.

---

## Summary

This research program transforms a failed prediction system into five valuable contributions:

1. **Methodological warning** about temporal leakage in spatial features
2. **Theoretical insight** about mean reversion in community health
3. **Validated metric** for measuring community health burden
4. **Equity analysis** of burden distribution and prediction fairness
5. **Policy critique** showing that food access alone cannot heal structurally harmed communities

The finding that prediction fails is itself valuable—it prevents investment in systems that cannot work and redirects attention to current burden levels rather than unstable trajectory classifications.

Paper 5 (The Grocery Store Paradox) may be the most policy-relevant of the series: it directly challenges the assumption underlying billions of dollars in food access investment.
