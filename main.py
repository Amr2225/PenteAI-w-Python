import pygame
import sys
import math
from Pente import WIDTH, HEIGHT, BLACK, BLOCK_SIZE, Board, Piece, GameAI

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pente Board")
myfont = pygame.font.SysFont("monospace", 75)


# Intializing the board
board = Board(screen)

# Initializing the Pieces
piece = Piece(screen)


def main():
    running = True
    turn = 0
    game = GameAI(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the coordinates of the rect and then convert it to the index to play
                row = event.pos[1] // BLOCK_SIZE
                col = event.pos[0] // BLOCK_SIZE

                if turn == 0:  # Player turn
                    # currentPiece =
                    game.setCurrentPiece(piece.player)
                    board.placeStone(row, col, game.currentPiece)
                    game.removeCapturedPiece(board.board)
                    turn = 1  # Changes the turn to the other player

                    if (game.isWinning(board.board)):
                        label = myfont.render(
                            f"Player {game.currentPiece} wins", 5, BLACK)
                        running = False
                        break

            if turn == 1:  # AI turn
                # At the start must change the current player to the AI so that the minimax works properly
                game.setCurrentPiece(piece.AI)

                bestMove = game.minimax(
                    board.board, 2, True, -math.inf, math.inf)[1]
                print(bestMove)

                # difineing the current piece because the minimax changes it
                game.setCurrentPiece(piece.AI)
                print(f"Current Piece: {game.currentPiece}")
                board.placeStone(
                    bestMove["row"], bestMove["col"], game.currentPiece)  # Places the AI Stone

                game.removeCapturedPiece(board.board)
                print(board.board)
                turn = 0

                if (game.isWinning(board.board)):
                    label = myfont.render(
                        f"Player {game.currentPiece} wins", 5, BLACK)
                    running = False
                    break  # if found a winner breaks out of the loop

        board.drawBoard()  # Draws the board
        pygame.display.update()  # Updates the screen

        if not running:
            screen.blit(label, (150, 50))  # Print the label and shows how won
            pygame.display.update()  # Updates the screen
            # Waits a second to let the user see how won
            pygame.time.wait(1000)

    # Quit Pygame
    pygame.quit()
    sys.exit()


# Main game loop
if __name__ == '__main__':
    main()  # starting the game
