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
- **Semantic release** - Automated versioning and GitHub releases with enhanced bot actor handling
- **Package publishing** - Build artifacts and PyPI publishing via Trusted Publishers
- **Enhanced security** - Uses SEMANTIC_RELEASE_ADMIN_TOKEN for improved permission management

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
