import json
import os
import sys
import threading

from dotenv import load_dotenv

from Client.client import *
from core.Message.message_type import MessageType


# #client()
    # # for a in MessageType:
    # #     print(str(a.name).lower())
    # command = 'read'
    # if command in MessageType.to_dict():
    #     print("trueaaa")
    # if command in MessageType.to_list():
    #     print("trueaaaaa")
    # for i in MessageType.to_list():
    #     print(i)
    # # if command in str(MessageType.name).lower():
    # #     print("true")
def jsonstring_to_dict(data: dict) -> dict:
        dict = {}
        for key, value in data.items():
            key = tuple(eval(key))
            dict[key] = value
        return dict
if __name__ == "__main__":
    print(MessageType.MOUNT)
