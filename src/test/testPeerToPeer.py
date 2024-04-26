import json
import os
import sys
import threading

from dotenv import load_dotenv

from Client.client import *
from core.Message.message_type import MessageType
from utils.helpers import *

PROJECT_ROOT = os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                os.pardir)
)
sys.path.append(PROJECT_ROOT)

def jsonstring_to_dict(data: dict) -> dict:
        dict = {}
        for key, value in data.items():
            key = tuple(eval(key))
            dict[key] = value
        return dict
# Function to handle incoming messages
def listen_for_messages(sock):
    while True:
        message, address = sock.recvfrom(1024)
        print(f"Received from {address}: {message.decode('utf-8')}")

# Function to send messages
def send_messages(sock):
    while True:
        message_to_send = input("Enter message to send: ").split()
        message = ' '.join(message_to_send[:-1])

        port_to_send = int(message_to_send[-1])
        receiver = tuple(('127.0.0.1', port_to_send))
        sock.sendto(message.encode('utf-8'), receiver)

# Main function to set up the socket and threads
def main():
    host = '127.0.0.1'  # Use the appropriate host
    port = 7670         # Use the appropriate port
    target_host = '127.0.0.1'  # Target host to send messages
    target_port = 7670         # Target port to send messages
    input_port = int(sys.argv[1])
    #snif_port = int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((host, input_port))
        print(sock)
        print(sock)
        print(f"Listening for messages on {host}:{input_port}")

        # Creating threads for listening and sending
        listen_thread = threading.Thread(target=listen_for_messages, args=(sock,))
        send_thread = threading.Thread(target=send_messages, args=(sock,))

        # Starting threads
        listen_thread.start()
        send_thread.start()

        # Joining threads to the main thread
        listen_thread.join()
        send_thread.join()

