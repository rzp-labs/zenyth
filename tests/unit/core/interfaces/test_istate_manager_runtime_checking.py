"""Test IStateManager runtime protocol checking.

This test validates that the IStateManager protocol correctly performs runtime
type checking, ensuring that implementations honor the protocol contract in
accordance with the Liskov Substitution Principle.
"""

from zenyth.core.interfaces import IStateManager
from zenyth.core.types import SessionContext


def test_istate_manager_runtime_checking() -> None:
    """Test IStateManager runtime protocol checking.

    Validates Liskov Substitution - implementations must honor protocol contract.
    Tests that implementations with correct methods pass runtime checks.
    """

    # Create correct implementation with instance state
    class ValidStateManager:
        def __init__(self) -> None:
            self.sessions: dict[str, SessionContext] = {}

        async def load_session(self, session_id: str) -> SessionContext:
            return self.sessions.get(session_id, SessionContext(session_id=session_id, task="test"))

        async def save_session(self, session: SessionContext) -> None:
            self.sessions[session.session_id] = session

    # Create incorrect implementation (missing method)
    class InvalidStateManager:
        async def save_session(self, session: SessionContext) -> None:
            pass

        # Missing load_session method

    valid_manager = ValidStateManager()
    invalid_manager = InvalidStateManager()

    # Runtime checking should work correctly
    assert isinstance(valid_manager, IStateManager)
    assert not isinstance(invalid_manager, IStateManager)
