from enum import Enum

"""
    MessageType: Type of messages
"""
class MessageType(Enum):
    # Type when sending a message
    SEND_MOUNT = 1
    SEND_READ = 2
    SEND_WRITE = 3
    SEND_START_WRITING = 4
    SEND_STOP_WRITING = 5

    # Type When receiving a message and then reply back
    RECEIVE_MOUNT = -1
    RECEIVE_READ = -2
    RECEIVE_WRITE = -3
    RECEIVE_START_WRITING = -4
    RECEIVE_STOP_WRITING = -5

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
