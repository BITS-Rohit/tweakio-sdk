"""
WapiSession maintains all the other Core Internal Managers. 
Managers : 
    - ChatApiManager
    - MessageApiManager
    - CoreBridge
"""
from camouchat.WhatsApp.wa_js import WapiWrapper
from playwright.async_api import Page
from .chat_api_processor import ChatApiManager
from .msg_api_processor import MessageApiManager
from camouchat.camouchat_logger import camouchatLogger

class WapiSession: 
    # Todo , Initiate WapiSession with weakref to maintain Obj Singleton
    def __init__(self, page : Page) :
        self.page = page
        self.bridge = WapiWrapper(page)
        self.chat_manager = ChatApiManager(self.bridge, camouchatLogger)
        self.message_manager = MessageApiManager(self.bridge, camouchatLogger)
        self.log = camouchatLogger
        self.is_ready = False

    async def start(self): 
        self.log.info("WapiSession starting...")
        flag = await self.bridge.wait_for_ready()

        if flag : 
            self.is_ready = True
            await self.message_manager._setup_bridge()
            self.log.info("WapiSession is ready to use.")
        else :
            self.log.error("""
            Wapi Session failed to establish the connection. Please consider restarting the browser.
            If issuer persists consider creating a new profile.
            """)
        # create wpp instance ready in Browser.
        # Create the MessageEventListener Setup in browser.
        # provide more wapi.chatmanager. functions , same for msgmanager. functions

    async def stop(self):
        await self.message_manager.stop_bridge()
        self.is_ready = False
        self.log.info("WapiSession stopped successfully")
