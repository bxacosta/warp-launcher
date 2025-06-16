import logging
import unittest
import winreg
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.registry import AppPathsRegister

logging.getLogger().setLevel(logging.CRITICAL)


class TestAppPathsRegister(unittest.TestCase):
    def setUp(self):
        self.executable_name = "testapp"
        self.executable_path = Path(r"C:\test\path\app.vbs")
        self.app_paths_register = AppPathsRegister(self.executable_path)
        self.registry_key = r"Software\Microsoft\Windows\CurrentVersion\App Paths\testapp.exe"

    @patch("winreg.CreateKeyEx")
    @patch("winreg.SetValueEx")
    @patch("winreg.CloseKey")
    def test_register_success(self, mock_close_key, mock_set_value, mock_create_key):
        mock_key = MagicMock()
        mock_create_key.return_value = mock_key

        self.app_paths_register.register(self.executable_name)

        mock_create_key.assert_called_once_with(winreg.HKEY_CURRENT_USER, self.registry_key, access=winreg.KEY_WRITE)
        mock_set_value.assert_called_once_with(mock_key, "", 0, winreg.REG_SZ, str(self.executable_path))
        mock_close_key.assert_called_once_with(mock_key)

    @patch("winreg.CreateKeyEx", side_effect=Exception("Access denied"))
    def test_register_failure(self, mock_create_key):
        with self.assertRaises(RuntimeError):
            self.app_paths_register.register(self.executable_name)

        mock_create_key.assert_called_once()

    @patch("src.registry.AppPathsRegister.is_registered", return_value=True)
    @patch("winreg.DeleteKey", side_effect=Exception("Access denied"))
    def test_unregister_failure(self, mock_delete_key, mock_is_registered):
        with self.assertRaises(RuntimeError):
            self.app_paths_register.unregister(self.executable_name)

        mock_delete_key.assert_called_once()
        mock_is_registered.assert_called_once()

    @patch("winreg.OpenKey")
    @patch("winreg.CloseKey")
    def test_is_registered_true(self, mock_close_key, mock_open_key):
        mock_key = MagicMock()
        mock_open_key.return_value = mock_key

        is_registered = self.app_paths_register.is_registered(self.executable_name)

        mock_open_key.assert_called_once_with(winreg.HKEY_CURRENT_USER, self.registry_key, access=winreg.KEY_READ)
        mock_close_key.assert_called_once_with(mock_key)
        self.assertTrue(is_registered)

    @patch("winreg.OpenKey", side_effect=FileNotFoundError())
    def test_is_registered_false_not_found(self, mock_open_key):
        is_registered = self.app_paths_register.is_registered(self.executable_name)

        mock_open_key.assert_called_once()
        self.assertFalse(is_registered)

    @patch("winreg.OpenKey", side_effect=Exception("Access denied"))
    def test_is_registered_false_error(self, mock_open_key):
        is_registered = self.app_paths_register.is_registered(self.executable_name)

        mock_open_key.assert_called_once()
        self.assertFalse(is_registered)


if __name__ == "__main__":
    pytest.main()
