import winreg
from pathlib import Path
from typing import Tuple, Optional, Final

from src.logger import setup_logger

_HKEY_NAME: Final[str] = "HKEY_CURRENT_USER"
_APP_PATHS_SUBKEY: Final[str] = r"Software\Microsoft\Windows\CurrentVersion\App Paths"

logger = setup_logger(__name__)


class AppPathsRegister:
    def __init__(self, executable_file_path: Path, executable_name: str) -> None:
        self.__hive = winreg.HKEY_CURRENT_USER
        self.executable_file_path: Path = executable_file_path
        self.executable_subkey: str = f"{_APP_PATHS_SUBKEY}\\{executable_name}.exe"

    def register(self) -> Tuple[bool, Optional[str]]:
        """
        Registers the application in Windows App Paths Subkey.
        """
        logger.debug(f"Registering key '{_HKEY_NAME}\\{self.executable_subkey}'")
        try:
            registry_key = winreg.CreateKeyEx(
                self.__hive,
                self.executable_subkey,
                0,
                winreg.KEY_WRITE
            )

            logger.debug(f"Setting key default value to '{self.executable_file_path}'")
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
                f"Error creating key '{self.executable_subkey}' with value '{self.executable_file_path}': {e}")
            return False, f"Failed to register App Paths: {e}"

    def unregister(self) -> Tuple[bool, Optional[str]]:
        """
        Unregisters the application from Windows App Paths Subkey.
        """
        logger.debug(f"Removing registry key '{_HKEY_NAME}\\{self.executable_subkey}'")
        if not self.is_registered():
            logger.info("Key is not registered")
            return True, None

        try:
            winreg.DeleteKey(self.__hive, self.executable_subkey)
            logger.info(f"Registry key removed")
            return True, None
        except Exception as e:
            logger.error(f"Error unregistering key '{self.executable_subkey}': {e}")
            return False, f"Failed to unregister App Paths: {e}"

    def is_registered(self) -> bool:
        """
        Checks if the application is already registered in Windows App Paths.
        """
        try:
            registry_key = winreg.OpenKey(
                self.__hive,
                self.executable_subkey,
                0,
                winreg.KEY_READ
            )
            winreg.CloseKey(registry_key)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            logger.error(f"Error opening key '{self.executable_subkey}': {e}")
            return False
