"""
Contracts for platform & browser based plugins.
"""

from .chat import ChatProtocol
from .chat_processor import ChatProcessorProtocol
from .interaction_controller import InteractionControllerProtocol
from .login import LoginProtocol
from .media_controller import FileTyped, MediaControllerProtocol, MediaType
from .message import MessageProtocol
from .message_processor import MessageProcessorProtocol
from .storage import StorageProtocol
from .ui_config import UiConfigProtocol

__all__ = [
    "ChatProcessorProtocol",
    "ChatProtocol",
    "MessageProcessorProtocol",
    "MessageProtocol",
    "MediaControllerProtocol",
    "InteractionControllerProtocol",
    "UiConfigProtocol",
    "StorageProtocol",
    "LoginProtocol",
    "MediaType",
    "FileTyped",
]
