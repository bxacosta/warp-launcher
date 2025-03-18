import winreg
from typing import Tuple, Optional, Final

APP_PATHS_SUB_KEY: Final[str] = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"


class AppPathsRegister:
    def __init__(self, executable_path: str, executable_name: str = "warp") -> None:
        self.executable_path: str = executable_path
        self.executable_sub_key: str = f"{APP_PATHS_SUB_KEY}\\{executable_name}.exe"

    def register(self) -> Tuple[bool, Optional[str]]:
        """
        Registers the application in Windows App Paths Sub Key.

        Returns:
            Tuple[bool, Optional[str]]: (True, None) if registration is successful,
            or (False, error message) if an error occurs.
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
                self.executable_path
            )

            winreg.CloseKey(registry_key)
            return True, None
        except Exception as e:
            return False, f"Registration error: {e}"

    def is_registered(self) -> bool:
        """
        Checks if the application is already registered in Windows App Paths.

        Returns:
            bool: True if the application is registered, False otherwise.
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
