"""Test that all validation methods follow consistent return contract.

This test validates the Liskov Substitution Principle by ensuring all
validation methods are substitutable with the same return pattern: None for
valid input and ValidationError for invalid input.
"""

from zenyth.core.validation import ValidationError, Validator


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
            result,
            ValidationError,
        ), f"{method.__name__} should return ValidationError for invalid input"
