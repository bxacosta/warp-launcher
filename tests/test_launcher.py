import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch, mock_open

from src.config import Config
from src.constants import PARENT_PROCESS_IDENTIFIER
from src.enums import LaunchMode
from src.launcher import Launcher


class TestLauncher(unittest.TestCase):
    def setUp(self):
        self.test_install_dir = Path("test_install_dir")
        self.test_config_file = "config.json"
        self.test_script_file = "launcher.vbs"
        self.test_command_name = "test-warp"

        self.test_launch_mode = LaunchMode.TAB
        self.test_launch_path = Path("/test/path")
        self.config = Config(self.test_launch_mode, self.test_launch_path)

        self.launcher = Launcher(
            command_name=self.test_command_name,
            install_directory=self.test_install_dir,
            config_file_name=self.test_config_file,
            script_file_name=self.test_script_file
        )

    @patch('src.launcher.Path.mkdir', side_effect=PermissionError("Access denied"))
    def test_create_install_directory_raises_error(self, mock_mkdir):
        with self.assertRaises(PermissionError):
            self.launcher.install(self.config)
            mock_mkdir.assert_called_once()

    @patch('src.launcher.Path.mkdir')
    @patch('src.launcher.Path.open', new_callable=mock_open)
    @patch('src.config.ConfigHandler.save_config', return_value=(True, None))
    @patch('src.registry.AppPathsRegister.register', return_value=(True, None))
    def test_install_success(self, mock_register, mock_save_config, mock_script_open, mock_mkdir):
        success, error = self.launcher.install(self.config)

        # Verify installation directory was created
        mock_mkdir.assert_called_once_with(exist_ok=True)
        # Verify script was saved
        mock_script_open.assert_called_once_with("w", encoding="utf-8")
        # Verify config was saved
        mock_save_config.assert_called_once_with(self.config)
        # Verify command was registered
        mock_register.assert_called_once()

        # Verify script content
        script_handle = mock_script_open()
        write_calls = script_handle.write.call_args_list
        script_content = ''.join(call[0][0] for call in write_calls)
        self.assertIn(f'path = "{self.test_launch_path}"', script_content)
        self.assertIn(f'warpURI = "warp://action/{self.test_launch_mode.value}?path=" & path', script_content)

        # Verify installation was successful
        self.assertTrue(success)
        self.assertIsNone(error)

    @patch('src.launcher.Path.mkdir')
    @patch('src.config.Path.open', new_callable=mock_open)
    @patch('src.config.ConfigHandler.save_config', return_value=(True, None))
    @patch('src.registry.AppPathsRegister.register', return_value=(True, None))
    def test_install_with_parent_process_path(self, mock_register, mock_save_config, mock_script_open, mock_mkdir):
        config = Config(self.test_launch_mode, Path(PARENT_PROCESS_IDENTIFIER))

        success, error = self.launcher.install(config)

        mock_mkdir.assert_called_once()
        mock_save_config.assert_called_once()
        mock_register.assert_called_once()

        script_handle = mock_script_open()
        write_calls = script_handle.write.call_args_list
        script_content = ''.join(call[0][0] for call in write_calls)
        self.assertIn('path = CreateObject("Scripting.FileSystemObject").GetAbsolutePathName(".")', script_content)

        self.assertTrue(success)
        self.assertIsNone(error)

    @patch('src.registry.AppPathsRegister.unregister', return_value=(True, None))
    @patch('src.launcher.Launcher.remove_install_directory', return_value=(True, None))
    def test_uninstall_success(self, mock_remove_dir, mock_unregister):
        success, error = self.launcher.uninstall()

        mock_unregister.assert_called_once()
        mock_remove_dir.assert_called_once()

        self.assertTrue(success)
        self.assertIsNone(error)

    @patch('pathlib.Path.exists')
    @patch('src.registry.AppPathsRegister.register', return_value=(False, "Unregister error"))
    def test_uninstall_unregister_failure(self, mock_rmtree, mock_exists):
        # Act
        success, error = self.launcher.uninstall()

        # Assert
        self.assertFalse(success)
        self.assertEqual(error, "Unregister error")
        mock_rmtree.assert_not_called()  # Verifica que no se llamó a rmtree

    @patch('pathlib.Path.exists', return_value=True)
    @patch('shutil.rmtree', return_value=None)
    def test_remove_directory_success(self, mock_rmtree, mock_exists):
        success, error = self.launcher.remove_install_directory()

        self.assertTrue(success)
        self.assertIsNone(error)
        mock_exists.assert_called_once()
        mock_rmtree.assert_called_once_with(self.test_install_dir)

    @patch('pathlib.Path.exists', return_value=True)
    @patch('shutil.rmtree', side_effect=PermissionError("Access denied"))
    def test_remove_directory_failure(self, mock_rmtree, mock_exists):
        success, error = self.launcher.remove_install_directory()

        self.assertFalse(success)
        self.assertIn("Access denied", error)
        mock_exists.assert_called_once()
        mock_rmtree.assert_called_once_with(self.test_install_dir)

    @patch('subprocess.Popen')
    def test_launch_warp(self, mock_popen):
        expected_uri = f"warp://action/{self.test_launch_mode.value}?path={self.test_launch_path}"
        expected_command = ["cmd", "/c", "start", "", expected_uri]

        Launcher.launch_warp(self.config)

        mock_popen.assert_called_once_with(
            expected_command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.DETACHED_PROCESS
        )


if __name__ == '__main__':
    unittest.main()
