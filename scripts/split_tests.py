#!/usr/bin/env python3
"""Script to split test files into single responsibility test files."""

import ast
import os
import re
from pathlib import Path
from typing import List, Tuple


def extract_tests_from_file(file_path: str) -> List[Tuple[str, str, str, List[str]]]:
    """Extract test functions from a Python file.
    
    Returns list of (test_name, docstring, test_code, imports) tuples.
    """
    with open(file_path, 'r') as f:
        content = f.read()
    
    tree = ast.parse(content)
    
    # Extract imports
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(f"import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                imports.append(f"from {module} import {alias.name}")
    
    # Extract test functions
    tests = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
            # Get function code
            start_line = node.lineno - 1
            end_line = node.end_lineno or start_line
            lines = content.split('\n')[start_line:end_line]
            test_code = '\n'.join(lines)
            
            # Get docstring
            docstring = ast.get_docstring(node) or ""
            
            tests.append((node.name, docstring, test_code, imports))
    
    return tests


def create_single_test_file(test_name: str, docstring: str, test_code: str, 
                          imports: List[str], output_dir: str) -> None:
    """Create a single test file for one test function."""
    # Create file content
    content_lines = ['"""' + docstring + '"""', '']
    
    # Add unique imports
    unique_imports = []
    for imp in imports:
        if imp not in unique_imports:
            # Filter out imports that are likely test-specific
            if 'zenyth' in imp or 'pytest' in imp:
                unique_imports.append(imp)
    
    content_lines.extend(sorted(unique_imports))
    content_lines.extend(['', '', test_code])
    
    # Write file
    file_path = os.path.join(output_dir, f"{test_name}.py")
    with open(file_path, 'w') as f:
        f.write('\n'.join(content_lines))
    
    print(f"Created: {file_path}")


def split_test_file(input_file: str, output_dir: str) -> None:
    """Split a test file into multiple single-test files."""
    os.makedirs(output_dir, exist_ok=True)
    
    tests = extract_tests_from_file(input_file)
    
    for test_name, docstring, test_code, imports in tests:
        create_single_test_file(test_name, docstring, test_code, imports, output_dir)
    
    print(f"\nSplit {len(tests)} tests from {input_file}")


# Split core/test_types.py
split_test_file(
    "/Users/stephen/Projects/rzp-labs/zenyth/tests/unit/core/test_types.py",
    "/Users/stephen/Projects/rzp-labs/zenyth/tests/unit/core/types"
)

# Split core/test_validation.py  
split_test_file(
    "/Users/stephen/Projects/rzp-labs/zenyth/tests/unit/core/test_validation.py",
    "/Users/stephen/Projects/rzp-labs/zenyth/tests/unit/core/validation"
)

# Split core/test_interfaces.py
split_test_file(
    "/Users/stephen/Projects/rzp-labs/zenyth/tests/unit/core/test_interfaces.py",
    "/Users/stephen/Projects/rzp-labs/zenyth/tests/unit/core/interfaces"
)