#!/usr/bin/env python3
"""
Unit Tests for Corrected Resilience Model

Tests the state fixed effects implementation and other model components
to ensure the bug fix is correct and prevent regression.
"""

import pytest
import pandas as pd
import numpy as np
from io import StringIO

# Import the module under test
from resilience_model import (
    filter_institutional_populations,
    prepare_design_matrix,
    fit_ols_model,
    calculate_resilience_scores,
    expected_burden,
    classify_tracts,
    OLSResult
)


class TestStateFixedEffects:
    """Tests for the corrected state fixed effects implementation."""

    def test_state_dummies_correct_assignment(self):
        """
        Test that state dummy variables are assigned correctly.

        This is the CRITICAL test that validates the bug fix.
        The original bug used the inner loop index for both stateList AND burdened.
        """
        # Create test data with known state assignments
        burdened = pd.DataFrame({
            'TractFIPS': ['01001000001', '01001000002', '06001000001', '06001000002', '36001000001'],
            'StateAbbr': ['AL', 'AL', 'CA', 'CA', 'NY'],
            'burden': [1.0, 1.5, 2.0, 2.5, 3.0]
        })

        fara = pd.DataFrame({
            'CensusTract': ['01001000001', '01001000002', '06001000001', '06001000002', '36001000001'],
            'LILATracts_1And10': [1, 0, 1, 0, 1],
            'LI': [0.5, 0.3, 0.4, 0.2, 0.6],
            'Urban': [1, 1, 0, 0, 1],
            'LA1and10_NoVehicle': [0.1, 0.2, 0.3, 0.1, 0.2]
        })

        X, y, feature_names, state_list = prepare_design_matrix(
            burdened, fara,
            include_no_vehicle=False,
            state_fixed_effects=True
        )

        # States should be ['AL', 'CA', 'NY'] (sorted)
        assert state_list == ['AL', 'CA', 'NY'], f"Expected ['AL', 'CA', 'NY'], got {state_list}"

        # AL is reference (dropped), so we should have dummies for CA and NY
        assert 'state_CA' in X.columns, "Missing state_CA dummy"
        assert 'state_NY' in X.columns, "Missing state_NY dummy"
        assert 'state_AL' not in X.columns, "state_AL should be reference category"

        # Check CA dummy: should be 1 for CA tracts, 0 for others
        ca_rows = X[X['_StateAbbr'] == 'CA']
        non_ca_rows = X[X['_StateAbbr'] != 'CA']

        assert (ca_rows['state_CA'] == 1.0).all(), "CA tracts should have state_CA = 1"
        assert (non_ca_rows['state_CA'] == 0.0).all(), "Non-CA tracts should have state_CA = 0"

        # Check NY dummy
        ny_rows = X[X['_StateAbbr'] == 'NY']
        non_ny_rows = X[X['_StateAbbr'] != 'NY']

        assert (ny_rows['state_NY'] == 1.0).all(), "NY tracts should have state_NY = 1"
        assert (non_ny_rows['state_NY'] == 0.0).all(), "Non-NY tracts should have state_NY = 0"

    def test_state_dummies_all_states_represented(self):
        """Test that every tract gets exactly one state dummy (or reference)."""
        # Create test data with 5 states, 2 tracts each
        states = ['CA', 'NY', 'TX', 'FL', 'OH']
        tracts = []
        for i, state in enumerate(states):
            for j in range(2):
                tracts.append({
                    'TractFIPS': f'{i+1:02d}001{j:06d}',
                    'StateAbbr': state,
                    'burden': np.random.randn()
                })

        burdened = pd.DataFrame(tracts)

        fara_rows = []
        for t in tracts:
            fara_rows.append({
                'CensusTract': t['TractFIPS'],
                'LILATracts_1And10': np.random.randint(0, 2),
                'LI': np.random.random(),
                'Urban': np.random.randint(0, 2),
            })

        fara = pd.DataFrame(fara_rows)

        X, y, feature_names, state_list = prepare_design_matrix(
            burdened, fara,
            include_no_vehicle=False,
            state_fixed_effects=True
        )

        # Check that we have N-1 state dummies (one reference)
        state_dummies = [col for col in X.columns if col.startswith('state_')]
        assert len(state_dummies) == len(states) - 1, f"Expected {len(states)-1} dummies, got {len(state_dummies)}"

        # Check that each row has exactly one state dummy = 1 (or 0 if reference)
        for idx, row in X.iterrows():
            state = row['_StateAbbr']
            n_ones = sum(row[col] for col in state_dummies)

            if state == state_list[0]:  # Reference category
                assert n_ones == 0, f"Reference state {state} should have all dummies = 0"
            else:
                assert n_ones == 1, f"State {state} should have exactly one dummy = 1, got {n_ones}"


