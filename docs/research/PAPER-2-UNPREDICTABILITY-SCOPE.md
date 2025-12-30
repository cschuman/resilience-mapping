# Paper 2: The Fundamental Unpredictability of Community Health Trajectories

**Working Title:** "Why Community Health Trajectories Resist Prediction: Distinguishing Measurement Noise from Structural Chaos"

**Target Journal:** Epidemiology / Milbank Quarterly

---

## 1. RESEARCH QUESTION

Our best models achieve only F1=0.26 (macro) and balanced accuracy=0.33—essentially chance performance for 3-class prediction. **Why?**

Four competing hypotheses:
1. **Measurement Noise**: CDC PLACES estimates have substantial uncertainty (~3-5% for many measures). Trajectory "changes" may be measurement artifact.
2. **Temporal Resolution**: Year-over-year changes may be too fine-grained; true trajectories emerge over 3-5+ years.
3. **Missing Predictors**: We lack the variables that actually drive change (policy, investment, migration, etc.).
4. **Structural Chaos**: Community health dynamics may be genuinely unpredictable due to complex system dynamics.

---

## 2. DATA AVAILABLE

From existing infrastructure:
- **CDC PLACES 2020-2024**: 5 years of tract-level estimates (72,161 tracts)
- **Uncertainty Estimates**: CDC provides confidence intervals for all measures
- **Spatial Structure**: Queen contiguity neighbor graph
- **Composite Index**: CHBI with 7 components

Can potentially obtain:
- **Census ACS**: Demographics, economics, housing
- **Policy databases**: Medicaid expansion, minimum wage, etc.
- **Health investment**: HRSA grant data, FQHC locations

---

## 3. PROPOSED ANALYSES

### 3.1 Measurement Error Analysis

**Objective**: Quantify how much of observed "change" is measurement artifact.

Methods:
1. **Signal-to-Noise Ratio**
   - Compare observed year-over-year variance to known measurement uncertainty
   - Formula: SNR = Var(true_change) / Var(measurement_error)
   - Estimate Var(measurement_error) from CDC confidence intervals

2. **Attenuation Correction**
   - Apply measurement error correction to importance estimates
   - Re-estimate predictive performance under various noise assumptions

3. **Reliability Analysis**
   - Calculate test-retest reliability (year-to-year correlation)
   - Compare to reliability of individual PLACES measures
   - Identify which measures drive composite reliability

**Expected Output**: Table showing what fraction of unpredictability is measurement artifact.

### 3.2 Temporal Scale Analysis

**Objective**: Test whether longer trajectories are more predictable.

Methods:
1. **Multi-horizon Prediction**
   - Compare 1-year, 2-year, 3-year trajectory prediction
   - Hypothesis: Longer horizons = more predictable (signal averages out noise)

2. **Trajectory Typology**
   - Cluster tracts by 4-year trajectory shape (improving, declining, stable, volatile)
   - Test if typology is more predictable than year-over-year class

3. **Momentum Analysis**
   - Test if 2-year momentum predicts 3rd year better than 1-year
   - Quantify "trajectory inertia"

**Expected Output**: Performance curves by temporal horizon, optimal prediction window.

### 3.3 Missing Predictor Analysis

**Objective**: Estimate the variance explained by observable vs unobservable factors.

Methods:
1. **Upper Bound Estimation**
   - Calculate theoretical maximum R² given measurement error
   - Compare to achieved R² (0.09)
   - Gap = variance from unobserved factors

2. **Fixed Effects Analysis**
   - Add state, county, or tract fixed effects
   - How much variance do geographic constants explain?
   - Remaining variance = time-varying unexplained

3. **Lagged Dependent Variable Model**
   - AR(1) model: CHBI_t = β*CHBI_{t-1} + ε
   - What is the "natural" predictability from autocorrelation alone?

**Expected Output**: Decomposition of variance into measurement, geography, autoregression, and unexplained.

### 3.4 Chaos vs Randomness

**Objective**: Distinguish deterministic chaos from pure stochastic noise.

Methods:
1. **Lyapunov Exponent Estimation** (if feasible with 4 time points)
   - Positive = chaos; Near zero = random walk

2. **Recurrence Quantification Analysis**
   - Look for deterministic patterns in apparent noise

3. **Tipping Point Detection**
   - Test if trajectory changes are sudden (regime shift) vs gradual
   - Sudden shifts suggest underlying dynamics

**Expected Output**: Evidence for/against deterministic dynamics underlying trajectories.

---

## 4. ACTUAL FINDINGS (From Initial Analysis)

