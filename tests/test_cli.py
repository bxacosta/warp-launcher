import unittest
from unittest.mock import patch, MagicMock

from src.cli import parse_cli_arguments, cli
from src.constants import PARENT_PROCESS_IDENTIFIER


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.mock_logger = MagicMock()
        self.patcher = patch('src.cli.logger', self.mock_logger)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_parse_cli_arguments_no_args(self):
        with self.assertRaises(SystemExit) as cm:
            parse_cli_arguments([])
        self.assertEqual(cm.exception.code, 0)

    def test_parse_cli_arguments_mode(self):
        args = parse_cli_arguments(['-m', 'tab'])
        self.assertEqual(args.mode, 'tab')

    def test_parse_cli_arguments_invalid_mode(self):
        with self.assertRaises(SystemExit):
            parse_cli_arguments(['-m', 'invalid'])

    def test_parse_cli_arguments_path(self):
        test_path = 'C:\\test\\path'
        args = parse_cli_arguments(['-p', test_path])
        self.assertEqual(args.path, test_path)

    def test_parse_cli_arguments_parent_process_path(self):
        args = parse_cli_arguments(['-p', PARENT_PROCESS_IDENTIFIER])
        self.assertEqual(args.path, PARENT_PROCESS_IDENTIFIER)

    def test_parse_cli_arguments_launch(self):
        args = parse_cli_arguments(['-l'])
        self.assertTrue(args.launch)

    def test_parse_cli_arguments_install(self):
        args = parse_cli_arguments(['-i'])
        self.assertTrue(args.install)

    def test_parse_cli_arguments_uninstall(self):
        args = parse_cli_arguments(['-u'])
        self.assertTrue(args.uninstall)

    def test_parse_cli_arguments_verbose(self):
        args = parse_cli_arguments(['-v'])
        self.assertTrue(args.verbose)

    def test_parse_cli_arguments_combined(self):
        args = parse_cli_arguments(['-m', 'window', '-p', 'C:\\test', '-l', '-i', '-v'])
        self.assertEqual(args.mode, 'window')
        self.assertEqual(args.path, 'C:\\test')
        self.assertTrue(args.launch)
        self.assertTrue(args.install)
        self.assertTrue(args.verbose)

    @patch('src.cli.Launcher')
    @patch('src.cli.validate_path')
    def test_cli_successful_installation(self, mock_validate_path, mock_launcher_class):
        mock_launcher = MagicMock()
        mock_launcher_class.return_value = mock_launcher
        mock_launcher.install.return_value = (True, None)
        mock_launcher.config_handler.load_config.return_value = MagicMock()
        mock_validate_path.return_value = (True, None)

        exit_code = cli()
        self.assertEqual(exit_code, 0)

    @patch('src.cli.Launcher')
    def test_cli_successful_uninstallation(self, mock_launcher_class):
        mock_launcher = MagicMock()
        mock_launcher_class.return_value = mock_launcher
        mock_launcher.uninstall.return_value = (True, None)
        mock_launcher.config_handler.load_config.return_value = MagicMock()

        with patch('sys.argv', ['script.py', '-u']):
            exit_code = cli()
        self.assertEqual(exit_code, 0)

    @patch('src.cli.Launcher')
    def test_cli_failed_uninstallation(self, mock_launcher_class):
        mock_launcher = MagicMock()
        mock_launcher_class.return_value = mock_launcher
        mock_launcher.uninstall.return_value = (False, 'Test error')
        mock_launcher.config_handler.load_config.return_value = MagicMock()

        with patch('sys.argv', ['script.py', '-u']):
            exit_code = cli()
        self.assertEqual(exit_code, 1)
        self.mock_logger.error.assert_called_once_with('Failed to uninstall: Test error')

    @patch('src.cli.Launcher')
    def test_cli_invalid_mode(self, mock_launcher_class):
        mock_launcher = MagicMock()
        mock_launcher_class.return_value = mock_launcher
        mock_launcher.config_handler.load_config.return_value = MagicMock()

        with patch('sys.argv', ['script.py', '-m', 'invalid']):
            exit_code = cli()
        self.assertEqual(exit_code, 1)
        self.mock_logger.error.assert_called_once()

    @patch('src.cli.Launcher')
    @patch('src.cli.validate_path')
    def test_cli_invalid_path(self, mock_validate_path, mock_launcher_class):
        mock_launcher = MagicMock()
        mock_launcher_class.return_value = mock_launcher
        mock_launcher.config_handler.load_config.return_value = MagicMock()
        mock_validate_path.return_value = (False, 'Invalid path')

        with patch('sys.argv', ['script.py', '-p', 'invalid/path']):
            exit_code = cli()
        self.assertEqual(exit_code, 1)
        self.mock_logger.error.assert_called_once_with('Invalid path')

    @patch('src.cli.Launcher')
    @patch('os.getcwd')
    def test_cli_launch_warp(self, mock_getcwd, mock_launcher_class):
        mock_launcher = MagicMock()
        mock_launcher_class.return_value = mock_launcher
        mock_config = MagicMock()
        mock_config.is_launch_path_parent_process.return_value = True
        mock_launcher.config_handler.load_config.return_value = mock_config
        mock_getcwd.return_value = 'C:\\test'

        with patch('sys.argv', ['script.py', '-l']):
            exit_code = cli()
        self.assertEqual(exit_code, 0)
        mock_launcher.launch_warp.assert_called_once_with(mock_config)


if __name__ == '__main__':
    unittest.main()
