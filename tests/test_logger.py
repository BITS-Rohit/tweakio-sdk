import json
import logging
import sys
from unittest.mock import patch
from camouchat_core import LoggerFactory


def test_logger_initialization():
    """Test that the logger factory produces a valid adapter."""
    log = LoggerFactory.get_logger("test")
    assert isinstance(log, logging.LoggerAdapter)
    assert log.extra["platform"] == "CORE"
    assert log.extra["profile_id"] == "GLOBAL"


def test_logger_metadata_injection(caplog):
    """Test that metadata is injected into the logging record."""
    root_val = logging.getLogger("camouchat")
    root_val.addHandler(caplog.handler)
    caplog.set_level(logging.INFO, logger="camouchat")

    log = LoggerFactory.get_logger("test_meta", platform="UNIX", profile_id="Bot1")
    log.info("Hello coverage")

    assert any("Hello coverage" in r.message for r in caplog.records)
    record = [r for r in caplog.records if "Hello coverage" in r.message][0]
    assert record.platform == "UNIX"
    assert record.profile_id == "Bot1"
    root_val.removeHandler(caplog.handler)


def test_json_formatter():
    """Test that JSONFormatter outputs valid JSON with expected fields."""
    from camouchat_core.logger import JSONFormatter

    formatter = JSONFormatter()
    record = logging.LogRecord("name", logging.INFO, "path", 10, "msg", (), None)
    record.profile_id = "P"
    record.platform = "PL"

    # Test with exception
    try:
        raise ValueError("error")
    except ValueError:
        record.exc_info = sys.exc_info()

    formatted = formatter.format(record)
    data = json.loads(formatted)
    assert "exception" in data
    assert data["profile_id"] == "P"


def test_logger_singleton_handlers():
    """Test that root handlers are not duplicated."""
    LoggerFactory.get_logger("l1")
    LoggerFactory.get_logger("l2")

    root = logging.getLogger("camouchat")
    assert len(root.handlers) >= 1

    prev_handler_count = len(root.handlers)
    LoggerFactory.get_logger("l3")
    assert len(root.handlers) == prev_handler_count


def test_logger_set_level():
    """Test global level setting."""
    LoggerFactory.set_level(logging.ERROR)
    root = logging.getLogger("camouchat")
    assert root.level == logging.ERROR
    LoggerFactory.set_level(logging.INFO)


def test_logger_file_handler_setup(tmp_path):
    """Test that file handler is correctly initialized when path is provided."""
    log_file = tmp_path / "test.log"
    LoggerFactory._root_initialized = False
    LoggerFactory._handlers = {}

    log = LoggerFactory.get_logger("test_file", log_file=str(log_file), level=logging.DEBUG)
    log.info("trigger file creation")
    assert log_file.exists()

    logger = logging.getLogger("camouchat.test_file")
    assert logger.level == logging.DEBUG


def test_logger_adapter_process():
    """Test CamouAdapter.process correctly merges extra kwargs."""
    from camouchat_core.logger import CamouAdapter

    base_logger = logging.getLogger("test_adapter")
    adapter = CamouAdapter(base_logger, {"profile_id": "P1"})

    msg, kwargs = adapter.process("hello", {"extra": {"custom": "val"}})
    assert kwargs["extra"]["profile_id"] == "P1"
    assert kwargs["extra"]["custom"] == "val"


def test_logger_import_fallbacks():
    """Test the try-except import blocks for colorlog and concurrent_log_handler."""
    with patch.dict("sys.modules", {"colorlog": None, "concurrent_log_handler": None}):
        # We need to reload or re-import the module to trigger the try-except blocks
        # or just inspect the definitions if we can re-execute the module code.
        import importlib
        import camouchat_core.logger

        importlib.reload(camouchat_core.logger)

        # Verify that the fallbacks (logging.Formatter and RotatingFileHandler) were used.
        # This is a bit internal, but we can verify the assignments.
        assert camouchat_core.logger.ColoredFormatter == logging.Formatter
        assert (
            camouchat_core.logger.ConcurrentRotatingFileHandler
            == logging.handlers.RotatingFileHandler
        )

    # Restore module state for other tests!
    import camouchat_core.logger

    importlib.reload(camouchat_core.logger)
