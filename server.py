import socket
import atexit
from utils import db, tictactoe_queue_utils, tictactoe_utils, fourinarow_queue_utils, fourinarow_utils, chat_utils
from threading import Thread

global_connected = []
tictactoe_queue = {}
fourinarow_queue = {}
active_chats = {}

def exit_handler():
    for client in global_connected:
        client.close()

atexit.register(exit_handler)

def get_client_from_tictactoe_queue(my_socket, username):
    if username in tictactoe_queue.keys():
        return tictactoe_queue[username]
    return my_socket

def get_client_from_fourinarow_queue(my_socket, username):
    if username in fourinarow_queue.keys():
        return fourinarow_queue[username]
    return my_socket

def handle_client_command(my_socket, request):
    request = str(request)
    args = request.split(",")
    command = args[0]
    if command == "db":
        return db.check_request(request)
    
    elif command == "tictactoe_queue":
        if len(args) >= 3:
            username = args[2]
        if args[1] == "addtoqueue":
            tictactoe_queue[username] = my_socket
            return tictactoe_queue_utils.check_request(request)
        elif args[1] == "removefromqueue":
            del tictactoe_queue[username]
            return tictactoe_queue_utils.check_request(request)
        elif args[1] == "append":
            for client in tictactoe_queue:
                message = "append,"
                for key in tictactoe_queue:
                    if client != key:
                        message += key + ","
                message = message[:-1]
                if message != "append":
                    tictactoe_queue[client].send(message.encode())
            return "append"
        elif args[1] == "deappend":
            for client in tictactoe_queue:
                tictactoe_queue[client].send(f"deappend,{username}".encode())
            return "deappend"
        elif args[1] == "invite":
            target = args[3]
            client = get_client_from_tictactoe_queue(my_socket, target)
            if client != my_socket:
                client.send(f"new_invitation,{username},{target}".encode()) #username -> inviter, target -> invited
            else:
                my_socket.send(f"error_box,An error occurred!,There was an error during the invitation proccess. Please try again in few seconds.".encode())
            return "tictactoe_queue,invite"
        elif args[1] == "cancel_invite":
            target = args[3]
            target_client = get_client_from_tictactoe_queue(my_socket, target)
            target_client.send(f"cancel_invite,{username}".encode())
            return "tictactoe_queue,cancel_invite"
        elif args[1] == "reset_selection":
            for client in tictactoe_queue:
                tictactoe_queue[client].send("reset_selection".encode())
            return "tictactoe_queue,reset_selection"
        elif args[1] == "start_game":
            target = args[3]
            client1 = my_socket
            client2 = get_client_from_tictactoe_queue(my_socket, username)
            for i in range(2):
                tictactoe_queue_utils.check_request("tictactoe_queue,removefromqueue")
            tictactoe_utils.check_request(command = "new_game", client1 = client1, client2 = client2)
            del tictactoe_queue[username]
            del tictactoe_queue[target]
            return "tictactoe_queue,start_game"
        elif args[1] == "info_box_to_another_client":
            target = args[2]
            title = args[3]
            description = args[4]
            target_client = get_client_from_tictactoe_queue(my_socket, target)
            if len(args) == 6:
                cmd = args[5]
                target_client.send(f"info_box,{title},{description},{cmd}".encode())
            else:
                target_client.send(f"info_box,{title},{description}".encode())
            return "tictactoe_queue,info_box"
        elif args[1] == "error_box_to_another_client":
            target = args[2]
            title = args[3]
            description = args[4]
            target_client = get_client_from_tictactoe_queue(my_socket, target)
            if len(args) == 6:
                cmd = args[5]
                target_client.send(f"error_box,{title},{description},{cmd}".encode())
            else:
                target_client.send(f"error_box,{title},{description}".encode())
            return "tictactoe_queue,error_box"

    elif command == "tictactoe":
        if len(args) == 3:
            command = args[1]
            game_id = int(args[2])
            return tictactoe_utils.check_request(sender=my_socket, command=command, game_id=game_id)
        elif len(args) == 4:
            command = args[1]
            game_id = int(args[2])
            figure = int(args[3])
            return tictactoe_utils.check_request(sender=my_socket, command=command, game_id=game_id, figure=figure)
        elif len(args) == 6:
            command = args[1]
            game_id = int(args[2])
            figure = int(args[3])
            row = int(args[4])
            col = int(args[5])
            return tictactoe_utils.check_request(sender=my_socket, command=command, game_id=game_id, figure=figure, row=row, col=col)

    elif command == "fourinarow_queue":
        if len(args) >= 3:
            username = args[2]
        if args[1] == "addtoqueue":
            fourinarow_queue[username] = my_socket
            return fourinarow_queue_utils.check_request(request)
        elif args[1] == "removefromqueue":
            del fourinarow_queue[username]
            return fourinarow_queue_utils.check_request(request)
        elif args[1] == "append":
            for client in fourinarow_queue:
                message = "append,"
                for key in fourinarow_queue:
                    if client != key:
                        message += key + ","
                message = message[:-1]
                if message != "append":
                    fourinarow_queue[client].send(message.encode())
            return "append"
        elif args[1] == "deappend":
            for client in fourinarow_queue:
                fourinarow_queue[client].send(f"deappend,{username}".encode())
            return "deappend"
        elif args[1] == "invite":
            target = args[3]
            client = get_client_from_fourinarow_queue(my_socket, target)
            if client != my_socket:
                client.send(f"new_invitation,{username},{target}".encode()) #username -> inviter, target -> invited
            else:
                my_socket.send(f"error_box,An error occurred!,There was an error during the invitation proccess. Please try again in few seconds.".encode())
            return "fourinarow_queue,invite"
        elif args[1] == "cancel_invite":
            target = args[3]
            target_client = get_client_from_fourinarow_queue(my_socket, target)
            target_client.send(f"cancel_invite,{username}".encode())
            return "fourinarow_queue,cancel_invite"
        elif args[1] == "reset_selection":
            for client in fourinarow_queue:
                fourinarow_queue[client].send("reset_selection".encode())
            return "fourinarow_queue,reset_selection"
        elif args[1] == "start_game":
            target = args[3]
            client1 = my_socket
            client2 = get_client_from_fourinarow_queue(my_socket, username)
            for i in range(2):
                fourinarow_queue_utils.check_request("fourinarow_queue,removefromqueue")
            fourinarow_utils.check_request(command = "new_game", client1 = client1, client2 = client2)
            del fourinarow_queue[username]
            del fourinarow_queue[target]
            return "fourinarow_queue,start_game"
        elif args[1] == "info_box_to_another_client":
            target = args[2]
            title = args[3]
            description = args[4]
            target_client = get_client_from_fourinarow_queue(my_socket, target)
            if len(args) == 6:
                cmd = args[5]
                target_client.send(f"info_box,{title},{description},{cmd}".encode())
            else:
                target_client.send(f"info_box,{title},{description}".encode())
            return "fourinarow_queue,info_box"
        elif args[1] == "error_box_to_another_client":
            target = args[2]
            title = args[3]
            description = args[4]
            target_client = get_client_from_fourinarow_queue(my_socket, target)
            if len(args) == 6:
                cmd = args[5]
                target_client.send(f"error_box,{title},{description},{cmd}".encode())
            else:
                target_client.send(f"error_box,{title},{description}".encode())
            return "fourinarow_queue,error_box"

    elif command == "fourinarow":
        if len(args) == 3:
            command = args[1]
            game_id = int(args[2])
            return fourinarow_utils.check_request(sender=my_socket, command=command, game_id=game_id)
        elif len(args) == 4:
            command = args[1]
            game_id = int(args[2])
            figure = int(args[3])
            return fourinarow_utils.check_request(sender=my_socket, command=command, game_id=game_id, figure=figure)
        elif len(args) == 6:
            command = args[1]
            game_id = int(args[2])
            figure = int(args[3])
            row = int(args[4])
            col = int(args[5])
            return fourinarow_utils.check_request(sender=my_socket, command=command, game_id=game_id, figure=figure, row=row, col=col)
            
    elif command == "chat":
        if args[1] == "get_last_chat_id":
            chat_id = chat_utils.get_last_chat_id()
            if chat_id not in active_chats:
                active_chats[chat_id] = []
            active_chats[chat_id].append(my_socket)
            my_socket.send(str(chat_id).encode())
        elif args[1] == "addmessage":
            chat_id = int(args[2])
            for client in active_chats[chat_id]:
                client.send(f"chat,addmessage,{args[3]}: {args[4]}".encode())
        elif args[1] == "remove_room":
            chat_id = int(args[2])
            if chat_id in active_chats:
                del active_chats[chat_id]
                my_socket.send("Success".encode())
            else:
                my_socket.send("Already removed".encode())
        return "chat"
        
