from .constants import *
import numpy as np
import pygame
from .piece import Piece


class Board():
    def __init__(self, screen):
        self.board = self.createBoard()
        self.screen = screen
        self.label = None

    def createBoard(self):
        return np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

    def drawBoard(self):
        self.screen.fill(GRID_COLOR)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                pygame.draw.rect(
                    self.screen,
                    BLACK,
                    (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    1,
                )
                if self.board[row][col] == 1:
                    piece = Piece(self.screen)
                    piece.drawPiece(1, row, col)
                elif self.board[row][col] == 2:
                    piece = Piece(self.screen)
                    piece.drawPiece(2, row, col)

    def placeStone(self, row, col, piece):
        if self.board[row][col] == int(0):
            self.board[row][col] = int(piece)
            return True
        return False

    def printBoard(self):
        return self.board

    def winning_move(self, board, piece):
        self.board = board
        # Check horizontal locations for win
        for col in range(GRID_SIZE - 4):
            for row in range(GRID_SIZE):
                if self.board[row][col] == piece and self.board[row][col+1] == piece and self.board[row][col+2] == piece and self.board[row][col+3] == piece and self.board[row][col+4] == piece:
                    return True

        # Check vertical locations for win
        for col in range(GRID_SIZE):
            for row in range(GRID_SIZE-4):
                if self.board[row][col] == piece and self.board[row+1][col] == piece and self.board[row+2][col] == piece and self.board[row+3][col] == piece and self.board[row+4][col] == piece:
                    return True

        # Check positively sloped diaganols
        for col in range(GRID_SIZE-4):
            for row in range(GRID_SIZE-4):
                if self.board[row][col] == piece and self.board[row+1][col+1] == piece and self.board[row+2][col+2] == piece and self.board[row+3][col+3] == piece and self.board[row+4][col+4] == piece:
                    return True

        # Check negatively sloped diaganols
        for col in range(GRID_SIZE-4):
            for row in range(4, GRID_SIZE):
                if self.board[row][col] == piece and self.board[row-1][row+1] == piece and self.board[row-2][col+2] == piece and self.board[row-3][col+3] == piece and self.board[row-4][col+4] == piece:
                    return True

        return False
