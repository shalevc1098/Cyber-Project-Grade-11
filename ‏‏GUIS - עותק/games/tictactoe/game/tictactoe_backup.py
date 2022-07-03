import pygame
import sys
import numpy as np

pygame.init()

# screen stuff
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

# colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (242, 235, 211)
CROSS_COLOR = (84, 84, 84)

# screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC TAC TOE")
screen.fill(BG_COLOR)

# board
board = np.zeros((BOARD_ROWS, BOARD_COLS))


# draws the lines of the tic tac toe game.
def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH)

# draws cross or circle depends on the figure the player is.
def draw_figures(row, col):
    if board[row][col] == 1:
        pygame.draw.line(screen, CROSS_COLOR, (col * 200 + SPACE, row * 200 + 200 - SPACE), (col * 200 + 200 - SPACE, row * 200 + SPACE), CROSS_WIDTH)
        pygame.draw.line(screen, CROSS_COLOR, (col * 200 + SPACE, row * 200 + SPACE), (col * 200 + 200 - SPACE, row * 200 + 200 - SPACE), CROSS_WIDTH)
        return True

    elif board[row][col] == 2:
        pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * 200 + 100), int(row * 200 + 100)), CIRCLE_RADIUS, CIRCLE_WIDTH)
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

def check_win(player):
    # vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True
    # horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True

    # asc win check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal(player)
        return True
    
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal(player)
        return True

    return False

def draw_vertical_winning_line(col, player):
    if player == 1:
        pygame.draw.line(screen, CROSS_COLOR, (col * 200 + 100, 15), (col * 200 + 100, HEIGHT - 15), 15)

    elif player == 2:
        pygame.draw.line(screen, CIRCLE_COLOR, (col * 200 + 100, 15), (col * 200 + 100, HEIGHT - 15), 15)


def draw_horizontal_winning_line(row, player):
    if player == 1:
        pygame.draw.line(screen, CROSS_COLOR, (15, row * 200 + 100), (HEIGHT - 15, row * 200 + 100), 15)

    elif player == 2:
        pygame.draw.line(screen, CIRCLE_COLOR, (15, row * 200 + 100), (HEIGHT - 15, row * 200 + 100), 15)

def draw_asc_diagonal(player):
    if player == 1:
        pygame.draw.line(screen, CROSS_COLOR, (15, HEIGHT - 15), (HEIGHT - 15, 15), 15)

    elif player == 2:
        pygame.draw.line(screen, CIRCLE_COLOR, (15, HEIGHT - 15), (HEIGHT - 15, 15), 15)

def draw_desc_diagonal(player):
    if player == 1:
        pygame.draw.line(screen, CROSS_COLOR, (15, 15), (HEIGHT - 15, HEIGHT - 15), 15)

    elif player == 2:
        pygame.draw.line(screen, CIRCLE_COLOR, (15, 15), (HEIGHT - 15, HEIGHT - 15), 15)

def restart():
    pass

draw_lines()

player = 1

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = int(mouseY // 200)
            clicked_col = int(mouseX // 200)
            if available_square(clicked_row, clicked_col):
                if player == 1:
                    mark_square(clicked_row, clicked_col, 1)
                    check_win(player)
                    player = 2
                elif player == 2:
                    mark_square(clicked_row, clicked_col, 2)
                    check_win(player)
                    player = 1
                draw_figures(clicked_row, clicked_col)
    pygame.display.update()