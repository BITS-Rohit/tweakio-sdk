from enum import StrEnum


class MediaType(StrEnum):
    """Supported media types for upload across all platforms."""

    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"