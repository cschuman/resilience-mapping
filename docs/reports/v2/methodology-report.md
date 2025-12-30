# Health Resilience Mapping: Methodology Report

**Version 2.0 | December 2025**
**Revised following peer review**

---

## Executive Summary

This report details the statistical methodology underlying the Health Resilience Mapping project, which analyzes health burden variation across 63,847 U.S. census tracts (after population filtering) representing 219.8 million Americans. The methodology employs z-score standardization to create comparable burden metrics. Following rigorous peer review, we provide an honest assessment of strengths, limitations, and validity concerns.

**Methodology Grade: C- (Significant Limitations)**

---

## 1. Data Sources and Coverage

### 1.1 Primary Data Sources

| Source | Year | Coverage | Variables |
|--------|------|----------|-----------|
| CDC PLACES | 2023 | Tract-level health estimates | 29 health measures (model-based) |
| USDA Food Access Research Atlas | 2019 | Food desert classifications | LILA indicators, vehicle access |
| U.S. Census Bureau | 2020 | Population demographics | Total population, group quarters |
| American Community Survey | 2019-2023 | Socioeconomic indicators | Income, education, housing |

### 1.2 Critical Data Limitation: Temporal Misalignment

**The 4-year gap between FARA (2019) and PLACES (2023) spans the COVID-19 pandemic.** This temporal misalignment introduces substantial confounding:
- Food access patterns changed dramatically during COVID-19
- Healthcare utilization was disrupted
- Residential mobility shifted
- Over 1 million Americans died, disproportionately in high-burden areas

We cannot assume 2019 food access conditions predict 2023 health outcomes.

### 1.3 Sample Construction

| Step | Tracts | Population | Rationale |
|------|--------|------------|-----------|
| Initial universe | 72,531 | — | Census Bureau |
| Matched to PLACES | 68,170 | — | 94% match rate |
| Excluded >20% group quarters | 67,892 | — | Remove institutional populations |
| **Excluded population < 500** | **63,847** | **219.8M** | **Reliability threshold (NEW)** |

**Population Filter Justification:**
Per Census Bureau guidelines, tracts below 500 population produce unreliable estimates (Federal Register, 2018). CDC recommends minimum 50 adult population for PLACES estimates. We applied a 500-person threshold as a conservative reliability standard.

**Critical Note:** This exclusion is non-random. Excluded tracts include:
- Sparsely populated rural areas
- Recently depopulated industrial zones
- Areas with high transient populations

---

## 2. Score Construction Methodology

### 2.1 Health Burden Index

The composite health burden index is calculated as the mean z-score across five health outcomes:

- Obesity prevalence (BMI ≥30)
- Type 2 Diabetes prevalence
- Coronary Heart Disease prevalence
- Hypertension prevalence
- Physical Inactivity rate

**Internal consistency:** Cronbach's α = 0.87

**Limitation:** High alpha suggests the five components are highly collinear and may reflect a single underlying factor rather than distinct constructs.

### 2.2 Resilience Score Calculation

Resilience scores are calculated using OLS regression with state fixed effects:

```
Burden_i = β₀ + β₁LILA_i + β₂LowIncome_i + β₃Rural_i + β₄NoVehicle_i + State_FE + ε_i
```

The resilience score is the inverted standardized residual:

```
Resilience_i = -1 × (ε_i - mean(ε)) / SD(ε)
```

### 2.3 CRITICAL VALIDITY CONCERN: Tautological Construct

**The burden-resilience correlation is r = -0.72.**

This strong correlation is **partially mechanical**, not purely empirical. By definition:

> Resilience = "How much lower is your health burden than predicted by our model"

The residuals from regression are not orthogonal to the outcome variable—they capture unexplained variance in burden. We are effectively measuring one construct (health burden) twice and calling the unexplained portion "resilience."

**Implication:** The "resilience score" may be better described as **"Unexplained Burden Variance"** rather than an independent protective construct.

**What would establish construct independence:**
1. External validation against outcomes not used in construction (mortality, hospitalizations)
2. Demonstrating resilience predicts future health trajectories independent of current burden
3. Identifying specific protective factors that explain the residual variance

---

## 3. Distribution Properties

### 3.1 Observed Distribution

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Mean | 0.0000 | By design |
| Standard Deviation | 1.0000 | By design |
| Median | 0.0281 | Slight positive skew |
| Range | -6.84 to +5.22 | 12.06 SD |
| IQR | 1.1570 | Compressed vs. theoretical |

### 3.2 The 12 SD Range: Red Flag, Not Badge of Honor

The observed range of 12.06 SD is **wider than expected** for a sample of 63,847 observations. Under normality, we would expect maximum ~4.5 SD on each side (~9 SD total range).

**This suggests:**
1. Heavy tails / outliers driven by data artifacts
2. Heteroscedasticity across subpopulations
3. Measurement error in PLACES model-based estimates

**After population filtering:** The most extreme values moderated, but the range remains wider than theoretically expected.

### 3.3 Age Standardization Limitation

**Critical finding from CDC documentation:**

> "Age-adjusted estimates are only available at the county and place-level. We don't provide age-adjusted prevalence estimates at census tract and ZCTA levels."
> — CDC PLACES Methodology

**Implication:** Our tract-level regional comparisons are **NOT age-standardized**. Regional differences may partially reflect age structure rather than underlying health disparities. Southern states have older populations; this confounds burden comparisons.

