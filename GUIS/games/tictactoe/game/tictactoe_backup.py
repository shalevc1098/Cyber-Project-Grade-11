import threading
import pygame
import socket
import sys
import time
import importlib
import numpy as np
from GUIS.hub import hub

# screen stuff
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (242, 235, 211)
CROSS_COLOR = (84, 84, 84)

# screen setup

# board
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# draws the lines of the tic tac toe game.
def draw_lines(screen):
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# draws cross or circle depends on the figure the player is.
def draw_figures(row, col, screen):
    print(board[row][col])
    if board[row][col] == 1:
        pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
        pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
        return True

    elif board[row][col] == 2:
        pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
        return True

# inserting 1 || 2 into the row and col of the board that the player clicked on.
def mark_square(row, col, player):
    board[row][col] = player

# checks if the square that the user clicked on is available. it will return true if yes, otherwise it will return false.
def available_square(row, col):
    return board[row][col] == 0

# checks if all the board slots are full. it will return true if yes, otherwise it will return false.
def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True

def check_win(player, screen):
    # vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player, screen)
            return True
    # horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player, screen)
            return True

    # asc win check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal(player, screen)
        return True
    
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal(player, screen)
        return True

    return False

def draw_vertical_winning_line(col, player, screen):
    if player == 1:
        pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, 15), (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 15), 15)

    elif player == 2:
        pygame.draw.line(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, 15), (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 15), 15)


def draw_horizontal_winning_line(row, player, screen):
    if player == 1:
        pygame.draw.line(screen, CROSS_COLOR, (15, row * SQUARE_SIZE + SQUARE_SIZE // 2), (HEIGHT - 15, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    elif player == 2:
        pygame.draw.line(screen, CIRCLE_COLOR, (15, row * SQUARE_SIZE + SQUARE_SIZE // 2), (HEIGHT - 15, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

def draw_asc_diagonal(player, screen):
    if player == 1:
        pygame.draw.line(screen, CROSS_COLOR, (15, HEIGHT - 15), (HEIGHT - 15, 15), 15)

    elif player == 2:
        pygame.draw.line(screen, CIRCLE_COLOR, (15, HEIGHT - 15), (HEIGHT - 15, 15), 15)

def draw_desc_diagonal(player, screen):
    if player == 1:
        pygame.draw.line(screen, CROSS_COLOR, (15, 15), (HEIGHT - 15, HEIGHT - 15), 15)

    elif player == 2:
        pygame.draw.line(screen, CIRCLE_COLOR, (15, 15), (HEIGHT - 15, HEIGHT - 15), 15)

def restart(my_socket, game_id, screen):
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, (250, 102, 5), (100,450,100,50))
    pygame.draw.rect(screen, (150, 202, 15), (400,450,100,50))

current = 1
game_over = False
running = True
ready = False

def new_game(screen):
    global current, game_over, running, ready
    screen.fill(BG_COLOR)
    draw_lines(screen)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0
    game_over = False
    ready = False
    current = 1
    
def hanlde_server_response(my_socket, screen, game_id, username):
    global current, game_over, running
    while running:
            print(game_id)
            response = my_socket.recv(1024).decode()
            print(response)
            args = response.split(",")
            if args[0] == "update_turn" or args[0] == "check_turn":
                current = int(args[1])
                if game_over:
                    restart(my_socket, game_id, screen)
            elif args[0] == "mark_square":
                row = int(args[1])
                col = int(args[2])
                figure = int(args[3])
                mark_square(row, col, figure)
                draw_figures(row, col, screen)
                if check_win(figure, screen):
                    game_over = True
                    time.sleep(0.25)
            elif args[0] == "end_game":
                running = False
            elif args[0] == "new_game":
                new_game(screen)

# main loop
def start(game_id, player, my_socket, username, geometry):
    global currnet, game_over, running, ready
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    if player == 1:
        pygame.display.set_caption("TIC TAC TOE - X")
    elif player == 2:
        pygame.display.set_caption("TIC TAC TOE - O")
    screen.fill(BG_COLOR)
    draw_lines(screen)
    a = threading.Thread(target=hanlde_server_response, args=(my_socket, screen, game_id, username,))
    a.start()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                my_socket.send(f"tictactoe,end_game,{game_id}".encode())
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                if not game_over:
                    clicked_row = int(mouseY // SQUARE_SIZE)
                    clicked_col = int(mouseX // SQUARE_SIZE)
                    if current == player:
                        if available_square(clicked_row, clicked_col):
                            my_socket.send(f"tictactoe,mark_square,{game_id},{player},{clicked_row},{clicked_col}".encode())
                            my_socket.send(f"tictactoe,update_turn,{game_id},{player % 2 + 1}".encode())
                else:
                    if 100 <= mouseX <= 200 and 450 <= mouseY <= 500:
                        my_socket.send(f"tictactoe,end_game,{game_id}".encode())
                    elif 400 <= mouseX <= 500 and 450 <= mouseY <= 500:
                        if not ready:
                            ready = True
                            pygame.draw.rect(screen, (150, 0, 15), (400,450,100,50))
                            my_socket.send(f"tictactoe,ready,{game_id}".encode())
                        else:
                            ready = False
                            pygame.draw.rect(screen, (150, 202, 15), (400,450,100,50))
                            my_socket.send(f"tictactoe,unready,{game_id}".encode())

        pygame.display.update()
    pygame.quit()
    importlib.reload(hub)
    hub.vp_start_gui(my_socket, username, geometry)