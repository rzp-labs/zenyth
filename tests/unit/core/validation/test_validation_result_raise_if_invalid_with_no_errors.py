"""Test raise_if_invalid does nothing when valid.

This test validates that ValidationResult.raise_if_invalid() does not raise
any exception when the result contains no validation errors.
"""

import pytest

from zenyth.core.validation import ValidationResult


def test_validation_result_raise_if_invalid_with_no_errors() -> None:
    """Test raise_if_invalid does nothing when valid.

    Validates that no exception is raised for valid results.

    SOLID Assessment:
    - SRP: Test focused solely on valid result handling
    - DIP: Exception handling independent of specific error types
    """
    result = ValidationResult()

    # Should not raise when valid
    try:
        result.raise_if_invalid()
    except Exception:
        pytest.fail("Should not raise exception for valid result")
