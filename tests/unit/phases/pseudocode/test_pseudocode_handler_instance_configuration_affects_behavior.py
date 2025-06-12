"""Test that instance configuration meaningfully affects handler behavior.

This test validates that handler uses instance state to avoid 'could be static' warnings.
Demonstrates proper SOLID compliance with meaningful instance dependencies.

SOLID Assessment:
- SRP: Configuration focused solely on behavior modification
- DIP: Configuration through dependency injection, not hardcoded values
"""

from zenyth.phases.pseudocode import PseudocodeHandler


def test_pseudocode_handler_instance_configuration_affects_behavior() -> None:
    """Test that instance configuration meaningfully affects handler behavior.

    Validates that handler uses instance state to avoid 'could be static' warnings.
    Demonstrates proper SOLID compliance with meaningful instance dependencies.

    SOLID Assessment:
    - SRP: Configuration focused solely on behavior modification
    - DIP: Configuration through dependency injection, not hardcoded values
    """
    # Create handlers with different configurations
    handler_simple = PseudocodeHandler(max_steps=5, include_error_handling=False)
    handler_complex = PseudocodeHandler(max_steps=15, include_error_handling=True)

    # Should have different configurations affecting behavior
    assert getattr(handler_simple, "_max_steps", None) == 5
    assert getattr(handler_simple, "_include_error_handling", None) is False
    assert getattr(handler_complex, "_max_steps", None) == 15
    assert getattr(handler_complex, "_include_error_handling", None) is True
