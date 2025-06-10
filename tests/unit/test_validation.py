"""Test suite for structured validation framework.

Tests the validation framework implementation following SOLID principles
and ensuring proper validation logic, error handling, and data structures.

SOLID PRINCIPLES VALIDATION:

✅ Single Responsibility Principle (SRP):
   - ErrorCode: Solely responsible for defining standard error codes
   - ValidationError: Solely responsible for holding validation error data
   - ValidationResult: Solely responsible for collecting and managing validation errors
   - Validator: Solely responsible for providing reusable validation rules
   - Each test function: Single focused validation concern

✅ Open/Closed Principle (OCP):
   - Validator class open for extension via new static methods
   - ErrorCode enum open for extension via new error types
   - ValidationResult open for extension via new error handling methods
   - Tests validate extensibility without modification

✅ Liskov Substitution Principle (LSP):
   - ValidationError dataclass maintains consistent interface contract
   - All validator methods follow consistent return pattern (ValidationError | None)
   - Tests ensure all validation methods are substitutable

✅ Interface Segregation Principle (ISP):
   - Validator methods focused on specific validation concerns
   - ValidationResult focused solely on error collection and checking
   - No fat interfaces forcing unnecessary implementations

✅ Dependency Inversion Principle (DIP):
   - Validation framework depends on abstractions (ErrorCode enum, structured data)
   - Validator methods are pure functions with no concrete dependencies
   - ValidationResult raises abstract ValidationError, not concrete implementation details
"""

import pytest

from zenyth.core.exceptions import ValidationError as ZenythValidationError
from zenyth.core.validation import (
    ErrorCode,
    ValidationError,
    ValidationResult,
    Validator,
)


# ErrorCode enum tests
def test_error_code_enum_has_required_values() -> None:
    """Test that ErrorCode enum contains all expected error codes.

    Validates Interface Segregation Principle - enum provides focused
    set of error codes without unnecessary complexity.

    SOLID Assessment:
    - SRP: Test focused solely on enum value existence
    - ISP: Validates minimal, focused error code interface
    """
    # Should have all standard validation error codes
    assert ErrorCode.REQUIRED.value == "FIELD_REQUIRED"
    assert ErrorCode.EMPTY.value == "FIELD_EMPTY"
    assert ErrorCode.TOO_SHORT.value == "FIELD_TOO_SHORT"
    assert ErrorCode.TOO_LONG.value == "FIELD_TOO_LONG"
    assert ErrorCode.INVALID_FORMAT.value == "FIELD_INVALID_FORMAT"
    assert ErrorCode.INVALID_TYPE.value == "FIELD_INVALID_TYPE"


def test_error_code_enum_extensibility() -> None:
    """Test that ErrorCode enum follows Open/Closed Principle.

    Validates that new error codes can be added without modifying existing code.

    SOLID Assessment:
    - OCP: Enum structure allows extension without modification
    - SRP: Test focused solely on extensibility validation
    """
    # Should be able to use all error codes as enum members
    all_codes = list(ErrorCode)
    assert len(all_codes) >= 6  # At least the core validation codes

    # All codes should have string values
    for code in all_codes:
        assert isinstance(code.value, str)
        assert code.value.startswith("FIELD_")


# ValidationError dataclass tests
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


# ValidationResult tests
def test_validation_result_initialization() -> None:
    """Test ValidationResult proper initialization.

    Validates Single Responsibility Principle - initialization
    focused solely on setting up error collection state.

    SOLID Assessment:
    - SRP: Test focused solely on initialization logic
    - DIP: No concrete dependencies in initialization
    """
    result = ValidationResult()

    # Should initialize with empty error list
    assert result.errors == []
    assert result.is_valid() is True


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


def test_validation_result_add_error_with_custom_message() -> None:
    """Test adding validation error with custom message.

    Validates flexibility in error message customization.

    SOLID Assessment:
    - OCP: Custom message parameter allows extension without modification
    - SRP: Test focused solely on custom message handling
    """
    result = ValidationResult()
    custom_message = "Username is required for registration"
    result.add_error("username", ErrorCode.REQUIRED, message=custom_message)

    # Should use custom message
    assert len(result.errors) == 1
    error = result.errors[0]
    assert error.message == custom_message


