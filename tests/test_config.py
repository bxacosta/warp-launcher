import logging
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# noinspection PyProtectedMember
from src.config import _COMMAND_NAME_KEY, _LAUNCH_MODE_KEY, _LAUNCH_PATH_KEY, Config, ConfigHandler
from src.constants import DEFAULT_COMMAND_NAME, DEFAULT_LAUNCH_MODE, DEFAULT_LAUNCH_PATH
from src.enums import LaunchMode

logging.getLogger().setLevel(logging.CRITICAL)


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        temp_path = Path(self.temp_dir.name)
        self.test_config = Config("test_command", LaunchMode.TAB, Path.home())
        self.default_config = Config(DEFAULT_COMMAND_NAME, DEFAULT_LAUNCH_MODE, DEFAULT_LAUNCH_PATH)
        self.config_file_path = temp_path / "test_config.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_config_to_dict(self):
        for launch_mode_item in LaunchMode:
            config = Config(self.test_config.command_name, launch_mode_item, self.test_config.launch_path)
            expected_dict = {
                _COMMAND_NAME_KEY: self.test_config.command_name,
                _LAUNCH_MODE_KEY: str(launch_mode_item),
                _LAUNCH_PATH_KEY: str(self.test_config.launch_path),
            }
            self.assertEqual(config.to_dict(), expected_dict)

    def test_config_from_dict_with_valid_data(self):
        for launch_mode_item in LaunchMode:
            config_dict = {
                _COMMAND_NAME_KEY: self.test_config.command_name,
                _LAUNCH_MODE_KEY: str(launch_mode_item),
                _LAUNCH_PATH_KEY: str(self.test_config.launch_path),
            }
            config = Config.from_dict(config_dict)
            expected_config = Config(self.test_config.command_name, launch_mode_item, self.test_config.launch_path)
            self.assertEqual(config, expected_config)

    def test_config_from_dict_with_invalid_config(self):
        test_cases = [
            {},
            {
                _COMMAND_NAME_KEY: "_invalid_command_name_",
                _LAUNCH_MODE_KEY: str(self.test_config.launch_mode),
                _LAUNCH_PATH_KEY: str(self.test_config.launch_path),
            },
            {
                _COMMAND_NAME_KEY: str(self.test_config.command_name),
                _LAUNCH_MODE_KEY: "invalid_mode",
                _LAUNCH_PATH_KEY: str(self.test_config.launch_path),
            },
            {
                _COMMAND_NAME_KEY: str(self.test_config.command_name),
                _LAUNCH_MODE_KEY: str(self.test_config.launch_mode),
                _LAUNCH_PATH_KEY: "<invalid_path>",
            },
        ]

        for config_dict in test_cases:
            with self.subTest(input=config_dict), self.assertRaises(ValueError):
                Config.from_dict(config_dict)

    def test_load_config_non_existing_file(self):
        non_existing_config_file_path = Path("/non/existent") / "test.json"

        handler = ConfigHandler(non_existing_config_file_path)
        config = handler.load_config()

        self.assertEqual(config, self.default_config)

    def test_load_config_invalid_json(self):
        self.config_file_path.write_text("not valid json", encoding="utf-8")
        handler = ConfigHandler(self.config_file_path)
        config = handler.load_config()

        self.assertEqual(config, self.default_config)

    def test_load_config_missing_fields(self):
        self.config_file_path.write_text(f'"{_LAUNCH_MODE_KEY}": "{self.default_config.launch_mode}"', encoding="utf-8")
        handler = ConfigHandler(self.config_file_path)
        config = handler.load_config()

        self.assertEqual(config, self.default_config)

    def test_save_and_load_config(self):
        handler = ConfigHandler(self.config_file_path)
        save_result, _ = handler.save_config(self.test_config)

        self.assertTrue(save_result)
        self.assertTrue(self.config_file_path.exists())

        config = handler.load_config()
        self.assertEqual(config, self.test_config)

    @patch("src.config.json.dump", side_effect=OSError("Permission denied"))
    def test_save_config_io_error(self, mock_class):
        handler = ConfigHandler(self.config_file_path)

        with self.assertRaises(RuntimeError):
            handler.save_config(self.test_config)

        mock_class.assert_called_once()

    @patch("pathlib.Path.exists", side_effect=PermissionError("Permission denied"))
    def test_load_config_with_permission_error(self, mock_class):
        handler = ConfigHandler(self.config_file_path)
        config = handler.load_config()

        mock_class.assert_called_once()
        self.assertEqual(config, self.default_config)


if __name__ == "__main__":
    unittest.main()
