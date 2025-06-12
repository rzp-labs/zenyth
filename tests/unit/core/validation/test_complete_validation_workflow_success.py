"""Test complete validation workflow with valid input.

This test validates the end-to-end validation process with no errors,
demonstrating how validation rules can be chained together to validate
task descriptions.
"""

from zenyth.core.validation import ValidationResult, Validator


def test_complete_validation_workflow_success() -> None:
    """Test complete validation workflow with valid input.

    Validates end-to-end validation process with no errors.

    SOLID Assessment:
    - SRP: Test focused solely on successful validation workflow
    - DIP: Workflow uses abstractions for all validation steps
    """
    result = ValidationResult()
    validator = Validator()

    # Valid input data
    task_description = "Build a user authentication system with JWT tokens"

    # Chain validation rules
    if (
        (error := validator.validate_required(task_description, "task_description"))
        or (error := validator.validate_not_empty(task_description, "task_description"))
        or (error := validator.validate_min_length(task_description, "task_description", 10))
        or (error := validator.validate_max_length(task_description, "task_description", 100))
    ):
        result.errors.append(error)

    # Should pass all validations
    assert result.is_valid() is True
    assert len(result.errors) == 0
