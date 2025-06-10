"""Structured validation framework for Zenyth SPARC orchestration system.

This module provides a consistent, type-safe approach to input validation that
treats validation as data flow rather than control flow. It eliminates the need
for proliferating custom exception classes while maintaining clear error semantics.

The framework supports:
- Composable validation rules
- Machine-readable error codes
- Contextual error information
- Consistent error messaging
- Type-safe validation results

Examples:
    Basic validation with single rule::

        validator = Validator()
        result = ValidationResult()

        if error := validator.validate_required(data.get('description'), 'description'):
            result.errors.append(error)

        if not result.is_valid():
            result.raise_if_invalid()

    Complex validation with multiple rules::

        def validate_task_context(context: PhaseContext) -> ValidationResult:
            result = ValidationResult()
            validator = Validator()

            # Chain validation rules
            if error := validator.validate_required(context.task_description, 'task_description'):
                result.errors.append(error)
            elif error := validator.validate_min_length(
                context.task_description, 'task_description', 10
            ):
                result.errors.append(error)

            return result
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any

from zenyth.core.exceptions import ValidationError as ZenythValidationError


class ErrorCode(Enum):
    """Standard validation error codes for consistent error handling."""

    REQUIRED = "FIELD_REQUIRED"
    EMPTY = "FIELD_EMPTY"
    TOO_SHORT = "FIELD_TOO_SHORT"
    TOO_LONG = "FIELD_TOO_LONG"
    INVALID_FORMAT = "FIELD_INVALID_FORMAT"
    INVALID_TYPE = "FIELD_INVALID_TYPE"


@dataclass
class ValidationError:
    """Individual validation error with structured information.

    Represents a single validation failure with machine-readable error code,
    human-readable message, and optional context for debugging or detailed
    error reporting.

    Attributes:
        field: Name of the field that failed validation
        code: Standardized error code for programmatic handling
        message: Human-readable error description
        context: Optional additional context information
    """

    field: str
    code: ErrorCode
    message: str
    context: dict[str, Any] | None = None


class ValidationResult:
    """Collection of validation errors with utilities for error handling.

    Accumulates multiple validation errors and provides methods for checking
    validity and raising exceptions when validation fails. Supports both
    gradual error collection and immediate failure modes.

    Examples:
        Gradual error collection::

            result = ValidationResult()
            result.add_error('name', ErrorCode.REQUIRED)
            result.add_error('email', ErrorCode.INVALID_FORMAT, pattern='email')

            if not result.is_valid():
                result.raise_if_invalid()

        Immediate failure mode::

            result = ValidationResult()
            result.add_error('critical_field', ErrorCode.REQUIRED)
            result.raise_if_invalid()  # Raises immediately
    """

    def __init__(self) -> None:
        """Initialize empty validation result."""
        self.errors: list[ValidationError] = []

    def add_error(
        self, field: str, code: ErrorCode, message: str | None = None, **context: Any
    ) -> None:
        """Add validation error to the result.

        Args:
            field: Name of the field that failed validation
            code: Standardized error code
            message: Optional custom message (defaults to standard message)
            **context: Additional context information for the error
        """
        if message is None:
            message = f"{field}: {code.value}"

        self.errors.append(
            ValidationError(field=field, code=code, message=message, context=context)
        )

    def is_valid(self) -> bool:
        """Check if validation passed (no errors).

        Returns:
            True if no validation errors, False otherwise
        """
        return len(self.errors) == 0

    def raise_if_invalid(self) -> None:
        """Raise ValidationError if any validation errors exist.

        Combines all error messages into a single exception message.

        Raises:
            ZenythValidationError: If validation errors exist
        """
        if not self.is_valid():
            messages = [error.message for error in self.errors]
            combined_message = "; ".join(messages)
            raise ZenythValidationError(combined_message)


class Validator:
    """Collection of reusable validation rules.

    Provides standard validation methods that return ValidationError objects
    for failed validations or None for successful validations. All methods
    are pure functions with no side effects.

    The validator methods follow a consistent pattern:
    - Accept the value to validate and field name
    - Accept additional parameters for validation criteria
    - Return ValidationError for failures, None for success
    - Include relevant context in error objects
    """

    @staticmethod
    def validate_required(value: Any, field: str) -> ValidationError | None:
        """Validate that a field has a non-None value.

        Args:
            value: Value to validate (any type)
            field: Name of the field being validated

        Returns:
            ValidationError if value is None, None if valid
        """
        if value is None:
            return ValidationError(
                field=field, code=ErrorCode.REQUIRED, message="Task description required"
            )
        return None

    @staticmethod
    def validate_not_empty(value: str, field: str) -> ValidationError | None:
        """Validate that a string field is not empty or whitespace-only.

        Args:
            value: String value to validate
            field: Name of the field being validated

        Returns:
            ValidationError if value is empty/whitespace, None if valid
        """
        if not value or not value.strip():
            return ValidationError(
                field=field, code=ErrorCode.EMPTY, message="Task description empty"
            )
        return None

    @staticmethod
    def validate_min_length(
        value: str, field: str, min_length: int
    ) -> ValidationError | None:
        """Validate that a string meets minimum length requirement.

        Args:
            value: String value to validate
            field: Name of the field being validated
            min_length: Minimum required length

        Returns:
            ValidationError if too short, None if valid
        """
        if len(value.strip()) < min_length:
            return ValidationError(
                field=field,
                code=ErrorCode.TOO_SHORT,
                message=f"{field} must be at least {min_length} characters",
                context={"min_length": min_length, "actual_length": len(value.strip())},
            )
        return None

    @staticmethod
    def validate_max_length(
        value: str, field: str, max_length: int
    ) -> ValidationError | None:
        """Validate that a string does not exceed maximum length.

        Args:
            value: String value to validate
            field: Name of the field being validated
            max_length: Maximum allowed length

        Returns:
            ValidationError if too long, None if valid
        """
        if len(value) > max_length:
            return ValidationError(
                field=field,
                code=ErrorCode.TOO_LONG,
                message=f"{field} cannot exceed {max_length} characters",
                context={"max_length": max_length, "actual_length": len(value)},
            )
        return None
