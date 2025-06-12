"""Test validate_required with non-None value.

This test validates that the Validator.validate_required method correctly
accepts any non-None value as valid.
"""

from zenyth.core.validation import Validator


def test_validate_required_with_valid_value() -> None:
    """Test validate_required with non-None value.

    Validates required field validation with valid input.

    SOLID Assessment:
    - SRP: Test focused solely on valid required field validation
    - LSP: Consistent return pattern (None for valid)
    """
    result = Validator.validate_required("valid_value", "test_field")

    # Should return None for valid value
    assert result is None
