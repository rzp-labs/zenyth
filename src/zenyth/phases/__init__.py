"""Phase implementations for SPARC methodology.

This package contains all phase handler implementations following the
Open/Closed Principle - base abstractions are closed for modification
but open for extension through concrete phase implementations.
"""

from .architecture import (
    ArchitectureDiagrammer,
    ArchitectureHandler,
    BasicArchitectureDiagrammer,
    BasicSystemDesigner,
    SystemDesigner,
)
from .base import PhaseHandler
from .specification import (
    BasicRequirementsAnalyzer,
    BasicSpecificationGenerator,
    RequirementsAnalyzer,
    SpecificationGenerator,
    SpecificationHandler,
)

__all__ = [
    "ArchitectureDiagrammer",
    "ArchitectureHandler",
    "BasicArchitectureDiagrammer",
    "BasicRequirementsAnalyzer",
    "BasicSpecificationGenerator",
    "BasicSystemDesigner",
    "PhaseHandler",
    "RequirementsAnalyzer",
    "SpecificationGenerator",
    "SpecificationHandler",
    "SystemDesigner",
]
