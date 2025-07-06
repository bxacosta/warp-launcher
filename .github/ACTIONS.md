# GitHub Actions Deployment Guide

This project uses GitHub Actions for CI/CD and automatically publishes packages to the **GitLab Package Registry**.

## Available Workflows

### 1. `ci.yml` - CI Pipeline

**Trigger:** Push to `main` and Pull Requests to `main`.

This workflow validates code quality and functionality:

- **Quality Job:**
    - Run the Ruff linter for style and error checking.
    - Run the Ruff formatter to ensure code consistency.
    - Run the MyPy type checker for static analysis.

- **Test Job:**
    - Run the test suite using Pytest.
    - Generate a test report from a JUnit XML file.

### 2. `release.yml` - Release and Publish

**Trigger:** Push tags with the format `v*` (e.g., `v1.0.0`, `v2.1.3`) or manual dispatch from the Actions tab.

This workflow automates the release process:

- Determine the version from the Git tag or manual input.
- Update the `version` field in `pyproject.toml`.
- Build the `wheel` (.whl) and `sdist` (.tar.gz) packages using `uv build`.
- Publish the packages to the GitLab Package Registry.
- Create a GitHub Release and attach the built packages as artifacts.

## How to Create a Release

### Recommended Method (Automatic via Git Tags)

1. **Ensure `main` is stable** with all changes committed and pushed:

    - Switch to the `main` branch:
   ```bash
   git checkout main
   ```

    - Pull the latest changes from the remote `main` branch:
   ```bash
   git pull origin main
   ```

2. **Create and push a new version tag** to trigger the release:

    - Create a new annotated tag (e.g., `v1.0.0`):
   ```bash
   git tag v1.0.0
   ```

    - Push the created tag to the remote repository:
   ```bash
   git push origin --tags
   ```

3. **The workflow takes over automatically**:
    - Extract the version from the tag (e.g., `v1.0.0` → `1.0.0`).
    - Build the project with the correct version.
    - Publish the packages to GitLab.
    - Create a corresponding GitHub Release.

### Manual Method

1. Navigate to the **Actions** tab in the GitHub repository.
2. In the left sidebar, click on the **Release and Publish** workflow.
3. Click the **Run workflow** dropdown button.
4. (Optional) Manually enter a version number to release.
5. Click the **Run workflow** button.

## Required Configuration

### GitHub Secret (`Settings` → `Secrets and variables` → `Actions`)

Configure the following secret for the repository:

```
GITLAB_DEPLOY_TOKEN=your_gitlab_deploy_token
```

**To get the `GITLAB_DEPLOY_TOKEN`:**

1. In the GitLab project, go to **Settings → Repository**.
2. Expand the **Deploy tokens** section.
3. Create a new token with the following scopes:
    - `read_package_registry`
    - `write_package_registry`
4. Copy the generated token and add it as a secret in GitHub.

## Versioning Conventions

This project follows [Semantic Versioning (SemVer)](https://semver.org/):

- **v1.0.0** - Major release (potential breaking changes).
- **v1.1.0** - Minor release (new, backward-compatible features).
- **v1.0.1** - Patch release (backward-compatible bug fixes).

The `v` prefix is required for Git tags to trigger the release workflow.