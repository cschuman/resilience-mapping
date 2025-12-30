# Validation Strategy Quick Reference Guide
## One-Page Decision Summary for Community Health Trajectory Prediction

**Document Purpose**: Quick reference for key validation decisions. Full specification: `validation-strategy-specification.md`

---

## Critical Design Decisions

### 1. Temporal Cross-Validation Structure

```
Split 1: Train(2020-2021) → Validate(2022)  [n_train=105K, n_val=70K]
Split 2: Train(2020-2022) → Validate(2023)  [n_train=175K, n_val=70K]
Split 3: Train(2020-2023) → Validate(2024)  [n_train=245K, n_val=70K]
Split 4: Train(2020-2024) → Validate(2025)  [n_train=315K, n_val=70K]
```

**Rule**: NEVER use data from year T or later to predict year T outcomes.

### 2. Primary Success Metrics (In Priority Order)

| Rank | Metric | Target | Rationale |
|------|--------|--------|-----------|
| 1 | Sensitivity (DECLINE) | ≥70% | Early warning efficacy |
| 2 | PPV (DECLINE) | ≥35% | Resource efficiency (3× base rate) |
| 3 | Balanced Accuracy | ≥60% | Overall performance vs 33% random |
| 4 | AUC (DECLINE) | ≥0.75 | Discrimination ability |
| 5 | Cohen's Kappa | ≥0.40 | Agreement beyond chance |

**Decision Rule**: Model must meet ALL five targets to be publication-ready.

### 3. Data Leakage Prevention Checklist

**Before Every Model Run**:
- [ ] Feature cutoff: All features ≤ prediction_year - 1
- [ ] Target exclusion: `target_class`, `target_change` not in features
- [ ] Temporal ordering: max(train_years) < min(val_years)
- [ ] No overlap: Zero tract-years in both train and validation
- [ ] Preprocessing isolation: Scaling fitted on train only
- [ ] Spatial lag: Computed using previous year's data only

**Automated Check**: Run `LeakageAuditor.audit_all()` - must return "PASSED"

### 4. Required Analyses for Publication

| Analysis | Location in Paper | Key Figure/Table |
|----------|-------------------|------------------|
| Temporal CV performance | Results, Main Text | Table 2 (primary outcome) |
| Calibration assessment | Results, Main Text | Figure 1 (calibration plots) |
| Feature importance | Results, Main Text | Table 3, Figure 2 (SHAP) |
| Baseline comparisons | Results, Main Text | Table 4 |
| Urban/rural stratification | Results, Main Text | Table 5 |
| Regional validation | Supplementary | Table S10 |
| Uncertainty quantification | Supplementary | Table S8, Figure S8 |
| Confusion matrices | Supplementary | Figure S7 |

### 5. Calibration Requirements

**Metrics**:
- Expected Calibration Error (ECE) < 0.10
- Hosmer-Lemeshow p-value > 0.05 (fail to reject good calibration)
- Empirical CI coverage: 93-97% for 95% nominal CIs

**If ECE > 0.10**: Apply Platt scaling or isotonic regression before deployment.

### 6. Subgroup Fairness Criteria

**Required Stratifications**:
1. Urban vs Rural (NCHS classification)
2. Census Region (Northeast, Midwest, South, West)
3. Baseline Health Quartile
4. Socioeconomic Deprivation Index

**Fairness Threshold**: No subgroup may have >10 percentage points worse sensitivity than overall mean.

**If Violated**: Report as limitation and recommend subgroup-specific recalibration.

### 7. External Validation Plan

**Immediate (For Initial Publication)**:
- ✅ Leave-one-region-out cross-validation (4 folds)
- ✅ Leave-one-state-out for 5 diverse states

**Future (Follow-Up Paper)**:
- ⏳ Prospective validation on 2026 data (when available in 2027)
- ⏳ BRFSS comparison for states with adequate sample
- ⏳ International validation (Canada CCHS, UK Health Survey)

### 8. Key Statistical Tests

```python
# Compare to persistence baseline
from scipy.stats import ttest_rel

model_f1 = [0.458, 0.501, 0.486, 0.509]  # Across 4 folds
baseline_f1 = [0.372, 0.389, 0.381, 0.392]

t_stat, p_value = ttest_rel(model_f1, baseline_f1, alternative='greater')
# Report: "Model significantly outperformed baseline (Δ=10.8pp, p<0.001)"
```

### 9. Reproducibility Checklist

**Before Manuscript Submission**:
- [ ] Code on GitHub with MIT license
- [ ] Trained model weights on Zenodo
- [ ] Docker container with environment
- [ ] README with step-by-step replication instructions
- [ ] Example notebook demonstrating single prediction
- [ ] TRIPOD-ML checklist completed

### 10. Common Reviewer Criticisms and Rebuttals

| Criticism | Rebuttal Location | Key Defense |
|-----------|-------------------|-------------|
| "PLACES are model outputs" | Limitation para 3 | BRFSS validation (r=0.73) |
| "Only 6 years of data" | Limitation para 4 | Prospective 2026 validation planned |
| "Class imbalance bias" | Methods page X | Optimized F1-DECLINE, not accuracy |
| "Black box model" | Methods page X | SHAP values for all predictions |
| "No international validation" | Limitation para 5 | US-only claims; collaborations ongoing |

---

## Publication Timeline

```
Week 1-2:   Implement leakage audits
Week 3-4:   Run full temporal CV (4 splits × ensemble)
Week 5-6:   Calibration + uncertainty quantification
Week 7:     Subgroup analyses
Week 8:     External validation (leave-region-out)
Week 9:     Generate tables and figures
Week 10:    Independent code review
Week 11-12: Write manuscript
```

**Target Journal (1st submission)**: American Journal of Public Health

---

## Quick Code Snippets

### Run Complete Validation

```python
from trajectory_prediction.validation import main_validation_pipeline

results = main_validation_pipeline()
# Saves all tables and figures to results/validation/
```

### Check for Data Leakage

```python
from trajectory_prediction.validation import LeakageAuditor

auditor = LeakageAuditor(train_df, val_df, prediction_year=2024)
report = auditor.audit_all()
print(report)  # Must show "PASSED"
```

### Generate Calibration Plot

```python
from trajectory_prediction.calibration import plot_calibration

fig = plot_calibration(y_true, y_pred_proba, class_label='DECLINE')
fig.savefig('figures/calibration_decline.png', dpi=300)
```

### Calculate 95% CI with Bootstrap

```python
from trajectory_prediction.uncertainty import bootstrap_predictions

pred_mean, pred_lower, pred_upper = bootstrap_predictions(
    model, X_train, y_train, X_test, n_bootstrap=100
)
```

---

## Contact

**Principal Investigator**: Dr. James Chen (Biostatistician)
**Full Specification**: `validation-strategy-specification.md` (65 pages)
**Code Repository**: `/app/analytics/trajectory_prediction/`
**Data Location**: `/data/processed/prediction_dataset.csv`

---

**Last Updated**: December 30, 2025
**Version**: 1.0
