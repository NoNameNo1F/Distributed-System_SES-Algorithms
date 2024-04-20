from enum import Enum

"""
    MessageType: Type of messages
"""
class MessageType(Enum):
    MOUNT = 1
    READ = 2
    WRITE = 3
    START_WRITING = 4
    STOP_WRITING = 5

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
