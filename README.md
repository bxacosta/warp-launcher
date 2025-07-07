# Warp Launcher

A tool that generates a launch script to open the [Warp terminal](https://www.warp.dev/) from the current working
directory on Windows. It provides a simple CLI to manage configuration and supports customizable launch modes,
enabling you to start Warp directly from the Windows Explorer address bar or from the terminal.

## Features

- Open Warp at the current directory from the Windows Explorer address bar or from the console by using the
  customizable command.
- Customizable launch options, choose between opening Warp in a new window or tab, and define the initial directory
  path.

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
| `-c`, `--command`   | Command name                               | `warp`            |
| `-m`, `--mode`      | Launch mode: `window` or `tab`             | `window`          |
| `-p`, `--path`      | Initial path                               | Current directory |
| `-v`, `--verbose`   | Enable detailed logging                    | Disabled          |
| `-i`, `--install`   | Install the launcher                       | -                 |
| `-l`, `--launch`    | Launch Warp with the current configuration | -                 |
| `-u`, `--uninstall` | Remove the launcher                        | -                 |

### Install

Install with default settings:

```bash
warp-launcher -i
```

Install with a custom command (`wp`) and tab mode:

```bash
warp-launcher -c wp -m tab -i
```

After installation, type `warp` (or your custom command) in any directory from the Explorer address bar or run
`start warp` from the terminal to launch Warp at that location.

### Uninstall

Remove al files created by the install process und unregister the command

```bash
warp-launcher -u
```

> [!TIP]
> Use the `-v` option to print detailed logs about the tool’s actions.

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

## How It Works

When installed, `warp-launcher` performs the following actions:

- Creates a configuration file (`config.json`) with your settings.
- Generates a Visual Basic Script (`launcher.vbs`) that
  uses [Warp's URI scheme](https://docs.warp.dev/features/uri-scheme).
- Registers the command (default: `warp`) in
  Windows [App Paths](https://learn.microsoft.com/en-us/windows/win32/shell/app-registration) registry
- Installs everything to `%LOCALAPPDATA%\Programs\WarpLauncher\`

## Contributing

To contribute to Warp Launcher, see the [Contributing Guidelines](.github/CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).