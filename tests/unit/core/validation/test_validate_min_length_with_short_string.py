"""Test validate_min_length with string below minimum length.

This test validates that the Validator.validate_min_length method correctly
identifies strings shorter than the minimum requirement and returns an error
with appropriate context.
"""

from zenyth.core.validation import ErrorCode, ValidationError, Validator


def test_validate_min_length_with_short_string() -> None:
    """Test validate_min_length with string below minimum length.

    Validates minimum length validation with invalid input.

    SOLID Assessment:
    - SRP: Test focused solely on minimum length violation detection
    - OCP: Error context information extensible
    """
    result = Validator.validate_min_length("hi", "test_field", 5)

    # Should return ValidationError for short string
    assert isinstance(result, ValidationError)
    assert result.field == "test_field"
    assert result.code == ErrorCode.TOO_SHORT
    assert result.message == "test_field must be at least 5 characters"
    assert result.context == {"min_length": 5, "actual_length": 2}
