"""Test SessionContext stores artifacts field when provided.

This test validates that SessionContext properly accepts and stores artifacts
information when provided during initialization.
"""

from zenyth.core.types import SessionContext


def test_session_context_stores_artifacts_when_provided() -> None:
    """Test SessionContext stores artifacts field when provided."""
    artifacts = {"spec": "requirement"}
    context = SessionContext(session_id="test", task="test", artifacts=artifacts)
    assert context.artifacts == artifacts

