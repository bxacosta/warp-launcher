# Contributing

## Requirements

Before getting started, ensure your system has access to the following tools:

- [Python](https://www.python.org/) 3.12 or later
- [uv](https://docs.astral.sh/uv/): The Python package manager and installer
- [Git](https://git-scm.com/): For version control

## Quick Start

1. Clone the repository:

   ```bash
   git clone https://github.com/bxacosta/warp-launcher.git
   cd warp-launcher
   ```

2. Install dependencies with uv:

   ```bash
   uv sync --all-groups
   ```

3. Run the application locally:

   ```bash
   uv run main.py
   ```

## Coding standards

The project enforces code quality standards using pre-commit hooks. The configured hooks perform linting, formatting,
and type checking.

Install the hooks with:

```bash
uv run pre-commit install
```

To execute all hooks across the entire codebase:

```bash
uv run pre-commit run --all-files
```

## Quality Assurance

### Testing

Execute the test suite using `pytest`:

```bash
uv run pytest
```

### Linting

Run the linter to check for code style and quality issues:

```bash
uv run ruff check
```

### Formatting

Format the codebase according to the project's style guidelines:

```bash
uv run ruff format
```

### Type Checking

Perform static type analysis with `mypy`:

```bash
uv run mypy
```

## Contribution Workflow

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b my-feature`.
3. Implement your changes and include tests where applicable.
4. Ensure all development checks pass.
5. Commit your changes with a descriptive message: `git commit -m 'feat: Add new feature'`.
6. Push your branch to your fork: `git push origin my-feature`.
7. Open a Pull Request against the `main` branch.