# Warp Launcher

A tool to quickly launch the [Warp terminal](https://www.warp.dev/) for windows from your current working directory,
either via the Windows Explorer address bar or directly from the console. It supports configurable launch modes and
includes a simple CLI for managing its configuration.

## Features

- Open Warp at the current directory from the Windows Explorer address bar or from the console by using the
  `start warp` command.
- Choose between launching Warp in a new window or a new tab.
- Automatically create a launcher script and register the `warp` command within Windows registry `App Paths` Subkey.

## Quick Start

1. **Requirements:**
    - Python 3.12 or later
    - [Warp terminal](https://www.warp.dev/download) for Windows

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/warp-launcher.git
   cd warp-launcher
   ```

3. **Run the Program:**
    ```bash
    # Chose between 'tab' or 'window' launch mode and install 
    python main.py -m tab -i
    ```

4. **Test if it works:**
   > Type `warp` into the Windows Explorer address bar and press `Enter`, or execute `start warp` from the console.

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
│   ├── launcher.py      # Core functionalities to launch Warp
│   ├── logger.py        # Logging system configuration
│   ├── registry.py      # Windows registry integration
│   └── utils.py         # General-purpose utilities
├── tests/               # Unit tests
├── main.py              # Main entry point
└── pyproject.toml       # Project configuration file

```

## How it Works

- **Configuration:** Settings are saved in a JSON file (`config.json`) within the installation directory.
- **Registration:** During installation, the app registers the `warp` command in
  Windows [App Paths](https://learn.microsoft.com/en-us/windows/win32/shell/app-registration) Subkey, enabling you to
  launch Warp from anywhere.
- **Launcher Script:** A Visual Basic Script (`launcher.vbs`) is created in the installation directory, utilizing
  the [Warp URI Scheme](https://docs.warp.dev/features/uri-scheme) to open the terminal according to the provided
  configuration.

## License

This project is licensed under the [MIT License](LICENSE).
