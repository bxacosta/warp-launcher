import argparse
import logging
import os
import sys
from typing import List, Optional

from src.constants import PARENT_PROCESS_IDENTIFIER, LOG_LEVEL
from src.enums import LaunchMode
from src.launcher import Launcher
from src.logger import setup_logger
from src.utils import validate_path

logger = setup_logger(__name__)


def parse_cli_arguments(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Warp Terminal Launcher",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-m', '--mode',
        choices=[mode.name.lower() for mode in LaunchMode],
        help="Select the launch mode for Warp."
    )

    parser.add_argument(
        '-p', '--path',
        type=str,
        help=f"Initial path for Warp (use '{PARENT_PROCESS_IDENTIFIER}' for the current process directory)."
    )

    parser.add_argument(
        '-i', '--install',
        action='store_true',
        help="Save the configuration and create the launch script."
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
    level = logging.DEBUG if args.verbose else LOG_LEVEL
    logging.getLogger().setLevel(level)

    launcher = Launcher()
    config = launcher.config_handler.load_config()
    logger.debug(f"Loaded configuration: {config.to_dict()}")

    # Process launch mode if provided
    if args.mode:
        selected_mode = LaunchMode.from_name(args.mode)
        if not selected_mode:
            logger.error(f"Invalid mode specified: '{args.mode}'.")
            return 1
        config.mode = selected_mode
        logger.info(f"Launch mode set to '{config.mode.name}'")

    # Validate and set the starting path if provided
    if args.path:
        valid_path, error_message = validate_path(args.path)
        if not valid_path:
            logger.error(error_message)
            return 1
        config.starting_path = valid_path
        logger.info(f"Starting path set to '{config.starting_path}'")

    # Process installation if requested
    if args.install:
        success, error_message = launcher.install(config)
        if not success:
            logger.error(f"Failed to save configuration: {error_message}")
            return 1
        logger.info("Configuration saved successfully.")

    # Launch Warp if requested
    if args.launch:
        launcher.launch_warp(config)
        resolved_path = os.getcwd() if config.is_starting_path_parent_process() else config.starting_path
        logger.info(f"Warp launched in '{config.mode.value}' mode at '{resolved_path}'.")

    return 0


if __name__ == "__main__":
    parse_cli_arguments(["-m", "tab"])
