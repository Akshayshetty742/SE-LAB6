"""
Lab 6: Code Coverage Analysis
SRN: PES1UG24AM026
Test Suite: CodeCoverageTest_PES1UG24AM026_application.py

This test suite focuses on code (statement) coverage for loan_eligibility.py.
It systematically covers normal cases, boundary values, decision outcomes,
and invalid-input error handling to achieve >= 90% (targeting 100%) code coverage.
"""

import os
import sys
import pytest

# Ensure module path resolution works from any working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loan_eligibility import credit_band, is_eligible, interest_rate


# =====================================================================
# Tests for credit_band(score)
# =====================================================================

def test_credit_band_invalid_low():
    """Verify invalid score below lower bound (< 300) raises ValueError."""
    with pytest.raises(ValueError, match="invalid score"):
        credit_band(299)
    with pytest.raises(ValueError, match="invalid score"):
        credit_band(100)


def test_credit_band_invalid_high():
    """Verify invalid score above upper bound (> 900) raises ValueError."""
    with pytest.raises(ValueError, match="invalid score"):
        credit_band(901)
    with pytest.raises(ValueError, match="invalid score"):
        credit_band(1200)


def test_credit_band_excellent():
    """Verify score >= 750 maps to 'excellent' band (including boundaries)."""
    assert credit_band(750) == "excellent"
    assert credit_band(800) == "excellent"
    assert credit_band(900) == "excellent"


def test_credit_band_good():
    """Verify score in [650, 749] maps to 'good' band (including boundaries)."""
    assert credit_band(650) == "good"
    assert credit_band(700) == "good"
    assert credit_band(749) == "good"


def test_credit_band_fair():
    """Verify score in [550, 649] maps to 'fair' band (including boundaries)."""
    assert credit_band(550) == "fair"
    assert credit_band(600) == "fair"
    assert credit_band(649) == "fair"


def test_credit_band_poor():
    """Verify score in [300, 549] maps to 'poor' band (including boundaries)."""
    assert credit_band(300) == "poor"
    assert credit_band(450) == "poor"
    assert credit_band(549) == "poor"


# =====================================================================
# Tests for is_eligible(age, income, employment, score)
# =====================================================================

def test_is_eligible_invalid_employment():
    """Verify unknown employment type raises ValueError."""
    with pytest.raises(ValueError, match="unknown employment"):
        is_eligible(30, 50000, "contractor", 750)
    with pytest.raises(ValueError, match="unknown employment"):
        is_eligible(25, 30000, "unemployed", 700)


def test_is_eligible_age_under_21():
    """Verify applicant below minimum age (< 21) is ineligible."""
    assert is_eligible(20, 50000, "salaried", 750) is False
    assert is_eligible(18, 60000, "self_employed", 800) is False


def test_is_eligible_age_over_60():
    """Verify applicant above maximum age (> 60) is ineligible."""
    assert is_eligible(61, 50000, "salaried", 750) is False
    assert is_eligible(70, 80000, "self_employed", 850) is False


def test_is_eligible_salaried_below_min_income():
    """Verify salaried applicant with income < 25000 is ineligible."""
    assert is_eligible(30, 24999, "salaried", 750) is False
    assert is_eligible(35, 15000, "salaried", 800) is False


def test_is_eligible_self_employed_below_min_income():
    """Verify self-employed applicant with income < 40000 is ineligible."""
    assert is_eligible(30, 39999, "self_employed", 750) is False
    assert is_eligible(40, 25000, "self_employed", 800) is False


def test_is_eligible_poor_credit():
    """Verify applicant with 'poor' credit band (< 550) is ineligible."""
    assert is_eligible(30, 50000, "salaried", 549) is False
    assert is_eligible(35, 60000, "self_employed", 400) is False


def test_is_eligible_valid_salaried_applicant():
    """Verify valid salaried applicant satisfies all criteria."""
    assert is_eligible(25, 30000, "salaried", 700) is True


def test_is_eligible_valid_self_employed_applicant():
    """Verify valid self-employed applicant satisfies all criteria."""
    assert is_eligible(40, 55000, "self_employed", 600) is True


def test_is_eligible_boundary_ages():
    """Verify boundary ages 21 and 60 are eligible."""
    assert is_eligible(21, 25000, "salaried", 750) is True
    assert is_eligible(60, 40000, "self_employed", 750) is True


def test_is_eligible_boundary_income():
    """Verify exact minimum incomes (25000 for salaried, 40000 for self_employed) are eligible."""
    assert is_eligible(30, 25000, "salaried", 650) is True
    assert is_eligible(30, 40000, "self_employed", 650) is True


# =====================================================================
# Tests for interest_rate(score, employment, has_collateral)
# =====================================================================

def test_interest_rate_excellent_salaried_no_collateral():
    """Base rate 8, salaried (+0), no collateral (-0) => 8%."""
    assert interest_rate(800, "salaried", False) == 8


def test_interest_rate_excellent_self_employed_collateral():
    """Base rate 8, self-employed (+1), collateral (-2) => 7%."""
    assert interest_rate(750, "self_employed", True) == 7


def test_interest_rate_good_salaried_collateral():
    """Base rate 10, salaried (+0), collateral (-2) => 8%."""
    assert interest_rate(700, "salaried", True) == 8


def test_interest_rate_good_self_employed_no_collateral():
    """Base rate 10, self-employed (+1), no collateral (-0) => 11%."""
    assert interest_rate(650, "self_employed", False) == 11


def test_interest_rate_fair_salaried_no_collateral():
    """Base rate 13, salaried (+0), no collateral (-0) => 13%."""
    assert interest_rate(600, "salaried", False) == 13


def test_interest_rate_poor_self_employed_collateral():
    """Base rate 13, self-employed (+1), collateral (-2) => 12%."""
    assert interest_rate(400, "self_employed", True) == 12
