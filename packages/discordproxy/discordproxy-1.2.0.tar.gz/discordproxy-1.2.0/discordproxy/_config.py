import argparse
import logging
import logging.config
import os
from pathlib import Path
from typing import Tuple

from . import __version__, _constants

_LOG_FILE_NAME = "discordproxyserver.log"


def setup_server(args_list: list) -> Tuple[str, argparse.Namespace]:
    """Parse all command line arguments and configures logging."""
    my_args = _parse_args(args_list)
    token = (
        os.environ.get("DISCORD_BOT_TOKEN") if my_args.token is None else my_args.token
    )
    if not token:
        print("ERROR: No Discord bot token provided")
        exit(1)
    logging.config.dictConfig(_logging_config(my_args))
    return token, my_args


def _parse_args(args_list: list) -> argparse.Namespace:
    """Return parsed command line arguments."""
    my_arg_parser = argparse.ArgumentParser(
        description="Server with HTTP API for sending messages to Discord",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    my_arg_parser.add_argument(
        "--token",
        help=(
            "Discord bot token. Can alternatively be specified as "
            "environment variable DISCORD_BOT_TOKEN."
        ),
    )
    my_arg_parser.add_argument(
        "--host", default=_constants.DEFAULT_HOST, help="server host address"
    )
    my_arg_parser.add_argument(
        "--port", type=int, default=_constants.DEFAULT_PORT, help="server port"
    )
    my_arg_parser.add_argument(
        "--log-console-level",
        default="CRITICAL",
        help="Log level of log file",
        choices=["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"],
    )
    my_arg_parser.add_argument(
        "--log-file-level",
        default="INFO",
        help="Log level of log file",
        choices=["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"],
    )
    my_arg_parser.add_argument(
        "--log-file-path",
        help=(
            "Path for storing the log file. If no path if provided, "
            "the log file will be stored in the current working folder"
        ),
    )
    my_arg_parser.add_argument(
        "--version",
        help="show the program version and exit",
        action="version",
        version=__version__,
    )
    return my_arg_parser.parse_args(args_list)


def _logging_config(my_args) -> dict:
    """Generate logging configuration based on parsed args."""
    file_log_path_full = my_args.log_file_path
    filename = (
        Path(file_log_path_full) / _LOG_FILE_NAME
        if file_log_path_full
        else Path.cwd() / _LOG_FILE_NAME
    )
    print(f"Writing logfile to: {filename}")
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {"format": "[%(levelname)s] %(message)s"},
            "file": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        },
        "handlers": {
            "console": {
                "level": my_args.log_console_level,
                "formatter": "console",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",  # Default is stderr
            },
            "file": {
                "level": my_args.log_file_level,
                "formatter": "file",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(filename),
                "maxBytes": 1024 * 1024 * 10,
                "backupCount": 10,
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
            "discord": {  # discord.py library
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }
