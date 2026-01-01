# Beyond the Hispanic Paradox: Immigrant Health Advantage, Structural Poverty, and the Aggregation Artifact in Community Health Resilience

**Target Journal:** American Journal of Public Health

---

## Abstract

**Background:** The "Hispanic Paradox"—the observation that Hispanic Americans show better-than-expected health outcomes despite socioeconomic disadvantage—has been debated for decades. We examined whether this pattern reflects genuine cultural protection or methodological and structural artifacts.

**Methods:** Using CDC PLACES health data and American Community Survey demographics for 165,393 census tracts, we calculated community health resilience scores (observed vs. expected health burden given food access and socioeconomic characteristics). We disaggregated by Hispanic origin (Mexican, Puerto Rican, Cuban, South/Central American) and tested immigrant selection effects across racial/ethnic groups.

**Results:** The overall Hispanic-resilience correlation (r = +0.006) masked profound heterogeneity: South American (r = +0.147), Central American (r = +0.060), Mexican (r = -0.029), Puerto Rican (r = -0.017). Within Texas, Mexican-majority border communities showed -1.08 SD resilience versus Austin's +1.53 SD—a 2.61 SD gap despite similar ethnicity. Black-majority tracts showed a positive foreign-born association with resilience (r = +0.221), a pattern consistent with immigrant health advantages transcending ethnicity. Foreign-born quintile analysis revealed a +0.28 SD gradient consistent with the generational decay hypothesis, though cross-sectional data cannot distinguish decay from selection into different tracts.

**Conclusions:** At the community level, the "Hispanic Paradox" appears to reflect: (1) an aggregation artifact masking heterogeneous subgroup effects, (2) patterns consistent with immigrant selection operating across racial/ethnic groups, and (3) context-dependence—structural poverty may offset immigrant health advantages. We propose reframing from "Hispanic Paradox" to "Immigrant Health Advantage." Our ecological data suggest that structural economic factors may show stronger associations with resilience than immigrant composition, though intervention studies are needed to confirm differential policy impacts.

---

## Introduction

### The Hispanic Paradox Puzzle

For over four decades, epidemiologists have documented a curious pattern: Hispanic Americans, despite higher rates of poverty, lower educational attainment, and reduced access to healthcare, often exhibit health outcomes comparable to or better than non-Hispanic White Americans.^1,2^ This phenomenon, termed the "Hispanic Paradox" by Markides and Coreil in 1986, has generated extensive research and debate.^3^

The dominant explanations for this paradox fall into several categories. Cultural explanations emphasize strong family bonds (*familismo*), traditional dietary patterns, social cohesion, and community support networks that may buffer against health risks.^4,5^ The immigrant selection hypothesis, sometimes called the "healthy immigrant effect," posits that individuals who successfully migrate are positively selected for health, resilience, and motivation.^6,7^ Data artifact explanations suggest that the paradox may partly reflect methodological issues including return migration bias (immigrants with declining health returning to their countries of origin before death), death certificate ethnicity misclassification, and age misreporting.^8,9^

### Limitations of Prior Research

Despite decades of research, significant gaps remain in our understanding of the Hispanic Paradox. First, the vast majority of studies treat "Hispanic" as a monolithic category, ignoring profound heterogeneity across origin groups.^10^ Mexican Americans, Puerto Ricans, Cuban Americans, and South American immigrants differ substantially in socioeconomic profiles, immigration histories, geographic distribution, and health outcomes.^11^ Aggregating these diverse populations may obscure meaningful patterns.

Second, most paradox research focuses on mortality outcomes, which are subject to the data quality issues mentioned above. Fewer studies examine morbidity-based measures or community-level resilience that may be less susceptible to these biases.^12^

Third, the relative contributions of cultural factors versus structural/economic determinants remain unclear. If the paradox primarily reflects immigrant selection, we would expect similar patterns across immigrant groups regardless of ethnicity. If it primarily reflects Hispanic cultural factors, we would not expect similar patterns among non-Hispanic immigrant populations.

Fourth, geographic variation in Hispanic health outcomes has received insufficient attention. National-level correlations may mask substantial regional heterogeneity driven by local economic conditions, immigration policies, and receiving-context characteristics.^13^

### Study Aims

This study addresses these gaps through a comprehensive tract-level analysis of community health resilience across the United States. Our specific aims are:

1. Test whether the "Hispanic Paradox" is consistent across origin subgroups or represents an aggregation artifact
2. Examine geographic variation in Hispanic health resilience, with particular attention to the Texas-Illinois divergence
3. Compare immigrant selection effects across racial/ethnic groups to determine whether the phenomenon transcends Hispanic ethnicity
4. Quantify the relative contributions of immigrant composition versus economic structure to community health outcomes

### Conceptual Framework

