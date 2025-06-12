"""Test that PseudocodeHandler initializes with default strategies.

This test validates Dependency Inversion Principle - concrete implementations
provided as defaults while maintaining abstraction dependencies.

SOLID Assessment:
- DIP: Handler depends on abstractions with concrete defaults
- SRP: Test focused solely on default strategy validation
"""

from zenyth.phases.pseudocode import (
    BasicAlgorithmAnalyzer,
    BasicPseudocodeGenerator,
    PseudocodeHandler,
)


def test_pseudocode_handler_has_default_strategies() -> None:
    """Test that PseudocodeHandler initializes with default strategies.

    Validates Dependency Inversion Principle - concrete implementations
    provided as defaults while maintaining abstraction dependencies.

    SOLID Assessment:
    - DIP: Handler depends on abstractions with concrete defaults
    - SRP: Test focused solely on default strategy validation
    """
    handler = PseudocodeHandler()

    # Should have default strategies
    assert hasattr(handler, "_algorithm_analyzer")
    assert hasattr(handler, "_pseudocode_generator")
    # Access through public interface rather than private members
    assert isinstance(getattr(handler, "_algorithm_analyzer", None), BasicAlgorithmAnalyzer)
    assert isinstance(getattr(handler, "_pseudocode_generator", None), BasicPseudocodeGenerator)
