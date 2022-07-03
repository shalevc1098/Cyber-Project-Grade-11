import threading
import pygame
import socket
import sys
import time
import importlib
import numpy as np
from GUIS.hub import hub
from GUIS.chat import chat

WIDTH = 800
HEIGHT = 800
BOARD_ROWS = 6
BOARD_COLS = 7
SQUARE_SIZE_ROWS = (WIDTH - 200) // BOARD_ROWS
SQUARE_SIZE_COLS = (WIDTH - 100) // BOARD_COLS

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
ONE_COLOR = (84, 84, 84)
TWO_COLOR = (242, 235, 211)

board = np.zeros((BOARD_ROWS, BOARD_COLS))

current = 1
motion_x = 0
motion_y = 0
running = True
game_over = False
drawing = False
circles = []

# object class

class Circle:
    def __init__(self, x, y, color, radius, width, stop_y = None):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.width = width
        self.gravity = 0.002
        self.stop_y = stop_y

    def draw(self, screen):
        if self.stop_y and self.y + self.gravity > self.stop_y:
            pygame.draw.circle(screen, self.color, (self.x, self.stop_y), self.radius, self.width)
        else:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.width)
    
    def update(self, screen):
        screen.fill(BG_COLOR)
        draw_board(screen)
        draw_circles(screen)
        if self.y + self.gravity > self.stop_y:
            return False
        else:
            self.y += self.gravity
            self.gravity += 0.5
            return True

def draw_circles(screen):
    for circle in circles:
        circle.draw(screen)

def draw_board(screen):
    # horizontal lines
    horizontal_counter = 150
    for i in range(7):
        pygame.draw.line(screen, LINE_COLOR, (50, horizontal_counter), (750, horizontal_counter), 15)
        horizontal_counter += 100

    # vertical lines
    vertical_counter = 150
    pygame.draw.line(screen, LINE_COLOR, (50, 143), (50, 757), 15)
    for i in range(6):
        pygame.draw.line(screen, LINE_COLOR, (vertical_counter, 150), (vertical_counter, 750), 15)
        vertical_counter += 100
    pygame.draw.line(screen, LINE_COLOR, (750, 143), (750, 757), 15)

def available_square(row, col):
    return board[row][col] == 0

def update_turn():
    global current
    current = current % 2 + 1
    if current == 1:
        pygame.display.set_caption("FOUR IN A ROW - BLACK")
    elif current == 2:
        pygame.display.set_caption("FOUR IN A ROW - WHITE")

def draw_circle_helper(screen, circle):
    global drawing
    drawing = True
    while True:
        if circle.update(screen):
            circle.draw(screen)
        else:
            circle.draw(screen)
            pygame.display.update()
            break
        pygame.display.update()
    drawing = False

def draw_circle(screen, row, col):
    global current, motion_x, motion_y
    circle = None
    while row >= 0:
        if available_square(row, col):
            board[row][col] = current
            x = 100 + (100 * col)
            y = 200 + (100 * row)
            if current == 1:
                circle = Circle(x, motion_y, ONE_COLOR, 35, 100, y)
                draw_circle_helper(screen, circle)
            elif current == 2:
                circle = Circle(x, motion_y, TWO_COLOR, 35, 100, y)
                draw_circle_helper(screen, circle)
            circles.append(circle)
            return
        row -= 1

def restart(screen):
    screen.fill(BG_COLOR)
    draw_board(screen)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

def row_full(row, col):
    while row >= 0:
        if available_square(row, col):
            return False
        row -= 1
    return True

def board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if available_square(row, col):
                return False
    return True

one_counter = 0
two_counter = 0
first_pos = ()
last_pos = ()

def check_winner(screen, row, col):
    global one_counter, two_counter, first_pos, last_pos
    if board[row][col] == 0:
        if one_counter > 0:
            one_counter = 0
        if two_counter > 0:
            two_counter = 0
        first_pos = ()
        last_pos = ()
    elif board[row][col] == 1:
        if two_counter > 0:
            two_counter = 0
        if one_counter == 0:
            first_pos = (row, col)
        one_counter += 1
        if one_counter >= 4:
            last_pos = (row, col)
            pygame.draw.line(screen, TWO_COLOR, (100 + (100 * first_pos[1]), 200 + (100 * first_pos[0])), (100 + (100 * last_pos[1]), 200 + (100 * last_pos[0])), 15)
            return True
    elif board[row][col] == 2:
        if one_counter > 0:
            one_counter = 0
        if two_counter == 0:
            first_pos = (row, col)
        two_counter += 1
        if two_counter >= 4:
            last_pos = (row, col)
            pygame.draw.line(screen, ONE_COLOR, (100 + (100 * first_pos[1]), 200 + (100 * first_pos[0])), (100 + (100 * last_pos[1]), 200 + (100 * last_pos[0])), 15)
            return True
    return False