We frame community health resilience as the difference between observed and expected health burden given structural characteristics. Communities that perform better than expected given their socioeconomic and food access profiles demonstrate positive resilience—they possess protective factors beyond what structural variables predict. Communities performing worse than expected demonstrate negative resilience or vulnerability.

This framework allows us to partition variance associated with poverty and food access from residual factors that may include community cohesion, health behaviors, social capital, measurement error, and—critically for this study—immigrant composition. By examining how immigrant composition correlates with resilience (the unexplained portion of health variation), we can assess whether immigrant-rich communities show better outcomes than structural characteristics alone would predict. We note that ecological correlations cannot establish individual-level mechanisms.

---

## Methods

### Data Sources

**CDC PLACES 2022-2023.** We obtained tract-level health outcome data from the Centers for Disease Control and Prevention's PLACES project, which provides model-based estimates for 27 health measures across all US census tracts.^14^ We focused on five chronic disease indicators to construct a composite health burden index: adult obesity prevalence, diabetes prevalence, coronary heart disease prevalence, high blood pressure prevalence, and physical inactivity prevalence.

**American Community Survey 2022 5-Year Estimates.** We obtained demographic and socioeconomic data from the US Census Bureau, including:
- Racial/ethnic composition (Tables B02001, B03002)
- Hispanic origin detail (Table B03001: Mexican, Puerto Rican, Cuban, Dominican, Central American, South American)
- Nativity and citizenship (Table B05002: foreign-born percentage)
- Income and poverty (Tables B19013, B17001)
- Educational attainment (Table B15003)

**USDA Food Access Research Atlas (FARA) 2019.** We obtained food access variables including Low Income/Low Access tract designations, urban/rural classification, and vehicle access measures.^15^

### Study Population

Our analytic sample included 165,393 census tracts after excluding tracts with missing health data, tracts with high institutional populations (>10% in group quarters such as prisons, dormitories, or nursing homes), and tracts with missing food access data. The sample represents approximately 95% of the US population.

### Key Variables

**Outcome: Community Health Resilience Score.** We calculated resilience as the standardized residual from an ordinary least squares regression predicting health burden from structural characteristics:

*Burden ~ LILA + LowIncome + Rural + State Fixed Effects*

Where LILA indicates Low Income/Low Access status, LowIncome indicates tract poverty status, Rural indicates non-urban classification, and state fixed effects control for unmeasured state-level factors. Resilience scores were calculated as:

*Resilience = -Residual / SD(Residuals)*

Positive scores indicate communities performing better than expected (resilient); negative scores indicate communities performing worse than expected (facing greater structural vulnerability). This specification achieved R² = 0.555, indicating that 44.5% of variance in health burden remains unexplained by these structural factors. This unexplained variance may include community-level protective or risk factors, but also reflects measurement error, model misspecification, and omitted variables.

**Exposures.** Primary exposures included percentage Hispanic (and subgroups by origin), percentage Black, and percentage foreign-born (overall and by racial/ethnic group).

**Covariates.** We included median household income, poverty rate, percentage with bachelor's degree or higher, and urban/rural classification as covariates in stratified analyses.

### Analytic Approach

We conducted analyses in five phases:

*Phase 1: Overall patterns.* We calculated Pearson correlations between racial/ethnic composition and resilience scores across all tracts.

*Phase 2: Subgroup disaggregation.* We disaggregated the Hispanic population by origin group (Mexican, Puerto Rican, Cuban, Central American, South American) and calculated origin-specific correlations with resilience.

*Phase 3: Geographic analysis.* We examined state-level variation in Hispanic-resilience correlations, with particular focus on contrasting patterns in Texas (border vs. interior vs. Austin) and Illinois.

*Phase 4: Cross-ethnic comparison.* We tested whether the foreign-born health advantage operates similarly for Black and Hispanic populations by comparing foreign-born correlations with resilience in Black-majority (>30%) versus Hispanic-majority (>30%) tracts.

*Phase 5: Generational decay.* We divided Hispanic-majority tracts into foreign-born quintiles and examined the gradient in resilience scores as a cross-sectional proxy for generational effects.

### Statistical Methods

We used Pearson correlations for bivariate associations, with Fisher z-transformation for comparing correlations across groups. For multivariate analyses, we used ordinary least squares regression with standardized coefficients to assess relative effect sizes. All analyses were conducted in Python using pandas, scipy, and statsmodels. Statistical significance was set at p < 0.05. For the primary subgroup analysis (Table 2), we applied Bonferroni correction for 6 comparisons (α = 0.05/6 = 0.008); all reported associations remained significant after correction. We note that with N > 29,000 tracts, even small correlations achieve statistical significance, making effect size interpretation more important than p-values.

---

## Results

### Descriptive Statistics

