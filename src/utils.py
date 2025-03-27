import logging
import os
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
