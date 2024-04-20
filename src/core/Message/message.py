import json

from core.Message.message_type import MessageType


class Message:
    def __init__(self, sender: str, receiver: str, messageType: int, messageContent: str, timestamp: dict, vp: dict) -> None:
        self._sender = sender
        self._receiver = receiver
        self._messageType = messageType
        self._messageContent = messageContent
        self._timestamp = timestamp
        self._vp = vp
    """
        return from dict to Message
    """
    def from_dict(self, message):
        return Message(
            message["sender"],
            message["receiver"],
            message["message"],
            message["timestamps"],
            message["vp"],
            message["message_type"],
        )

    """
        load dict from string
    """
    def from_string(self, message):
        return Message.from_dict(json.loads(message))
    """
        convert dict to string
    """
    def to_string(self) -> str:
        return json.dumps(self.__dict__)
