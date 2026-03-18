"""Abstract base class for media upload functionality."""

from logging import Logger, LoggerAdapter
from camouchat.camouchat_logger import camouchatLogger
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Generic, Optional, TypeVar, Union

from playwright.async_api import Page

from camouchat.Interfaces.web_ui_selector import WebUISelectorCapable

T = TypeVar("T", bound=WebUISelectorCapable)


class MediaType(str, Enum):
    """Supported media types for upload."""

    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"


@dataclass(frozen=True)
class FileTyped:
    """File metadata for media upload."""

    uri: str
    name: str
    mime_type: Optional[str] = None
    size_bytes: Optional[int] = None


class MediaCapableInterface(ABC, Generic[T]):
    """Base interface for media upload operations."""

    UIConfig: T

    @abstractmethod
    def __init__(
        self,
        page: Page,
        log: Optional[Union[Logger, LoggerAdapter]],
        UIConfig: T,
        **kwargs,
    ):
        self.page = page
        self.log = log or camouchatLogger
        self.UIConfig = UIConfig

    @abstractmethod
    async def add_media(self, mtype: MediaType, file: FileTyped, **kwargs) -> bool:
        """Upload media file to a chat."""
        ...
