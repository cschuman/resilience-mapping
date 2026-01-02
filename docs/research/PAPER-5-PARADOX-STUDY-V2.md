# Paper 5: The Limits of Food Access

> ## ⚠️ ARCHIVED - NOT FOR PUBLICATION
>
> **Status:** ABANDONED (January 2026)
>
> **Reason:** Fatal methodological flaw identified during rigorous peer review.
>
> ### The Problem
>
> CDC PLACES health data are **modeled estimates** using multilevel regression with poststratification (MRP) that incorporates tract-level demographics. Our baseline model used the **same demographics** to predict health burden. Therefore:
>
> - The "unexplained health burden" we identified is indistinguishable from **CDC model prediction error**
> - Tracts flagged as having "unexplained burden" may simply be areas where CDC's MRP model underperforms
> - We cannot distinguish true health disparities from measurement artifacts
>
> ### What We Learned
>
> 1. CDC PLACES data are inherently circular for this type of analysis
> 2. Effect sizes shrank 67-85% from V1 to V2 (evidence of V1 overfitting)
> 3. The 13.5% "paradox" rate is approximately the expected tail of a normal distribution
> 4. Tract-level measured health data do not exist to validate findings
>
> ### What Remains Valid
>
> The literature review critiquing food desert interventions (Cummins et al. 2014, Dubowitz et al. 2015, Shannon 2014, Ghosh-Dastidar et al. 2017) remains useful for future work.
>
> ---

**Original Working Title:** "Beyond Food Deserts: Adequate Grocery Access Is Not Associated with Expected Health Outcomes"

**Original Target Journal:** American Journal of Public Health

---

## Abstract

Food access interventions rest on the premise that proximity to grocery stores is associated with better health outcomes. We examine this premise using data from 47,326 U.S. census tracts with adequate food access (non-LILA designation). Using a comprehensive baseline model that includes demographics, socioeconomic status, and social vulnerability (R² = 73.9%), we identify 6,369 tracts (13.5%) with health outcomes substantially worse than predicted.

These tracts with unexplained health burden are modestly but significantly more likely to be majority-Black (d = 0.25 after demographic controls) and have higher Environmental Justice Index scores (d = 0.61). Notably, the environmental contamination component of EJI does not differ (d = -0.05); the association is with social vulnerability factors.

Longitudinal analysis (2020-2025) shows this pattern is stable (r = 0.97), though stability does not establish causation. We discuss alternative explanations including reverse causality (health-based residential sorting), unmeasured confounding (healthcare access, discrimination), and the limitations of ecological inference.

Our findings are consistent with—though do not prove—the hypothesis that cumulative structural disadvantage is associated with community health burden beyond what food access or demographic composition can explain. Policy implications should be interpreted cautiously given the observational design.

---

## Relationship to Prior Literature

This study extends a substantial body of work critiquing the "food desert" paradigm:

- **Cummins et al. (2014)** demonstrated that new grocery stores do not change purchasing behavior
- **Dubowitz et al. (2015)** found Pittsburgh's grocery store intervention did not improve diet quality
- **Shannon (2014)** proposed "food apartheid" to emphasize structural causes over geographic access
- **Ghosh-Dastidar et al. (2017)** showed proximity alone does not predict shopping patterns

We do not claim novelty in critiquing food access interventions. Our contribution is:
1. A comprehensive baseline model controlling for demographics (73.9% variance explained)
2. Identification of tracts with unexplained poor health after demographic controls
3. Longitudinal stability analysis across 6 years of CDC PLACES data
4. Integration of the Environmental Justice Index as a potential explanatory factor

---

## Key Findings

### Finding 1: Demographics Explain Most Health Variation

A baseline model including race, poverty, education, employment, housing tenure, and social vulnerability explains **73.9%** of health burden variation across tracts with adequate food access.

| Model | R² |
|-------|-----|
| Demographics + SES + State FE | 73.9% |

This is the primary finding: **most of what appears as a "food access paradox" is actually predictable from demographics and socioeconomic status.** Food access may be a marker for, rather than independent of, deeper structural factors.

### Finding 2: Tracts with Unexplained Health Burden Exist

After controlling for demographics, 6,369 tracts (13.5%) have health outcomes more than one standard deviation worse than predicted. These are communities where something beyond demographics is associated with poor health.

| Metric | Unexplained Burden | Non-Burdened | Cohen's d (95% CI) |
|--------|----------------------|--------------|-------------------|
| % Black population | 17.1% | 11.2% | +0.25 (0.22, 0.28) |
| Poverty rate | 15.5% | 12.0% | +0.31 (0.28, 0.34) |
| EJI score | 0.58 | 0.43 | +0.61 (0.58, 0.64) |
| Environmental burden | 0.50 | 0.51 | -0.05 (-0.08, -0.02) |

