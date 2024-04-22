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
        message = message_to_send[0:-1]

        port_to_send = int(message_to_send[-1])
        sock.sendto(message.encode('utf-8'), ('127.0.0.1', port_to_send))

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
    #print(get_parent_path())
    # sites = {
    #     7670: {'siteName': 'Site1'},
    #     7671: {'siteName': 'Site2'},
    #     7672: {'siteName': 'Site3'},
    #     7673: {'siteName': 'Site4'},
    #     7674: {'siteName': 'Site5'}
    # }

    #sender = tuple(('127.0.0.1', 7670))
    sender = 7670
    receiver = 7671
    #receiver = tuple(('127.0.0.1', 7671))
    message_type = MessageType.SEND_MOUNT.value
    message_content = ""
    tms = {'Site1': 1, 'Site2': 0, 'Site3': 0, 'Site4': 0, 'Site5': 0}
    vp = {}
    message = Message(sender, receiver, message_type, message_content, tms, vp)
    print(f'{message}\nType: {type(message)}\n')
    print(f'{str(message)}\nType: {type(str(message))}\n')


    message_json = str(message).encode('utf-8')
    print(f'{message_json}\nType: {type(message_json)}\n')
    recv = message_json.decode('utf-8')
    print(f'{recv}\nType: {type(recv)}\n')
    recvvv = Message.from_string(recv)
    print(f'{recvvv}\nType: {type(recvvv)}\n')
    # convertStr2Msg = json.loads(recv)
    # print(f'{convertStr2Msg}\nType: {type(convertStr2Msg)}\n')
    # cStr2Msg = Message.from_dict(convertStr2Msg)
    # print(f'{cStr2Msg}\nType: {type(cStr2Msg)}\n')


    #rere = Message.from_string(recv)

    #print(rere)
    # rere = Message.from_dict(Message(recv_msg))
    # print(rev_rve)
    #main()

