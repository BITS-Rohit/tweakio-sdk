"""WhatsApp reply functionality with message targeting."""

from __future__ import annotations

import asyncio
import random
import weakref
from logging import Logger, LoggerAdapter
from typing import Optional, Union

from playwright.async_api import Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from camouchat.Exceptions.whatsapp import ReplyCapableError
from camouchat.Interfaces.reply_capable_interface import ReplyCapableInterface
from camouchat.WhatsApp.human_interaction_controller import HumanInteractionController
from camouchat.WhatsApp.models.message import Message
from camouchat.WhatsApp.web_ui_config import WebSelectorConfig


class ReplyCapable(ReplyCapableInterface[Message, HumanInteractionController, WebSelectorConfig]):
    """Enables replying to specific WhatsApp messages."""

    _instances: weakref.WeakKeyDictionary[Page, ReplyCapable] = weakref.WeakKeyDictionary()
    _initialized: bool = False

    def __new__(cls, *args, **kwargs) -> ReplyCapable:
        page = kwargs.get("page") or (args[0] if args else None)
        if page is None:
            return super(ReplyCapable, cls).__new__(cls)
        if page not in cls._instances:
            instance = super(ReplyCapable, cls).__new__(cls)
            cls._instances[page] = instance
        return cls._instances[page]

    def __init__(
        self,
        page: Page,
        ui_config: WebSelectorConfig,
        log: Optional[Union[LoggerAdapter, Logger]] = None,
    ) -> None:
        if hasattr(self, "_initialized") and self._initialized:
            return
        super().__init__(page=page, log=log, ui_config=ui_config)
        if self.page is None:
            raise ValueError("page must not be None")
        self._initialized = True

    async def reply(
        self,
        message: Message,
        humanize: HumanInteractionController,
        text: Optional[str],
        **kwargs,
    ) -> bool:
        """Reply to a message with optional text."""
        try:
            await self._side_edge_click(message)

            in_box = self.UIConfig.message_box()
            await in_box.click(timeout=3000)

            text = text or ""
            success = await humanize.typing(
                source=await in_box.element_handle(timeout=1000), text=text
            )

            if success:
                await self.page.keyboard.press("Enter")

            return success

        except PlaywrightTimeoutError as e:
            raise ReplyCapableError("reply timed out while preparing input box") from e

    async def _side_edge_click(self, message: Message) -> bool:
        """Double-click on message edge to trigger reply action.

        Strategy — avoid Playwright's internal ElementHandle chain:
        - `Locator.scroll_into_view_if_needed()` internally calls `_with_element()`
          which snapshots an ElementHandle. WhatsApp's virtual-scroll unmounts the
          node mid-action → "not attached to DOM". Same applies to `bounding_box()`.
        - Fix: use raw JavaScript for scroll + dimension lookup (both bypass the
          ElementHandle chain entirely), then `locator.click()` which has built-in
          retry / wait-for-stability semantics.
        - An outer retry loop with a short sleep covers the brief window where
          WhatsApp re-renders a node to update message status ticks (✓ → ✓✓).
        """
        if message is None or not message.data_id:
            raise ReplyCapableError("Message or data_id is missing.")

        data_id = str(message.data_id)
        is_incoming = getattr(message, "direction", "IN") == "IN"

        retries = 20
        delay = 1.0

        for attempt in range(1, retries + 1):
            try:
                # ── Step 1: Get dimensions via JS (no ElementHandle) ──────────
                dims = await self.page.evaluate(
                    """(id) => {
                        const el = document.querySelector(`div[data-id="${id}"]`);
                        if (!el) return null;
                        el.scrollIntoView({ behavior: 'instant', block: 'center' });
                        
                        const r = el.getBoundingClientRect();
                        return { x: r.left, y: r.top, width: r.width, height: r.height };
                    }""",
                    data_id,
                )

                # ── Step 2: Calculate absolute CDP coordinates ───────────────
                if dims and dims.get("width") and dims.get("height"):
                    # Calculate click target: 20% from left for IN, 20% from right (80%) for OUT
                    rel_x = dims["width"] * (0.2 if is_incoming else 0.8)
                    rel_y = dims["height"] / 2

                    abs_x = dims["x"] + rel_x
                    abs_y = dims["y"] + rel_y

                    # ── Step 3: CDP Double Click ───────────────────────────────
                    self.log.debug(
                        f"[side_edge_click] Attempt {attempt}/{retries}: "
                        f"Double-clicking CDP coordinates ({abs_x}, {abs_y})"
                    )
                    await self.page.mouse.click(
                        x=abs_x, y=abs_y, click_count=2, delay=random.randint(55, 70)
                    )
                    await self.page.wait_for_timeout(500)
                    return True
                else:
                    self.log.debug(
                        f"[side_edge_click] Attempt {attempt}/{retries}: "
                        f"Message '{data_id}' not found in DOM."
                    )

                if attempt < retries:
                    await asyncio.sleep(delay)
                else:
                    raise ReplyCapableError(f"side_edge_click failed after {retries} attempts.")

            except ReplyCapableError:
                raise

            except Exception as e:
                self.log.error(f"[side_edge_click] Error on attempt {attempt}: {e}")
                if attempt < retries:
                    await asyncio.sleep(delay)
                else:
                    raise ReplyCapableError(f"Unexpected error in side_edge_click: {e}") from e

        raise ReplyCapableError("side_edge_click failed after max attempts.")
