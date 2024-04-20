import ast
import json
import os
import socket

from dotenv import load_dotenv

from core.Buffer.buffer import *
from core.Message.message import *
from core.Message.message_buffer import *
from core.Message.message_compare import *
from core.Message.message_type import *
from core.Message.message_type import MessageType
from core.VectorClock.vectorclock import *
from utils.helpers import *
from utils.loggings import Logging


class PeerYLS:
    # load HOST, PORT from .ENV
    config = load_dotenv()
    HOST = os.environ.get('HOST')
    #PORT = int(os.environ.get('PORT'))

    def __init__(self, port: int) -> None:
        self._sites = {
            7670: {'siteName': 'Site1'},
            7671: {'siteName': 'Site2'},
            7672: {'siteName': 'Site3'},
            7673: {'siteName': 'Site4'},
            7674: {'siteName': 'Site5'}
        }
        self._logger = Logging("../logs","logs.txt")
        self._sites = self.setup_site(port)

        self._clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._clientSocket.bind((PeerYLS.HOST, port))
        self._address = self._clientSocket.getsockname() # address ('127.0.0.1', port)

        self.send_broadcast_command(messa)

    def setup_site(self, port) -> dict:
        """
            Hàm để tạo folder:
            ├───FolderSite1
            │   ├───OtherSites
            │   │   ├───SharePeerSite2
            │   │   └───SharePeerSite3
            │   └───PeerSite1
            └───FolderSite2
            và loại site có port trong site
        """
        site_name = self._sites[port]['siteName']
        main_folder = f'Folder{site_name}'
        subfolders = [f'Peer{site_name}', 'OtherSites']

        self._sites = self.remove_sites(port)
        other_sites_subfolders = []
        for siteName in self._sites.values():
            other_sites_subfolders.append(f'SharePeer{siteName}')

        # Call the function to create the directory structure
        create_folders(main_folder, subfolders, other_sites_subfolders)
        return self._sites

    def remove_sites(self, port: int) -> dict:
        """
            bỏ sites có port trong _sites
        """
        if port in self._sites.keys():
            del self._sites[port]
            print(f"Site with port {port} removed successfully.")
        return self._sites

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

    def send_broadcast_sites_updatdhdfge(self):
        if len(self._clients) > 1:
            """
                For loop này sẽ gửi msg cho client_socket, chứ ko gửi cho
                từng th khác , fOck
            """
            for addr, sock in self._clients.items():
                sites = self._clients.copy()
                del sites[addr]
                #print(f"{sites[addr]}")
                sites = self.dict_to_string(sites)

                #self._serverSocket.sendall(json.dumps(sites).encode(),
                #addr)
                """
                    ? gửi từ
                    client_socket.sendall(json.dumps(sites).encode())
                """
                client_socket.sendall(json.dumps(sites).encode())
                    #self._serverSocket.sendto(json.dumps(sites).encode(), addr)
    def send_message_broadcast(self, messageType: MessageType):
        for site in self._sites.keys():
            message = {
                'message_type': message.message_type,
                'file_name': aa
            }
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
    def client_listen_event(self):
        """
            Dùng để lắng nghe sự kiện từ các sites khác
            received message_type có thể là: mount, read, write events
                    message_content: nội dung cần ghi nếu là options write
                    file_name: là file cần thực hiện read/write hoặc mount
        """
        while True:
            #received_data, sender = self._clientSocket.recvfrom(2048,???).decode()
            #received_data = self._clientSocket.recvfrom(2048, ((ClientYLS.HOST, ClientYLS.PORT))).decode()
            received_data, address = self._clientSocket.recvfrom(2048)
            self._logger.Log(f"Received data: {received_data.decode('utf-8')} from {address}", "INFO")
            try:
                data = json.loads(received_data)
                received_data = self.jsonstring_to_dict(data)
            except json.JSONDecodeError as e:
                self._logger.Log(f"Invalid JSON format received: {received_data}", "ERROR")
                continue

            print(f"Thông tin site từ server: {received_data}")

            self.updating_sites_address(received_data)

            print("Other clients:", self._sites)


    def display_user_options(self):
        print("Port's of Site Informations\n")
        for addr, sitename in self._sites.items():
            print(f"{sitename['siteName']} running at {addr}\n")
        print("========= Helping when sending a command========= \n")
        print("read {SITE} {FILENAME}")
        print("write {SITE} {FILENAME} {MESSAGE_TO_WRITE}")



    def handle_site_command(self):
        """
            tham số 1 - [0]: các lệnh READ/WRITE
            tham số 2 - [1]: tên Site để thực hiện READ/WRITE
            tham số 3 - [2]: tên file nếu như là READ/WRITE,
            tham số 4 - [3]: nội dung cần ghi nếu là WRITE
        """

        while True:
            self.display_user_options()
            user_command = input(f"{self._address}$ ").split()

            command = user_command[0].lower()
            command_options = user_command[1:]

            if command == 'read':
                """
                    Để handle cần {Site} {FileToRead}
                """
                if len(command_options) == 2:
                    if command_options[0].lower() not in self._sites.values():
                        self._logger.Log(f"READ COMMAND - {command_options[0]} not in sites known")
                    site = command_options[0]
                    file_name = command_options[1]
                    self.handle_read_command(site, file_name)

                else:
                    self._logger.Log(f"READ COMMAND - missing or got more than 2 params")

            if command == 'write':
                """
                    Để handle cần {Site} {FileToWrite} {ContentToWrite}
                """
                if len(command_options) == 3:
                    if command_options[0].lower() not in self._sites.values():
                        self._logger.Log(f"WRITE COMMAND - {command_options[0]} not in sites known")
                    site = command_options[0]
                    file_name = command_options[1]
                    message_content = command_options[2]
                    self.handle_write_command(site, file_name, message_content)

                else:
                    self._logger.Log(f"WRITE COMMAND - missing or got more than 3 params")

            if command == 'exit':
                self._logger.Log(f"{self._address} Closing Port", "INFO")
                return

            else:
                self._logger.Log(f"{self._address} command not appropriate {command} {[str(arg) for arg in command_options]}", "INFO")
