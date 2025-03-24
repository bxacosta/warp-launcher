import os
import subprocess
from pathlib import Path
from typing import Tuple, Optional

from src.config import Config, ConfigHandler
from src.constants import INSTALL_PATH, CONFIG_FILE_NAME, LAUNCHER_SCRIPT_NAME, COMMAND_NAME
from src.logger import setup_logger
from src.registry import AppPathsRegister

logger = setup_logger(__name__)


class Launcher:
    def __init__(self,
                 command_name: str = COMMAND_NAME,
                 install_path: Path = INSTALL_PATH,
                 config_file_name: str = CONFIG_FILE_NAME,
                 script_file_name: str = LAUNCHER_SCRIPT_NAME):

        if not command_name:
            raise RuntimeError("Must specify a 'command_name'")

        if not install_path:
            raise RuntimeError("Must specify a 'install_path'")

        if not config_file_name:
            raise RuntimeError("Must specify a 'config_file_name'")

        if not script_file_name:
            raise RuntimeError("Must specify a 'script_file_name'")

        self.install_path = install_path
        self.install_path.mkdir(exist_ok=True)

        # Setup config
        config_file_path: Path = self.install_path / config_file_name
        self.config_handler: ConfigHandler = ConfigHandler(config_file_path)

        # Setup registry
        self.script_file_path: Path = self.install_path / script_file_name
        self.app_paths_register: AppPathsRegister = AppPathsRegister(self.script_file_path, command_name)

    def install(self, config: Config) -> Tuple[bool, Optional[str]]:
        """
        Persists the configuration by saving the script, config file, and create App Paths sub key.
        """
        # Save script
        script_success, script_error = self.save_script(config)
        if not script_success:
            return False, script_error

        # Save config
        config_success, config_error = self.config_handler.save_config(config)
        if not config_success:
            return False, config_error

        # Register app paths
        register_success, register_error = self.app_paths_register.register()
        if not register_success:
            return False, register_error

        return True, None

    def save_script(self, config: Config) -> Tuple[bool, Optional[str]]:
        """
        Creates or updates the .vbs launcher script in the installation directory.
        """
        script_content = (
                'If Right(path, 1) = "\\" Then path = Left(path, Len(path) - 1) End If\n' +
                # 'WScript.Echo "Path: " & path\n' +
                f'warpURI = "warp://action/{config.mode.value}?path=" & path\n' +
                'CreateObject("WScript.Shell").Run warpURI, 0, False')

        if config.is_starting_path_parent_process():
            script_content = (f'path = CreateObject("Scripting.FileSystemObject").GetAbsolutePathName(".")\n' +
                              f'{script_content}')
        else:
            script_content = (f'path = "{config.starting_path}"\n' +
                              f'{script_content}')

        try:
            with self.script_file_path.open("w", encoding="utf-8") as script_file:
                script_file.write(script_content)
            return True, None
        except IOError as e:
            logger.error(f"Error writing script '{self.script_file_path}' with content '{script_content}': {e}")
            return False, f"Failed to write script: {e}"

    @staticmethod
    def launch_warp(config: Config):
        """
        Launches the warp application using the provided Config.
        """
        if config.is_starting_path_parent_process():
            config.starting_path = Path(os.getcwd())

        uri = f"warp://action/{config.mode.value}?path={config.starting_path}"

        subprocess.Popen(
            ["cmd", "/c", "start", "", uri],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.DETACHED_PROCESS
        )
