"""Test that AlgorithmAnalysis is properly immutable.

This test validates immutable data container following functional programming principles.

SOLID Assessment:
- SRP: Data container focused solely on holding analysis results
- OCP: Immutable structure prevents accidental modification
"""

import pytest

from zenyth.phases.pseudocode import AlgorithmAnalysis


def test_algorithm_analysis_immutability() -> None:
    """Test that AlgorithmAnalysis is properly immutable.

    Validates immutable data container following functional programming principles.

    SOLID Assessment:
    - SRP: Data container focused solely on holding analysis results
    - OCP: Immutable structure prevents accidental modification
    """
    analysis = AlgorithmAnalysis(
        logical_steps=["Step 1", "Step 2"],
        data_structures=["List", "Dict"],
        control_flow=["loop", "condition"],
        complexity_estimate="low",
    )

    # Should be frozen/immutable
    try:
        analysis.logical_steps = ["Modified"]
        # If we reach here, the dataclass is not properly frozen
        pytest.fail("Should not allow modification of frozen dataclass")
    except AttributeError:
        # This is expected behavior for frozen dataclass
        pass
