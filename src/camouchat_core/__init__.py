"""src — Anti-detection WhatsApp automation SDK."""

__version__ = "0.7.0"

# Encryption
# Contracts
from .contracts import (
    ChatProcessorProtocol,
    ChatProtocol,
    FileTyped,
    InteractionControllerProtocol,
    LoginProtocol,
    MediaControllerProtocol,
    MediaType,
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
from .global_metadata import Platform, StorageType

# Logging
from .logger import CamouAdapter, LoggerFactory

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
