# Tract-Level Heterogeneity in Chronic Disease Burden: Geographic Patterns and Outlier Communities Across 63,847 U.S. Census Tracts

**Authors:** Health Resilience Mapping Research Collaborative
**Date:** December 2025 (Version 2.0, Post-Peer Review)
**Target Venue:** Journal of Community Health / Population Health Metrics

---

## Abstract

**Background:** Geographic variation in health outcomes has been documented for decades, including the Stroke Belt (1965), Diabetes Belt (2011), and Appalachian health disparities. Less attention has focused on systematic identification of communities with better-than-expected outcomes at census tract resolution.

**Methods:** We analyzed CDC PLACES tract-level health estimates (2023) linked to USDA Food Access Research Atlas data (2019) for 63,847 census tracts (population ≥ 500) representing 219.8 million Americans. Using OLS regression with state fixed effects, we calculated standardized residuals to identify statistical outliers.

**Results:** Regional patterns replicated known disparities, with the South (+0.30 SD) and Midwest (+0.16 SD) showing elevated burden compared to the Northeast (-0.17 SD) and West (-0.37 SD). We identified 1,047 Low-Income Low-Access tracts (12.0%) with health outcomes substantially better than predicted, representing candidate communities for positive deviance investigation.

**Conclusions:** This analysis confirms known geographic health patterns at tract-level resolution and identifies statistical outliers warranting further investigation. However, significant methodological limitations—including temporal misalignment, construct validity concerns (burden-resilience r = -0.72), and lack of external validation—preclude causal interpretation. The identified outliers represent hypotheses, not validated protective factors. Future research should employ positive deviance methodology with community engagement to investigate outlier mechanisms.

**Keywords:** health disparities, geographic variation, positive deviance, census tract, chronic disease, methodology

---

## 1. Introduction

### 1.1 Background

Health outcomes in the United States exhibit profound geographic variation. Life expectancy differs by over 20 years between the longest- and shortest-lived counties (Dwyer-Lindgren et al., 2017). The "Stroke Belt"—elevated stroke mortality in Southeastern states—has been documented since 1965 (Borhani, 1965; Howard et al., 2019). The "Diabetes Belt" was characterized by Barker et al. (2011) with 644 counties showing prevalence ≥11%. Appalachian health disparities have been studied for decades (ARC, 2017).

Despite this extensive documentation, two gaps remain:

1. **Resolution:** Most analyses use county-level data. Census tract analysis provides finer geographic resolution for targeting.

2. **Positive deviance:** Most research documents disparities rather than systematically identifying communities achieving better-than-expected outcomes.

### 1.2 Theoretical Framework

We draw on established frameworks:

1. **Positive Deviance** (Marsh et al., 2004): Identifying individuals or communities that succeed despite predicted failure, then investigating how they do so.

2. **Social Determinants of Health** (WHO, 2008): Place-based factors including economic stability, healthcare access, and built environment influence health outcomes.

3. **Place Effects vs. Selection** (Diez Roux, 2001): Observed geographic patterns may reflect either neighborhood influence on health or systematic sorting of people with different health into different areas.

### 1.3 Research Questions

1. Do regional burden patterns documented at county level persist at tract level?
2. Can we systematically identify tracts with better-than-expected health outcomes?
3. What is the prevalence and geographic distribution of such statistical outliers?

### 1.4 Contribution

This study makes three contributions:

- **Methodological:** Demonstrates tract-level positive deviance identification at national scale
- **Replication:** Confirms regional health patterns at finer geographic resolution
- **Hypothesis generation:** Identifies candidate communities for mixed-methods investigation

**Explicit non-contribution:** This study does not identify protective factors, establish causality, or validate intervention targets.

---

## 2. Methods

### 2.1 Data Sources

**Health Outcomes:** CDC PLACES 2023 release providing model-based small-area estimates for 29 health measures at census tract level.

**Food Access:** USDA Food Access Research Atlas 2019 containing Low-Income Low-Access (LILA) indicators at multiple distance thresholds.

