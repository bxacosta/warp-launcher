import json
from pathlib import Path
from typing import Final, Dict, Any

from src.constants import DEFAULT_LAUNCH_MODE, DEFAULT_STARTING_PATH
from src.enums import LaunchMode

_LAUNCH_MODE_KEY: Final[str] = "launchMode"
_STARTING_PATH_KEY: Final[str] = "startingPath"


class Config:
    def __init__(self, mode: LaunchMode, starting_path: str) -> None:
        self.mode: LaunchMode = mode
        self.starting_path: str = starting_path

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Config instance to a dictionary for JSON serialization.
        """
        return {
            _LAUNCH_MODE_KEY: self.mode.value,
            _STARTING_PATH_KEY: self.starting_path,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Config":
        """
        Create a Config instance from a dictionary, handling defaults gracefully.
        """
        launch_mode = LaunchMode.from_value(data.get(_LAUNCH_MODE_KEY)) or DEFAULT_LAUNCH_MODE

        starting_path = data.get(_STARTING_PATH_KEY)
        if not starting_path or not isinstance(starting_path, str):
            starting_path = DEFAULT_STARTING_PATH

        return Config(launch_mode, starting_path)


class ConfigHandler:
    def __init__(self, config_file_path: Path) -> None:
        self.config_file_path: Path = config_file_path

    def load_config(self) -> Config:
        """
        Load configuration from file, or return default config on error.
        """
        try:
            if not self.config_file_path.exists():
                return Config(DEFAULT_LAUNCH_MODE, DEFAULT_STARTING_PATH)

            with self.config_file_path.open("r", encoding="utf-8") as config_file:
                return Config.from_dict(json.load(config_file))
        except Exception as e:
            print(f"Error loading configuration ({self.config_file_path}): {e}")
            return Config(DEFAULT_LAUNCH_MODE, DEFAULT_STARTING_PATH)

    def save_config(self, config: Config) -> bool:
        """
        Save the provided configuration to file.
        """
        try:
            with self.config_file_path.open("w", encoding="utf-8") as config_file:
                json.dump(config.to_dict(), config_file, indent=4)
            return True
        except IOError as e:
            print(f"Error saving configuration ({self.config_file_path}): {e}")
            return False
