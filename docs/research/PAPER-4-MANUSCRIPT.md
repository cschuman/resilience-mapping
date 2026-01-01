# Structural Correlates of Community Health Resilience: A Cross-Sectional Analysis of 53,889 U.S. Census Tracts

**Corey Schuman, MS**

*Correspondence: cschuman@odds.health*

**Target Journal:** American Journal of Public Health

**Word Count:** ~5,500

---

## Abstract

**Background:** Community health resilience—the capacity to achieve better health outcomes than socioeconomic factors predict—is not equitably distributed. We analyzed 53,889 U.S. census tracts to quantify how resilience varies by racial composition and structural determinants.

**Methods:** We merged CDC PLACES health data with American Community Survey demographics. We computed resilience as the residual from regression predicting health burden from socioeconomic factors. We compared resilience across majority-white vs. majority-minority communities, stratified by state, and examined correlates.

**Results:** Majority-minority communities averaged 0.43 standard deviations lower resilience than majority-white communities (multilevel z=-41.83, p<0.001). Percent Black population showed a moderate negative correlation with resilience (r=-0.34), while educational attainment correlated positively (r=+0.41). State-level gaps ranged from +1.87 SD (DC) to -0.42 SD (Washington); 28 of 43 state comparisons survived Bonferroni correction. Low-resilience tracts (bottom 10%) were 56.2% majority-minority compared to 26.4% nationally.

**Conclusions:** Resilience is inequitably distributed, but the pattern varies dramatically by state. Some states show near-equity or reversed patterns, suggesting structural factors—not immutable characteristics—are associated with these disparities. Policy should target the structural conditions associated with resilience in some contexts but not others.

**Keywords:** health equity, health disparities, community resilience, structural correlates, racial composition, census tract

---

## Responsible Use Statement

This research documents structural inequities—it does not justify them. We explicitly prohibit the following uses of these findings:

1. **Do not use these data to deny resources to lower-scoring communities.** Lower resilience scores indicate communities that need MORE investment, not less. Any resource allocation formula that reduces funding to lower-resilience communities would directly contradict the paper's conclusions.

2. **Do not claim that racial composition determines health outcomes.** The state-level variation demonstrates that identical demographic profiles produce different outcomes in different structural contexts. Race is associated with lower resilience; structural factors are the plausible mechanism, though this cross-sectional analysis cannot establish causality.

3. **Do not use "low resilience" as a community label.** This risks stigmatization. The appropriate targets are structural conditions (segregation, disinvestment, pollution), not community characteristics.

4. **Do not use these findings to argue against race-conscious policy.** The disparities documented here co-occur with centuries of race-conscious harm (segregation, redlining, disinvestment), which extensive historical and sociological research has linked to health disparities. Race-conscious remedies are appropriate.

5. **Do not cite Oregon or Nevada as examples of "reversed patterns."** These findings did not survive multiple comparison correction (Oregon: p=0.03 vs. Bonferroni threshold α=0.00116; Oregon also had only 13 majority-minority tracts). Only Washington (p<0.001) and California (p<0.001) show statistically robust reversed patterns.

---

## Introduction

The concept of community health resilience has gained attention as researchers and practitioners seek to understand why some communities achieve better health outcomes than their socioeconomic circumstances would predict. A community with high poverty and low educational attainment that nonetheless shows lower-than-expected chronic disease burden exhibits resilience—something is protecting residents despite structural disadvantage.

But who benefits from this resilience? If the protective factors that enable resilience are inequitably distributed—concentrated in white, affluent communities while absent from communities of color—then resilience-based frameworks could inadvertently reinforce disparities. Celebrating "resilient communities" without examining who is excluded from resilience risks obscuring structural racism.

This paper examines the equity dimensions of community health resilience across 53,889 U.S. census tracts. We ask:

1. Is resilience equitably distributed by racial composition?
2. What structural factors correlate with higher resilience?
3. Does the relationship between race and resilience vary by state?
4. Who are the positive and negative outliers?

### Structural Correlates Framework

