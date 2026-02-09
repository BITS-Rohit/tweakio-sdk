"""
Abstract interfaces and protocols for tweakio components.

These interfaces define contracts that platform-specific implementations
must follow, enabling clean separation between core logic and platform integrations.
"""
from .chat_interface import ChatInterface
from .chat_processor_interface import ChatProcessorInterface
from .humanize_operation_interface import HumanizeOperationInterface
from .login_interface import LoginInterface
from .message_interface import MessageInterface
from .media_capable_interface import MediaCapableInterface
from .reply_capable_interface import ReplyCapableInterface
from .storage_interface import StorageInterface
from .web_ui_selector import WebUISelectorCapable

__all__ = [
    'ChatInterface',
    'ChatProcessorInterface',
    'HumanizeOperationInterface',
    'LoginInterface',
    'MessageInterface',
    'MediaCapableInterface',
    'ReplyCapableInterface',
    'StorageInterface',
    'WebUISelectorCapable'
]

