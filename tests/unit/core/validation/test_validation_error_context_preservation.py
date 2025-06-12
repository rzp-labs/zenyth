"""Test that validation error context is preserved through workflow.

This test validates that context information flows properly through the
validation workflow, ensuring that detailed error information is available
for debugging and user feedback.
"""

from zenyth.core.validation import ValidationResult, Validator


def test_validation_error_context_preservation() -> None:
    """Test that validation error context is preserved through workflow.

    Validates that context information flows properly through validation.

    SOLID Assessment:
    - SRP: Test focused solely on context preservation
    - DIP: Context handling independent of specific context types
    """
    result = ValidationResult()
    validator = Validator()

    # Input that will fail length validation
    short_text = "hi"
    min_length = 10

    if error := validator.validate_min_length(short_text, "description", min_length):
        result.errors.append(error)

    # Should preserve context information
    assert len(result.errors) == 1
    error = result.errors[0]
    assert error.context is not None
    assert error.context["min_length"] == min_length
    assert error.context["actual_length"] == len(short_text.strip())
