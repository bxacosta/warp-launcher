import logging
import os
import re
from pathlib import Path
from typing import Optional, Tuple, Union

from src.logger import setup_logger

logger = setup_logger(__name__)


def string_to_path(path_str: Optional[str]) -> Optional[Path]:
    """
    Convert a string to a Path object if the string represents a valid path.
    """
    if not isinstance(path_str, str) or not path_str.strip():
        return None

    invalid_chars = ['<', '>', '"', '|', '?', '*']
    if any(char in str(path_str) for char in invalid_chars):
        return None

    colon_positions = [i for i, char in enumerate(path_str) if char == ':']
    if colon_positions and not (len(colon_positions) == 1 and colon_positions[0] == 1):
        return None

    try:
        return Path(path_str.strip()).expanduser()
    except Exception as error:
        logging.error(error)
        return None


def validate_path(path: Union[str, Path]) -> Tuple[Optional[Path], Optional[str]]:
    """
    Validate that a path exists and is accessible.
    """
    logger.debug(f"Validating path: {path}")

    path_object = None
    try:
        if isinstance(path, str):
            path_object = string_to_path(path)

        if not path_object:
            return None, f"Path '{path}' is not valid"

        if not path_object.exists():
            return None, f"Path '{path_object}' does not exist"

        if not os.access(path_object, os.R_OK):
            return None, f"Path '{path_object}' is not accessible"

        return path_object, None
    except Exception as error:
        logging.error(error)
        return None, f"Path '{path}' is not valid"


def validate_command_name(command_name: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Validate that .
    """
    if not command_name: return None, "Command is not valid"

    symbols_allowed = ['-', '_']
    symbols_allowed_message = " or ".join(f"'{symbol}'" for symbol in symbols_allowed)

    if command_name[0] in symbols_allowed or command_name[-1] in symbols_allowed:
        return None, f"Command name '{command_name}' should not start or end with {symbols_allowed_message}"

    pattern = re.compile(r"^[a-zA-Z0-9_-]+$")

    if not pattern.match(command_name):
        return None, f"Only alphanumeric characters are allowed and {symbols_allowed_message}"

    return command_name, None
