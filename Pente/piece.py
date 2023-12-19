import pygame
from . import BLACK, WHITE, BLOCK_SIZE


class Piece():
    PADDING = 5

    def __init__(self, screen):
        self.AI = 2
        self.player = 1
        self.screen = screen

    def drawPiece(self, piece, row, col):
        color = BLACK if piece == self.AI else WHITE
        radius = BLOCK_SIZE // 2 - self.PADDING
        pygame.draw.circle(
            self.screen,
            color,
            (col * BLOCK_SIZE + BLOCK_SIZE // 2,
             row * BLOCK_SIZE + BLOCK_SIZE // 2),
            radius)
