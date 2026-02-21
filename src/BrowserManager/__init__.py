"""
Browser Manager Class for whatsapp Module
"""
import json
import os
import pickle
import shutil
from dataclasses import asdict
from pathlib import Path
from typing import Optional, Tuple

import camoufox.exceptions
from browserforge.fingerprints import FingerprintGenerator
from camoufox.async_api import launch_options, AsyncCamoufox
from playwright.async_api import BrowserContext, Page
from src.BrowserManager.profile_info import ProfileInfo

from src import directory as dirs

from Custom_logger import logger

from src.BrowserManager.camoufox_browser import CamoufoxBrowser
from src.BrowserManager.profile_manager import ProfileManager
from src.BrowserManager.browserforge_manager import BrowserForgeCompatible
from src.BrowserManager import runtime_state

class BrowserManager:
    """
    Manages a Playwright BrowserContext instance integrated with Camoufox and BrowserForge fingerprints.

    This class ensures that the browser fingerprint matches the system's actual screen dimensions,
    and provides optional parameters to customize browser launch behavior such as locale, cache,
    headless mode, and add-ons.

    Attributes
    ----------
    fingerprint : dict, optional
        A specific BrowserForge-style fingerprint to use.
        If None, a valid fingerprint will be automatically generated or loaded from cache.
        Reference format: https://camoufox.com/

    override_fingerprint : bool, default=False
        If True, any existing stored fingerprint will be replaced with a newly generated one.

    addons : list[str], optional
        A list of paths to browser extensions (add-ons) to be installed in the browser instance.
        Also give the path to the add-ons to a list of str

    locale : str, default="en-US"
        The locale setting for the browser.

    enable_cache : bool, default=True
        Enables or disables browser caching(going forward to backward in pages).

    cache_dir : pathlib.Path, optional
        The directory used for storing browser cache and session data.
        If not provided, the default application cache directory will be used.

    headless : bool, default=True
        Runs the browser in headless (non-UI) mode if True, or with visible UI if False.

    debug_fingerprint : bool, default=False
        It saves the fingerprint to a json file for debugging

    debug_fingerprint_json_path : Path
        It saves the json to this location

    Notes
    -----
    - If no arguments are provided, the browser instance will still initialize with default settings.
    - Fingerprints are automatically validated against system screen dimensions for realism.
    - Uses Camoufox’s internal `AsyncCamoufox` launcher under the hood.

    Example
    -------
    python
    from tweakio.browser import BrowserManager

    manager = BrowserManager()
    browser = await manager.getInstance()

    page = await browser.new_page()
    await page.goto("https://example.com")
    """

    def __init__(
        self,
        addons=None,
        cache_dir_path: Path = dirs.cache_dir,
        override_cookies: bool = False,
        headless: bool = False,
        locale: str = "en-US",
        enable_cache: bool = True,
        fingerprint=None,
        override_fingerprint: bool = False,
        debug_fingerprint: bool = False,
        debug_fingerprint_json_path: Path = dirs.fingerprint_debug_json,
        profile_id: Optional[str] = None,
        platform: str = "whatsapp",
):


        if override_cookies:
            shutil.rmtree(cache_dir_path) if os.path.exists(cache_dir_path) else None

        self.debug_fingerprint_json_path = debug_fingerprint_json_path
        self.debug_fingerprint = debug_fingerprint
        self.cache_dir_path = cache_dir_path
        if addons is None:
            addons = []
        self.enable_cache = enable_cache
        self.locale = locale
        self.headless = headless
        self.addons = addons
        self.browser: Optional[BrowserContext] = None
        self.override_fingerprint = override_fingerprint
        self.fg = fingerprint
        self.profile_id = profile_id
        self.platform = platform


    async def getInstance(self) -> BrowserContext:
        """Provides the Instance of the BrowserContext."""
        if self.browser is None:
            self.browser = await self.__GetBrowser__()
        return self.browser

    """
    Handles both legacy mode (direct path usage) and
    profile mode (ProfileManager integration).

    In profile mode:
    - Auto-detects login state
    - Applies multi-profile headless override
    - Delegates browser creation to CamoufoxBrowser
    """

    async def __GetBrowser__(self, tries: int = 1) -> BrowserContext:

        # If profile mode
        if self.profile_id is not None:
            pm = ProfileManager(app_name="tweakio")
            profile = pm.get_profile(self.platform, self.profile_id)

            runtime_state.register(self.profile_id)

            if not pm.is_logged_in(self.platform, self.profile_id):
                logger.info(f"Profile '{self.profile_id}' requires login.")
                # Future: call login flow
            else:
                logger.info(f"Profile '{self.profile_id}' already logged in.")


            bf = BrowserForgeCompatible(log=logger)

            active_profiles = pm.get_active_profiles(self.platform)

            if len(active_profiles) > 0:
                effective_headless = True
            else:
                effective_headless = self.headless

            cam_browser = CamoufoxBrowser(
                profile_info=profile,
                BrowserForge=bf,
                log=logger,
                headless=effective_headless,
                locale=self.locale,
                enable_cache=self.enable_cache
            )


            self.browser = await cam_browser.getInstance()
            return self.browser

    
    async def CloseBrowser(self):
        """
        Safely close the browser and unregister runtime profile.
        """
        if self.browser:
            try:
                # Close pages safely
                for page in list(self.browser.pages):
                    try:
                        await page.close()
                    except Exception:
                        pass  # ignore page close errors

                try:
                    await self.browser.__aexit__(None, None, None)
                except Exception:
                    pass

            finally:
                from src.BrowserManager import runtime_state
                runtime_state.unregister(self.profile_id)
                self.browser = None

    async def getPage(self) -> Page:
        """
        Returns an available blank page if it exists, otherwise creates a new page.
        Automatically initializes the browser if not already initialized.
        """
        Browser = self.browser
        if Browser is None:
            Browser = await self.getInstance()

        for page in Browser.pages:
            try:
                if page.url == "about:blank":
                    return page
            except Exception as e:
                logger.warning(f"⚠️ Error checking page URL: {e}")

        try:
            new_page = await Browser.new_page()
            return new_page
        except Exception as e:
            logger.error(f"❌ Failed to create new page: {e}", exc_info=True)
            raise


def get_screen_size() -> Tuple[int, int]:
    """
    Returns the width and height of the primary display in pixels.
    Works on Windows, Linux, and macOS.
    """
    try:
        import platform
        system = platform.system()

        # ---------------- Windows ----------------
        if system == "Windows":
            import ctypes
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()  # High-DPI aware
            width = user32.GetSystemMetrics(0)
            height = user32.GetSystemMetrics(1)
            return width, height

        # ---------------- Linux ----------------
        elif system == "Linux":
            try:
                import subprocess
                out = subprocess.check_output("xdpyinfo | grep dimensions", shell=True).decode()
                dims = out.split()[1].split("x")
                return int(dims[0]), int(dims[1])
            except Exception:
                pass  # fallback to Tkinter below

        # ---------------- macOS ----------------
        elif system == "Darwin":
            try:
                import Quartz
                main_display = Quartz.CGMainDisplayID()
                width = Quartz.CGDisplayPixelsWide(main_display)
                height = Quartz.CGDisplayPixelsHigh(main_display)
                return width, height
            except Exception:
                pass  # fallback to Tkinter below

    except Exception:
        pass

    # --------------- Fallback (Tkinter) ----------------
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # hide window
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return width, height
    except Exception:
        # Default fallback if everything fails
        return 1920, 1080
