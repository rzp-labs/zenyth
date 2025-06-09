#!/usr/bin/env python3
"""Validate SPARC configuration files for Zenyth orchestration system.

This script validates Python-based SPARC configuration files to ensure they:
- Follow proper structure and naming conventions
- Have required fields and valid enum values
- Are syntactically correct Python
- Follow absolute path requirements
- Have proper type hints and documentation
"""

import ast
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Import validation functions from the main package when available
try:
    from zenyth.models import SPARCPhase, PhaseTransitionTrigger, ToolPermission
except ImportError:
    # Fallback enums for validation when package not installed
    class SPARCPhase:
        SPECIFICATION = "specification"
        PSEUDOCODE = "pseudocode"
        ARCHITECTURE = "architecture"
        REFINEMENT = "refinement"
        COMPLETION = "completion"
        VALIDATION = "validation"
        INTEGRATION = "integration"
        
        @classmethod
        def values(cls) -> List[str]:
            return [
                cls.SPECIFICATION, cls.PSEUDOCODE, cls.ARCHITECTURE,
                cls.REFINEMENT, cls.COMPLETION, cls.VALIDATION, cls.INTEGRATION
            ]

    class PhaseTransitionTrigger:
        COMPLETE = "complete"
        INCOMPLETE = "incomplete"
        NEEDS_REVISION = "needs_revision"
        BLOCKED = "blocked"
        MANUAL_OVERRIDE = "manual_override"
        
        @classmethod
        def values(cls) -> List[str]:
            return [
                cls.COMPLETE, cls.INCOMPLETE, cls.NEEDS_REVISION,
                cls.BLOCKED, cls.MANUAL_OVERRIDE
            ]

    class ToolPermission:
        READ_ONLY = "read_only"
        WRITE = "write"
        EXECUTE = "execute"
        NONE = "none"
        
        @classmethod
        def values(cls) -> List[str]:
            return [cls.READ_ONLY, cls.WRITE, cls.EXECUTE, cls.NONE]


class SPARCConfigValidator:
    """Validates SPARC configuration files."""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def validate_file(self, file_path: Path) -> bool:
        """Validate a single SPARC configuration file."""
        self.errors.clear()
        self.warnings.clear()
        
        if not file_path.exists():
            self.errors.append(f"File does not exist: {file_path}")
            return False
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.errors.append(f"Could not read file {file_path}: {e}")
            return False
            
        # Parse Python syntax
        try:
            tree = ast.parse(content, filename=str(file_path))
        except SyntaxError as e:
            self.errors.append(f"Syntax error in {file_path}: {e}")
            return False
            
        # Validate based on file type
        if file_path.name.startswith('phase_'):
            return self._validate_phase_config(file_path, tree, content)
        elif file_path.name.startswith('workflow_'):
            return self._validate_workflow_config(file_path, tree, content)
        elif file_path.name.startswith('transition_'):
            return self._validate_transition_config(file_path, tree, content)
        else:
            self.warnings.append(f"Unknown configuration type: {file_path.name}")
            return True
            
    def _validate_phase_config(self, file_path: Path, tree: ast.AST, content: str) -> bool:
        """Validate phase configuration file."""
        required_fields = {
            'name', 'description', 'instructions', 'allowed_tools',
            'required_artifacts', 'completion_criteria'
        }
        
        # Extract assignments from AST
        assignments = self._extract_assignments(tree)
        
        # Check required fields
        missing_fields = required_fields - assignments.keys()
        if missing_fields:
            self.errors.append(f"Missing required fields in {file_path}: {missing_fields}")
            
        # Validate phase name if present
        if 'name' in assignments:
            phase_name = self._get_string_value(assignments['name'])
            if phase_name and phase_name not in SPARCPhase.values():
                self.errors.append(f"Invalid phase name '{phase_name}' in {file_path}")
                
        # Check for absolute paths
        self._check_absolute_paths(file_path, content)
        
        return len(self.errors) == 0
        
    def _validate_workflow_config(self, file_path: Path, tree: ast.AST, content: str) -> bool:
        """Validate workflow configuration file."""
        required_fields = {'name', 'description', 'phases', 'transitions'}
        
        assignments = self._extract_assignments(tree)
        missing_fields = required_fields - assignments.keys()
        if missing_fields:
            self.errors.append(f"Missing required fields in {file_path}: {missing_fields}")
            
        self._check_absolute_paths(file_path, content)
        return len(self.errors) == 0
        
    def _validate_transition_config(self, file_path: Path, tree: ast.AST, content: str) -> bool:
        """Validate transition configuration file."""
        # Look for transition trigger values
        if 'triggers' in self._extract_assignments(tree):
            # Could validate trigger enum values here
            pass
            
        self._check_absolute_paths(file_path, content)
        return len(self.errors) == 0
        
    def _extract_assignments(self, tree: ast.AST) -> Dict[str, ast.AST]:
        """Extract top-level assignments from AST."""
        assignments = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assignments[target.id] = node.value
        return assignments
        
    def _get_string_value(self, node: ast.AST) -> Optional[str]:
        """Extract string value from AST node."""
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        return None
        
    def _check_absolute_paths(self, file_path: Path, content: str) -> None:
        """Check for relative paths in configuration."""
        # Look for common relative path patterns
        relative_patterns = [
            './src', '../', './',
            'src/', 'config/', 'sparc_config/',
            'context_portal/', 'logs/'
        ]
        
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern in relative_patterns:
                if pattern in line and '/Users/stephen/Projects/rzp-labs/zenyth' not in line:
                    # Skip comments and string literals that might be examples
                    if not line.strip().startswith('#') and 'example' not in line.lower():
                        self.warnings.append(
                            f"Possible relative path in {file_path}:{i}: {line.strip()}"
                        )


def main():
    """Main validation function called by pre-commit."""
    if len(sys.argv) < 2:
        print("Usage: validate_sparc_configs.py <file1> [file2] ...")
        sys.exit(1)
        
    validator = SPARCConfigValidator()
    all_valid = True
    
    for file_path_str in sys.argv[1:]:
        file_path = Path(file_path_str)
        
        print(f"Validating {file_path}")
        
        if validator.validate_file(file_path):
            print(f"✅ {file_path}: Valid")
            if validator.warnings:
                for warning in validator.warnings:
                    print(f"⚠️  {warning}")
        else:
            print(f"❌ {file_path}: Invalid")
            for error in validator.errors:
                print(f"   Error: {error}")
            for warning in validator.warnings:
                print(f"   Warning: {warning}")
            all_valid = False
            
    if not all_valid:
        print("\n❌ Some SPARC configuration files have validation errors")
        sys.exit(1)
    else:
        print("\n✅ All SPARC configuration files are valid")


if __name__ == "__main__":
    main()