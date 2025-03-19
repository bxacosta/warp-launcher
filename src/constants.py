import os
from pathlib import Path
from typing import Final

from src.enums import LaunchMode

COMMAND_NAME: Final[str] = "warp"
CONFIG_FILE_NAME: Final[str] = "config.json"
LAUNCHER_SCRIPT_NAME: Final[str] = "launcher.vbs"
PARENT_PROCESS_IDENTIFIER: Final[str] = "."
INSTALL_PATH: Final[Path] = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "Programs" / "WarpLauncher"

DEFAULT_LAUNCH_MODE: Final[LaunchMode] = LaunchMode.WINDOW
DEFAULT_STARTING_PATH: Final[Path] = Path(PARENT_PROCESS_IDENTIFIER)