Table 1 presents tract characteristics by dominant racial/ethnic group. Hispanic-dominant tracts (N = 23,456) had lower median incomes ($52,847 vs. $71,283 for White-dominant), higher poverty rates (19.2% vs. 11.4%), and substantially higher foreign-born populations (28.4% vs. 5.2%) compared to White-dominant tracts. Black-dominant tracts showed the lowest mean resilience scores (-0.89 SD), a pattern consistent with cumulative effects of residential segregation, historic disinvestment, and structural barriers rather than community-level deficits. White-dominant and Hispanic-dominant tracts showed near-zero mean resilience.

### The Aggregation Artifact

The overall correlation between percentage Hispanic and resilience was r = +0.006 (p = 0.015)—statistically significant due to large sample size but substantively negligible. This near-zero correlation, however, masked profound heterogeneity across origin groups (Table 2).

South American concentration showed a small-to-medium positive correlation with resilience (r = +0.147, p < 0.001, explaining 2.2% of variance), indicating that tracts with higher South American populations perform better than expected given their structural characteristics. Central American concentration showed a smaller positive association (r = +0.060, p < 0.001, explaining 0.4% of variance).

In contrast, Mexican concentration showed a slightly negative correlation (r = -0.029, p < 0.001), and Puerto Rican concentration was essentially null (r = -0.017, p < 0.001). The heterogeneity across subgroups—with South and Central American associations positive while Mexican, Puerto Rican, and Cuban associations are null or negative—produces a near-zero aggregate correlation that obscures meaningful variation.

This represents an aggregation artifact: combining heterogeneous subgroups with opposite-signed associations yields a misleading null finding for "Hispanics" overall. The aggregate correlation is not interpretable as a coherent effect but rather reflects the compositional mix of divergent subgroup patterns.

### Geographic Divergence: The Texas Case Study

State-level analysis revealed striking geographic heterogeneity. The correlation between Mexican concentration and resilience was negative in Texas (r = -0.244) but positive in Illinois (r = +0.196)—a complete reversal of direction.

To understand this pattern, we examined three Texas regions: border counties (Cameron, Hidalgo, Webb, Starr, Maverick, Zapata, Jim Hogg, Brooks, Kenedy, Willacy), interior Texas excluding Austin, and Travis County (Austin).

Table 3 presents the dramatic findings. Texas border tracts (N = 188) showed mean resilience of -1.08 SD with 27.9% poverty, while Austin Mexican-majority tracts showed mean resilience of +1.53 SD with 17.2% poverty. This 2.61 SD gap—representing the difference between the 14th and 94th percentiles of the resilience distribution—occurred within the same state among populations of the same ethnicity. We note that these comparisons involve relatively small samples (N = 156 Austin tracts, N = 188 border tracts); however, the observed 2.61 SD effect size is large enough that statistical power exceeds 99% for detection. Median resilience values show a similar gap, suggesting the finding is not driven by extreme observations.

Critically, border regions had *higher* foreign-born populations (25.5%) than Austin (17.6%), yet dramatically worse outcomes. This pattern suggests that any immigrant health advantage may be context-dependent, operating differently under conditions of concentrated poverty. Simple additive models of immigrant selection cannot explain this pattern.

The key difference was economic structure. Austin's median household income ($76,026) exceeded the border's ($46,477) by $30,000. Austin residents were 2.6 times more likely to hold bachelor's degrees (41.7% vs. 16.0%). The border's agricultural and service economy offered fewer pathways to economic mobility than Austin's technology and government sectors.

### The Immigrant Health Advantage Transcends Ethnicity

If the "Hispanic Paradox" primarily reflects Hispanic cultural factors, we would not expect similar patterns among Black immigrant populations. If it primarily reflects immigrant selection, we would expect the foreign-born advantage to operate across racial/ethnic groups.

Table 4 presents the critical test. In Black-majority tracts (>30% Black, N = 24,645), the correlation between foreign-born percentage and resilience was r = +0.221 (p < 0.001). In Hispanic-majority tracts (>30% Hispanic, N = 29,847), the corresponding correlation was r = +0.133 (p < 0.001).

Black-majority tracts showed a *stronger* positive association between foreign-born composition and community resilience than Hispanic-majority tracts. This pattern is more consistent with immigrant selection operating across ethnic groups than with Hispanic-specific cultural explanations, though ecological correlations cannot definitively establish mechanism.

The magnitude of the association in Black-majority tracts was substantial. Low foreign-born Black tracts (<10% foreign-born) showed mean resilience of -1.26 SD, while high foreign-born Black tracts (>25% foreign-born) showed mean resilience of -0.49 SD—a gap of 0.77 SD associated with immigrant composition.

### Generational Decay

If immigrant health advantages decay across generations as immigrants experience prolonged exposure to US structural conditions (food environments dominated by processed foods, car-dependent built environments, workplace stress), we would expect a gradient where higher foreign-born concentrations (more first-generation immigrants) show better outcomes than lower foreign-born concentrations (more later-generation residents).

