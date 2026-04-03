from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class MessageModelAPI:
    """
    Normalized Data Model for a WhatsApp Message.
    Parses the raw Webpack dictionary into a clean, predictable Python object.

    Attributes:
        id_serialized (str | None): Full unique ID (e.g., 'false_1234@c.us_ABCDEF').
        rowId (int | None): IndexedDB row ID (useful for pagination/anchors).
        fromMe (bool | None): True if the message was sent by the authenticated user.
        jid_From (str | None): JID of the sender (or the Group JID if received in a group).
        jid_To (str | None): JID of the recipient.
        author (str | None): JID of the specific person who sent it (ONLY present in group chats).
        pushname (str | None): The notification name of the sender.
        broadcast (bool | None): True if sent via a Broadcast List.
        MsgType (str | None): Message type: 'chat', 'image', 'video', 'ptt', 'document', 'revoked', etc.
        body (str | None): Text content, or base64 thumbnail for media.
        caption (str | None): Text caption attached to media.
        timestamp (int | None): Unix timestamp of the message.
        ack (int | None): 0=Pending, 1=Sent, 2=Delivered, 3=Read(Blue Ticks), 4=Played.
        isNew (bool | None): True if the message is unread LOCALLY in the browser UI.
        isStarMsg (bool | None): True if the message is starred/favorited.
        isForwarded (bool | None): True if the message has the "Forwarded" tag.
        forwardsCount (int | None): Number of times this message was forwarded.
        hasReaction (bool | None): True if someone reacted to this message.
        ephemeralDuration (int | None): Disappearing message duration in seconds (0 if off).
        isAvatar (bool | None): True if message is an avatar sticker.
        isVideoCallMessage (bool | None): True if the message is a call log/missed call alert.
        fromQuotedMsg (bool | None): True if this message is a reply to another message.
        isQuotedMsgAvailable (bool | None): True if the quoted message still exists in the local database.
        quotedMsgId (str | None): The serialized ID of the message being replied to.
        quotedParticipant (str | None): The JID of the person who sent the original quoted message.
        mimetype (str | None): e.g., 'image/jpeg', 'audio/ogg; codecs=opus'.
        directPath (str | None): Decryption URL path for the CDN.
        mediaKey (str | None): Base64 encryption key for downloading media.
        size (int | None): Size of the media in bytes.
        duration (int | None): Duration in seconds (for audio/video).
        isViewOnce (bool | None): True if sent as "View Once" media.
        isQuestion (bool | None): True if this is a Poll message.
        questionResponsesCount (int | None): Number of people who voted.
        readQuestionResponsesCount (int | None): Number of read question responses (if applicable).
        stickerSentTs (int | None): Original creation timestamp for stickers (used for "Recents" sorting).
        isViewed (bool | None): Local UI state: True if the bubble no longer has the green unread dot.
        vcardList (list | None): List of vCards if MsgType == "vcard" or "multi_vcard".

    If the specified field is None , its Mostly means the webpack was not successfully patched the whatsapp.
    Or the webpack ids are changed due to silent update from whatsapp.
    """

    id_serialized: str | None
    rowId: int | None
    fromMe: bool | None
    jid_From: str | None
    jid_To: str | None
    author: str | None
    pushname: str | None
    broadcast: bool | None
    MsgType: str | None
    body: str | None
    caption: str | None
    timestamp: int | None
    ack: int | None
    isNew: bool | None
    isStarMsg: bool | None
    isForwarded: bool | None
    forwardsCount: int | None
    hasReaction: bool | None
    ephemeralDuration: int | None
    isAvatar: bool | None
    isVideoCallMessage: bool | None
    fromQuotedMsg: bool | None
    isQuotedMsgAvailable: bool | None
    quotedMsgId: str | None
    quotedParticipant: str | None
    mimetype: str | None
    directPath: str | None
    mediaKey: str | None
    size: int | None
    duration: int | None
    isViewOnce: bool | None
    isQuestion: bool | None
    questionResponsesCount: int | None
    readQuestionResponsesCount: int | None
    stickerSentTs: int | None
    isViewed: bool | None
    vcardList: list | None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MessageModelAPI":
        """
        Safely maps the raw WhatsApp WA-JS dictionary to this Python dataclass.
        Automatically handles '__x_' prefixes and nested ID fields.
        """

        def get_val(key: str, default: Any = None) -> Any:
            return data.get(key, data.get(f"__x_{key}", default))

        id_obj = get_val("id") or {}
        id_serialized = get_val("id_serialized") or id_obj.get("_serialized")
        from_me = get_val("fromMe")
        if from_me is None:
            from_me = id_obj.get("fromMe", False)

        return cls(
            id_serialized=id_serialized,
            rowId=get_val("rowId") or None,
            fromMe=from_me,
            jid_From=get_val("from") or None,
            jid_To=get_val("to") or None,
            author=get_val("author") or None,
            pushname=get_val("notifyName") or get_val("pushname") or None,
            broadcast=get_val("broadcast") or None,
            MsgType=get_val("type") or None,
            body=get_val("body") or None,
            caption=get_val("caption") or None,
            timestamp=get_val("t") or get_val("timestamp") or None,
            ack=get_val("ack", 0) or None,
            isNew=get_val("isNew") or None,
            isStarMsg=get_val("star") or None,
            isForwarded=get_val("isForwarded") or None,
            forwardsCount=get_val("forwardingScore", 0) or get_val("forwardsCount", 0) or None,
            hasReaction=get_val("hasReaction") or None,
            ephemeralDuration=get_val("ephemeralDuration", 0) or None,
            isAvatar=get_val("isAvatar") or None,
            isVideoCallMessage=get_val("isVideoCall") or None,
            fromQuotedMsg=bool(get_val("quotedMsg")) or None,
            isQuotedMsgAvailable=not get_val("quotedStanzaID")
            and bool(get_val("quotedMsg"))
            or None,
            quotedMsgId=get_val("quotedStanzaID")
            or (get_val("msgContextInfo") or {}).get("stanzaId")
            or None,
            quotedParticipant=get_val("quotedParticipant")
            or (get_val("msgContextInfo") or {}).get("participant")
            or None,
            mimetype=get_val("mimetype") or None,
            directPath=get_val("directPath") or None,
            mediaKey=get_val("mediaKey") or None,
            size=get_val("size") or get_val("fileLength") or None,
            duration=get_val("duration") or None,
            isViewOnce=get_val("isViewOnce") or None,
            isQuestion=get_val("isAnyQuestion") or (get_val("type") == "poll_creation") or None,
            questionResponsesCount=get_val("pollOptions", [])
            and len(get_val("pollOptions", []))
            or None,
            readQuestionResponsesCount=None,  # Extracted dynamically if needed via poll API
            stickerSentTs=get_val("stickerSentTs") or None,
            isViewed=get_val("viewed") or None,
            vcardList=get_val("vcardList") or None,
        )

    def __str__(self):
        return (
            f"MessageModelAPI(\n"
            f"    id_serialized={self.id_serialized!r},\n"
            f"    rowId={self.rowId},\n"
            f"    fromMe={self.fromMe},\n"
            f"    jid_From={self.jid_From!r},\n"
            f"    jid_To={self.jid_To!r},\n"
            f"    author={self.author!r},\n"
            f"    pushname={self.pushname!r},\n"
            f"    broadcast={self.broadcast},\n"
            f"    MsgType={self.MsgType!r},\n"
            f"    body={self.body!r},\n"
            f"    caption={self.caption!r},\n"
            f"    timestamp={self.timestamp},\n"
            f"    ack={self.ack},\n"
            f"    isNew={self.isNew},\n"
            f"    isStarMsg={self.isStarMsg},\n"
            f"    isForwarded={self.isForwarded},\n"
            f"    forwardsCount={self.forwardsCount},\n"
            f"    hasReaction={self.hasReaction},\n"
            f"    ephemeralDuration={self.ephemeralDuration},\n"
            f"    isAvatar={self.isAvatar},\n"
            f"    isVideoCallMessage={self.isVideoCallMessage},\n"
            f"    fromQuotedMsg={self.fromQuotedMsg},\n"
            f"    isQuotedMsgAvailable={self.isQuotedMsgAvailable},\n"
            f"    quotedMsgId={self.quotedMsgId!r},\n"
            f"    quotedParticipant={self.quotedParticipant!r},\n"
            f"    mimetype={self.mimetype!r},\n"
            f"    directPath={self.directPath!r},\n"
            f"    mediaKey={self.mediaKey!r},\n"
            f"    size={self.size},\n"
            f"    duration={self.duration},\n"
            f"    isViewOnce={self.isViewOnce},\n"
            f"    isQuestion={self.isQuestion},\n"
            f"    questionResponsesCount={self.questionResponsesCount},\n"
            f"    readQuestionResponsesCount={self.readQuestionResponsesCount},\n"
            f"    stickerSentTs={self.stickerSentTs},\n"
            f"    isViewed={self.isViewed},\n"
            f"    vcardList={self.vcardList!r},\n"
            f")"
        )

    def __repr__(self):
        return self.__str__()
