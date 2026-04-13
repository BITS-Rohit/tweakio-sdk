"""
Contracts for platform & browser based plugins.
"""

from .chat_processor import ChatProcessorProtocol
from .chat import ChatProtocol
from .message_processor import MessageProcessorProtocol
from .message import MessageProtocol
from .meda_controller import MediaControllerProtocol
from .interaction_controller import InteractionControllerProtocol
from .ui_config import UiConfigProtocol
from .storage import StorageProtocol
from .login import LoginProtocol

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
]
