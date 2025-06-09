"""Core data models for Zenyth orchestration system.

Based on homelab practitioner patterns, these models prioritize:
- Explicit type safety with Pydantic
- Serialization support for session persistence
- Clear separation between phases and workflows
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict


class SPARCPhase(str, Enum):
    """SPARC methodology phases."""
    
    SPECIFICATION = "specification"
    PSEUDOCODE = "pseudocode"
    ARCHITECTURE = "architecture"
    REFINEMENT = "refinement"
    COMPLETION = "completion"
    
    # Additional phases observed in homelab implementations
    VALIDATION = "validation"
    INTEGRATION = "integration"


class PhaseTransitionTrigger(str, Enum):
    """Events that can trigger phase transitions."""
    
    COMPLETE = "complete"
    INCOMPLETE = "incomplete"
    NEEDS_REVISION = "needs_revision"
    BLOCKED = "blocked"
    MANUAL_OVERRIDE = "manual_override"


class ToolPermission(str, Enum):
    """Tool permission levels per phase."""
    
    READ_ONLY = "read_only"
    WRITE = "write"
    EXECUTE = "execute"
    NONE = "none"


class PhaseConfig(BaseModel):
    """Configuration for a single SPARC phase."""
    
    model_config = ConfigDict(extra="allow")
    
    name: SPARCPhase
    description: str
    instructions: str  # Prompt template for the phase
    allowed_tools: List[str] = Field(default_factory=list)
    forbidden_tools: List[str] = Field(default_factory=list)
    required_artifacts: List[str] = Field(default_factory=list)
    completion_criteria: Dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: Optional[int] = None
    max_retries: int = 3
    
    # Homelab-specific optimizations
    cache_responses: bool = True
    allow_human_override: bool = True


class PhaseArtifact(BaseModel):
    """Artifact produced by a phase execution."""
    
    name: str
    content: Any  # Can be string, dict, list, etc.
    mime_type: str = "text/plain"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PhaseResult(BaseModel):
    """Result of executing a single phase."""
    
    phase: SPARCPhase
    status: PhaseTransitionTrigger
    artifacts: List[PhaseArtifact] = Field(default_factory=list)
    next_phase: Optional[SPARCPhase] = None
    execution_time_seconds: float
    llm_calls: int = 0
    tool_calls: int = 0
    error: Optional[str] = None
    
    # Homelab patterns: comprehensive logging
    logs: List[str] = Field(default_factory=list)
    metrics: Dict[str, float] = Field(default_factory=dict)


class SessionContext(BaseModel):
    """Context preserved across phase transitions."""
    
    session_id: UUID = Field(default_factory=uuid4)
    workflow_id: str
    current_phase: SPARCPhase
    task_description: str
    phase_history: List[PhaseResult] = Field(default_factory=list)
    global_artifacts: Dict[str, Any] = Field(default_factory=dict)
    
    # Homelab optimization: selective context
    active_tools: Set[str] = Field(default_factory=set)
    llm_context_window: int = 8192
    
    def get_phase_context(self, phase: SPARCPhase) -> Dict[str, Any]:
        """Get relevant context for a specific phase.
        
        Based on practitioner feedback: phases don't need all historical context,
        just relevant artifacts from dependent phases.
        """
        context = {
            "task": self.task_description,
            "current_phase": phase.value,
            "session_id": str(self.session_id),
        }
        
        # Add relevant artifacts based on phase dependencies
        if phase == SPARCPhase.ARCHITECTURE:
            # Architecture needs specification
            spec_results = [r for r in self.phase_history if r.phase == SPARCPhase.SPECIFICATION]
            if spec_results:
                context["specification"] = spec_results[-1].artifacts
                
        elif phase == SPARCPhase.REFINEMENT:
            # Refinement needs architecture and code
            for needed_phase in [SPARCPhase.ARCHITECTURE, SPARCPhase.COMPLETION]:
                results = [r for r in self.phase_history if r.phase == needed_phase]
                if results:
                    context[needed_phase.value] = results[-1].artifacts
        
        # Add global artifacts
        context["global_artifacts"] = self.global_artifacts
        
        return context


class WorkflowConfig(BaseModel):
    """Configuration for an entire SPARC workflow."""
    
    name: str
    description: str
    phases: Dict[SPARCPhase, PhaseConfig]
    transitions: Dict[str, Dict[str, Any]]  # Phase transition rules
    
    # Homelab patterns
    allow_phase_skip: bool = False
    enable_checkpointing: bool = True
    checkpoint_storage: str = "file"  # file, redis, postgres
    
    def get_valid_transitions(self, from_phase: SPARCPhase) -> List[SPARCPhase]:
        """Get valid next phases from current phase."""
        if from_phase.value not in self.transitions:
            return []
        
        return [
            SPARCPhase(to_phase)
            for to_phase in self.transitions[from_phase.value].keys()
        ]


class OrchestrationMetrics(BaseModel):
    """Metrics for monitoring orchestration performance."""
    
    total_llm_calls: int = 0
    total_tool_calls: int = 0
    total_execution_time: float = 0.0
    phase_durations: Dict[str, float] = Field(default_factory=dict)
    cache_hits: int = 0
    cache_misses: int = 0
    retry_counts: Dict[str, int] = Field(default_factory=dict)
    
    # Homelab-specific metrics
    memory_peak_mb: float = 0.0
    cpu_peak_percent: float = 0.0
    mcp_connection_failures: int = 0
