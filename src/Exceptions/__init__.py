"""Tweakio SDK Exceptions Package"""
from src.Exceptions.base import (
    TweakioError,
    AuthenticationError,
    ElementNotFoundError,
    HumanizedOperationError,
)
from src.Exceptions.whatsapp import (
    ChatError,
    ChatNotFoundError,
    ChatClickError,
    ChatUnreadError,
    ChatProcessorError,
    MessageError,
    MessageNotFoundError,
    MessageListEmptyError,
    WhatsAppError,
    LoginError,
    ReplyCapableError,
    MediaCapableError,
    MenuError,
    MessageProcessorError,
)

__all__ = [
    "TweakioError",
    "ChatError",
    "ChatNotFoundError",
    "ChatClickError",
    "ChatUnreadError",
    "ChatProcessorError",
    "MessageError",
    "MessageNotFoundError",
    "MessageListEmptyError",
    "AuthenticationError",
    "WhatsAppError",
    "LoginError",
    "ReplyCapableError",
    "MediaCapableError",
    "MenuError",
    "MessageProcessorError",
    "ElementNotFoundError",
    "HumanizedOperationError",
]
