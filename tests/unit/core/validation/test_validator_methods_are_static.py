"""Test that all Validator methods are static methods.

This test validates that validation methods follow the pure function pattern
without instance dependencies, ensuring they can be called without creating
a Validator instance.
"""

from zenyth.core.validation import Validator


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
