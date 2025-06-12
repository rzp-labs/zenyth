"""Test validate_required with various non-None types.

This test validates that the Validator.validate_required method accepts any
type of value as long as it's not None, including empty strings, zero, and
empty collections.
"""

from zenyth.core.validation import Validator


def test_validate_required_with_various_valid_types() -> None:
    """Test validate_required with various non-None types.

    Validates that required validation accepts any non-None value.

    SOLID Assessment:
    - SRP: Test focused solely on type-agnostic required validation
    - DIP: Validation logic independent of specific value types
    """
    valid_values = ["string", 123, [], {}, False, 0, ""]

    for value in valid_values:
        result = Validator.validate_required(value, "test_field")
        assert result is None, f"Should accept {type(value).__name__}: {value}"
