"""
Central Logger Configuration for tweakio-sdk
"""

import logging
from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter
from src.directory import DirectoryManager


# --------------------------------------------------
# Initialize Directory Manager
# --------------------------------------------------
_directory = DirectoryManager()

log_file_path = _directory.get_log_root() / "tweakio.log"
log_file_path.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Create Main Logger
# --------------------------------------------------
logger = logging.getLogger("tweakio")
logger.setLevel(logging.INFO)
logger.propagate = False


# --------------------------------------------------
# Console Handler (Colored)
# --------------------------------------------------
if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):

    console_formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)s | %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)


# --------------------------------------------------
# File Handler (Rotating)
# --------------------------------------------------
file_handler = RotatingFileHandler(
    filename=log_file_path,
    maxBytes=20 * 1024 * 1024,  # 20MB
    backupCount=3,
    encoding="utf-8",
)

file_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