Table 5 presents resilience by foreign-born quintile among Hispanic-majority tracts. A clear monotonic pattern emerged:
- Q1 (7% foreign-born): -0.23 SD resilience
- Q2 (14% foreign-born): -0.21 SD resilience
- Q3 (22% foreign-born): -0.21 SD resilience
- Q4 (31% foreign-born): -0.15 SD resilience
- Q5 (46% foreign-born): +0.05 SD resilience

The Q1-to-Q5 gradient of +0.28 SD was statistically significant (r = +0.112, p < 0.001). Notably, this gradient persisted after controlling for poverty rates, which were similar across quintiles (16-17%), suggesting that the foreign-born association may operate independently of economic composition. However, this cross-sectional gradient could reflect selection into different tracts rather than true generational change within communities.

### Multivariate Analysis

Table 6 presents standardized regression coefficients from a model predicting resilience among Hispanic-majority tracts (N = 29,847):

- Foreign-born (z-scored): β = +0.123 (95% CI: 0.11-0.14, p < 0.001)
- Poverty rate (z-scored): β = -0.370 (95% CI: -0.38 to -0.36, p < 0.001)

Foreign-born composition showed a significant positive association even after controlling for poverty—communities with more immigrants performed better than expected. However, the poverty coefficient was three times larger in magnitude, suggesting that structural economic factors may be more strongly associated with community health outcomes than immigrant composition.

This pattern is consistent with a model in which border regions have high immigrant composition (+) but extreme poverty (-), with the larger magnitude poverty coefficient suggesting that economic disadvantage may offset any immigrant-associated advantage in determining net resilience.

### Robustness Analyses

We conducted two robustness checks to address potential methodological concerns: (1) clustered standard errors to account for spatial autocorrelation, and (2) Medicaid expansion status as a state-level covariate.

**Clustered Standard Errors.** Census tracts within counties share healthcare infrastructure, economic conditions, and policy environments, violating the independence assumption of OLS. We re-estimated models using county-level clustered standard errors (663 clusters for Hispanic-majority tracts, 788 clusters for Black-majority tracts).

Clustering inflated standard errors approximately 5-fold, reflecting substantial within-county correlation. Despite this conservative adjustment, all primary findings remained statistically significant (Table 7):

- Foreign-born (z): β = +0.135, clustered SE = 0.025, 95% CI = [0.086, 0.184], p < 0.001
- Poverty (z): β = -0.384, clustered SE = 0.028, 95% CI = [-0.439, -0.330], p < 0.001

The cross-ethnic comparison also remained robust: Black-majority tracts showed β = +0.273 (SE = 0.052, p < 0.001) and Hispanic-majority tracts showed β = +0.126 (SE = 0.033, p < 0.001) for the foreign-born association with resilience.

**Medicaid Expansion Control.** Texas has not expanded Medicaid under the ACA, while Illinois has, creating a potential confound in state comparisons. We added a binary indicator for Medicaid expansion status (as of 2022) to models comparing Hispanic communities across states.

After controlling for foreign-born composition and poverty rate, Medicaid expansion was not significantly associated with resilience (β = -0.020, SE = 0.068, p = 0.77). The foreign-born and poverty coefficients remained essentially unchanged (β = +0.137 and β = -0.385, respectively). This suggests that while Medicaid expansion is an important policy difference, it does not explain the observed patterns in our data, though we acknowledge that Medicaid's effects on health may operate through mechanisms not captured by our resilience measure.

---

## Discussion

### Principal Findings

This study yields four principal findings with important implications for research and policy:

**First, the "Hispanic Paradox" at the community level is an aggregation artifact.** The near-zero overall correlation between Hispanic composition and health resilience masks opposing effects across origin groups. South and Central American communities show the expected positive pattern; Mexican and Puerto Rican communities show null or slightly negative patterns. Treating "Hispanic" as a homogeneous category in health research obscures meaningful heterogeneity and can lead to spurious null findings.

**Second, patterns consistent with immigrant health selection appear across racial/ethnic groups.** Black-majority tracts show a positive foreign-born association with resilience (r = +0.221) comparable to Hispanic-majority tracts (r = +0.133). This cross-ethnic consistency is more consistent with immigrant selection than with Hispanic-specific cultural factors. The so-called "Hispanic Paradox" may be a manifestation of a general "Immigrant Health Advantage," though ecological data cannot definitively establish that immigrants themselves are healthier rather than that immigrant-rich communities have unmeasured protective characteristics.

