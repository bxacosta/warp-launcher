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