**Demographics:** U.S. Census Bureau 2020 population counts.

**Critical Limitation: Temporal Misalignment**

The 4-year gap between FARA (2019) and PLACES (2023) spans the COVID-19 pandemic, introducing substantial confounding. We cannot assume 2019 structural conditions predict 2023 health outcomes.

### 2.2 Sample Construction

| Step | Tracts | Rationale |
|------|--------|-----------|
| Initial FARA universe | 72,531 | — |
| Matched to PLACES | 68,170 | 94% match rate |
| Excluded >20% group quarters | 67,892 | Remove institutional populations |
| **Excluded population < 500** | **63,847** | Reliability threshold |

**Population filter justification:** Per Census Bureau guidelines, tracts below 500 population produce unreliable estimates (Federal Register, 2018). This exclusion is non-random and may bias results.

### 2.3 Measures

**Composite Health Burden Index:**
Mean z-score across five outcomes: obesity, diabetes, CHD, hypertension, physical inactivity.

Internal consistency: Cronbach's α = 0.87.

**Statistical Outlier Identification:**
Using OLS regression with state fixed effects:

```
Burden_i = β₀ + β₁LILA_i + β₂LowIncome_i + β₃Rural_i + β₄NoVehicle_i + State_FE + ε_i
```

Outliers defined as standardized residuals beyond ±1.5 SD.

### 2.4 Construct Validity Concern

We initially termed standardized residuals "resilience scores." However, peer review identified this as potentially tautological:

- The residual captures unexplained variance in burden
- Correlation between "resilience" and burden: r = -0.72
- This strong correlation is partially mechanical, not purely empirical

**We therefore refer to outliers as "statistical deviants" rather than "resilient communities."** The mechanism underlying better-than-expected outcomes is unknown without investigation.

### 2.5 Limitations Acknowledged A Priori

1. **Temporal misalignment:** 4-year data gap spans pandemic
2. **Model-based estimates:** PLACES uses small-area estimation, not measurement
3. **No age adjustment:** Tract-level estimates are crude, not age-standardized
4. **Construct validity:** "Resilience" may measure same construct as burden
5. **Cross-sectional:** Cannot establish causality
6. **Selection bias:** Excluded tracts may differ systematically

---

## 3. Results

### 3.1 Descriptive Statistics

**Table 1: Sample Characteristics (N = 63,847 tracts)**

| Variable | Mean (SD) | Range |
|----------|-----------|-------|
| Health burden index | 0.00 (1.00) | -6.84 to +5.22 |
| Total population per tract | 3,448 (2,102) | 500 to 37,452 |
| LILA (1+10 miles) | 12.7% | Binary |
| Low-income tract | 23.1% | Binary |
| Rural | 19.4% | Binary |

### 3.2 Regional Patterns

**Table 2: Regional Health Burden (Replication of Known Disparities)**

| Region | Tracts | Population | Mean Burden | SD |
|--------|--------|------------|-------------|-----|
| South | 20,312 | 63.1M | +0.295 | 1.09 |
| Midwest | 15,847 | 53.9M | +0.159 | 1.04 |
| Northeast | 12,408 | 46.1M | -0.169 | 0.91 |
| West | 15,280 | 56.7M | -0.371 | 0.87 |

ANOVA: F(3, 63843) = 847.2, p < 0.001

**Interpretation:** These patterns replicate the Stroke Belt (Borhani, 1965), Diabetes Belt (Barker et al., 2011), and established regional health research. Our contribution is confirming persistence at tract level, not discovering new patterns.

### 3.3 State-Level Patterns

**Table 3: Highest and Lowest Burden States**

| Highest Burden | Score | Lowest Burden | Score |
|----------------|-------|---------------|-------|
| West Virginia | +0.97 | Colorado | -0.72 |
| Mississippi | +0.85 | Hawaii | -0.60 |
| Alabama | +0.75 | Utah | -0.58 |
| Arkansas | +0.65 | Massachusetts | -0.44 |
| Louisiana | +0.55 | California | -0.42 |

