"""
    logging writes into file with specifics info, error, warn,...

"""
import os
from datetime import datetime

from core.Message.message import Message
from core.Message.message_type import *
from core.Message.message_type import MessageType

from .helpers import *


class Logging:
    def __init__(self, dir, filename, file_log_time):
        self._path = get_data_file_path(dir, filename)
        self._path_log = get_data_file_path(dir, file_log_time)

    def Log(self, message, status):
        if status in ["ERROR", "INFO", "WARNING"]:
            # print(f"{datetime.now().strftime('%m-%d-%Y %I:%M:%S.%f %p')} - {status} - {message}\n")
            os.makedirs(os.path.dirname(self._path), exist_ok=True)
            with open(self._path, "a+") as output_file:
                output_file.write(f"{datetime.now().strftime('%m-%d-%Y %I:%M:%S.%f %p')} - {status} - {message}\n")

    def Log_Sent(self, message: Message, status):
        if status in ["SEND_MOUNT", "RECEIVE_MOUNT", "SEND_READ", "RECEIVE_READ", "SEND_WRITE", "RECEIVE_WRITE"]:
            print(f"[{status}]\t[{message._sender} -> {message._receiver}]\t[{message._timestamps}]\n")
            os.makedirs(os.path.dirname(self._path_log), exist_ok=True)
            with open(self._path_log, "a+") as output_file:
                output_file.write(f"[{status}]\t[{message._sender} -> {message._receiver}]\t[{message._timestamps}]\n")
            output_file.close()

            # os.makedirs(os.path.dirname(self._path_log), exist_ok=True)
            # with open(self._path_log, "a+") as output_file:
            #     output_file.write(f"[{status}]\t[{message._sender} -> {message._receiver}]\t[{message._vp}]\n")
            # output_file.close()

    def Log_Received(self, sender: int, receiver: int, timestamps: dict, vp: dict, messageType: int):
        status = MessageType.get_messagetype_by_index(messageType)
        if messageType > 0:
            # Receiving a RequestMessage
            print(f"RECEIVED_REQ\t[{status}]\t[{sender} -> {receiver}]\t[{timestamps}]\n")

            os.makedirs(os.path.dirname(self._path_log), exist_ok=True)
            with open(self._path_log, "a+") as output_file:
                output_file.write(f"RECEIVED_REQ\t[{status}]\t[{sender} -> {receiver}]\t[{timestamps}]\n")
                #output_file.write(f"RECEIVED_REQ\t[{status}]\t[{sender} -> {receiver}]\t[{vp}]\n")
            output_file.close()

        else:
            # Receiving a ResponseMessage after sending a RequestMessage
            print(f"RECEIVED_RES\t[{status}]\t[{sender} -> {receiver}]\t[{timestamps}]\n")

            os.makedirs(os.path.dirname(self._path_log), exist_ok=True)
            with open(self._path_log, "a+") as output_file:
                output_file.write(f"RECEIVED_RES\t[{status}]\t[{sender} -> {receiver}]\t[{timestamps}]\n")
                #output_file.write(f"RECEIVED_RES\t[{status}]\t[{sender} -> {receiver}]\t[{vp}]\n")
            output_file.close()
