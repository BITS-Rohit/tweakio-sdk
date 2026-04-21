from typing import Any, Protocol


class ChatProtocol(Protocol):
    """Chat Interface Base Class — platform-agnostic."""

    name: str | None
    id_serialized: str | None
    ui: Any | None
    timestamp: float | int | None