**Interpretation:** After demographic controls, a modest racial disparity persists (d = 0.25). The Environmental Justice Index shows a medium-large association (d = 0.61), but this is attributable to social vulnerability components, not environmental contamination.

### Finding 3: The Pattern Is Stable Over Time

Longitudinal analysis using CDC PLACES data (2020-2025) shows high year-to-year stability:

| Metric | Value |
|--------|-------|
| Year-to-year correlation | r = 0.97 |
| Tracts with unexplained burden in all years | 9.1% |
| Retention rate (2020→2025) | 67.8% |

**Interpretation:** This stability is consistent with—but does not prove—a persistent structural association. Alternative explanations include:
- Compositional stability (same residents aging with chronic conditions)
- Unmeasured confounders that are themselves stable
- Self-reinforcing cycles without clear intervention points

### Finding 4: Historical Redlining Shows Limited Independent Association

Among tracts in HOLC-mapped cities:

| Metric | Unexplained Burden | Non-Burdened |
|--------|----------------------|--------------|
| In redlined (D grade) areas | 28.4% | 22.1% |
| Odds ratio | 1.39x | — |

After controlling for current demographics, the HOLC association is attenuated (OR = 1.39 vs. 1.65 in unadjusted analysis). This pattern is consistent with—but does not prove—the hypothesis that historical redlining is associated with current health burden primarily through its association with current demographic composition.

---

## Methodological Approach

### Critical Design Decision: Comprehensive Baseline

Previous analyses of "food access paradoxes" have been criticized for circular reasoning—excluding demographics from baseline models, then "discovering" that paradox tracts are disadvantaged.

We address this by including all known predictors in our baseline:

**Baseline model predictors:**
- Race/ethnicity (% Black, % White, % Hispanic)
- Socioeconomic status (poverty rate, median income, education, unemployment)
- Housing (% renter-occupied)
- Social vulnerability (CDC SVI overall theme)
- State fixed effects

This model explains 73.9% of health burden variation. Our analysis focuses on the 26.1% that remains unexplained.

### Sample Selection

Our analysis includes 47,326 census tracts, which differs from the 64,336 tracts in the full USDA Food Access Research Atlas. The reduction reflects:

1. **Non-LILA filter**: We exclude Low-Income Low-Access (LILA) tracts to focus on communities with adequate food access (our research question concerns why adequate access does not predict good health)
2. **Complete case analysis**: Tracts missing ACS demographic data, SVI scores, or CDC PLACES estimates are excluded
3. **Income data cleaning**: Tracts with Census missing-value codes (-666666666) for median household income are excluded rather than imputed

This conservative approach ensures all 47,326 tracts have complete data for our baseline model, avoiding imputation-induced bias.

### Exploratory Matched Analysis

As a sensitivity check, we conducted propensity-score matching (1:1, nearest neighbor without replacement) pairing each unexplained-burden tract with a demographically similar non-burdened tract. Results were consistent with the primary analysis: matched unexplained-burden tracts showed elevated EJI scores (d = 0.62) attributable to social vulnerability components rather than environmental contamination. However, matching on observed demographics cannot address unmeasured confounding, and the matching itself was exploratory rather than pre-registered. We present these results in supplementary materials rather than as primary findings.

### Data Sources and Limitations

| Source | Year | Limitation |
|--------|------|------------|
| CDC PLACES | 2020-2025 | **Modeled estimates**, not measured outcomes. Uses multilevel regression with poststratification (MRP) from BRFSS survey responses. Small-area estimates are derived from regression models incorporating tract-level demographics—the same predictors in our baseline model. This creates potential circularity: tracts we identify as having "unexplained" poor health may simply be areas where the MRP model underperforms. True prevalence data at tract level do not exist for validation. |
| USDA FARA | 2019 | **Outdated** post-pandemic. Food retail landscape has changed significantly. |
| ACS Demographics | 2022 | Standard survey limitations; margins of error not incorporated |
| CDC SVI | 2022 | Composite measure; potential collinearity with other predictors |
| CDC EJI | 2022 | Contains health outcome components; potential circularity |
| HOLC Maps | 1930s | Historical; covers only 42,074 tracts in mapped cities |

### Terminology: "Unexplained Health Burden"

We use the term "unexplained health burden" (rather than "structurally burdened") throughout this paper to describe tracts with health outcomes worse than demographic predictors explain. This terminology is intentionally neutral:

- **What we observe**: Health burden exceeding predictions from our comprehensive baseline model
- **What we do not claim**: That structural factors cause this excess burden

