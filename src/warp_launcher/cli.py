import argparse
import logging
import sys
from pathlib import Path

from warp_launcher.constants import DEFAULT_COMMAND_NAME, DEFAULT_LAUNCH_MODE, DEFAULT_LAUNCH_PATH, LOG_LEVEL
from warp_launcher.enums import LaunchMode
from warp_launcher.launcher import Launcher
from warp_launcher.logger import configure_logging


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


def main(args: list[str] | None = None) -> int:
    """Main entry point for the CLI."""
    parsed_args = parse_cli_arguments(args)

    # Set the log level based on verbosity
    log_level = logging.DEBUG if getattr(parsed_args, "verbose", False) else LOG_LEVEL
    configure_logging(level=log_level)

    logger = logging.getLogger(__name__)
    logger.debug("Executing main function with args: %s", parsed_args)

    try:
        launcher = Launcher()

        if getattr(parsed_args, "command", None):
            launcher.command_name = parsed_args.command

        if getattr(parsed_args, "mode", None):
            launcher.launch_mode = parsed_args.mode

        if getattr(parsed_args, "path", None):
            launcher.launch_path = parsed_args.path

        if getattr(parsed_args, "launch", False):
            launcher.launch_warp()
        elif getattr(parsed_args, "install", False):
            launcher.install()
        elif getattr(parsed_args, "uninstall", False):
            launcher.uninstall()
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e, exc_info=True)
        return 1

    return 0
