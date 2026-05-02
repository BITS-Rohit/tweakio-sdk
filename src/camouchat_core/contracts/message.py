from typing import Any, Protocol, runtime_checkable

from camouchat_core.global_metadata.msg_type import MessageType

from .chat import ChatProtocol


@runtime_checkable
class MessageProtocol(Protocol):
    """Message Interface Base Class — platform-agnostic."""

    timestamp: float | int | None
    body: str | None
    msgtype: str | MessageType | None
    from_chat: ChatProtocol | str
    ui: Any | None
    id_serialized: str | None
    encryption_nonce: bytes | None
