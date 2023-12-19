from .constants import GRID_SIZE
from .board import Board
from .piece import Piece
import pygame
import random
import math


class GameAI():
    def __init__(self, screen):
        self.screen = screen
        self.boardObject = Board(self.screen)
        self.board = self.boardObject.board
        self.piece = Piece(self.screen)
        self.currentPiece = self.piece.AI
        self.subArrayLength = 5

    def setCurrentPiece(self, piece):
        self.currentPiece = piece

    def isWinning(self, board):
        return self.boardObject.winning_move(board, self.currentPiece)

    def _checkCapture(self, board):
        self.board = board
        oppentPiece = self.piece.player if self.currentPiece == self.piece.AI else self.piece.AI
        positions = []
        # Check horizontal locations for win
        for col in range(GRID_SIZE - 4):
            for row in range(GRID_SIZE):
                if self.board[row][col] == self.currentPiece and self.board[row][col+1] == oppentPiece and self.board[row][col+2] == oppentPiece and self.board[row][col+3] == self.currentPiece:
                    positions.append([row, col+1])
                    positions.append([row, col+2])

        # Check vertical locations for win
        for col in range(GRID_SIZE):
            for row in range(GRID_SIZE-4):
                if self.board[row][col] == self.currentPiece and self.board[row+1][col] == oppentPiece and self.board[row+2][col] == oppentPiece and self.board[row+3][col] == self.currentPiece:
                    positions.append([row+1, col])
                    positions.append([row+2, col])

        # Check positively sloped diaganols
        for col in range(GRID_SIZE-4):
            for row in range(GRID_SIZE-4):
                if self.board[row][col] == self.currentPiece and self.board[row+1][col+1] == oppentPiece and self.board[row+2][col+2] == oppentPiece and self.board[row+3][col+3] == self.currentPiece:
                    positions.append([row+1, col+1])
                    positions.append([row+2, col+2])

        # Check negatively sloped diaganols
        for col in range(GRID_SIZE-4):
            for row in range(4, GRID_SIZE):
                if self.board[row][col] == self.currentPiece and self.board[row-1][row+1] == oppentPiece and self.board[row-2][col+2] == oppentPiece and self.board[row-3][col+3] == self.currentPiece:
                    positions.append([row-1, col+1])
                    positions.append([row-2, col+2])

        return positions

    def removeCapturedPiece(self, board):
        self.board = board
        positions = self._checkCapture(self.board)
        if (len(positions) > 0):
            for position in positions:
                board[position[0]][position[1]] = 0

    def getValidLocations(self, board):
        validLocations = []
        for i, _ in enumerate(board):
            for j, _ in enumerate(board):
                if board[i][j] == 0:
                    if self.hasAdjacentStone(board, i, j):
                        validLocations.append({"row": i, "col": j})

        return validLocations

    def hasAdjacentStone(self, board, i, j):
        directions = [
            [-1, 0],
            [1, 0],
            [0, 1],
            [0, -1],
            [-1, 1],
            [-1, -1],
            [1, 1],
            [1, -1],
        ]
        for direction in directions:
            newRow = i + direction[0]
            newCol = j + direction[1]

            if newRow >= 0 and newRow < GRID_SIZE and newCol >= 0 and newCol < GRID_SIZE:
                if (board[newRow][newCol] != 0):
                    return True
        return False

    def minimax(self, board, depth, isMaxizingPlayer, alpha, beta):
        if self.isWinning(board):
            return (10000, None) if self.currentPiece == self.piece.AI else (-1000, None)
        elif depth == 0:
            return (self.evaluation(board, self.piece.AI), None)

        if isMaxizingPlayer:
            bestScore = -math.inf
            newState = board.copy()
            validLocations = self.getValidLocations(newState)
            try:
                bestMove = random.choice(validLocations)
            except:
                pass

            for location in validLocations:
                newState[location['row']][location['col']] = int(self.piece.AI)
                self.currentPiece = self.piece.AI
                score = self.minimax(newState, depth-1, False, alpha, beta)[0]
                newState[location['row']][location['col']] = int(0)

                if score > bestScore:
                    bestScore = score
                    bestMove = {"row": location['row'], "col": location['col']}

                alpha = max(alpha, score)
                if (beta <= alpha):
                    break

            return bestScore, bestMove

        else:
            bestScore = math.inf
            newState = board.copy()
            validLocations = self.getValidLocations(newState)
            try:
                bestMove = random.choice(validLocations)
            except:
                pass

            for location in validLocations:
                newState[location['row']][location['col']] = int(
                    self.piece.player)
                self.currentPiece = self.piece.player
                score = self.minimax(newState, depth-1, True, alpha, beta)[0]
                newState[location['row']][location['col']] = int(0)

                if score < bestScore:
                    bestScore = score
                    bestMove = {"row": location['row'], "col": location['col']}
                beta = min(beta, score)
                if beta <= alpha:
                    break

            return bestScore, bestMove

    def evaluateSubArray(self, subArray, piece):
        score = 0
        # print(subArray)
        if subArray.count(piece) == 5:
            score += 1000
        elif subArray.count(piece) == 4 and subArray.count(0) == 1:
            score += 500
        elif self.isCaptured(subArray, piece):
            score += 150
        elif subArray.count(piece) == 3 and subArray.count(0) == 2:
            score += 20

        return score

    def evaluation(self, board, piece):
        oppentPiece = 1
        score = 0

        # Check for horizontal
        for row in range(GRID_SIZE):
            rowArray = [int(i) for i in list(board[row, :])]
            for col in range(GRID_SIZE-4):
                subArray = rowArray[col:col+self.subArrayLength]
                score += self.evaluateSubArray(subArray, piece)
                score -= self.evaluateSubArray(subArray, oppentPiece)

        # Check for vertical
        for col in range(GRID_SIZE):
            colArray = [int(i) for i in list(board[:, col])]
            for row in range(GRID_SIZE-4):
                subArray = colArray[row:row+self.subArrayLength]
                score += self.evaluateSubArray(subArray, piece)
                score -= self.evaluateSubArray(subArray, oppentPiece)

        # Check for Postive Slope Diagonal
        for row in range(GRID_SIZE-4):
            for col in range(GRID_SIZE-4):
                subArray = [board[row+i][col+i]
                            for i in range(self.subArrayLength)]
                score += self.evaluateSubArray(subArray, piece)
                score -= self.evaluateSubArray(subArray, oppentPiece)

        # Check for Negative Slope Diagonal
        for row in range(GRID_SIZE-4):
            for col in range(GRID_SIZE-4):
                subArray = [board[row+4-i][col+i]
                            for i in range(self.subArrayLength)]
                score += self.evaluateSubArray(subArray, piece)
                score -= self.evaluateSubArray(subArray, oppentPiece)

        return score

    def isCaptured(self, subArray, piece):
        oppentPiece = 1
        try:
            i = subArray.index(piece)
        except ValueError:
            return False

        if i + 3 < self.subArrayLength and subArray[i+1] == oppentPiece and subArray[i+2] == oppentPiece and subArray[i+3] == piece:
            return True
        return False

    def bestMove(self, board):
        validLocations = self.getValidLocations(board)
        try:
            bestMove = random.choice(validLocations)
        except:
            pass
        bestScore = 0
        newState = board.copy()
        score = 0

        for location in validLocations:
            newState[location["row"]][location["col"]] = int(self.piece.AI)
            score = self.evaluation(newState, self.piece.AI)
            newState[location["row"]][location["col"]] = 0

            if score > bestScore:
                bestScore = score
                bestMove = {"row": location["row"], "col": location["col"]}

        return bestMove["row"], bestMove["col"]
