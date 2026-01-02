# Paper 5: The Grocery Store Paradox

> ## ⚠️ ARCHIVED - SUPERSEDED BY V2 (ALSO ABANDONED)
>
> **Status:** ABANDONED (January 2026)
>
> **Reason:** This V1 draft had circular reasoning—excluding demographics from baseline, then "discovering" paradox tracts were demographically disadvantaged. V2 attempted to fix this but was also abandoned due to a deeper flaw (CDC PLACES data circularity).
>
> See: `PAPER-5-PARADOX-STUDY-V2.md` for the final analysis and explanation of why the entire approach was abandoned.
>
> ---

**Original Working Title:** "The Grocery Store Paradox: Why Food Access Alone Cannot Heal Structurally Harmed Communities"

**Original Target Journal:** American Journal of Public Health or Health Affairs

---

## Abstract

Food access interventions assume that proximity to grocery stores improves health outcomes. We identify 7,102 U.S. census tracts that challenge this assumption: communities with adequate food access but health outcomes more than one standard deviation worse than predicted. These "paradox tracts" are not randomly distributed. They are disproportionately majority-Black (26.9% vs. 3.7%), higher poverty (20.8% vs. 11.2%), located in historically redlined areas (1.65x odds ratio), and concentrated in the highest quartile of social vulnerability (46.5% vs. 25% expected).

Longitudinal analysis (2020-2025) confirms paradox status is stable (r = 0.973 year-to-year), with 9.1% of tracts paradox in all years observed. The CDC Environmental Justice Index shows the largest effect size (d = 1.11), and matched comparison analysis demonstrates that even demographically similar communities differ on cumulative vulnerability (d = 0.62).

The paradox is not paradoxical—it reflects the limits of single-factor interventions in communities experiencing cumulative structural disadvantage. Food access is necessary but insufficient; investment must be proportional to historical harm.

---

## Key Findings

### Finding 1: The Paradox Is Large and Systematic

| Metric | Value |
|--------|-------|
| Total tracts analyzed | 64,419 |
| Tracts with good food access (non-LILA) | 56,537 |
| **Paradox tracts** (good access + poor health) | **7,102 (12.6%)** |
| Extreme paradox (<-2 SD) | 1,500 (2.7%) |

For comparison: We previously identified 2,767 *resilient* tracts (poor access + good health). The paradox population is **2.6x larger**.

### Finding 2: Racial Composition Is the Strongest Differentiator

| Metric | Paradox Tracts | Non-Paradox | Difference |
|--------|---------------|-------------|------------|
| Majority Black | 26.9% | 3.7% | +23.2 pp |
| Majority White | 48.6% | 64.2% | -15.6 pp |
| % Black population (mean) | 30.7% | 10.0% | +20.7 pp |

