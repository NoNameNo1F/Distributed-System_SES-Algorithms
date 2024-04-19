import os
import threading

from dotenv import load_dotenv

from Client.client import *
from core.Message.message_type import MessageType

if __name__ == "__main__":
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
    client = ClientYLS()
    client_yls = threading.Thread(target=client.client_run, args=())
    client_input = threading.Thread(target=client.handle_site_command, args=())
    #client_input = threading.Thread(target=handle_site_command, args=(client,))
    client_yls.daemon = True
    client_yls.start()
    client_input.start()