def checker_for_horizontal(screen):
    global one_counter, two_counter
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_winner(screen, row, col):
                return True
        one_counter = 0
        two_counter = 0
    return False

def checker_for_vertical(screen):
    global one_counter, two_counter
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS):
            if check_winner(screen, row, col):
                return True
        one_counter = 0
        two_counter = 0

def checker1_for_diag1(screen):
    global one_counter, two_counter
    for row in range(BOARD_ROWS):
        for col in range(row + 1):
            if check_winner(screen, row, col):
                return True
            if row > 0:
                row -= 1
        one_counter = 0
        two_counter = 0

def checker2_for_diag1(screen):
    global one_counter, two_counter
    for row in range(BOARD_ROWS - 1, -1, -1):
        for col in range(BOARD_COLS - 1, row, -1):
            if check_winner(screen, row, col):
                return True
            if row < BOARD_ROWS:
                row += 1
        one_counter = 0
        two_counter = 0

def checker1_for_diag2(screen):
    global one_counter, two_counter
    for row in range(BOARD_ROWS - 1, -1, -1):
        for col in range(BOARD_COLS - 1 - row):
            if check_winner(screen, row, col):
                return True
            if row < BOARD_ROWS:
                row += 1
        one_counter = 0
        two_counter = 0

def checker2_for_diag2(screen):
    global one_counter, two_counter
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 1, BOARD_ROWS - row - 1, -1):
            if check_winner(screen, row, col):
                return True
            if row > 0:
                row -= 1
        one_counter = 0
        two_counter = 0

def check_win(screen):
    if checker_for_horizontal(screen) or checker_for_vertical(screen) or checker1_for_diag1(screen) or checker2_for_diag1(screen) or checker1_for_diag2(screen) or checker2_for_diag2(screen):
        return True
    return False

def hanlde_server_response(my_socket, screen, game_id, username):
    global current, game_over, running
    while running:
            response = my_socket.recv(1024).decode()
            args = response.split(",")
            if args[0] == "chat":
                chat.messages.put(args)
                continue
            if args[0] == "update_turn":
                current = int(args[1])
                if game_over:
                    #restart(my_socket, game_id, screen)
                    pass
            elif args[0] == "mark_square":
                row = int(args[1])
                col = int(args[2])
                figure = int(args[3])
                draw_circle(screen, row, col)
                if check_win(screen):
                    game_over = True
            elif args[0] == "end_game":
                running = False
                chat.set_running(False)
            elif args[0] == "new_game":
                new_game(screen)

def game_handler(game_id, player, my_socket, username, geometry, screen,):
    global running, current, game_over, motion_x, motion_y, drawing
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                my_socket.send(f"fourinarow,end_game,{game_id}".encode())
                break
            if event.type == pygame.MOUSEMOTION and not game_over and player == current and not drawing:
                motion_x = event.pos[0]
                motion_y = 100
                screen.fill(BG_COLOR)
                draw_board(screen)
                draw_circles(screen)
                if current == 1:
                    circle = Circle(motion_x, motion_y, ONE_COLOR, 35, 100)
                elif current == 2:
                    circle = Circle(motion_x, motion_y, TWO_COLOR, 35, 100)
                circle.draw(screen)
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == current and not drawing:
                mouseX = event.pos[0] - 50
                mouseY = event.pos[1] - 143
                row = mouseY // SQUARE_SIZE_ROWS
                col = mouseX // SQUARE_SIZE_COLS
                if -1 <= row < 6 and 0 <= col < 7 and not row_full(row + 1, col):
                    my_socket.send(f"fourinarow,mark_square,{game_id},{player},{BOARD_ROWS - 1},{col}".encode())
                    my_socket.send(f"fourinarow,update_turn,{game_id},{player % 2 + 1}".encode())
        if board_full():
            #restart(screen)
            pass
        if not drawing:
            pygame.display.update()
            
def start(game_id, player, my_socket, username, geometry):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("FOUR IN A ROW - BLACK")
    screen.fill(BG_COLOR)
    draw_board(screen)
    my_socket.send("chat,get_last_chat_id".encode())
    chat_id = int(my_socket.recv(1024).decode())
    a = threading.Thread(target=hanlde_server_response, args=(my_socket, screen, game_id, username,))
    a.start()
    a = threading.Thread(target=game_handler, args=(game_id, player, my_socket, username, geometry, screen,))
    a.start()
    importlib.reload(chat)
    chat.start(my_socket, username, chat_id)
    pygame.quit()
    my_socket.send(f"chat,remove_room,{chat_id}".encode())
    my_socket.recv(1024)
    importlib.reload(hub)
    hub.vp_start_gui(my_socket, username, geometry)

if __name__ == "__main__":
    start()