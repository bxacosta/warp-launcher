from __future__ import annotations

from enum import Enum


class LaunchMode(Enum):
    WINDOW = "new_window"
    TAB = "new_tab"

    @classmethod
    def from_value(cls, value: str) -> LaunchMode | None:
        try:
            return cls(value)
        except ValueError:
            return None

    @classmethod
    def from_name(cls, name: str | None) -> LaunchMode | None:
        if not name:
            return None

        try:
            return cls[name.upper()]
        except KeyError:
            return None

    def __str__(self) -> str:
        return self.name.lower()
