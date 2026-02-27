from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from src.BrowserManager.platform_manager import Platform
from src.Interfaces.browserforge_capable_interface import BrowserForgeCapable


# Here we will add a new BrowserConfig data class
# this would help us to override the data and clean abstraction
@dataclass
class BrowserConfig:
    """
    Config dataclass for browser.
    """
    # This can be extended this way for further capabilities
    # we are using real OS which is os bound process ,
    # removing these prefs won't harm the browser & maintain stealth better
    # we would need then async locking for OS bound pasting
    # {
    #     "dom.event.clipboardevents.enabled": True,
    #     "dom.allow_cut_copy": True,
    #     "dom.allow_copy": True,
    #     "dom.allow_paste": True,
    #     "dom.events.testing.asyncClipboard": True,
    # }
    platform: Platform
    locale: str
    enable_cache: bool
    headless: bool
    fingerprint_obj: BrowserForgeCapable
    prefs: Optional[Dict[str, bool]] = None
    addons: List[str] = field(default_factory=list)


