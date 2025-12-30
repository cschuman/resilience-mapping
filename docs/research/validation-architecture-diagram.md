# Validation Architecture: Visual Reference
## Community Health Trajectory Prediction System

---

## 1. Temporal Cross-Validation Flow

```
TIME FLOW (Strictly Forward) →
═══════════════════════════════════════════════════════════════════════

SPLIT 1: Early Model Validation
┌─────────────┬─────────────┬─────────────┐
│   2020      │   2021      │   2022      │
│             │             │             │
│  ←────── TRAIN ────────→  │             │
│   (n=52K)   │   (n=53K)   │             │
│             │             │             │
│   Features through 2021   │  VALIDATE   │
│                           │   (n=70K)   │
│   Target: 2021→2022       │             │
└─────────────┴─────────────┴─────────────┘
                              ↓
                         Predict 2022
                         trajectory


SPLIT 2: Intermediate Model Validation
┌─────────────┬─────────────┬─────────────┬─────────────┐
│   2020      │   2021      │   2022      │   2023      │
│             │             │             │             │
│  ←──────────── TRAIN ─────────────────→ │             │
│            (n=105K, then n=70K)         │             │
│                                         │  VALIDATE   │
│   Features through 2022                 │   (n=70K)   │
│                                         │             │
│   Target: 2022→2023                     │             │
└─────────────┴─────────────┴─────────────┴─────────────┘
                                            ↓
                                       Predict 2023
                                       trajectory


SPLIT 3: Mature Model Validation
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│   2020      │   2021      │   2022      │   2023      │   2024      │
│             │             │             │             │             │
│  ←──────────────────── TRAIN ──────────────────────→  │             │
│                    (n=210K)                           │  VALIDATE   │
│                                                       │   (n=70K)   │
│   Features through 2023                               │             │
│                                                       │             │
│   Target: 2023→2024                                   │             │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
                                                          ↓
                                                     Predict 2024
                                                     trajectory


SPLIT 4: Production Model Validation
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│   2020      │   2021      │   2022      │   2023      │   2024      │   2025      │
│             │             │             │             │             │             │
│  ←────────────────────────── TRAIN ────────────────────────────────→│             │
│                           (n=280K)                                  │  VALIDATE   │
│                                                                     │   (n=70K)   │
│   Features through 2024                                             │             │
│                                                                     │             │
│   Target: 2024→2025                                                 │             │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
                                                                        ↓
                                                                   Predict 2025
                                                                   trajectory

═══════════════════════════════════════════════════════════════════════

KEY PRINCIPLE: Training data ALWAYS predates validation data
             NO future information EVER flows backward in time
```

---

## 2. Nested Cross-Validation for Hyperparameter Tuning

```
OUTER LOOP: Performance Estimation (Unbiased)
═══════════════════════════════════════════════════════════════

For Split 3 (Validating on 2024):

    INNER LOOP: Hyperparameter Selection
    ┌─────────────────────────────────────────────────────┐
    │                                                     │
    │  Train Set        Val Set         Test Set         │
    │  (2020-2021)   →  (2022)          (2023)          │
    │     ↓                ↓              ↓              │
    │  Try XGBoost     Evaluate       HOLD OUT          │
    │  depth=4,6,8     each config    (never seen)      │
    │  lr=0.01,0.05    ───────→                         │
    │                  Select best                       │
    │                  (e.g., depth=6)                   │
    └─────────────────────────────────────────────────────┘
                            ↓
                    Best hyperparameters
                            ↓
    OUTER LOOP: Final Training
    ┌─────────────────────────────────────────────────────┐
    │                                                     │
    │  Train on ALL 2020-2023  →  Validate on 2024      │
    │  (using selected hyperparameters)                  │
    │                                                     │
    │  Report metrics from 2024 as UNBIASED estimate     │
    │  (these are what goes in publication Table 2)      │
    └─────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════
PREVENTS: Hyperparameter overfitting to validation set
```

