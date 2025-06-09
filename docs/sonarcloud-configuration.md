# SonarCloud Configuration for Zenyth

This document explains the SonarCloud configuration for the Zenyth project, including file exclusions and analysis scope.

## Configuration Files

### `sonar-project.properties`
Primary configuration file for SonarCloud analysis with project metadata and exclusion patterns.

### `.sonarcloud.properties`
GitHub Actions integration file automatically detected by SonarCloud scanner.

## File Exclusion Strategy

### Build and Distribution Artifacts
- `**/__pycache__/**` - Python bytecode cache
- `**/*.pyc`, `**/*.pyo` - Compiled Python files
- `**/*.egg-info/**` - Python package metadata
- `**/build/**`, `**/dist/**` - Build artifacts

### Development Environment
- `**/.venv/**`, `**/venv/**`, `**/env/**` - Virtual environments
- `**/.tox/**` - Tox testing environments
- `**/.pytest_cache/**` - Pytest cache

### IDE and Editor Files
- `**/.vscode/**`, `**/.idea/**` - IDE configuration
- `**/*.swp`, `**/*.swo`, `**/*~` - Editor temporary files

### Generated Files
- `**/htmlcov/**` - Coverage reports
- `**/.coverage`, `**/coverage.xml` - Coverage data
- `**/.mypy_cache/**`, `**/.ruff_cache/**` - Type checker and linter caches

### Database and Migration Files
- `**/*.db`, `**/*.sqlite`, `**/*.sqlite3` - SQLite databases
- `**/alembic/versions/**` - Database migration files

### Configuration and Secrets
- `**/.secrets.baseline` - Security baseline
- `**/.mcp.json` - MCP configuration
- `**/*.env`, `**/.env.*` - Environment variables

### Examples and Mock Files
- `**/examples/**` - Example code (not production)
- `**/mocks/**` - Mock implementations for testing

### Third-party Dependencies
- `**/node_modules/**` - Node.js dependencies
- `**/vendor/**` - Vendored dependencies

## Coverage Analysis Exclusions

Files excluded from coverage analysis but still analyzed for other quality metrics:

- Test files (`**/test_*.py`, `**/*_test.py`, `**/tests/**`)
- Mock implementations (`**/mocks/**`)
- Example code (`**/examples/**`)
- CLI entry points (`**/__main__.py`)
- Database migrations (`**/alembic/**`)
- Development scripts (`**/scripts/**`)

## Duplicate Code Analysis Exclusions

Test files are excluded from duplicate code detection since test patterns naturally repeat:

- `**/test_*.py`
- `**/*_test.py`
- `**/tests/**`
- `**/conftest.py`

## Project-Specific Considerations

### SPARC Orchestration
The project uses SPARC methodology with phase-based execution. Mock implementations in `src/zenyth/mocks/` are excluded as they're for testing infrastructure, not production code.

### MCP Integration
MCP (Model Context Protocol) configuration files are excluded as they contain environment-specific settings that shouldn't affect code quality metrics.

### Homelab Focus
As a homelab automation tool, certain files like migration scripts and example configurations are excluded since they're deployment artifacts rather than core application logic.

## Quality Gates

SonarCloud will analyze:
- Source code in `src/zenyth/` (excluding mocks)
- Test quality and coverage
- Code smells and maintainability
- Security vulnerabilities
- Duplication in production code

## Troubleshooting

If files are still being analyzed despite exclusions:

1. Check the exact path format in SonarCloud logs
2. Verify wildcard patterns match your file structure
3. Use forward slashes (`/`) in patterns regardless of OS
4. Test patterns with double asterisks (`**`) for directory traversal

## Integration with CI/CD

The `.sonarcloud.properties` file is automatically detected by SonarCloud GitHub Actions. No additional configuration is needed in the workflow file beyond specifying the token.

Example GitHub Actions step:
```yaml
- name: SonarCloud Scan
  uses: SonarSource/sonarcloud-github-action@master
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```