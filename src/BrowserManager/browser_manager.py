"""
BrowserManager facade for ease of use.
Provides a simple entry point for launching anti-detection browsers.
"""
import asyncio
from typing import Optional

from playwright.async_api import Page, BrowserContext

from src.BrowserManager.camoufox_browser import CamoufoxBrowser
from src.BrowserManager.browser_config import BrowserConfig
from src.BrowserManager.profile_manager import ProfileManager
from src.BrowserManager.profile_info import ProfileInfo
from src.BrowserManager.platform_manager import Platform
from src.BrowserManager.browserforge_manager import BrowserForgeCompatible
from src.custom_logger import TweakioLogger

class BrowserManager:
    """
    Main entry point for browser management.
    Handles configuration, profile selection, and browser lifecycle.
    """
    def __init__(
        self, 
        platform: str = "whatsapp", 
        profile_id: str = "default",
        headless: bool = False,
        locale: str = "en-US",
        enable_cache: bool = True
    ):
        self.logger = TweakioLogger.get_logger("tweakio")
        self.browser_logger = TweakioLogger.get_logger("tweakio.browser", log_type="browser")
        
        self.pm = ProfileManager()
        # Convert string platform to Enum if needed, but existing code uses strings often
        # Validating platform
        plat = platform.lower()
        
        if not self.pm.is_profile_exists(plat, profile_id):
            self.logger.info(f"Creating new profile: {profile_id} for {plat}")
            self.profile = self.pm.create_profile(plat, profile_id)
        else:
            self.profile = self.pm.get_profile(plat, profile_id)
            
        self.bf = BrowserForgeCompatible(log=self.browser_logger)
        
        self.config = BrowserConfig(
            platform=plat,
            locale=locale,
            enable_cache=enable_cache,
            headless=headless,
            fingerprint_obj=self.bf
        )
        
        self.browser_impl = CamoufoxBrowser(
            config=self.config,
            profileInfo=self.profile,
            log=self.browser_logger
        )
        
        # Activate profile
        self.pm.activate_profile(plat, profile_id, self.browser_impl)

    async def getPage(self) -> Page:
        """Alias for compatibility with README and existing scripts."""
        return await self.get_page()

    async def get_page(self) -> Page:
        """Returns a new or existing page."""
        return await self.browser_impl.get_page()

    async def close(self):
        """Closes the browser."""
        await self.browser_impl.close_browser()
