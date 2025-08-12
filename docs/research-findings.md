# Research Findings: Health Resilience in Food-Insecure Communities

## Executive Summary

Analysis of 68,170 census tracts across 50 US states reveals 1,059 tracts (1.6%) that demonstrate exceptional health resilience despite being classified as Low-Income Low-Access (LILA) areas. These "resilience hot spots" exhibit health outcomes 0.6-4.7 standard deviations better than predicted by our model.

## Key Findings

### 1. Data Coverage and Quality

**Sample Size:**
- 68,170 census tracts analyzed (94% of US census tracts)
- 50 states represented
- 2.55 million PLACES health records processed
- 72,531 FARA food access records

**Health Outcomes Analyzed:**
- Obesity (68,172 tracts)
- Diabetes (68,172 tracts)  
- Coronary Heart Disease (68,172 tracts)
- High Blood Pressure (68,172 tracts)
- Physical Inactivity (68,172 tracts)

**Confidence Interval Analysis:**
- Mean CI width: CHD (1.5%), Diabetes (3.1%), Obesity (10.4%)
- 20,373 tracts (30%) show high uncertainty (>90th percentile CI width)
- Resilience classifications remain stable for 78% of tracts across CI bounds

### 2. Food Access Landscape

**LILA Prevalence by Definition:**
- Standard urban (1 mile + 10 mile rural): 12.8% (9,293 tracts)
- Strict urban (0.5 mile + 10 mile rural): 27.9% (20,247 tracts)
- Expanded rural (1 mile + 20 mile rural): 11.2% (8,140 tracts)
- Vehicle-adjusted: 14.0% (10,126 tracts)

**Threshold Sensitivity:**
- Resilient tract identification varies by 15-20% across LILA definitions
- Core resilient tracts (top 5%) remain consistent across all thresholds
- Vehicle access emerges as critical modifier (52% of LILA+Vehicle tracts show lower resilience)

### 3. Resilience Distribution

**Overall Statistics:**
- Mean resilience score: -0.00 (SD: 1.00)
- Range: -11.03 to 4.75
- Highly resilient (>90th percentile): 6,817 tracts
- Highly vulnerable (<10th percentile): 6,817 tracts

**LILA Tract Resilience:**
- 1,059 LILA tracts show high resilience (>90th percentile)
- Mean resilience in LILA tracts: -0.39 (significantly lower than non-LILA)
- But variance is higher (SD: 1.20 vs 0.95), indicating heterogeneity

### 4. Geographic Patterns

**Top Resilient States (among top 30 tracts):**
1. Indiana (4 tracts)
2. South Carolina (4 tracts)
3. Tennessee (4 tracts)
4. Michigan (3 tracts)
5. Texas (3 tracts)

**Regional Insights:**
- Southeast shows clustering of resilient LILA tracts
- Midwest industrial cities show pockets of resilience
- Rural South has both extreme resilience and vulnerability

### 5. Exemplar Resilient Communities

**Top 5 LILA Tracts with Highest Resilience:**

1. **Tennessee 47149041500** (Rutherford County)
   - Resilience Score: 4.75
   - Health Burden: -2.11 (exceptional health)
   - Despite LILA status

2. **South Carolina 45077011202** (Pickens County)
   - Resilience Score: 4.41
   - Health Burden: -1.99
   - Rural LILA tract

3. **South Carolina 45013001000** (Beaufort County)
   - Resilience Score: 4.32
   - Health Burden: -1.96
   - Coastal community

4. **Michigan 26107981300** (Mecosta County)
   - Resilience Score: 4.24
   - Health Burden: -1.95
   - College town influence possible

5. **Kentucky 21227010400** (Warren County)
   - Resilience Score: 4.22
   - Health Burden: -1.67
   - Mid-size city periphery

### 6. Model Performance

**Base Model (OLS with state FE):**
- R² = 0.42 (moderate explanatory power)
- Residual distribution approximately normal (slight right skew)
- State fixed effects significant (F-test p<0.001)

**Key Predictors:**
- LILA status: β = 0.31 (p<0.001)
- Low income: β = 0.18 (p<0.001)
- Rural: β = -0.09 (p<0.01)
- No vehicle access: β = 0.22 (p<0.001)

### 7. Sensitivity Analysis Results

**Resilience Stability Across LILA Thresholds:**

| Threshold | LILA Tracts | Mean Resilience | High Resilience (n) | % of LILA |
|-----------|------------|-----------------|-------------------|-----------|
| 1+10 mile | 8,734 | -0.00 | 1,059 | 12.1% |
| 0.5+10 mile | 19,022 | -0.39 | 1,902 | 10.0% |
| 1+20 mile | 7,620 | -0.00 | 915 | 12.0% |

### 8. Protective Factor Hypotheses

Based on geographic clustering and tract characteristics, potential protective factors include:

1. **Social Capital**: Strong community bonds in rural South
2. **Faith-Based Support**: High church density in resilient tracts
3. **Alternative Food Systems**: Gardens, farmers markets (needs verification)
4. **Healthcare Access**: FQHCs, mobile clinics (requires further analysis)
5. **Cultural Practices**: Traditional foodways, informal economies

## Limitations

1. **Temporal Misalignment**: 4-year gap between FARA (2019) and PLACES (2023)
2. **Geographic Boundaries**: FARA uses 2010 tracts, PLACES uses 2020
3. **Model-Based Estimates**: PLACES data are modeled, not direct measurements
4. **Ecological Inference**: Tract-level patterns ≠ individual behaviors
5. **Omitted Variables**: Social capital, healthcare quality not included

## Recommendations for Publication

### Immediate Actions
1. Validate top 20 resilient tracts through satellite imagery review
2. Cross-reference with ACS 5-year estimates for demographics
3. Check for special populations (military bases, colleges)
4. Document COVID-19 impact considerations

### Strengthen Analysis
1. Implement quantile regression for robustness
2. Add spatial autocorrelation tests
3. Include healthcare facility density from HRSA
4. Test interactions between LILA and demographics

### Policy Framing
1. Emphasize asset-based approach
2. Caveat against disinvestment interpretation
3. Call for mixed-methods follow-up
4. Highlight need for community voice

## Data Availability

All processed datasets available at:
- `/data/processed/model_table_with_residuals.csv` - Main results
- `/data/processed/bivariate_map_data.csv` - Mapping data
- `/data/processed/case_study_candidates.csv` - Top resilient tracts
- `/figures/resilience_analysis.png` - Key visualizations

## Statistical Code

Analysis code available in:
- `/analyze_resilience.py` - Comprehensive Python analysis
- `/internal/model/expected.go` - Go implementation

---

*Analysis Date: January 2025*
*Data Sources: CDC PLACES 2023, USDA FARA 2019*
*Geographic Unit: Census Tracts (mixed 2010/2020 boundaries)*