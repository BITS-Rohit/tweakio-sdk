from enum import StrEnum


class MessageType(StrEnum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    LOCATION = "location"
    CONTACT = "contact"
    STICKER = "sticker"
    UNKNOWN = "unknown"
    CAMOU_CIPHERTEXT = "camou-ciphertext"
    PLATFORM_CIPHERTEXT = "platform-ciphertext"
