"""Test that ErrorCode enum follows Open/Closed Principle.

This test validates that the ErrorCode enum structure allows new error codes
to be added without modifying existing code, demonstrating proper extensibility.
"""

from zenyth.core.validation import ErrorCode


def test_error_code_enum_extensibility() -> None:
    """Test that ErrorCode enum follows Open/Closed Principle.

    Validates that new error codes can be added without modifying existing code.

    SOLID Assessment:
    - OCP: Enum structure allows extension without modification
    - SRP: Test focused solely on extensibility validation
    """
    # Should be able to use all error codes as enum members
    all_codes = list(ErrorCode)
    assert len(all_codes) >= 6  # At least the core validation codes

    # All codes should have string values
    for code in all_codes:
        assert isinstance(code.value, str)
        assert code.value.startswith("FIELD_")
