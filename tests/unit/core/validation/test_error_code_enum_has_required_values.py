"""Test that ErrorCode enum contains all expected error codes.

This test validates that the ErrorCode enum provides all standard validation
error codes needed by the validation framework. It ensures the Interface
Segregation Principle by providing a focused set of error codes without
unnecessary complexity.
"""

from zenyth.core.validation import ErrorCode


def test_error_code_enum_has_required_values() -> None:
    """Test that ErrorCode enum contains all expected error codes.

    Validates Interface Segregation Principle - enum provides focused
    set of error codes without unnecessary complexity.

    SOLID Assessment:
    - SRP: Test focused solely on enum value existence
    - ISP: Validates minimal, focused error code interface
    """
    # Should have all standard validation error codes
    assert ErrorCode.REQUIRED.value == "FIELD_REQUIRED"
    assert ErrorCode.EMPTY.value == "FIELD_EMPTY"
    assert ErrorCode.TOO_SHORT.value == "FIELD_TOO_SHORT"
    assert ErrorCode.TOO_LONG.value == "FIELD_TOO_LONG"
    assert ErrorCode.INVALID_FORMAT.value == "FIELD_INVALID_FORMAT"
    assert ErrorCode.INVALID_TYPE.value == "FIELD_INVALID_TYPE"
