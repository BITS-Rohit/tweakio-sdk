"""
Shared Resources Module for tweakio-sdk library
"""
import logging
from logging.handlers import RotatingFileHandler

from colorlog import ColoredFormatter

import directory as dirs

# ------ Logger Configs ---------
logger = logging.getLogger("tweakio")
logger.setLevel(logging.INFO)

# -------------------------------
# Console handler
# -------------------------------

console_formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s | %(levelname)s | %(message)s",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red'
    }
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# -------------------------------
# File handler with rotation
# -------------------------------
file_handler = RotatingFileHandler(
    dirs.ErrorTrace_file,  # file path
    maxBytes=20 * 1024 * 1024,  # 20 MB per file
    backupCount=3  # keep last 3 files
)
file_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# -------------------------------
# General settings
# -------------------------------
logger.propagate = False

