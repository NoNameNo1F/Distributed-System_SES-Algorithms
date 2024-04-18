from enum import Enum

"""
    MessageType: Type of messages
"""
class MessageType(Enum):
    BROADCAST = 1
    GET = 2
    READ = 3
    WRITE = 4
    START_WRITING = 5
    STOP_WRITING = 6

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
