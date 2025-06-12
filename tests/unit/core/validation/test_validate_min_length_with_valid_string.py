"""Test validate_min_length with string meeting minimum length.

This test validates that the Validator.validate_min_length method correctly
accepts strings that meet the minimum length requirement.
"""

from zenyth.core.validation import Validator


def test_validate_min_length_with_valid_string() -> None:
    """Test validate_min_length with string meeting minimum length.

    Validates minimum length validation with valid input.

    SOLID Assessment:
    - SRP: Test focused solely on valid minimum length validation
    - DIP: Length validation independent of string content
    """
    result = Validator.validate_min_length("valid string", "test_field", 5)

    # Should return None for string meeting minimum length
    assert result is None
