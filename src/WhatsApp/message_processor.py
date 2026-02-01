"""WhatsApp message processor with storage and filtering support."""
from __future__ import annotations

import logging
from typing import List, Optional, Sequence

from playwright.async_api import Page

from src.Decorators.Chat_Click_decorator import ensure_chat_clicked
from src.Exceptions.whatsapp import MessageNotFoundError, WhatsAppError, MessageProcessorError, MessageListEmptyError
from src.FIlter.message_filter import MessageFilter
from src.Interfaces.message_processor_interface import MessageProcessorInterface
from src.Interfaces.storage_interface import StorageInterface
from src.WhatsApp.DerivedTypes.Chat import whatsapp_chat
from src.WhatsApp.DerivedTypes.Message import whatsapp_message
from src.WhatsApp.chat_processor import ChatProcessor
from src.WhatsApp.web_ui_config import WebSelectorConfig


class MessageProcessor(MessageProcessorInterface):
    """Extracts and processes messages from WhatsApp Web UI."""

    def __init__(
            self,
            storage_obj: Optional[StorageInterface],
            filter_obj: Optional[MessageFilter],
            chat_processor: ChatProcessor,
            page: Page,
            log: logging.Logger,
            UIConfig: WebSelectorConfig
    ) -> None:
        super().__init__(
            storage_obj=storage_obj,
            filter_obj=filter_obj,
            log=log,
            page=page,
            UIConfig=UIConfig)
        self.chat_processor = chat_processor
        if self.page is None:
            raise ValueError("page must not be None")

    @staticmethod
    async def sort_messages(msgList: Sequence[whatsapp_message], incoming: bool) -> List[whatsapp_message]:
        """Filter messages by direction (incoming or outgoing)."""
        if not msgList:
            raise MessageListEmptyError("Empty list passed in sort messages.")

        if incoming:
            return [msg for msg in msgList if msg.direction == "in"]
        return [msg for msg in msgList if msg.direction == "out"]

    @ensure_chat_clicked(lambda self, chat: self.chat_processor._click_chat(chat))
    async def _get_wrapped_Messages(
            self,
            chat: whatsapp_chat,
            retry: int = 3, *args, **kwargs) \
            -> List[whatsapp_message]:

        wrapped_list: List[whatsapp_message] = []
        try:
            sc = self.UIConfig
            all_Msgs = await sc.messages()
            count = await all_Msgs.count()
            c = 0
            while c < retry and count == 0:
                all_Msgs = await sc.messages()
                count = await all_Msgs.count()
                c += 1

            if not count:
                raise MessageNotFoundError("Messages Not able to extract")

            for i in range(count):
                msg = all_Msgs.nth(i)
                text = await sc.get_message_text(msg)
                data_id = await sc.get_dataID(msg)

                c2 = 0
                while not data_id and c2 < 3:
                    data_id = await sc.get_dataID(msg)
                    c2 += 1

                if not data_id:
                    self.log.debug("Data ID in WA / get wrapped Messages , None/Empty. Skipping")
                    continue

                wrapped_list.append(
                    whatsapp_message(
                        message_ui=msg,
                        direction="in" if await msg.locator(".message-in").count() > 0 else "out",
                        raw_data=text,
                        parent_chat=chat,
                        data_id=data_id
                    )
                )

            return wrapped_list
        except WhatsAppError as e:
            raise MessageProcessorError("failed to wrap messages") from e

    async def Fetcher(self, chat: whatsapp_chat, retry: int, *args, **kwargs) -> List[whatsapp_message]:
        """Fetch, store, and filter messages from a chat."""
        msgList = await self._get_wrapped_Messages(chat, retry, *args, **kwargs)

        if self.storage and msgList:
            new_msgs = [
                msg for msg in msgList
                if not self.storage.check_message_if_exists(msg.message_id)
            ]
            if new_msgs:
                await self.storage.enqueue_insert(new_msgs)
                self.log.debug(f"Enqueued {len(new_msgs)}/{len(msgList)} new messages for storage.")

        if self.filter:
            msgList = self.filter.apply(msgList)

        return msgList
