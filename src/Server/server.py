import json
import os
import socket
import sys
import threading

from dotenv import load_dotenv

from utils.loggings import Logging


class Server:
    def __init__(self):
        self._clients = {}
        self._lock = threading.Lock()
        self._logger = Logging("..\logs", "server_logs.txt")
        
    def BroadcastClientList(self):
        with self._lock:
            client_list = list(self._clients.keys())
            client_data = json.dumps(client_list).encode()
            print("data123",client_data)
            for client_socket in self._clients.values():
                client_socket.sendall(client_data)

    def HandleClientConnected(self, client_socket, address):
        self._logger.Log(f"Connection from {address}", "INFO")
        with self._lock:
            self._clients[address] = client_socket

            #client_socket.sendall(str(list(self._clients.keys())).encode())
            ##client_socket.sendall(json.dumps(list(self._clients.keys())).encode())
            
           
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            self._logger.Log(f"from connected Site: {data}", "INFO")
            self.BroadcastClientList()
            
            # with self._lock:
            #     for addr, sock in self._clients.items():
            #         if sock != client_socket:
            #             sock.sendall(data.encode())

        # with self._lock:
        #     del self._clients[address]
        client_socket.close()

    def ServerRun(self):
        config = load_dotenv()
        host = os.environ.get('HOST')
        port = int(os.environ.get('PORT'))

        server_socket = socket.socket()

        server_socket.bind((host, port))

        server_socket.listen(2)

        self._logger.Log(f"Server Start at {host}:{port}","INFO")

        while True:
            client_socket, address = server_socket.accept()
            threading.Thread(target=self.HandleClientConnected, \
                            args= (client_socket, address)).start()