---

## 3. Data Leakage Prevention Architecture

```
FEATURE ENGINEERING PIPELINE (SAFE)
═══════════════════════════════════════════════════════════════

For predicting 2024 outcomes:

┌─────────────────────────────────────────────────────────────┐
│                    RAW DATA                                 │
├─────────────────────────────────────────────────────────────┤
│  CDC PLACES:        2020, 2021, 2022, 2023 ✓               │
│                     2024 ✗ (this is what we predict!)       │
│                                                             │
│  Census ACS:        2019, 2020, 2021, 2022 ✓               │
│                     (1-year publication lag)                │
│                                                             │
│  Spatial Features:  Computed from 2023 data ✓              │
│                     (neighbors' CHBI in 2023)               │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    FEATURE CREATION
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  FEATURE MATRIX                             │
├─────────────────────────────────────────────────────────────┤
│  CHBI_zscore_prev:     2023 value ✓                        │
│  CHBI_change_1yr:      2022→2023 change ✓                  │
│  trend_slope:          Slope through 2023 ✓                │
│  spatial_lag:          Neighbors' 2023 CHBI ✓              │
│  median_income:        2022 ACS value ✓                    │
│                                                             │
│  FORBIDDEN FEATURES:                                        │
│  ✗ CHBI_2024          (target year!)                       │
│  ✗ target_change      (what we're predicting!)             │
│  ✗ future_anything    (time traveler information)          │
└─────────────────────────────────────────────────────────────┘
                            ↓
                      LEAKAGE AUDIT
                            ↓
                 ┌─────────────────────┐
                 │   All checks pass?  │
                 └──────────┬──────────┘
                            │
           ┌────────────────┴────────────────┐
           │                                 │
          YES                               NO
           │                                 │
           ↓                                 ↓
    PROCEED TO                        FIX LEAKAGE
     TRAINING                          (CRITICAL!)
           │
           ↓
   MODEL TRAINING ON
   2020-2023 DATA
           │
           ↓
   PREDICT 2024
   TRAJECTORIES
           │
           ↓
   EVALUATE ON
   ACTUAL 2024
   OUTCOMES

═══════════════════════════════════════════════════════════════
```

---

## 4. Model Performance Evaluation Flow