Running `unpredictability_analysis.py` revealed:

1. **STRONG MEAN REVERSION (NOT noise)**
   - Adjacent year correlation: r = -0.40 to -0.58
   - Tracts that improved one year tend to decline the next
   - Beta = -0.40: A 1-unit improvement is followed by 0.4 decline
   - This is the primary driver of unpredictability

2. **Levels are highly persistent (R² = 99.7%)**
   - CHBI levels almost perfectly autocorrelated
   - Healthy tracts stay healthy, unhealthy stay unhealthy
   - But CHANGES are near-random (or reversed)

3. **Geography explains 28% of variance in change**
   - Between-tract differences matter
   - Some tracts are inherently more volatile
   - Between-year differences: <1%

4. **Classification is inherently unstable**
   - With mean reversion, DECLINE → IMPROVE is common
   - Trajectory "class" is unstable year-over-year
   - The 0.3 SD threshold catches temporary fluctuations

---

## 5. PAPER STRUCTURE

**Abstract** (300 words)
**Introduction** (1000 words)
- The promise of trajectory prediction for resource allocation
- The failure: F1=0.26 despite rich features
- Why understanding "why" matters

**Methods** (1500 words)
- Data and composite index construction
- Measurement error framework
- Multi-horizon prediction design
- Variance decomposition approach

**Results** (2000 words)
- Measurement error contribution
- Temporal scale effects
- Geographic vs temporal variance
- (Non-)evidence for deterministic dynamics

**Discussion** (1500 words)
- Implications for "early warning" systems
- When prediction is/isn't appropriate
- Alternative approaches (monitoring, responsiveness)
- Honest limitations

---

## 6. POLICY IMPLICATIONS

If trajectories are fundamentally unpredictable:

1. **Don't build "early warning systems"** based on trajectory prediction
2. **Focus on current burden, not predicted trajectory**
3. **Build responsive systems** that detect and react to change quickly
4. **Invest in better measurement** to reduce noise floor
5. **Use longer time horizons** for strategic planning (3-5 years, not annual)

---

## 7. ANALYSIS SCRIPT OUTLINE

```python
# unpredictability_analysis.py

# 1. MEASUREMENT ERROR ANALYSIS
def estimate_measurement_variance():
    """Use CDC confidence intervals to estimate measurement error variance."""
    pass

def compute_signal_to_noise():
    """SNR = Var(observed_change) / Var(measurement_error)."""
    pass

def reliability_analysis():
    """Test-retest reliability of CHBI and components."""
    pass

# 2. TEMPORAL SCALE ANALYSIS
def multi_horizon_prediction():
    """Compare F1 at 1, 2, 3 year horizons."""
    pass

def trajectory_clustering():
    """Cluster 4-year trajectory shapes."""
    pass

def momentum_analysis():
    """Does 2-year momentum predict 3rd year?"""
    pass

# 3. VARIANCE DECOMPOSITION
def fixed_effects_analysis():
    """State/county/tract fixed effects contribution."""
    pass

def ar1_baseline():
    """AR(1) model predictability baseline."""
    pass

def upper_bound_r2():
    """Theoretical maximum R² given measurement error."""
    pass

# 4. CHAOS ANALYSIS (if feasible)
def recurrence_analysis():
    """Recurrence quantification for chaos detection."""
    pass
```

---

## 8. DATA REQUIREMENTS

**Already have:**
- [ ] CHBI time series 2020-2024
- [ ] Prediction dataset with features
- [ ] Tract neighbor graph

**Need to extract/compute:**
- [ ] CDC confidence intervals for each measure
- [ ] Per-tract, per-year uncertainty estimates
- [ ] Longer trajectory classifications (4-year patterns)

**Nice to have:**
- [ ] ACS demographic controls
- [ ] Policy timing variables

---

## 9. TIMELINE AND DEPENDENCIES

This paper can be written with existing data. New analysis needed:
1. Extract CDC uncertainty estimates from source data
2. Implement measurement error framework
3. Run multi-horizon experiments
4. Variance decomposition analysis

Estimated new code: ~400 lines
Estimated runtime: ~30 minutes (mostly model retraining at different horizons)

---

## 10. CONTRIBUTION

**Novelty:** First systematic analysis of *why* community health trajectories are unpredictable, distinguishing measurement, temporal, and structural sources.

**Impact:** Prevents wasted investment in trajectory-based "early warning" systems that cannot work. Redirects field toward monitoring and responsiveness.

**Audience:** Health planners, epidemiologists, health services researchers, policy analysts.
