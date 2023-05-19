import numpy as np
import random
import math
import pygame

NumberOfRows = 6
NumberOfColumns = 7
# GUI Attributes
SQUARE_SIZE = 100
width = NumberOfColumns * SQUARE_SIZE
height = (NumberOfRows + 1) * SQUARE_SIZE
size = (width, height)
RADIUS = int(SQUARE_SIZE / 2 - 5)
screen = pygame.display.set_mode(size)
NumberOfRows = 6
NumberOfColumns = 7
EMPTY_CELL = 0
COMPUTER_PIECE = 1
AGENT_PIECE = 2
WINDOW_LENGTH = 4
# Infinity Vars
PositiveInf = 100000000000000
MinusInf = -100000000000000

# GUI Colours
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)


def CreateBoard():
    board = np.zeros((NumberOfRows, NumberOfColumns))
    return board

def PutPiece(board, row, col, piece):
    board[row][col] = piece

def ValidColumn(board, col):
    return board[NumberOfRows - 1][col] == 0

def Next_Available_Row(board, col):
    for r in range(NumberOfRows):
        if board[r][col] == 0:
            return r

# Print Board History to Console
def PrintBoard(board):
    print(np.flip(board, 0))

# Check if the current play is the winning play
def winMove(board, piece):
    # Check horizontal locations for win
    for c in range(NumberOfColumns - 3):
        for r in range(NumberOfRows):
            if board[r][c] == piece and board[r][c + 1] == piece \
                    and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True
    # Check vertical locations for win
    for c in range(NumberOfColumns):
        for r in range(NumberOfRows - 3):
            if board[r][c] == piece and board[r + 1][c] == piece \
                    and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True
    # Check positively sloped diagonals for win
    for c in range(NumberOfColumns - 3):
        for r in range(NumberOfRows - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece \
                    and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True
    # Check negatively sloped diagonals for win
    for c in range(NumberOfColumns - 3):
        for r in range(3, NumberOfRows):
            if board[r][c] == piece and board[r - 1][c + 1] == piece \
                    and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True
    return False

def evaluate_window(window, piece):
    score = 0
    Turn_Piece = COMPUTER_PIECE
    if piece == COMPUTER_PIECE:
        Turn_Piece = AGENT_PIECE
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY_CELL) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY_CELL) == 2:
        score += 2
    if window.count(Turn_Piece) == 3 and window.count(EMPTY_CELL) == 1:
        score -= 4
    return score

def ScorePos(board, piece):
    score = 0
    # Score center column
    center_array = [int(i) for i in list(board[:, NumberOfColumns // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3
    # Score Horizontal
    for r in range(NumberOfRows):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(NumberOfColumns - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    # Score Vertical
    for c in range(NumberOfColumns):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(NumberOfRows - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    # Score Positive sloped diagonal
    for r in range(NumberOfRows - 3):
        for c in range(NumberOfColumns - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    # Score Negative sloped diagonal
    for r in range(NumberOfRows - 3):
        for c in range(NumberOfColumns - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    return score

def AllValidLocations(board):
    valid_locations = []
    for col in range(NumberOfColumns):
        if ValidColumn(board, col):
            valid_locations.append(col)
    return valid_locations

def IsLastMove(board):
    return winMove(board, COMPUTER_PIECE) or \
        winMove(board, AGENT_PIECE) or len(AllValidLocations(board)) == 0

#   Normal MiniMax Algorithm
def MiniMax(board, depth, maximizingPlayer):
    valid_locations = AllValidLocations(board)
    LastMove = IsLastMove(board)
    if depth == 0 or LastMove:
        if LastMove:
            if winMove(board, AGENT_PIECE):
                return None, PositiveInf
            elif winMove(board, COMPUTER_PIECE):
                return None, MinusInf
            else:  # Game is over, no more valid moves
                return None, 0
        else:  # Depth is zero
            return None, ScorePos(board, AGENT_PIECE)
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = Next_Available_Row(board, col)
            if row is None:
                continue
            board_copy = board.copy()
            PutPiece(board_copy, row, col, AGENT_PIECE)
            new_score = MiniMax(board_copy, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = Next_Available_Row(board, col)
            if row is None:
                continue
            board_copy = board.copy()
            PutPiece(board_copy, row, col, COMPUTER_PIECE)
            new_score = MiniMax(board_copy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value

#   MiniMax Algorithm Using Alpha Beta
def MiniMaxUsingAlphaBeta(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = AllValidLocations(board)
    LastMove = IsLastMove(board)
    if depth == 0 or LastMove:
        if LastMove:
            if winMove(board, AGENT_PIECE):
                return None, PositiveInf
            elif winMove(board, COMPUTER_PIECE):
                return None, MinusInf
            else:  # Game is over, no more valid moves
                return None, 0
        else:  # Depth is zero
            return None, ScorePos(board, AGENT_PIECE)
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = Next_Available_Row(board, col)
            b_copy = board.copy()
            PutPiece(b_copy, row, col, AGENT_PIECE)
            new_score = MiniMaxUsingAlphaBeta(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = Next_Available_Row(board, col)
            b_copy = board.copy()
            PutPiece(b_copy, row, col, COMPUTER_PIECE)
            new_score = MiniMaxUsingAlphaBeta(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def DrawBoard(board):
    for c in range(NumberOfColumns):
        for r in range(NumberOfRows):
            pygame.draw.rect(screen, yellow, (c * SQUARE_SIZE, r * SQUARE_SIZE +
                                              SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, black, (
                int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE +
                                                            SQUARE_SIZE / 2)), RADIUS)
    for c in range(NumberOfColumns):
        for r in range(NumberOfRows):
            if board[r][c] == COMPUTER_PIECE:
                pygame.draw.circle(screen, red, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE +
                                                                         SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == AGENT_PIECE:
                pygame.draw.circle(screen, blue, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE +
                                                                         SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()

board = CreateBoard()
# board = [
#     [0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0],
#     [0,2,0,0,0,0,0],
#     [0,1,2,1,0,0,0],
#     [0,1,2,2,0,0,0],
#     [0,1,1,1,2,1,2]]


col = MiniMaxUsingAlphaBeta(board, 3, -math.inf, math.inf, False)
print(IsLastMove(board))
print(col)
PutPiece(board,0,3,AGENT_PIECE)
PrintBoard(board)
DrawBoard(board)
pygame.time.wait(3000)

# Console Output
# False
# (0, 3)
# [[0. 0. 0. 0. 0. 0. 0.]
#  [0. 0. 0. 0. 0. 0. 0.]
#  [0. 0. 0. 0. 0. 0. 0.]
#  [0. 0. 0. 0. 0. 0. 0.]
#  [0. 0. 0. 0. 0. 0. 0.]
#  [0. 0. 0. 0. 0. 0. 0.]]