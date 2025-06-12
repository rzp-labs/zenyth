"""Test BasicPseudocodeGenerator with verbosity_level='concise'.

This test validates the main conditional branch for concise output formatting.
"""

import pytest

from zenyth.phases.pseudocode import AlgorithmAnalysis, BasicPseudocodeGenerator


@pytest.mark.asyncio()
async def test_basic_pseudocode_generator_with_concise_verbosity() -> None:
    """Test BasicPseudocodeGenerator with verbosity_level='concise'.

    Tests the main conditional branch for concise output formatting.
    """
    generator = BasicPseudocodeGenerator(verbosity_level="concise", include_comments=False)
    task_description = "Simple API endpoint"
    analysis = AlgorithmAnalysis(
        logical_steps=["Validate input", "Process request"],
        data_structures=["Request"],
        control_flow=["validation"],
        complexity_estimate="low",
    )

    result = await generator.generate(task_description, analysis, "test-session")

    # Should use concise formatting without extra details
    logic_text = " ".join(result.step_by_step_logic)
    assert "1. Validate input" in logic_text  # Concise format
    assert "STEP 1:" not in logic_text  # Not verbose format
