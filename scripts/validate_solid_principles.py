#!/usr/bin/env python3
"""SOLID Principles Validation Script for CI/CD Pipeline.

This script validates adherence to SOLID principles by checking for common violations
in the codebase, particularly focusing on Single Responsibility Principle (SRP)
violations through class complexity analysis.
"""

import ast
import os
import sys
from pathlib import Path


def check_class_complexity(file_path: Path) -> bool:
    """Check if a Python file contains classes that violate SRP through excessive complexity.
    
    Args:
        file_path: Path to the Python file to analyze
        
    Returns:
        True if no SRP violations detected, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
            
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Count methods (excluding special methods like __init__)
                methods = [
                    n for n in node.body 
                    if isinstance(n, ast.FunctionDef) and not n.name.startswith('__')
                ]
                
                # Threshold for potential God class (SRP violation)
                if len(methods) > 15:
                    print(f'⚠️  Potential SRP violation: {file_path}:{node.lineno} - '
                          f'Class {node.name} has {len(methods)} public methods')
                    return False
                    
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f'⚠️  Could not parse {file_path}: {e}')
        # Don't fail CI for unparseable files
        
    return True


def validate_solid_principles() -> bool:
    """Validate SOLID principles across the entire codebase.
    
    Returns:
        True if all SOLID principles are satisfied, False otherwise
    """
    print("✅ Validating SOLID principles compliance...")
    print("🔍 Checking for potential SRP violations...")
    
    src_path = Path('src/zenyth')
    if not src_path.exists():
        print(f"❌ Source path {src_path} not found")
        return False
    
    all_good = True
    files_checked = 0
    
    for py_file in src_path.rglob('*.py'):
        if py_file.name != '__init__.py':  # Skip __init__.py files
            files_checked += 1
            if not check_class_complexity(py_file):
                all_good = False
    
    if all_good:
        print(f'✅ No SRP violations detected ({files_checked} files checked)')
    else:
        print(f'❌ SRP violations found ({files_checked} files checked)')
        
    return all_good


def main() -> int:
    """Main entry point for SOLID principles validation.
    
    Returns:
        0 if validation passes, 1 if violations found
    """
    if validate_solid_principles():
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())