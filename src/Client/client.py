import ast
import json
import os
import socket

from dotenv import load_dotenv

from core.Message.message import *
from core.Message.message_type import *
from core.Message.message_type import MessageType
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
        self._logger = Logging("../logs","logs.txt", f"logs_{port}.txt")
        self._sites, self._peerId = self.__setup_site(port)

        self._clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._clientSocket.bind((PeerYFS.HOST, port))

        self._address = self._clientSocket.getsockname()
        self._port = port
        self._timestamps = self.__init_timestamps()
        self._vp = {}
        self._messageQueue = []
        self.send_broadcast_mount()

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
            other_sites_subfolders.append(f'SharePeer{siteName['siteName']}')

        # Call the function to create the directory structure
        create_folders(main_folder, subfolders, other_sites_subfolders)
        return self._sites, self._peerId

    def __remove_sites(self, port: int) -> dict:
        """
            remove site have port in _sites
        """
        if port in self._sites.keys():
            self._peerId = {port: self._sites[port]['siteName']}
            del self._sites[port]
        return self._sites, self._peerId

    def __get_peer_sitename(self) -> str:
        """
            Return siteName of peer
        """
        return self._peerId[self._port]

    def __init_timestamps(self) -> dict:
        """
            Initialize timestamps at first
        """
        return {'Site1': 0, 'Site2': 0, 'Site3': 0, 'Site4': 0, 'Site5': 0}

    def __increase_timestamps(self) -> dict:
        """update_receive_vp
            Increasing timestamps local by 1
        """
        site_name = self.__get_peer_sitename()
        self._timestamps[site_name] += 1
        return self._timestamps

    def __update_receive_timestamps(self, timestamps: dict) -> dict:
        """
            Updating local timestamps when receiving message with timestamps
        """
        self._timestamps = self.__increase_timestamps()

        for tstamps_site in timestamps.keys():
            if tstamps_site != self.__get_peer_sitename():
                self._timestamps[tstamps_site] = max(timestamps[tstamps_site], self._timestamps[tstamps_site])

        return self._timestamps

    def __update_receive_vp(self, vp: dict) -> dict:
        """
            Updating local V_P when receiving message with V_Ps
        """
        for vp_site in vp.keys():
            if vp_site != self.__get_peer_sitename():
                # vp_site:
                # 1. if site not in vp_site receive
                if vp_site not in self._vp.keys():
                    self._vp[vp_site] = vp[vp_site].copy()
                else:
                    # nếu có thì kt các update site khác
                    for vp_child in vp[vp_site].keys():
                        if vp_child in self._vp[vp_site]:
                            if self._vp[vp_site][vp_child] < vp[vp_site][vp_child]:
                                self._vp[vp_site][vp_child] = vp[vp_site][vp_child]
                        else:
                            self._vp[vp_site][vp_child] = vp[vp_site][vp_child]

        return self._vp

    def __check_delivery(self, vp) -> bool:
        """
            Check local timestamps with VP of message receiving
            If it could delivery message instantly or not?
        """

        site_name = self.__get_peer_sitename()
        if site_name in vp.keys():
            return self.__compare_timestamps(vp[site_name])
        return True

    def __compare_timestamps(self, timestamps):
        """
            compare 2 timestamps
        """
        for site, tS in timestamps.items():
            if tS > self._timestamps[site]:
                return False
        return True

    def pop_message(self) -> Message:
        """
            thực hiện cập nhật tm, vp sau đó unqueue message ra khỏi buffer
            get the message out of self._queueMessage
        """
        message = self.get_msg_unqueue()
        if message != None:
            return message

    def get_msg_unqueue(self) -> Message| None:
        """
            If there are any message that timestamps-in-vp-received is lower
            than local timestamps
        """
        if len(self._messageQueue) > 0:
            site_name = self.__get_peer_sitename()
            for message in self._messageQueue:
                flag = True
                for i in self._timestamps.keys() and flag != False:
                    if site_name in message._vp.keys():
                        if message._vp[site_name][i] > self._timestamps[i]:
                        # message vẫn chưa đc release
                            flag = False
                            break
                # check valid
                if flag:
                    # True thì unqueue message update tm, vp
                    return message
        return None

    def _check_unqueue(self) -> bool:
        """
            Kiểm tra có msg nào có thể unqueue dc ko
            Nếu có thì gọi hàm pop message
            Sau đó bỏ message
        """
        if len(self._messageQueue) > 0:
            site_name = self.__get_peer_sitename()
            for message in self._messageQueue:
                flag = True
                for i in self._timestamps.keys() and flag != False:
                    if site_name in message._vp.keys():
                        if message._vp[site_name][i] > self._timestamps[i]:
                        # message vẫn chưa đc release
                            flag = False
                            break
                # check valid
                if flag:
                    # True thì unqueue message update tm, vp
                    return True
        return False

    def __check_port_valid(self, port: int) -> bool:
        """
            Is Port input valid or not?
        """
        if port in self._sites.keys():
            return True
        return False

    def __check_siteName_valid(self, site_name: str):
        """
            Is SiteName input valid or not?
        """
        site_name = site_name.lower()
        for siteName in self._sites.values():
            if siteName['siteName'].lower() == site_name:
                return True
        return False

    def __get_port_by_sitename(self, site: str) -> int | None:
        """
            Return port with site_name required
        """
        for port, site in self._sites.items():
            if site['siteName'] == site:
                return port
        return None

    def __get_sitename_by_port(self, port: int) -> str | None:
        """
            Return site_name with port required
        """
        for site_port in self._sites.keys():
            if site_port == port:
                return self._sites[port]['siteName']
        return None

    def send_broadcast_mount(self):
        """
            first mount command when initialize a port
        """
        for sitePort in self._sites.keys():
            self.send_message_SES(sitePort,
                                MessageType.SEND_MOUNT.value,
                                "",
                                "")


    def send_broadcast_update(self, file_name: str, file_content: str):
        """
            first mount command when initialize a port
        """
        for sitePort in self._sites.keys():
            self.send_message_SES(sitePort,
                                MessageType.RECEIVE_WRITE.value,
                                file_name,
                                file_content)

    def send_message_SES(self, receiver_port: int, messageType: int, file_name: str, message: str):
        """
            receiver_port: int -> site_port that received message
            messateType: int -> the index of MessageType.MOUNT/READ/WRITE
            file_name: str -> file_name if messageType is MOUNT/READ/WRITE
            message: message if messageType is WRITE
        """
        # 1. Update timestamps of the site send
        self._timestamps = self.__increase_timestamps()

        # 2. Create a message
        message = Message(
            self._port,
            receiver_port,
            messageType,
            message,
            file_name,
            self._timestamps,
            self._vp
        )

        # 3. Create Address recipient to receive message
        receiver = tuple((PeerYFS.HOST, receiver_port))

        # 4. Send message to receiver
        self._clientSocket.sendto(str(message).encode('utf-8'), receiver)

        # 5. Logging
        msg_type_name = MessageType.get_messagetype_by_index(messageType)
        if messageType > 0:
            #self._logger.Log(f"[{self._address}]: Sent Request [{msg_type_name}] to [{receiver}]", "INFO")
            self._logger.Log_Sent(message, msg_type_name)

        # 6. Update VP after sending message
        site_name = self.__get_sitename_by_port(receiver_port)
        self._vp[site_name] = self._timestamps.copy()

    def handle_receive_SES_message(self, message: Message):
        """Xử lý REQUEST MOUNT/READ/WRITE VÀ RESPONSE MOUNT/READ/WRITE"""
        if self.__check_delivery(message._vp):
            #Nếu có thể chuyển giao msg
            """ 1. Kiểm tra có thể deliver message không"""

            if message._messageType == MessageType.SEND_MOUNT.value \
                or message._messageType == MessageType.RECEIVE_MOUNT.value:
                """Trường hợp xử lý cờ REQUEST MOUNT VÀ RESPONSE MOUNT"""
                self.receive_command_mount(message)

            elif message._messageType == MessageType.SEND_READ.value \
                or message._messageType == MessageType.RECEIVE_READ.value:
                """Trường hợp xử lý cờ REQUEST READ VÀ RESPONSE READ"""
                self.receive_command_read(message)

            elif message._messageType == MessageType.SEND_WRITE.value \
                or message._messageType == MessageType.RECEIVE_WRITE.value:
                """Trường hợp xử lý cờ REQUEST WRITE VÀ RESPONSE WRITE"""
                self.receive_command_write(message)

        elif self._check_unqueue():
            """ 2. Nếu không deliver được thì Kiểm tra có msg trong buffer không"""
            self.unqueue_message()

        else:
            """ 3. Nếu vẫn không thể lấy message ra khỏi buffer thì tức là vẫn còn message chưa qua, nên buffer lại message"""
            self._messageQueue.append(message)

    def unqueue_message(self):
        msg_to_unqueue = self.pop_message()
        self._messageQueue.remove(msg_to_unqueue)
        self.handle_receive_message_SES(msg_to_unqueue)

    def receive_command_mount(self, message: Message):
        """
            Handle MessageType SEND_MOUNT and RECEIVE_MOUNT with specific context.
        """
        if message._messageType > 0:
            """
                Receiving a MOUNT REQUEST from sender
            """
            # 1. Cập nhật timestamps site nhận
            self._timestamps = self.__update_receive_timestamps(message._timestamps)

            # 2. Cập nhật VP site nhận nếu các timestamp-trong-vp-msg-gửi thỏa timestamps
            self._vp = self.__update_receive_vp(message._vp)

            self._logger.Log_Received(message._sender,
                                    message._receiver,
                                    self._timestamps,
                                    self._vp,
                                    message._messageType)
            # 3. Lấy path tới file_name cần đọc
            siteName = self.__get_peer_sitename()
            folder_site = get_peer_folder(siteName)

            # 4. Lấy danh sách fileNames cần đọc
            file_names = get_files_in_folder(folder_site)
            for file in file_names:
                path_to_read = get_data_file_path(folder_site, file)
                content_read = read_data_from_file(path_to_read)

                self.send_message_SES(message._sender, MessageType.RECEIVE_MOUNT.value,file, content_read)

        else:
            """
                Receiving a MOUNT RESPONSE from sender
            """
            try:
                # 1. Cập nhật timestamps site nhận
                self._timestamps = self.__update_receive_timestamps(message._timestamps)

                # 2. Cập nhật VP site nhận nếu các timestamp-trong-vp-msg-gửi thỏa timestamps
                self._vp = self.__update_receive_vp(message._vp)
                self._logger.Log_Received(message._sender,
                                        message._receiver,
                                        self._timestamps,
                                        self._vp,
                                        message._messageType)
                # 3. Lấy fileName cần ghi xuống vào othersite sharepeersite và in ra console
                file_name = message._filename
                file_content = message._messageContent

                # 4. Lấy path tới sharepeersite response để save/ ghi vào
                site_response_name = self.__get_sitename_by_port(message._sender)
                site_name = self.__get_peer_sitename()
                folder_site = get_otherpeer_folder(site_name, site_response_name)
                path_to_save = get_data_file_path(folder_site, file_name)

                content_read = write_data_to_file(path_to_save, file_content)
                #self._logger.Log(f"[{message._receiver}]: Received Response MOUNT and saved content: [{message._messageContent}]", "INFO")

                msg_type_name = MessageType.get_messagetype_by_index(message._messageType)
                self._logger.Log_Sent(message, msg_type_name)
            except Exception as e:
                print(e)
    def receive_command_read(self, message: Message):
        """
            Handle MessageType SEND_READ and RECEIVE_READ with specific context.
        """
        if message._messageType > 0:
            """
                Receiving a request read from sender
            """
            # 1. Cập nhật timestamps site nhận
            self._timestamps = self.__update_receive_timestamps(message._timestamps)
            # 2. Cập nhật VP site nhận nếu các timestamp-trong-vp-msg-gửi thỏa timestamps
            self._vp = self.__update_receive_vp(message._vp)
            self._logger.Log_Received(message._sender,
                                    message._receiver,
                                    self._timestamps,
                                    self._vp,
                                    message._messageType)
            # 3. Lấy fileName cần đọc
            file_name = message._filename
            # 4. Lấy path tới file_name cần đọc
            siteName = self.__get_peer_sitename()
            folder_site = get_peer_folder(siteName)
            path_to_read = get_data_file_path(folder_site, file_name)
            if is_filename_exists(path_to_read):
                content_read = read_data_from_file(path_to_read)
                self.send_message_SES(message._sender, MessageType.RECEIVE_READ.value,file_name, content_read)
            else:
                self._logger.Log(f"[{file_name}] isn't exists in folder", "ERROR")

        else:
            """
                Receiving a response read from sender
            """
            # 1. Cập nhật timestamps site nhận
            self._timestamps = self.__update_receive_timestamps(message._timestamps)
            # 2. Cập nhật VP site nhận nếu các timestamp-trong-vp-msg-gửi thỏa timestamps
            self._vp = self.__update_receive_vp(message._vp)
            self._logger.Log_Received(message._sender,
                                    message._receiver,
                                    self._timestamps,
                                    self._vp,
                                    message._messageType)
            # 3. Lấy fileName cần đọc
            file_name = message._filename
            file_content = message._messageContent

            # 4. Lấy path tới sharepeersite response để save
            site_response_name = self.__get_sitename_by_port(message._sender)
            site_name = self.__get_peer_sitename()
            folder_site = get_otherpeer_folder(site_name, site_response_name)

            path_to_save = get_data_file_path(folder_site, file_name)

            content_read = write_data_to_file(path_to_save, file_content)
            print(f"{content_read}")
            msg_type_name = MessageType.get_messagetype_by_index(message._messageType)
            self._logger.Log_Sent(message, msg_type_name)


    def receive_command_write(self, message: Message):
        """
            Handle MessageType SEND_WRITE and RECEIVE_WRITE with specific context.
        """
        if message._messageType > 0:
            # 1. Cập nhật timestamps site nhận
            self._timestamps = self.__update_receive_timestamps(message._timestamps)
            # 2. Cập nhật VP site nhận nếu các timestamp-trong-vp-msg-gửi thỏa timestamps
            self._vp = self.__update_receive_vp(message._vp)

            self._logger.Log_Received(message._sender,
                                    message._receiver,
                                    self._timestamps,
                                    self._vp,
                                    message._messageType)

            file_name = message._filename
            file_content = message._messageContent

            site_name = self.__get_peer_sitename()
            folder_path = get_peer_folder(site_name)
            path_to_write = get_data_file_path(folder_path, file_name)
            content_write = write_data_to_file(path_to_write, file_content)
            print(content_write)

            msg_type_name = MessageType.get_messagetype_by_index(message._messageType)
            self._logger.Log_Sent(message, msg_type_name)
            self.send_broadcast_update(file_name, content_write)

        else:
            # 1. Cập nhật timestamps site nhận
            self._timestamps = self.__update_receive_timestamps(message._timestamps)
            # 2. Cập nhật VP site nhận nếu các timestamp-trong-vp-msg-gửi thỏa timestamps
            self._vp = self.__update_receive_vp(message._vp)

            self._logger.Log_Received(message._sender,
                                    message._receiver,
                                    self._timestamps,
                                    self._vp,
                                    message._messageType)
            # 3. Lấy filename, file content để update
            file_name = message._filename
            file_content = message._messageContent
            # 4. Lấy path tới sharepeersite để update file
            site_name = self.__get_peer_sitename()
            site_response_name = self.__get_sitename_by_port(message._sender)
            folder_site = get_otherpeer_folder(site_name, site_response_name)


            path_to_write = get_data_file_path(folder_site, file_name)
            content_update = write_data_to_file(path_to_write, file_content)
            print(content_update)

            msg_type_name = MessageType.get_messagetype_by_index(message._messageType)
            self._logger.Log_Sent(message, msg_type_name)


    def client_listen_event(self):
        """
            Dùng để lắng nghe sự kiện từ các sites khác
            received message_type có thể là: mount, read, write events
                    message_content: nội dung cần ghi nếu là options write
                    file_name: là file cần thực hiện read/write hoặc mount
        """
        while True:
            try:
                received_msg = self._clientSocket.recv(2048)
                message = received_msg.decode('utf-8')
                #self._logger.Log(f"{self._address}: Received {message} from
                #{address}", "INFO")
                message = Message.from_string(message)
                msg_type_name = MessageType.get_messagetype_by_index(message._messageType)
                self._logger.Log_Sent(message,msg_type_name)
                self.handle_receive_SES_message(message)
                if self._check_unqueue():
                    self.unqueue_message()

            except Exception as e:
                continue

    def display_user_options(self):
        print("Port's of Site Informations\n")
        for addr, sitename in self._sites.items():
            print(f"{sitename['siteName']} running at {addr}\n")
        print("========= Helping when sending a command========= \n")
        print("READ {SITE_PORT} {FILENAME}")
        print("WRITE {SITE_PORT} {FILENAME} {MESSAGE_TO_WRITE}")
        print("check: to print current timestamp")
        print("vp: to print current vp")
        print("list: length of the buffer message")
        print("exit: end programs")

    def handle_site_command(self):
        """
            tham số 1 - [0]: các lệnh READ/WRITE
            tham số 2 - [1]: Site port để thực hiện READ/WRITE
            tham số 3 - [2]: tên file nếu như là READ/WRITE,
            tham số 4 - [3]: nội dung cần ghi nếu là WRITE
        """

        while True:
            self.display_user_options()
            user_command = input(f"{self._address}$ ").split()


            if len(user_command) > 0:
                # go back to display user optio...
                command = user_command[0].lower()
                command_options = user_command[1:]
                receiver_port = int()
                file_name = str()

                if command == 'exit':
                    self._logger.Log(f"{self._address} Closing Port", "INFO")
                    break

                elif command == 'list':
                    print(f"\n {len(self._messageQueue)}\n")

                elif command == 'check':
                    print(f"\n{self._timestamps}\n")

                elif command == 'vp':
                    print(f"\n{self._vp}\n")

                else:
                    # 1. Checking is input Sitename or port
                    if command_options[0].lower().startswith('site') and \
                        self.__check_siteName_valid(command_options[0]):
                        """
                            If user input siteName instead of site Port(xxxx)
                        """
                        receiver_port = self.__get_port_by_sitename(command_options[0])
                    elif self.__check_port_valid(int(command_options[0])):
                        receiver_port = int(command_options[0])


                    # 2. Checking filename input have additional filetype
                    if ".txt" not in command_options[1]:
                        file_name = f"{command_options[1]}.txt"
                    else:
                        file_name = command_options[1]

                    # 3. Checking Command Options
                    if command == 'read':
                        """
                            Để handle cần {Site_port} {FileToRead}
                        """
                        if len(command_options) == 2:
                            self.send_message_SES(receiver_port, MessageType.SEND_READ.value, file_name, "")
                        else:
                            self._logger.Log(f"READ COMMAND - missing or got more than 2 params","ERROR")

                    elif command == 'write':
                        """
                            Để handle cần {Site} {FileToWrite} {ContentToWrite}
                        """
                        if len(command_options) >= 3:
                            # message content to write end of the file
                            message_content = ' '.join(command_options[2:])
                            self.send_message_SES(receiver_port, MessageType.SEND_WRITE.value, file_name, message_content)

                        else:
                            self._logger.Log(f"WRITE COMMAND - missing or got more than 3 params", "ERROR")

                    else:
                        self._logger.Log(f"{self._address} command not appropriate {command} {[str(arg) for arg in command_options]}", "INFO")
