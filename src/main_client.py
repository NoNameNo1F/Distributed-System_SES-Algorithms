import os
import sys
import threading
import time

from dotenv import load_dotenv

from Client.client import *
from core.Message.message_type import MessageType

if __name__ == "__main__":
    if(len(sys.argv) == 2):
        input_port = int(sys.argv[1])
        if input_port in range(7670,7675):
            time.sleep(2)
            client = PeerYFS(input_port)
            client_yls = threading.Thread(target=client.client_listen_event, args=())
            client_input = threading.Thread(target=client.handle_site_command, args=())
            #client_input = threading.Thread(target=handle_site_command, args=(client,))
            #client_yls.daemon = True
            client_yls.start()
            client_input.start()

            # client_yls.join()
            # client_input.join()

    else:
        print(f'command require PORT or PORT not appropriate to initialize the client')
