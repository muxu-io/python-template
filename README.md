# CI/CD Template for Python MQTT Projects

This template provides GitHub Actions workflows for Python projects with MQTT integration.

## Usage

1. Copy the `.github/` and `.ci/` directories to your project root
2. Ensure your project has the following files:
   - `requirements.txt` - Python dependencies
   - `setup.py` or `pyproject.toml` - Package configuration
   - `tests/` directory with pytest tests
   - `src/` directory with source code

## Workflows Included

### Default Workflow (Pull Requests)
- **Commit validation** - Enforces conventional commit messages
- **Code quality** - Black formatting, Ruff linting, Bandit security scanning
- **Vulnerability scanning** - pip-audit and TruffleHog secret detection
- **Testing** - Multi-version Python testing (3.8-3.12) with MQTT broker
- **Build validation** - Package building and verification

### Release Workflow (Main Branch)
- **Semantic release** - Automated versioning and GitHub releases
- **Package publishing** - Build artifacts and optional PyPI publishing

## Requirements

Your project should have:
- Python package structure with `src/` directory
- `requirements.txt` file
- pytest test suite
- Conventional commit messages for semantic release

## MQTT Testing

The workflows include a Mosquitto MQTT broker for integration testing. Tests should connect to `localhost:1883` during CI runs.