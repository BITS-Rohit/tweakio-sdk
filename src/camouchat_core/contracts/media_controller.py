from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Protocol, TypeVar

from .ui_config import UiConfigProtocol


class MediaType(StrEnum):
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
    mime_type: str | None = None
    size_bytes: int | None = None


T = TypeVar("T", bound=UiConfigProtocol)


class MediaControllerProtocol(Protocol[T]):
    """Base contract for platform-specific media operations."""

    ui_config: T

    async def add_media(self, file: FileTyped, **kwargs: Any) -> bool:
        """Upload media file to a chat."""
        ...