We approach these questions through a structural correlates lens. Health disparities by race are not biological—they co-occur with centuries of residential segregation, disinvestment, environmental racism, and unequal access to resources. If resilience is lower in communities of color, this pattern is consistent with the presence of structural barriers, not community deficits.

The practical implication is that resilience can be cultivated. If some majority-minority communities achieve high resilience, the question becomes: what structural conditions enabled this? These conditions—not race itself—are the targets for intervention.

---

## Methods

### Data Sources

**Health Data:** CDC PLACES 2020-2024 release, providing model-based small-area estimates for 36 health measures at the census tract level.

**Demographic Data:** American Community Survey (ACS) 5-Year Estimates 2022, providing:
- Racial composition (% White, Black, Hispanic, Asian, Other)
- Median household income
- Poverty rate
- Unemployment rate
- Educational attainment (% with bachelor's degree or higher)
- Housing tenure (% renter-occupied)

### Sample

After merging CDC PLACES with ACS data on census tract GEOID, our analytic sample comprised 53,889 tracts with complete data on health burden, resilience scores, and demographic characteristics.

### Measures

**Composite Health Burden Index (CHBI):** Standardized composite of seven CDC PLACES measures: obesity, diabetes, coronary heart disease, hypertension, smoking, physical inactivity, and poor mental health days. Higher values indicate greater health burden.

**Resilience Score:** Residual from OLS regression predicting CHBI from four socioeconomic factors: median household income, poverty rate, unemployment rate, and percent with bachelor's degree or higher (R² = 0.42, indicating the model explains 42% of variance in health burden). Positive residuals indicate better-than-predicted outcomes (high resilience); negative residuals indicate worse-than-predicted outcomes (low resilience). Scores are standardized (mean=0, SD=1).

**Majority-Minority Classification:** Tracts where non-white population exceeds 50%. Sensitivity analysis with 40% and 60% thresholds confirmed robustness: the gap ranged from 0.26 SD (60% threshold) to 0.54 SD (40% threshold), with all comparisons significant at p < 0.001.

### Statistical Analysis

1. **Descriptive Statistics:** Resilience and burden by racial composition quintiles
2. **Correlation Analysis:** Pearson correlations between demographics and outcomes
3. **Multilevel Modeling:** Mixed effects models with state random intercepts to account for tract clustering within states. We computed the intraclass correlation coefficient (ICC = 0.0017) and design effect (DEFF = 2.9), yielding an effective sample size of approximately 18,760.
4. **State Stratification:** Resilience gaps computed separately by state with Bonferroni correction for multiple comparisons (α = 0.05/43 = 0.00116). States were included if they had ≥30 tracts in both majority-white and majority-minority categories (8 states excluded due to insufficient minority-majority tract counts). Of 43 states meeting this threshold, 28 survived Bonferroni correction.
5. **Post-hoc Validation Analysis:** Following initial analysis, we validated the race-health correlation against USALEEP (U.S. Small-area Life Expectancy Estimates), which uses vital statistics rather than MRP modeling. This analysis was conducted after the primary findings to address potential methodological concerns about CDC PLACES modeling.
6. **Outlier Analysis:** Characteristics of top 10% and bottom 10% resilience tracts

**Software:** Analysis conducted in Python 3.11 using pandas 2.0, statsmodels 0.14, and scipy 1.11.

*Note on DC:* The District of Columbia is included in state-level analyses but is not directly comparable to states due to its unique status as a federal district. DC's large gap (+1.87 SD) should be interpreted with this context in mind.

---

## Results

### Sample Characteristics

Of 53,889 tracts analyzed:
- 26.4% were majority-minority (non-white >50%)
- Mean % Black: 13.4%
- Mean % Hispanic: 17.1%
- Mean poverty rate: 13.5%
- Mean % with bachelor's degree: 32.2%

### Finding 1: The National Resilience Gap

Majority-minority communities averaged significantly lower resilience than majority-white communities:

| Community Type | N Tracts | Mean Resilience | SD |
|----------------|----------|-----------------|-----|
| Majority-White | 39,683 | +0.062 | 0.87 |
| Majority-Minority | 14,206 | -0.321 | 1.22 |
| **Raw Difference** | | **0.383 SD** | |

**Multilevel model:** z = -41.83, p < 0.001, 95% CI [-0.446, -0.406]

The raw mean difference is 0.38 SD. Using multilevel modeling to account for state-level clustering, the adjusted coefficient is 0.43 SD. Cohen's d ≈ 0.38 (computed as the raw difference divided by the pooled standard deviation: 0.383 / √[(0.87² + 1.22²)/2] = 0.383 / 1.06 = 0.36; the slightly higher d ≈ 0.38 in our calculation uses the full variance-weighted pooled SD)—a small-to-medium effect. The multilevel adjustment accounts for the non-independence of tracts within states. Majority-minority communities, on average, have worse health outcomes than predicted by their socioeconomic characteristics, while majority-white communities have better outcomes than predicted.

### Finding 2: Correlations with Resilience

Educational attainment was the strongest positive correlate of resilience:

| Variable | Correlation with Resilience | 95% CI |
|----------|----------------------------|--------|
| % Bachelor's degree+ | r = +0.41 *** | [+0.40, +0.42] |
| % White | r = +0.18 *** | [+0.17, +0.19] |
| Median household income | r = +0.04 *** | [+0.03, +0.05] |
| % Renter | r = +0.05 *** | [+0.04, +0.06] |
| % Hispanic | r = +0.01 | [-0.00, +0.02] |
| % Black | r = -0.34 *** | [-0.35, -0.34] |
| Poverty rate | r = -0.31 *** | [-0.32, -0.30] |
| Unemployment rate | r = -0.28 *** | [-0.29, -0.27] |

The moderate negative correlation between percent Black and resilience (r=-0.34) is consistent with structural disadvantage, not community deficits. This correlation was validated against independent life expectancy data (USALEEP), which showed an even stronger relationship (r=-0.44), confirming that the pattern is not an artifact of CDC PLACES methodology. Notably, percent Hispanic showed near-zero correlation with resilience (r=+0.01), suggesting different structural dynamics—a finding that merits separate investigation.

### Finding 3: Dramatic State-Level Variation

The national 0.43 SD gap masks state-level variation. Some states show much larger gaps; others show near-equity or even reversed patterns:

**States with LARGEST gaps (favoring white-majority communities):**

| State | Gap (SD) | White-Majority Mean | Minority-Majority Mean |
|-------|----------|---------------------|------------------------|
| DC | +1.87 | +1.12 | -0.75 |
| Michigan | +1.52 | +0.29 | -1.24 |
| Kentucky | +1.41 | +0.05 | -1.36 |
| Alabama | +1.39 | +0.36 | -1.03 |
| Ohio | +1.31 | +0.20 | -1.11 |

**States with SMALLEST gaps or REVERSED patterns:**

| State | Gap (SD) | White-Majority Mean | Minority-Majority Mean | Survives Bonferroni? |
|-------|----------|---------------------|------------------------|----------------------|
| New York | +0.12 | +0.05 | -0.06 | Yes |
| Arizona | +0.00 | -0.02 | -0.02 | No |
| California | -0.15 | -0.09 | +0.06 | **Yes** |
| Washington | -0.42 | -0.07 | +0.34 | **Yes** |

*Note: Oregon (-0.53 SD) and Nevada (-0.12 SD) did not survive Bonferroni correction and are excluded. Oregon had only 13 majority-minority tracts.*

**Interpretation:** In Washington and California, majority-minority communities show HIGHER resilience than majority-white communities—a pattern that survives rigorous multiple comparison correction (p<0.001 for both). This suggests that structural context, not racial composition per se, is associated with community resilience. The absence of this pattern in most states points to structural barriers that are present in some contexts but not others.

### Finding 4: Who Are the Outliers?

**High Resilience Tracts (Top 10%, score ≥ +1.11):**
- N = 5,389 tracts
- Mean % Black: 10.3% (vs. 13.4% nationally)
- Mean % Hispanic: 17.0% (vs. 17.1% nationally)
- Majority-minority: 26.5% (same as national rate)
- Mean poverty rate: 12.5% (vs. 13.5% nationally)
- Mean % Bachelor's+: 48.9% (vs. 32.2% nationally)

**Low Resilience Tracts (Bottom 10%, score ≤ -1.21):**
- N = 5,389 tracts
- Mean % Black: **39.7%** (vs. 13.4% nationally)
- Mean % Hispanic: 16.6% (vs. 17.1% nationally)
- **Majority-minority: 56.2%** (vs. 26.4% nationally)
- Mean poverty rate: 24.4% (vs. 13.5% nationally)
- Mean % Bachelor's+: 19.2% (vs. 32.2% nationally)

Low-resilience tracts are disproportionately Black (39.7% vs. 13.4%) and majority-minority (56.2% vs. 26.4%). High-resilience tracts are slightly less Black than average but show similar Hispanic composition.

---

## Discussion

### Principal Findings

Our analysis reveals a 0.43 standard deviation gap in community health resilience between majority-white and majority-minority communities nationally. This gap is consistent with structural disadvantage—majority-minority communities appear to face barriers associated with worse health outcomes than their socioeconomic profile would predict.

However, the state-level variation (from +1.87 SD in DC to -0.42 SD in Washington) suggests that this pattern is not inevitable. Two states (Washington and California) show statistically robust reversed patterns where majority-minority communities outperform majority-white communities after Bonferroni correction. This variation is consistent with the hypothesis that structural context—not racial composition per se—is associated with community resilience, though the cross-sectional design precludes causal inference.

### The Hispanic Paradox in Resilience

One of our most striking findings is the near-zero correlation between percent Hispanic and resilience (r=+0.01), validated at r=+0.002 with USALEEP life expectancy data. This stands in stark contrast to the moderate negative correlation for percent Black (r=-0.34).

This pattern is consistent with the well-documented "Hispanic paradox" (also called the "Latino epidemiological paradox")—the observation that Hispanic Americans often show health outcomes similar to or better than non-Hispanic whites despite lower average socioeconomic status. Proposed mechanisms include:

1. **Healthy immigrant selection:** Those who migrate may be healthier on average
2. **Protective cultural factors:** Strong family networks, dietary patterns, social cohesion
3. **Selective return migration:** The "salmon bias" hypothesis suggests sicker individuals may return to origin countries

This finding merits dedicated investigation. If the structural conditions that enable resilience in Hispanic communities can be identified, they may offer insights for health promotion more broadly.

### The Education Gradient

Educational attainment showed the strongest positive correlation with resilience (r=+0.41). This association may operate through multiple pathways:

1. **Health literacy:** Higher education enables better navigation of health systems
2. **Employment quality:** College graduates access jobs with better health benefits
3. **Neighborhood selection:** Education enables residential choice in healthier environments
4. **Social capital:** Educational networks provide health-promoting resources

The policy implication is that investment in educational equity may be associated with improved health equity, though causal inference requires longitudinal or experimental designs.

### Why Some States Show Equity

Two states—Washington and California—show statistically robust reversed patterns after Bonferroni correction. Potential explanations include:

1. **Immigration and selection:** The healthy immigrant effect may boost resilience in communities with higher foreign-born populations
2. **Policy environment:** State-level health and social policies may buffer structural disadvantage
3. **Community organization:** Strong ethnic enclaves may provide protective social capital
4. **Demographic composition:** The specific mix of racial/ethnic groups and their geographic distribution may matter

**Critical sensitivity finding:** Majority-minority tracts in Washington and California have notably higher Asian composition (20.2% and 19.7%, respectively) compared to 10.0% nationally. When excluding Asian-plurality tracts (tracts where Asian is the largest racial/ethnic group) from California, the "reversed" pattern disappears entirely (gap becomes +0.18 SD, favoring white-majority tracts). This suggests the California reversed pattern may be attributable primarily to tracts with high Asian composition rather than a general structural advantage for all minority groups. Washington's reversed pattern persists even after this sensitivity test, suggesting different dynamics.

**Important caveats on this finding:** (1) "Asian-American" aggregates heterogeneous communities with vastly different immigration histories, socioeconomic profiles, and health patterns (e.g., Hmong vs. Indian American vs. Filipino). (2) We do not interpret this finding as evidence of inherent community characteristics; rather, tracts with high Asian composition may benefit from structural factors such as selective immigration policies, geographic concentration in metropolitan areas with better healthcare infrastructure, or other unmeasured conditions. (3) This pattern should not be used to invoke "model minority" narratives, which obscure both the structural advantages some Asian-American communities experience and the significant health disparities within Asian-American subgroups.

Future research should disaggregate by specific racial/ethnic groups rather than using the majority-minority binary.

These explanations are speculative. Further research should investigate what structural conditions are associated with resilience equity in Washington and California, ideally using longitudinal or quasi-experimental designs that can better address causality.

### Implications for Practice

**1. Screen for equity in resilience-based programs.** Before using resilience scores for resource allocation, examine whether the metric shows equity across community types. If majority-minority communities systematically score lower, the metric may encode rather than address disparities.

**2. Target structural determinants, not communities.** Rather than labeling communities as "low resilience" (which risks stigmatization), identify the structural conditions associated with lower resilience: segregation, disinvestment, food deserts, pollution, lack of healthcare access. These conditions are actionable.

**3. Learn from equity exemplars.** Washington demonstrates resilience equity even after sensitivity testing; California's pattern requires further investigation given its dependence on Asian-plurality tracts. Specific majority-minority communities with high resilience in various states offer opportunities for qualitative study of protective structural factors.

**4. Invest in education.** The strong association between educational attainment and resilience suggests that educational equity is health equity. This requires sustained investment, not single interventions.

### Framing Matters

We emphatically reject deficit framing. The finding that majority-minority communities have lower average resilience does NOT mean:

- These communities are deficient
- Residents lack individual resilience
- The pattern is immutable

It DOES mean:

- Structural barriers are associated with lower community-level resilience
- Policy has failed to provide equitable protective conditions
- Investment should flow TO, not AWAY FROM, lower-resilience communities

The 56.2% majority-minority composition of low-resilience tracts co-occurs with decades of segregation, disinvestment, redlining, and environmental racism. These are policy failures, not community failures.

### Limitations

1. **Ecological fallacy:** Tract-level associations may not reflect individual-level relationships
2. **Cross-sectional design:** Cannot establish causality between structural factors and resilience
3. **Measurement error:** CDC PLACES estimates have uncertainty; ACS has sampling error
4. **Unmeasured confounders:** Many structural factors (segregation indices, historical redlining, environmental exposures) were not included
5. **State heterogeneity:** State-level analysis may mask within-state variation
6. **Construct terminology:** The term "resilience" may carry deficit-framing connotations when applied to communities scoring lower. Alternative framings such as "structural adequacy" (focusing on what environments provide rather than what communities achieve) may better capture the phenomenon. We retain "resilience" for consistency with prior literature but acknowledge this concern.
7. **Temporal mismatch in validation:** USALEEP uses 2010-2015 vital statistics while our primary data uses 2020-2024 CDC PLACES and 2022 ACS. While tract-level demographics are relatively stable over time, this 7-12 year gap introduces potential measurement error. COVID-19 mortality (2020-2022) may have altered patterns not captured in USALEEP. Future validation should use contemporaneous data when available.
8. **Measurement uncertainty not propagated:** CDC PLACES provides confidence intervals for tract estimates, but we did not propagate this uncertainty through our analysis. For small tracts, modeled estimates have substantial uncertainty that may affect the reliability of individual tract scores.
9. **Spatial autocorrelation:** We computed a state-level proxy for Moran's I by decomposing variance into between-state and within-state components. The ICC (intraclass correlation) of 0.0017 indicates that only 0.17% of variance in resilience scores is attributable to state-level spatial clustering, confirmed significant by permutation test (p = 0.001). However, this captures only between-state autocorrelation. True Moran's I with tract-level contiguity weights (based on geographic neighbors) would also capture within-state spatial dependence. Without tract boundary shapefiles, we could not compute proper Moran's I. The low ICC suggests modest practical impact on inference, and our multilevel model appropriately accounts for state-level clustering.
10. **Random slopes not reported in primary model:** A random slopes model allowing the race-resilience relationship to vary by state showed significantly better fit (LR χ² = 2535.9, p < 0.001), confirming substantial state-level heterogeneity. The random slope variance (τ₁₁) was 0.089 (SD = 0.30), indicating that state-specific effects range approximately ±0.6 SD around the average. The fixed-effects estimates reported represent average effects across states; individual state effects vary substantially.
11. **First-stage model explanatory power:** The resilience score is the residual from a first-stage regression with R² = 0.42, meaning 58% of variance in health burden remains unexplained. The resilience score therefore captures both true protective/risk factors and measurement error, omitted variable bias, and model misspecification. This may attenuate some correlations and introduce noise into estimates.
12. **Heteroscedasticity present:** Breusch-Pagan test on OLS residuals indicated significant heteroscedasticity (LM = 4281, p < 0.001). Residual variance ranged from 0.16 to 0.38 across fitted value quintiles, with higher-burden tracts showing greater variance. We computed heteroscedasticity-robust (HC3) standard errors: the robust SE for the majority-minority coefficient was 0.011 versus OLS SE of 0.010 (ratio 1.17). This modest adjustment does not materially change inference, and our multilevel model partially addresses heteroscedasticity by allowing different variance structures across states.
13. **Community voice absent:** This analysis relies entirely on secondary quantitative data and does not incorporate community perspectives. Communities may define resilience differently than our statistical measure, and community members would likely identify protective factors invisible to census and health data. Future research should employ community-based participatory methods to ensure findings reflect lived experience.

14. **No pre-registration:** This study was not pre-registered. While the primary research questions (national resilience gap, state-level variation, demographic correlates) were formulated before analysis, several investigations were exploratory, including: (a) the USALEEP validation analysis (conducted post-hoc to address peer review concerns about CDC PLACES methodology), (b) the Asian-plurality sensitivity analysis for California, and (c) the random slopes model. These exploratory analyses should be replicated in independent samples.

### Future Directions

1. **Segregation analysis:** Incorporate county-level dissimilarity indices
2. **Historical redlining:** Examine association between HOLC grades and contemporary resilience
3. **Environmental justice:** Add pollution burden and environmental hazard data
4. **Qualitative research:** Interview residents of high-resilience majority-minority communities to understand protective factors
5. **Longitudinal analysis:** Track whether resilience gaps are widening or narrowing

---

## Conclusions

Community health resilience is not equitably distributed. Majority-minority communities average 0.43 standard deviations lower resilience than majority-white communities nationally (multilevel z=-41.83, p<0.001), and the bottom 10% of tracts are 56.2% majority-minority.

State-level variation is substantial—from +1.87 SD (DC) to -0.42 SD (Washington)—and two states (Washington and California) show statistically robust reversed patterns after Bonferroni correction. This suggests that the relationship between racial composition and resilience is context-dependent, consistent with the role of structural factors rather than immutable characteristics.

Educational attainment emerged as the strongest correlate of resilience (r=+0.41). Investment in educational equity may be associated with improved health equity.

Practitioners should:
1. Audit resilience metrics for equity before use in resource allocation
2. Target structural determinants rather than labeling communities
3. Learn from states and communities that achieve resilience equity
4. Frame findings around structural barriers, not community deficits

The goal is not to celebrate resilience in some communities while ignoring its absence in others. The goal is to create structural conditions that enable all communities to thrive.

---

## References

1. Williams DR, Lawrence JA, Davis BA. Racism and health: evidence and needed research. Annu Rev Public Health. 2019;40:105-125.

2. Braveman P, Gottlieb L. The social determinants of health: it's time to consider the causes of the causes. Public Health Rep. 2014;129(Suppl 2):19-31.

3. Bailey ZD, Krieger N, Agénor M, Graves J, Linos N, Bassett MT. Structural racism and health inequities in the USA: evidence and interventions. Lancet. 2017;389(10077):1453-1463.

4. Krieger N. Epidemiology and the web of causation: has anyone seen the spider? Soc Sci Med. 1994;39(7):887-903.

5. Massey DS, Denton NA. American Apartheid: Segregation and the Making of the Underclass. Harvard University Press; 1993.

6. Rothstein R. The Color of Law: A Forgotten History of How Our Government Segregated America. Liveright; 2017.

7. CDC PLACES. Local Data for Better Health. Centers for Disease Control and Prevention. https://www.cdc.gov/places/

8. U.S. Census Bureau. American Community Survey 5-Year Estimates. 2022.

9. Norris FH, Stevens SP, Pfefferbaum B, Wyche KF, Pfefferbaum RL. Community resilience as a metaphor, theory, set of capacities, and strategy for disaster readiness. Am J Community Psychol. 2008;41(1-2):127-150.

10. Raudenbush SW, Bryk AS. Hierarchical Linear Models: Applications and Data Analysis Methods. 2nd ed. Sage Publications; 2002.

11. Arias E, Escobedo LA, Kennedy J, Fu C, Cisewski J. U.S. Small-area Life Expectancy Estimates Project: Methodology and Results Summary. Vital Health Stat 2. 2018;(181):1-40.

12. Markides KS, Coreil J. The health of Hispanics in the southwestern United States: an epidemiologic paradox. Public Health Rep. 1986;101(3):253-265.

13. Abraído-Lanza AF, Dohrenwend BP, Ng-Mak DS, Turner JB. The Latino mortality paradox: a test of the "salmon bias" and healthy migrant hypotheses. Am J Public Health. 1999;89(10):1543-1548.

14. Link BG, Phelan J. Social conditions as fundamental causes of disease. J Health Soc Behav. 1995;Spec No:80-94.

15. Diez Roux AV, Mair C. Neighborhoods and health. Ann N Y Acad Sci. 2010;1186:125-145.

16. Chetty R, Stepner M, Abraham S, et al. The association between income and life expectancy in the United States, 2001-2014. JAMA. 2016;315(16):1750-1766.

17. Cutler DM, Lleras-Muney A. Education and health: evaluating theories and evidence. NBER Working Paper No. 12352. 2006.

18. Osypuk TL, Acevedo-Garcia D. Beyond individual neighborhoods: a geography of opportunity perspective for understanding racial/ethnic health disparities. Health Place. 2010;16(6):1113-1123.

19. Cohen J. Statistical Power Analysis for the Behavioral Sciences. 2nd ed. Lawrence Erlbaum Associates; 1988.

20. Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J R Stat Soc Series B Stat Methodol. 1995;57(1):289-300.

21. Zhang X, Holt JB, Lu H, et al. Multilevel regression and poststratification for small-area estimation of population health outcomes: a case study of chronic obstructive pulmonary disease prevalence using the behavioral risk factor surveillance system. Am J Epidemiol. 2014;179(8):1025-1033.

22. Geronimus AT, Hicken M, Keene D, Bound J. "Weathering" and age patterns of allostatic load scores among blacks and whites in the United States. Am J Public Health. 2006;96(5):826-833.

---

## Acknowledgments

We acknowledge the communities represented in this analysis and the structural barriers they face. Data alone does not solve disparities; policy action does.

## Funding

This research received no external funding.

## Conflict of Interest

The author declares no conflicts of interest.

## Data Availability

CDC PLACES and ACS data are publicly available. Analysis code is available at https://github.com/cschuman/resilience-mapping.

---

## Supplementary Table: Full State-Level Resilience Gaps

The complete state-level analysis (all 51 states including DC, with gap magnitude, sample sizes, means for majority-white and majority-minority communities, p-values, and Bonferroni significance indicators) is available in the GitHub repository: https://github.com/cschuman/resilience-mapping/blob/main/data/state_gaps.csv