These align with decades of state health rankings research.

### 3.4 Statistical Outlier Identification

Among 8,127 LILA tracts in our analytic sample:

- **Positive deviants** (residual < -1.5 SD): 1,047 tracts (12.9%)
- **Negative deviants** (residual > +1.5 SD): 1,089 tracts (13.4%)
- **Within expected range**: 5,991 tracts (73.7%)

### 3.5 Characteristics of Positive Deviants

**Table 4: Positive Deviant LILA Tracts (n = 1,047)**

| Characteristic | Positive Deviants | Other LILA | Difference |
|----------------|-------------------|------------|------------|
| Mean population | 3,892 | 3,234 | +20% |
| % Rural | 28.4% | 31.2% | -2.8 pp |
| Mean state burden | +0.12 | +0.18 | -0.06 |

**Interpretation caution:** These differences may reflect unmeasured confounders (age structure, healthcare access, social capital) rather than transferable protective factors. Investigation required.

### 3.6 Geographic Clustering

Positive deviants cluster in:
- Suburban tracts near major universities
- Tracts adjacent to major medical centers
- Coastal communities in otherwise high-burden states

Negative deviants cluster in:
- Post-industrial urban cores (Cleveland, Detroit)
- Remote rural areas
- Areas with environmental contamination history

**These clusters replicate known patterns** from urban health and environmental justice research.

---

## 4. Discussion

### 4.1 Principal Findings

This analysis confirms known geographic health patterns at census tract resolution and identifies statistical outliers warranting investigation. Three findings merit emphasis:

**First,** regional patterns documented at county level since the 1960s persist at tract level. This is replication with increased resolution, not novel discovery.

**Second,** approximately 13% of LILA tracts show substantially better-than-expected health outcomes. This prevalence is consistent with positive deviance literature suggesting 10-15% of communities "beat the odds."

**Third,** positive deviants cluster geographically, suggesting place-based protective factors rather than random variation. However, we cannot distinguish true protective factors from measurement artifact or unmeasured confounders.

### 4.2 Comparison with Prior Work

**Stroke Belt (Howard et al., 2019):** Our burden patterns align with the geographic distribution of elevated stroke mortality documented since 1965. We add tract-level resolution but no mechanistic insight.

**Diabetes Belt (Barker et al., 2011):** Our high-burden regions substantially overlap with the 644 counties identified as having diabetes prevalence ≥11%. We extend their county-level analysis to tracts.

**County Health Rankings (Remington et al., 2015):** Our regional and state patterns correlate with established county rankings. We provide finer geographic resolution but use similar underlying data sources.

### 4.3 Limitations

**This analysis has significant limitations that constrain interpretation:**

1. **Temporal misalignment:** The 4-year gap between food access (2019) and health (2023) data spans COVID-19. We cannot assume 2019 conditions predict 2023 outcomes.

2. **Construct validity:** The strong correlation (r = -0.72) between our "resilience" measure and burden suggests these may not be independent constructs. We may be measuring one thing twice.

3. **Model-based estimates:** CDC PLACES uses small-area estimation. Tract-level estimates have substantial uncertainty not quantified in our analysis.

4. **No age adjustment:** Tract-level PLACES estimates are not age-standardized. Regional differences may reflect demographics, not health disparities.

5. **No external validation:** We did not validate scores against mortality, hospitalization, or other outcomes.

6. **Selection bias:** The 33% of population excluded (tracts with <500 population, >20% group quarters) may differ systematically.

7. **Cross-sectional design:** Cannot distinguish place effects from selection effects. People with different health may sort into different communities.

8. **No investigation of outliers:** We identify statistical deviants but do not investigate what makes them different.

### 4.4 Distinguishing Place Effects from Selection

A fundamental limitation is our inability to distinguish:

- **Place effects:** Living in a community causes health outcomes
- **Selection effects:** People with certain health sort into certain communities
- **Confounding:** Unmeasured factors drive both location and health

