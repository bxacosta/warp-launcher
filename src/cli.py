import argparse
import logging
import sys
from pathlib import Path

from src.constants import DEFAULT_COMMAND_NAME, DEFAULT_LAUNCH_MODE, DEFAULT_LAUNCH_PATH, LOG_LEVEL
from src.enums import LaunchMode
from src.launcher import Launcher
from src.logger import setup_logger

logger = setup_logger(__name__)


def parse_cli_arguments(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        argument_default=argparse.SUPPRESS,
        description="Warp Terminal Launcher",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-m",
        "--mode",
        choices=[str(launch_mode) for launch_mode in LaunchMode],
        help=f"Select the launch mode for Warp (default: {DEFAULT_LAUNCH_MODE})",
    )

    parser.add_argument(
        "-c",
        "--command",
        type=str,
        help=f"The name of the command to start Warp (default: '{DEFAULT_COMMAND_NAME}')",
    )

    parser.add_argument(
        "-p",
        "--path",
        type=Path,
        help=f"Initial path for Warp (default: '{DEFAULT_LAUNCH_PATH}' for parent process directory).",
    )

    parser.add_argument("-l", "--launch", action="store_true", help="Start Warp with the specified configuration.")

    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")

    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        "-i",
        "--install",
        action="store_true",
        help="Save the configuration, create the launch script and register the command.",
    )
    action_group.add_argument(
        "-u", "--uninstall", action="store_true", help="Unregister the command and remove the installation directory."
    )

    # Use command-line args if not provided
    if args is None:
        args = sys.argv[1:]

    # Print help if no parameter is provided
    if not args:
        parser.print_help()
        sys.exit(0)

    return parser.parse_args(args)


def cli() -> int:
    """Main entry point for the CLI."""
    args = parse_cli_arguments()

    # Set log level based on verbosity
    logging.getLogger().setLevel(logging.DEBUG if getattr(args, "verbose", False) else LOG_LEVEL)

    try:
        launcher = Launcher()

        if getattr(args, "command", None):
            launcher.command_name = args.command

        if getattr(args, "mode", None):
            launcher.launch_mode = args.mode

        if getattr(args, "path", None):
            launcher.launch_path = args.path

        if getattr(args, "launch", False):
            launcher.launch_warp()

        if getattr(args, "install", False):
            launcher.install()

        if getattr(args, "uninstall", False):
            launcher.uninstall()
    except Exception as e:
        logger.error(e)
        return 1

    return 0
