from enum import Enum
from dataclasses import dataclass
from typing import Protocol, TypeVar, Any, Optional

from .ui_config import UiConfigProtocol


class MediaType(str, Enum):
    """Supported media types for upload across all platforms."""

    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"


@dataclass(frozen=True)
class FileTyped:
    """Standard file metadata for media operations."""

    uri: str
    name: str
    mime_type: Optional[str] = None
    size_bytes: Optional[int] = None


T = TypeVar("T", bound=UiConfigProtocol)


class MediaControllerProtocol(Protocol[T]):
    """Base contract for platform-specific media operations."""

    ui_config: T

    async def add_media(self, file: FileTyped, **kwargs: Any) -> bool:
        """Upload media file to a chat."""
        ...
