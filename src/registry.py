import winreg
from pathlib import Path
from typing import Final

from src.logger import setup_logger

_HKEY_NAME: Final[str] = "HKEY_CURRENT_USER"
_APP_PATHS_SUBKEY: Final[str] = r"Software\Microsoft\Windows\CurrentVersion\App Paths"

logger = setup_logger(__name__)


def _build_app_paths_subkey(executable_name: str) -> str:
    if not executable_name:
        raise ValueError("executable_name cannot be empty")

    return f"{_APP_PATHS_SUBKEY}\\{executable_name}.exe"


class AppPathsRegister:
    def __init__(self, executable_file_path: Path):
        self.__hkey = winreg.HKEY_CURRENT_USER
        self.executable_file_path: Path = executable_file_path

    def register(self, executable_name: str) -> None:
        """
        Registers the application in Windows App Paths Subkey.
        """
        subkey = _build_app_paths_subkey(executable_name)

        logger.debug(f"Registering key '{subkey}' in '{_HKEY_NAME}'")

        try:
            registry_key = winreg.CreateKeyEx(self.__hkey, subkey, access=winreg.KEY_WRITE)

            logger.debug(f"Setting key default value to '{self.executable_file_path}'")
            winreg.SetValueEx(registry_key, "", 0, winreg.REG_SZ, str(self.executable_file_path))

            winreg.CloseKey(registry_key)
        except Exception as e:
            logger.error(f"Error registering key '{subkey}' with value '{self.executable_file_path}': {e}")
            raise RuntimeError(f"Error registering App Paths registry key: {e}") from e

    def unregister(self, executable_name: str) -> None:
        """
        Unregisters the application from Windows App Paths Subkey.
        """
        subkey = _build_app_paths_subkey(executable_name)

        logger.debug(f"Removing key '{subkey}' from '{_HKEY_NAME}'")
        if not self.is_registered(executable_name):
            logger.info("Key is not registered")

        try:
            winreg.DeleteKey(self.__hkey, subkey)
            logger.info("Registry key removed")
        except Exception as e:
            logger.error(f"Error unregistering key '{subkey}': {e}")
            raise RuntimeError(f"Error unregistering App Paths registry key: {e}") from e

    def is_registered(self, executable_name: str) -> bool:
        """
        Checks if the application is already registered in Windows App Paths.
        """
        subkey = _build_app_paths_subkey(executable_name)

        try:
            registry_key = winreg.OpenKey(self.__hkey, subkey, access=winreg.KEY_READ)
            winreg.CloseKey(registry_key)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            logger.error(f"Error opening key '{subkey}': {e}")
            return False
