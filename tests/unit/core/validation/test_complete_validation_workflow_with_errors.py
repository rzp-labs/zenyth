"""Test complete validation workflow with validation errors.

This test validates the end-to-end validation process with error collection,
demonstrating how validation errors are captured when validation rules fail.
"""

from zenyth.core.validation import ErrorCode, ValidationResult, Validator


def test_complete_validation_workflow_with_errors() -> None:
    """Test complete validation workflow with validation errors.

    Validates end-to-end validation process with error collection.

    SOLID Assessment:
    - SRP: Test focused solely on error collection workflow
    - OCP: Error collection extensible to any validation rules
    """
    result = ValidationResult()
    validator = Validator()

    # Invalid input data
    task_description = None

    # Chain validation rules (will fail on first check)
    if error := validator.validate_required(task_description, "task_description"):
        result.errors.append(error)

    # Should collect validation error
    assert result.is_valid() is False
    assert len(result.errors) == 1
    assert result.errors[0].code == ErrorCode.REQUIRED
