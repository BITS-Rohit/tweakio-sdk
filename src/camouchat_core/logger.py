import json
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, Optional, Union

try:
    from colorlog import ColoredFormatter
except ImportError:
    ColoredFormatter = logging.Formatter  # type: ignore

try:
    from concurrent_log_handler import ConcurrentRotatingFileHandler
except ImportError:
    ConcurrentRotatingFileHandler = RotatingFileHandler  # type: ignore


class JSONFormatter(logging.Formatter):
    """Formatter that outputs log records as JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Add profile/process metadata if present
        for attr in ["profile_id", "process_id", "platform"]:
            if hasattr(record, attr):
                log_record[attr] = getattr(record, attr)

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)


class CamouAdapter(logging.LoggerAdapter):
    """
    Adapter that ensures profile_id, platform, and process_id are always present.
    """

    def process(self, msg: Any, kwargs: Any) -> tuple[Any, Any]:
        extra = dict(self.extra) if self.extra else {}
        if "extra" in kwargs:
            extra.update(kwargs["extra"])
        kwargs["extra"] = extra
        return msg, kwargs


class LoggerFactory:
    """
    Centralizing logging infrastructure for all CamouChat plugins.
    Ensures standard formatting, rotation, and colors.
    """

    LOG_FORMAT = "%(asctime)s | %(levelname)s | [%(platform)s][%(profile_id)s][%(process_id)s] | %(name)s | %(message)s"
    COLOR_FORMAT = (
        "%(log_color)s%(asctime)s | %(levelname)s | [%(platform)s][%(profile_id)s] | %(message)s"
    )

    _root_initialized = False
    _handlers: Dict[str, logging.Handler] = {}

    @classmethod
    def set_level(cls, level: Union[int, str]) -> None:
        """Globally sets the logging level for the camouchat namespace."""
        logging.getLogger("camouchat").setLevel(level)

    @classmethod
    def get_logger(
        self,
        name: str,
        platform: str = "CORE",
        profile_id: str = "GLOBAL",
        log_file: Optional[str] = None,
        level: Optional[Union[int, str]] = None,
    ) -> logging.LoggerAdapter:
        """
        Retrieves a contextual logger for a specific module or profile.

        Args:
            name: Sub-logger name (e.g. 'browser', 'whatsapp')
            platform: Platform identifier
            profile_id: Unique ID for the active profile
            log_file: Optional file path for persistent logs
            level: Optional level override for this specific logger
        """
        logger_name = f"camouchat.{name}"
        logger = logging.getLogger(logger_name)

        if not self._root_initialized:
            self._setup_root_handlers(log_file)
            self._root_initialized = True

        if level:
            logger.setLevel(level)

        adapter = CamouAdapter(
            logger,
            {
                "platform": platform,
                "profile_id": profile_id,
                "process_id": os.getpid(),
            },
        )
        return adapter

    @classmethod
    def _setup_root_handlers(cls, log_file: Optional[str] = None) -> None:
        root = logging.getLogger("camouchat")
        root.setLevel(logging.INFO)
        root.propagate = False

        # Console Handler
        if "console" not in cls._handlers:
            c_handler = logging.StreamHandler(sys.stdout)
            c_formatter = ColoredFormatter(
                cls.COLOR_FORMAT,
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            )
            c_handler.setFormatter(c_formatter)
            root.addHandler(c_handler)
            cls._handlers["console"] = c_handler

        # File Handler (Optional)
        if log_file and "file" not in cls._handlers:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            f_handler = ConcurrentRotatingFileHandler(
                log_file, maxBytes=10 * 1024 * 1024, backupCount=5
            )
            f_handler.setFormatter(logging.Formatter(cls.LOG_FORMAT))
            root.addHandler(f_handler)
            cls._handlers["file"] = f_handler
