"""Test validate_max_length with string exceeding maximum length.

This test validates that the Validator.validate_max_length method correctly
identifies strings that exceed the maximum length and returns an error with
appropriate context.
"""

from zenyth.core.validation import ErrorCode, ValidationError, Validator


def test_validate_max_length_with_long_string() -> None:
    """Test validate_max_length with string exceeding maximum length.

    Validates maximum length validation with invalid input.

    SOLID Assessment:
    - SRP: Test focused solely on maximum length violation detection
    - OCP: Error context information extensible
    """
    long_string = "this is a very long string that exceeds the limit"
    result = Validator.validate_max_length(long_string, "test_field", 10)

    # Should return ValidationError for long string
    assert isinstance(result, ValidationError)
    assert result.field == "test_field"
    assert result.code == ErrorCode.TOO_LONG
    assert result.message == "test_field cannot exceed 10 characters"
    assert result.context == {"max_length": 10, "actual_length": len(long_string)}
