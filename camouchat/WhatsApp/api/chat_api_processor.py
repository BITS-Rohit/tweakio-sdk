from logging import Logger, LoggerAdapter

from camouchat.camouchat_logger import camouchatLogger
from .models import ChatModelAPI, MessageModelAPI
from .wa_js import WapiWrapper


class ChatApiManager:
    def __init__(self, bridge: WapiWrapper, logger: Logger | LoggerAdapter | None = None) -> None:
        self.bridge = bridge
        self.log = logger or camouchatLogger

    async def get_chat(self, chat_id: str) -> ChatModelAPI:
        """
        Fetch all the Scaled data from React memory to structured via ChatModelAPI.
        :return: ChatModelAPI
        """
        return ChatModelAPI.from_dict(await self.bridge.get_chat(chat_id=chat_id))

    async def get_chat_list(self) -> list[ChatModelAPI]:
        ...

    async def get_messages(self)-> list[MessageModelAPI]:
        ...

    async def get_msg_by_id(self, msg_id: str)-> MessageModelAPI:
        return MessageModelAPI.from_dict(await self.bridge.get_message_by_id(msg_id=msg_id))

