"""Test that WorkflowResult has proper type annotations.

This test validates type safety and enables static analysis tools using proper
type introspection instead of fragile string-based checks.
"""

import typing
from typing import Union, get_args, get_origin

from zenyth.core.types import WorkflowResult


def test_workflow_result_type_annotations() -> None:
    """Test that WorkflowResult has proper type annotations."""
    # Get field type annotations
    annotations = WorkflowResult.__annotations__

    # Test exact type matches for simple types
    assert annotations["success"] is bool
    assert annotations["task"] is str

    # Test list type for phases_completed
    phases_type = annotations["phases_completed"]
    assert get_origin(phases_type) is list
    # The list contains PhaseResult (forward reference as string)
    args = get_args(phases_type)
    assert len(args) == 1
    assert args[0] == "PhaseResult"

    # Test dict type for artifacts
    artifacts_type = annotations["artifacts"]
    assert get_origin(artifacts_type) is dict
    artifacts_args = get_args(artifacts_type)
    assert len(artifacts_args) == 2
    assert artifacts_args[0] is str  # Key type
    assert artifacts_args[1] is typing.Any  # Value type

    # Test Union type for error (str | None)
    error_type = annotations["error"]
    # Handle both modern (str | None) and legacy (Union[str, None]) union syntax
    error_origin = get_origin(error_type)
    assert error_origin is Union or str(error_origin) == "<class 'types.UnionType'>"
    error_args = get_args(error_type)
    assert len(error_args) == 2
    assert str in error_args
    assert type(None) in error_args

    # Test dict type for metadata
    metadata_type = annotations["metadata"]
    assert get_origin(metadata_type) is dict
    metadata_args = get_args(metadata_type)
    assert len(metadata_args) == 2
    assert metadata_args[0] is str  # Key type
    assert metadata_args[1] is typing.Any  # Value type
