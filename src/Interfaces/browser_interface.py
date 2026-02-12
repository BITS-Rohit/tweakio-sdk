"""
Browser abstraction interface.

Defines the core contract for browser lifecycle management.
Any browser implementation (Camoufox, Playwright, etc.) must implement this.
"""

from abc import ABC, abstractmethod

from playwright.async_api import BrowserContext, Page


class BrowserInterface(ABC):
    """
    Base interface for browser operations.
    
    Implementations handle browser initialization, page management, and cleanup.
    """

    @abstractmethod
    async def getInstance(self, **kwargs) -> BrowserContext:
        """Get or create the browser context instance."""
        ...

    @abstractmethod
    async def close_browser(self) -> bool:
        """Close the browser context. Returns True if successful."""
        ...

    @abstractmethod
    async def get_page(self, **kwargs) -> Page:
        """Get an available page or create a new one."""
        ...