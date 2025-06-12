"""Test is_valid returns False when errors exist.

This test validates that ValidationResult properly reports invalid state when
validation errors have been collected.
"""

from zenyth.core.validation import ErrorCode, ValidationResult


def test_validation_result_is_valid_with_errors() -> None:
    """Test is_valid returns False when errors exist.

    Validates proper validation state reporting with errors.

    SOLID Assessment:
    - SRP: Test focused solely on validation state with errors
    - LSP: Consistent validation state behavior
    """
    result = ValidationResult()
    result.add_error("field", ErrorCode.REQUIRED)

    # Should be invalid with errors
    assert result.is_valid() is False
