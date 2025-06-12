"""Test algorithm analysis with database-specific task.

This test validates the main conditional branch for database-related tasks.
"""

import pytest

from zenyth.phases.pseudocode import BasicAlgorithmAnalyzer


@pytest.mark.asyncio()
async def test_algorithm_analyzer_with_database_task() -> None:
    """Test algorithm analysis with database-specific task.

    Tests the main conditional branch for database-related tasks.
    """
    analyzer = BasicAlgorithmAnalyzer()
    task_description = "Build database connection pool manager"
    context = {"scale": "large"}

    result = await analyzer.analyze(task_description, context)

    # Should identify database-specific steps and structures
    steps_text = " ".join(result.logical_steps).lower()
    assert "database" in steps_text or "connection" in steps_text
    structures_text = " ".join(result.data_structures).lower()
    assert "connection" in structures_text
