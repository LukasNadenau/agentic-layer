"""Centralized logging configuration with file and console handlers.

This module provides logging setup functions that configure both
Rich console output and detailed file logging for ADW.
"""
# /// script
# dependencies = [
#   "rich",
#   "python-dotenv",
# ]
# ///

import logging
from datetime import datetime
from rich.logging import RichHandler
from get_or_create_folders import get_or_create_run_folder

def setup_logging(run_id: str) -> logging.Logger:
    """
    Set up logging with both console (Rich) and file output.

    Args:
        run_id: The run identifier for log file naming

    Returns:
        Logger instance for the root logger
    """
    # Check if logging is already initialized by checking for handlers
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return root_logger

    # Create log file path
    run_folder = get_or_create_run_folder(run_id)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = run_folder / f"{run_id}_adw_{timestamp}.log"

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Console handler (INFO level, Rich formatting)
    console_handler = RichHandler(
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        show_time=False,
        show_path=False
    )
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File handler (DEBUG level, detailed formatting)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    root_logger.info("Logging initialized. Log file: %s", log_file)
    return root_logger

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module."""
    return logging.getLogger(name)
