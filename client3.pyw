import sys
import socket
import threading
#sys.path.insert(0, './GUIS/authentication')
#import authentication
sys.path.insert(0, './GUIS/hub')
import hub

def client_send(my_socket):
    hub.vp_start_gui(my_socket, "3")

    #my_socket.shutdown(socket.SHUT_RDWR)
    #my_socket.close()

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