if __name__ == "__main__":
    #main()
    #print(get_parent_path())
    # sites = {
    #     7670: {'siteName': 'Site1'},
    #     7671: {'siteName': 'Site2'},
    #     7672: {'siteName': 'Site3'},
    #     7673: {'siteName': 'Site4'},
    #     7674: {'siteName': 'Site5'}
    # }

    #sender = tuple(('127.0.0.1', 7670))
    # sender = 7670
    # receiver = 7671
    # #receiver = tuple(('127.0.0.1', 7671))
    # message_type = MessageType.SEND_MOUNT.value
    # message_content = ""
    # tms = {'Site1': 1, 'Site2': 1, 'Site3': 0}
    # _vp = {
    #     'Site1': {
    #         'Site1': 0,
    #         'Site2': 1,
    #         'Site3': 1
    #     },
    #     'Site2': {
    #         'Site1': 0,
    #         'Site2': 1,
    #         'Site3': 0
    #     }
    # }
    # vp = {
    #     'Site1':{
    #         'Site1': 0,
    #         'Site2': 2,
    #         'Site3': 0
    #     },
    #     'Site3': {
    #         'Site1': 0,
    #         'Site2': 0,
    #         'Site3': 0
    #     }
    # }
    # # def update_vp(vp, _vp) -> dict:
    # #     for vp_site in vp.keys():
    # #         if vp_site not in _vp.keys():
    # #             #print(vp_site)
    # #             _vp[vp_site] = vp[vp_site]
    # #         else:
    # #             # nếu có thì kt update
    # #             for vp_chill in _vp[vp_site].keys():
    # #                 if _vp[vp_site][vp_chill] >= vp[vp_site][vp_chill]:
    # #                     _vp[vp_site][vp_chill] = vp[vp_site][vp_chill]
    # #     return _vp
    # # print(update_vp(vp, _vp))
    # # message1 = Message(sender, receiver, message_type, message_content, tms, vp)
    # # message2 = Message(sender, 7677, message_type, message_content, tms, vp)
    # # print(f'{message}\nType: {type(message)}\n')
    # # print(f'{str(message)}\nType: {type(str(message))}\n')
    # # message_json = str(message).encode('utf-8')
    # # print(f'{message_json}\nType: {type(message_json)}\n')
    # # recv = message_json.decode('utf-8')
    # # print(f'{recv}\nType: {type(recv)}\n')
    # # recvvv = Message.from_string(recv)
    # # print(f'{recvvv}\nType: {type(recvvv)}\n')
    # # print(recvvv._sender)

    # # convertStr2Msg = json.loads(recv)
    # # print(f'{convertStr2Msg}\nType: {type(convertStr2Msg)}\n')
    # # cStr2Msg = Message.from_dict(convertStr2Msg)
    # # print(f'{cStr2Msg}\nType: {type(cStr2Msg)}\n')
    # # queue = []
    # # queue.append(message1)
    # # queue.append(message2)

    # # print(queue)

    # # queue.remove(message1)
    # # print(queue)
    # # a =1
    # # def change_value(a: int,value: int):
    # #     a = value
    # # change_value(a,4)
    # # print(a)
    # # A = 1
    # # MessageType.get_messagetype_by_index(A)
    # sites = {
    #         7670: {'siteName': 'Site1'},
    #         7672: {'siteName': 'Site3'},
    #         7673: {'siteName': 'Site4'},
    #         7674: {'siteName': 'Site5'}
    #     }
    # def __check_siteName_valid(sites ,site_name: str):
    #     """
    #         Is SiteName input valid or not?
    #     """
    #     site_name = site_name.lower()
    #     print(site_name)
    #     for siteName in sites.values():
    #         print(type(siteName['siteName']))
    #         print(siteName['siteName'].lower())
    #         if siteName["siteName"].lower() == site_name:
    #             print("???")
    #             return True
    #     return False

    # command_options = ['site1']
    # if command_options[0].lower().startswith('site'):
    #     print('OKK')
    # if __check_siteName_valid(sites, command_options[0]) == False:
    #     print('OK')
    # # path_to_read = get_data_file_path(folder_site, 'aa.txt')
    # # print(path_to_read)
    # # a = ['aaaa','aaaa','aaaa','aaaa','aaaa','aaaa','aaaa','aaaa','aaaa','aaa']
    # # x = ''.join(a[2:])
    # # print(type(x))
    # #a = get_data_file_path()
    # #doc data ghi vao file_content
    # timestamps = {"Site1": 1, "Site2": 0, "Site3": 0, "Site4": 0, "Site5": 0}
    # tm1 = {"Site1": 4, "Site2": 3, "Site3": 5, "Site4": 1, "Site5": 2}
    # def __increase_timestamps(_timestamps) -> dict:
    #     """
    #         Increasing timestamps local by 1
    #     """
    #     site_name = "Site3"
    #     _timestamps[site_name] += 1
    #     return _timestamps

    # def __update_receive_timestamps(root_tms, timestamps: dict) -> dict:
    #     """
    #         Updating local timestamps when receiving message with timestamps
    #     """
    #     root_tms = __increase_timestamps(root_tms)

    #     for tstamps_site in timestamps.keys():
    #         if tstamps_site != "Site3":
    #             root_tms[tstamps_site] = max(timestamps[tstamps_site], root_tms[tstamps_site])

    #     return root_tms
    # print(__update_receive_timestamps(timestamps, tm1))
    # def __update_receive_vp(root_vp, vp: dict) -> dict:
    #     """
    #         Updating local V_P when receiving message with V_Ps
    #     """
    #     for vp_site in vp.keys():
    #         if vp_site != "Site3":
    #             # vp_site:
    #             # 1. if site not in vp_site receive
    #             if vp_site not in root_vp.key():
    #                 self._vp[vp_site] = vp[vp_site]
    #             else:
    #                 # nếu có thì kt các update site khác
    #                 for vp_child in self._vp[vp_site].keys():
    #                     # if self._vp[vp_site][vp_child] <= vp[vp_site][vp_child]:
    #                     #     self._vp[vp_site][vp_child] = vp[vp_site][vp_child]
    #                     self._vp[vp_site][vp_child] = max(self._vp[vp_site][vp_child], vp[vp_site][vp_child])
    #     return self._vp

    # a = MessageType.RECEIVE_MOUNT.value
    # if a < 0:
    #     print(a)
    # 1. Cập nhật timestamps site nhận

    # 3. Lấy fileName cần ghi xuống vào othersite sharepeersite và in ra console

    file_name = 'filesite2.txt'
    file_content = "aaaaaaaaa"

    # 4. Lấy path tới sharepeersite response để save/ ghi vào
    site_response_name = "Site2"
    site_name = "Site1"
    folder_site = get_otherpeer_folder(site_name, site_response_name)
    path_to_save = get_data_file_path(folder_site, file_name)

    content_read = write_data_to_file(path_to_save, file_content)
    #self._logger.Log(f"[{message._receiver}]: Received Response MOUNT and saved content: [{message._messageContent}]", "INFO")

    # msg_type_name = MessageType.get_messagetype_by_index(message._messageType)
    # self._logger.Log_Sent(message, msg_type_name)
    def get_files_in_folder(folder_path) -> list:
        file_names = []
        for _, _, files in os.walk(folder_path):
            file_names.extend(files)

        return file_names
    folder = get_peer_folder(site_name)
    list = get_files_in_folder(folder)
    print(list)
    a = get_otherpeer_folder("Site1", "Site2")
    aa = get_data_file_path(a, "filesite2.txt")
    print(is_filename_exists(aa))
    print(a)
