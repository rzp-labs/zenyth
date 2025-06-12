"""Test validate_required with None value.

This test validates that the Validator.validate_required method correctly
identifies None values as invalid and returns an appropriate error.
"""

from zenyth.core.validation import ErrorCode, ValidationError, Validator


def test_validate_required_with_none_value() -> None:
    """Test validate_required with None value.

    Validates required field validation with invalid (None) input.

    SOLID Assessment:
    - SRP: Test focused solely on invalid required field validation
    - LSP: Consistent return pattern (ValidationError for invalid)
    """
    result = Validator.validate_required(None, "test_field")

    # Should return ValidationError for None
    assert isinstance(result, ValidationError)
    assert result.field == "test_field"
    assert result.code == ErrorCode.REQUIRED
    assert result.message == "Task description required"
