"""Test that BasicPseudocodeGenerator creates proper pseudocode document.

This test validates core generation functionality with structured output.

SOLID Assessment:
- SRP: Generator focused solely on document structure creation
- OCP: Document format extensible through configuration
"""

import pytest

from zenyth.phases.pseudocode import (
    AlgorithmAnalysis,
    BasicPseudocodeGenerator,
    PseudocodeDocument,
)


@pytest.mark.asyncio()
async def test_basic_pseudocode_generator_creates_document() -> None:
    """Test that BasicPseudocodeGenerator creates proper pseudocode document.

    Validates core generation functionality with structured output.

    SOLID Assessment:
    - SRP: Generator focused solely on document structure creation
    - OCP: Document format extensible through configuration
    """
    generator = BasicPseudocodeGenerator()
    task_description = "Build user authentication API"
    analysis = AlgorithmAnalysis(
        logical_steps=["Validate input", "Check credentials", "Generate token"],
        data_structures=["User", "Token", "Session"],
        control_flow=["if-else", "try-catch"],
        complexity_estimate="medium",
    )
    session_id = "generator-test-session"

    result = await generator.generate(task_description, analysis, session_id)

    # Should return PseudocodeDocument with proper structure
    assert isinstance(result, PseudocodeDocument)
    assert len(result.overview) > 0
    assert len(result.algorithm_analysis.logical_steps) > 0
    assert len(result.step_by_step_logic) > 0
    assert result.algorithm_analysis.complexity_estimate == "medium"

    # Should incorporate task information
    overview_lower = result.overview.lower()
    assert "authentication" in overview_lower or "api" in overview_lower
