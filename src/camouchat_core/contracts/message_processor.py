"""Contracts for message extraction and normalization."""

from collections.abc import Sequence
from typing import Protocol, TypeVar

from .chat import ChatProtocol
from .message import MessageProtocol

T = TypeVar("T", bound=MessageProtocol, covariant=True)
C = TypeVar("C", bound=ChatProtocol, contravariant=True)


class MessageProcessorProtocol(Protocol[T, C]):
    """Contract for message processors.

    Defines a standard interface for fetching and normalizing messages
    from a given chat source.

    Implementations are responsible for:
    - Deciding how messages are retrieved (DOM, API, cache, etc.)
    - Handling retries and transient failures
    - Returning messages conforming to MessageProtocol

    The generic type `T` allows implementations to return specialized
    message types while still adhering to the base MessageProtocol.
    """

    async def fetch_messages(self, chat: C, **kwargs) -> Sequence[T]:
        """Fetch messages from a given chat.

        Args:
            chat: Target chat instance implementing ChatProtocol
            **kwargs: Additional implementation-specific parameters

        Returns:
            List[T]: A list of messages conforming to MessageProtocol (or subtype)
        """
        ...
