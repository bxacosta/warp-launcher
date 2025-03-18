import os
from pathlib import Path
from typing import Final

from src.enums import LaunchMode

CONFIG_FILE_NAME: Final[str] = "config.json"

DEFAULT_STARTING_PATH: Final[str] = "."
DEFAULT_LAUNCH_MODE: Final[LaunchMode] = LaunchMode.WINDOW
DEFAULT_INSTALL_PATH: Final[Path] = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "Programs" / "WarpLauncher"
