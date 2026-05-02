from typing import Any, Protocol, TypeVar

from .ui_config import UiConfigProtocol

T = TypeVar("T", bound=UiConfigProtocol)


class MediaControllerProtocol(Protocol[T]):
    """Base contract for platform-specific media operations."""

    ui_config: T

    async def add_media(self, file: Any, **kwargs: Any) -> bool:
        """Upload media file to a chat."""
        ...
