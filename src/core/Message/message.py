import json

from core.Message.message_type import MessageType


class Message:
    def __init__(self, sender: int, receiver: int, messageType: int, messageContent: str, timestamps: dict, vp: dict) -> None:
        self._sender = sender
        self._receiver = receiver
        self._messageType = messageType
        self._messageContent = messageContent
        self._timestamps = timestamps
        self._vp = vp

    @classmethod
    def from_dict(cls, message):
        """
            return from dict to Message
        """
        return Message(
            message["_sender"],
            message["_receiver"],
            message["_messageType"],
            message["_messageContent"],
            message["_timestamps"],
            message["_vp"],
        )

    @classmethod
    def from_string(csl, message):
        """
            load dict from string
        """
        msgStr2Dict = json.loads(message)
        return Message.from_dict(msgStr2Dict)


    def __str__(self) -> str:
        """
            convert dict to string
        """
        return json.dumps(self.__dict__)
