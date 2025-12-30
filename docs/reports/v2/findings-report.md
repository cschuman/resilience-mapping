# Health Resilience Mapping: Findings Report

**Version 2.0 | December 2025**
**Revised following peer review**

---

## Executive Summary

Analysis of 63,847 U.S. census tracts (population ≥ 500) representing 219.8 million Americans reveals geographic variation in health burden consistent with decades of established research on the Stroke Belt, Diabetes Belt, and Appalachian health disparities. This report presents descriptive findings with appropriate caveats about what can and cannot be concluded from cross-sectional ecological data.

### Key Numbers

| Metric | Value | Caveat |
|--------|-------|--------|
| Census tracts analyzed | 63,847 | After population filter |
| Population represented | 219.8 million | 67% of U.S. |
| Burden score range | -6.84 to +5.22 | Wider than expected |
| Burden-Resilience correlation | r = -0.72 | Raises construct validity concerns |

---

## 1. National Health Burden Distribution

### 1.1 Overall Distribution

The health burden metric demonstrates near-normal distribution:

- **Mean:** 0.00 (by design)
- **Standard deviation:** 1.00 (by design)
- **Range:** -6.84 to +5.22 (12.06 SD)

### 1.2 Population by Burden Category

| Burden Level | Score Range | Tracts | Population | % of Total |
|--------------|-------------|--------|------------|------------|
| Low burden | < -0.50 | 30,102 | 93.2M | 42.4% |
| Moderate burden | -0.50 to +0.50 | 28,163 | 101.1M | 46.0% |
| High burden | > +0.50 | 5,582 | 25.5M | 11.6% |

**Important Caveat:** These categories are arbitrary statistical thresholds, not clinically validated cutpoints. "High burden" means above +0.50 SD on our composite index—not a validated epidemiological risk category.

---

## 2. Regional Patterns: Replication of Known Disparities

### 2.1 Four-Region Comparison

| Region | Tracts | Population | Avg Burden | Std Dev |
|--------|--------|------------|------------|---------|
| **South** | 20,312 | 63.1M | **+0.30** | 1.09 |
| **Midwest** | 15,847 | 53.9M | **+0.16** | 1.04 |
| **Northeast** | 12,408 | 46.1M | **-0.17** | 0.91 |
| **West** | 15,280 | 56.7M | **-0.37** | 0.87 |

### 2.2 These Patterns Are Not Novel

**We must be transparent:** These regional findings replicate well-established geographic health patterns:

- **The Stroke Belt** has been documented since 1965 (Borhani, 1965; Howard et al., 2019)
- **The Diabetes Belt** was characterized by Barker et al. (2011) with 644 counties showing ≥11% prevalence
- **Appalachian health disparities** have been studied for decades (ARC, 2017)

Our contribution is **methodological and granular**—demonstrating these patterns persist at census tract level—not geographic discovery.

### 2.3 Age Standardization Caveat

**CDC PLACES tract-level estimates are NOT age-adjusted.** Regional differences may partially reflect age structure:
- Florida: 21% population over 65
- Colorado: 15% population over 65

Chronic disease prevalence increases dramatically with age. Some observed regional difference may be demographic, not health disparity.

---

## 3. State-Level Analysis

### 3.1 Highest Burden States

| State | Avg Burden | Std Dev | Population |
|-------|------------|---------|------------|
| West Virginia | +0.97 | 0.87 | 1.3M |
| Mississippi | +0.85 | 1.16 | 1.5M |
| Alabama | +0.75 | 1.22 | 3.0M |
| Arkansas | +0.65 | 1.01 | 1.9M |
| Louisiana | +0.55 | 1.22 | 2.6M |
| Ohio | +0.51 | 1.15 | 8.5M |

### 3.2 Lowest Burden States

| State | Avg Burden | Std Dev | Population |
|-------|------------|---------|------------|
| Colorado | -0.72 | 0.80 | 4.2M |
| Hawaii | -0.60 | 0.85 | 0.7M |
| Utah | -0.58 | 0.78 | 2.1M |
| Massachusetts | -0.44 | 0.90 | 5.6M |
| California | -0.42 | 0.84 | 29.7M |