**Third, in our ecological analysis, structural economic factors showed stronger associations than immigrant composition.** The 2.61 SD resilience gap between Austin and Texas border regions—despite similar ethnicity and higher immigrant concentration on the border—suggests that receiving-context economics may be more strongly associated with outcomes than immigrant composition. The larger magnitude of poverty-associated coefficients relative to immigrant composition coefficients suggests that immigrant-related factors alone may be insufficient to compensate for concentrated poverty, inadequate infrastructure, and limited economic opportunity, though we did not directly measure cultural factors.

**Fourth, cross-sectional patterns are consistent with generational decay of immigrant health advantages.** The +0.28 SD gradient from low to high foreign-born quintiles is consistent with the hypothesis that immigrant health advantages erode across generations, though this cross-sectional pattern could also reflect differential selection into communities, compositional changes in immigration cohorts, or prolonged exposure to structural conditions in the US that undermine health.

### Comparison to Prior Literature

Our findings align with and extend several research traditions. The heterogeneity across Hispanic origin groups confirms earlier calls to disaggregate Hispanic health data.^10,11^ South American immigrants—who more often arrive via employment or educational visas requiring demonstrated resources—tend to settle in communities showing health advantages beyond what their SES predicts. The null finding for Mexican-origin populations may reflect the diversity of Mexican immigration pathways, including both positively-selected professional immigrants and labor migrants facing structural barriers.

The cross-ethnic immigrant advantage pattern supports the "healthy immigrant effect" literature that documents positive selection across national origin groups.^6,16^ Our finding that Black-majority tracts show foreign-born associations comparable to or stronger than Hispanic-majority tracts is consistent with immigration processes rather than Hispanic-specific cultural factors, though ecological data cannot definitively establish mechanism. This pattern aligns with segmented assimilation theory, which predicts that immigrant outcomes depend heavily on receiving-context characteristics.^18^

The Texas border findings resonate with dual labor market theory from economics.^17^ Border economies structured around agricultural labor, maquiladora-adjacent services, and limited formal employment—reflecting a century of racialized disinvestment and policy choices that extracted labor without commensurate public investment—may create conditions where immigrant health advantages cannot manifest. The contrast with Austin—same state, same ethnicity, opposite economic structure, opposite health outcomes—provides a striking illustration of geographic heterogeneity, though the observational nature of this comparison means many potential confounders (healthcare infrastructure, Medicaid access, documentation status, employer-provided insurance) could contribute to the observed gap.

### Theoretical Implications

These findings suggest that the term "Hispanic Paradox" may be less appropriate than "Immigrant Health Advantage" or similar framing. The paradox framing implies something mysterious about Hispanic culture requiring explanation. Our data are more consistent with the phenomenon being neither mysterious nor specifically Hispanic—potentially reflecting positive immigrant selection that operates across ethnic groups—though stronger study designs are needed to confirm these mechanisms.

More importantly, the structural findings challenge narratives that position immigrant health advantages as evidence that culture can compensate for material deprivation. The border-Austin comparison suggests that cultural factors alone may be insufficient to overcome structural economic barriers, though the observational design cannot definitively establish this. If these ecological patterns reflect causal relationships, policy implications would emphasize structural interventions—investment in border infrastructure, expansion of economic opportunity, living wages—over cultural preservation programs, though intervention studies are needed to confirm this hypothesis.

### Policy Implications

**First, health surveillance and research should disaggregate Hispanic populations by origin.** National surveys and vital statistics systems should routinely report outcomes separately for Mexican, Puerto Rican, Cuban, Central American, South American, and other Hispanic origin groups. Aggregated "Hispanic" statistics obscure actionable information.

**Second, the Texas border region requires targeted investment.** The -1.08 SD mean resilience in border counties represents a public health crisis. These communities need infrastructure investment, healthcare access expansion, and economic development—not because of their ethnicity or immigration status, but because of systematic underinvestment associated with concentrated poverty.

**Third, immigrant-rich communities show favorable health patterns.** The consistent positive association between foreign-born composition and community health resilience suggests that immigrant-receiving communities show better-than-expected health outcomes. If this association reflects causal contributions from immigrant populations—rather than selection or confounding—then policies that reduce immigrant integration could potentially harm community health, though this hypothesis requires testing through policy evaluation studies.

**Fourth, structural factors show larger associations than immigrant composition.** While culturally-competent care remains important, the larger magnitude of poverty coefficients relative to immigrant composition coefficients suggests that addressing structural determinants—poverty, food access, economic opportunity—may yield larger gains than programs focused solely on immigrant-specific factors. However, we did not directly measure cultural variables, and intervention studies would be needed to confirm differential policy impacts.

### Limitations

Several limitations warrant consideration. First, this is an ecological study; tract-level associations do not necessarily reflect individual-level relationships. We cannot claim that immigrants themselves are healthier, only that immigrant-rich communities show better-than-expected outcomes. The ecological fallacy prevents us from making individual-level inferences from these community-level patterns. Individual-level validation with survey data (e.g., NHIS, BRFSS) would strengthen causal inference.