def handle_client(client_socket):
    blacklisted_words = [
        "tictactoe",
        "fourinarow",
        "append",
        "deappend",
        "invite",
        "tictactoe_queue",
        "fourinarow_queue",
        "chat"
    ]
    global_connected.append(client_socket)
    while True:
        try:
            request = client_socket.recv(1024).decode()
        except:
            break
        if request == "":
            break
        request = str(handle_client_command(client_socket, request))
        args = request.split(",")
        if args[0] == "tictactoe_queue_addtoqueue" or args[0] == "tictactoe_queue_removefromqueue":
            request = request.replace("tictactoe_queue_", "")
            for client in tictactoe_queue:
                tictactoe_queue[client].send(request.encode())
        elif args[0] == "fourinarow_queue_addtoqueue" or args[0] == "fourinarow_queue_removefromqueue":
            request = request.replace("fourinarow_queue_", "")
            for client in fourinarow_queue:
                fourinarow_queue[client].send(request.encode())
        elif args[0] not in blacklisted_words:
            client_socket.send(f"{request}".encode())

    if client_socket in global_connected:
        global_connected.remove(client_socket)
    client_socket.close()
    print("Client Disconnected")


class Server():
    def __init__(self, ip, port):
        self.server_socket = socket.socket()
        print ("Socket successfully created")
        self.ip = ip
        self.port = port
        self.server_socket.bind((ip, port))
        print("socket binded to %s" %(self.port))

    def run(self):
        self.server_socket.listen(5)
        print("socket is listening")
        while True:
            (client_socket, client_address) = self.server_socket.accept()
            print(f"Client connected {client_address}")
            a = Thread(target=handle_client, args=(client_socket,))
            a.start()

if __name__ == "__main__":
    a = Server("127.0.0.1", 8820)
    a.run()