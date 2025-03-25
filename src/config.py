import json
from pathlib import Path
from typing import Final, Dict, Any, Optional, Tuple

from src.constants import DEFAULT_LAUNCH_MODE, DEFAULT_LAUNCH_PATH, PARENT_PROCESS_IDENTIFIER
from src.enums import LaunchMode
from src.logger import setup_logger
from src.utils import string_to_path

_LAUNCH_MODE_KEY: Final[str] = "launchMode"
_LAUNCH_PATH_KEY: Final[str] = "launchPath"

logger = setup_logger(__name__)


class Config:
    def __init__(self, launch_mode: LaunchMode, launch_path: Path) -> None:
        self.launch_mode: LaunchMode = launch_mode
        self.launch_path: Path = launch_path

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Config instance to a dictionary for JSON serialization.
        """
        return {
            _LAUNCH_MODE_KEY: str(self.launch_mode),
            _LAUNCH_PATH_KEY: str(self.launch_path),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Config":
        """
        Create a Config instance from a dictionary, handling defaults gracefully.
        """
        launch_mode = LaunchMode.from_name(data.get(_LAUNCH_MODE_KEY)) or DEFAULT_LAUNCH_MODE
        launch_path = string_to_path(data.get(_LAUNCH_PATH_KEY)) or DEFAULT_LAUNCH_PATH

        return Config(launch_mode, launch_path)

    def is_launch_path_parent_process(self) -> bool:
        return str(self.launch_path) == PARENT_PROCESS_IDENTIFIER


class ConfigHandler:
    def __init__(self, config_file_path: Path) -> None:
        self.config_file_path: Path = config_file_path

    def load_config(self) -> Config:
        """
        Load configuration from file, or return default config if not exist or an error occurs.
        """
        logger.debug(f"Loading configuration from '{self.config_file_path}'")

        default_config = Config(DEFAULT_LAUNCH_MODE, DEFAULT_LAUNCH_PATH)
        try:
            if not self.config_file_path.exists():
                logger.debug(f"Configuration file not found, using default configuration '{default_config.to_dict()}'")
                return default_config

            with self.config_file_path.open("r", encoding="utf-8") as config_file:
                config_dict = json.load(config_file)
                logger.debug(f"Loaded configuration '{config_dict}'")
                return Config.from_dict(config_dict)
        except Exception as e:
            logger.error(f"Error loading configuration from '{self.config_file_path}': {e}")
            return default_config

    def save_config(self, config: Config) -> Tuple[bool, Optional[str]]:
        """
        Save the provided configuration to file.
        """
        logger.debug(f"Saving configuration to '{self.config_file_path}'")
        config_dict = config.to_dict()
        try:
            with self.config_file_path.open("w", encoding="utf-8") as config_file:
                json.dump(config_dict, config_file, indent=4)
                logger.debug(f"Saved configuration '{config_dict}'")
            return True, None
        except IOError as e:
            logger.error(
                f"Error saving configuration to '{self.config_file_path}' with content '{config_dict}': {e}")
            return False, f"Failed to save config: {e}"
