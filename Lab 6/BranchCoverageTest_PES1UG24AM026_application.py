"""
Lab 6: Branch Coverage Analysis
SRN: PES1UG24AM026
Test Suite: BranchCoverageTest_PES1UG24AM026_application.py

This test suite focuses on branch coverage for loan_eligibility.py.
It systematically evaluates:
  1. Both True and False outcomes for all conditional decisions.
  2. Individual branch conditions in compound boolean predicates (e.g., OR operators).
  3. All if-elif-else execution paths.
  4. Both outcomes for optional modifiers (employment type and collateral presence).
Targeting >= 90% (achieving 100%) branch coverage.
"""

import os
import sys
import pytest

# Ensure module path resolution works from any working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loan_eligibility import credit_band, is_eligible, interest_rate


# =====================================================================
# Branch Tests for credit_band(score)
# Decision 1: if score < 300 or score > 900
# Decision 2: if score >= 750
# Decision 3: elif score >= 650
# Decision 4: elif score >= 550
# Fall-through: return "poor"
# =====================================================================

def test_branch_credit_band_score_below_300_true():
    """Branch 1: score < 300 evaluates to True -> raises ValueError."""
    with pytest.raises(ValueError, match="invalid score"):
        credit_band(250)


def test_branch_credit_band_score_above_900_true():
    """Branch 1: score < 300 is False, score > 900 is True -> raises ValueError."""
    with pytest.raises(ValueError, match="invalid score"):
        credit_band(950)


def test_branch_credit_band_score_valid_range_false():
    """Branch 1: both conditions False (valid range [300, 900]) -> proceeds."""
    # Verified by downstream valid returns
    assert credit_band(750) == "excellent"


def test_branch_credit_band_excellent_true():
    """Branch 2: score >= 750 evaluates to True -> returns 'excellent'."""
    assert credit_band(750) == "excellent"
    assert credit_band(850) == "excellent"


def test_branch_credit_band_excellent_false_good_true():
    """Branch 2 False, Branch 3 True: score < 750 and score >= 650 -> returns 'good'."""
    assert credit_band(650) == "good"
    assert credit_band(720) == "good"


def test_branch_credit_band_good_false_fair_true():
    """Branch 3 False, Branch 4 True: score < 650 and score >= 550 -> returns 'fair'."""
    assert credit_band(550) == "fair"
    assert credit_band(600) == "fair"


def test_branch_credit_band_fair_false_poor():
    """Branch 4 False: score < 550 (down to 300) -> returns 'poor'."""
    assert credit_band(300) == "poor"
    assert credit_band(500) == "poor"


# =====================================================================
# Branch Tests for is_eligible(age, income, employment, score)
# Decision 5: if employment not in MIN_INCOME
# Decision 6: if age < 21 or age > 60
# Decision 7: if income < MIN_INCOME[employment]
# Decision 8: if credit_band(score) == "poor"
# Fall-through: return True
# =====================================================================

def test_branch_is_eligible_unknown_employment_true():
    """Branch 5: employment not in MIN_INCOME is True -> raises ValueError."""
    with pytest.raises(ValueError, match="unknown employment"):
        is_eligible(30, 50000, "freelancer", 750)


def test_branch_is_eligible_known_employment_false():
    """Branch 5: employment not in MIN_INCOME is False -> proceeds."""
    assert is_eligible(30, 50000, "salaried", 750) is True


def test_branch_is_eligible_age_under_21_true():
    """Branch 6: age < 21 is True -> returns False."""
    assert is_eligible(20, 50000, "salaried", 750) is False


def test_branch_is_eligible_age_over_60_true():
    """Branch 6: age < 21 is False, age > 60 is True -> returns False."""
    assert is_eligible(61, 50000, "salaried", 750) is False


def test_branch_is_eligible_age_in_range_false():
    """Branch 6: both age < 21 and age > 60 are False -> proceeds."""
    assert is_eligible(21, 50000, "salaried", 750) is True
    assert is_eligible(60, 50000, "salaried", 750) is True