### 3.3 Interpretation

These state patterns align with established literature:
- West Virginia's challenges reflect the opioid crisis, deindustrialization, and rural healthcare access—documented extensively in Appalachian health research
- Colorado's low burden reflects high education levels and health-conscious culture—not a novel finding

---

## 4. Geographic Clustering

### 4.1 Observed Clustering Extends Documented Patterns

Our analysis identifies clustering in regions previously characterized as:

- **Stroke Belt** (Southeastern states): Elevated stroke mortality documented since 1965
- **Diabetes Belt** (644 counties): Characterized by Barker et al. (2011)
- **Heart Failure Belt** (6 Southeastern states): Documented by Mujib et al. (2011)

**We hypothesize** a composite "Chronic Disease Burden Belt" extending through Appalachia and the Deep South, but this requires validation against mortality data before being treated as an established geographic entity.

### 4.2 Clustering Caveats

**We cannot distinguish between:**
1. **Place effects:** Living in a community causes health outcomes
2. **Selection effects:** People with health characteristics sort into communities
3. **Confounding:** Unmeasured factors drive both location and health

The Moving to Opportunity experiment (Katz et al., 2001) demonstrated that randomized relocation improves mental health, suggesting place effects exist. But our observational data cannot estimate relative contributions.

---

## 5. Statistical Outlier Communities

### 5.1 Identification of Outliers

We identified tracts with substantially better or worse outcomes than predicted by our model. These represent **statistical outliers requiring investigation**, not validated "resilient communities."

### 5.2 What Outliers Mean

**High-resilience outliers** (e.g., WV tract with burden -0.96 despite state average +0.97) represent:
- Possible measurement error in model-based estimates
- Unmeasured protective factors (healthcare access, social capital)
- Statistical regression to mean
- Genuine positive deviance warranting investigation

**We do not know which explanation applies.** Claiming these communities have "protective factors" without investigation is speculation.

### 5.3 Positive Deviance Methodology Requirements

Per Bradley et al. (2009), validating outliers requires:
1. **Confirm persistence:** Do outliers remain outliers across multiple years?
2. **Match and contrast:** Compare to similar communities without positive outcomes
3. **Qualitative investigation:** Ask communities what makes them different
4. **Hypothesis testing:** Verify identified factors through controlled comparison

**We have completed step 1 (identification). Steps 2-4 remain as future research.**

---

## 6. The Burden-Resilience Relationship

### 6.1 Correlation

**Pearson correlation:** r = -0.72 (p < 0.001)

### 6.2 Construct Validity Concern

This strong correlation raises questions about whether we are measuring two independent constructs:

- **If resilience = inverse of adjusted burden:** The correlation is mathematical, not empirical
- **Coefficient of determination:** r² = 0.52 means 52% shared variance
- **Implication:** "Resilience" may largely measure the same thing as "burden"

**Honest interpretation:** We have created a composite burden index and identified tracts that deviate from predictions. The deviation could reflect protective factors, measurement error, or model misspecification. External validation is required.

---

## 7. What We Can and Cannot Conclude

### 7.1 Supported Conclusions

| Conclusion | Evidence Level |
|------------|----------------|
| Health burden varies geographically | Strong (replicates known patterns) |
| South and Midwest show elevated burden | Strong (consistent with 60 years of research) |
| Some tracts deviate from predictions | Moderate (statistical finding) |
| Tract-level analysis provides finer resolution | Moderate (methodological contribution) |

### 7.2 Unsupported Conclusions

| Claim | Why Unsupported |
|-------|-----------------|
| ~~"5-7 years life expectancy difference"~~ | No citation; we did not link to mortality data |
| ~~"67 million Americans at risk"~~ | Arithmetic, not validated risk estimate |
| ~~"Geography is destiny"~~ | Deterministic framing unsupported by cross-sectional data |
| ~~"Resilient communities have protective factors"~~ | Speculation without investigation |
| ~~"Burden Belt" as novel discovery~~ | Extends documented Stroke/Diabetes Belt |

