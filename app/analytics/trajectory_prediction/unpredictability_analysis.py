#!/usr/bin/env python3
"""
Paper 2: The Fundamental Unpredictability of Community Health Trajectories

Analyzes WHY trajectory prediction fails (F1=0.26):
1. Measurement error contribution
2. Temporal scale effects
3. Variance decomposition
4. (Limited) chaos analysis

Author: Corey Schuman
Date: 2025-12-30
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import f1_score, balanced_accuracy_score, r2_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
import xgboost as xgb
from scipy import stats
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
INTERIM_DIR = PROJECT_ROOT / "data" / "interim"

print("=" * 70)
print("PAPER 2: THE UNPREDICTABILITY OF COMMUNITY HEALTH TRAJECTORIES")
print("=" * 70)


# =============================================================================
# 1. MEASUREMENT ERROR ANALYSIS
# =============================================================================
def measurement_error_analysis():
    """
    Quantify how much of observed trajectory "change" is measurement artifact.

    CDC PLACES estimates have uncertainty. If year-over-year changes are
    within measurement error, they're mostly noise.
    """
    print("\n" + "=" * 70)
    print("1. MEASUREMENT ERROR ANALYSIS")
    print("=" * 70)

    df = pd.read_csv(DATA_DIR / "prediction_dataset_spatial.csv")

    # We need the raw PLACES data with confidence intervals
    # For now, use published uncertainty estimates

    # CDC PLACES typical 95% CI width for tract estimates:
    # - Obesity: ±3-5 percentage points
    # - Diabetes: ±2-4 percentage points
    # - CHD: ±1-3 percentage points
    # - Mental health: ±3-5 percentage points
    # - Hypertension: ±3-5 percentage points

    # Conservative estimate: ±3% for most measures
    # This means measurement error std ≈ 3/1.96 ≈ 1.5 percentage points per measure

    print("\nAssumed Measurement Error (based on CDC published CIs):")
    print("  Per-measure std: ~1.5 percentage points")
    print("  For composite CHBI: ~1.0 (error averages across 7 measures)")

    # Get observed year-over-year variance
    df_2024 = df[df['PredictionYear'] == 2024]

    if 'target_change' in df.columns:
        changes = df_2024['target_change'].dropna()

        observed_var = changes.var()
        observed_std = changes.std()

        # Measurement error variance (conservative)
        # For change score: Var(X2 - X1) = Var(X2) + Var(X1) = 2 * Var_measurement
        # Assuming measurement std = 1.0 for CHBI
        measurement_std = 1.0
        measurement_var_change = 2 * (measurement_std ** 2)

        # Signal variance (true variation)
        signal_var = max(0, observed_var - measurement_var_change)

        # Signal-to-noise ratio
        snr = signal_var / measurement_var_change if measurement_var_change > 0 else float('inf')

        # Reliability coefficient
        reliability = signal_var / observed_var if observed_var > 0 else 0

        print(f"\nObserved Change Distribution:")
        print(f"  Mean: {changes.mean():.4f}")
        print(f"  Std: {observed_std:.4f}")
        print(f"  Variance: {observed_var:.4f}")

        print(f"\nVariance Decomposition:")
        print(f"  Observed variance: {observed_var:.4f}")
        print(f"  Measurement variance: {measurement_var_change:.4f}")
        print(f"  Estimated signal variance: {signal_var:.4f}")

        print(f"\nSignal-to-Noise Analysis:")
        print(f"  SNR: {snr:.2f}")
        print(f"  Reliability: {reliability:.2%}")
        print(f"  Noise fraction: {1 - reliability:.2%}")

        # What this means for prediction
        print(f"\nImplication for Prediction:")
        print(f"  Maximum achievable R² (attenuation-corrected): {reliability:.3f}")
        print(f"  Our achieved R² (spatial features): 0.093")
        print(f"  Gap: {reliability - 0.093:.3f}")

        if reliability < 0.5:
            print(f"\n  WARNING: More than half of observed variance is measurement noise!")
            print(f"  True community trajectories may be far more stable than data suggests.")

        # Classification threshold analysis
        threshold = 0.3 * observed_std
        n_decline = (changes > threshold).sum()
        n_improve = (changes < -threshold).sum()
        n_stable = len(changes) - n_decline - n_improve

        print(f"\nClassification Threshold Analysis:")
        print(f"  Threshold (0.3 SD): {threshold:.3f}")
        print(f"  Tracts classified as DECLINE: {n_decline:,} ({n_decline/len(changes)*100:.1f}%)")
        print(f"  Tracts classified as IMPROVE: {n_improve:,} ({n_improve/len(changes)*100:.1f}%)")
        print(f"  Tracts classified as STABLE: {n_stable:,} ({n_stable/len(changes)*100:.1f}%)")

        # If threshold is less than measurement error, classifications are unreliable
        if threshold < measurement_std * np.sqrt(2):
            print(f"\n  WARNING: Classification threshold ({threshold:.2f}) is smaller than")
            print(f"  measurement error for change ({measurement_std * np.sqrt(2):.2f}).")
            print(f"  Many 'trajectory changes' may be measurement artifact.")

    return {
        'observed_std': observed_std,
        'measurement_std': measurement_std,
        'reliability': reliability,
        'snr': snr
    }


# =============================================================================
# 2. TEMPORAL SCALE ANALYSIS
# =============================================================================
def temporal_scale_analysis():
    """
    Test whether longer trajectories are more predictable.

    Hypothesis: If year-over-year changes are noisy, averaging over
    longer periods should improve signal-to-noise and predictability.
    """
    print("\n" + "=" * 70)
    print("2. TEMPORAL SCALE ANALYSIS")
    print("=" * 70)

    # Load trajectory panel to compute multi-year trajectories
    trajectory_path = DATA_DIR / "tract_trajectories.csv"

    if not trajectory_path.exists():
        print("Trajectory data not found. Using spatial dataset.")
        df = pd.read_csv(DATA_DIR / "prediction_dataset_spatial.csv")

        # We can still analyze what we have
        print("\nAnalyzing available temporal structure...")

        # Test: Does 2-year momentum predict better than 1-year?
        df_2024 = df[df['PredictionYear'] == 2024].dropna(subset=['target_change'])

        if 'CHBI_change_1yr' in df.columns and 'CHBI_change_2yr' in df.columns:
            # Correlation: does 2-year change correlate with outcome?
            corr_1yr = df_2024['CHBI_change_1yr'].corr(df_2024['target_change'])
            corr_2yr = df_2024['CHBI_change_2yr'].corr(df_2024['target_change'])

            print(f"\nPredictive Correlation with Future Change:")
            print(f"  1-year prior change (t-1): r = {corr_1yr:.4f}")
            print(f"  2-year prior change (t-2): r = {corr_2yr:.4f}")

            # Interpretation
            if abs(corr_1yr) > abs(corr_2yr):
                print(f"\n  Recent trajectory is more predictive than older trend")
            else:
                print(f"\n  Longer-term trend is more predictive than recent change")

        return None

    # Load full trajectory data
    traj = pd.read_csv(trajectory_path)
    print(f"Loaded trajectory data: {len(traj):,} rows")

    # Compute multi-year changes
    # TODO: Implement when trajectory data available

    return None


# =============================================================================
# 3. VARIANCE DECOMPOSITION
# =============================================================================
def variance_decomposition():
    """
    Decompose variance in CHBI change into:
    - Geographic (between-tract)
    - Temporal (between-year, within-tract)
    - Residual
    """
    print("\n" + "=" * 70)
    print("3. VARIANCE DECOMPOSITION")
    print("=" * 70)

    df = pd.read_csv(DATA_DIR / "prediction_dataset_spatial.csv")
    df = df.dropna(subset=['target_change'])

    print(f"Analyzing {len(df):,} tract-year observations")

    # Total variance
    total_var = df['target_change'].var()

    print(f"\nTotal variance in CHBI change: {total_var:.4f}")

    # Between-tract variance (do some tracts always change more than others?)
    tract_means = df.groupby('TractFIPS')['target_change'].mean()
    between_tract_var = tract_means.var()

    print(f"\nBetween-tract variance (tract mean differences): {between_tract_var:.4f}")
    print(f"  Fraction of total: {between_tract_var/total_var*100:.1f}%")

    # Between-year variance (are some years different?)
    year_means = df.groupby('PredictionYear')['target_change'].mean()
    print(f"\nYear means:")
    for year, mean in year_means.items():
        print(f"  {year}: {mean:.4f}")

    between_year_var = year_means.var()
    print(f"\nBetween-year variance: {between_year_var:.4f}")
    print(f"  Fraction of total: {between_year_var/total_var*100:.1f}%")

    # State-level variance
    if 'StateAbbr' in df.columns:
        state_means = df.groupby('StateAbbr')['target_change'].mean()
        between_state_var = state_means.var()

        print(f"\nBetween-state variance: {between_state_var:.4f}")
        print(f"  Fraction of total: {between_state_var/total_var*100:.1f}%")

        # Top/bottom states
        print(f"\nStates with most decline (highest CHBI increase):")
        for state in state_means.nlargest(5).index:
            print(f"  {state}: {state_means[state]:.4f}")

        print(f"\nStates with most improvement (lowest CHBI increase):")
        for state in state_means.nsmallest(5).index:
            print(f"  {state}: {state_means[state]:.4f}")

    # AR(1) Analysis: How much is explained by autocorrelation?
    print("\n" + "-" * 50)
    print("AUTOREGRESSIVE BASELINE")
    print("-" * 50)

    # For each tract, does prior CHBI predict current CHBI?
    if 'CHBI_prev' in df.columns and 'target_change' in df.columns:
        # Compute current CHBI = prev + change
        df['CHBI_current'] = df['CHBI_prev'] + df['target_change']

        # AR(1) model: CHBI_t = a + b*CHBI_{t-1} + e
        ar1 = LinearRegression()
        X = df['CHBI_prev'].values.reshape(-1, 1)
        y = df['CHBI_current'].values
        ar1.fit(X, y)

        r2_ar1 = ar1.score(X, y)

        print(f"\nAR(1) Model: CHBI(t) = {ar1.intercept_:.3f} + {ar1.coef_[0]:.3f} * CHBI(t-1)")
        print(f"R² (level prediction): {r2_ar1:.4f}")
        print(f"\nInterpretation:")
        print(f"  CHBI levels are {r2_ar1*100:.1f}% predictable from prior level")
        print(f"  (This is mostly 'persistence' - healthy tracts stay healthy)")

        # What about predicting CHANGE?
        lr_change = LinearRegression()
        lr_change.fit(X, df['target_change'].values)
        r2_change = lr_change.score(X, df['target_change'].values)

        print(f"\nPredicting CHANGE from prior level:")
        print(f"  R² = {r2_change:.4f}")
        print(f"  Prior level explains only {r2_change*100:.1f}% of change variance")

        # What about predicting change from prior CHANGE?
        if 'CHBI_change_1yr' in df.columns:
            df_with_prior_change = df.dropna(subset=['CHBI_change_1yr'])
            X_change = df_with_prior_change['CHBI_change_1yr'].values.reshape(-1, 1)
            y_change = df_with_prior_change['target_change'].values

            lr_change2 = LinearRegression()
            lr_change2.fit(X_change, y_change)
            r2_change2 = lr_change2.score(X_change, y_change)

            print(f"\nPredicting CHANGE from prior CHANGE:")
            print(f"  R² = {r2_change2:.4f}")
            print(f"  Beta = {lr_change2.coef_[0]:.3f}")

            if lr_change2.coef_[0] > 0:
                print(f"  Positive momentum: declining tracts continue declining")
            else:
                print(f"  Mean reversion: changes tend to reverse")

    return {
        'total_var': total_var,
        'between_tract_var': between_tract_var,
        'between_year_var': between_year_var
    }


# =============================================================================
# 4. TEST-RETEST RELIABILITY
# =============================================================================
def test_retest_reliability():
    """
    Compute reliability as correlation of change across adjacent year-pairs.

    If trajectories are stable, change(t-1,t) should correlate with change(t,t+1).
    If they're random, correlation should be near zero.
    """
    print("\n" + "=" * 70)
    print("4. TEST-RETEST RELIABILITY")
    print("=" * 70)

    df = pd.read_csv(DATA_DIR / "prediction_dataset_spatial.csv")

    # Get change by tract and year
    tract_year_changes = df.pivot_table(
        index='TractFIPS',
        columns='PredictionYear',
        values='target_change',
        aggfunc='first'
    )

    print(f"Tract-year matrix: {tract_year_changes.shape}")

    years = sorted(tract_year_changes.columns)
    print(f"Years available: {years}")

    # Compute year-over-year correlations
    print("\nYear-over-Year Change Correlations:")
    for i in range(len(years) - 1):
        y1, y2 = years[i], years[i+1]

        # Get tracts with data in both years
        valid = tract_year_changes[[y1, y2]].dropna()

        if len(valid) > 100:
            corr = valid[y1].corr(valid[y2])
            print(f"  Change({y1}) vs Change({y2}): r = {corr:.4f} (n={len(valid):,})")

    # Overall reliability estimate (average of adjacent correlations)
    correlations = []
    for i in range(len(years) - 1):
        y1, y2 = years[i], years[i+1]
        valid = tract_year_changes[[y1, y2]].dropna()
        if len(valid) > 100:
            correlations.append(valid[y1].corr(valid[y2]))

    if correlations:
        avg_corr = np.mean(correlations)
        print(f"\nAverage adjacent-year correlation: {avg_corr:.4f}")

        if avg_corr > 0.5:
            print("  Interpretation: MODERATE reliability - trajectories show persistence")
        elif avg_corr > 0.2:
            print("  Interpretation: WEAK reliability - some persistence but much noise")
        else:
            print("  Interpretation: POOR reliability - changes appear nearly random")

    return correlations


# =============================================================================
# 5. PREDICTION CEILING ANALYSIS
# =============================================================================
def prediction_ceiling():
    """
    What is the theoretical maximum predictive performance?

    Given measurement noise, even a perfect model has limits.
    """
    print("\n" + "=" * 70)
    print("5. PREDICTION CEILING ANALYSIS")
    print("=" * 70)

    # Key parameters from earlier analyses
    measurement_std = 1.0  # Estimated measurement error in CHBI

    df = pd.read_csv(DATA_DIR / "prediction_dataset_spatial.csv")
    df_2024 = df[df['PredictionYear'] == 2024].dropna(subset=['target_change'])

    observed_std = df_2024['target_change'].std()

    # Reliability coefficient
    measurement_var = 2 * (measurement_std ** 2)  # For change score
    observed_var = observed_std ** 2
    reliability = max(0, 1 - measurement_var / observed_var)

    print(f"\nMeasurement Error Framework:")
    print(f"  Observed change std: {observed_std:.3f}")
    print(f"  Assumed measurement std (each timepoint): {measurement_std:.3f}")
    print(f"  Change score measurement std: {np.sqrt(measurement_var):.3f}")
    print(f"  Reliability: {reliability:.3f}")

    # Maximum achievable metrics
    max_r2 = reliability  # R² ceiling

    # For classification, it's more complex
    # Simulate: if we had perfect knowledge of true values
    print(f"\nTheoretical Ceilings:")
    print(f"  Maximum R² for continuous prediction: {max_r2:.3f}")
    print(f"  Our achieved R²: 0.093")
    print(f"  Gap (unexplained true variance): {max_r2 - 0.093:.3f}")

    # Classification simulation
    threshold = 0.3 * observed_std

    # True classification (if we knew true values)
    # Assume observed = true + noise, simulate
    np.random.seed(42)
    n_sims = 1000

    observed_changes = df_2024['target_change'].values
    n = len(observed_changes)

    classification_accuracy_sims = []
    for _ in range(n_sims):
        # Generate "true" values by removing estimated noise
        noise_realization = np.random.normal(0, np.sqrt(measurement_var), n)
        estimated_true = observed_changes - noise_realization

        # Classify both
        observed_class = np.where(observed_changes > threshold, 'DECLINE',
                         np.where(observed_changes < -threshold, 'IMPROVE', 'STABLE'))
        true_class = np.where(estimated_true > threshold, 'DECLINE',
                     np.where(estimated_true < -threshold, 'IMPROVE', 'STABLE'))

        # Agreement
        agreement = (observed_class == true_class).mean()
        classification_accuracy_sims.append(agreement)

    mean_agreement = np.mean(classification_accuracy_sims)

    print(f"\nClassification Reliability Simulation:")
    print(f"  Probability that observed class = true class: {mean_agreement:.3f}")
    print(f"  Even with PERFECT predictors, misclassification due to noise: {1-mean_agreement:.3f}")

    # F1 ceiling (rough estimate)
    # If baseline accuracy is ~50% due to noise, F1 ceiling is similar
    print(f"\nImplication:")
    print(f"  Observed F1: 0.26")
    print(f"  If ~{(1-mean_agreement)*100:.0f}% of classifications are 'wrong' due to noise,")
    print(f"  the ceiling on F1 may be around {mean_agreement * 0.6:.2f}")  # Rough heuristic

    return {
        'max_r2': max_r2,
        'classification_reliability': mean_agreement
    }


# =============================================================================
# 6. SUMMARY AND IMPLICATIONS
# =============================================================================
def summarize_findings():
    """
    Synthesize all findings into paper-ready summary.
    """
    print("\n" + "=" * 70)
    print("6. SUMMARY: WHY TRAJECTORIES ARE UNPREDICTABLE")
    print("=" * 70)

    print("""
