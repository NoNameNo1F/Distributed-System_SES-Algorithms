
from core.Message.message_type import MessageType


class Message:
    def __init__(self, sender: int, receiver: int, messageType: MessageType, timestamp: list, vp: dict, messageContent: str) -> None:
        self._sender = sender
        self._receiver = receiver
        self._messageType = messageType
        self._timestamp = timestamp
        self._vp = vp
        self._messageContent = messageContent