---

## 8. Geographic Life Expectancy (From External Literature)

Since we did not link to mortality data, we cite established findings:

| Finding | Source |
|---------|--------|
| 20-year county gap (Summit CO: 86.8 vs Oglala Lakota SD: 66.8) | Dwyer-Lindgren et al., 2017, JAMA Intern Med |
| 14.6-year gap between top and bottom 1% income | Chetty et al., 2016, JAMA |
| 5-year gap for low-income men (NYC vs Gary, IN) | Chetty et al., 2016, JAMA |
| Rural-urban gap widened 0.4→3.5 years (1971-2017) | Singh & Siahpush, PMC |

**These are external findings, not derived from our analysis.**

---

## 9. Limitations

### 9.1 Data Limitations

1. **Temporal misalignment:** 4-year gap between FARA (2019) and PLACES (2023) spans COVID-19
2. **Model-based estimates:** CDC PLACES uses small-area estimation, not direct measurement
3. **No age adjustment:** Tract-level estimates are crude, not age-standardized
4. **67% coverage:** Excluded tracts may differ systematically

### 9.2 Methodological Limitations

1. **Tautological construct:** Resilience correlates r=-0.72 with burden (construct overlap)
2. **No external validation:** Scores not validated against mortality or utilization
3. **Cross-sectional design:** Cannot establish causality
4. **No uncertainty quantification:** Did not propagate PLACES confidence intervals

### 9.3 Interpretation Limitations

1. **Ecological fallacy:** Tract-level patterns may not apply to individuals
2. **Selection vs. place effects:** Cannot distinguish with observational data
3. **Omitted variables:** Unmeasured confounders may drive patterns

---

## 10. Implications

### 10.1 For Research

1. **Hypothesis generation:** Outlier tracts warrant mixed-methods investigation
2. **Validation needed:** Link burden scores to mortality data (CDC WONDER)
3. **Longitudinal analysis:** Track trajectories using historical PLACES data
4. **Mechanism identification:** What infrastructure features predict better-than-expected outcomes?

### 10.2 For Policy

1. **Advocacy value:** Documents geographic inequity at tract level
2. **Targeting questions:** Identifies areas for further investigation (not direct intervention)
3. **Caution required:** Do not allocate resources based solely on these scores

### 10.3 What This Analysis Is Useful For

- Generating hypotheses about protective factors
- Prioritizing communities for qualitative research
- Advocating for regional health investment
- Monitoring geographic patterns over time

### 10.4 What This Analysis Is NOT Useful For

- Designing interventions
- Making causal claims
- Predicting individual health outcomes
- Direct resource allocation decisions

---

## 11. References

1. Borhani, N. O. (1965). Changes and geographic distribution of mortality from cerebrovascular disease. *AJPH*, 55, 673-681.
2. Howard, V. J., et al. (2019). Twenty years of progress toward understanding the Stroke Belt. *Stroke*, 50(6), 1508-1515.
3. Barker, L. E., et al. (2011). Geographic distribution of diagnosed diabetes. *Am J Prev Med*, 40(4), 434-439.
4. Mujib, M., et al. (2011). Evidence of a Heart Failure Belt. *Am J Cardiol*, 107(6), 935-937.
5. Chetty, R., et al. (2016). Income and life expectancy in the United States. *JAMA*, 315(16), 1750-1766.
6. Dwyer-Lindgren, L., et al. (2017). Inequalities in life expectancy among US counties. *JAMA Intern Med*, 177(7), 1003-1011.
7. Appalachian Regional Commission. (2017). Health Disparities in Appalachia.
8. Bradley, E. H., et al. (2009). A practical guide to using the positive deviance method. *BMC Health Services Research*, 9, 233.
9. Katz, L. F., et al. (2001). Moving to Opportunity in Boston: Early results. *QJE*, 116(2), 607-654.

---

**Document Control**

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Dec 30, 2025 | Initial release |
| 2.0 | Dec 30, 2025 | Post-peer review: Removed fabricated claims, added citations, honest framing |

**Contact:** research@odds.health
