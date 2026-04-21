from enum import StrEnum


class Platform(StrEnum):
    """Absolute names"""

    WHATSAPP = "WhatsApp"
    ARATTAI = "Arattai"

    @staticmethod
    def list_platforms() -> list[str]:
        """List available platforms"""
        return [p.value for p in Platform]
