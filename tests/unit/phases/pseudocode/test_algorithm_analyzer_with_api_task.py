"""Test algorithm analysis with API-specific task.

This test validates the main conditional branch for API-related tasks.
"""

import pytest

from zenyth.phases.pseudocode import BasicAlgorithmAnalyzer


@pytest.mark.asyncio()
async def test_algorithm_analyzer_with_api_task() -> None:
    """Test algorithm analysis with API-specific task.

    Tests the main conditional branch for API-related tasks.
    """
    analyzer = BasicAlgorithmAnalyzer()
    task_description = "Create REST API endpoint for user management"
    context = {"flow_type": "parallel"}

    result = await analyzer.analyze(task_description, context)

    # Should identify API-specific steps and structures
    steps_text = " ".join(result.logical_steps).lower()
    assert "request" in steps_text or "validate" in steps_text
    structures_text = " ".join(result.data_structures).lower()
    assert "request" in structures_text
    assert "response" in structures_text
