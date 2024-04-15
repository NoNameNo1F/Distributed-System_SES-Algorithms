import os
import socket

from dotenv import load_dotenv

from utils.loggings import Logging


def server():
    logger = Logging("logs","logs.txt")
    config = load_dotenv()
    host = os.environ.get('HOST')
    port = os.environ.get('PORT')
    server_socket = socket.socket()

    server_socket.bind((host, port))

    server_socket.listen(2)
    connection, address = server_socket.accept()
    logger.Log(f"Connection from {address}","INFO")

    while True:
        data = connection.recv(1024).decode()

        if not data:
            break

        logger.Log(f"from connected Site: {data}", "INFO")
        data = input(' -> ')
        connection.send(data.encode('utf'))

    connection.close()

if __name__ == "__main__":
    server()
