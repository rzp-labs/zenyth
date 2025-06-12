"""Test ValidationError creation with minimal required fields.

This test validates that ValidationError dataclass can be created with just
the required fields, demonstrating the Single Responsibility Principle by
focusing solely on holding validation error data.
"""

from zenyth.core.validation import ErrorCode, ValidationError


def test_validation_error_creation_with_required_fields() -> None:
    """Test ValidationError creation with minimal required fields.

    Validates Single Responsibility Principle - dataclass focused
    solely on holding validation error data.

    SOLID Assessment:
    - SRP: Test focused solely on basic error creation
    - LSP: Validates consistent interface contract
    """
    error = ValidationError(field="test_field", code=ErrorCode.REQUIRED, message="Test message")

    # Should store all required fields
    assert error.field == "test_field"
    assert error.code == ErrorCode.REQUIRED
    assert error.message == "Test message"
    assert error.context is None  # Default value
