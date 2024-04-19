import json
import os
import socket
import sys
import threading

from dotenv import load_dotenv

from utils.loggings import Logging


class Server:
    """
        client_socket: type socket
        address: type tuple

        Server khi nhận yêu cầu connect từ client , sẽ gửi thông tin các client
        còn lại cho connect mới, và cũng như update cho các sites còn lại
    """
    config = load_dotenv()
    HOST = os.environ.get('HOST')
    PORT = int(os.environ.get('PORT'))
    def __init__(self):
        self._clients = {}
        self._lock = threading.Lock()
        self._logger = Logging("../logs", "server_logs.txt")

        self._serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._serverSocket.bind((Server.HOST,Server.PORT))
    def dict_to_string(self, dict: dict) -> dict:
        return {str(addr): str(socketInfo) for addr, socketInfo in
        dict.items()}


    def send_broadcast_sites_update(self, client_socket):
        with self._lock:
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

    def handle_client_connected(self, client_socket, address):
        self._logger.Log(f"Adding Connection {address} to pool", "INFO")
        # Them sites vao trong server
        with self._lock:
            #self._clients[address] = client_socket
            self._clients[address] = f"Site{len(self._clients)+1}"
        print(self._clients)
        """ Test
        # for key, val in self._clients.items():
        #     print(f"{key} : {type(key)} | {val} : {type(val)}")
        #     print(f"{val.getsockname()} : {val.getpeername()}")
        """
        self.send_broadcast_sites_update(client_socket)

        # Nhận data từ các sites
        while True:
            data = client_socket.recv(2048).decode()
            #data = json.loads(data)
            #data = self._serverSocket.recv(1024).decode()
            print(f"{data} : {type(data)}")
            print(f"{client_socket.getpeername()} : {client_socket.getsockname()}")
            # if not data:
            #     self._logger.Log(f"Sites: {client_socket.getpeername()} nothing data", "INFO")
            if data == 'exit':
                self._logger.Log(f"Sites: {client_socket.getpeername()} sent Disconnect", "INFO")
                break

            self._logger.Log(f"from connected Site: {data}", "INFO")
            # with self._lock:
            #     for addr, sock in self._clients.items():
            #         if sock != client_socket:
            #             sock.sendall(data.encode())

        with self._lock:
            del self._clients[address]
        client_socket.close()

    def server_run(self):
        self._serverSocket.listen(2)
        self._logger.Log(f"Server Start at {self.HOST}:{self.PORT}","INFO")

        while True:
            client_socket, address = self._serverSocket.accept()
            server_receive = threading.Thread(target=self.handle_client_connected, \
                            args= (client_socket, address))
            server_receive.start()
