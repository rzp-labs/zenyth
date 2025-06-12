"""Test that validation framework supports extension.

This test validates the Open/Closed Principle by demonstrating that the
framework can be extended with new validation rules without modifying
existing code.
"""

from zenyth.core.validation import ErrorCode, ValidationError, ValidationResult


def test_validation_framework_extensibility() -> None:
    """Test that validation framework supports extension.

    Validates Open/Closed Principle - framework can be extended
    with new validation rules without modification.

    SOLID Assessment:
    - OCP: Framework extensible through new validation methods
    - DIP: Extension depends on abstractions, not concrete implementations
    """
    result = ValidationResult()

    # Custom validation logic (simulating framework extension)
    def validate_email_format(value: str, field: str) -> ValidationError | None:
        """Custom email validation following framework pattern."""
        if "@" not in value:
            return ValidationError(
                field=field,
                code=ErrorCode.INVALID_FORMAT,
                message=f"{field} must contain @ symbol",
                context={"expected_format": "email"},
            )
        return None

    # Use custom validation with framework
    email = "invalid-email"
    if error := validate_email_format(email, "email"):
        result.errors.append(error)

    # Should work seamlessly with existing framework
    assert result.is_valid() is False
    assert len(result.errors) == 1
    assert result.errors[0].code == ErrorCode.INVALID_FORMAT
    assert result.errors[0].context["expected_format"] == "email"