Previous versions of this analysis used "structurally burdened," which implied causation we cannot establish. "Unexplained" accurately describes our finding: after controlling for demographics, socioeconomic status, and social vulnerability, 6,369 tracts have health outcomes we cannot account for. Whether this reflects unmeasured structural factors, healthcare access, measurement error in CDC PLACES, or compositional effects remains unknown.

### What We Cannot Measure

Several critical factors remain unmeasured:

1. **Healthcare access and quality** - Distance to providers, insurance coverage, discrimination in care. *Note: We downloaded HRSA Health Professional Shortage Area (HPSA) data (73,034 designations) but could not incorporate it. HPSA designations operate at county, service area, or population-group level—not census tract level. Crosswalking would require assuming all tracts within a designated area share the same shortage status, obscuring within-county variation. Given that healthcare access may be the most plausible unmeasured confounder explaining our "unexplained" health burden, this gap is a significant limitation. Future research should pursue tract-level healthcare access metrics such as distance to nearest Federally Qualified Health Center or primary care provider density.*
2. **Individual behaviors** - Diet quality, physical activity, substance use
3. **Social networks** - Family structure, community cohesion, mutual aid
4. **Crime and safety** - Violence exposure, chronic stress
5. **Occupational hazards** - Job type, workplace exposures
6. **Store quality** - FARA measures distance, not affordability or product quality

These unmeasured factors may fully or partially explain the unexplained health burden pattern we observe.

---

## Alternative Explanations

### Reverse Causality

We cannot rule out that poor health causes concentration in certain tracts rather than the reverse:

1. **Health-based residential sorting**: Individuals with chronic illness may have lower earnings, less mobility, and concentrate in cheaper housing
2. **Mortality selection**: Healthier residents may move out or die at lower rates, leaving sicker populations behind
3. **Intergenerational transmission**: Health conditions with genetic/epigenetic components concentrate in families that stay in place

The stability we observe (r = 0.97) is equally consistent with reverse causality as with structural causation.

### Unmeasured Confounding

Variables we could not measure may explain the entire pattern:

- **Healthcare discrimination**: Black Americans receive worse care even in well-resourced settings (IOM, 2003; Hoffman et al., 2016)
- **Medical mistrust**: Historical and ongoing discrimination may be associated with reduced care-seeking behavior
- **Chronic stress**: Racism-related stress may affect health independently of material conditions

### Measurement Artifact

The CDC PLACES data are modeled estimates, not measured outcomes. Tracts we identify as having unexplained health burden may simply be areas where CDC's small-area estimation performs poorly.

---

## Limitations

### Not Addressed

1. **Cross-sectional inference**: Longitudinal stability does not establish causation. We show the pattern persists, not that it is caused by structural factors.

2. **Selection on the dependent variable**: We define "unexplained health burden" by health outcomes, then look for associated factors. This guarantees finding associations but cannot establish causation.

3. **Ecological fallacy**: Tract-level associations may not hold for individuals within those tracts.

4. **Missing healthcare data**: HRSA data on Federally Qualified Health Centers was available but not incorporated. This is a significant gap.

5. **No community voice**: This analysis uses only administrative data. We have not spoken with residents of these tracts about their experiences or priorities.

### Partially Addressed

6. **Circular baseline**: By including demographics in our baseline model (R² = 73.9%), we identify tracts with unexplained poor health, not simply disadvantaged tracts.

7. **Environmental hazards**: EJI analysis shows environmental contamination specifically (d = -0.05) does not distinguish burdened tracts; the effect is social vulnerability.

### Remaining Unexplained Variance

Our full model explains 73.9% of variance. The 26.1% that remains unexplained may reflect:
- True unmeasured structural factors (healthcare access, discrimination)
- Measurement error in CDC PLACES estimates
- Random variation with no systematic cause

---

## Discussion

### What We Can Say

1. **Food access alone does not predict health.** Tracts with adequate grocery access vary enormously in health outcomes.

2. **Demographics explain most variation.** A 73.9% R² suggests that race, poverty, education, and social vulnerability capture most of what matters.

3. **Something beyond demographics is associated with health burden.** 6,369 tracts have worse health than demographics predict, consistent with unmeasured factors.

4. **Environmental contamination is not associated with unexplained burden.** The EJI association is with social vulnerability components, not pollution exposure.

5. **The pattern is stable.** Whether due to causation or compositional effects, these tracts remain burdened over time.

### What We Cannot Say

1. **We cannot say structural factors cause poor health.** We observe associations, not causes.

2. **We cannot recommend specific interventions.** Without causal evidence, policy prescriptions exceed our evidence base.

3. **We cannot say these communities need more grocery stores.** Our data suggest they do not—food access is adequate by USDA definition.

4. **We cannot say these communities would benefit from "reparative" investments.** This is a normative claim that requires value judgments beyond our empirical analysis.

