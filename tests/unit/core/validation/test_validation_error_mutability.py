"""Test that ValidationError allows field access and modification.

This test validates that ValidationError dataclass provides normal attribute
access patterns for validation error data, allowing both reading and modification
of fields as needed.
"""

from zenyth.core.validation import ErrorCode, ValidationError


def test_validation_error_mutability() -> None:
    """Test that ValidationError allows field access and modification.

    Validates that dataclass provides normal attribute access patterns
    for validation error data.

    SOLID Assessment:
    - SRP: Test focused solely on data structure access validation
    - OCP: Mutable structure allows field inspection and modification
    """
    error = ValidationError(field="test", code=ErrorCode.EMPTY, message="Test message")

    # Should allow field access
    assert error.field == "test"
    assert error.code == ErrorCode.EMPTY
    assert error.message == "Test message"

    # Should allow modification (normal dataclass behavior)
    error.field = "modified"
    assert error.field == "modified"
