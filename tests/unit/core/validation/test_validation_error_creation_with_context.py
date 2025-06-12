"""Test ValidationError creation with optional context.

This test validates that ValidationError supports extensibility through an
optional context parameter, allowing additional error information without
modifying the core structure.
"""

from zenyth.core.validation import ErrorCode, ValidationError


def test_validation_error_creation_with_context() -> None:
    """Test ValidationError creation with optional context.

    Validates extensibility through optional context parameter.

    SOLID Assessment:
    - OCP: Optional context allows extension without modification
    - SRP: Test focused solely on context handling
    """
    context_data = {"min_length": 5, "actual_length": 2}
    error = ValidationError(
        field="description",
        code=ErrorCode.TOO_SHORT,
        message="Description too short",
        context=context_data,
    )

    # Should store context information
    assert error.context == context_data
    assert error.context["min_length"] == 5
    assert error.context["actual_length"] == 2