---

## 4. Validity Assessment

### 4.1 What We Can Validate

| Aspect | Evidence | Assessment |
|--------|----------|------------|
| Distribution shape | Approximately normal with heavy tails | Acceptable |
| Sample size | n = 63,847 | Excellent power |
| Geographic coverage | 50 states + DC | Comprehensive |
| Internal consistency | α = 0.87 | High (possibly too high) |

### 4.2 What We Cannot Validate

| Aspect | Problem | Required Fix |
|--------|---------|--------------|
| Construct independence | r = -0.72 with burden | External validation needed |
| Predictive validity | No outcome data | Link to mortality (CDC WONDER) |
| Temporal validity | 4-year data gap | Obtain contemporaneous data |
| Age adjustment | Not available at tract level | Use county-level for validation |

### 4.3 Uncertainty Quantification: NOT DONE

CDC PLACES provides 95% confidence intervals for tract estimates. **We did not propagate this uncertainty through our analysis.**

This is a significant omission. Tract-level prevalence estimates have margins of error potentially spanning 5-10 percentage points. Our burden rankings may be substantially driven by measurement noise rather than true differences.

**Required for future versions:** Bootstrap confidence intervals incorporating PLACES estimation uncertainty.

---

## 5. Honest Methodology Assessment

### 5.1 Revised Grade: C-

| Criterion | Grade | Justification |
|-----------|-------|---------------|
| Data Quality | C | Temporal misalignment, model-based estimates |
| Model Specification | D+ | Tautological resilience construct |
| Validity | D | No external validation |
| Uncertainty | F | No CI propagation |
| Documentation | B | Transparent about limitations |
| **Overall** | **C-** | Significant limitations acknowledged |

### 5.2 What This Methodology CAN Support

1. **Descriptive analysis:** Documenting geographic variation in health burden
2. **Hypothesis generation:** Identifying outlier communities for further investigation
3. **Replication:** Confirming known regional health patterns at finer resolution
4. **Advocacy:** Quantifying geographic health inequity for policy discussions

### 5.3 What This Methodology CANNOT Support

1. **Causal inference:** Cannot establish that place causes health outcomes
2. **Independent resilience measurement:** Current construct overlaps with burden
3. **Precise population risk estimates:** "67 million at risk" is arithmetic, not epidemiology
4. **Policy prescription:** Cannot determine what interventions would work

---

## 6. Comparison to Established Standards

### 6.1 CDC Social Vulnerability Index (SVI)

The CDC SVI has undergone formal validation (ATSDR, 2020):
- Correlates with disaster recovery outcomes
- Predicts COVID-19 mortality
- Externally validated against multiple outcome measures

**Our methodology lacks equivalent validation.**

### 6.2 County Health Rankings

County Health Rankings (Remington et al., 2015):
- Decades of refinement
- Transparent, replicable methodology
- External review process
- Annual updates with consistent methodology

**Our methodology is a single cross-sectional analysis without external review.**

---

## 7. Recommendations for Users

### 7.1 Appropriate Uses

- Identifying geographic areas for further investigation
- Generating hypotheses about protective factors
- Advocacy for regional health investment
- Baseline for longitudinal tracking (if methodology is repeated)

### 7.2 Inappropriate Uses

- Direct resource allocation based on "resilience" scores
- Claiming to understand what makes communities resilient
- Making causal claims about geography and health
- Treating burden scores as precise individual-level risk estimates

### 7.3 Required Caveats for Any Citation

Any use of these findings should note:
1. Resilience scores have not been externally validated
2. Tract-level estimates are not age-adjusted
3. 4-year temporal gap between data sources
4. Model-based estimates have substantial uncertainty
5. Cross-sectional design cannot establish causality

---

## 8. Path to Improved Validity

### 8.1 Immediate Improvements (Implemented in v2.0)

- [x] Population filter (n ≥ 500)
- [x] Honest methodology grade (C-)
- [x] Explicit uncertainty acknowledgment
- [x] Age standardization limitation noted

### 8.2 Required for Future Versions

| Enhancement | Data Needed | Timeline |
|-------------|-------------|----------|
| External validation | CDC WONDER mortality | 1-2 months |
| Uncertainty quantification | PLACES confidence intervals | 1 month |
| Age-adjusted comparison | County-level validation | 1 month |
| Longitudinal analysis | Historical PLACES (2020-2024) | 2-3 months |
| Construct independence | External protective factor data | 3-6 months |

---

## 9. References

1. CDC. (2023). PLACES: Local Data for Better Health. Methodology. https://www.cdc.gov/places/methodology/
2. NCHS. (2017). NCHS Data Presentation Standards for Proportions. Series 2, No. 200.
3. Federal Register. (2018). Census Tracts for the 2020 Census—Proposed Criteria. Vol. 83, No. 32.
4. ATSDR. (2020). CDC/ATSDR Social Vulnerability Index Validation White Paper.
5. Remington, P. L., et al. (2015). The County Health Rankings: Rationale and methods. *Population Health Metrics*, 13(1), 11.

---

**Document Control**

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Dec 30, 2025 | Initial release |
| 2.0 | Dec 30, 2025 | Post-peer review revision: Honest grade (C-), population filter, validity concerns |

**Contact:** research@odds.health

---

*This methodology report reflects an honest assessment following rigorous peer review. We acknowledge significant limitations and commit to addressing them in future work.*