def test_validation_result_add_error_with_context() -> None:
    """Test adding validation error with context information.

    Validates context handling for detailed error reporting.

    SOLID Assessment:
    - SRP: Test focused solely on context handling
    - DIP: Context handling independent of specific context types
    """
    result = ValidationResult()
    result.add_error(
        "password", ErrorCode.TOO_SHORT, message="Password too short", min_length=8, actual_length=4
    )

    # Should add context as kwargs
    assert len(result.errors) == 1
    error = result.errors[0]
    assert error.context == {"min_length": 8, "actual_length": 4}


def test_validation_result_multiple_errors() -> None:
    """Test ValidationResult with multiple validation errors.

    Validates proper error accumulation without interference.

    SOLID Assessment:
    - SRP: Test focused solely on multiple error collection
    - OCP: Error collection extensible to any number of errors
    """
    result = ValidationResult()
    result.add_error("username", ErrorCode.REQUIRED)
    result.add_error("email", ErrorCode.INVALID_FORMAT)
    result.add_error("password", ErrorCode.TOO_SHORT)

    # Should collect all errors
    assert len(result.errors) == 3
    assert result.is_valid() is False

    # Should maintain error order
    assert result.errors[0].field == "username"
    assert result.errors[1].field == "email"
    assert result.errors[2].field == "password"


def test_validation_result_is_valid_with_no_errors() -> None:
    """Test is_valid returns True when no errors exist.

    Validates proper validation state reporting.

    SOLID Assessment:
    - SRP: Test focused solely on validation state checking
    - LSP: is_valid method consistent across all ValidationResult instances
    """
    result = ValidationResult()

    # Should be valid with no errors
    assert result.is_valid() is True


def test_validation_result_is_valid_with_errors() -> None:
    """Test is_valid returns False when errors exist.

    Validates proper validation state reporting with errors.

    SOLID Assessment:
    - SRP: Test focused solely on validation state with errors
    - LSP: Consistent validation state behavior
    """
    result = ValidationResult()
    result.add_error("field", ErrorCode.REQUIRED)

    # Should be invalid with errors
    assert result.is_valid() is False


def test_validation_result_raise_if_invalid_with_no_errors() -> None:
    """Test raise_if_invalid does nothing when valid.

    Validates that no exception is raised for valid results.

    SOLID Assessment:
    - SRP: Test focused solely on valid result handling
    - DIP: Exception handling independent of specific error types
    """
    result = ValidationResult()

    # Should not raise when valid
    try:
        result.raise_if_invalid()
    except Exception:
        pytest.fail("Should not raise exception for valid result")


def test_validation_result_raise_if_invalid_with_single_error() -> None:
    """Test raise_if_invalid raises exception with single error.

    Validates proper exception raising with single validation error.

    SOLID Assessment:
    - SRP: Test focused solely on single error exception handling
    - DIP: Uses abstract ZenythValidationError, not concrete implementation
    """
    result = ValidationResult()
    result.add_error("username", ErrorCode.REQUIRED, message="Username is required")

    # Should raise with error message
    with pytest.raises(ZenythValidationError, match="Username is required"):
        result.raise_if_invalid()


def test_validation_result_raise_if_invalid_with_multiple_errors() -> None:
    """Test raise_if_invalid combines multiple error messages.

    Validates proper error message combination for multiple errors.

    SOLID Assessment:
    - SRP: Test focused solely on multiple error message handling
    - OCP: Error message combination extensible to any number of errors
    """
    result = ValidationResult()
    result.add_error("username", ErrorCode.REQUIRED, message="Username required")
    result.add_error("email", ErrorCode.INVALID_FORMAT, message="Email invalid")

    # Should combine error messages
    with pytest.raises(ZenythValidationError, match="Username required; Email invalid"):
        result.raise_if_invalid()


