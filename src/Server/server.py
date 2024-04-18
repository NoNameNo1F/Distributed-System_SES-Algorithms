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

    def send_broadcast_sites_update(self, client_socket):
        with self._lock:
            #sites = self._clients.copy()
            for addr, sock in self._clients.items():
                sites = self._clients.copy()
                print(sites)
                del sites[addr]
                if len(sites) > 0:
                    #self._serverSocket.sendall(json.dumps(sites).encode(), addr)
                    client_socket.sendall(json.dumps(sites).encode())
                else:
                    #self._serverSocket.sendall(json.dumps('You are connected').encode())
                    client_socket.sendall(json.dumps(sites).encode())
                # if addr in sites.keys():
                #     del sites[addr]
                #     self._serverSocket.sendto(json.dumps(sites).encode(), addr)
                # client_socket.sendall(json.dumps(update_item).encode())
                # if item != address:
                #     print(f"{item} : {type(item)} {self._clients[item]} : {type(self._clients[item])}")
                #     update_item.append(item)

    def handle_client_connected(self, client_socket, address):
        self._logger.Log(f"Adding Connection {address} to pool", "INFO")
        # Them sites vao trong server
        with self._lock:
            self._clients[address] = client_socket

        self.send_broadcast_sites_update(client_socket)

        # Nhận data từ các sites
        while True:
            data = client_socket.recv(2048).decode()
            #data = self._serverSocket.recv(1024).decode()
            if data == 'exit' or not data:
                self._logger.Log(f"Sites: {data.getsockname()} sent Disconnect", "INFO")
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
            server_receive.setDaemon(True)
            server_receive.start()
# import json
# import os
# import socket

# from dotenv import load_dotenv

# from utils.loggings import Logging


# class Server:
#     def __init__(self):
#         self._clients = {}
#         self._lock = None  # No need for threading lock
#         self._logger = Logging("../logs", "server_logs.txt")

#     def HandleClientConnected(self, client_socket, address):
#         self._logger.Log(f"Connection from {address}", "INFO")
#         self._clients[address] = client_socket

#         client_socket.sendall(json.dumps(list(self._clients.keys())).encode())

#         while True:
#             data = client_socket.recv(1024).decode()
#             if not data:
#                 break

#             self._logger.Log(f"from connected Site: {data}", "INFO")
#             for addr, sock in self._clients.items():
#                 if sock != client_socket:
#                     sock.sendall(data.encode())

#         del self._clients[address]
#         client_socket.close()

#     def ServerRun(self):
#         config = load_dotenv()
#         host = os.environ.get('HOST')
#         port = int(os.environ.get('PORT'))

#         server_socket = socket.socket()
#         server_socket.bind((host, port))
#         server_socket.listen(2)

#         self._logger.Log(f"Server Start at {host}:{port}","INFO")

#         while True:
#             client_socket, address = server_socket.accept()
#             self.HandleClientConnected(client_socket, address)

#         server_socket.close()  # Close the server socket when done
