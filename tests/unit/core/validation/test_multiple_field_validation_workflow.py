"""Test validation workflow with multiple fields.

This test validates that the validation framework handles multiple fields
with different validation rules properly, collecting errors for each field
that fails validation.
"""

from zenyth.core.validation import ValidationResult, Validator


def test_multiple_field_validation_workflow() -> None:
    """Test validation workflow with multiple fields.

    Validates that validation framework handles multiple fields
    with different validation rules properly.

    SOLID Assessment:
    - SRP: Test focused solely on multi-field validation
    - OCP: Framework extensible to any number of fields and rules
    """
    result = ValidationResult()
    validator = Validator()

    # Multiple fields with different validation requirements
    fields = {
        "username": "",  # Empty - should fail
        "email": "user@example.com",  # Valid
        "password": "123",  # Too short - should fail
        "description": "A" * 200,  # Too long - should fail
    }

    # Validate each field with appropriate rules
    for field_name, value in fields.items():
        error = None
        if field_name == "username":
            error = validator.validate_not_empty(value, field_name)
        elif field_name == "password":
            error = validator.validate_min_length(value, field_name, 8)
        elif field_name == "description":
            error = validator.validate_max_length(value, field_name, 100)

        if error:
            result.errors.append(error)

    # Should collect errors for username, password, and description
    assert result.is_valid() is False
    assert len(result.errors) == 3

    error_fields = {error.field for error in result.errors}
    assert error_fields == {"username", "password", "description"}