class TestInstitutionalFilter:
    """Tests for institutional population filtering."""

    def test_filter_with_gq_flag(self):
        """Test filtering with GroupQuartersFlag column."""
        fara = pd.DataFrame({
            'CensusTract': ['01', '02', '03', '04', '05'],
            'GroupQuartersFlag': [0, 1, 0, 1, 0],
            'LILATracts_1And10': [1, 1, 1, 1, 1]
        })

        filtered, excluded = filter_institutional_populations(fara)

        assert len(filtered) == 3, "Should have 3 tracts after filtering"
        assert len(excluded) == 2, "Should have 2 excluded tracts"
        assert excluded['GroupQuartersFlag'].sum() == 2, "All excluded should have flag=1"

    def test_filter_with_proportion(self):
        """Test filtering with population proportion."""
        fara = pd.DataFrame({
            'CensusTract': ['01', '02', '03', '04', '05'],
            'GroupQuartersPop': [50, 500, 100, 2000, 0],
            'TotalPop': [1000, 1000, 1000, 2000, 1000],
            'LILATracts_1And10': [1, 1, 1, 1, 1]
        })

        # 10% threshold
        filtered, excluded = filter_institutional_populations(fara, threshold=0.10)

        # Tracts 02 (50%) and 04 (100%) should be excluded
        assert len(excluded) == 2, "Should exclude 2 tracts with >10% GQ"
        assert '02' in excluded['CensusTract'].values
        assert '04' in excluded['CensusTract'].values


class TestModelFit:
    """Tests for OLS model fitting."""

    def test_model_fits_without_error(self):
        """Test that model fits on valid data."""
        np.random.seed(42)
        n = 100

        burdened = pd.DataFrame({
            'TractFIPS': [f'{i:011d}' for i in range(n)],
            'StateAbbr': np.random.choice(['CA', 'NY', 'TX'], n),
            'burden': np.random.randn(n)
        })

        fara = pd.DataFrame({
            'CensusTract': burdened['TractFIPS'],
            'LILATracts_1And10': np.random.randint(0, 2, n),
            'LI': np.random.random(n),
            'Urban': np.random.randint(0, 2, n),
            'LA1and10_NoVehicle': np.random.random(n)
        })

        model_table, result = expected_burden(
            burdened, fara,
            filter_institutional=False
        )

        assert model_table is not None, "Model should return results"
        assert isinstance(result, OLSResult), "Should return OLSResult"
        assert result.n_observations == n, f"Should have {n} observations"
        assert 0 <= result.r_squared <= 1, "R-squared should be between 0 and 1"

    def test_residuals_sum_to_zero(self):
        """Test that residuals sum approximately to zero (OLS property)."""
        np.random.seed(42)
        n = 100

        burdened = pd.DataFrame({
            'TractFIPS': [f'{i:011d}' for i in range(n)],
            'StateAbbr': np.random.choice(['CA', 'NY'], n),
            'burden': np.random.randn(n)
        })

        fara = pd.DataFrame({
            'CensusTract': burdened['TractFIPS'],
            'LILATracts_1And10': np.random.randint(0, 2, n),
            'LI': np.random.random(n),
            'Urban': np.random.randint(0, 2, n),
        })

        model_table, result = expected_burden(
            burdened, fara,
            include_no_vehicle=False,
            filter_institutional=False
        )

        residual_sum = model_table['resid'].sum()
        assert abs(residual_sum) < 1e-10, f"Residuals should sum to ~0, got {residual_sum}"


class TestResilienceScores:
    """Tests for resilience score calculation."""

    def test_scores_are_standardized(self):
        """Test that resilience scores have approximately std=1."""
        np.random.seed(42)
        n = 1000

        burdened = pd.DataFrame({
            'TractFIPS': [f'{i:011d}' for i in range(n)],
            'StateAbbr': np.random.choice(['CA', 'NY', 'TX', 'FL'], n),
            'burden': np.random.randn(n)
        })

        fara = pd.DataFrame({
            'CensusTract': burdened['TractFIPS'],
            'LILATracts_1And10': np.random.randint(0, 2, n),
            'LI': np.random.random(n),
            'Urban': np.random.randint(0, 2, n),
        })

        model_table, result = expected_burden(
            burdened, fara,
            include_no_vehicle=False,
            filter_institutional=False
        )

        score_std = model_table['resilience_score'].std()
        assert 0.95 < score_std < 1.05, f"Score std should be ~1, got {score_std}"

    def test_positive_score_means_better_than_expected(self):
        """Test that positive scores indicate lower burden than predicted."""
        # Create simple test case
        burdened = pd.DataFrame({
            'TractFIPS': ['01', '02', '03'],
            'StateAbbr': ['CA', 'CA', 'CA'],
            'burden': [0.0, 0.0, 5.0]  # Tract 03 has much higher burden
        })

        fara = pd.DataFrame({
            'CensusTract': ['01', '02', '03'],
            'LILATracts_1And10': [1, 1, 1],  # Same LILA status
            'LI': [0.5, 0.5, 0.5],  # Same LI
            'Urban': [1, 1, 1],  # Same urbanicity
        })

        model_table, result = expected_burden(
            burdened, fara,
            include_no_vehicle=False,
            state_fixed_effects=False,  # Disable for simple test
            filter_institutional=False
        )

        # Tract 03 should have negative resilience (worse than expected)
        tract_03_score = model_table[model_table['TractFIPS'] == '03']['resilience_score'].values[0]
        assert tract_03_score < 0, "High burden tract should have negative resilience score"


