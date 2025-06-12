"""Test ValidationResult with multiple validation errors.

This test validates that ValidationResult can properly accumulate multiple
errors without interference, maintaining order and correctness for each error.
"""

from zenyth.core.validation import ErrorCode, ValidationResult


def test_validation_result_multiple_errors() -> None:
    """Test ValidationResult with multiple validation errors.

    Validates proper error accumulation without interference.

    SOLID Assessment:
    - SRP: Test focused solely on multiple error collection
    - OCP: Error collection extensible to any number of errors
    """
    result = ValidationResult()
    result.add_error("username", ErrorCode.REQUIRED)
    result.add_error("email", ErrorCode.INVALID_FORMAT)
    result.add_error("password", ErrorCode.TOO_SHORT)

    # Should collect all errors
    assert len(result.errors) == 3
    assert result.is_valid() is False

    # Should maintain error order
    assert result.errors[0].field == "username"
    assert result.errors[1].field == "email"
    assert result.errors[2].field == "password"
