"""
Global Metadata enforce to every plugin to use this instead of creating their own.
provides :
- Platform
- StorageType
"""

from .platforms import Platform
from .storage_type import StorageType

__all__ = ["Platform", "StorageType"]
