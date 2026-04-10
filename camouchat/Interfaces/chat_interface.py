from abc import ABC
from typing import Optional, Union

from playwright.async_api import ElementHandle, Locator


class ChatInterface(ABC):
    """Chat Interface Base Class"""

    name: str
    id_serialized: str
    ui: Optional[Union[Locator, ElementHandle]]
    timestamp: float
