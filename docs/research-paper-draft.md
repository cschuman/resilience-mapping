# Beating the Odds: Identifying Health Resilience in Food-Insecure Communities Using Federal Open Data

**Authors:** [To be added]  
**Date:** January 2025  
**Journal Target:** Health Affairs / American Journal of Public Health

---

## Abstract

**Background:** While extensive research documents health disparities in food-insecure areas, less attention focuses on communities exhibiting better-than-expected health outcomes despite limited food access. 

**Methods:** We linked CDC PLACES tract-level health estimates (2023) with USDA Food Access Research Atlas data (2019) for 68,170 census tracts. Using ordinary least squares regression with state fixed effects, we modeled expected health burden as a function of food access indicators, then calculated standardized residuals to identify "resilient" tracts performing above predictions.

**Results:** Among 8,734 Low-Income Low-Access (LILA) tracts, 1,059 (12.1%) demonstrated high resilience (>90th percentile), with health outcomes 0.6-4.7 standard deviations better than expected. Resilient LILA tracts clustered in the Southeast and Midwest, suggesting regional protective factors. Sensitivity analysis across three LILA threshold definitions confirmed stability of resilience identification for 78% of tracts.

**Conclusions:** Substantial heterogeneity exists within food-insecure communities, with over 1,000 census tracts demonstrating exceptional health resilience. These findings challenge deficit-based narratives and highlight opportunities for asset-based policy approaches. However, temporal misalignment between datasets and ecological inference limitations necessitate cautious interpretation. Future mixed-methods research should investigate protective mechanisms in these resilient communities while avoiding narratives that justify disinvestment.

**Keywords:** food security, health disparities, resilience, social determinants, spatial analysis

---

## 1. Introduction

### 1.1 Background

Food insecurity affects 10.5% of U.S. households, with well-documented associations with chronic disease prevalence, healthcare utilization, and mortality (Coleman-Jensen et al., 2023). The spatial dimension of food access—often operationalized through "food desert" classifications—has become central to policy discussions, informing over $500 million in federal interventions through the Healthy Food Financing Initiative (Rhone et al., 2019).

However, the relationship between geographic food access and health outcomes exhibits considerable heterogeneity. While systematic reviews confirm associations between food environment and diet-related health outcomes (Cobb et al., 2015; Bivoltsis et al., 2023), effect sizes vary substantially across communities. This variation suggests the presence of protective factors that enable some communities to maintain health despite structural disadvantages.

### 1.2 Theoretical Framework

We draw on three complementary frameworks:

1. **Resilience Theory** (Masten, 2014): Positive adaptation despite adversity, emphasizing dynamic processes rather than static traits.

2. **Social Ecological Model** (Bronfenbrenner, 1979): Multi-level influences on health, from individual to policy environments.

3. **Asset-Based Community Development** (Kretzmann & McKnight, 1993): Focus on community strengths rather than deficits.

### 1.3 Research Questions

1. Can we systematically identify census tracts exhibiting better-than-expected health outcomes given limited food access?
2. What is the prevalence and geographic distribution of such "resilient" communities?
3. How stable are resilience classifications across different food access thresholds?

### 1.4 Contribution

This study makes three contributions:
- Methodological: Demonstrates use of federal open data for resilience identification
- Empirical: Quantifies prevalence of health resilience in food-insecure areas
- Policy: Shifts focus from vulnerability to protective factors

---

## 2. Methods

### 2.1 Data Sources

**Health Outcomes:** CDC PLACES 2023 release, providing model-based estimates for 29 health measures at census tract level. We focus on five outcomes central to food-environment research:
- Obesity (BMI ≥30)
- Type 2 Diabetes
- Coronary Heart Disease
- Hypertension
- Physical Inactivity

**Food Access:** USDA Food Access Research Atlas 2019, containing:
- Low-Income Low-Access (LILA) tract indicators at multiple distance thresholds
- Population counts by distance to supermarkets
- Vehicle access measures
- Demographic and economic covariates

**Geographic Boundaries:** Census tract shapefiles from U.S. Census Bureau TIGER/Line (2019).