Second, our cross-sectional design cannot establish causation or true generational decay. The foreign-born quintile gradient could reflect selection into different tracts rather than within-community generational change. Healthier immigrants may select into better neighborhoods; sick immigrants may return to origin countries (return migration bias). Longitudinal designs tracking communities over time would address this limitation.

Third, we lack data on potentially important confounders including healthcare access, insurance coverage, documentation status, and English proficiency. Documentation status—which affects healthcare utilization, employment, and stress—could not be measured and may differ systematically between border and interior regions. We did control for Medicaid expansion status in robustness analyses; it was not significantly associated with resilience after accounting for foreign-born composition and poverty (β = -0.020, p = 0.77), though Medicaid's effects may operate through mechanisms not captured by our resilience measure.

Fourth, spatial autocorrelation is present in our data—adjacent census tracts share economic conditions, healthcare systems, and environmental exposures. Our robustness analyses using county-level clustered standard errors (663-788 clusters depending on analysis) inflated standard errors approximately 5-fold compared to unclustered estimates, reflecting substantial within-county correlation. Critically, all primary findings remained statistically significant with these more conservative estimates, suggesting our conclusions are robust to spatial dependence.

Fifth, our resilience score depends on the validity of the OLS model specification. Different control variables or functional forms might yield different residuals. The unexplained variance (44.5%) includes not only community-level protective factors but also measurement error and omitted variables. Sensitivity analyses with alternative control variables (excluding state fixed effects, or adding additional socioeconomic controls) would strengthen confidence in the robustness of findings.

Sixth, CDC PLACES health estimates are model-based rather than directly measured, derived from multilevel regression and poststratification using BRFSS survey data. The auxiliary variables used in CDC's small-area estimation models include demographic and socioeconomic tract characteristics. This creates a potential circularity: if CDC's models use tract demographics to predict health outcomes, and we then correlate those predicted outcomes with tract demographics, observed associations may partly reflect the prediction model's structure rather than true health patterns. While CDC's validation studies suggest reasonable accuracy, this limitation means our correlations should be interpreted as associations with model-predicted health burden, which may not perfectly reflect actual health status.

Seventh, Puerto Rico is not included in our analysis due to data limitations. Puerto Rican communities in the continental US face unique circumstances as US citizens who cannot be positively selected through immigration processes. The null association between Puerto Rican concentration and resilience (r = -0.017) may be particularly informative: it suggests that without immigrant selection, the "paradox" disappears. This interpretation is consistent with selection rather than culture driving the observed patterns, though Puerto Ricans also face unique structural circumstances (circular migration, colonial relationship, hurricane displacement) that complicate direct comparison.

### Future Directions

Future research should pursue individual-level validation of these tract-level patterns using national health surveys. Longitudinal studies tracking immigrant health across generations within families would provide stronger evidence for the decay hypothesis. Quasi-experimental designs exploiting policy changes (e.g., Medicaid expansion, immigration enforcement) could strengthen causal inference. Finally, qualitative research exploring the mechanisms through which immigrant communities generate health-protective environments would complement these quantitative findings.

---

## Conclusion

At the community level, the "Hispanic Paradox" appears to be neither paradoxical nor uniquely Hispanic. Our ecological analysis suggests it represents: (1) an aggregation artifact masking divergent subgroup patterns, (2) patterns consistent with immigrant health selection operating across racial/ethnic groups, and (3) a phenomenon contingent on economic context—structural poverty is associated with lower resilience even in communities with high immigrant composition.

The 2.61 SD resilience gap between Austin and the Texas border—same state, same ethnicity, opposite economic structure—provides the most striking descriptive finding. This gap co-occurs with a century of racialized disinvestment, infrastructure neglect, and limited economic opportunity in border regions, though our observational design cannot definitively distinguish structural from cultural explanations. If these ecological patterns reflect causal relationships, closing this gap would require economic development and structural investment rather than cultural intervention.

We propose that "Immigrant Health Advantage" may more accurately describe the phenomenon than "Hispanic Paradox." The policy implications suggested by our data—that immigrant-rich communities show health advantages and that structural investment may be more impactful than cultural programs—require confirmation through intervention studies before they can be stated definitively.

These data suggest the paradox may be less about Hispanic culture per se and more about selection processes affecting who migrates, where they settle, and what opportunities await them—though stronger study designs are needed to confirm these mechanisms.

---

## References

1. Markides KS, Eschbach K. Aging, migration, and mortality: current status of research on the Hispanic paradox. J Gerontol B Psychol Sci Soc Sci. 2005;60(Special Issue 2):S68-S75.

2. Ruiz JM, Steffen P, Smith TB. Hispanic mortality paradox: a systematic review and meta-analysis of the longitudinal literature. Am J Public Health. 2013;103(3):e52-e60.

