"""Test ValidationResult proper initialization.

This test validates that ValidationResult initializes correctly with an empty
error list and valid state, demonstrating the Single Responsibility Principle
by focusing solely on error collection state setup.
"""

from zenyth.core.validation import ValidationResult


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
