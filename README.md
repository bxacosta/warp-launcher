# Warp Launcher

A tool that generates a launch script to open the [Warp terminal](https://www.warp.dev/) from the current working
directory on Windows. It provides a simple CLI to manage configuration and supports customizable launch modes,
enabling you to start Warp directly from the Windows Explorer address bar or from the terminal.

## Features

- Open Warp at the current directory from the Windows Explorer address bar or from the console by using the
  customizable command (default: `warp`).
- Choose between launching Warp in a new window or a new tab.
- Automatically create a launcher script and register the command within Windows registry `App Paths` Subkey.

## Requirements

- Python 3.12 or later
- [Warp Terminal](https://www.warp.dev/download) for Windows

## Setup

Set up the `warp-launcher` CLI tool using one of the following methods:

### Using uvx (Recommended)

Run the tool directly without installing it locally using [`uvx`](https://docs.astral.sh/uv/guides/tools/):

```bash
uvx --index-url "https://gitlab.com/api/v4/projects/70108742/packages/pypi/simple" warp-launcher
```

### Using pip

Install the package directly from GitLab using [`pip`](https://pip.pypa.io/en/stable/):

```bash
pip install --index-url "https://gitlab.com/api/v4/projects/70108742/packages/pypi/simple" warp-launcher
```

### From Source

Clone the repository and run the tool from source:

```bash
git clone https://github.com/bxacosta/warp-launcher.git
cd warp-launcher
python main.py
```

## Usage

### Command-Line Options

| Option              | Description                                | Default           |
|---------------------|--------------------------------------------|-------------------|
| `-c`, `--command`   | Custom command name                        | `warp`            |
| `-m`, `--mode`      | Launch mode: `window` or `tab`             | `window`          |
| `-p`, `--path`      | Initial path                               | Current directory |
| `-v`, `--verbose`   | Enable detailed logging                    | Off               |
| `-i`, `--install`   | Install the launcher                       | -                 |
| `-l`, `--launch`    | Launch Warp with the current configuration | -                 |
| `-u`, `--uninstall` | Remove the launcher                        | -                 |

### Install

Install with default settings:

```bash
warp-launcher -i
```

Install with a custom command (`wp`) and `tab` mode:

```bash
warp-launcher -c wp -m tab -i
```

After installation, type `warp` (or your custom command) in any directory from the Explorer address bar or terminal to
launch Warp at that location.

### Uninstall

```bash
warp-launcher -u
```

## Project Structure

```text
warp-launcher/
├── src/warp_launcher/
│   ├── cli.py           # CLI argument handling
│   ├── config.py        # User configuration management
│   ├── constants.py     # Global project constants
│   ├── enums.py         # Launch mode enumerations
│   ├── launcher.py      # Core functionalities for installation and configuration
│   ├── logger.py        # Logging system configuration
│   ├── registry.py      # Windows registry integration
│   ├── script.py        # Script generation and handling
│   └── utils.py         # General-purpose utilities
├── tests/               # Unit tests
├── main.py              # Main entry point
└── pyproject.toml       # Project configuration file

```

## Development

> [!NOTE]
> This project uses [uv](https://docs.astral.sh/uv/) as the package manager.

### Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to automatically run code quality checks before each commit. The
hooks include:

- **Ruff**: Code linting and formatting
- **MyPy**: Static type checking

To install pre-commit hooks:

```bash
uv run pre-commit install
```

To manually run all hooks on all files:

```bash
uv run pre-commit run --all-files
```

### Running Tests

To run all unit tests with [pytest](https://docs.pytest.org/en/stable/index.html), execute:

```bash
uv run pytest
```

This will discover and run all test files in the `tests` directory that match the pattern `test*.py`.

### Code Linting

To run code linting with [Ruff](https://github.com/astral-sh/ruff), execute:

```bash
uv run ruff check
```

This will analyze the code for potential issues and style violations.

### Code Formatting

To format code with [Ruff](https://github.com/astral-sh/ruff), execute:

```bash
uv run ruff format
```

This will automatically format the code according to the project's style guidelines.

### Type Checking

To run static type checking with [mypy](https://mypy-lang.org/), execute:

```bash
uv run mypy
```

This will validate type annotations across the project's source code files.

## How It Works

1. **Installation**: When you run `warp-launcher -i`, the tool:
    - Creates a configuration file (`config.json`) with your settings
    - Generates a launcher script (`launcher.vbs`) that uses Warp's URI scheme
    - Registers your command (default: `warp`) in Windows App Paths registry
    - Installs everything to `%LOCALAPPDATA%\Programs\WarpLauncher\`

2. **Usage**: Once installed, you can:
    - Type your command in any Explorer address bar to open Warp at that location
    - Run the command from any terminal/command prompt
    - The launcher automatically detects the current directory and opens Warp there

3. **Customization**: You can change settings anytime by running the install command again with different options.

> [!TIP]
> Use `warp-launcher -v -l` to see current configuration and launch Warp with verbose output.

## License

This project is licensed under the [MIT License](LICENSE).

- [] COnfigurar bien el reporte del test
- configurar la platafomra de que solo es para windows