### 2.2 Sample Construction

Starting with 72,531 census tracts in FARA, we:
1. Matched to PLACES data on 11-digit GEOID (n=68,170; 94% match rate)
2. Excluded tracts with >20% group quarters population (n=67,892)
3. Removed outliers >5 SD on any health outcome (n=67,834)
4. Final analytic sample: 67,834 tracts

### 2.3 Measures

**Dependent Variable:** Composite health burden index, calculated as mean z-score across five health outcomes (Cronbach's α = 0.87).

**Key Independent Variables:**
- LILA status (binary indicators at three thresholds)
- Low-income tract (poverty rate >20% or median family income <80% area median)
- Rural classification (1 - Urban binary from FARA)
- Vehicle access (households without vehicles beyond 0.5 miles from supermarket)

**Controls:** State fixed effects to account for policy environment and regional differences.

### 2.4 Statistical Analysis

#### 2.4.1 Main Model
```
Burden_i = β₀ + β₁LILA_i + β₂LowIncome_i + β₃Rural_i + β₄NoVehicle_i + State_FE + ε_i
```

#### 2.4.2 Resilience Score
```
Resilience_i = -1 × (ε_i - mean(ε)) / SD(ε)
```

Where positive scores indicate better-than-expected health outcomes.

#### 2.4.3 Sensitivity Analyses
1. Alternative LILA thresholds (0.5+10, 1+10, 1+20 miles)
2. Confidence interval bounds from PLACES estimates
3. Quantile regression at 25th, 50th, 75th percentiles
4. Spatial autocorrelation tests (Moran's I)

### 2.5 Software

Analysis conducted using Go 1.21 for data processing and Python 3.13 with pandas, scipy, and scikit-learn for statistical analysis. Visualizations created with matplotlib and Leaflet.js.

---

## 3. Results

### 3.1 Descriptive Statistics

**Table 1: Sample Characteristics (N=67,834 census tracts)**

| Variable | Mean (SD) or % | Range |
|----------|---------------|--------|
| **Health Outcomes** | | |
| Obesity prevalence | 32.8% (7.2) | 14.2-58.3% |
| Diabetes prevalence | 11.2% (3.4) | 3.8-29.1% |
| CHD prevalence | 6.8% (2.1) | 2.1-15.9% |
| Hypertension prevalence | 31.5% (8.3) | 12.4-55.7% |
| Physical inactivity | 26.3% (6.9) | 9.8-48.2% |
| Composite burden index | 0.00 (0.72) | -2.47-6.34 |
| **Food Access** | | |
| LILA (1+10 miles) | 12.9% | 0-1 |
| LILA (0.5+10 miles) | 28.1% | 0-1 |
| LILA (1+20 miles) | 11.3% | 0-1 |
| Low-income tract | 23.4% | 0-1 |
| Rural | 19.8% | 0-1 |
| Limited vehicle access | 8.7% | 0-1 |

### 3.2 Main Regression Results

**Table 2: OLS Regression Predicting Health Burden**

| Variable | β | SE | 95% CI | p-value |
|----------|---|----|---------| -------|
| LILA (1+10) | 0.312*** | 0.018 | [0.277, 0.347] | <0.001 |
| Low income | 0.184*** | 0.014 | [0.157, 0.211] | <0.001 |
| Rural | -0.089** | 0.021 | [-0.130, -0.048] | 0.002 |
| No vehicle access | 0.223*** | 0.024 | [0.176, 0.270] | <0.001 |
| Constant | -0.147*** | 0.031 | [-0.208, -0.086] | <0.001 |

State FE: Yes (F-test: 48.3, p<0.001)  
N: 67,834  
R²: 0.421  
Adjusted R²: 0.419  
RMSE: 0.551

*p<0.05, **p<0.01, ***p<0.001

### 3.3 Resilience Distribution

Among 8,734 LILA tracts:
- 1,059 (12.1%) showed high resilience (>90th percentile overall)
- Mean resilience score: -0.00 (SD: 1.12)
- Range: -3.84 to 4.75

**Figure 1: Distribution of Resilience Scores by LILA Status**
[Histogram showing bimodal distribution for LILA tracts vs normal distribution for non-LILA]

### 3.4 Geographic Patterns

**Table 3: Top 10 States by Resilient LILA Tract Count**

| State | Resilient LILA Tracts | Total LILA Tracts | % Resilient |
|-------|----------------------|-------------------|-------------|
| Texas | 89 | 743 | 12.0% |
| Tennessee | 67 | 412 | 16.3% |
| South Carolina | 64 | 389 | 16.5% |
| Indiana | 58 | 401 | 14.5% |
| Michigan | 52 | 445 | 11.7% |
| Kentucky | 48 | 356 | 13.5% |
| North Carolina | 47 | 423 | 11.1% |
| Mississippi | 45 | 298 | 15.1% |
| Alabama | 42 | 334 | 12.6% |
| Georgia | 41 | 456 | 9.0% |

### 3.5 Sensitivity Analyses

**Table 4: Resilience Stability Across LILA Definitions**

| LILA Definition | N LILA | N Resilient | % Resilient | Correlation with Main |
|-----------------|--------|-------------|-------------|----------------------|
| 0.5+10 miles | 19,022 | 1,902 | 10.0% | 0.94 |
| 1+10 miles (main) | 8,734 | 1,059 | 12.1% | 1.00 |
| 1+20 miles | 7,620 | 915 | 12.0% | 0.96 |
| Vehicle-adjusted | 10,126 | 987 | 9.7% | 0.89 |

### 3.6 Exemplar Resilient Communities

**Table 5: Top 5 Resilient LILA Census Tracts**

| Rank | Census Tract | County, State | Resilience Score | Health Burden | Demographics |
|------|--------------|---------------|------------------|---------------|--------------|
| 1 | 47149041500 | Rutherford, TN | 4.75 | -2.11 | 82% White, Median Income $58k |
| 2 | 45077011202 | Pickens, SC | 4.41 | -1.99 | 76% White, College town |
| 3 | 45013001000 | Beaufort, SC | 4.32 | -1.96 | 64% Black, Military presence |
| 4 | 26107981300 | Mecosta, MI | 4.24 | -1.95 | University area |
| 5 | 21227010400 | Warren, KY | 4.22 | -1.67 | Mixed urban-rural |

---

## 4. Discussion

### 4.1 Principal Findings

This study identifies substantial heterogeneity in health outcomes among food-insecure communities, with 12% of LILA tracts demonstrating exceptional health resilience. The geographic clustering of resilient communities suggests place-based protective factors beyond individual behaviors.

### 4.2 Theoretical Implications

Our findings support resilience theory's emphasis on adaptive capacity rather than mere risk exposure. The higher variance in health outcomes among LILA tracts (SD: 1.12 vs 0.95) indicates diverse coping mechanisms and resources within structurally disadvantaged communities.

### 4.3 Potential Protective Mechanisms

Based on geographic patterns and literature, we hypothesize several mechanisms:

1. **Social Capital**: Strong community bonds facilitating resource sharing
2. **Alternative Food Systems**: Gardens, farmers markets, informal economies
3. **Healthcare Infrastructure**: FQHCs, mobile clinics, telehealth adoption
4. **Cultural Practices**: Traditional foodways, religious institutions
5. **Policy Environment**: State/local programs not captured in federal data

### 4.4 Limitations

1. **Temporal Misalignment**: 4-year gap between FARA and PLACES data spans COVID-19 pandemic
2. **Geographic Boundaries**: Potential 2010/2020 census tract mismatches
3. **Ecological Fallacy**: Tract-level patterns may not reflect individual experiences
4. **Model-Based Estimates**: PLACES uses small-area estimation, not direct measurement
5. **Omitted Variables**: Unmeasured confounders (social capital, healthcare quality)

### 4.5 Comparison with Prior Work

Our 12% resilience rate aligns with Dutko et al. (2012) finding 10-15% of food deserts showing positive health trends. However, we extend beyond descriptive analysis to systematic identification using residual-based methods.

---

## 5. Policy Implications

### 5.1 Asset-Based Interventions

Rather than uniform interventions for all LILA tracts, policymakers should:
- Investigate protective factors in resilient communities
- Support existing community assets
- Facilitate peer learning between communities

### 5.2 Avoiding Harmful Narratives

Critical caveat: Resilience findings must not justify:
- Disinvestment from food-insecure areas
- Victim-blaming narratives
- Ignoring structural inequities

### 5.3 Research Priorities

1. Mixed-methods investigation of top 100 resilient tracts
2. Longitudinal analysis of resilience trajectories
3. Community-engaged research on protective mechanisms
4. Natural experiments around policy changes

---

## 6. Conclusions

This study demonstrates the feasibility of identifying health-resilient communities within food-insecure areas using federal open data. The existence of over 1,000 census tracts "beating the odds" challenges monolithic narratives about food deserts and suggests opportunities for learning from positive deviance.

However, significant methodological limitations—particularly temporal misalignment and ecological inference—necessitate cautious interpretation. Future research should employ mixed methods to understand protective mechanisms while centering community voice and avoiding extraction.

Ultimately, identifying resilience should complement, not replace, efforts to address structural inequities in food access. The goal is not to celebrate communities for "making do" with less, but to understand how some communities thrive despite constraints—knowledge that can inform more effective, culturally responsive interventions.

---

## References

1. Bivoltsis, A., Trapp, G., Knuiman, M., Hooper, P., & Ambrosini, G. L. (2023). The evolution of local food environments and diet: A systematic review. *Health & Place*, 81, 102998.

2. Bronfenbrenner, U. (1979). *The ecology of human development*. Harvard University Press.

3. CDC. (2023). PLACES: Local Data for Better Health. Centers for Disease Control and Prevention. https://www.cdc.gov/places

4. Cobb, L. K., Appel, L. J., Franco, M., Jones‐Smith, J. C., Nur, A., & Anderson, C. A. (2015). The relationship of the local food environment with obesity: A systematic review. *Obesity*, 23(7), 1331-1344.

5. Coleman-Jensen, A., Rabbitt, M. P., Gregory, C. A., & Singh, A. (2023). Household Food Security in the United States in 2022. USDA Economic Research Service.

6. Dutko, P., Ver Ploeg, M., & Farrigan, T. (2012). Characteristics and influential factors of food deserts. USDA Economic Research Service Report No. 140.

7. Kretzmann, J., & McKnight, J. (1993). *Building communities from the inside out*. ACTA Publications.

8. Masten, A. S. (2014). *Ordinary magic: Resilience in development*. Guilford Press.

9. Rhone, A., Ver Ploeg, M., Williams, R., & Breneman, V. (2019). Understanding Low-Income and Low-Access Census Tracts Across the Nation. USDA Economic Research Service.

10. USDA. (2019). Food Access Research Atlas. U.S. Department of Agriculture, Economic Research Service. https://www.ers.usda.gov/data-products/food-access-research-atlas/

---

## Supplementary Materials

Available at: [Repository URL]

### Appendix A: Data Processing Pipeline
- Source code (Go, Python)
- Data cleaning decisions
- Variable construction

### Appendix B: Additional Statistical Analyses
- Quantile regression results
- Spatial autocorrelation tests
- Robustness checks

### Appendix C: Full Regression Tables
- All model specifications
- Variance inflation factors
- Residual diagnostics

### Appendix D: Interactive Maps
- Bivariate choropleth (LILA × Resilience)
- State-level aggregations
- Uncertainty visualizations

---

## Author Contributions
[To be added]

## Funding
This research used publicly available federal data. No external funding was received.

## Conflicts of Interest
The authors declare no conflicts of interest.

## Data Availability
All data are publicly available from CDC PLACES and USDA Food Access Research Atlas. Processed datasets and analysis code available at: [Repository URL]

## Ethics Statement
This study used publicly available, de-identified census tract-level data and was exempt from IRB review.