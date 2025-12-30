# Paper 4: Structural Determinants of Community Health Burden

**Working Title:** "Racial Residential Segregation and Community Health Burden: A Tract-Level Analysis of 72,000 U.S. Communities"

**Target Journal:** American Journal of Public Health / Journal of Health Disparities Research and Practice

---

## 1. RESEARCH QUESTION

How do structural determinants—particularly racial residential segregation, economic inequality, and disinvestment—shape community health burden at the census tract level?

Sub-questions:
1. What is the association between tract racial composition and CHBI?
2. Does this association persist after controlling for socioeconomic factors?
3. Are health trajectories (improving/declining) equitably distributed?
4. Does our model perform equitably across community types?

---

## 2. MOTIVATION

The "Spatial Synchrony" paper identified that communities change together due to shared causes. But *which* communities bear the heaviest burden, and *which* are improving vs. declining?

Equity lens matters because:
- Resource allocation based on CHBI could reinforce or reduce disparities
- Trajectory prediction could be less accurate for marginalized communities
- Policy implications differ if burden is concentrated vs. distributed

---

## 3. PROPOSED ANALYSES

### 3.1 Descriptive Epidemiology of Health Burden

**Analysis:**
- Distribution of CHBI by tract racial composition quintiles
- Heat maps of high-burden tracts by region
- Urban/suburban/rural stratification

**Key Metrics:**
- Mean CHBI by % Black, % Hispanic, % White non-Hispanic
- Concentration index: What % of total burden is in communities of color?
- Geographic clustering of high-burden tracts

### 3.2 Regression Analysis: Structural Determinants

**Dependent Variable:** CHBI (continuous)

**Key Predictors:**
- Racial composition (% Black, % Hispanic, % Other)
- Economic factors (median income, poverty rate, unemployment)
- Housing factors (% renter, housing value, age of housing)
- Segregation measures (dissimilarity index at county level)
- Healthcare access (distance to hospital, FQHC presence)

**Model Hierarchy:**
1. Model 1: Race/ethnicity only
2. Model 2: + Economic factors
3. Model 3: + Housing and place factors
4. Model 4: + Healthcare access

**Question:** How much of the racial association is "explained" by socioeconomic factors? What remains?

### 3.3 Equity in Trajectory Distribution

**Analysis:**
- Are improving/declining trajectories equitably distributed?
- Chi-square test: trajectory class × racial composition
- Logistic regression: P(DECLINE) ~ racial composition + controls

**Hypothesis:** Communities of color may be more likely to be classified as "STABLE" (stuck at high burden) rather than "IMPROVING."

### 3.4 Model Equity Audit

**Analysis:**
- Stratified model performance by tract racial composition
- F1, precision, recall by community type
- Error analysis: Where does our model fail, and for whom?

**Question:** Does our trajectory model work equally well for all communities, or does it have blind spots?

---

## 4. DATA REQUIREMENTS

**Already have:**
- [ ] CHBI for all tracts
- [ ] Trajectory classifications
- [ ] Prediction errors by tract

**Need from ACS:**
- [ ] Racial composition (% by race/ethnicity)
- [ ] Median household income
- [ ] Poverty rate
- [ ] Unemployment rate
- [ ] % Renter occupied
- [ ] Median housing value
- [ ] Educational attainment

**Need from other sources:**
- [ ] County-level segregation indices (may exist pre-calculated)
- [ ] FQHC locations (HRSA)
- [ ] Hospital locations (CMS)

---

## 5. EXPECTED FINDINGS

1. **Racial composition strongly associated with CHBI**
   - Tracts with higher % Black or Hispanic will have higher CHBI
   - Association partially but not fully explained by SES

2. **Improving trajectories concentrated in White, affluent communities**
   - Communities of color more likely to be stable-at-high-burden
   - Trajectory mobility is not equitable

3. **Model performance may vary by community type**
   - Prediction may be harder for communities with more instability
   - Under/overprediction patterns may differ

4. **Structural factors dominate individual behavior**
   - Even after controlling for behavior measures (LPA, etc.), place-based factors significant

---

## 6. PAPER STRUCTURE

**Abstract** (300 words)
**Introduction** (1200 words)
- Health disparities as structural, not individual
- Residential segregation and health
- Need for tract-level analysis

**Methods** (1500 words)
- Data sources and sample
- Variable construction
- Analytic approach (descriptive, regression, equity audit)

**Results** (2200 words)
- Descriptive findings
- Regression models
- Trajectory equity
- Model equity audit

**Discussion** (1500 words)
- Structural interpretation
- Policy implications
- Limitations (ecological fallacy, causal inference)
- Future directions

---

## 7. ETHICAL CONSIDERATIONS

**Framing Matters:**
- Avoid deficit framing of communities of color
- Emphasize structural/policy causes, not community deficits
- Language review for bias

**Potential Misuse:**
- CHBI could be used for redlining, insurance discrimination
- Trajectory labels could stigmatize communities
- Must discuss responsible use prominently

**Community Engagement:**
- Ideal: Community advisory board review
- Minimum: Clear statement of limitations and intended use

---

## 8. CONTRIBUTION

**Novelty:**
- Tract-level analysis at national scale (72,000 tracts)
- Links structural determinants to composite health measure
- Equity audit of predictive model

**Impact:**
- Provides evidence for health equity policy
- Identifies where intervention is most needed
- Warns against naive use of CHBI for resource allocation

**Practical Value:**
- Informs targeted investment strategies
- Identifies communities at risk of declining further
- Supports health equity frameworks

---

## 9. ANALYSIS SCRIPT OUTLINE

```python
# health_equity_analysis.py

# 1. DATA PREPARATION
def load_acs_demographics():
    """Load ACS tract-level demographics."""
    pass

def merge_with_chbi():
    """Merge demographics with CHBI data."""
    pass

# 2. DESCRIPTIVE ANALYSIS
def chbi_by_racial_composition():
    """CHBI distribution by race quintiles."""
    pass

def concentration_analysis():
    """What share of burden is in communities of color?"""
    pass

def geographic_clustering():
    """Map high-burden tracts by region."""
    pass

# 3. REGRESSION ANALYSIS
def hierarchical_regression():
    """Build models 1-4 progressively."""
    pass

def mediation_analysis():
    """How much of race effect is mediated by SES?"""
    pass

# 4. TRAJECTORY EQUITY
def trajectory_by_race():
    """Trajectory distribution by racial composition."""
    pass

def decline_prediction():
    """Logistic regression for P(DECLINE)."""
    pass

# 5. MODEL EQUITY AUDIT
def stratified_performance():
    """F1, precision, recall by community type."""
    pass

def error_analysis():
    """Where does the model fail?"""
    pass
```

---

## 10. DEPENDENCIES

**Data Acquisition:**
- ACS data via Census API or NHGIS (free, straightforward)
- Segregation indices from published sources
- HRSA/CMS for healthcare access

**Analysis Dependencies:**
- Paper 1 complete (provides trajectory classifications)
- Paper 2 findings inform interpretation (if trajectories unpredictable, equity in trajectories matters less)

**Estimated effort:**
- Data acquisition: 1-2 days
- Analysis: 300 lines, 2-3 hours runtime
- Writing: Straightforward given clear framework
