from __future__ import annotations

import importlib
import logging
from pathlib import Path
from typing import Optional

import camoufox.exceptions
from browserforge.fingerprints import Fingerprint
from camoufox.async_api import AsyncCamoufox, launch_options
from playwright.async_api import Page, BrowserContext

from src.Exceptions.base import BrowserException
from src.Interfaces.browser_interface import BrowserInterface
from src.Interfaces.browserforge_capable_interface import BrowserForgeCapable


class CamoufoxBrowser(BrowserInterface):
    """
    Camoufox browser implementation with fingerprint support.
    
    Handles browser lifecycle, fingerprint loading, and retry logic for IP issues.
    Uses dependency injection for logging and fingerprint generation.
    """

    def __init__(
            # Removed old dependencies of
            # debug_fingerprint , fingerprint , debug_fingerprint_json_path, override_cookies option, override_fingerprint
            # override ones creates ambiguity and not good to overwrite.
            # As having same cookies with diff fingerprint next time , would cause mismatch error at platform side , gives potential Ban issue.
            # Better we will just create a new login for it. Clean and safe trackable path
            self,
            cache_dir_path: Path,
            fingerprint_path: Path,
        BrowserForge: BrowserForgeCapable,
            log: logging.Logger = None,
            addons=None,
            headless: bool = False,
            locale: str = "en-US",
            enable_cache: bool = True,
    ) -> None:
        """
        :param cache_dir_path: saves the browser cache dir
        :param BrowserForge: Obj of BrowserForge
        :param log: obj of logging
        :param addons: a List of str of addons downloaded path.
        they will be reflected to the browser as browser will load those addons file.
        also path given should be correct not bad. better to leave as empty but given for more safety check.
        Default to Empty List []
        :param headless: determines of browser being visible or not. Defaults to False
        :param locale: headers for site.
        :param enable_cache: good for when debugging, makes the browser to remember last/forward visited pages.
        Default is True .
        """
        if addons is None:
            addons = []
        self.BrowserForge = BrowserForge
        self.fingerprint_path = fingerprint_path
        self.cache_dir_path = cache_dir_path
        self.enable_cache = enable_cache
        self.locale = locale
        self.headless = headless
        self.addons = addons
        self.browser: Optional[BrowserContext] = None
        self.log = log

        # Path compulsory. If user want to specific , they can. Else can use from directory.py
        if self.log is None:
            raise BrowserException("Logger is missing from the browser instance.")

        if self.BrowserForge is None:
            raise BrowserException("BrowserForge is missing from the browser instance.")

        if self.cache_dir_path is None:
            raise BrowserException("Cache dir path is missing from the browser instance.")

        if self.fingerprint_path is None:
            raise BrowserException("Fingerprint path is missing from the browser instance.")

        if not self.headless:
            self.log.info("Opening Browser into visible Mode. Change headless to True for Invisible Browser.")

    async def getInstance(self, **kwargs) -> BrowserContext:
        if self.browser is None:
            self.browser = await self.__GetBrowser__()
        return self.browser

    async def __GetBrowser__(self, tries: int = 1) -> BrowserContext:
        if self.browser is not None:
            return self.browser

        if tries > 5:
            raise BrowserException("Max Camoufox IP retry attempts exceeded")

        fg: Fingerprint = self.BrowserForge.get_fg(
            profile_path=self.fingerprint_path
        )

        try:
            self.browser = await AsyncCamoufox(
                **launch_options(
                    locale=self.locale,
                    headless=self.headless,
                    humanize=True,
                    geoip=True,
                    fingerprint=fg,
                    enable_cache=self.enable_cache,
                    i_know_what_im_doing=True,
                    firefox_user_prefs={
                        "dom.event.clipboardevents.enabled": True,
                        "dom.allow_cut_copy": True,
                        "dom.allow_copy": True,
                        "dom.allow_paste": True,
                        "dom.events.testing.asyncClipboard": True,
                    },
                    main_world_eval=True,
                ),
                persistent_context=True,
                user_data_dir=self.cache_dir_path,
            ).__aenter__()

            return self.browser

        except camoufox.exceptions.InvalidIP:
            self.log.warning(
                f"Camoufox IP failed (attempt {tries}/5). Retrying..."
            )
            return await self.__GetBrowser__(tries=tries + 1)

        except Exception as e:
            raise BrowserException("Failed to launch Camoufox browser") from e

    async def get_page(self, **kwargs) -> Page:
        """
        Returns an available blank page if one exists,
        otherwise creates and returns a new page.
        Automatically initializes the browser if needed.
        """
        browser = self.browser
        if browser is None:
            browser = await self.getInstance()

        # Reuse an existing blank page if possible
        for page in browser.pages:
            try:
                if page.url == "about:blank" and not page.is_closed():
                    return page
            except Exception as e:
                self.log.warning(f"Error checking page state: {e}")

        # Otherwise create a new page
        try:
            return await browser.new_page()
        except Exception as e:
            self.log.error("Failed to create new page", exc_info=True)
            raise BrowserException("Could not create a new page") from e

    async def close_browser(self) -> bool:
        """
        Closes the browser context safely.
        Returns True if closed, False otherwise.
        """
        if self.browser is None:
            return True

        try:
            await self.browser.__aexit__(None, None, None)
            self.browser = None
            return True

        except Exception as e:
            self.log.error(f"Failed to close browser: {e}")
            return False



