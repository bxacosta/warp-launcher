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
    def from_name(cls, name: Optional[str]) -> Optional["LaunchMode"]:
        if not name: return None

        try:
            return getattr(cls, name.upper())
        except AttributeError:
            return None

    def __str__(self):
        return self.name.lower()
