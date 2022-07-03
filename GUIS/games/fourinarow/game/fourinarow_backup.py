import pygame
import sys
import time
import threading
import random
import numpy as np

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
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.width)
    
    def update(self, screen):
        screen.fill(BG_COLOR)
        draw_board(screen)
        draw_circles(screen)
        if self.y + self.gravity > self.stop_y:
            return False
        else:
            self.y += self.gravity
            self.gravity += 0.004
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

def mark_square(row, col):
    global current
    board[row][col] = current

def update_turn():
    global current
    current = current % 2 + 1
    if current == 1:
        pygame.display.set_caption("FOUR IN A ROW - BLACK")
    elif current == 2:
        pygame.display.set_caption("FOUR IN A ROW - WHITE")

def draw_circle_helper(screen, circle):
    while True:
        if circle.update(screen):
            circle.draw(screen)
        else:
            circle.draw(screen)
            pygame.display.update()
            break
        pygame.display.update()

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
            update_turn()
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

def start():
    global running, current, game_over, motion_x, motion_y
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("FOUR IN A ROW - BLACK")
    screen.fill(BG_COLOR)
    draw_board(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION and not game_over:
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
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0] - 50
                mouseY = event.pos[1] - 143
                row = mouseY // SQUARE_SIZE_ROWS
                col = mouseX // SQUARE_SIZE_COLS
                print(row, col)
                if -1 <= row < 6 and 0 <= col < 7 and not row_full(row + 1, col):
                    draw_circle(screen, BOARD_ROWS - 1, col)
                    if check_win(screen):
                        game_over = True
                    else:
                        if current == 1:
                            circle = Circle(motion_x, motion_y, ONE_COLOR, 35, 100)
                        elif current == 2:
                            circle = Circle(motion_x, motion_y, TWO_COLOR, 35, 100)
                        circle.draw(screen)
        if board_full():
            #restart(screen)
            pass
        pygame.display.update()

if __name__ == "__main__":
    start()