# Validator tests
def test_validate_required_with_valid_value() -> None:
    """Test validate_required with non-None value.

    Validates required field validation with valid input.

    SOLID Assessment:
    - SRP: Test focused solely on valid required field validation
    - LSP: Consistent return pattern (None for valid)
    """
    result = Validator.validate_required("valid_value", "test_field")

    # Should return None for valid value
    assert result is None


def test_validate_required_with_none_value() -> None:
    """Test validate_required with None value.

    Validates required field validation with invalid (None) input.

    SOLID Assessment:
    - SRP: Test focused solely on invalid required field validation
    - LSP: Consistent return pattern (ValidationError for invalid)
    """
    result = Validator.validate_required(None, "test_field")

    # Should return ValidationError for None
    assert isinstance(result, ValidationError)
    assert result.field == "test_field"
    assert result.code == ErrorCode.REQUIRED
    assert result.message == "Task description required"


def test_validate_required_with_various_valid_types() -> None:
    """Test validate_required with various non-None types.

    Validates that required validation accepts any non-None value.

    SOLID Assessment:
    - SRP: Test focused solely on type-agnostic required validation
    - DIP: Validation logic independent of specific value types
    """
    valid_values = ["string", 123, [], {}, False, 0, ""]

    for value in valid_values:
        result = Validator.validate_required(value, "test_field")
        assert result is None, f"Should accept {type(value).__name__}: {value}"


def test_validate_not_empty_with_valid_string() -> None:
    """Test validate_not_empty with non-empty string.

    Validates empty string validation with valid input.

    SOLID Assessment:
    - SRP: Test focused solely on valid non-empty string validation
    - LSP: Consistent return pattern for valid input
    """
    result = Validator.validate_not_empty("valid string", "test_field")

    # Should return None for non-empty string
    assert result is None


def test_validate_not_empty_with_empty_string() -> None:
    """Test validate_not_empty with empty string.

    Validates empty string validation with invalid input.

    SOLID Assessment:
    - SRP: Test focused solely on empty string detection
    - LSP: Consistent error return pattern
    """
    result = Validator.validate_not_empty("", "test_field")

    # Should return ValidationError for empty string
    assert isinstance(result, ValidationError)
    assert result.field == "test_field"
    assert result.code == ErrorCode.EMPTY
    assert result.message == "Task description empty"


def test_validate_not_empty_with_whitespace_only() -> None:
    """Test validate_not_empty with whitespace-only string.

    Validates that whitespace-only strings are treated as empty.

    SOLID Assessment:
    - SRP: Test focused solely on whitespace handling
    - OCP: Whitespace logic extensible without modifying core validation
    """
    whitespace_strings = ["   ", "\t", "\n", "\r\n", "  \t  \n  "]

    for whitespace in whitespace_strings:
        result = Validator.validate_not_empty(whitespace, "test_field")
        assert isinstance(result, ValidationError)
        assert result.code == ErrorCode.EMPTY


def test_validate_min_length_with_valid_string() -> None:
    """Test validate_min_length with string meeting minimum length.

    Validates minimum length validation with valid input.

    SOLID Assessment:
    - SRP: Test focused solely on valid minimum length validation
    - DIP: Length validation independent of string content
    """
    result = Validator.validate_min_length("valid string", "test_field", 5)

    # Should return None for string meeting minimum length
    assert result is None


def test_validate_min_length_with_short_string() -> None:
    """Test validate_min_length with string below minimum length.

    Validates minimum length validation with invalid input.

    SOLID Assessment:
    - SRP: Test focused solely on minimum length violation detection
    - OCP: Error context information extensible
    """
    result = Validator.validate_min_length("hi", "test_field", 5)

    # Should return ValidationError for short string
    assert isinstance(result, ValidationError)
    assert result.field == "test_field"
    assert result.code == ErrorCode.TOO_SHORT
    assert result.message == "test_field must be at least 5 characters"
    assert result.context == {"min_length": 5, "actual_length": 2}