Effect size (Cohen's d) for % Black: **d = 0.76** (large effect)

### Finding 3: Poverty Is Significant But Not Determinative

| Metric | Paradox Tracts | Non-Paradox | Difference | Cohen's d |
|--------|---------------|-------------|------------|-----------|
| Poverty rate | 20.8% | 11.2% | +9.6 pp | +0.83 |
| Median household income | $56,226 | $88,774 | -$32,548 | -0.96 |
| Unemployment rate | 8.2% | 5.1% | +3.1 pp | +0.58 |
| Bachelor's degree+ | 21.6% | 35.9% | -14.3 pp | -0.84 |

Note: These tracts are *not* classified as Low-Income Low-Access (LILA) by USDA standards. They have "good" food access by federal definition. The income gap (d = -0.96) is the largest effect size observed.

### Finding 4: Paradox Tracts Cluster in Highest Social Vulnerability

Distribution across CDC Social Vulnerability Index quartiles:

| Quartile | Expected | Paradox Actual | Difference |
|----------|----------|----------------|------------|
| Q1 (Lowest vulnerability) | 25% | 7.6% | -17.4 pp |
| Q2 | 25% | 18.1% | -6.9 pp |
| Q3 | 25% | 27.7% | +2.7 pp |
| Q4 (Highest vulnerability) | 25% | **46.5%** | **+21.5 pp** |

Nearly half of all paradox tracts fall in the most vulnerable quartile nationally.

### Finding 5: Historical Redlining Persists

Among tracts in HOLC-mapped cities (n=5,549 paradox, n=26,644 comparison):

| Metric | Paradox | Non-Paradox |
|--------|---------|-------------|
| In redlined (D grade) areas | 31.6% | 21.9% |
| In C or D grade areas | 77.3% | 65.2% |
| **Odds ratio** | **1.65x** | — |

Chi-square: χ² = 239.6, p < 0.0001

Paradox tracts are 1.65 times more likely to be located in areas that were designated "Hazardous" by the Home Owners' Loan Corporation in the 1930s.

### Finding 6: Geographic Concentration

**Top 10 Cities by Paradox Tract Count:**

| City | Paradox Tracts | % in Redlined Areas | Avg Resilience Score |
|------|---------------|---------------------|---------------------|
| Chicago, IL | 588 | 37.9% | -1.91 |
| Detroit, MI | 459 | 26.8% | -2.28 |
| Cleveland, OH | 202 | 25.2% | -2.15 |
| Los Angeles, CA | 147 | 20.4% | -1.54 |
| Milwaukee, WI | 147 | 25.2% | -1.95 |
| Philadelphia, PA | 130 | 42.3% | -1.67 |
| Baltimore, MD | 122 | 21.3% | -1.96 |
| Kansas City, MO | 117 | 58.1% | -2.06 |
| Norfolk, VA | 100 | 51.0% | -2.51 |
| Memphis, TN | 83 | 37.3% | -2.87 |

These are cities with documented histories of segregation, redlining, and disinvestment.

---

## Statistical Model

### Variance Explained

| Model | R² | Incremental |
|-------|-----|-------------|
| Demographics only | 23.8% | — |
| Demographics + SVI themes | 24.0% | +0.2 pp |
| Demographics + SVI + HOLC | 24.2% | +0.2 pp |
| **+ Environmental Justice Index** | **35.4%** | **+11.2 pp** |

The CDC Environmental Justice Index (EJI) explains an additional 11.2% of within-paradox variance beyond demographics, SVI, and HOLC.

### Feature Coefficients (Standardized)

| Variable | β | Interpretation |
|----------|---|----------------|
| % Black population | -0.289 | Higher → worse health |
| Poverty rate | -0.285 | Higher → worse health |
| Redlined (D grade) | -0.022 | Redlined → worse health |
| HOLC score | -0.013 | Higher grade → worse health |

### Interpretation of R²

The 24% explained variance and 76% unexplained variance require interpretation:

1. **We are explaining within-paradox variance** — all tracts already have good food access and poor health. We ask: "Why are some paradox tracts worse than others?"

2. **HOLC doesn't add incremental R² because current demographics mediate historical redlining.** The racial and economic composition of these tracts *is* the legacy of redlining.

3. **Unexplained variance likely reflects:**
   - Healthcare quality and access (trust, discrimination)
   - Social cohesion and community networks
   - Chronic stress exposure
   - Built environment factors
   - Individual-level behaviors (unmeasurable at tract level)

### Note on Collinearity

The CDC Social Vulnerability Index includes demographic variables (poverty, minority status) that overlap with our direct demographic measures. We present both because: (1) SVI provides a validated, policy-relevant composite; (2) direct demographic measures allow finer-grained interpretation; (3) the minimal incremental R² from SVI confirms that our direct measures already capture the relevant variance. Readers should interpret the demographic and SVI findings as complementary rather than additive.

---

## Methods

### Data Sources

| Source | Year | Coverage |
|--------|------|----------|
| CDC PLACES | 2020-2025 | 15 health outcomes, tract-level, 6 years |
| USDA Food Access Research Atlas | 2019 | LILA classification, food access metrics |
| American Community Survey | 2022 | Demographics, socioeconomic indicators |
| CDC Social Vulnerability Index | 2022 | 16 vulnerability indicators, 4 themes |
| CDC Environmental Justice Index | 2022 | 36 environmental/social/health factors |
| HOLC Redlining Maps | 1930s (digitized) | 42,074 tracts in mapped cities |

### Paradox Definition

A tract is classified as "paradox" if:
1. **Not LILA** (LILATracts_1And10 = 0): Good food access by USDA definition
2. **Resilience score < -1.0**: Health burden more than 1 SD worse than predicted by our model

The resilience score is calculated as:
```
resilience_score = -residual / std(residuals)
```
Where the residual is from an OLS regression predicting health burden from LILA status, low-income status, rural/urban classification, and state fixed effects.

### Comparison Groups

- **Paradox tracts** (n=7,102): Good food access, poor health
- **Non-paradox tracts** (n=49,435): Good food access, normal/good health
- **Within HOLC-mapped cities**: Paradox (n=5,549) vs. non-paradox (n=26,644)

---

## Discussion

### The Paradox Is Not Paradoxical

These findings reveal that the "paradox" is only paradoxical if we assume food access alone determines health outcomes. When we account for structural factors—racial composition, poverty concentration, historical redlining, and cumulative social vulnerability—the pattern becomes predictable.

Communities that were:
- Designated "Hazardous" and denied mortgage access in the 1930s
- Subject to subsequent decades of disinvestment
- Targeted for highway construction and urban renewal
- Exposed to white flight and tax base erosion

...do not become healthy simply because a grocery store opens nearby.

### Food Access Is Necessary But Not Sufficient

This study does not argue that food access is unimportant. Communities with *both* poor food access and poor health outcomes exist (the vulnerable population in our original analysis). Food access interventions may be necessary.

But food access is not sufficient. In 7,102 communities, adequate food access coexists with poor health. Investment in these communities must address root causes:

- Economic opportunity and wealth-building
- Healthcare access and quality
- Housing stability and quality
- Environmental conditions
- Social infrastructure

### Policy Implications

1. **Food access programs should not be evaluated in isolation.** Success should not be measured by grocery store proximity but by health outcome improvement.

2. **Investment should be proportional to historical harm.** Communities with deeper histories of disinvestment require more comprehensive intervention, not equal treatment.

3. **Single-factor interventions are insufficient.** "Food desert" framing oversimplifies the problem and suggests oversimplified solutions.

4. **Reparative frameworks may be more appropriate than ameliorative ones.** These communities were harmed by policy; healing may require acknowledgment and repair, not just services.

---

## Sensitivity Analysis

To assess robustness, we tested our findings across alternative threshold definitions for paradox classification.

### Threshold Sensitivity

| Threshold | N Paradox | % of Total | % Majority Black | Mean Poverty Rate |
|-----------|-----------|------------|------------------|-------------------|
| -0.5 SD | 15,126 | 26.8% | 16.0% | 17.0% |
| -0.75 SD | 10,423 | 18.4% | 20.9% | 18.8% |
| **-1.0 SD (primary)** | **7,102** | **12.6%** | **26.9%** | **20.8%** |
| -1.25 SD | 4,698 | 8.3% | 34.4% | 23.3% |
| -1.5 SD | 3,149 | 5.6% | 42.2% | 26.0% |
| -1.75 SD | 2,146 | 3.8% | 50.0% | 28.3% |
| -2.0 SD | 1,500 | 2.7% | 54.9% | 30.2% |

### Key Findings from Sensitivity Analysis

1. **Patterns are consistent across all thresholds.** The association between paradox status and racial composition, poverty, and structural disadvantage holds regardless of where we draw the line.

2. **More extreme thresholds reveal more extreme disadvantage.** As the threshold becomes more stringent (from -0.5 to -2.0 SD), the proportion of majority-Black tracts increases from 16% to 55%, and mean poverty rate increases from 17% to 30%. This is not an artifact of threshold selection—it reflects the reality that the most extreme health deficits occur in the most disadvantaged communities.

3. **The primary threshold (-1.0 SD) is neither too lenient nor too strict.** At this threshold, we capture communities with health outcomes one standard deviation worse than predicted, which is both statistically meaningful and clinically relevant.

### 95% Confidence Interval for Key Finding

The difference in majority-Black proportion between paradox and non-paradox tracts:
- Point estimate: 23.2 percentage points
- 95% CI: 22.0% to 24.4%

This narrow confidence interval indicates high precision in our estimate and rules out chance as an explanation for the observed disparity.

---

## Longitudinal Validation

To address concerns about cross-sectional design, we tracked paradox status across six years of CDC PLACES data (2020-2025).

### Persistence of Paradox Status

| Category | N Tracts | % of Total |
|----------|----------|------------|
| Never paradox | 49,933 | 80.4% |
| Rarely paradox (1-25% of years) | 921 | 1.5% |
| Sometimes paradox (25-50% of years) | 2,010 | 3.2% |
| Often paradox (50-75% of years) | 2,735 | 4.4% |
| Usually paradox (75-99% of years) | 821 | 1.3% |
| **Always paradox (100% of years)** | **5,680** | **9.1%** |

### Stability Metrics

| Metric | Value |
|--------|-------|
| Year-to-year resilience score correlation | r = 0.973 |
| Paradox retention rate (2020→2025) | 67.8% |
| Persistently paradox (75%+ years) | 6,501 tracts (10.5%) |

### Demographics by Persistence

| Variable | Persistent Paradox | Transient Paradox | Never Paradox |
|----------|-------------------|-------------------|---------------|
| % Black | 33.8% | 15.3% | 8.8% |
| Poverty rate | 28.6% | 18.4% | 10.0% |
| Median income | $41,261 | $57,625 | $92,532 |

**Key finding:** Paradox status is stable, not transient. 9.1% of tracts with good food access are paradox in all years observed. Persistently paradox tracts have significantly worse structural disadvantage than transiently paradox tracts.

---

## Environmental Justice Analysis

The CDC Environmental Justice Index (EJI) measures cumulative environmental burden across 36 indicators.

### EJI Comparison

| Indicator | Paradox | Non-Paradox | Cohen's d |
|-----------|---------|-------------|-----------|
| Overall EJI | 0.715 | 0.429 | **+1.11** |
| Social Vulnerability (EJI) | 0.638 | 0.450 | +0.67 |
| Environmental Burden | 0.539 | 0.496 | +0.15 |

The overall EJI effect size (d = 1.11) is the largest observed in this study, indicating that environmental justice burden is a powerful distinguishing factor for paradox tracts.

### EJI Contribution to Variance

EJI variables explain 11.2% of within-paradox variance, bringing total explained variance to 35.4%. This is the largest single contribution after demographics.

---

## Matched Comparison Analysis

To address selection on the dependent variable, we matched each paradox tract to 3 similar non-paradox tracts on demographics (% Black, % White, poverty rate, median income).

### Methodology

- Paradox tracts matched: 6,222
- Total matched controls: 10,591
- Matching variables: race composition, poverty, income
- Matching distance: mean = 0.146

### Results After Matching

**Even after controlling for demographics, paradox tracts differ significantly on:**

| Factor | Cohen's d | p-value |
|--------|-----------|---------|
| EJI overall | +0.62 | < 0.0001 |
| Social vulnerability (EJI) | +0.34 | < 0.0001 |
| Environmental burden | +0.07 | < 0.0001 |
| % Renter occupied | +0.07 | < 0.0001 |

**Key finding:** The paradox is not fully explained by demographics. Among demographically similar communities, those with poor health outcomes have higher cumulative vulnerability as measured by the Environmental Justice Index. The paradox reflects multi-dimensional structural disadvantage that cannot be reduced to any single factor.

---

## Limitations

### Addressed in This Study

1. ~~**Cross-sectional design**~~: **ADDRESSED.** Longitudinal analysis (2020-2025) confirms paradox status is stable (r = 0.973 year-to-year), not a cross-sectional artifact. 9.1% of tracts are paradox in all years observed.

2. ~~**Environmental hazards not included**~~: **ADDRESSED.** CDC Environmental Justice Index now incorporated, explaining additional 11.2% of within-paradox variance.

3. ~~**Selection on dependent variable**~~: **ADDRESSED.** Matched comparison analysis shows that even when controlling for demographics, paradox tracts differ significantly on EJI (d = 0.62).

### Remaining Limitations

4. **Tract-level analysis**: Individual-level variation is masked; ecological fallacy remains possible.

5. **FARA data currency**: Food Access Research Atlas is from 2019; grocery store locations may have changed.

6. **HOLC coverage**: Only 42,074 tracts were in cities mapped by HOLC; many paradox tracts in unmapped areas.

7. **Unexplained variance**: 64.6% of within-paradox variance remains unexplained (reduced from 76% by adding EJI).

8. **Causal inference**: Despite longitudinal and matching analyses, we cannot definitively establish causal relationships. The structural factors we identify are strongly associated with paradox status but not proven causes.

---

## Future Directions

1. **Qualitative research**: Conduct community-based participatory research in paradox tracts to understand lived experience and community-identified factors.

2. **Intervention evaluation**: Assess health outcomes in paradox tracts that have received comprehensive (vs. single-factor) interventions.

3. **Healthcare access analysis**: Incorporate HRSA data on Federally Qualified Health Centers and hospital locations to assess healthcare access as a potential mediating factor.

4. **Policy impact assessment**: Track whether paradox status changes following major policy interventions (Medicaid expansion, place-based investments).

---

## Conclusion

The grocery store paradox reveals the limits of food access as a health intervention. In 7,102 American communities, grocery stores exist but health remains poor. These communities are disproportionately Black, poor, historically redlined, and socially vulnerable. The paradox is not a mystery—it is strongly associated with cumulative structural disadvantage that a grocery store cannot address.

Food access programs are well-intentioned and may be necessary. But they are not sufficient. Communities that have been systematically harmed by policy over decades require investment proportional to that harm. Anything less is expecting a band-aid to heal a wound that is still being inflicted.

---

## Data Availability

Analysis code and processed datasets available at: [repository URL]

Raw data sources:
- CDC PLACES: https://www.cdc.gov/places
- USDA FARA: https://www.ers.usda.gov/data-products/food-access-research-atlas/
- CDC SVI: https://www.atsdr.cdc.gov/placeandhealth/svi/
- CDC EJI: https://www.atsdr.cdc.gov/place-health/php/eji/
- HOLC Maps: https://dsl.richmond.edu/panorama/redlining/

---

## Ethics Statement

This study uses publicly available, de-identified secondary data from federal agencies (CDC, USDA, Census Bureau) and is exempt from Institutional Review Board review per 45 CFR 46.104(d)(4).

---

## Funding

[To be completed prior to submission]

---

## Conflicts of Interest

The authors declare no conflicts of interest.

---

## Outputs Generated

```
data/processed/paradox_study/
├── paradox_tracts_full.csv              # All 7,102 paradox tracts
├── paradox_tracts_extreme.csv           # Top 50 most extreme cases
├── paradox_tracts_enhanced.csv          # With demographic analysis
├── paradox_tracts_with_svi.csv          # With SVI overlay
├── paradox_tracts_with_holc.csv         # With HOLC overlay
├── paradox_tracts_with_eji.csv          # With EJI overlay
├── paradox_cities_holc.csv              # City-level summary
├── demographic_comparison.csv           # Statistical comparisons
├── demographic_comparison_corrected.csv # With fixed income data
├── svi_theme_comparison.csv             # SVI theme analysis
├── sensitivity_thresholds.csv           # Threshold robustness test
├── longitudinal_persistence.csv         # Multi-year paradox tracking
├── year_to_year_correlations.csv        # Stability metrics
├── eji_comparison.csv                   # EJI analysis results
├── matched_pairs.csv                    # Matched comparison pairs
├── matched_comparison_results.csv       # Matched analysis results
└── paradox_summary.txt                  # Key statistics
```

---

## Analysis Scripts

```
app/analytics/
├── paradox_study.py                  # Initial paradox identification
├── paradox_structural_analysis.py    # Demographic analysis
├── paradox_svi_analysis.py           # SVI overlay
├── paradox_holc_analysis.py          # HOLC redlining overlay
├── paradox_sensitivity_analysis.py   # Threshold robustness testing
├── paradox_longitudinal_analysis.py  # Multi-year stability analysis
├── paradox_eji_analysis.py           # Environmental Justice Index overlay
└── paradox_matched_comparison.py     # Matched comparison study
```

---

*Draft completed: January 1, 2026*
*Analysis window: Single session*
*Total tracts analyzed: 64,419*
*Paradox tracts identified: 7,102*
