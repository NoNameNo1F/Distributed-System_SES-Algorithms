import json
import os
import sys
import threading

from dotenv import load_dotenv

from Client.client import *
from core.Message.message_type import MessageType
from utils.helpers import *


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
        port_to_send = int(message_to_send[1])
        sock.sendto(message_to_send[0].encode('utf-8'), ('127.0.0.1', port_to_send))

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
        send_thread = threading.Thread(target=send_messages, args=(sock))

        # Starting threads
        listen_thread.start()
        send_thread.start()

        # Joining threads to the main thread
        listen_thread.join()
        send_thread.join()

if __name__ == "__main__":
    #print(get_parent_path())

    main()
