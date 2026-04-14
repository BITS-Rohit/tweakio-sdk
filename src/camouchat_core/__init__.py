"""src — Anti-detection WhatsApp automation SDK."""

__version__ = "0.7.0"

# Encryption
from .Encryption import (
    MessageEncryptor,
    MessageDecryptor,
    KeyManager,
)

from .Exceptions import CamouChatError

# Logging
from .logger import LoggerFactory, CamouAdapter

# Contracts
from .contracts import (
    ChatProtocol,
    MessageProtocol,
    UiConfigProtocol,
    MessageProcessorProtocol,
    ChatProcessorProtocol,
    StorageProtocol,
    LoginProtocol,
    InteractionControllerProtocol,
    MediaControllerProtocol,
    MediaType,
    FileTyped,
)

# Metadata
from .global_metadata import Platform, StorageType

__all__ = [
    # Metadata
    "Platform",
    "StorageType",
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
    "MediaType",
    "FileTyped",
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
