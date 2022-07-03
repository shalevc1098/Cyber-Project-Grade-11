import sys
import socket
import random
from GUIS.games.tictactoe.game import tictactoe

active_games = {}
last_game_id = 1

def check_request(command = None, client1 = None, client2 = None, sender = None, figure = None, game_id = None, row = None, col = None):
    global last_game_id
    if command == "new_game":
        active_games[last_game_id] = TicTacToe(client1, client2, last_game_id)
        last_game_id += 1
        return "tictactoe,new_game"
    elif command == "check_turn":
        sender.send(str(active_games[game_id].get_turn()).encode())
        return "tictactoe,check_turn"
    elif command == "update_turn":
        active_games[game_id].update_turn(figure)
        for client in active_games[game_id].get_clients():
            try:
                client.send(f"update_turn,{figure}".encode())
            except:
                pass
        return "tictactoe,update_turn"
    elif command == "mark_square":
        for client in active_games[game_id].get_clients():
            try:
                client.send(f"mark_square,{row},{col},{figure}".encode())
            except:
                pass
        return "tictactoe,mark_square"
    elif command == "end_game":
        active_games[game_id].empty_ready_list()
        try:
            for client in active_games[game_id].get_clients():
                client.send(f"end_game".encode())
            del active_games[game_id]
        except:
            pass
        return "tictactoe,end_game"
    elif command == "ready":
        ready_list = active_games[game_id].get_ready_list()
        clients = active_games[game_id].get_clients()
        ready_list.append(sender)
        for client in clients:
            if client not in ready_list:
                sender.send("cant".encode())
                return "tictactoe,ready"
        for client in clients:
            client.send("new_game".encode())
        active_games[game_id].empty_ready_list()
        return "tictactoe,ready"
    elif command == "unready":
        ready_list = active_games[game_id].get_ready_list()
        ready_list.remove(sender)

class TicTacToe:
    def __init__(self, client1, client2, game_id):
        self.client1 = client1
        self.client2 = client2
        self.client1_figure = random.randint(1, 2)
        if self.client1_figure == 1:
            self.client2_figure = 2
        elif self.client1_figure == 2:
            self.client2_figure = 1
        self.current = 1
        self.ready = []
        client1.send(f"start_tictactoe,{game_id},{self.client1_figure}".encode())
        client2.send(f"start_tictactoe,{game_id},{self.client2_figure}".encode())
    
    def get_turn(self):
        return self.current

    def update_turn(self, current):
        self.current = current

    def get_clients(self):
        return [self.client1, self.client2]

    def get_ready_list(self):
        return self.ready

    def empty_ready_list(self):
        self.ready = []