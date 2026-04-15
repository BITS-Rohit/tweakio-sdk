"""Contracts for chat discovery and chat activation."""

from __future__ import annotations

from typing import Sequence, Protocol, TypeVar

from .chat import ChatProtocol

T = TypeVar("T", bound=ChatProtocol, covariant=True)


class ChatProcessorProtocol(Protocol[T]):
    """Base contract for components that list chats and activate a chat.

    Implementations own platform-specific state such as selectors, browser
    pages, bridge clients, and logger defaults. The interface only captures the
    behavior expected by callers.
    """

    async def fetch_chats(self, **kwargs) -> Sequence[T]:
        """Fetch available chats from the UI."""
        ...