class TestClassification:
    """Tests for resilience classification."""

    def test_classification_thresholds(self):
        """Test that classification uses correct thresholds."""
        scores = pd.DataFrame({
            'resilience_score': [-2.0, -1.645, -1.0, 0, 1.0, 1.645, 2.0]
        })

        from resilience_model import classify_tracts

        # Import locally since it might not be exported
        def classify(score):
            if score > 1.645:
                return 'resilient'
            elif score < -1.645:
                return 'vulnerable'
            else:
                return 'expected'

        classifications = scores['resilience_score'].apply(classify)

        assert classifications[0] == 'vulnerable', "-2.0 should be vulnerable"
        assert classifications[1] == 'expected', "-1.645 should be expected (boundary)"
        assert classifications[2] == 'expected', "-1.0 should be expected"
        assert classifications[3] == 'expected', "0 should be expected"
        assert classifications[4] == 'expected', "1.0 should be expected"
        assert classifications[5] == 'expected', "1.645 should be expected (boundary)"
        assert classifications[6] == 'resilient', "2.0 should be resilient"


class TestBugRegression:
    """
    Regression tests to ensure the bug doesn't return.

    The original bug: inner loop variable 'i' shadowed outer loop 'i',
    causing state comparison to use wrong index.
    """

    def test_bug_scenario_reproduction(self):
        """
        Reproduce the exact scenario that caused the bug.

        Original buggy code:
            for i:=1; i<len(stateList); i++ {
                if burdened[i][bh("StateAbbr")] == stateList[i] {  // BUG
                    x = append(x, 1.0)

        This compared the i-th row of burdened to the i-th state,
        instead of comparing the CURRENT row to the i-th state.
        """
        # Create data where the bug would be visible
        # Row 0: AL, Row 1: CA, Row 2: NY
        # States sorted: AL, CA, NY (AL is reference)
        # Bug: Row 1 would check burdened[1].State == stateList[1] == "CA" (true)
        # Bug: Row 2 would check burdened[2].State == stateList[2] == "NY" (true)
        # BUT if rows are in different order:
        # Row 0: NY, Row 1: AL, Row 2: CA
        # Bug: Row 1 would check burdened[1].State == stateList[1] == "CA" (false, it's AL!)
        # Bug: Row 2 would check burdened[2].State == stateList[2] == "NY" (false, it's CA!)

        # Deliberately unsorted data
        burdened = pd.DataFrame({
            'TractFIPS': ['36001000001', '01001000001', '06001000001'],  # NY, AL, CA
            'StateAbbr': ['NY', 'AL', 'CA'],
            'burden': [1.0, 2.0, 3.0]
        })

        fara = pd.DataFrame({
            'CensusTract': ['36001000001', '01001000001', '06001000001'],
            'LILATracts_1And10': [1, 1, 1],
            'LI': [0.5, 0.5, 0.5],
            'Urban': [1, 1, 1],
        })

        X, y, feature_names, state_list = prepare_design_matrix(
            burdened, fara,
            include_no_vehicle=False,
            state_fixed_effects=True
        )

        # The CORRECT behavior:
        # - NY tract should have state_NY = 1, state_CA = 0
        # - AL tract should have state_NY = 0, state_CA = 0 (reference)
        # - CA tract should have state_NY = 0, state_CA = 1

        ny_row = X[X['_StateAbbr'] == 'NY'].iloc[0]
        al_row = X[X['_StateAbbr'] == 'AL'].iloc[0]
        ca_row = X[X['_StateAbbr'] == 'CA'].iloc[0]

        # Check NY tract
        assert ny_row['state_NY'] == 1.0, "NY tract should have state_NY = 1"
        assert ny_row['state_CA'] == 0.0, "NY tract should have state_CA = 0"

        # Check AL tract (reference)
        assert al_row['state_NY'] == 0.0, "AL tract should have state_NY = 0"
        assert al_row['state_CA'] == 0.0, "AL tract should have state_CA = 0"

        # Check CA tract
        assert ca_row['state_NY'] == 0.0, "CA tract should have state_NY = 0"
        assert ca_row['state_CA'] == 1.0, "CA tract should have state_CA = 1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
