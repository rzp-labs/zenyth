"""Test validate_min_length trims whitespace before checking.

This test validates that the Validator.validate_min_length method trims
whitespace from the string before checking its length, ensuring consistent
validation behavior.
"""

from zenyth.core.validation import ValidationError, Validator


def test_validate_min_length_with_trimmed_string() -> None:
    """Test validate_min_length trims whitespace before checking.

    Validates that minimum length validation uses trimmed length.

    SOLID Assessment:
    - SRP: Test focused solely on whitespace trimming behavior
    - DIP: Trimming logic independent of validation context
    """
    # String with padding that becomes too short when trimmed
    result = Validator.validate_min_length("  hi  ", "test_field", 5)

    # Should use trimmed length (2) not padded length (6)
    assert isinstance(result, ValidationError)
    assert result.context["actual_length"] == 2