```
METRICS CALCULATION HIERARCHY
═══════════════════════════════════════════════════════════════

Raw Predictions (from model)
        │
        ├──→ y_pred (class labels: 0, 1, 2)
        │
        └──→ y_pred_proba (probabilities: n × 3 matrix)
                │
                ├─────────────────────────────────────────────┐
                │                                             │
                ↓                                             ↓
    PRIMARY METRICS                              CALIBRATION METRICS
    (Clinical Utility)                           (Trustworthiness)
    ┌─────────────────────┐                     ┌──────────────────┐
    │ Sensitivity         │                     │ ECE              │
    │ (DECLINE class)     │                     │ Brier Score      │
    │                     │                     │ Hosmer-Lemeshow  │
    │ PPV (Precision)     │                     │ Calibration Plot │
    │                     │                     └──────────────────┘
    │ F1-Score            │                              │
    │                     │                              ↓
    │ Balanced Accuracy   │                     Is ECE < 0.10?
    │                     │                              │
    │ Cohen's Kappa       │                    ┌─────────┴─────────┐
    │                     │                    │                   │
    │ AUC-ROC             │                   YES                 NO
    └─────────────────────┘                    │                   │
            │                                  │                   ↓
            ↓                                  │             Apply Platt
    Do all meet targets?                       │             Scaling
            │                                  │                   │
    ┌───────┴────────┐                        │                   ↓
    │                │                         │             Re-evaluate
   YES              NO                         │                   │
    │                │                         └───────────────────┘
    │                ↓                                      │
    │         INVESTIGATE                                  │
    │         - Class imbalance?                           │
    │         - Feature quality?                           │
    │         - Model architecture?                        │
    │                                                      │
    ↓                                                      ↓
PROCEED TO                                      DEPLOY CALIBRATED
SUBGROUP                                        PREDICTIONS
ANALYSIS
    │
    ↓
┌────────────────────────────────────────────────────────────┐
│              STRATIFIED PERFORMANCE                        │
├────────────────────────────────────────────────────────────┤
│  Urban vs Rural                                            │
│  ├─ Urban:  Sensitivity = X%                              │
│  └─ Rural:  Sensitivity = Y%                              │
│      └─ Disparity = |X - Y| < 10pp? ──→ YES ──→ PASS     │
│                                      └→ NO ──→ LIMITATION  │
│                                                            │
│  By Census Region                                         │
│  ├─ Northeast: Z₁%                                        │
│  ├─ Midwest:   Z₂%                                        │
│  ├─ South:     Z₃%                                        │
│  └─ West:      Z₄%                                        │
│      └─ Max disparity < 10pp? ──→ Report in Table 5      │
│                                                            │
│  By Baseline Health                                       │
│  └─ Check for ceiling/floor effects                       │
└────────────────────────────────────────────────────────────┘
    │
    ↓
COMPARE TO
BASELINES
    │
    ├──→ Persistence: Does model beat "no change"?
    ├──→ Linear Trend: Better than simple extrapolation?
    └──→ Logistic Regression: Ensemble worth complexity?
           │
           ↓
    Statistical Test (paired t-test across folds)
           │
           ├──→ p < 0.05? ──→ YES ──→ SIGNIFICANT
           │                          IMPROVEMENT
           │
           └──→ p ≥ 0.05? ──→ NO ──→  MODEL NOT
                                       BETTER THAN
                                       BASELINE

═══════════════════════════════════════════════════════════════
```

---

## 5. Uncertainty Quantification Architecture

```
PREDICTION WITH UNCERTAINTY
═══════════════════════════════════════════════════════════════

For each test sample (census tract):

Point Prediction                    Uncertainty Quantification
       │                                      │
       ↓                                      ↓
┌──────────────┐                    ┌──────────────────┐
│ Ensemble     │                    │ Bootstrap        │
│ produces:    │                    │ (100 resamples)  │
│              │                    │                  │
│ P(DECLINE)   │                    │ Train on boot_i  │
│   = 0.68     │                    │ Predict on test  │
│              │                    │ ↓                │
│ P(STABLE)    │                    │ Get 100 sets of  │
│   = 0.24     │                    │ predictions      │
│              │                    │ ↓                │
│ P(IMPROVE)   │                    │ Calculate:       │
│   = 0.08     │                    │ - Mean = 0.68    │
└──────────────┘                    │ - 2.5th% = 0.53  │
       │                            │ - 97.5th%= 0.81  │
       │                            └──────────────────┘
       │                                      │
       ↓                                      ↓
┌────────────────────────────────────────────────────────────┐
│              FINAL PREDICTION OUTPUT                       │
├────────────────────────────────────────────────────────────┤
│  Tract: 06037268401                                        │
│  Prediction: DECLINE (68% probability)                     │
│  95% CI: [53% - 81%]                                       │
│  Interpretation: High confidence (narrow CI)               │
│                                                            │
│  Risk Tier: HIGH RISK (Confident)                         │
│             → Recommend Priority Intervention              │
│                                                            │
│  Top Contributing Factors (SHAP):                          │
│    1. Rising poverty rate (+0.12)                          │
│    2. Upward CHBI trend (+0.09)                            │
│    3. High neighboring burden (+0.07)                      │
└────────────────────────────────────────────────────────────┘

Alternative: Conformal Prediction Sets
┌────────────────────────────────────────────────────────────┐
│  Prediction Set: {DECLINE, STABLE}                         │
│  (90% guaranteed coverage)                                 │
│                                                            │
│  Set Size = 2 → Moderate uncertainty                       │
│  Either DECLINE or STABLE plausible                        │
│  Recommend: Enhanced surveillance, not immediate           │
│             intervention                                   │
└────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════
```