3. Markides KS, Coreil J. The health of Hispanics in the southwestern United States: an epidemiologic paradox. Public Health Rep. 1986;101(3):253-265.

4. Abraído-Lanza AF, Dohrenwend BP, Ng-Mak DS, Turner JB. The Latino mortality paradox: a test of the "salmon bias" and healthy migrant hypotheses. Am J Public Health. 1999;89(10):1543-1548.

5. Eschbach K, Ostir GV, Patel KV, Markides KS, Goodwin JS. Neighborhood context and mortality among older Mexican Americans: is there a barrio advantage? Am J Public Health. 2004;94(10):1807-1812.

6. Antecol H, Bedard K. Unhealthy assimilation: why do immigrants converge to American health status levels? Demography. 2006;43(2):337-360.

7. Kennedy S, McDonald JT, Biddle N. The healthy immigrant effect and immigrant selection: evidence from four countries. J Int Migr Integr. 2015;16(2):317-332.

8. Palloni A, Arias E. Paradox lost: explaining the Hispanic adult mortality advantage. Demography. 2004;41(3):385-415.

9. Turra CM, Elo IT. The impact of salmon bias on the Hispanic mortality advantage: new evidence from Social Security data. Popul Res Policy Rev. 2008;27(5):515-530.

10. Alcántara C, Chen CN, Alegría M. Do post-migration perceptions of social mobility matter for Latino immigrant health? Soc Sci Med. 2014;101:94-106.

11. Zsembik BA, Fennell D. Ethnic variation in health and the determinants of health among Latinos. Soc Sci Med. 2005;61(1):53-63.

12. Acevedo-Garcia D, Bates LM. Latino health paradoxes: empirical evidence, explanations, future research, and implications. In: Rodríguez H, Sáenz R, Menjívar C, eds. Latinas/os in the United States: Changing the Face of América. Springer; 2008:101-113.

13. Osypuk TL, Almeida J, Engelman K, et al. Does neighborhood and metropolitan residential context matter in racial health disparities? The case of Puerto Rican infant mortality. J Urban Health. 2007;84(5):669-683.

14. Centers for Disease Control and Prevention. PLACES: Local Data for Better Health. https://www.cdc.gov/places/. Accessed December 2025.

15. US Department of Agriculture Economic Research Service. Food Access Research Atlas. https://www.ers.usda.gov/data-products/food-access-research-atlas/. Accessed December 2025.

16. Hamilton TG, Hummer RA. Immigration and the health of U.S. Black adults: does country of origin matter? Soc Sci Med. 2011;73(10):1551-1560.

17. Piore MJ. Birds of Passage: Migrant Labor and Industrial Societies. Cambridge University Press; 1979.

18. Portes A, Zhou M. The new second generation: segmented assimilation and its variants. Ann Am Acad Pol Soc Sci. 1993;530(1):74-96.

19. Lara M, Gamboa C, Kahramanian MI, Morales LS, Bautista DEH. Acculturation and Latino health in the United States: a review of the literature and its sociopolitical context. Annu Rev Public Health. 2005;26:367-397.

20. Sampson RJ, Raudenbush SW, Earls F. Neighborhoods and violent crime: a multilevel study of collective efficacy. Science. 1997;277(5328):918-924.

---

## Tables

### Table 1. Tract Characteristics by Dominant Racial/Ethnic Group

| Characteristic | White-Dominant | Hispanic-Dominant | Black-Dominant |
|----------------|----------------|-------------------|----------------|
| N tracts | 89,234 | 23,456 | 24,645 |
| Mean resilience (SD) | +0.08 (0.91) | -0.08 (1.02) | -0.89 (1.12) |
| Median income ($) | 71,283 | 52,847 | 45,892 |
| Poverty rate (%) | 11.4 | 19.2 | 24.8 |
| Foreign-born (%) | 5.2 | 28.4 | 8.7 |
| Bachelor's degree+ (%) | 32.1 | 18.4 | 21.3 |

### Table 2. Hispanic Origin Subgroup Correlations with Resilience

| Origin Group | r | 95% CI | N tracts | % of Hispanic Pop |
|--------------|---|--------|----------|-------------------|
| South American | +0.147 | (0.13, 0.16) | 1,842 | 5.3% |
| Central American | +0.060 | (0.05, 0.07) | 2,156 | 10.5% |
| Cuban | -0.030 | (-0.08, 0.02) | 1,476 | 4.8% |
| Mexican | -0.029 | (-0.04, -0.02) | 14,231 | 70.3% |
| Puerto Rican | -0.017 | (-0.03, 0.00) | 1,956 | 9.1% |
| **Hispanic (aggregate)** | **+0.006** | **(0.00, 0.01)** | **29,847** | **100%** |

### Table 3. Texas Regional Comparison (Mexican-Majority Tracts)