The Moving to Opportunity experiment (Katz et al., 2001) demonstrated that randomized relocation to lower-poverty neighborhoods causally improved mental health, suggesting place effects are real. However, our observational data cannot estimate the relative contributions of these mechanisms.

### 4.5 Positive Deviance Methodology Requirements

Following Bradley et al. (2009), validating positive deviants requires:

1. **Confirm persistence:** Do deviants remain deviants across years? (NOT DONE)
2. **Match and contrast:** Compare to similar communities without positive outcomes (NOT DONE)
3. **Qualitative investigation:** Ask communities what makes them different (NOT DONE)
4. **Hypothesis testing:** Verify factors through controlled comparison (NOT DONE)

**We have completed only the identification step.** Claims about protective factors would be speculation.

---

## 5. Implications

### 5.1 For Research

This analysis supports:

1. **Hypothesis generation:** The 1,047 positive deviant LILA tracts are candidates for mixed-methods investigation using positive deviance methodology.

2. **Longitudinal analysis:** Using historical PLACES data (2020-2024), future research could examine whether positive deviants maintain better-than-expected trajectories over time.

3. **External validation:** Linking burden scores to CDC WONDER mortality data would test predictive validity.

4. **Mechanism identification:** Merging with HRSA (FQHCs), FCC (broadband), and social capital data could identify infrastructure correlates of positive deviance.

### 5.2 For Policy

**What this analysis can support:**

- Advocacy for regional health investment (documents geographic inequity)
- Prioritizing communities for qualitative investigation
- Baseline for longitudinal monitoring

**What this analysis cannot support:**

- Designing interventions (no causal evidence)
- Direct resource allocation (no external validation)
- Claims about protective factors (no investigation)

### 5.3 Evidence-Based Policy (From Separate Literature)

The following have causal evidence independent of our analysis:

| Intervention | Evidence | Citation |
|--------------|----------|----------|
| Medicaid expansion | Mortality reduction | Sommers et al., 2017 |
| CHW programs | $2.47 ROI | Penn IMPaCT RCT |
| HRSN navigation | 9% ED reduction | CMS AHC evaluation |

Our geographic analysis might inform where to target these evidence-based interventions, but cannot substitute for their independent evidence base.

### 5.4 What We Recommend Against

**Zone designations without intervention specificity:** Evidence on Enterprise Zones, Promise Neighborhoods, and generic place-based initiatives is mixed at best (BMC umbrella review, 2021). Exception: Maryland Health Enterprise Zones showed positive results through specific healthcare delivery mechanisms.

**"Learning from outliers" without investigation:** Statistical identification is hypothesis generation. Without qualitative investigation, we cannot claim to know what makes positive deviants different.

---

## 6. Future Directions

### 6.1 Validation (Required)

1. Link burden scores to mortality (CDC WONDER)
2. Confirm outlier persistence across 2020-2024 PLACES releases
3. Quantify uncertainty using PLACES confidence intervals

### 6.2 Investigation (Recommended)

1. Mixed-methods case studies in 25 positive deviant and 25 negative deviant tracts
2. Community-engaged research centering resident voice
3. Matched comparison designs (adjacent high/low deviant tracts)

### 6.3 Mechanism Identification (Exploratory)

1. Merge FQHC locations (HRSA) with deviant tracts
2. Overlay broadband access (FCC) data
3. Incorporate social capital indices
4. Analyze historical redlining (HOLC maps) overlap

### 6.4 Prediction (Ambitious)

1. Build trajectory forecasting model using 5 years of PLACES data
2. Identify communities likely to decline before crisis
3. Validate predictions against subsequent health outcomes

---

## 7. Conclusion

This analysis documents geographic variation in chronic disease burden across 63,847 U.S. census tracts, confirming regional patterns established by decades of prior research and identifying 1,047 statistical outliers in food-insecure areas with better-than-expected health outcomes.

However, significant methodological limitations—temporal misalignment, construct validity concerns, and lack of external validation—preclude causal interpretation. The identified positive deviants represent hypotheses for investigation, not validated protective factors.

