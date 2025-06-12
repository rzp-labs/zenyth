"""Test BasicAlgorithmAnalyzer with include_edge_cases=False.

This test validates the main conditional branch when edge cases are disabled.
"""

import pytest

from zenyth.phases.pseudocode import BasicAlgorithmAnalyzer


@pytest.mark.asyncio()
async def test_basic_algorithm_analyzer_with_include_edge_cases_false() -> None:
    """Test BasicAlgorithmAnalyzer with include_edge_cases=False.

    Tests the main conditional branch when edge cases are disabled.
    """
    analyzer = BasicAlgorithmAnalyzer(include_edge_cases=False)
    task_description = "Build user authentication system"
    context = {"complexity": "medium"}

    result = await analyzer.analyze(task_description, context)

    # Should not include edge case steps when disabled
    steps_text = " ".join(result.logical_steps).lower()
    assert "error conditions" not in steps_text or "edge cases" not in steps_text