FINDING 1: STRONG MEAN REVERSION IN HEALTH TRAJECTORIES
  - Adjacent year correlation of changes: r = -0.40 to -0.58
  - Tracts that improved one year tend to decline the next
  - Beta = -0.40: A 1-unit improvement is followed by 0.4 decline
  - RESULT: "Momentum" predicts the OPPOSITE of future change
  - IMPLICATION: Improving tracts are not on stable upward paths

FINDING 2: LEVELS ARE HIGHLY PERSISTENT, CHANGES ARE NOT
  - CHBI levels: R² = 99.7% (healthy tracts stay healthy)
  - CHBI changes: R² = 9.3% from prior change (weak, reversed sign)
  - RESULT: Level matters, trajectory direction doesn't persist
  - IMPLICATION: Focus on current burden, not trajectory class

FINDING 3: GEOGRAPHY EXPLAINS MEANINGFUL VARIANCE
  - Between-tract differences: 28% of variance
  - Between-state differences: 4% of variance
  - Between-year differences: <1% of variance
  - RESULT: Some tracts are consistently more volatile than others
  - IMPLICATION: Geographic context matters for change magnitude

FINDING 4: CLASSIFICATION THRESHOLDS ARE ARBITRARY
  - Threshold (0.3 SD): 0.11 CHBI units
  - ~40% classified as DECLINE, ~33% IMPROVE, ~28% STABLE
  - With mean reversion, DECLINE→IMPROVE and vice versa is common
  - RESULT: Trajectory "class" is unstable year-over-year
  - IMPLICATION: Don't label communities by trajectory class

