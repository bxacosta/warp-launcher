import logging
import os
import shutil
import subprocess
from pathlib import Path

from warp_launcher.config import ConfigHandler
from warp_launcher.constants import CONFIG_FILE_NAME, INSTALL_DIRECTORY, LAUNCHER_SCRIPT_NAME
from warp_launcher.enums import LaunchMode
from warp_launcher.registry import AppPathsRegister
from warp_launcher.script import ScriptHandler
from warp_launcher.utils import validate_command_name, validate_path

logger = logging.getLogger(__name__)


class Launcher:
    def __init__(
        self,
        install_directory: Path = INSTALL_DIRECTORY,
        config_filename: str = CONFIG_FILE_NAME,
        script_filename: str = LAUNCHER_SCRIPT_NAME,
    ):
        if not install_directory:
            raise ValueError("Installation directory must be provided")
        if not config_filename:
            raise ValueError("Configuration filename must be provided")
        if not script_filename:
            raise ValueError("Script filename must be provided")

        self.install_directory = install_directory
        logger.debug(f"Installation directory: {self.install_directory}")

        # Setup configuration handler
        config_file_path: Path = self.install_directory / config_filename
        self._config_handler: ConfigHandler = ConfigHandler(config_file_path)

        # Setup script handler
        script_file_path: Path = self.install_directory / script_filename
        self._script_handler: ScriptHandler = ScriptHandler(script_file_path)

        # Setup registry for the application paths
        self._app_paths_register: AppPathsRegister = AppPathsRegister(script_file_path)

        # Load the configuration from the configuration file
        self._config = self._config_handler.load_config()

    @property
    def command_name(self) -> str:
        return self._config.command_name

    @command_name.setter
    def command_name(self, new_command_name: str) -> None:
        command_name, error = validate_command_name(new_command_name)
        if not command_name:
            raise ValueError(error)
        self._config.command_name = command_name
        logger.info(f"Command name set to '{command_name}'")

    @property
    def launch_mode(self) -> LaunchMode:
        return self._config.launch_mode

    @launch_mode.setter
    def launch_mode(self, new_launch_mode: str) -> None:
        launch_mode = LaunchMode.from_name(new_launch_mode)
        if not launch_mode:
            raise ValueError(f"Invalid mode specified: '{new_launch_mode}'")
        self._config.launch_mode = launch_mode
        logger.info(f"Launch mode set to '{launch_mode}'")

    @property
    def launch_path(self) -> Path:
        return self._config.launch_path

    @launch_path.setter
    def launch_path(self, new_launch_path: str) -> None:
        path, error = validate_path(new_launch_path)
        if not path:
            raise ValueError(error)
        self._config.launch_path = path
        logger.info(f"Launch path set to '{path}'")

    def launch_warp(self) -> Path:
        """
        Launches the warp application using the provided Config.
        """
        launch_path = Path(os.getcwd()) if self._config.is_launch_path_parent_process() else self._config.launch_path

        uri = f"warp://action/{self._config.launch_mode.value}?path={launch_path}"

        subprocess.Popen(
            ["cmd", "/c", "start", "", uri],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.DETACHED_PROCESS,
        )

        logger.info(f"Warp launched in '{self._config.launch_mode}' mode at '{launch_path}'")
        return launch_path

    def install(self) -> None:
        """
        Persists the configuration by saving the script, the configuration file,
        and registering the command in the App Paths registry.
        """
        try:
            if self._config_handler.config_file_path.exists():
                logger.debug("Found existing configuration, checking if the previous command should be removed")
                saved_command_name = self._config_handler.load_config().command_name
                is_command_registered = self._app_paths_register.is_registered(saved_command_name)
                if saved_command_name != self._config.command_name and is_command_registered:
                    logger.info(f"Removing previous command '{saved_command_name}'")
                    self._app_paths_register.unregister(saved_command_name)

            self.install_directory.mkdir(exist_ok=True)

            self._script_handler.save_script(self._config)

            self._config_handler.save_config(self._config)

            self._app_paths_register.register(self._config.command_name)
        except (RuntimeError, OSError) as e:
            raise RuntimeError(f"Failed to install. {e}") from e

        logger.info("Installation completed successfully.")
        logger.info(
            f"Now you can type '{self.command_name}' in the Explorer address bar "
            f"or run 'start {self.command_name}' in the terminal to open Warp at that location."
        )

    def uninstall(self) -> None:
        """
        Removes the installation directory and unregisters the command from the App Paths registry.
        """
        try:
            config = self._config_handler.load_config()

            self._app_paths_register.unregister(config.command_name)

            self._remove_install_directory()
        except RuntimeError as e:
            raise RuntimeError(f"Failed to uninstall. {e}") from e

        logger.info("Uninstallation completed successfully")

    def _remove_install_directory(self) -> None:
        # Remove installation directory if it exists
        logger.debug(f"Removing installation directory '{self.install_directory}'")

        if not self.install_directory.exists():
            logger.info("Installation directory does not exist")

        try:
            shutil.rmtree(self.install_directory)
            logger.info("Installation directory removed")
        except OSError as e:
            logger.error(f"Error removing installation directory '{self.install_directory}': {e}")
            raise RuntimeError(f"Error removing installation directory: {e}") from e
