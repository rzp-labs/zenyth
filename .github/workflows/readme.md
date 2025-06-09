# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the Zenyth project's CI/CD pipeline.

## Workflows

### `sonarcloud.yml` - Code Quality Analysis
Comprehensive code quality analysis using SonarCloud, including:
- Test execution with coverage
- Security scanning
- Quality metrics collection
- Automated reporting

### `quality-gate.yml` - Quality Gate Enforcement  
Enforces quality standards on pull requests:
- Code formatting (Black)
- Linting (Ruff)
- Type checking (MyPy)
- Security analysis (Bandit)
- Test coverage (≥80%)
- SOLID principles validation

## Setup Required

1. Add `SONAR_TOKEN` to repository secrets
2. Configure branch protection rules
3. Review workflow permissions

See `docs/github-actions-setup.md` for detailed setup instructions.