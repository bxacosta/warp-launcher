import logging
import os
from pathlib import Path
from typing import Final

from warp_launcher.enums import LaunchMode

CONFIG_FILE_NAME: Final[str] = "config.json"
LAUNCHER_SCRIPT_NAME: Final[str] = "launcher.vbs"
INSTALL_DIRECTORY: Final[Path] = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "Programs" / "WarpLauncher"

LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(message)" if LOG_LEVEL == logging.DEBUG else "%(message)s"

PARENT_PROCESS_IDENTIFIER: Final[str] = "."

DEFAULT_COMMAND_NAME: Final[str] = "warp"
DEFAULT_LAUNCH_MODE: Final[LaunchMode] = LaunchMode.WINDOW
DEFAULT_LAUNCH_PATH: Final[Path] = Path(PARENT_PROCESS_IDENTIFIER)
