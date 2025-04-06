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
        for launch_mode_item in LaunchMode:
            config = Config(launch_mode_item, self.test_config.launch_path)
            expected_dict = {
                _LAUNCH_MODE_KEY: str(launch_mode_item),
                _LAUNCH_PATH_KEY: str(self.test_config.launch_path)
            }
            self.assertEqual(config.to_dict(), expected_dict)

    def test_config_from_dict_with_valid_data(self):
        for launch_mode_item in LaunchMode:
            config_dict = {
                _LAUNCH_MODE_KEY: str(launch_mode_item),
                _LAUNCH_PATH_KEY: str(self.test_config.launch_path)
            }
            config = Config.from_dict(config_dict)
            self.assertEqual(config.launch_mode, launch_mode_item)
            self.assertEqual(config.launch_path, self.test_config.launch_path)

    def test_config_from_dict_with_defaults(self):
        config = Config.from_dict({})
        self.assertEqual(config.launch_mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.launch_path, DEFAULT_LAUNCH_PATH)

        config_dict = {_LAUNCH_MODE_KEY: str(self.test_config.launch_mode)}
        config = Config.from_dict(config_dict)
        self.assertEqual(config.launch_mode, self.test_config.launch_mode)
        self.assertEqual(config.launch_path, DEFAULT_LAUNCH_PATH)

        config_dict = {_LAUNCH_PATH_KEY: str(self.test_config.launch_path)}
        config = Config.from_dict(config_dict)
        self.assertEqual(config.launch_mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.launch_path, self.test_config.launch_path)

    def test_config_from_dict_with_invalid_config(self):
        config_dict = {
            _LAUNCH_MODE_KEY: "invalid_mode",
            _LAUNCH_PATH_KEY: ""
        }
        config = Config.from_dict(config_dict)
        self.assertEqual(config.launch_mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.launch_path, DEFAULT_LAUNCH_PATH)

    def test_config_from_dict_with_invalid_types(self):
        config_dict = {
            _LAUNCH_MODE_KEY: 123,
            _LAUNCH_PATH_KEY: 456
        }
        config = Config.from_dict(config_dict)
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

    @mock.patch('src.config.json.dump', side_effect=IOError("Permission denied"))
    def test_save_config_io_error(self, mock_class):
        handler = ConfigHandler(self.config_file_path)
        save_result, error = handler.save_config(self.test_config)

        mock_class.assert_called_once()
        self.assertFalse(save_result)
        self.assertIn("Permission denied", error)

    @mock.patch('pathlib.Path.exists', side_effect=PermissionError("Permission denied"))
    def test_load_config_with_permission_error(self, mock_class):
        handler = ConfigHandler(self.config_file_path)
        config = handler.load_config()

        mock_class.assert_called_once()
        self.assertEqual(config.launch_mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.launch_path, DEFAULT_LAUNCH_PATH)


if __name__ == "__main__":
    unittest.main()
