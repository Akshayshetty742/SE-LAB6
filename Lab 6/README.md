# L6_L7_26_loan_eligibility — Loan Eligibility

Lab 6: Code and Branch Coverage Analysis  
**Student SRN:** `PES1UG24AM026`

## About

A Python module that maps credit scores to bands, checks loan eligibility by age, income, and employment, and computes interest rates with employment and collateral modifiers.

## Files

| File | Description |
|------|-------------|
| `loan_eligibility.py` | The module under test |
| `test_loan_eligibility.py` | Starter baseline test file |
| `CodeCoverageTest_PES1UG24AM026_application.py` | Comprehensive code (statement) coverage suite (>= 90%, achieved 100%) |
| `BranchCoverageTest_PES1UG24AM026_application.py` | Comprehensive branch coverage suite (>= 90%, achieved 100%) |
| `pytest.ini` | Pytest configuration for test discovery |
| `screenshots/lab6/` | Directory containing terminal coverage report screenshots |

## Execution & Verification Commands

### 1. Code Coverage (Statement Coverage)
Run pytest with coverage against `loan_eligibility.py`:
```powershell
python -m coverage erase
python -m coverage run --source=loan_eligibility -m pytest CodeCoverageTest_PES1UG24AM026_application.py
python -m coverage report -m
```

### 2. Branch Coverage
Run pytest with branch coverage against `loan_eligibility.py`:
```powershell
python -m coverage erase
python -m coverage run --branch --source=loan_eligibility -m pytest BranchCoverageTest_PES1UG24AM026_application.py
python -m coverage report -m
```

### 3. Run All Test Suites
```powershell
python -m pytest
```

## Coverage Summary

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| **Statement Coverage** | >= 90% | **100%** (33/33 statements) | Pass |
| **Branch Coverage** | >= 90% | **100%** (24/24 branches) | Pass |
