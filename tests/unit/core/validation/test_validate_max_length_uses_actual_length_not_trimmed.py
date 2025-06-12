"""Test validate_max_length uses actual string length, not trimmed.

This test validates that the Validator.validate_max_length method counts all
characters including whitespace, not just the trimmed length, ensuring proper
validation of actual string length.
"""

from zenyth.core.validation import ValidationError, Validator


def test_validate_max_length_uses_actual_length_not_trimmed() -> None:
    """Test validate_max_length uses actual string length, not trimmed.

    Validates that maximum length validation counts all characters including whitespace.

    SOLID Assessment:
    - SRP: Test focused solely on actual vs trimmed length behavior
    - DIP: Length calculation independent of validation context
    """
    # String that would be valid if trimmed but invalid as-is
    padded_string = "  short  "  # 9 characters total
    result = Validator.validate_max_length(padded_string, "test_field", 8)

    # Should use actual length (9) not trimmed length (5)
    assert isinstance(result, ValidationError)
    assert result.context["actual_length"] == 9
