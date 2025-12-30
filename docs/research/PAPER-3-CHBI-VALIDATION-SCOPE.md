# Paper 3: Validating the Composite Health Burden Index

**Working Title:** "Development and Validation of a Composite Health Burden Index for U.S. Census Tracts: A Multi-Dimensional Assessment"

**Target Journal:** Health Services Research / Medical Care

---

## 1. RESEARCH QUESTION

We constructed a Composite Health Burden Index (CHBI) from 7 CDC PLACES measures with expert-derived weights. But is this composite valid? Does it capture what we intend to measure?

Key validation questions:
1. **Construct Validity**: Does CHBI correlate with external measures of community health?
2. **Face Validity**: Do domain experts agree with the weighting scheme?
3. **Sensitivity Analysis**: How robust is CHBI to alternative specifications?
4. **Predictive Validity**: Does higher CHBI predict worse outcomes?

---

## 2. CURRENT CHBI SPECIFICATION

```
CHBI = 0.20 × OBESITY +
       0.20 × DIABETES +
       0.15 × CHD (coronary heart disease) +
       0.15 × MHLTH (mental health not good) +
       0.10 × BPHIGH (hypertension) +
       0.10 × LPA (physical inactivity) +
       0.10 × PHLTH (physical health not good)
```

**Rationale for current weights:**
- Obesity and diabetes: High prevalence, strong chronic disease drivers
- CHD and mental health: Severe outcomes, healthcare utilization
- Others: Important but less severe/prevalent

---

## 3. VALIDATION FRAMEWORK

### 3.1 Construct Validity

**External Correlates to Test:**

| Measure | Expected Correlation | Data Source |
|---------|---------------------|-------------|
| All-cause mortality | Strong positive | CDC WONDER |
| Life expectancy | Strong negative | USALEEP |
| Healthcare expenditure | Moderate positive | CMS |
| Disability rate | Strong positive | ACS |
| Medicaid enrollment | Moderate positive | CMS |
| Uninsured rate | Moderate positive | ACS |
| Poverty rate | Moderate positive | ACS |
| Food insecurity | Moderate positive | USDA |

**Analysis:**
- Pearson/Spearman correlations with 95% CIs
- Scatterplots with LOESS smoothers
- Partial correlations controlling for demographics

### 3.2 Face Validity (Expert Survey)

**Design:**
- Survey 20-50 public health practitioners and researchers
- Present CHBI components and ask for weight allocation
- Compare expert-derived weights to our specification

**Questions:**
1. "If you had to allocate 100 points across these 7 measures to reflect their contribution to overall community health burden, how would you distribute them?"
2. "Is any important dimension missing from this index?"
3. "Should any measures be removed?"

### 3.3 Sensitivity Analysis

**Alternative Specifications to Test:**

| Specification | Description | Rationale |
|---------------|-------------|-----------|
| Equal weights | 0.143 each | Atheoretical baseline |
| PCA-derived | First principal component | Data-driven |
| Mortality-optimized | Weights maximize mortality correlation | Criterion validity |
| Mental-health-weighted | MHLTH = 0.30, others adjusted | Mental health emphasis |
| Chronic-only | Drop PHLTH, MHLTH | Objective measures only |

**Analysis:**
- Correlation matrix across specifications
- Rank stability: Do "worst" and "best" tracts remain consistent?
- Trajectory classification stability

### 3.4 Predictive Validity

**Does baseline CHBI predict future outcomes?**

Outcomes to test (if data available):
- 5-year mortality rate change
- ED visit rate change
- Hospital admission rate change
- COVID-19 death rate (2020-2022)

---

## 4. DATA REQUIREMENTS

**Already have:**
- [ ] CHBI computed for all tracts, all years
- [ ] Component measures
- [ ] Trajectory classifications

**Need to obtain:**
- [ ] CDC WONDER mortality data (county level, can aggregate)
- [ ] USALEEP life expectancy (tract level)
- [ ] ACS demographics (tract level)
- [ ] Expert survey responses (new data collection)

**Nice to have:**
- [ ] CMS healthcare utilization (may be county level)
- [ ] COVID-19 death rates by tract

---

## 5. EXPECTED FINDINGS

1. **CHBI will correlate r > 0.6 with mortality and life expectancy**
   - These are the ultimate outcomes we're trying to capture

2. **Expert weights will show high variance but cluster near our specification**
   - Public health practitioners will weight obesity/diabetes highly
   - Mental health weights will vary most

3. **Alternative specifications will be highly correlated (r > 0.90)**
   - Exact weights matter less than including the right components
   - Ranking stability will be high

4. **Predictive validity may be weak**
   - Baseline health level predicts future level (autocorrelation)
   - But predicting *change* is still difficult (per Paper 2)

---

## 6. PAPER STRUCTURE

**Abstract** (300 words)
**Introduction** (800 words)
- Need for composite health indices at tract level
- Existing indices (CHR, SVI, CHVI) and their limitations
- CHBI development rationale

**Methods** (1500 words)
- CHBI construction
- Validation framework (construct, face, sensitivity, predictive)
- Data sources and sample

**Results** (1800 words)
- External correlations
- Expert survey findings
- Sensitivity analysis
- Predictive validity

**Discussion** (1200 words)
- CHBI validity evidence
- Comparison to other indices
- Recommended use cases
- Limitations

---

## 7. CONTRIBUTION

**Novelty:**
- First validation study of a PLACES-based composite at tract level
- Combines multiple validation approaches (construct, face, sensitivity, predictive)

**Impact:**
- Provides defensible composite for resource allocation
- Transparency about what CHBI does/doesn't capture

**Practical Value:**
- Validated index for health planners
- Clear guidance on when to use vs. not use

---

## 8. DEPENDENCIES

- This paper can be written largely independently
- Expert survey requires IRB approval or exemption determination
- External data (mortality, life expectancy) may require data requests

**Estimated effort:**
- Analysis: 200 lines of code, 1-2 hours runtime
- Expert survey: 2-4 weeks for IRB + data collection
- Could write methods/intro while awaiting survey data