def test_validate_min_length_with_trimmed_string() -> None:
    """Test validate_min_length trims whitespace before checking.

    Validates that minimum length validation uses trimmed length.

    SOLID Assessment:
    - SRP: Test focused solely on whitespace trimming behavior
    - DIP: Trimming logic independent of validation context
    """
    # String with padding that becomes too short when trimmed
    result = Validator.validate_min_length("  hi  ", "test_field", 5)

    # Should use trimmed length (2) not padded length (6)
    assert isinstance(result, ValidationError)
    assert result.context["actual_length"] == 2


def test_validate_max_length_with_valid_string() -> None:
    """Test validate_max_length with string within maximum length.

    Validates maximum length validation with valid input.

    SOLID Assessment:
    - SRP: Test focused solely on valid maximum length validation
    - LSP: Consistent return pattern for valid input
    """
    result = Validator.validate_max_length("short", "test_field", 10)

    # Should return None for string within maximum length
    assert result is None


def test_validate_max_length_with_long_string() -> None:
    """Test validate_max_length with string exceeding maximum length.

    Validates maximum length validation with invalid input.

    SOLID Assessment:
    - SRP: Test focused solely on maximum length violation detection
    - OCP: Error context information extensible
    """
    long_string = "this is a very long string that exceeds the limit"
    result = Validator.validate_max_length(long_string, "test_field", 10)

    # Should return ValidationError for long string
    assert isinstance(result, ValidationError)
    assert result.field == "test_field"
    assert result.code == ErrorCode.TOO_LONG
    assert result.message == "test_field cannot exceed 10 characters"
    assert result.context == {"max_length": 10, "actual_length": len(long_string)}


def test_validate_max_length_uses_actual_length_not_trimmed() -> None:
    """Test validate_max_length uses actual string length, not trimmed.

    Validates that maximum length validation counts all characters including whitespace.

    SOLID Assessment:
    - SRP: Test focused solely on actual vs trimmed length behavior
    - DIP: Length calculation independent of validation context
    """
    # String that would be valid if trimmed but invalid as-is
    padded_string = "  short  "  # 9 characters total
    result = Validator.validate_max_length(padded_string, "test_field", 8)

    # Should use actual length (9) not trimmed length (5)
    assert isinstance(result, ValidationError)
    assert result.context["actual_length"] == 9


def test_validator_methods_are_static() -> None:
    """Test that all Validator methods are static methods.

    Validates that validation methods follow pure function pattern
    without instance dependencies.

    SOLID Assessment:
    - SRP: Test focused solely on static method validation
    - DIP: Static methods have no instance dependencies
    """
    # Should be able to call methods without instance
    assert Validator.validate_required("test", "field") is None
    assert Validator.validate_not_empty("test", "field") is None
    assert Validator.validate_min_length("test", "field", 1) is None
    assert Validator.validate_max_length("test", "field", 10) is None


def test_validator_methods_follow_consistent_contract() -> None:
    """Test that all validation methods follow consistent return contract.

    Validates Liskov Substitution Principle - all validation methods
    are substitutable with consistent return pattern.

    SOLID Assessment:
    - LSP: All validation methods follow same contract pattern
    - ISP: Each method focused on single validation concern
    """
    methods_with_valid_input = [
        (Validator.validate_required, ("valid", "field")),
        (Validator.validate_not_empty, ("valid", "field")),
        (Validator.validate_min_length, ("valid", "field", 1)),
        (Validator.validate_max_length, ("valid", "field", 10)),
    ]

    # All methods should return None for valid input
    for method, args in methods_with_valid_input:
        result = method(*args)
        assert result is None, f"{method.__name__} should return None for valid input"

    methods_with_invalid_input = [
        (Validator.validate_required, (None, "field")),
        (Validator.validate_not_empty, ("", "field")),
        (Validator.validate_min_length, ("x", "field", 10)),
        (Validator.validate_max_length, ("very long string", "field", 5)),
    ]

    # All methods should return ValidationError for invalid input
    for method, args in methods_with_invalid_input:
        result = method(*args)
        assert isinstance(
            result, ValidationError
        ), f"{method.__name__} should return ValidationError for invalid input"


# Integration tests
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
