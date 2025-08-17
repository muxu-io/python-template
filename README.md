# Reusable CI/CD Workflows for Python MQTT Projects

This repository provides reusable GitHub Actions workflows for Python projects with MQTT integration. Use these workflows to standardize your CI/CD pipeline across multiple Python repositories.

## Quick Start

### 1. Create CI/CD Workflow

Create `.github/workflows/ci.yml` in your Python project:

```yaml
name: CI/CD
run-name: ${{ github.event_name == 'pull_request' && 'Checks' || 'Release' }}
on:
  push:
    branches: [master, main, 'maint/**']
  pull_request:
  workflow_dispatch:

permissions:
  contents: write
  packages: write
  id-token: write
  statuses: write

jobs:
  checks:
    if: github.event_name == 'pull_request'
    uses: muxu-io/python-template/.github/workflows/checks.yml@master
    with:
      python-versions: '["3.9", "3.10", "3.11", "3.12"]'
      source-directory: 'src/'
      enable-mqtt-broker: true
      mqtt-config-path: '.github/mosquitto.conf'
      dockerhub-username: ${{ vars.DOCKERHUB_USERNAME }}
    secrets:
      DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}

  release:
    if: github.event_name == 'push' && (github.ref == 'refs/heads/master' || github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/heads/maint/')) && github.ref_type != 'tag' && github.event.head_commit.author.email != 'semantic-release'
    uses: muxu-io/python-template/.github/workflows/release.yml@master
    secrets:
      SEMANTIC_RELEASE_ADMIN_TOKEN: ${{ secrets.SEMANTIC_RELEASE_ADMIN_TOKEN }}
```

### 2. Create PyPI Publish Workflow

For PyPI publishing with Trusted Publishers, create `.github/workflows/pypi-publish.yml`:

```yaml
name: PyPI Publish
run-name: Publish ${{ github.ref_name }}

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: read
  id-token: write

jobs:
  pypi-publish:
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/${{ github.event.repository.name }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install build dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine

      - name: Build package
        run: python -m build

      - name: Check package
        run: twine check dist/*

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          verbose: true
          print-hash: true
          # Alternative: password: ${{ secrets.PYPI_API_TOKEN }}  # If not using Trusted Publishers
```

## Project Requirements

Ensure your project has:
- **Dependencies**: Either `requirements.txt` OR `pyproject.toml` with dependencies
- **Package config**: `pyproject.toml` with semantic-release setup
- **Tests**: `tests/` directory with pytest tests (or dev dependencies including pytest)
- **Source code**: `src/` directory with your Python package
- **MQTT config**: `.github/mosquitto.conf` - MQTT broker config (if using MQTT features)
- **Commit config**: `.github/.commitlintrc.json` - Conventional commit validation

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
- `dockerhub-username`: Docker Hub username for authentication (optional)
- `skip-build`: Skip build job to avoid attestation conflicts (default: `false`)

**Secrets:**
- `DOCKERHUB_TOKEN`: Docker Hub token for authentication (optional)

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

## Configuration

### Required Secrets and Variables

Your repository/organization needs these configured:

**Required Secrets:**
1. **`SEMANTIC_RELEASE_ADMIN_TOKEN`** - GitHub token with admin permissions for semantic release
   - Generate at: Settings → Developer settings → Personal access tokens → Fine-grained tokens
   - Required scopes: `contents:write`, `metadata:read`, `pull_requests:write`

**Optional (for Docker Hub authentication):**
2. **`DOCKERHUB_TOKEN`** - Docker Hub personal access token
   - Generate at: Docker Hub → Account Settings → Security → New Access Token
   - Used to avoid rate limiting when pulling images

**Optional Variables:**
3. **`DOCKERHUB_USERNAME`** - Your Docker Hub username
   - Set at organization or repository level
   - Used with `DOCKERHUB_TOKEN` for authentication

**Optional (alternative to Trusted Publishers):**
4. **`PYPI_API_TOKEN`** - PyPI API token for publishing
   - Only needed if NOT using PyPI Trusted Publishers
   - Generate at: https://pypi.org/manage/account/token/
   - Requires modifying `pypi-publish.yml` to use `password: ${{ secrets.PYPI_API_TOKEN }}`

### PyPI Publishing Setup

#### Option A: Trusted Publishers (Recommended)

The workflow uses PyPI's Trusted Publishers feature for secure publishing without API tokens:

1. **Create PyPI account** and register your package name
2. **Configure Trusted Publisher** at https://pypi.org/manage/account/publishing/
   - Repository owner: `your-username`
   - Repository name: `your-repo-name`
   - Workflow name: `pypi-publish.yml`
   - Environment name: `pypi`

