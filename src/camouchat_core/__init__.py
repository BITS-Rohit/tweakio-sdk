"""src — Anti-detection WhatsApp automation SDK."""

__version__ = "0.7.0"

# Encryption
from .Encryption import (
    MessageEncryptor,
    MessageDecryptor,
    KeyManager,
)

# Exceptions
from .Exceptions import CamouChatError

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
    MediaCapableProtocol,
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
    "MediaCapableProtocol",
    "UiConfigProtocol",
    "MessageProcessorProtocol",
    "ChatProcessorProtocol",

    # Encryption
    "MessageEncryptor",
    "MessageDecryptor",
    "KeyManager",

    # Exceptions
    "CamouChatError",
]