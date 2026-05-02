"""
Global Metadata enforce to every plugin to use this instead of creating their own.
provides :
- Platform
- StorageType
- MessageType
- MediaType
"""

from .media_type import MediaType
from .msg_type import MessageType
from .platforms import Platform
from .storage_type import StorageType

__all__ = ["Platform", "StorageType", "MessageType", "MediaType"]
