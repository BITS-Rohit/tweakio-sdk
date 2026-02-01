"""
WhatsApp Errors.


Hierarchy:
    WhatsApp.py
    ├── ChatError
    ├──MessageError
    ├──ReplyCapableError
    ├──MediaCapableError
    └── LoginError
"""
from src.Exceptions.base import TweakioError


class WhatsAppError(TweakioError):
    """Base Class for all WhatsApp Errors"""
    pass


# ----------------- Chat Errors ----------------------------------------

class ChatError(WhatsAppError):
    """Base Class for all WhatsApp Chat Errors"""
    pass


class ChatClickError(ChatError):
    """Click Chat Error"""
    pass


class ChatNotFoundError(ChatError):
    """Chat Not Found Error"""
    pass



class ChatListEmptyError(ChatError):
    """Chat List Empty Error"""
    pass


class ChatProcessorError(ChatError):
    """Chat Processing Error"""
    pass


class ChatUnreadError(ChatError):
    """Chat Unread Error"""
    pass

class ChatMenuError(ChatUnreadError):
    """Chat Menu Error when opening the chat operation menu on WEB UI for unread/read/archive etc"""
    pass



# ----------------- Message Errors ----------------------------------------

class MessageError(WhatsAppError):
    """Base Class for all WhatsApp Message Errors"""
    pass


class MessageNotFoundError(MessageError):
    """Message Not Found Error"""
    pass


class MessageListEmptyError(MessageError):
    """Message List Empty Error"""
    pass


class MessageProcessorError(WhatsAppError):
    """Message Processor Error"""
    pass


# ----------------- Login Errors ----------------------------------------
class LoginError(WhatsAppError):
    """Base Class for all WhatsApp Login Errors"""
    pass


# ----------------- ReplyCapable Errors ----------------------------------------
class ReplyCapableError(WhatsAppError):
    """Base Class for all WhatsApp Reply Capable Errors"""
    pass


# ----------------- MediaCapable Errors ----------------------------------------
class MediaCapableError(WhatsAppError):
    """Base Class for all WhatsApp Media Capable Errors"""
    pass

class MenuError(MediaCapableError):
    """Menu Error for Media Sending"""
    pass
