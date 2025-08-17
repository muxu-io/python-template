# Reusable CI/CD Workflows for Python MQTT Projects

This repository provides reusable GitHub Actions workflows for Python projects with MQTT integration. Use these workflows to standardize your CI/CD pipeline across multiple Python repositories.

## Quick Start

Create `.github/workflows/ci.yml` in your Python project:

```yaml
name: CI
on: [push, pull_request]

jobs:
  checks:
    uses: your-org/python-template/.github/workflows/checks.yml@main
    with:
      python-versions: '["3.9", "3.10", "3.11", "3.12"]'
      source-directory: 'src/'
      enable-mqtt-broker: true

  release:
    if: github.ref == 'refs/heads/main'
    needs: checks
    uses: your-org/python-template/.github/workflows/release.yml@main
    secrets:
      SEMANTIC_RELEASE_ADMIN_TOKEN: ${{ secrets.SEMANTIC_RELEASE_ADMIN_TOKEN }}

  publish:
    if: needs.release.outputs.released == 'true'
    needs: [checks, release]
    uses: your-org/python-template/.github/workflows/publish.yml@main
```

## Project Requirements

Ensure your project has:
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Package configuration with semantic-release setup
- `tests/` directory with pytest tests
- `src/` directory with source code
- `.github/mosquitto.conf` - MQTT broker config (if using MQTT features)

## Available Workflows

#### `checks.yml`
Comprehensive CI checks including:
- **Commit validation** - Enforces conventional commit messages
- **Code quality** - Black formatting, Ruff linting, Bandit security scanning
- **Vulnerability scanning** - pip-audit and TruffleHog secret detection
- **Testing** - Multi-version Python testing with optional MQTT broker
- **Build validation** - Package building and verification

**Inputs:**
- `python-versions`: JSON array of Python versions (default: 3.9-3.12)
- `source-directory`: Source directory to scan (default: `src/`)
- `requirements-file`: Requirements file path (default: `requirements.txt`)
- `enable-mqtt-broker`: Whether to start MQTT broker (default: `true`)
- `mqtt-config-path`: Mosquitto config file path (default: `.github/mosquitto.conf`)

#### `release.yml`
Semantic release workflow:
- **Automated versioning** - Uses semantic-release for version management
- **GitHub releases** - Creates releases with changelogs
- **Tag creation** - Git tags for version tracking

**Inputs:**
- `python-version`: Python version for release (default: `3.11`)

**Secrets:**
- `SEMANTIC_RELEASE_ADMIN_TOKEN`: Required GitHub token with admin permissions

**Outputs:**
- `released`: Whether a release was made
- `version`: Version that was released
- `tag`: Git tag that was created

#### `publish.yml`
PyPI publishing workflow:
- **Trusted Publishers** - Secure PyPI publishing without API tokens
- **Artifact verification** - Package validation before publishing
- **TestPyPI support** - Optional publishing to test repository

**Inputs:**
- `python-version`: Python version for publishing (default: `3.11`)
- `environment`: GitHub environment name (default: `pypi`)
- `testpypi`: Publish to TestPyPI instead (default: `false`)


## Configuration

### Required Secrets

Your repository needs these GitHub secrets configured:

1. **`SEMANTIC_RELEASE_ADMIN_TOKEN`** - GitHub token with admin permissions for semantic release
   - Generate at: Settings → Developer settings → Personal access tokens → Fine-grained tokens
   - Required scopes: `contents:write`, `metadata:read`, `pull_requests:write`

### PyPI Trusted Publishers Setup

The workflow uses PyPI's Trusted Publishers feature for secure publishing without API tokens:

1. **Create PyPI account** and register your package name
2. **Configure Trusted Publisher** at https://pypi.org/manage/account/publishing/
   - Repository owner: `your-username`
   - Repository name: `your-repo-name`
   - Workflow name: `release.yml`
   - Environment name: (leave empty)

### Semantic Release Configuration

Add to your `pyproject.toml`:

```toml
[tool.semantic_release]
version_toml = ["pyproject.toml:project.version"]
build_command = "python -m build"
dist_path = "dist/"
upload_to_vcs_release = true

[tool.semantic_release.commit_parser_options]
allowed_tags = ["build", "chore", "ci", "docs", "feat", "fix", "perf", "style", "refactor", "test"]
minor_tags = ["feat"]
patch_tags = ["fix", "perf"]
```

### Renovate Setup

The template includes Renovate configuration for automated dependency updates:

1. **Enable Renovate** - Install the [Renovate GitHub App](https://github.com/apps/renovate) on your repository
2. **Configuration** - The `.github/renovate.json` file is pre-configured with:
   - Weekly updates scheduled for Monday mornings
   - Semantic commit messages with `chore(deps):` prefix
   - Grouped updates for related packages (pytest, MQTT, dev tools)
   - Auto-merge for patch updates and GitHub Actions
   - Vulnerability alerts enabled

3. **Customize** - Update the `assignees` and `reviewers` fields in `.github/renovate.json` to match your GitHub username

## Requirements

Your project should have:
- Python package structure with `src/` directory
- `requirements.txt` file
- pytest test suite
- Conventional commit messages for semantic release
- `pyproject.toml` with semantic release configuration
- PyPI Trusted Publishers configured (for automatic publishing)

## MQTT Testing

The workflows include a Mosquitto MQTT broker for integration testing. Tests should connect to `localhost:1883` during CI runs.
