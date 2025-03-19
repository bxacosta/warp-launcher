import json
from pathlib import Path
from typing import Final, Dict, Any, Optional, Tuple

from src.constants import DEFAULT_LAUNCH_MODE, DEFAULT_STARTING_PATH, PARENT_PROCESS_IDENTIFIER
from src.enums import LaunchMode
from src.utils import string_to_path

_LAUNCH_MODE_KEY: Final[str] = "launchMode"
_STARTING_PATH_KEY: Final[str] = "startingPath"


class Config:
    def __init__(self, mode: LaunchMode, starting_path: Path) -> None:
        self.mode: LaunchMode = mode
        self.starting_path: Path = starting_path

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Config instance to a dictionary for JSON serialization.
        """
        return {
            _LAUNCH_MODE_KEY: self.mode.value,
            _STARTING_PATH_KEY: str(self.starting_path),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Config":
        """
        Create a Config instance from a dictionary, handling defaults gracefully.
        """
        launch_mode = LaunchMode.from_value(data.get(_LAUNCH_MODE_KEY)) or DEFAULT_LAUNCH_MODE
        starting_path = string_to_path(data.get(_STARTING_PATH_KEY)) or DEFAULT_STARTING_PATH

        return Config(launch_mode, starting_path)

    def is_starting_path_parent_process(self) -> bool:
        return str(self.starting_path) == PARENT_PROCESS_IDENTIFIER


class ConfigHandler:
    def __init__(self, config_file_path: Path) -> None:
        self.config_file_path: Path = config_file_path

    def load_config(self) -> Config:
        """
        Load configuration from file, or return default config if not exist or an error occurs.
        """
        try:
            if not self.config_file_path.exists():
                return Config(DEFAULT_LAUNCH_MODE, DEFAULT_STARTING_PATH)

            with self.config_file_path.open("r", encoding="utf-8") as config_file:
                return Config.from_dict(json.load(config_file))
        except Exception as e:
            print(f"Error loading configuration ({self.config_file_path}): {e}")
            return Config(DEFAULT_LAUNCH_MODE, DEFAULT_STARTING_PATH)

    def save_config(self, config: Config) -> Tuple[bool, Optional[str]]:
        """
        Save the provided configuration to file.
        """
        try:
            with self.config_file_path.open("w", encoding="utf-8") as config_file:
                json.dump(config.to_dict(), config_file, indent=4)
            return True, None
        except IOError as e:
            print(f"Error saving configuration '{self.config_file_path}' with content '{config.to_dict()}': {e}")
            return False, f"Failed to save config: {e}"
