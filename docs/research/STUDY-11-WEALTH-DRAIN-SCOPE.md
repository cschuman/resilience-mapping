# Study 11: Wealth Drain Analysis

**Status:** Scoping (January 2026)

**Key Advantage:** No CDC PLACES dependency - uses economic outcomes only

---

## Research Question

**Primary:** Do communities with higher "wealth extraction" (predatory lending, lack of banking access, mortgage denial) experience worse economic trajectories over time?

**Secondary:** Is wealth extraction spatially concentrated, and does it correlate with historically redlined areas?

---

## Why This Study Avoids the PLACES Problem

| Study 5 (Abandoned) | Study 11 (Proposed) |
|---------------------|---------------------|
| Dependent variable: CDC PLACES health estimates | Dependent variable: ACS economic outcomes |
| Health data is modeled from demographics | Economic data is directly measured (surveys, tax records) |
| Circular: demographics predict demographics | Not circular: financial services → economic outcomes |

---

## Data Sources

### Primary Sources (Census Tract Level)

| Source | Variables | Availability | Format |
|--------|-----------|--------------|--------|
| **HMDA** (Urban Institute) | Mortgage applications, denials, by race/income | 2018-2023, free | CSV, 14MB/year |
| **FDIC Summary of Deposits** | Bank branch locations, deposits | Annual, free | CSV + geocoding needed |
| **ACS 5-Year** | Median income, poverty rate, home values | 2018-2022, free | API/CSV |
| **HOLC Redlining Maps** | Historical D-grade (redlined) status | 1930s, already downloaded | CSV |
| **CDC SVI** | Social vulnerability (non-health) | 2022, already downloaded | CSV |

### Secondary Sources (Requires Processing)

| Source | Variables | Challenge |
|--------|-----------|-----------|
| **State payday lender licenses** | Alternative financial service locations | State-by-state, inconsistent |
| **County Business Patterns** | Business density by NAICS | ZIP code level, not tract |
| **IRS SOI** | Income migration, tax data | County level only |

---

## Proposed Variables

### Independent Variables (Wealth Extraction Indicators)

1. **Mortgage denial rate** - HMDA applications denied / total applications
2. **High-cost loan share** - Loans with APR >1.5% above prime
3. **Bank branch density** - FDIC branches per 10,000 population
4. **Banking desert indicator** - Tract has 0 bank branches within 1 mile
5. **Mortgage refinance access** - Refinance applications per homeowner
6. **Loan-to-income ratio** - Average DTI of approved mortgages
7. **Historical redlining** - HOLC D-grade status (already have)

### Dependent Variables (Economic Outcomes)

1. **Median income change** - ACS 2018 → 2022 (inflation-adjusted)
2. **Poverty rate change** - ACS 2018 → 2022
3. **Home value change** - ACS median home value trajectory
4. **Homeownership rate change** - Owner-occupied % change
5. **Economic mobility index** - Composite of above

### Control Variables

1. **Baseline demographics** - Race, age, education (ACS)
2. **Urbanicity** - RUCA codes
3. **State fixed effects**
4. **Baseline economic status** - 2018 income/poverty

---

## Methodology

### Phase 1: Data Assembly (Week 1-2)

1. Download HMDA tract summaries from Urban Institute
2. Download FDIC branch locations and geocode to tracts
3. Calculate ACS economic changes 2018 → 2022
4. Merge with existing HOLC and SVI data

### Phase 2: Wealth Extraction Index (Week 2-3)

Create composite "Wealth Extraction Index" (WEI):
- Standardize each extraction indicator (z-scores)
- Weight by factor analysis or equal weights
- Validate with known high-extraction areas

### Phase 3: Analysis (Week 3-4)

**Model 1: Cross-sectional**
```
Economic_Status_2022 ~ WEI + Controls + State_FE
```

**Model 2: Change model (preferred)**
```
Δ Economic_Status (2018→2022) ~ WEI_2018 + Baseline_Status + Controls
```

**Model 3: Spatial analysis**
- Moran's I for WEI clustering
- Local indicators of spatial association (LISA)
- Correlation with HOLC redlining

### Phase 4: Validation (Week 4-5)

- Test on held-out tracts
- Sensitivity to WEI construction
- Comparison with known case studies (Detroit, Baltimore, etc.)

---

## Key Hypotheses

1. **H1:** Tracts with higher wealth extraction experience slower income growth
2. **H2:** Wealth extraction spatially clusters in historically redlined areas
3. **H3:** Banking deserts predict worse economic trajectories independent of baseline poverty
4. **H4:** High mortgage denial rates predict declining homeownership
5. **H5:** Effects are stronger in majority-Black tracts (interaction)

---

## What This Study CAN Claim

- Associations between financial service access and economic outcomes
- Spatial patterns of wealth extraction
- Correlation with historical redlining
- Predictive relationships (X in 2018 → Y change by 2022)

## What This Study CANNOT Claim

- Causation (observational design)
- That wealth extraction "causes" poverty (reverse causality possible)
- Individual-level effects (ecological inference limitation)
- Mechanisms (why extraction leads to worse outcomes)

---

## Advantages Over Study 5

| Issue | Study 5 | Study 11 |
|-------|---------|----------|
| Data circularity | Fatal flaw | Avoided - different data sources |
| Measured vs modeled | PLACES is modeled | ACS is measured |
| Causal language | "Unexplained" implies causation | "Predictive" is honest |
| Policy actionability | What intervention? | Clear: banking access, lending regulation |
| Novelty | Food desert critique exists | Tract-level wealth extraction is novel |

---

## Potential Limitations

1. **ACS measurement error** - Small tracts have large margins of error
2. **Temporal mismatch** - HMDA year vs ACS year alignment
3. **Selection effects** - Banks locate where profitable; causation unclear
4. **Missing payday data** - No centralized payday lender database
5. **Ecological fallacy** - Tract-level patterns may not reflect individual experiences

---

## Paper Potential

**Strong.** This addresses:
- Growing policy interest in banking deserts and predatory lending
- Financial redlining as modern discrimination mechanism
- Actionable implications (CRA enforcement, bank branch incentives)
- Complements health-focused food desert literature with economic lens

**Target journals:**
- Journal of Urban Economics
- Regional Science and Urban Economics
- Housing Policy Debate
- American Economic Review (if findings are strong)

---

## Next Steps

1. [ ] Download HMDA tract summaries (Urban Institute)
2. [ ] Download FDIC Summary of Deposits
3. [ ] Geocode bank branches to census tracts
4. [ ] Calculate ACS economic change variables
5. [ ] Merge datasets and create analysis file
6. [ ] Compute Wealth Extraction Index
7. [ ] Run preliminary analyses

---

## Data Links

- **HMDA Tract Summaries:** https://datacatalog.urban.org/dataset/home-mortgage-disclosure-act-neighborhood-summary-files-census-tract-level
- **FDIC Data Downloads:** https://www.fdic.gov/resources/tools/bank-data-guide/data-download.html
- **CFPB HMDA Portal:** https://www.consumerfinance.gov/data-research/hmda/

---

*Created: January 1, 2026*
