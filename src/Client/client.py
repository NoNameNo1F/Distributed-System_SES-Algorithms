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
        self._clientSocket = socket.socket()
        self._clientSocket.connect((ClientYLS.HOST, ClientYLS.PORT))
        self._address = self._clientSocket.getsockname()

    def updating_sites_address(self, addresses):
        for addr in addresses:
            if addr not in self._sites.keys():
                self._sites[addr] = len(self._sites) + 1
    def client_run(self):
        while True:
            received_data, sender = self._clientSocket.recv(1024).decode()

            try:
                data = json.loads(received_data)
                print(data)
            except json.JSONDecodeError as e:
                self._logger.Log(f"Invalid JSON format received: {received_data}", "ERROR")
                continue
            print(sender)
            self._logger.Log(f"RECEIVED FROM {sender} - {data}", "INFO")

            #received_data = eval(received_data)
            print(f"{type(received_data)} : {received_data}")
            print(f"Thông tin site từ server: {received_data}")

            self.updating_sites_address(received_data)

            print("Other clients:", self._sites)

            # data = client_socket.recv(1024).decode()

            # self._logger.Log(f"Received from server: {data}", "INFO")
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

def handle_site_command(client: ClientYLS):
    """
        tham số 1 - [0]: các lệnh READ/WRITE/GET/BROADCAST/
        tham số 2 - [1]: giá trị args cho command
    """

    while True:
        client.display_user_options()
        user_command = input(f"{client._address}$ ").split()

        command = user_command[0].lower()
        arg = user_command[1].lower()

        if command in MessageType.to_dict():
            client.handle_command(command, arg)

        if command == 'exit':
            client._logger.Log(f"{client._address} disconnected server", "INFO")
            return

        else:
            client._logger.Log(f"{client._address} command not appropriate {command} {arg}", "INFO")
