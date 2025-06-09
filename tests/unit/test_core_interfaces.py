#!/usr/bin/env python3
"""Core interface tests for Zenyth SPARC orchestration system.

These critical tests verify the fundamental interfaces and data models
that the entire system depends on. They run during pre-commit to catch
breaking changes early.
"""

import pytest
from enum import Enum
from typing import Any, Dict, List

# Test the core enums exist and have expected values
def test_sparc_phase_enum():
    """Test SPARCPhase enum values."""
    from zenyth.models import SPARCPhase
    
    # Verify all expected phases exist
    expected_phases = [
        "specification", "pseudocode", "architecture", 
        "refinement", "completion", "validation", "integration"
    ]
    
    for phase in expected_phases:
        assert hasattr(SPARCPhase, phase.upper())
        assert getattr(SPARCPhase, phase.upper()).value == phase


def test_phase_transition_trigger_enum():
    """Test PhaseTransitionTrigger enum values."""
    from zenyth.models import PhaseTransitionTrigger
    
    expected_triggers = [
        "complete", "incomplete", "needs_revision", 
        "blocked", "manual_override"
    ]
    
    for trigger in expected_triggers:
        assert hasattr(PhaseTransitionTrigger, trigger.upper())


def test_tool_permission_enum():
    """Test ToolPermission enum values."""
    from zenyth.models import ToolPermission
    
    expected_permissions = ["read_only", "write", "execute", "none"]
    
    for permission in expected_permissions:
        assert hasattr(ToolPermission, permission.upper())


def test_phase_config_model():
    """Test PhaseConfig model can be instantiated."""
    from zenyth.models import PhaseConfig, SPARCPhase
    
    config = PhaseConfig(
        name=SPARCPhase.SPECIFICATION,
        description="Test phase",
        instructions="Test instructions"
    )
    
    assert config.name == SPARCPhase.SPECIFICATION
    assert config.description == "Test phase"
    assert config.max_retries == 3  # Default value
    assert config.cache_responses is True  # Default value


def test_session_context_model():
    """Test SessionContext model functionality."""
    from zenyth.models import SessionContext, SPARCPhase
    
    context = SessionContext(
        workflow_id="test-workflow",
        current_phase=SPARCPhase.SPECIFICATION,
        task_description="Test task"
    )
    
    assert context.workflow_id == "test-workflow"
    assert context.current_phase == SPARCPhase.SPECIFICATION
    assert len(context.phase_history) == 0
    assert isinstance(context.session_id, type(context.session_id))  # UUID type


def test_phase_result_model():
    """Test PhaseResult model."""
    from zenyth.models import PhaseResult, SPARCPhase, PhaseTransitionTrigger
    
    result = PhaseResult(
        phase=SPARCPhase.SPECIFICATION,
        status=PhaseTransitionTrigger.COMPLETE,
        execution_time_seconds=45.2
    )
    
    assert result.phase == SPARCPhase.SPECIFICATION
    assert result.status == PhaseTransitionTrigger.COMPLETE
    assert result.execution_time_seconds == 45.2
    assert len(result.artifacts) == 0  # Default empty list


def test_workflow_config_model():
    """Test WorkflowConfig model."""
    from zenyth.models import WorkflowConfig, PhaseConfig, SPARCPhase
    
    phase_config = PhaseConfig(
        name=SPARCPhase.SPECIFICATION,
        description="Test spec phase",
        instructions="Test instructions"
    )
    
    workflow = WorkflowConfig(
        name="test-workflow",
        description="Test workflow",
        phases={SPARCPhase.SPECIFICATION: phase_config},
        transitions={"specification": {"architecture": {"condition": "complete"}}}
    )
    
    assert workflow.name == "test-workflow"
    assert SPARCPhase.SPECIFICATION in workflow.phases
    assert workflow.enable_checkpointing is True  # Default


def test_orchestration_metrics_model():
    """Test OrchestrationMetrics model."""
    from zenyth.models import OrchestrationMetrics
    
    metrics = OrchestrationMetrics()
    
    assert metrics.total_llm_calls == 0
    assert metrics.total_tool_calls == 0
    assert metrics.memory_peak_mb == 0.0
    assert isinstance(metrics.phase_durations, dict)


# Integration test stubs (will be expanded as implementation grows)
def test_phase_context_filtering():
    """Test that SessionContext properly filters context per phase."""
    from zenyth.models import SessionContext, SPARCPhase
    
    context = SessionContext(
        workflow_id="test",
        current_phase=SPARCPhase.ARCHITECTURE,
        task_description="Build API"
    )
    
    # Test that get_phase_context returns appropriate structure
    phase_context = context.get_phase_context(SPARCPhase.ARCHITECTURE)
    
    assert "task" in phase_context
    assert "current_phase" in phase_context
    assert "session_id" in phase_context
    assert phase_context["current_phase"] == "architecture"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])