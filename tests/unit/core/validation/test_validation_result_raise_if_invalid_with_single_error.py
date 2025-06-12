"""Test raise_if_invalid raises exception with single error.

This test validates that ValidationResult.raise_if_invalid() properly raises
a ValidationError exception with the correct message when a single validation
error exists.
"""

import pytest

from zenyth.core.exceptions import ValidationError as ZenythValidationError
from zenyth.core.validation import ErrorCode, ValidationResult


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
