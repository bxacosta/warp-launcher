import logging
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

import pytest

from src.config import Config
from src.enums import LaunchMode
from src.launcher import Launcher

logging.getLogger().setLevel(logging.CRITICAL)


class TestLauncher(unittest.TestCase):
    def setUp(self):
        self.test_command_name = "test-command"
        self.test_launch_mode = LaunchMode.TAB
        self.test_launch_path = Path(r"C:\test\path")
        self.test_config = Config(self.test_command_name, self.test_launch_mode, self.test_launch_path)

        # Patches ConfigHandler.load_config to not read from disk
        patcher = patch("src.config.ConfigHandler.load_config", return_value=self.test_config)
        self.addCleanup(patcher.stop)
        self.mock_load_config = patcher.start()

        self.test_install_dir = Path(r"C:\test\install")
        self.test_config_file = "test_config.json"
        self.test_script_file = "test_launcher.vbs"
        self.test_launcher = Launcher(self.test_install_dir, self.test_config_file, self.test_script_file)

    def test_command_name_getter_setter(self):
        self.assertEqual(self.test_launcher.command_name, self.test_command_name)

        with self.assertRaises(ValueError):
            self.test_launcher.command_name = "_invalid_command_name_"

    def test_launch_mode_getter_setter(self):
        self.assertEqual(self.test_launcher.launch_mode, self.test_launch_mode)

        with self.assertRaises(ValueError):
            self.test_launcher.launch_mode = "INVALID"

    def test_launch_path_getter_setter(self):
        self.assertEqual(self.test_launcher.launch_path, self.test_launch_path)

        with self.assertRaises(ValueError):
            self.test_launcher.launch_path = r"C:\Invalid\Path"

    @patch("src.launcher.Path.mkdir", side_effect=PermissionError("Access denied"))
    def test_create_install_directory_raises_error(self, mock_mkdir):
        with self.assertRaises(RuntimeError) as context:
            self.test_launcher.install()

        mock_mkdir.assert_called_once()
        self.assertIn("Failed to install", str(context.exception))

    @patch("src.registry.AppPathsRegister.register", return_value=None)
    @patch("src.config.ConfigHandler.save_config", return_value=None)
    @patch("src.script.ScriptHandler.save_script", return_value=None)
    @patch("src.launcher.Path.mkdir")
    def test_install_success(self, mock_mkdir, mock_save_script, mock_save_config, mock_register):
        self.test_launcher.install()

        mock_mkdir.assert_called_once_with(exist_ok=True)
        mock_save_script.assert_called_once_with(self.test_config)
        mock_save_config.assert_called_once_with(self.test_config)
        mock_register.assert_called_once_with(self.test_config.command_name)

    @patch("shutil.rmtree")
    @patch("src.registry.AppPathsRegister.unregister")
    @patch("pathlib.Path.exists", return_value=True)
    def test_uninstall_success(self, mock_exists, mock_unregister, mock_rmtree):
        self.test_launcher.uninstall()

        mock_unregister.assert_called_once_with(self.test_config.command_name)
        mock_exists.assert_called_once()
        mock_rmtree.assert_called_once_with(self.test_install_dir)

    @patch("shutil.rmtree", side_effect=PermissionError("Unregister error"))
    @patch("src.registry.AppPathsRegister.unregister")
    @patch("pathlib.Path.exists", return_value=True)
    def test_uninstall_failure(self, mock_exists, mock_unregister, mock_rmtree):
        with self.assertRaises(RuntimeError) as context:
            self.test_launcher.uninstall()

        mock_unregister.assert_called_once_with(self.test_config.command_name)
        mock_exists.assert_called_once()
        mock_rmtree.assert_called_once_with(self.test_install_dir)
        self.assertIn("Failed to uninstall", str(context.exception))

    @patch("subprocess.Popen")
    def test_launch_warp(self, mock_popen):
        self.test_launcher._config.is_launch_path_parent_process = lambda: False
        expected_uri = f"warp://action/{self.test_config.launch_mode.value}?path={self.test_config.launch_path}"
        expected_command = ["cmd", "/c", "start", "", expected_uri]

        self.test_launcher.launch_warp()
        mock_popen.assert_called_once_with(
            expected_command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.DETACHED_PROCESS,
        )


if __name__ == "__main__":
    pytest.main()
