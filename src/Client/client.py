import ast
import json
import os
import socket

from dotenv import load_dotenv

from core.Buffer.buffer import *
from core.Message.message import *
from core.Message.message_type import *
from core.Message.message_type import MessageType
from core.VectorClock.vectorclock import *
from utils.helpers import *
from utils.loggings import Logging


class PeerYFS:
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
        self._sites, self._peerId = self.__setup_site(port)
        self._folderPath = get_foldershares_path()

        self._clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._clientSocket.bind((PeerYFS.HOST, port))
        self._address = self._clientSocket.getsockname() # address ('127.0.0.1', port)

        self._timestamps = self.__init_timestamps() # init local vector time (){'Site1': 1, 'Site2': 3}
        self._vp = {} #{'_vp2': {'Site1': 1, 'Site2': 3}}
        self._messageQueue = []
        self.send_broadcast()

    def __setup_site(self, port) -> dict:
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

        self._sites, self._peerId = self.__remove_sites(port)
        other_sites_subfolders = []
        for siteName in self._sites.values():
            other_sites_subfolders.append(f'SharePeer{siteName}')

        # Call the function to create the directory structure
        create_folders(main_folder, subfolders, other_sites_subfolders)
        return self._sites, self._peerId

    def __remove_sites(self, port: int) -> dict:
        """
            bỏ sites có port trong _sites
        """
        if port in self._sites.keys():
            self._peerId = {port: self._sites[port]['siteName']}
            del self._sites[port]
            print(f"Site with port {port} removed successfully.")
        return self._sites, self._peerId

    def __updating_sites_address(self, addresses):
        for addr in addresses:
            if addr not in self._sites.keys():
                self._sites[addr] = len(self._sites) + 1

    def __init_timestamps(self):
        return {'Site1': 0, 'Site2': 0, 'Site3': 0, 'Site4': 0, 'Site5': 0}

    # def init_vp(self):
    #     for siteName in self._sites.values():
    #         self._vp[siteName['siteName']] = {'Site1': 0, 'Site2': 0, 'Site3': 0, 'Site4': 0, 'Site5': 0}
    #     return self._vp
    def __increase_timestamps(self) -> dict:
        self._timestamps[self._peerId.values()] += 1
        return self._timestamps

    def __update_receive_timestamps(self, timestamps):
        """
            Receive a message with timestamps
            timestamps = {
                'Site1': 2,
                'Site2': 4, // not updating this
                'Site3': 4,
                'Site4': 8,
                'Site5': 2
            }
        """
        self._timestamps = self.__increase_timestamps()

        for tstamps_site in timestamps.keys():
            if tstamps_site != self._peerId.values():
                self._timestamps[tstamps_site] = timestamps[tstamps_site]

    def __update_receive_vp(self, vp):
        for vp_site in vp.keys():
            if vp_site != self._peerId.values():
                # vp_site:
                # 1. if site not in vp_site receive
                if vp_site not in self._vp.key():
                    self._vp[vp_site] = vp[vp_site]
                else:
                    # nếu có thì kt các update site khác
                    for vp_chill in self._vp[vp_site].keys():
                        if self._vp[vp_site][vp_chill] >= vp[vp_site][vp_chill]:
                            self._vp[vp_site][vp_chill] = vp[vp_site][vp_chill]
        return self._vp
    def __check_delivery(self, vp) -> bool:
        """
            Kiểm tra timestamps của vp có thỏa với timestamps của site nhận ko
        """
        for vp_i in vp.keys():
            if vp[vp_i] == vp[self._peerId.values()]:
                for i in self._timestamps.key():
                    if vp[vp_i][i] > self._timestamps[i]:
                        return False
                return True

    def __compare_timestamps(self, timestamps):
        """
            so sánh 2 timestamps
        """
        for site, tS in timestamps.items():
            if site not in self._timestamps:
                return False
            if tS > self._timestamps[site]:
                return False
        return True

    def pop_message(self, message):
        """
            thực hiện cập nhật tm, vp sau đó unqueue message ra khỏi buffer
        """
        self.__update_receive_timestamps(message._timestamps[self._peerId.values()])
        self.__update_receive_vp(message._vp)

    def check_queue(self):
        """
            Kiểm tra có msg nào có thể unqueue dc ko
            Nếu có thì gọi hàm pop message
            Sau đó bỏ message
        """
        if len(self._messageQueue) > 0:
            for message in self._messageQueue:
                flag = True
                for i in self._timestamps.keys():
                    if message._vp[self._peerId.values()][i] > self._timestamps[i]:
                    # message vẫn chưa đc release
                        flag = False
                        break
                # check valid
                if flag:
                    # True thì unqueue message update tm, vp
                    self.pop_message(message)
                    self._messageQueue.remove(message)

    def __jsonstring_to_dict(self, data: dict) -> dict:
        dict = {}
        for key, value in data.items():
            key = tuple(eval(key))
            dict[key] = value
        return dict

    def send_broadcast(self):
        """
            first mount command when initialize a port
        """
        for sitePort, siteName in self._sites.items():
            # 1. set addr of receiver
            receiver = tuple((PeerYFS.HOST, sitePort))
            # 2. update timestamps of site send
            self._timestamps = self.__increase_timestamps()
            # 3. zip message # int/int/int/str/dict/dict
            message = Message(self._peerId.keys(), sitePort, MessageType.SEND_MOUNT.value, "",self._timestamps, self._vp)
            # 4. send message
            self._clientSocket.sendto(json.dumps(message).encode("utf-8"),receiver)
            self._logger.Log(f"{self._address}: Sent MOUNT to {receiver}", "INFO")

            # 5. after sending updating vp
            # cập nhật V_P2 = {P1: {0,1,0}} # V_P2[revc] = self._timestamps
            self._vp[siteName['siteName']] = self._timestamps

    def __check_port_valid(self, port: int) -> bool:
        if port in self._sites.keys():
            return True
        return False

    def send_message_SES(self, receiver: int, messageType: int, file_name: str, message: str):
        """
            receiver: int -> site_port that received message
            messateType: int -> the index of MessageType.MOUNT/READ/WRITE/START_WRITING/STOP_WRITING
            file_name: str -> file_name if messageType is READ/WRITE/START_WRITING/STOP_WRITING
            message: message if messageType is WRITE/START_WRITING/STOP_WRITING
        """
        if self.check_port_valid(receiver):
            self._timestamps = self.__update_timestamps()

        message = Message(
            self._peerId.keys(), # port send
            siteReceive, # port receive
            messageType,
            message,
            file_name,
            self._timestamps,
            self._vp)

        if messageType == MessageType.SEND_MOUNT.value:
            message = 1
        if messageType == MessageType.SEND_READ.value:
            Aaa
        if messageType == MessageType.SEND_MOUNT.value:
            Aaa
        for siteReceive in self._sites.keys():
            self._timestamps = self.__update_timestamps()

    def receive_message_SES(self, address_from, address_to, message):

        """
            tmp = {'Site1': 4, 'Site3': 1, '}
        """
        return
    def send_command_mount(self, address_to, messageType):
        self.send_message_broadcast()
        return
    def receive_command_mount(self, address_from, address_to, message):
        sitePeer = self._peerId[message._receiver]
        folder2read = get_peer_folder(sitePeer)


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

    def handle_read_command(site, file_name):
        return
    def handle_write_command(site, file_name, message_content):
        return
    def client_listen_event(self):
        """
            Dùng để lắng nghe sự kiện từ các sites khác
            received message_type có thể là: mount, read, write events
                    message_content: nội dung cần ghi nếu là options write
                    file_name: là file cần thực hiện read/write hoặc mount
        """
        while True:
            received_data, address = self._clientSocket.recvfrom(2048)
            received_data = received_data.decode('utf-8')
            self._logger.Log(f"{self._address}: Received {received_data} from {address}", "INFO")

            # Check msg_time
            if self.__check_delivery(message._vp):
                #Kiểm tra hàng đợi
                self.check_queue()

            else:
                # đưa vào buffer
                self._messageQueue.append(message)
            try:
                # extract data into Message type
                message = Message.from_string(received_data)
                if message._messageType == MessageType.SEND_MOUNT.value:
                    self.receive_command_mount(message)
                if message._messageType == MessageType.SEND_READ.value:
                    self.receive_command_read(message)
                if message._messageType == MessageType.SEND_WRITE.value:
                    self.receive_command_write(message)
                if message._messageType == MessageType.SEND_START_WRITING.value:
                    self.receive_command_start_writing(message)
                if message._messageType == MessageType.SEND_STOP_WRITING.value:
                    self.receive_command_stop_writing(message)

                else: #receive a reply
                    if message._messageType == MessageType.RECEIVE_MOUNT.value:
                        self.send_command_mount(message)
                    if message._messageType == MessageType.RECEIVE_READ.value:
                        self.send_command_(message)
                    if message._messageType == MessageType.RECEIVE_WRITE.value:
                        return
                    if message._messageType == MessageType.RECEIVE_START_WRITING.value:
                        return
                    if message._messageType == MessageType.RECEIVE_STOP_WRITING.value:
                        return

            except json.JSONDecodeError as e:
                self._logger.Log(f"Invalid JSON format received: {received_data}", "ERROR")
                continue

            print(f"Thông tin site từ server: {received_data}")

            self.__updating_sites_address(received_data)

            print("Other clients:", self._sites)




    def display_user_options(self):
        print("Port's of Site Informations\n")
        for addr, sitename in self._sites.items():
            print(f"{sitename['siteName']} running at {addr}\n")
        print("========= Helping when sending a command========= \n")
        print("read {SITE} {FILENAME}")
        print("write {SITE} {FILENAME} {MESSAGE_TO_WRITE}")

    def __get_port_by_site(self, site: str) -> int:
        for port, site in self._sites.items():
            if site['siteName'] == site:
                return port


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
                    site = self.__get_port_by_site(command_options[0])
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
                    site = self.__get_port_by_site(command_options[0])
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
