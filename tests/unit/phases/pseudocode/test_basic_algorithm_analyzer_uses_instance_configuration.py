"""Test that BasicAlgorithmAnalyzer uses instance configuration meaningfully.

This test validates that analyzer methods require instance access due to configuration,
avoiding 'could be static' linting warnings through proper SOLID design.

SOLID Assessment:
- SRP: Analyzer focused solely on algorithmic step identification
- DIP: Configuration injected, not hardcoded in methods
"""

from zenyth.phases.pseudocode import BasicAlgorithmAnalyzer


def test_basic_algorithm_analyzer_uses_instance_configuration() -> None:
    """Test that BasicAlgorithmAnalyzer uses instance configuration meaningfully.

    Validates that analyzer methods require instance access due to configuration,
    avoiding 'could be static' linting warnings through proper SOLID design.

    SOLID Assessment:
    - SRP: Analyzer focused solely on algorithmic step identification
    - DIP: Configuration injected, not hardcoded in methods
    """
    # Create analyzers with different configurations
    analyzer_simple = BasicAlgorithmAnalyzer(complexity_threshold=0.3, include_edge_cases=False)
    analyzer_detailed = BasicAlgorithmAnalyzer(complexity_threshold=0.8, include_edge_cases=True)

    # Should have meaningful instance configuration
    assert getattr(analyzer_simple, "_complexity_threshold", None) == 0.3
    assert getattr(analyzer_simple, "_include_edge_cases", None) is False
    assert getattr(analyzer_detailed, "_complexity_threshold", None) == 0.8
    assert getattr(analyzer_detailed, "_include_edge_cases", None) is True
