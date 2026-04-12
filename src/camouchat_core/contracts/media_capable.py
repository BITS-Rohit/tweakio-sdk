"""Contracts and value objects for media capabilities."""

from typing import Protocol, TypeVar

from .ui_config import UiConfigProtocol

T = TypeVar("T", bound=UiConfigProtocol)


class MediaCapableProtocol(Protocol[T]):
    """Base contract for media operations.

    Concrete implementations own platform-specific selectors, browser state,
    and logger defaults. This interface only defines the shared upload action.
    """

    ui_config: T

    async def add_media(self, **kwargs) -> bool:
        """Upload media file to a chat."""
        ...
