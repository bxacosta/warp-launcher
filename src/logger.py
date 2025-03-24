import logging
import sys
from typing import Optional

from src.constants import LOG_FORMAT

# ANSI color codes
_DEFAULT = "\033[0m"
_BUE = "\033[94m"
_RED = "\033[91m"
_YELLOW = "\033[93m"

_COLOR_MAP = {
    logging.INFO: _DEFAULT,
    logging.DEBUG: _BUE,
    logging.ERROR: _RED,
    logging.WARNING: _YELLOW,
}


class ColorFormatter(logging.Formatter):
    """Formatter that colors the log messages based on level."""

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        color = _COLOR_MAP.get(record.levelno, _DEFAULT)
        return f"{color}{message}{_DEFAULT}"


def setup_logger(name: str = None, level: Optional[int] = logging.NOTSET) -> logging.Logger:
    """Configure console logger."""

    logger = logging.getLogger(name or __name__)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        handler.setFormatter(ColorFormatter(LOG_FORMAT))
        logger.addHandler(handler)
        logger.propagate = False

    return logger
