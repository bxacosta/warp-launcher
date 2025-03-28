import unittest
import winreg
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.registry import AppPathsRegister


class TestAppPathsRegister(unittest.TestCase):
    def setUp(self):
        self.executable_name = 'testapp'
        self.executable_path = Path(r'C:\test\path\app.vbs')
        self.app_paths_register = AppPathsRegister(self.executable_path, self.executable_name)
        self.registry_key = r'Software\Microsoft\Windows\CurrentVersion\App Paths\testapp.exe'

    @patch('winreg.CreateKeyEx')
    @patch('winreg.SetValueEx')
    @patch('winreg.CloseKey')
    def test_register_success(self, mock_close_key, mock_set_value, mock_create_key):
        mock_key = MagicMock()
        mock_create_key.return_value = mock_key

        success, error = self.app_paths_register.register()

        mock_create_key.assert_called_once_with(
            winreg.HKEY_CURRENT_USER,
            self.registry_key,
            0,
            winreg.KEY_WRITE
        )
        mock_set_value.assert_called_once_with(
            mock_key,
            "",
            0,
            winreg.REG_SZ,
            str(self.executable_path)
        )
        mock_close_key.assert_called_once_with(mock_key)
        self.assertTrue(success)
        self.assertIsNone(error)

    @patch('winreg.CreateKeyEx')
    def test_register_failure(self, mock_create_key):
        mock_create_key.side_effect = Exception('Access denied')

        success, error = self.app_paths_register.register()

        self.assertFalse(success)
        self.assertIn('Access denied', error)

    @patch('src.registry.AppPathsRegister.is_registered')
    @patch('winreg.DeleteKey')
    def test_unregister_failure(self, mock_delete_key, mock_is_registered):
        mock_is_registered.return_value = True
        mock_delete_key.side_effect = Exception('Access denied')

        success, error = self.app_paths_register.unregister()

        self.assertFalse(success)
        self.assertIn('Access denied', error)

    @patch('winreg.OpenKey')
    @patch('winreg.CloseKey')
    def test_is_registered_true(self, mock_close_key, mock_open_key):
        mock_key = MagicMock()
        mock_open_key.return_value = mock_key

        is_registered = self.app_paths_register.is_registered()

        mock_open_key.assert_called_once_with(
            winreg.HKEY_CURRENT_USER,
            self.registry_key,
            0,
            winreg.KEY_READ
        )
        mock_close_key.assert_called_once_with(mock_key)
        self.assertTrue(is_registered)

    @patch('winreg.OpenKey')
    def test_is_registered_false_not_found(self, mock_open_key):
        mock_open_key.side_effect = FileNotFoundError()

        is_registered = self.app_paths_register.is_registered()

        self.assertFalse(is_registered)

    @patch('winreg.OpenKey')
    def test_is_registered_false_error(self, mock_open_key):
        mock_open_key.side_effect = Exception('Access denied')

        is_registered = self.app_paths_register.is_registered()

        self.assertFalse(is_registered)


if __name__ == '__main__':
    unittest.main()