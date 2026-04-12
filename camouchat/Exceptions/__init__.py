"""
Exception hierarchy for camouchat operations.

Defines structured exceptions for chat operations, message handling,
authentication, storage, and platform-specific errors. All exceptions
inherit from camouchatError for consistent error handling.
"""

from camouchat.Exceptions.base import (
    CamouChatError,
    AuthenticationError,
    ElementNotFoundError,
    HumanizedOperationError,
    MessageFilterError,
    StorageError,
    BrowserException,
)
from camouchat.Exceptions.whatsapp import (
    ChatError,
    ChatNotFoundError,
    ChatClickError,
    ChatUnreadError,
    ChatProcessorError,
    ChatListEmptyError,
    ChatMenuError,
    MessageError,
    MessageNotFoundError,
    MessageListEmptyError,
    WhatsAppError,
    LoginError,
    InteractionControllerError,
    MediaCapableError,
    MenuError,
    MessageProcessorError,
)

__all__ = [
    "CamouChatError",
    "BrowserException",
    "ChatError",
    "ChatNotFoundError",
    "ChatClickError",
    "ChatUnreadError",
    "ChatProcessorError",
    "ChatListEmptyError",
    "ChatMenuError",
    "MessageError",
    "MessageNotFoundError",
    "MessageListEmptyError",
    "AuthenticationError",
    "WhatsAppError",
    "LoginError",
    "InteractionControllerError",
    "MediaCapableError",
    "MenuError",
    "MessageProcessorError",
    "ElementNotFoundError",
    "HumanizedOperationError",
    "StorageError",
    "MessageFilterError",
]