#### Option B: API Token (Alternative)

If you can't use Trusted Publishers:

1. **Generate API token** at https://pypi.org/manage/account/token/
2. **Add secret** `PYPI_API_TOKEN` to your repository
3. **Modify workflow** to include:
   ```yaml
   - name: Publish to PyPI
     uses: pypa/gh-action-pypi-publish@release/v1
     with:
       password: ${{ secrets.PYPI_API_TOKEN }}
   ```

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

## Status Checks and Branch Protection

The workflows include a **unified status check system** that resolves issues with reusable workflow naming:

### How It Works
- The `checks` workflow creates individual status checks for each job (commit-check, code-quality, test matrix, build)
- A `summary` job aggregates all results and creates a single `checks` status via GitHub API
- Branch protection rules should require the unified status check created by the API

### Branch Protection Setup
Configure your repository's branch protection to require:
```
checks
```

**Note**: The `statuses: write` permission is required in your workflow for the API status check creation to work.

### Workflow Behavior
- **Pull Requests**: Shows as "Checks" and runs comprehensive CI checks
- **Pushes to main branches**: Shows as "Release" and runs semantic release
- **Tag creation**: Automatically triggers PyPI publishing via independent workflow
- **Maintenance branches**: Supports `master`, `main`, and `maint/**` patterns

## Requirements

Your project should have:
- **Package structure**: `src/` directory with your Python package
- **Dependencies**: Either `requirements.txt` OR `pyproject.toml` with `[project.dependencies]`
- **Testing**: pytest test suite (via requirements.txt or `[project.optional-dependencies.dev]`)
- **Commits**: Conventional commit messages for semantic release
- **Configuration**: `pyproject.toml` with semantic release configuration
- **Publishing**: PyPI Trusted Publishers configured (for automatic publishing)
- **System dependencies**: Projects using `systemd-python` work automatically (system libs installed in CI)

## MQTT Testing

The workflows include a Mosquitto MQTT broker for integration testing:
- **Broker**: Available at `localhost:1883` during CI runs
- **Configuration**: Place custom config in `.github/mosquitto.conf`
- **Authentication**: Docker Hub credentials optional but recommended to avoid rate limits
- **Environment**: Tests receive `MQTT_BROKER_HOST=localhost` and `MQTT_BROKER_PORT=1883`

## Real-World Examples

### Example 1: mqtt-connector (with requirements.txt)

Repository structure:
```
mqtt-connector/
├── .github/
│   ├── .commitlintrc.json
│   ├── mosquitto.conf
│   └── workflows/
│       ├── ci.yml
│       └── pypi-publish.yml
├── src/mqtt_connector/
├── tests/
├── requirements.txt
└── pyproject.toml
```

The `ci.yml` uses the reusable workflow:
```yaml
jobs:
  checks:
    if: github.event_name == 'pull_request'
    uses: muxu-io/python-template/.github/workflows/checks.yml@master
    with:
      python-versions: '["3.9", "3.10", "3.11", "3.12"]'
      source-directory: 'src/'
      enable-mqtt-broker: true
      mqtt-config-path: '.github/mosquitto.conf'
      dockerhub-username: ${{ vars.DOCKERHUB_USERNAME }}
    secrets:
      DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
```

### Example 2: mqtt-application (with pyproject.toml dependencies)

Repository structure:
```
mqtt-application/
├── .github/
│   ├── .commitlintrc.json
│   ├── mosquitto.conf
│   └── workflows/
│       ├── ci.yml
│       └── pypi-publish.yml
├── src/mqtt_application/
├── tests/
└── pyproject.toml  # No requirements.txt
```

Uses the same reusable workflow call - the workflow automatically detects and installs dev dependencies from `pyproject.toml`:
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    # ... other dev dependencies
]
```

### Example 3: Different Configuration

For a project without MQTT testing:
```yaml
jobs:
  checks:
    if: github.event_name == 'pull_request'
    uses: muxu-io/python-template/.github/workflows/checks.yml@master
    with:
      python-versions: '["3.10", "3.11"]'  # Fewer versions
      source-directory: 'lib/'              # Different source dir
      enable-mqtt-broker: false             # Disable MQTT
```

### How It Works

1. **Pull Request**: Triggers comprehensive checks via reusable workflow
2. **Push to main**: Triggers semantic release, creates git tag if needed
3. **Tag creation**: Automatically triggers local `pypi-publish.yml` workflow
4. **Result**: Clean separation, proper attestations, reliable publishing
