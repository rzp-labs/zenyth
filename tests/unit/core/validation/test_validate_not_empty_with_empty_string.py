"""Test validate_not_empty with empty string.

This test validates that the Validator.validate_not_empty method correctly
identifies empty strings as invalid and returns an appropriate error.
"""

from zenyth.core.validation import ErrorCode, ValidationError, Validator


def test_validate_not_empty_with_empty_string() -> None:
    """Test validate_not_empty with empty string.

    Validates empty string validation with invalid input.

    SOLID Assessment:
    - SRP: Test focused solely on empty string detection
    - LSP: Consistent error return pattern
    """
    result = Validator.validate_not_empty("", "test_field")

    # Should return ValidationError for empty string
    assert isinstance(result, ValidationError)
    assert result.field == "test_field"
    assert result.code == ErrorCode.EMPTY
    assert result.message == "Task description empty"
