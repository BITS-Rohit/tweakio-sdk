import logging
from camouchat_core import LoggerFactory

def test_logger_initialization():
    """Test that the logger factory produces a valid adapter."""
    log = LoggerFactory.get_logger("test")
    assert isinstance(log, logging.LoggerAdapter)
    assert log.extra["platform"] == "CORE"
    assert log.extra["profile_id"] == "GLOBAL"

def test_logger_metadata_injection(caplog):
    """Test that metadata is injected into the logging record."""
    caplog.set_level(logging.INFO)
    log = LoggerFactory.get_logger("test_meta", platform="UNIX", profile_id="Bot1")
    log.info("Hello coverage")

    # Check the latest record
    record = caplog.records[-1]
    assert record.message == "Hello coverage"
    assert record.platform == "UNIX"
    assert record.profile_id == "Bot1"

def test_logger_singleton_handlers():
    """Test that root handlers are not duplicated."""
    LoggerFactory.get_logger("l1")
    LoggerFactory.get_logger("l2")
    
    root = logging.getLogger("camouchat")
    # Should have console handler
    assert len(root.handlers) >= 1
    
    # Second initialization should not add more handlers
    prev_handler_count = len(root.handlers)
    LoggerFactory.get_logger("l3")
    assert len(root.handlers) == prev_handler_count
