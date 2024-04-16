import os
import socket

from dotenv import load_dotenv

from utils.loggings import Logging


def client():
    config = load_dotenv()
    host = os.environ.get('HOST')
    port = int(os.environ.get('PORT'))
    client_socket = socket.socket()
    client_socket.connect((host, port))
    logger = Logging("..\logs","logs.txt")

    client_socket.sendall(str((host, port)).encode())

    connected_clients = client_socket.recv(1024).decode()
    connected_clients = eval(connected_clients)
    logger.Log(f"Connected clients: {connected_clients}", "INFO")

    other_clients = []

    """
        Nếu có site khác thì sẽ thêm vào other_clients
    """
    if (host, port) in connected_clients:
        connected_clients.remove((host, port))
        other_clients = connected_clients

        print("Other clients:", other_clients)

    message = input(' -> ')
    while message.lower().strip() != 'bye':
        if len(other_clients) > 0:
            # Chọn site muốn communicate
            print("Select a client to communicate with:")
            for index, client_addr in enumerate(other_clients, start=1):
                print(f"{index}. {client_addr}")
            client_idx = int(input("Enter the client number: ")) - 1

            # Send message to selected client
            selected_client = other_clients[client_idx]
            client_socket.sendall(selected_client.encode())
        else:
            print("No other clients to communicate with.")

        data = client_socket.recv(1024).decode()

        logger.Log(f"Received from server: {data}", "INFO")

        message = input(' -> ')
    client_socket.close()

