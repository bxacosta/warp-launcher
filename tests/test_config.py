import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src.config import ConfigHandler, Config
from src.constants import DEFAULT_LAUNCH_MODE, DEFAULT_STARTING_PATH
from src.enums import LaunchMode


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        temp_path = Path(self.temp_dir.name)
        self.test_config = Config(LaunchMode.TAB, "/test/path")
        self.config_file_path = temp_path / "test_config.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_config_to_dict(self):
        for mode in LaunchMode:
            config = Config(mode, "/some/path")
            expected = {
                "launchMode": mode.value,
                "startingPath": "/some/path"
            }
            self.assertEqual(config.to_dict(), expected)

    def test_config_from_dict_with_valid_data(self):
        for mode in LaunchMode:
            data = {
                "launchMode": mode,
                "startingPath": "/valid/path"
            }
            config = Config.from_dict(data)
            self.assertEqual(config.mode, mode)
            self.assertEqual(config.starting_path, "/valid/path")

    def test_config_from_dict_with_defaults(self):
        data = {}
        config = Config.from_dict(data)
        self.assertEqual(config.mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.starting_path, DEFAULT_STARTING_PATH)

        data = {"launchMode": LaunchMode.TAB.value}
        config = Config.from_dict(data)
        self.assertEqual(config.mode, LaunchMode.TAB)
        self.assertEqual(config.starting_path, DEFAULT_STARTING_PATH)

        data = {"startingPath": "/custom/path"}
        config = Config.from_dict(data)
        self.assertEqual(config.mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.starting_path, "/custom/path")

    def test_config_from_dict_with_invalid_launch_mode(self):
        data = {
            "launchMode": "invalid_mode",
            "startingPath": "/some/path"
        }
        config = Config.from_dict(data)
        self.assertEqual(config.mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.starting_path, "/some/path")

    def test_config_from_dict_with_invalid_types(self):
        data = {
            "launchMode": 123,
            "startingPath": 456
        }
        config = Config.from_dict(data)
        self.assertEqual(config.mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.starting_path, DEFAULT_STARTING_PATH)

    def test_load_config_non_existing_file(self):
        non_existing_config_file_path = Path("/non/existent") / "test.json"

        handler = ConfigHandler(non_existing_config_file_path)
        config = handler.load_config()

        self.assertEqual(config.mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.starting_path, DEFAULT_STARTING_PATH)

    def test_load_config_invalid_json(self):
        self.config_file_path.write_text("not valid json", encoding="utf-8")
        handler = ConfigHandler(self.config_file_path)
        config = handler.load_config()

        self.assertEqual(config.mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.starting_path, DEFAULT_STARTING_PATH)

    def test_save_and_load_config(self):
        handler = ConfigHandler(self.config_file_path)
        save_result = handler.save_config(self.test_config)

        self.assertTrue(save_result)
        self.assertTrue(self.config_file_path.exists())

        loaded_config = handler.load_config()
        self.assertEqual(loaded_config.mode, self.test_config.mode)
        self.assertEqual(loaded_config.starting_path, self.test_config.starting_path)

    @mock.patch('src.config.json.dump')
    def test_save_config_io_error(self, mock_dump):
        mock_dump.side_effect = IOError("Permission denied")

        handler = ConfigHandler(self.config_file_path)
        save_result = handler.save_config(self.test_config)

        self.assertFalse(save_result)

    @mock.patch('pathlib.Path.exists')
    def test_load_config_with_permission_error(self, mock_exists):
        mock_exists.side_effect = PermissionError("Permission denied")

        handler = ConfigHandler(self.config_file_path)
        config = handler.load_config()

        self.assertEqual(config.mode, DEFAULT_LAUNCH_MODE)
        self.assertEqual(config.starting_path, DEFAULT_STARTING_PATH)


if __name__ == "__main__":
    unittest.main()
