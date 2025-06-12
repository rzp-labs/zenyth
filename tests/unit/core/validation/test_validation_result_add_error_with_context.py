"""Test adding validation error with context information.

This test validates that ValidationResult properly handles context information
for detailed error reporting, allowing additional error details to be captured
without modifying the core error structure.
"""

from zenyth.core.validation import ErrorCode, ValidationResult


def test_validation_result_add_error_with_context() -> None:
    """Test adding validation error with context information.

    Validates context handling for detailed error reporting.

    SOLID Assessment:
    - SRP: Test focused solely on context handling
    - DIP: Context handling independent of specific context types
    """
    result = ValidationResult()
    result.add_error(
        "password",
        ErrorCode.TOO_SHORT,
        message="Password too short",
        min_length=8,
        actual_length=4,
    )

    # Should add context as kwargs
    assert len(result.errors) == 1
    error = result.errors[0]
    assert error.context == {"min_length": 8, "actual_length": 4}
