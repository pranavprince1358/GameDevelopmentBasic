import math
import sys

import numpy as np
import pygame

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_COUNT = 87


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3]
                    == piece):
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c]
                    == piece):
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] ==
                    piece):
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] ==
                    piece):
                return True


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, (0, 0, 255), (c * SQUARE_COUNT, r * SQUARE_COUNT + SQUARE_COUNT, SQUARE_COUNT,
                                                   SQUARE_COUNT))
            pygame.draw.circle(screen, (0, 0, 0), (c * SQUARE_COUNT + SQUARE_COUNT / 2, r * SQUARE_COUNT
                                                   + SQUARE_COUNT + SQUARE_COUNT / 2), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, (255, 0, 0), (c * SQUARE_COUNT + SQUARE_COUNT / 2, height - (r * SQUARE_COUNT
                                                                                       + SQUARE_COUNT / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, (255, 255, 0), (c * SQUARE_COUNT + SQUARE_COUNT / 2, height - (r *
                                                                              SQUARE_COUNT + SQUARE_COUNT / 2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARE_SIZE = 600
width = COLUMN_COUNT + SQUARE_SIZE
height = (ROW_COUNT + 1) + SQUARE_SIZE
size = (width, height)
RADIUS = int(SQUARE_COUNT / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

my_font = pygame.font.SysFont("monospace", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARE_COUNT))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, (255, 0, 0), (posx, int(SQUARE_COUNT / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, (255, 255, 0), (posx, int(SQUARE_COUNT / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARE_COUNT))
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_COUNT))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = my_font.render("Player 1 Wins!!", 1, (255, 0, 0))
                        screen.blit(label, (40, 10))
                        game_over = True
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_COUNT))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = my_font.render("Player 2 Wins!!", 1, (255, 255, 0))
                        screen.blit(label, (40, 10))
                        game_over = True
            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
