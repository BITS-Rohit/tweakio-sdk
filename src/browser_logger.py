"""
Browser-specific logging module for Tweakio SDK.

This module provides a separate logger for browser operations,
allowing fine-grained control over browser-related log output
without cluttering the main application logs.
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from colorlog import ColoredFormatter

import directory as dirs


def create_browser_logger(
    name: str = "tweakio.browser",
    log_file: Optional[Path] = None,
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 3,
) -> logging.Logger:
    """
    Create a dedicated logger for browser operations.

    This logger is separate from the main application logger, allowing:
    - Different log levels for browser vs application logs
    - Separate log files for easier debugging
    - Option to disable browser logs without affecting app logs

    Args:
        name: Logger name (default: "tweakio.browser")
        log_file: Path to log file (default: browser.log in log directory)
        console_level: Console logging level (default: INFO)
        file_level: File logging level (default: DEBUG)
        max_bytes: Max size per log file before rotation (default: 10MB)
        backup_count: Number of backup files to keep (default: 3)

    Returns:
        Configured Logger instance for browser operations

    Example:
        >>> from src.browser_logger import create_browser_logger
        >>> browser_log = create_browser_logger()
        >>> browser_log.info("Browser launched")
        >>> browser_log.debug("Fingerprint generated: {...}")
    """
    logger = logging.getLogger(name)

    # Prevent duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Console handler with colors
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s | BROWSER | %(levelname)s | %(message)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'blue',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red'
        }
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler with rotation
    if log_file is None:
        log_file = dirs.log_dir / "browser.log"

    # Ensure directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setLevel(file_level)
    file_formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger


# Pre-configured browser logger instance
browser_logger = create_browser_logger()
