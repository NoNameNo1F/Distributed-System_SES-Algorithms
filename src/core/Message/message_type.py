from enum import Enum

"""
    MessageType: Type of messages
"""
class MessageType(Enum):
    # Type when sending a message
    SEND_MOUNT = 1
    SEND_READ = 2
    SEND_WRITE = 3


    # Type When receiving a message and then reply back
    RECEIVE_MOUNT = -1
    RECEIVE_READ = -2
    RECEIVE_WRITE = -3

    def to_dict() -> dict:
        dict = {}
        for item in MessageType:
            dict[item.name.lower()] = item.value
        return dict

    def to_list() -> list:
        list = []
        for item in MessageType:
            list.append(item.name.lower())
        return list

    def get_messagetype_by_index(index) -> str:
        match index:
            case MessageType.SEND_MOUNT.value:
                return MessageType.SEND_MOUNT.name

            case MessageType.RECEIVE_MOUNT.value:
                return MessageType.RECEIVE_MOUNT.name

            case MessageType.SEND_READ.value:
                return MessageType.SEND_READ.name

            case MessageType.RECEIVE_READ.value:
                return MessageType.RECEIVE_READ.name

            case MessageType.SEND_WRITE.value:
                return MessageType.SEND_WRITE.name

            case MessageType.RECEIVE_WRITE.value:
                return MessageType.RECEIVE_WRITE.name
