"""Test that PseudocodeDocument is properly immutable.

This test validates immutable data container following functional programming principles.

SOLID Assessment:
- SRP: Data container focused solely on holding document structure
- OCP: Immutable structure prevents accidental modification
"""

import pytest

from zenyth.phases.pseudocode import AlgorithmAnalysis, PseudocodeDocument


def test_pseudocode_document_immutability() -> None:
    """Test that PseudocodeDocument is properly immutable.

    Validates immutable data container following functional programming principles.

    SOLID Assessment:
    - SRP: Data container focused solely on holding document structure
    - OCP: Immutable structure prevents accidental modification
    """
    analysis = AlgorithmAnalysis(
        logical_steps=["Step 1"],
        data_structures=["Data"],
        control_flow=["flow"],
        complexity_estimate="low",
    )

    document = PseudocodeDocument(
        overview="Test overview",
        algorithm_analysis=analysis,
        step_by_step_logic=["Logic step 1"],
        next_phase_recommendations=["Proceed to architecture"],
    )

    # Should be frozen/immutable
    try:
        document.overview = "Modified overview"
        # If we reach here, the dataclass is not properly frozen
        pytest.fail("Should not allow modification of frozen dataclass")
    except AttributeError:
        # This is expected behavior for frozen dataclass
        pass