def test_branch_is_eligible_salaried_income_below_min_true():
    """Branch 7: salaried income < 25000 is True -> returns False."""
    assert is_eligible(30, 20000, "salaried", 750) is False


def test_branch_is_eligible_salaried_income_meets_min_false():
    """Branch 7: salaried income < 25000 is False (income >= 25000) -> proceeds."""
    assert is_eligible(30, 25000, "salaried", 750) is True


def test_branch_is_eligible_self_employed_income_below_min_true():
    """Branch 7: self_employed income < 40000 is True -> returns False."""
    assert is_eligible(35, 35000, "self_employed", 750) is False


def test_branch_is_eligible_self_employed_income_meets_min_false():
    """Branch 7: self_employed income < 40000 is False (income >= 40000) -> proceeds."""
    assert is_eligible(35, 40000, "self_employed", 750) is True


def test_branch_is_eligible_credit_poor_true():
    """Branch 8: credit_band(score) == 'poor' is True -> returns False."""
    assert is_eligible(30, 50000, "salaried", 450) is False


def test_branch_is_eligible_credit_not_poor_false():
    """Branch 8: credit_band(score) == 'poor' is False -> returns True."""
    assert is_eligible(30, 50000, "salaried", 550) is True   # fair
    assert is_eligible(30, 50000, "salaried", 650) is True   # good
    assert is_eligible(30, 50000, "salaried", 800) is True   # excellent


# =====================================================================
# Branch Tests for interest_rate(score, employment, has_collateral)
# Decision 9: if band == "excellent"
# Decision 10: elif band == "good"
# Else: rate = 13
# Decision 11: if employment == "self_employed" (True / False)
# Decision 12: if has_collateral (True / False)
# =====================================================================

def test_branch_interest_rate_band_excellent_all_combinations():
    """
    Branch 9 True (band == 'excellent', base rate 8).
    Tests all 4 sub-branch combinations of (self_employed, has_collateral):
      - salaried + no collateral:     8 + 0 - 0 = 8
      - salaried + collateral:        8 + 0 - 2 = 6
      - self_employed + no collateral:8 + 1 - 0 = 9
      - self_employed + collateral:   8 + 1 - 2 = 7
    """
    assert interest_rate(800, "salaried", False) == 8
    assert interest_rate(800, "salaried", True) == 6
    assert interest_rate(800, "self_employed", False) == 9
    assert interest_rate(800, "self_employed", True) == 7


def test_branch_interest_rate_band_good_all_combinations():
    """
    Branch 9 False, Branch 10 True (band == 'good', base rate 10).
    Tests all 4 sub-branch combinations:
      - salaried + no collateral:     10 + 0 - 0 = 10
      - salaried + collateral:        10 + 0 - 2 = 8
      - self_employed + no collateral:10 + 1 - 0 = 11
      - self_employed + collateral:   10 + 1 - 2 = 9
    """
    assert interest_rate(700, "salaried", False) == 10
    assert interest_rate(700, "salaried", True) == 8
    assert interest_rate(700, "self_employed", False) == 11
    assert interest_rate(700, "self_employed", True) == 9


def test_branch_interest_rate_band_other_all_combinations():
    """
    Branch 9 False, Branch 10 False -> Else (base rate 13).
    Tests fair and poor bands across modifier branches:
      - fair + salaried + no collateral:     13 + 0 - 0 = 13
      - fair + self_employed + collateral:   13 + 1 - 2 = 12
      - poor + salaried + collateral:        13 + 0 - 2 = 11
      - poor + self_employed + no collateral:13 + 1 - 0 = 14
    """
    assert interest_rate(600, "salaried", False) == 13
    assert interest_rate(600, "self_employed", True) == 12
    assert interest_rate(450, "salaried", True) == 11
    assert interest_rate(450, "self_employed", False) == 14
