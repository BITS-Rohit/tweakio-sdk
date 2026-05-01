"""src — Anti-detection WhatsApp automation SDK."""

__version__ = "0.7.0"

# Encryption
# Contracts
from .contracts import (
    ChatProcessorProtocol,
    ChatProtocol,
    InteractionControllerProtocol,
    LoginProtocol,
    MediaControllerProtocol,
    MessageProcessorProtocol,
    MessageProtocol,
    StorageProtocol,
    UiConfigProtocol,
)
from .Encryption import (
    KeyManager,
    MessageDecryptor,
    MessageEncryptor,
)
from .Exceptions import CamouChatError

# Metadata
from .global_metadata import MediaType, MessageType, Platform, StorageType

# Logging
from .logger import CamouAdapter, LoggerFactory

__all__ = [
    # Metadata
    "Platform",
    "StorageType",
    "MessageType",
    "MediaType",
    # Contracts
    "ChatProtocol",
    "MessageProtocol",
    "StorageProtocol",
    "LoginProtocol",
    "InteractionControllerProtocol",
    "MediaControllerProtocol",
    "UiConfigProtocol",
    "MessageProcessorProtocol",
    "ChatProcessorProtocol",
    # Encryption
    "MessageEncryptor",
    "MessageDecryptor",
    "KeyManager",
    # Exceptions
    "CamouChatError",
    # Logging
    "LoggerFactory",
    "CamouAdapter",
]
