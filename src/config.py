import json
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Dict, Any, Optional, Tuple

from src.constants import DEFAULT_LAUNCH_MODE, DEFAULT_LAUNCH_PATH, PARENT_PROCESS_IDENTIFIER, DEFAULT_COMMAND_NAME
from src.enums import LaunchMode
from src.logger import setup_logger
from src.utils import validate_command_name, validate_path, merge_dicts

_COMMAND_NAME_KEY: Final[str] = "commandName"
_LAUNCH_MODE_KEY: Final[str] = "launchMode"
_LAUNCH_PATH_KEY: Final[str] = "launchPath"

logger = setup_logger(__name__)


@dataclass
class Config:
    command_name: str
    launch_mode: LaunchMode
    launch_path: Path

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Config instance to a dictionary for JSON serialization.
        """
        return {
            _COMMAND_NAME_KEY: self.command_name,
            _LAUNCH_MODE_KEY: str(self.launch_mode),
            _LAUNCH_PATH_KEY: str(self.launch_path),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        """
        Create a Config instance from a dictionary, raise ValueError if a value is invalid.
        """
        command_name, command_name_error = validate_command_name(data.get(_COMMAND_NAME_KEY))
        if not command_name: raise ValueError(command_name_error)

        launch_mode = LaunchMode.from_name(data.get(_LAUNCH_MODE_KEY))
        if not launch_mode: raise ValueError(f"Invalid launch mode: '{data.get(_LAUNCH_MODE_KEY)}'")

        launch_path, launch_path_error = validate_path(data.get(_LAUNCH_PATH_KEY))
        if not launch_path: raise ValueError(launch_path_error)

        return cls(command_name, launch_mode, launch_path)

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

        default_config = Config(DEFAULT_COMMAND_NAME, DEFAULT_LAUNCH_MODE, DEFAULT_LAUNCH_PATH)
        try:
            if not self.config_file_path.exists():
                logger.debug(f"Configuration file not found, using default configuration '{default_config.to_dict()}'")
                return default_config

            with self.config_file_path.open("r", encoding="utf-8") as config_file:
                config_dict = merge_dicts(json.load(config_file), default_config.to_dict())
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
