"""Test raise_if_invalid combines multiple error messages.

This test validates that ValidationResult.raise_if_invalid() properly combines
multiple error messages when raising a ValidationError exception.
"""

import pytest

from zenyth.core.exceptions import ValidationError as ZenythValidationError
from zenyth.core.validation import ErrorCode, ValidationResult


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
