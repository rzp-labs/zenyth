"""Test that BasicAlgorithmAnalyzer properly identifies algorithmic steps.

This test validates core analysis functionality with proper step identification.

SOLID Assessment:
- SRP: Analyzer focused solely on step identification logic
- OCP: Analysis logic extensible through configuration
"""

import pytest

from zenyth.phases.pseudocode import AlgorithmAnalysis, BasicAlgorithmAnalyzer


@pytest.mark.asyncio()
async def test_basic_algorithm_analyzer_analyze_identifies_steps() -> None:
    """Test that BasicAlgorithmAnalyzer properly identifies algorithmic steps.

    Validates core analysis functionality with proper step identification.

    SOLID Assessment:
    - SRP: Analyzer focused solely on step identification logic
    - OCP: Analysis logic extensible through configuration
    """
    analyzer = BasicAlgorithmAnalyzer()
    task_description = "Implement user login validation with error handling"
    context = {"existing_auth": "JWT tokens"}

    result = await analyzer.analyze(task_description, context)

    # Should return AlgorithmAnalysis with identified steps
    assert isinstance(result, AlgorithmAnalysis)
    assert len(result.logical_steps) > 0
    assert len(result.data_structures) >= 0
    assert result.complexity_estimate in {"low", "medium", "high"}

    # Should identify key steps from task description
    steps_text = " ".join(result.logical_steps).lower()
    assert {"login", "validation"} & set(steps_text.split())