The magnitude of geographic health variation—with burden scores spanning 12 standard deviations—reflects profound health inequity documented since at least the 1960s. Addressing this inequity requires understanding mechanisms, not just mapping patterns.

Our contribution is methodological (tract-level resolution at national scale) and hypothesis-generating (systematic outlier identification). Claims beyond this would exceed what our cross-sectional descriptive analysis can support.

Future research should validate these findings against mortality data, investigate outlier communities using positive deviance methodology, and develop predictive models for community health trajectories. Until then, this analysis should inform research prioritization and advocacy—not direct policy implementation.

---

## References

1. Appalachian Regional Commission. (2017). Health Disparities in Appalachia. https://www.arc.gov/report/health-disparities-in-appalachia/

2. Barker, L. E., et al. (2011). Geographic distribution of diagnosed diabetes in the U.S.: A diabetes belt. *American Journal of Preventive Medicine*, 40(4), 434-439.

3. Borhani, N. O. (1965). Changes and geographic distribution of mortality from cerebrovascular disease. *American Journal of Public Health*, 55, 673-681.

4. Bradley, E. H., et al. (2009). A practical guide to using the positive deviance method in health services research. *BMC Health Services Research*, 9, 233.

5. CDC. (2023). PLACES: Local Data for Better Health. Methodology. https://www.cdc.gov/places/methodology/

6. Chetty, R., et al. (2016). The association between income and life expectancy in the United States, 2001-2014. *JAMA*, 315(16), 1750-1766.

7. CMS. (2024). Accountable Health Communities Model Final Evaluation Report.

8. Diez Roux, A. V. (2001). Investigating neighborhood and area effects on health. *American Journal of Public Health*, 91(11), 1783-1789.

9. Dwyer-Lindgren, L., et al. (2017). Inequalities in life expectancy among US counties, 1980 to 2014. *JAMA Internal Medicine*, 177(7), 1003-1011.

10. Federal Register. (2018). Census Tracts for the 2020 Census—Proposed Criteria. Vol. 83, No. 32.

11. Howard, V. J., et al. (2019). Twenty years of progress toward understanding the Stroke Belt. *Stroke*, 50(6), 1508-1515.

12. Kangovi, S., et al. (2020). Effect of community health worker support on clinical outcomes of low-income patients across primary care facilities. *Health Affairs*.

13. Katz, L. F., et al. (2001). Moving to Opportunity in Boston: Early results of a randomized mobility experiment. *Quarterly Journal of Economics*, 116(2), 607-654.

14. Marsh, D. R., et al. (2004). The power of positive deviance. *BMJ*, 329(7475), 1177-1179.

15. Mujib, M., et al. (2011). Evidence of a "Heart Failure Belt" in the Southeastern United States. *American Journal of Cardiology*, 107(6), 935-937.

16. Remington, P. L., et al. (2015). The County Health Rankings: Rationale and methods. *Population Health Metrics*, 13(1), 11.

17. Sommers, B. D., et al. (2017). Changes in utilization and health among ACA Medicaid expansion enrollees. *Health Affairs*.

---

## Supplementary Materials

Available at: https://odds.health/research

- Appendix A: Data processing code
- Appendix B: Full state-level results
- Appendix C: Sensitivity analyses
- Appendix D: Interactive map

---

## Author Contributions

All authors contributed to conception, analysis, and writing. Statistical review conducted following peer feedback.

## Funding

This research used publicly available federal data. No external funding.

## Conflicts of Interest

None declared.

## Data Availability

All source data are publicly available from CDC PLACES, USDA FARA, and U.S. Census Bureau.

## Ethics Statement

This study used publicly available, de-identified census tract-level data and was exempt from IRB review.

---

**Document Control**

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Dec 30, 2025 | Initial release |
| 2.0 | Dec 30, 2025 | Major revision following peer review: honest limitations, proper citations, removed unsupported claims |

**Corresponding Author:** research@odds.health