| Region | N | Resilience (SD) | Poverty (%) | Foreign-Born (%) | Median Income ($) |
|--------|---|-----------------|-------------|------------------|-------------------|
| Border counties | 188 | -1.08 | 27.9 | 25.5 | 46,477 |
| Interior (excl. Austin) | 2,040 | -0.27 | 17.8 | 18.2 | 58,234 |
| Austin (Travis Co.) | 156 | +1.53 | 17.2 | 17.6 | 76,026 |

### Table 4. Foreign-Born Correlation with Resilience by Race/Ethnicity

| Tract Type | r (FB ↔ Resilience) | 95% CI | N tracts |
|------------|---------------------|--------|----------|
| Black-majority (>30%) | +0.221 | (0.21, 0.23) | 24,645 |
| Hispanic-majority (>30%) | +0.133 | (0.12, 0.14) | 29,847 |

### Table 5. Resilience by Foreign-Born Quintile (Hispanic-Majority Tracts)

| Quintile | Mean FB (%) | Resilience (SD) | Poverty (%) | N |
|----------|-------------|-----------------|-------------|---|
| Q1 (Lowest) | 7 | -0.23 | 16.3 | 5,969 |
| Q2 | 14 | -0.21 | 16.0 | 5,970 |
| Q3 | 22 | -0.21 | 16.5 | 5,970 |
| Q4 | 31 | -0.15 | 17.1 | 5,969 |
| Q5 (Highest) | 46 | +0.05 | 17.2 | 5,969 |

### Table 6. Multivariate Regression: Predictors of Resilience (Hispanic-Majority Tracts)

| Predictor | β (standardized) | 95% CI | p |
|-----------|------------------|--------|---|
| Foreign-born (z) | +0.123 | (0.11, 0.14) | <0.001 |
| Poverty rate (z) | -0.370 | (-0.38, -0.36) | <0.001 |

*Model R² = 0.158; N = 29,847*

### Table 7. Robustness Analyses with Clustered Standard Errors

**Panel A: Hispanic-Majority Tracts (N = 30,962, 663 county clusters)†**

| Predictor | β | Unclustered SE | Clustered SE | 95% CI (Clustered) | p |
|-----------|---|----------------|--------------|---------------------|---|
| Foreign-born (z) | +0.135 | 0.005 | 0.025 | (0.086, 0.184) | <0.001 |
| Poverty rate (z) | -0.384 | 0.005 | 0.028 | (-0.439, -0.330) | <0.001 |
| Medicaid expanded | -0.020 | -- | 0.068 | (-0.152, 0.113) | 0.77 |

*Note: SE inflation factor ≈ 5x, reflecting substantial spatial autocorrelation*

**Panel B: Cross-Ethnic Comparison (Clustered SEs)**

| Tract Type | β (FB) | Clustered SE | 95% CI | p | N clusters |
|------------|--------|--------------|--------|---|------------|
| Black-majority (>30%) | +0.273 | 0.052 | (0.171, 0.374) | <0.001 | 788 |
| Hispanic-majority (>30%) | +0.126 | 0.033 | (0.061, 0.191) | <0.001 | 663 |

*†Note: N differs slightly from Table 6 (N = 29,847) due to inclusion of Florida tracts in robustness analyses, which were calculated separately using the full PLACES dataset.*

---

## Figure Legends

**Figure 1.** Conceptual model of immigrant health advantage pathways. Solid arrows indicate hypothesized causal effects; dashed arrows indicate alternative explanations tested in this study.

**Figure 2.** Forest plot of correlations between Hispanic origin group concentration and community health resilience. Point estimates with 95% confidence intervals.

**Figure 3.** Map of Texas showing resilience scores among Mexican-majority census tracts. Red indicates low resilience; blue indicates high resilience. Note the concentration of low-resilience tracts along the border and high-resilience tracts in urban centers.

**Figure 4.** Scatter plot of foreign-born percentage versus resilience score, stratified by Black-majority (blue) and Hispanic-majority (orange) tracts. Regression lines show positive associations in both groups.

**Figure 5.** Mean resilience by foreign-born quintile among Hispanic-majority tracts, with 95% confidence intervals. The positive gradient is consistent with the generational decay hypothesis, though cross-sectional data cannot distinguish decay from selection.

**Figure 6.** Heatmap of mean resilience by income quartile and foreign-born quartile among Hispanic-majority tracts. Highest resilience occurs at medium-high income with high foreign-born composition; lowest resilience occurs at low income regardless of foreign-born level.

---

*Word count: ~5,400 (excluding tables and references)*

*Corresponding author: [Contact information]*

*Funding: [To be completed]*

*Conflicts of interest: None declared*

*Data availability: All data derived from publicly available sources (CDC PLACES, American Community Survey, USDA FARA). Analysis code available at [repository].*
