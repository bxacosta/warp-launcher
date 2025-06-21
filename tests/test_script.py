import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from warp_launcher.config import Config
from warp_launcher.constants import PARENT_PROCESS_IDENTIFIER
from warp_launcher.enums import LaunchMode
from warp_launcher.script import ScriptHandler


class TestScriptHandler(unittest.TestCase):
    def setUp(self):
        self.test_script_path = Path("test_script.vbs")
        self.script_handler = ScriptHandler(self.test_script_path)
        self.test_launch_mode = LaunchMode.TAB
        self.test_launch_path = Path(r"C:\test\path")
        self.test_config = Config("test-command", self.test_launch_mode, self.test_launch_path)

    @patch("pathlib.Path.open", new_callable=mock_open)
    def test_save_script_with_regular_path(self, mock_file):
        self.script_handler.save_script(self.test_config)

        mock_file.assert_called_once_with("w", encoding="utf-8")
        handle = mock_file()

        write_calls = handle.write.call_args_list
        script_content = "".join(call[0][0] for call in write_calls)

        self.assertIn(f'path = "{self.test_launch_path}"', script_content)

    @patch("pathlib.Path.open", new_callable=mock_open)
    def test_save_script_with_parent_process_path(self, mock_file):
        config = Config("test-command", self.test_launch_mode, Path(PARENT_PROCESS_IDENTIFIER))

        self.script_handler.save_script(config)

        mock_file.assert_called_once_with("w", encoding="utf-8")
        handle = mock_file()

        write_calls = handle.write.call_args_list
        script_content = "".join(call[0][0] for call in write_calls)

        self.assertIn('path = CreateObject("Scripting.FileSystemObject").GetAbsolutePathName(".")', script_content)

    @patch("pathlib.Path.open", side_effect=OSError("Access denied"))
    def test_save_script_handles_file_error(self, mock_file):
        with self.assertRaises(RuntimeError) as context:
            self.script_handler.save_script(self.test_config)

        self.assertIn("Error writing script", str(context.exception))
        mock_file.assert_called_once_with("w", encoding="utf-8")


if __name__ == "__main__":
    pytest.main()
