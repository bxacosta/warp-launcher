import tempfile
import unittest
from pathlib import Path
from unittest import mock

# noinspection PyProtectedMember
from src.config import ConfigHandler, Config, _LAUNCH_MODE_KEY, _LAUNCH_PATH_KEY
from src.constants import DEFAULT_LAUNCH_MODE, DEFAULT_LAUNCH_PATH
from src.enums import LaunchMode
from src.utils import string_to_path


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        temp_path = Path(self.temp_dir.name)
        self.test_config = Config(LaunchMode.TAB, string_to_path("/test/path"))
        self.config_file_path = temp_path / "test_config.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_config_to_dict(self):
        for mode in LaunchMode:
            config = Config(mode, self.test_config.launch_path)
            expected = {
                _LAUNCH_MODE_KEY: mode.value,
                _LAUNCH_PATH_KEY: str(self.test_config.launch_path)
            }
            self.assertEqual(config.to_dict(), expected)

    def test_config_from_dict_with_valid_data(self):
        for mode in LaunchMode:
            data = {
                _LAUNCH_MODE_KEY: mode,
                _LAUNCH_PATH_KEY: str(self.test_config.launch_path)
            }
            config = Config.from_dict(data)
            self.assertEqual(config.launch_mode, mode)
            self.assertEqual(config.launch_path, self.test_config.launch_path)

    def test_config_from_dict_with_defaults(self):
        data = {}
        config = Config.from_dict(data)
        self.assertEqual(config.launch_mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.launch_path, DEFAULT_LAUNCH_PATH)

        data = {_LAUNCH_MODE_KEY: self.test_config.launch_mode.value}
        config = Config.from_dict(data)
        self.assertEqual(config.launch_mode, self.test_config.launch_mode)
        self.assertEqual(config.launch_path, DEFAULT_LAUNCH_PATH)

        data = {_LAUNCH_PATH_KEY: str(self.test_config.launch_path)}
        config = Config.from_dict(data)
        self.assertEqual(config.launch_mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.launch_path, self.test_config.launch_path)

    def test_config_from_dict_with_invalid_config(self):
        data = {
            _LAUNCH_MODE_KEY: "invalid_mode",
            _LAUNCH_PATH_KEY: ""
        }
        config = Config.from_dict(data)
        self.assertEqual(config.launch_mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.launch_path, DEFAULT_LAUNCH_PATH)

    def test_config_from_dict_with_invalid_types(self):
        data = {
            _LAUNCH_MODE_KEY: 123,
            _LAUNCH_PATH_KEY: 456
        }
        config = Config.from_dict(data)
        self.assertEqual(config.launch_mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.launch_path, DEFAULT_LAUNCH_PATH)

    def test_load_config_non_existing_file(self):
        non_existing_config_file_path = Path("/non/existent") / "test.json"

        handler = ConfigHandler(non_existing_config_file_path)
        config = handler.load_config()

        self.assertEqual(config.launch_mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.launch_path, DEFAULT_LAUNCH_PATH)

    def test_load_config_invalid_json(self):
        self.config_file_path.write_text("not valid json", encoding="utf-8")
        handler = ConfigHandler(self.config_file_path)
        config = handler.load_config()

        self.assertEqual(config.launch_mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.launch_path, DEFAULT_LAUNCH_PATH)

    def test_save_and_load_config(self):
        handler = ConfigHandler(self.config_file_path)
        save_result, _ = handler.save_config(self.test_config)

        self.assertTrue(save_result)
        self.assertTrue(self.config_file_path.exists())

        loaded_config = handler.load_config()
        self.assertEqual(loaded_config.launch_mode, self.test_config.launch_mode)
        self.assertEqual(loaded_config.launch_path, self.test_config.launch_path)

    @mock.patch('src.config.json.dump')
    def test_save_config_io_error(self, mock_class):
        mock_class.side_effect = IOError("Permission denied")

        handler = ConfigHandler(self.config_file_path)
        save_result, error = handler.save_config(self.test_config)

        self.assertFalse(save_result)
        self.assertIn("Permission denied", error)

    @mock.patch('pathlib.Path.exists')
    def test_load_config_with_permission_error(self, mock_class):
        mock_class.side_effect = PermissionError("Permission denied")

        handler = ConfigHandler(self.config_file_path)
        config = handler.load_config()

        self.assertEqual(config.launch_mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.launch_path, DEFAULT_LAUNCH_PATH)


if __name__ == "__main__":
    unittest.main()