---

## 6. Publication Reporting Flow

```
RESULTS → TABLES/FIGURES → MANUSCRIPT
═══════════════════════════════════════════════════════════════

Raw Model Outputs
       │
       ├──→ Fold 1 metrics
       ├──→ Fold 2 metrics
       ├──→ Fold 3 metrics
       └──→ Fold 4 metrics
              │
              ↓
       AGGREGATE METRICS
       (mean ± 95% CI)
              │
              ├────────────────────────────────────────────┐
              │                                            │
              ↓                                            ↓
    MAIN TEXT TABLES                           SUPPLEMENTARY MATERIALS
    ┌──────────────────┐                      ┌────────────────────────┐
    │ Table 1:         │                      │ Table S1: CONSORT      │
    │  Descriptives    │                      │ Table S2: Hyperparam   │
    │                  │                      │ Table S3: Feature List │
    │ Table 2:         │                      │ Table S4-S7: Subgroups │
    │  Performance★    │                      │ Table S8: Calibration  │
    │  (PRIMARY)       │                      │ Table S9: Sensitivity  │
    │                  │                      │ Table S10: External    │
    │ Table 3:         │                      └────────────────────────┘
    │  Feature Imp     │                                 │
    │                  │                                 │
    │ Table 4:         │                                 │
    │  Baselines       │                                 │
    │                  │                                 │
    │ Table 5:         │                                 │
    │  Urban/Rural     │                                 │
    └──────────────────┘                                 │
              │                                          │
              ├──────────────────────────────────────────┤
              │                                          │
              ↓                                          ↓
    MAIN TEXT FIGURES                        SUPPLEMENTARY FIGURES
    ┌──────────────────┐                    ┌─────────────────────┐
    │ Figure 1:        │                    │ Figure S1: Trends   │
    │  Calibration★    │                    │ Figure S2: Corr Heatmap│
    │                  │                    │ Figure S3: Extended Cal│
    │ Figure 2:        │                    │ Figure S4: SHAP Depend │
    │  SHAP Summary★   │                    │ Figure S5-S10: Other │
    │                  │                    └─────────────────────┘
    │ Figure 3:        │
    │  Geographic Map  │
    └──────────────────┘
              │
              ↓
    ┌─────────────────────────────────────────────┐
    │          MANUSCRIPT ASSEMBLY                │
    ├─────────────────────────────────────────────┤
    │                                             │
    │  ABSTRACT                                   │
    │    ├─ Primary finding: "71% sensitivity"   │
    │    └─ Key conclusion                        │
    │                                             │
    │  INTRODUCTION                               │
    │    ├─ Gap in literature                     │
    │    └─ Study objective                       │
    │                                             │
    │  METHODS                                    │
    │    ├─ Data sources                          │
    │    ├─ Temporal CV design★                   │
    │    ├─ Leakage prevention★                   │
    │    └─ Statistical analysis                  │
    │                                             │
    │  RESULTS                                    │
    │    ├─ Table 1 (descriptives)               │
    │    ├─ Table 2 (PRIMARY OUTCOME)★           │
    │    ├─ Figure 1 (calibration)               │
    │    └─ Figure 2 (SHAP)                      │
    │                                             │
    │  DISCUSSION                                 │
    │    ├─ Key findings interpretation           │
    │    ├─ Comparison to prior work             │
    │    ├─ Limitations (5 paragraphs)           │
    │    └─ Implications for practice            │
    │                                             │
    │  SUPPLEMENTARY MATERIALS                    │
    │    ├─ Extended methods                      │
    │    ├─ Additional tables (S1-S10)           │
    │    ├─ Additional figures (S1-S10)          │
    │    └─ Code availability statement          │
    └─────────────────────────────────────────────┘
                        │
                        ↓
                SUBMIT TO JOURNAL
                        │
                        ↓
            ┌───────────┴───────────┐
            │                       │
        ACCEPTED              MAJOR REVISION
            │                       │
            ↓                       ↓
       CELEBRATE!            RESPOND TO
                            REVIEWERS
                                  │
                                  ↓
                            RE-SUBMIT

═══════════════════════════════════════════════════════════════
★ = Critical components for peer review survival
```

