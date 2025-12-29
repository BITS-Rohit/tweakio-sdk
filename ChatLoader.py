"""
Chat Class for the whatsapp module
"""
import random
import time
from dataclasses import dataclass, field
from typing import Union, Optional, List

from playwright.async_api import Page, Locator, ElementHandle

import selector_config as sc
from Errors import ChatsNotFound
from Shared_Resources import logger


@dataclass
class Chat:
    """Chat class with metadata packed"""
    ChatUI: Union[ElementHandle, Locator]
    name: Optional[str] = field(default="")
    count: Optional[int] = field(default_factory=0)
    System_Hit_Time: float = field(default_factory=time.time)
    ID: Optional[str] = field(default=None)

    @staticmethod
    def _chat_key(chat: Chat) -> str:
        return str(id(chat))


async def _is_Unread(chat: Chat) -> int:
    """
    Returns:
      1 → chat has actual unread messages (numeric badge),
      0 → manually marked as unread (no numeric badge) or none,
     -1 → error occurred
    """
    try:
        chat: ElementHandle = await chat.ChatUI.element_handle(timeout=1000) \
            if isinstance(chat.ChatUI, Locator) else chat.ChatUI
        if not chat:
            return 0

        unread_badge = await chat.query_selector("[aria-label*='unread']")
        if unread_badge:
            number_span = await unread_badge.query_selector("span")
            if number_span:
                text = (await number_span.inner_text()).strip()
                return 1 if text.isdigit() else 0
        return 0
    except Exception as e:
        logger.error(f"[is_unread] Error: {e}", exc_info=True)
        return -1


class ChatLoader:
    """
    This class will contain :
    -- Chats Handling
    -- Unread / Read Markings

    """

    def __init__(self, page: Page):
        self.page = page

    @staticmethod
    async def _getWrappedChat(Max: int, page: Page) -> List["Chat"]:
        """Wraps the chats and return the list to fetcher"""
        try:
            chats = sc.chat_items(page)
            wrapped: List["Chat"] = []
            retry = 0
            while not (await chats.count()) and retry < 3:
                chats = sc.chat_items(page)
                await page.wait_for_timeout(1000)
                retry += 1

            if not (await chats.count()): return wrapped

            minimum = min(await chats.count(), Max)
            for i in range(minimum):
                wrapperChat = Chat(
                    ChatUI=chats.nth(i),
                    name=await sc.getChatName(chats.nth(i))
                )
                wrapperChat.ID = Chat._chat_key(wrapperChat)
                wrapped.append(wrapperChat)

            return wrapped
        except Exception as e:
            logger.error(f"[ChatLoader -> _getWrappedChat] Error: {e}", exc_info=True)

    async def Fetcher(self, MaxChat: int = 5):
        """
        Generator that yields chat elements and names.
        :param MaxChat: Max number of chats to process per iteration.
        """
        try:
            chatList = await ChatLoader._getWrappedChat(MaxChat, self.page)
            if not chatList:
                logger.error(f"Chat not found.")
                raise ChatsNotFound("No chats found in chat list during iteration")
            
            for chat in chatList:
                yield chat, chat.name

        except Exception as e:
            logger.critical(f"[ChatLoader] Error: {e}", exc_info=True)

    @staticmethod
    async def isUnread(chat: Chat) -> Optional[bool]:
        """
        Checks if the chat is unread or not.
        :param chat:
        :return:
        """
        chat_handle: ElementHandle = await chat.ChatUI.element_handle(timeout=1000) \
            if isinstance(chat.ChatUI, Locator) else chat.ChatUI

        i = await _is_Unread(chat=chat)
        if i == 1:
            return True
        elif i == 0:
            return None
        else:
            return False

    @staticmethod
    async def ChatClicker(chat: Chat) -> None:
        """
        clicks the chats with the correct timeout
        :param chat:
        """
        chat_handle: ElementHandle = await chat.ChatUI.element_handle(timeout=1000) \
            if isinstance(chat.ChatUI, Locator) else chat.ChatUI
        await chat_handle.click(timeout=3500)

    async def Do_Unread(self, chat: Chat) -> None:
        """
        Marks the given chat as unread by simulating right-click and selecting 'Mark as unread'.
        If already unread, logs info instead of failing.
        """
        try:
            chat_handle: ElementHandle = await chat.ChatUI.element_handle(timeout=1000) \
                if isinstance(chat.ChatUI, Locator) else chat.ChatUI
            page: Page = self.page

            if not chat_handle:
                logger.warning("[do_unread] Chat handle not found")
                return

            # Right-click on chat
            await chat_handle.click(button="right")
            await page.wait_for_timeout(random.randint(1300, 2500))  # 1.3s to 2.5s

            # Get the application menu as ElementHandle
            menu = await page.query_selector("role=application")
            if not menu:
                raise Exception("App Menu not found")

            # Look for 'Mark as unread' option inside menu
            unread_option = await menu.query_selector("li >> text=/mark.*as.*unread/i")
            if unread_option:
                await unread_option.click(timeout=random.randint(1701, 2001))
                logger.info("[do_unread] Marked as unread ✅")
            else:
                # Check if already unread
                read_option = await menu.query_selector("li >> text=/mark.*as.*read/i")
                if read_option:
                    logger.info("[do_unread] Chat already unread")
                else:
                    logger.info("[do_unread] Context menu option not found ❌")

        except Exception as e:
            logger.error(f"[do_unread] Error marking unread: {e}", exc_info=True)
            # Reset by clicking WA icon if available
            try:
                wa_icon = sc.wa_icon(page=self.page)
                if await wa_icon.count() > 0:
                    await wa_icon.first.click()
            except Exception as e:
                logger.warning(f"WA Icon Error : {e}")
