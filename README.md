# Warp Launcher

A tool that generates a launch script to open the [Warp terminal](https://www.warp.dev/) from the current working
directory on Windows. It provides a simple CLI to manage configuration and supports customizable launch modes,
enabling you to start Warp directly from the Windows Explorer address bar or from the terminal.

## Features

- Open Warp at the current directory from the Windows Explorer address bar or from the console by using the
  customizable command (default: `warp`).
- Choose between launching Warp in a new window or a new tab.
- Automatically create a launcher script and register the command within Windows registry `App Paths` Subkey.

## Quick Start

1. **Requirements:**
    - Python 3.12 or later
    - [Warp terminal](https://www.warp.dev/download) for Windows

2. **Clone the repository:**
   ```bash
   git clone https://github.com/bxacosta/warp-launcher.git
   cd warp-launcher
   ```

3. **Install with default settings:**
    ```bash
    python main.py -i
    ```

4. **Test if it works:**
    - Type `warp` into the Windows Explorer address bar and press `Enter`.
    - Alternatively, you can execute `start warp` from the console.

> [!TIP]
> Type `python main.py -h` to display the help message.

## Project Structure

```text
warp-launcher/
├── src/
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

### Running Tests

To run all unit tests, execute the `tests.py` file:

```bash
uv run tests.py
```

This will discover and run all test files in the `tests` directory that match the pattern `test*.py`.

### Type Checking

To run static type checking with [mypy](https://mypy.readthedocs.io/en/stable/), execute:

```bash
uv run mypy src
```

This will validate type annotations across the project's source code files.

## How it Works

- **Configuration:** Settings are saved in a JSON file (`config.json`) within the installation directory.
- **Registration:** During installation, the app registers the command (customizable, default: `warp`) in
  Windows [App Paths](https://learn.microsoft.com/en-us/windows/win32/shell/app-registration) Subkey, enabling you to
  launch Warp from anywhere.
- **Launcher Script:** A Visual Basic Script (`launcher.vbs`) is created in the installation directory, utilizing
  the [Warp URI Scheme](https://docs.warp.dev/features/uri-scheme) to open the terminal according to the provided
  configuration.

## License

This project is licensed under the [MIT License](LICENSE).
