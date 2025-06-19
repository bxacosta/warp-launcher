import logging
from pathlib import Path

from src.config import Config

logger = logging.getLogger(__name__)


class ScriptHandler:
    def __init__(self, script_file_path: Path) -> None:
        self._script_file_path: Path = script_file_path

    def save_script(self, config: Config) -> None:
        """
        Creates or updates the .vbs launcher script in the installation directory.
        """
        logger.debug(f"Saving launch script to '{self._script_file_path}'")

        path_definition = f'path = "{config.launch_path}"'

        if config.is_launch_path_parent_process():
            path_definition = 'path = CreateObject("Scripting.FileSystemObject").GetAbsolutePathName(".")'

        script_body = (
            'If Right(path, 1) = "\\" Then path = Left(path, Len(path) - 1) End If\n'
            f'warpURI = "warp://action/{config.launch_mode.value}?path=" & path\n'
            'CreateObject("WScript.Shell").Run warpURI, 0, False'
        )

        script_content = f"{path_definition}\n{script_body}"

        try:
            with self._script_file_path.open("w", encoding="utf-8") as script_file:
                script_file.write(script_content)
        except OSError as e:
            logger.error(f"Error writing script '{self._script_file_path}': {e}")
            raise RuntimeError(f"Error writing script: {e}") from e
