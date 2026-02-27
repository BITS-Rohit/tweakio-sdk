from enum import Enum
from typing import List


# Introducing a Platform dataclass to absolute the platform name for naming issues fixing
# Example right now platform : str -> can be whatsapp , WhatsAPP etc anything . It is not absolute to a fixed name.

class Platform(str, Enum):
    """Absolute names"""
    WHATSAPP = "WhatsApp"
    ARATTAI = "Arattai"

    @staticmethod
    def list_platforms() -> List[str]:
        """List available platforms"""
        return [p.value for p in Platform]
