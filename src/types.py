from collections.abc import Hashable
from typing import TypeVar

# Generic types for dicts
K = TypeVar("K", bound=Hashable)
V = TypeVar("V")
