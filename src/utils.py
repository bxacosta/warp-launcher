from pathlib import Path
from typing import Optional


def string_to_path(path_str: str) -> Optional[Path]:
    """
    Convert a string to a Path object if the string represents a valid path.
    """
    if not isinstance(path_str, str) or not path_str.strip():
        return None

    invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
    if any(char in str(path_str) for char in invalid_chars):
        return None

    try:
        path = Path(path_str.strip())
        path.absolute()
        return path
    except Exception:
        return None
