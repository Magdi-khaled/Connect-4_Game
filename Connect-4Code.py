import numpy as np

NumberOfRows = 6
NumberOfColumns = 7
EMPTY_CELL = 0
COMPUTER_PIECE = 1
AGENT_PIECE = 2
WINDOW_LENGTH = 4

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

board = CreateBoard()
board = [
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,2,0,0,0,0,0],
    [0,1,2,1,0,0,0],
    [0,1,2,2,0,0,0],
    [0,1,1,1,2,1,2]]

print(ScorePos(board,AGENT_PIECE))
print(winMove(board, AGENT_PIECE))
PrintBoard(board)
