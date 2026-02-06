"""
Interfaces module for Tweakio SDK.

This module provides abstract base classes and protocols that define
the contracts for platform-specific implementations.
"""
from src.Interfaces.chat_interface import ChatInterface
from src.Interfaces.message_interface import MessageInterface
from src.Interfaces.chat_processor_interface import ChatProcessorInterface
from src.Interfaces.message_processor_interface import MessageProcessorInterface
from src.Interfaces.login_interface import LoginInterface
from src.Interfaces.storage_interface import StorageInterface
from src.Interfaces.media_capable_interface import MediaCapableInterface, MediaType, FileTyped
from src.Interfaces.reply_capable_interface import ReplyCapableInterface
from src.Interfaces.humanize_operation_interface import HumanizeOperation
from src.Interfaces.web_ui_selector import WebUISelectorCapable

__all__ = [
    "ChatInterface",
    "MessageInterface",
    "ChatProcessorInterface",
    "MessageProcessorInterface",
    "LoginInterface",
    "StorageInterface",
    "MediaCapableInterface",
    "MediaType",
    "FileTyped",
    "ReplyCapableInterface",
    "HumanizeOperation",
    "WebUISelectorCapable",
]
