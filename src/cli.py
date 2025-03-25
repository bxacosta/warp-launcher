import argparse
import logging
import os
import sys
from typing import List, Optional

from src.constants import PARENT_PROCESS_IDENTIFIER, LOG_LEVEL, COMMAND_NAME
from src.enums import LaunchMode
from src.launcher import Launcher
from src.logger import setup_logger
from src.utils import validate_path

logger = setup_logger(__name__)


def parse_cli_arguments(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        argument_default=argparse.SUPPRESS,
        description="Warp Terminal Launcher",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-m', '--mode',
        choices=[str(launch_mode) for launch_mode in LaunchMode],
        help="Select the launch mode for Warp."
    )

    parser.add_argument(
        '-p', '--path',
        type=str,
        help=f"Initial path for Warp (use '{PARENT_PROCESS_IDENTIFIER}' for parent process directory)."
    )

    parser.add_argument(
        '-i', '--install',
        action='store_true',
        help=f"Save the configuration, create the launch script and register the '{COMMAND_NAME}' command."
    )

    parser.add_argument(
        '-l', '--launch',
        action='store_true',
        help="Start Warp with the specified configuration."
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Enable verbose logging."
    )

    # Print help if no parameter is provided
    if args is None:
        args = sys.argv[1:]
    if not args:
        parser.print_help()
        sys.exit(0)

    return parser.parse_args(args)


def cli() -> int:
    """Main entry point for the CLI."""
    args = parse_cli_arguments()

    # Set log level based on verbosity
    logging.getLogger().setLevel(logging.DEBUG if getattr(args, "verbose", False) else LOG_LEVEL)

    launcher = Launcher()
    config = launcher.config_handler.load_config()

    # Handle launch mode parameter
    if getattr(args, "mode", None):
        selected_mode = LaunchMode.from_name(args.mode)
        if not selected_mode:
            logger.error(f"Invalid mode specified: '{args.mode}'")
            return 1
        config.launch_mode = selected_mode
        logger.info(f"Launch mode set to '{config.launch_mode}'")

    # Handle launch path parameter
    if getattr(args, "path", None):
        valid_path, error_message = validate_path(args.path)
        if not valid_path:
            logger.error(error_message)
            return 1
        config.launch_path = valid_path
        logger.info(f"Launch path set to '{config.launch_path}'")

    # Launch Warp if requested
    if getattr(args, "launch", False):
        launcher.launch_warp(config)
        resolved_path = os.getcwd() if config.is_launch_path_parent_process() else config.launch_path
        logger.info(f"Warp launched in '{config.launch_mode}' mode at '{resolved_path}'")

    # Process installation if requested
    if getattr(args, "install", False):
        success, error_message = launcher.install(config)
        if not success:
            logger.error(f"Failed to save configuration: {error_message}")
            return 1
        logger.info("Configuration saved successfully")

    return 0
