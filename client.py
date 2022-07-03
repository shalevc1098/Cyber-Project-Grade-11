import sys
import socket
import threading
from GUIS.authentication import authentication

def client_send(my_socket):
    authentication.vp_start_gui(my_socket)

class Client():
    def __init__(self, ip, port):
        self.my_socket = socket.socket()
        self.ip = ip
        self.port = port
    
    def run(self):
        self.my_socket.connect((self.ip, self.port))
        sendThread = threading.Thread(target=client_send, args=(self.my_socket,))
        sendThread.start()

a = Client("127.0.0.1", 8820)
a.run()