OVERALL CONCLUSION:
  The F1 = 0.26 performance reflects fundamental dynamics:
  1. Community health CHANGES exhibit MEAN REVERSION
  2. This makes trajectory class inherently unstable
  3. "Momentum" features predict the WRONG direction
  4. Level persistence is high, but change direction is low

  Community health trajectories are MEAN REVERTING:
  - Short-term fluctuations cancel out
  - Communities oscillate around stable equilibria
  - True "trajectories" may require 5+ year windows

POLICY IMPLICATIONS:
  1. Don't label communities as "improving" or "declining"
     - These labels are unstable year-to-year
  2. Focus on CURRENT BURDEN LEVELS
     - Levels are stable and actionable
  3. Use MULTI-YEAR moving averages for trend assessment
     - Single-year changes are dominated by reversion
  4. Target persistent high-burden tracts, not "declining" ones
     - High burden today = high burden tomorrow (R² = 99.7%)
  5. Build responsive systems, not predictive ones
     - React to change as it happens, don't try to predict
""")


# =============================================================================
# MAIN
# =============================================================================
def main():
    results = {}

    results['measurement'] = measurement_error_analysis()
    results['temporal'] = temporal_scale_analysis()
    results['variance'] = variance_decomposition()
    results['reliability'] = test_retest_reliability()
    results['ceiling'] = prediction_ceiling()

    summarize_findings()

    return results


if __name__ == '__main__':
    results = main()
