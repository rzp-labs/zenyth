"""Test adding validation error with custom message.

This test validates that ValidationResult supports custom error messages,
demonstrating flexibility in error message customization following the
Open/Closed Principle.
"""

from zenyth.core.validation import ErrorCode, ValidationResult


def test_validation_result_add_error_with_custom_message() -> None:
    """Test adding validation error with custom message.

    Validates flexibility in error message customization.

    SOLID Assessment:
    - OCP: Custom message parameter allows extension without modification
    - SRP: Test focused solely on custom message handling
    """
    result = ValidationResult()
    custom_message = "Username is required for registration"
    result.add_error("username", ErrorCode.REQUIRED, message=custom_message)

    # Should use custom message
    assert len(result.errors) == 1
    error = result.errors[0]
    assert error.message == custom_message