---

## Policy Implications (Cautious)

Given the observational design and remaining limitations, we offer cautious observations rather than prescriptions:

1. **Food access programs should not be evaluated solely by grocery store proximity.** If communities with adequate access still have poor health, access metrics are insufficient.

2. **Demographic and socioeconomic factors warrant attention.** The 73.9% variance explained by these factors suggests they may be more strongly associated with health than food access.

3. **Healthcare access merits investigation.** Our inability to include healthcare data is a significant gap. Future research should examine whether healthcare access is associated with the patterns we observe.

4. **Community input is essential.** We cannot know what interventions would help without asking affected communities. Our administrative data analysis cannot substitute for participatory research.

### What We Do Not Recommend

We explicitly avoid recommending:
- Specific dollar amounts for investment
- "Proportional to historical harm" frameworks without defining proportion or harm
- Reparative programs without community-defined goals
- Any causal claims about what would improve health

---

## Conclusion

We find that 6,369 U.S. census tracts have health outcomes worse than their demographic composition predicts, despite adequate food access. This pattern is stable over 6 years and associated with higher Environmental Justice Index scores (attributable to social vulnerability components, not environmental contamination).

These findings are consistent with—but do not prove—the hypothesis that cumulative structural disadvantage is associated with health burden beyond what demographics or food access can explain. Alternative explanations including reverse causality, unmeasured confounding, and measurement artifacts cannot be ruled out.

The primary contribution of this analysis is methodological: by including demographics in our baseline model, we avoid the circularity of previous "food access paradox" studies. Our 73.9% R² demonstrates that most health variation is predictable from demographics. The 26.1% that remains unexplained merits further investigation with better data on healthcare access and community-level exposures.

Food access programs may be valuable for other reasons, but our data do not support the assumption that grocery store proximity is strongly associated with community health outcomes.

---

## Ethics Statement

This study uses publicly available, de-identified secondary data from federal agencies and is exempt from IRB review per 45 CFR 46.104(d)(4). No community members were contacted. This is a limitation.

---

## Funding

[To be completed]

---

## Conflicts of Interest

The authors declare no conflicts of interest.

---

## Data Availability

Analysis code and processed datasets: [repository URL]

Raw data sources:
- CDC PLACES: https://www.cdc.gov/places (modeled estimates, not measured outcomes)
- USDA FARA: https://www.ers.usda.gov/data-products/food-access-research-atlas/
- CDC SVI: https://www.atsdr.cdc.gov/placeandhealth/svi/
- CDC EJI: https://www.atsdr.cdc.gov/place-health/php/eji/
- HOLC Maps: https://dsl.richmond.edu/panorama/redlining/

---

## Analysis Scripts

```
app/analytics/
├── paradox_v2_fixed_baseline.py      # Core analysis with demographic controls
├── paradox_longitudinal_analysis.py  # Multi-year stability
├── paradox_eji_analysis.py           # Environmental Justice Index
├── paradox_matched_comparison.py     # Matched analysis (exploratory)
└── paradox_sensitivity_analysis.py   # Threshold robustness
```

---

## References

Cummins, S., Flint, E., & Matthews, S. A. (2014). New neighborhood grocery store increased awareness of food access but did not alter dietary habits or obesity. Health Affairs, 33(2), 283-291.

Dubowitz, T., Ghosh-Dastidar, M., Cohen, D. A., et al. (2015). Diet and perceptions change with supermarket introduction in a food desert, but not because of supermarket use. Health Affairs, 34(11), 1858-1868.

Ghosh-Dastidar, M., Hunter, G., Collins, R. L., et al. (2017). Does opening a supermarket in a food desert change the food environment? Health & Place, 46, 249-256.

Hoffman, K. M., Trawalter, S., Axt, J. R., & Oliver, M. N. (2016). Racial bias in pain assessment and treatment recommendations. PNAS, 113(16), 4296-4301.

Institute of Medicine. (2003). Unequal Treatment: Confronting Racial and Ethnic Disparities in Health Care. National Academies Press.

Krieger, N., Van Wye, G., Huynh, M., et al. (2020). Structural racism, historical redlining, and risk of preterm birth. American Journal of Public Health, 110(7), 1046-1053.

Nardone, A., Chiang, J., & Corburn, J. (2020). Historic redlining and urban health today. Environmental Justice, 13(4), 109-119.

Shannon, J. (2014). Food deserts: Governing obesity in the neoliberal city. Progress in Human Geography, 38(2), 248-266.

---

*Revised draft: January 2026 (V3 - causal language audit)*
*Peer review round: Addressing causal language and terminology*
*Analysis tracts: 47,326*
*Tracts with unexplained health burden: 6,369*
