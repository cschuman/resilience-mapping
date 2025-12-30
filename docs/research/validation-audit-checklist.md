# VALIDATION AUDIT CHECKLIST
## Community Health Trajectory Prediction Model

**Date**: ________________
**Model Version**: ________________
**Validation Split**: ☐ Split 1 (2022)  ☐ Split 2 (2023)  ☐ Split 3 (2024)  ☐ Split 4 (2025)
**Auditor Name**: ________________
**Signature**: ________________

---

## SECTION 1: DATA INTEGRITY (CRITICAL - Must Pass 100%)

### 1.1 Temporal Separation
- [ ] **All training years < validation year**
  - Training years: ____________
  - Validation year: ____________
  - Max train year < Min val year: ☐ YES ☐ NO

- [ ] **No future data used in features**
  - Latest feature year: ____________
  - Validation year: ____________
  - Latest feature year < Validation year: ☐ YES ☐ NO

### 1.2 Target Leakage Prevention
- [ ] **Target variable excluded from features**
  - `target_class` in feature_cols: ☐ NO ☐ YES (CRITICAL ERROR)
  - `target_change` in feature_cols: ☐ NO ☐ YES (CRITICAL ERROR)
  - Any `future_*` columns in feature_cols: ☐ NO ☐ YES (CRITICAL ERROR)

- [ ] **Current year CHBI excluded**
  - Feature cutoff year: ____________
  - Validation year CHBI used: ☐ NO ☐ YES (CRITICAL ERROR)

### 1.3 Train/Validation Contamination
- [ ] **No overlap between train and validation**
  - Number of overlapping tract-years: ____________ (MUST BE ZERO)
  - Overlap check passed: ☐ YES ☐ NO

### 1.4 Preprocessing Isolation
- [ ] **Scaler fitted on training data only**
  - Scaler.fit() called on: ☐ Train only ☐ Train+Val (ERROR)

- [ ] **Imputation used training statistics only**
  - Imputer.fit() called on: ☐ Train only ☐ Train+Val (ERROR)

- [ ] **CHBI z-scores computed within-year**
  - Z-score reference: ☐ Within-year ☐ Across all years (ERROR)

### 1.5 Spatial Feature Integrity
- [ ] **Spatial lag computed from previous year**
  - Spatial lag year: ____________
  - Validation year: ____________
  - Spatial lag year < Validation year: ☐ YES ☐ NO

---

## SECTION 2: MODEL TRAINING INTEGRITY

### 2.1 Hyperparameter Tuning
- [ ] **Hyperparameters tuned on separate fold**
  - Tuning set: ____________
  - Validation set: ____________
  - Tuning set ≠ Validation set: ☐ YES ☐ NO

- [ ] **No validation set contamination during tuning**
  - Confirmed separate: ☐ YES ☐ NO

### 2.2 Random Seed Control
- [ ] **Random seed set for reproducibility**
  - Random seed value: ____________
  - Seed set before train/test split: ☐ YES ☐ NO

### 2.3 Class Imbalance Handling
- [ ] **Class distribution documented**
  - Train: DECLINE=____% STABLE=____% IMPROVE=____%
  - Val: DECLINE=____% STABLE=____% IMPROVE=____%

- [ ] **Class imbalance addressed**
  - Method: ☐ Class weights ☐ SMOTE ☐ None ☐ Other: ____________

---

## SECTION 3: PREDICTION QUALITY

### 3.1 Missing Predictions Check
- [ ] **No missing predictions**
  - Predictions generated: ______ / ______ (should be 100%)
  - Missing predictions: ☐ NONE ☐ Some (investigate)

### 3.2 Probability Validity
- [ ] **Probabilities sum to 1.0**
  - Min sum: ____________ (should be ~1.0)
  - Max sum: ____________ (should be ~1.0)
  - All sums valid: ☐ YES ☐ NO

- [ ] **Probabilities in valid range [0,1]**
  - Min probability: ____________ (should be ≥0)
  - Max probability: ____________ (should be ≤1)
  - All valid: ☐ YES ☐ NO

---

## SECTION 4: PERFORMANCE METRICS

### 4.1 Primary Metrics (Early Warning)
- [ ] **Sensitivity (DECLINE) ≥ 70%**
  - Achieved: ________% ☐ PASS ☐ FAIL

- [ ] **PPV (DECLINE) ≥ 35%**
  - Achieved: ________% ☐ PASS ☐ FAIL

- [ ] **Balanced Accuracy ≥ 60%**
  - Achieved: ________% ☐ PASS ☐ FAIL

- [ ] **AUC (DECLINE) ≥ 0.75**
  - Achieved: ________ ☐ PASS ☐ FAIL

- [ ] **Cohen's Kappa ≥ 0.40**
  - Achieved: ________ ☐ PASS ☐ FAIL

**ALL PRIMARY METRICS PASS**: ☐ YES ☐ NO

### 4.2 Comparison to Baseline
- [ ] **Significantly better than persistence**
  - Model F1 (DECLINE): ________%
  - Baseline F1: ________%
  - Improvement: ________pp
  - P-value: ________ (should be <0.05)

---

## SECTION 5: CALIBRATION

### 5.1 Calibration Metrics
- [ ] **Expected Calibration Error < 0.10**
  - Achieved: ________ ☐ PASS ☐ FAIL

