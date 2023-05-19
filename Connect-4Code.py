import numpy as np

NumberOfRows = 6
NumberOfColumns = 7
EMPTY_CELL = 0

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


board = CreateBoard()
PrintBoard(board)
