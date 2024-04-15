import os
import socket

from dotenv import load_dotenv

from utils.loggings import Logging


def client():
    config = load_dotenv()
    host = os.environ.get('HOST')
    port = os.environ.get('PORT')
    client_socket = socket.socket()
    client_socket.connect((host, port))
    logger = Logging("logs","logs.txt")
    message = input(' -> ')
    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()

        logger.Log(f"Received from server: {data}", "INFO")

        message = input(' -> ')
    client_socket.close()

if __name__ == "__main__":
    client()