---

## 7. Quality Control Gates

```
VALIDATION PIPELINE WITH QUALITY GATES
═══════════════════════════════════════════════════════════════

START
  │
  ↓
┌─────────────────┐
│ GATE 1:         │ ──→ FAIL ──→ STOP: Fix data issues
│ Data Quality    │
│ - Missing data? │
│ - Duplicates?   │
│ - Outliers?     │
└────────┬────────┘
         │ PASS
         ↓
┌─────────────────┐
│ GATE 2:         │ ──→ FAIL ──→ STOP: Fix leakage (CRITICAL)
│ Leakage Audit   │
│ - Temporal?     │
│ - Target?       │
│ - Preprocessing?│
└────────┬────────┘
         │ PASS
         ↓
┌─────────────────┐
│ GATE 3:         │ ──→ FAIL ──→ INVESTIGATE: Model architecture
│ Training        │                           or data issues
│ - Converged?    │
│ - No errors?    │
│ - Time OK?      │
└────────┬────────┘
         │ PASS
         ↓
┌─────────────────┐
│ GATE 4:         │ ──→ FAIL ──→ RETUNE or RECALIBRATE
│ Performance     │
│ - Metrics ≥     │
│   targets?      │
│ - ECE < 0.10?   │
└────────┬────────┘
         │ PASS
         ↓
┌─────────────────┐
│ GATE 5:         │ ──→ FAIL ──→ REPORT AS LIMITATION
│ Subgroup        │              (may still publish)
│ Fairness        │
│ - Disparity     │
│   < 10pp?       │
└────────┬────────┘
         │ PASS
         ↓
┌─────────────────┐
│ GATE 6:         │ ──→ FAIL ──→ RE-RUN on new hardware
│ Reproducibility │              FIX random seeds
│ - Code runs?    │
│ - Results match?│
└────────┬────────┘
         │ PASS
         ↓
  APPROVED FOR
   PUBLICATION

═══════════════════════════════════════════════════════════════
```

---

## 8. Reviewer Response Decision Tree

```
HANDLING PEER REVIEW
═══════════════════════════════════════════════════════════════

Reviewer raises concern
         │
         ↓
  Is it about leakage?
         │
    ┌────┴────┐
    │         │
   YES       NO
    │         │
    ↓         ↓
Show audit  Is it about
protocol    generalizability?
    │            │
    │       ┌────┴────┐
    │       │         │
    │      YES       NO
    │       │         │
    │       ↓         ↓
    │   Acknowledge  Is it about
    │   limitation   sample size?
    │   + cite           │
    │   future       ┌───┴───┐
    │   validation   │       │
    │                │      YES    NO
    │                │       │      │
    │                │       ↓      ↓
    │                │   Show    Other
    │                │   power   concern
    │                │   calc      │
    │                │       │     ↓
    └────────────────┴───────┴─→ Assess:
                                Can fix with
                                 new analysis?
                                    │
                              ┌─────┴─────┐
                              │           │
                             YES         NO
                              │           │
                              ↓           ↓
                          Run new     Rebuttal with
                          analysis    evidence from
                              │       existing results
                              │           │
                              └─────┬─────┘
                                    │
                                    ↓
                              Revise manuscript
                                    │
                                    ↓
                                Re-submit

═══════════════════════════════════════════════════════════════
```

---

**Document Version**: 1.0
**Last Updated**: December 30, 2025
**Companion Documents**:
- Full specification: `validation-strategy-specification.md`
- Quick reference: `validation-quick-reference.md`
- Audit checklist: `validation-audit-checklist.md`