- [ ] **Hosmer-Lemeshow p-value > 0.05**
  - Achieved: ________ ☐ PASS ☐ FAIL

- [ ] **Calibration plot reviewed**
  - Visually well-calibrated: ☐ YES ☐ NO
  - Saved to: ________________________________

### 5.2 Calibration Correction (if needed)
- [ ] **If ECE > 0.10, calibration applied**
  - Calibration method: ☐ Platt ☐ Isotonic ☐ N/A
  - Post-calibration ECE: ________ (should be <0.10)

---

## SECTION 6: UNCERTAINTY QUANTIFICATION

### 6.1 Confidence Intervals
- [ ] **95% CIs generated**
  - Method: ☐ Bootstrap ☐ Conformal ☐ Both

- [ ] **CI coverage validated**
  - Empirical coverage: ________% (target: 93-97%)
  - Coverage check: ☐ PASS ☐ FAIL

### 6.2 Prediction Set Analysis (Conformal)
- [ ] **Prediction sets generated**
  - Mean set size: ________ (1=confident, 3=uncertain)
  - % singleton sets: ________% (higher = better)

---

## SECTION 7: SUBGROUP FAIRNESS

### 7.1 Urban/Rural Analysis
- [ ] **Urban performance documented**
  - Sensitivity (DECLINE): ________%

- [ ] **Rural performance documented**
  - Sensitivity (DECLINE): ________%

- [ ] **Disparity check**
  - Absolute difference: ________pp (should be <10pp)
  - Disparity acceptable: ☐ YES ☐ NO

### 7.2 Regional Analysis
- [ ] **Performance by region documented**
  - Northeast: ________%
  - Midwest: ________%
  - South: ________%
  - West: ________%
  - Max difference: ________pp (should be <10pp)

### 7.3 Baseline Health Stratification
- [ ] **Performance across health quartiles**
  - Q1 (Low): ________%
  - Q4 (High): ________%
  - Difference: ________pp (should be <10pp)

**ALL SUBGROUPS WITHIN 10pp**: ☐ YES ☐ NO

---

## SECTION 8: EXTERNAL VALIDATION (If Applicable)

### 8.1 Geographic External Validation
- [ ] **Leave-region-out CV conducted**
  - Holdout region: ____________
  - Performance: ________% (compare to internal)
  - Degradation: ________pp (should be <5pp)

### 8.2 Temporal External Validation
- [ ] **Prospective validation (2026 when available)**
  - Status: ☐ Pending ☐ Complete
  - Performance: ________%

---

## SECTION 9: REPRODUCIBILITY

### 9.1 Code Availability
- [ ] **Code committed to GitHub**
  - Commit hash: ________________________________
  - Branch: ____________

- [ ] **Environment documented**
  - environment.yml updated: ☐ YES ☐ NO

### 9.2 Results Saved
- [ ] **Model weights saved**
  - Location: ________________________________
  - File size: ____________

- [ ] **Predictions saved**
  - Location: ________________________________
  - Format: ☐ CSV ☐ Parquet ☐ Other: ____________

- [ ] **Metrics logged**
  - Location: ________________________________

### 9.3 Figures Generated
- [ ] **Calibration plot saved**
- [ ] **ROC curve saved**
- [ ] **SHAP summary plot saved**
- [ ] **Confusion matrix saved**

---

## SECTION 10: FINAL SIGN-OFF

### 10.1 Critical Errors (MUST BE ZERO)
Total critical errors detected: ________ (MUST BE 0 TO PROCEED)

**Critical errors include**:
- Target leakage
- Temporal contamination
- Train/validation overlap
- Missing/invalid predictions

### 10.2 Performance Requirements
- [ ] All 5 primary metrics pass: ☐ YES ☐ NO
- [ ] Calibration acceptable (ECE <0.10): ☐ YES ☐ NO
- [ ] Subgroup fairness (all within 10pp): ☐ YES ☐ NO
- [ ] Significantly better than baseline: ☐ YES ☐ NO

### 10.3 Approval Decision

**Model Status**:
☐ **APPROVED** - Ready for inclusion in manuscript
☐ **CONDITIONAL** - Minor issues to address (list below)
☐ **REJECTED** - Critical errors detected, must rerun

**Issues to Address (if conditional)**:
1. ________________________________________________
2. ________________________________________________
3. ________________________________________________

---

## SIGNATURES

**Primary Auditor**: ________________________  Date: __________
**Secondary Reviewer**: ________________________  Date: __________
**PI Approval**: ________________________  Date: __________

---

## NOTES/COMMENTS

_________________________________________________________________________
_________________________________________________________________________
_________________________________________________________________________
_________________________________________________________________________
_________________________________________________________________________

---

**Checklist Version**: 1.0
**Last Updated**: December 30, 2025
**Document Reference**: `validation-strategy-specification.md`

---

## APPENDIX: Automated Audit Script

```python
# Run this BEFORE manual checklist
from trajectory_prediction.validation import LeakageAuditor

auditor = LeakageAuditor(train_df, val_df, prediction_year)
report = auditor.audit_all()

if "CRITICAL" in report:
    print("❌ AUTOMATED AUDIT FAILED")
    print(report)
    exit(1)
else:
    print("✓ Automated audit passed - proceed to manual checklist")
```

**Save this completed checklist to**: `results/validation/audit_split{N}_{date}.pdf`
