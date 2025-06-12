"""Test BasicPseudocodeGenerator with verbosity_level='verbose'.

This test validates the main conditional branch for verbose output formatting.
"""

import pytest

from zenyth.phases.pseudocode import AlgorithmAnalysis, BasicPseudocodeGenerator


@pytest.mark.asyncio()
async def test_basic_pseudocode_generator_with_verbose_verbosity() -> None:
    """Test BasicPseudocodeGenerator with verbosity_level='verbose'.

    Tests the main conditional branch for verbose output formatting.
    """
    generator = BasicPseudocodeGenerator(verbosity_level="verbose", include_comments=True)
    task_description = "Create database API"
    analysis = AlgorithmAnalysis(
        logical_steps=["Connect to database", "Execute query", "Process results"],
        data_structures=["Connection", "ResultSet"],
        control_flow=["exception-handling"],
        complexity_estimate="medium",
    )

    result = await generator.generate(task_description, analysis, "test-session")

    # Should include verbose formatting and data structure declarations
    logic_text = " ".join(result.step_by_step_logic)
    assert "DECLARE" in logic_text  # Verbose mode includes data structure setup
    assert "// Data Structure Initialization" in logic_text
