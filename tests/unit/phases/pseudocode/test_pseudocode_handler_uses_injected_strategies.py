"""Test that handler uses dependency-injected strategies.

This test validates Dependency Inversion Principle - handler should use
injected strategies rather than hardcoded implementations.

SOLID Assessment:
- DIP: Handler depends on abstractions, accepts any compliant implementation
- OCP: New strategies can be injected without modifying handler
"""

from unittest.mock import Mock

from zenyth.phases.pseudocode import (
    AlgorithmAnalyzer,
    PseudocodeGenerator,
    PseudocodeHandler,
)


def test_pseudocode_handler_uses_injected_strategies() -> None:
    """Test that handler uses dependency-injected strategies.

    Validates Dependency Inversion Principle - handler should use
    injected strategies rather than hardcoded implementations.

    SOLID Assessment:
    - DIP: Handler depends on abstractions, accepts any compliant implementation
    - OCP: New strategies can be injected without modifying handler
    """
    # Create mock strategies
    mock_analyzer = Mock(spec=AlgorithmAnalyzer)
    mock_generator = Mock(spec=PseudocodeGenerator)

    # Inject strategies via constructor
    handler = PseudocodeHandler(
        algorithm_analyzer=mock_analyzer,
        pseudocode_generator=mock_generator,
    )

    # Should use injected strategies
    assert getattr(handler, "_algorithm_analyzer", None) is mock_analyzer
    assert getattr(handler, "_pseudocode_generator", None) is mock_generator
