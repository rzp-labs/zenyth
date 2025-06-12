"""Test is_valid returns True when no errors exist.

This test validates that ValidationResult properly reports valid state when
no validation errors have been collected.
"""

from zenyth.core.validation import ValidationResult


def test_validation_result_is_valid_with_no_errors() -> None:
    """Test is_valid returns True when no errors exist.

    Validates proper validation state reporting.

    SOLID Assessment:
    - SRP: Test focused solely on validation state checking
    - LSP: is_valid method consistent across all ValidationResult instances
    """
    result = ValidationResult()

    # Should be valid with no errors
    assert result.is_valid() is True
