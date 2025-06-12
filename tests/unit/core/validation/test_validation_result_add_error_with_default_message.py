"""Test adding validation error with default message generation.

This test validates that ValidationResult can add errors with sensible default
messages when no custom message is provided, demonstrating error collection
functionality with reasonable defaults.
"""

from zenyth.core.validation import ErrorCode, ValidationResult


def test_validation_result_add_error_with_default_message() -> None:
    """Test adding validation error with default message generation.

    Validates error collection functionality with sensible defaults.

    SOLID Assessment:
    - SRP: Test focused solely on error addition logic
    - OCP: Default message generation extensible
    """
    result = ValidationResult()
    result.add_error("username", ErrorCode.REQUIRED)

    # Should add error with default message
    assert len(result.errors) == 1
    error = result.errors[0]
    assert error.field == "username"
    assert error.code == ErrorCode.REQUIRED
    assert error.message == "username: FIELD_REQUIRED"
    assert error.context == {}  # Empty dict when no context provided
