"""Test validate_not_empty with non-empty string.

This test validates that the Validator.validate_not_empty method correctly
accepts non-empty strings as valid.
"""

from zenyth.core.validation import Validator


def test_validate_not_empty_with_valid_string() -> None:
    """Test validate_not_empty with non-empty string.

    Validates empty string validation with valid input.

    SOLID Assessment:
    - SRP: Test focused solely on valid non-empty string validation
    - LSP: Consistent return pattern for valid input
    """
    result = Validator.validate_not_empty("valid string", "test_field")

    # Should return None for non-empty string
    assert result is None
