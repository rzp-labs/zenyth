"""Test validate_max_length with string within maximum length.

This test validates that the Validator.validate_max_length method correctly
accepts strings that are within the maximum length limit.
"""

from zenyth.core.validation import Validator


def test_validate_max_length_with_valid_string() -> None:
    """Test validate_max_length with string within maximum length.

    Validates maximum length validation with valid input.

    SOLID Assessment:
    - SRP: Test focused solely on valid maximum length validation
    - LSP: Consistent return pattern for valid input
    """
    result = Validator.validate_max_length("short", "test_field", 10)

    # Should return None for string within maximum length
    assert result is None
