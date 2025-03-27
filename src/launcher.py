import os
import shutil
import subprocess
from pathlib import Path
from typing import Tuple, Optional

from src.config import Config, ConfigHandler
from src.constants import INSTALL_DIRECTORY, CONFIG_FILE_NAME, LAUNCHER_SCRIPT_NAME, COMMAND_NAME
from src.logger import setup_logger
from src.registry import AppPathsRegister

logger = setup_logger(__name__)


class Launcher:
    def __init__(self,
                 command_name: str = COMMAND_NAME,
                 install_directory: Path = INSTALL_DIRECTORY,
                 config_file_name: str = CONFIG_FILE_NAME,
                 script_file_name: str = LAUNCHER_SCRIPT_NAME):

        if not command_name: raise RuntimeError("Must specify a 'command_name'")
        if not install_directory: raise RuntimeError("Must specify a 'install_path'")
        if not config_file_name: raise RuntimeError("Must specify a 'config_file_name'")
        if not script_file_name: raise RuntimeError("Must specify a 'script_file_name'")

        self.install_directory = install_directory

        # Setup config
        config_file_path: Path = self.install_directory / config_file_name
        self.config_handler: ConfigHandler = ConfigHandler(config_file_path)

        # Setup registry
        self.script_file_path: Path = self.install_directory / script_file_name
        self.app_paths_register: AppPathsRegister = AppPathsRegister(self.script_file_path, command_name)

    def install(self, config: Config) -> Tuple[bool, Optional[str]]:
        """
        Persists the configuration by saving the script, config file, and create App Paths sub key.
        """
        self.install_directory.mkdir(exist_ok=True)

        script_success, script_error = self.save_script(config)
        if not script_success: return False, script_error

        config_success, config_error = self.config_handler.save_config(config)
        if not config_success: return False, config_error

        register_success, register_error = self.app_paths_register.register()
        if not register_success: return False, register_error

        return True, None

    def uninstall(self) -> Tuple[bool, Optional[str]]:
        """
        Removes the installation directory and unregisters the App Paths sub key.
        """
        unregister_success, unregister_error = self.app_paths_register.unregister()
        if not unregister_success: return False, unregister_error

        remove_success, remove_error = self.remove_install_directory()
        if not remove_success: return False, remove_error

        return True, None

    def remove_install_directory(self) -> Tuple[bool, Optional[str]]:
        # Remove installation directory if it exists
        logger.debug(f"Removing installation directory '{self.install_directory}'")

        if not self.install_directory.exists():
            logger.info("Installation directory does not exist")
            return True, None

        try:
            shutil.rmtree(self.install_directory)
            logger.info(f"Installation directory removed")
            return True, None
        except Exception as e:
            logger.error(f"Error removing installation directory '{self.install_directory}': {e}")
            return False, f"Failed to remove installation directory: {e}"

    def save_script(self, config: Config) -> Tuple[bool, Optional[str]]:
        """
        Creates or updates the .vbs launcher script in the installation directory.
        """
        logger.debug(f"Saving launch script to '{self.script_file_path}'")

        script_content = (
                'If Right(path, 1) = "\\" Then path = Left(path, Len(path) - 1) End If\n' +
                # 'WScript.Echo "Path: " & path\n' +
                f'warpURI = "warp://action/{config.launch_mode.value}?path=" & path\n' +
                'CreateObject("WScript.Shell").Run warpURI, 0, False')

        if config.is_launch_path_parent_process():
            script_content = (f'path = CreateObject("Scripting.FileSystemObject").GetAbsolutePathName(".")\n' +
                              f'{script_content}')
        else:
            script_content = (f'path = "{config.launch_path}"\n' +
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
        if config.is_launch_path_parent_process(): config.launch_path = Path(os.getcwd())

        uri = f"warp://action/{config.launch_mode.value}?path={config.launch_path}"

        subprocess.Popen(
            ["cmd", "/c", "start", "", uri],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.DETACHED_PROCESS
        )
