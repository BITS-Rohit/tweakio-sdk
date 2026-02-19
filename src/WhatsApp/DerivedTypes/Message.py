"""WhatsApp Message Class contracted with Message Interface Template"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Union, Literal, Optional

from playwright.async_api import ElementHandle, Locator

from src.WhatsApp.DerivedTypes.Chat import whatsapp_chat


@dataclass
class whatsapp_message:
    """Should inherit the protocol from Message Interface Template"""

    direction: Literal["in", "out"]
    data_id: str

    raw_data: str
    parent_chat: whatsapp_chat
    message_ui: Optional[Union[ElementHandle, Locator]]

    data_type: Optional[str] = None
    message_id: str = field(init=False)
    system_hit_time: float = field(default_factory=time.time)
    encrypted_message: Optional[str] = None
    encryption_nonce: Optional[str] = None

    def isIncoming(self) -> Optional[bool]:
        """
        Specifies the direction of message.
        returns : True if incoming else False
        """
        if self.direction == "in":
            return True
        if self.direction == "out":
            return False
        return None

    def __post_init__(self):
        self.message_id = self._message_key()

    def _message_key(self) -> str:
        return f"wa-msg::{self.data_id}"
