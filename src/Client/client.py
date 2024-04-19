import ast
import json
import os
import socket

from dotenv import load_dotenv

from core.Message.message_type import MessageType
from utils.loggings import Logging


class ClientYLS:
    # load HOST, PORT from .ENV
    config = load_dotenv()
    HOST = os.environ.get('HOST')
    PORT = int(os.environ.get('PORT'))

    def __init__(self) -> None:
        self._sites = {} # ADDRESS of other sites
        self._logger = Logging("../logs","logs.txt")
        self._clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._clientSocket.connect((ClientYLS.HOST, ClientYLS.PORT))
        self._address = self._clientSocket.getsockname()

    def updating_sites_address(self, addresses):
        for addr in addresses:
            if addr not in self._sites.keys():
                self._sites[addr] = len(self._sites) + 1
    def jsonstring_to_dict(self, data: dict) -> dict:
        dict = {}
        for key, value in data.items():
            key = tuple(eval(key))
            dict[key] = value
        return dict
    def send_message_broadcast(self, address_from, address_to, message):
        return
    def receive_message_broadcast(self, address_from, address_to, message):
        return
    def send_command_mount(self, address_from, address_to, message):
        return
    def receive_command_mount(self, address_from, address_to, message):
        return
    def send_command_read(self, address_from, address_to, message):
        return
    def receive_command_read(self, address_from, address_to, message):
        return
    def send_command_write(self, address_from, address_to, message):
        return
    def receive_command_write(self, address_from, address_to, message):
        return
    def send_command_start_writing(self, address_from, address_to, message):
        return
    def receive_command_start_writing(self, address_from, address_to, message):
        return
    def send_command_stop_writing(self, address_from, address_to, message):
        return
    def receive_command_stop_writing(self, address_from, address_to, message):
        return
    def handle_read_file(self):
        return
    def handle_write_file(self):
        return
    def client_run(self):
        while True:
            #received_data, sender = self._clientSocket.recvfrom(2048,???).decode()
            #received_data = self._clientSocket.recvfrom(2048, ((ClientYLS.HOST, ClientYLS.PORT))).decode()
            received_data = self._clientSocket.recv(2048).decode()
            self._logger.Log(f"Received: {received_data}", "INFO")
            try:
                data = json.loads(received_data)
                received_data = self.jsonstring_to_dict(data)
            except json.JSONDecodeError as e:
                self._logger.Log(f"Invalid JSON format received: {received_data}", "ERROR")
                continue

            print(f"Thông tin site từ server: {received_data}")

            self.updating_sites_address(received_data)

            print("Other clients:", self._sites)
        client_socket.close()

    def handle_command(self, command: str, args):
        self._logger.Log(f"{self._address}: {command} {args}", "INFO")
        match command:
            case 'broadcast':
                dosomeigh= []
            case 'get':
                return
            case 'read':
                return
            case 'write':
                return
            case 'start_writing':
                return
            case 'stop_writing':
                return
    def display_user_options(self):
        if len(self._sites) > 0:
            # Chọn site muốn communicate
            print("Select a client to communicate with:")
            for addr, index in self._sites.items():
                print(f"{index}. {addr}")

            # selected_client = other_clients[client_idx]
            # client_socket.sendall(f"selected_client Hahaha{selected_client}".encode())

    #def handle_site_command(client: ClientYLS):
    # """
    #     tham số 1 - [0]: các lệnh READ/WRITE/GET/BROADCAST/
    #     tham số 2 - [1]: giá trị args cho command
    # """

    #     while True:
    #         client.display_user_options()
    #         user_command = input(f"{client._address}$ ").split()

    #         command = user_command[0].lower()
    #         arg = user_command[1].lower()

    #         if command in MessageType.to_dict():
    #             client.handle_command(command, arg)

    #         if command == 'exit':
    #             client._logger.Log(f"{client._address} disconnected server", "INFO")
    #             return

    #         else:
    #             client._logger.Log(f"{client._address} command not appropriate {command} {arg}", "INFO")
    def handle_site_command(self):
        """
            tham số 1 - [0]: các lệnh READ/WRITE/GET/BROADCAST/
            tham số 2 - [1]: giá trị args cho command
        """

        while True:
            self.display_user_options()
            user_command = input(f"{self._address}$ ").split()

            command = user_command[0].lower()
            arg = user_command[1].lower()

            if command in MessageType.to_dict():
                self.handle_command(command, arg)

            if command == 'exit':
                self._logger.Log(f"{self._address} disconnected server", "INFO")
                return

            else:
                self._logger.Log(f"{self._address} command not appropriate {command} {arg}", "INFO")
