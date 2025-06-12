"""Test that WorkflowResult is immutable after creation.

This test validates Open/Closed principle - closed for modification after creation.
Ensures thread-safety and data integrity in concurrent environments.
"""

from dataclasses import FrozenInstanceError

import pytest

from zenyth.core.types import WorkflowResult


def test_workflow_result_immutability() -> None:
    """Test that WorkflowResult is immutable after creation."""
    result = WorkflowResult(success=True, task="Test task", artifacts={"test": "data"})

    # Should not be able to modify any attributes
    with pytest.raises(
        (AttributeError, FrozenInstanceError),
        match=r"can't set attribute|cannot assign to field",
    ):
        result.success = False

    with pytest.raises(
        (AttributeError, FrozenInstanceError),
        match=r"can't set attribute|cannot assign to field",
    ):
        result.task = "Modified task"
