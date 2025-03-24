import winreg
from pathlib import Path
from typing import Tuple, Optional, Final

from src.logger import setup_logger

_APP_PATHS_SUB_KEY: Final[str] = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"

logger = setup_logger(__name__)


class AppPathsRegister:
    def __init__(self, executable_file_path: Path, executable_name: str) -> None:
        self.executable_file_path: Path = executable_file_path
        self.executable_sub_key: str = f"{_APP_PATHS_SUB_KEY}\\{executable_name}.exe"

    def register(self) -> Tuple[bool, Optional[str]]:
        """
        Registers the application in Windows App Paths Sub Key.
        """
        try:
            registry_key = winreg.CreateKeyEx(
                winreg.HKEY_CURRENT_USER,
                self.executable_sub_key,
                0,
                winreg.KEY_WRITE
            )

            winreg.SetValueEx(
                registry_key,
                "",
                0,
                winreg.REG_SZ,
                str(self.executable_file_path)
            )

            winreg.CloseKey(registry_key)
            return True, None
        except Exception as e:
            logger.error(
                f"Error creating key '{self.executable_sub_key}' with value '{self.executable_file_path}': {e}")
            return False, f"Failed to register App Paths: {e}"

    def is_registered(self) -> bool:
        """
        Checks if the application is already registered in Windows App Paths.
        """
        try:
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.executable_sub_key,
                0,
                winreg.KEY_READ
            )
            winreg.CloseKey(registry_key)
            return True
        except OSError:
            return False
