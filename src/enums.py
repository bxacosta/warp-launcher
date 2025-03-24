from enum import Enum
from typing import Optional


class LaunchMode(Enum):
    WINDOW = "new_window"
    TAB = "new_tab"

    @classmethod
    def from_value(cls, value: str) -> Optional["LaunchMode"]:
        try:
            return cls(value)
        except ValueError:
            return None

    @classmethod
    def from_name(cls, name: str) -> Optional["LaunchMode"]:
        try:
            return getattr(LaunchMode, name.upper())
        except KeyError:
            return None
