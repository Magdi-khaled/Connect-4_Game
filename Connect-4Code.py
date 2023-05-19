import numpy as np
import random
import pygame
import math
import tkinter as tk

NumberOfRows = 6
NumberOfColumns = 7
COMPUTER = 0
AGENT = 1
EMPTY_CELL = 0
COMPUTER_PIECE = 1
AGENT_PIECE = 2
WINDOW_LENGTH = 4
# Infinity Vars
PositiveInf = 100000000000000
MinusInf = -100000000000000
Difficulty = 0
AlgorithmChoice = 0
MiniMaxNormal = 1
MiniMaxAlphaBeta = 2
# GUI Attributes
SQUARE_SIZE = 100
width = NumberOfColumns * SQUARE_SIZE
height = (NumberOfRows + 1) * SQUARE_SIZE
size = (width, height)
RADIUS = int(SQUARE_SIZE / 2 - 5)
screen = pygame.display.set_mode(size)
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
# Score Position for each player
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

def AllValidLocations(board):
    valid_locations = []
    for col in range(NumberOfColumns):
        if ValidColumn(board, col):
            valid_locations.append(col)
    return valid_locations

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

def Input_Gui_Level(AlgorithmType):
    def EasyLevelBoth():
        global Difficulty
        input_text = 1
        Difficulty = int(input_text)
        root.destroy()

    def NormalLevelMiniMax():
        global Difficulty
        input_text = 3
        Difficulty = int(input_text)
        root.destroy()

    def HardLevelMiniMax():
        global Difficulty
        input_text = 5
        Difficulty = int(input_text)
        root.destroy()

    def NormalLevelAlphaBeta():
        global Difficulty
        input_text = 4
        Difficulty = int(input_text)
        root.destroy()

    def HardLevelAlphaBeta():
        global Difficulty
        input_text = 6
        Difficulty = int(input_text)
        root.destroy()

    root = tk.Tk()
    root.title("Connect-4 Game")
    root.geometry("450x250")
    button_font = ('Arial', 12, 'bold')
    label = tk.Label(root, text="Select Your Level",
                     font=button_font, padx=10, pady=10)
    label.pack()
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)
    frame.config(bg="black")
    root.configure(bg='black')
    # Create the buttons and add them to the frame
    button1 = tk.Button(frame, text='Easy', width=15, fg='black',
                        font=button_font, command=EasyLevelBoth)
    button1.pack(side=tk.TOP, padx=5, pady=5)
    if AlgorithmType == 1:
        button2 = tk.Button(frame, text='Normal', width=15, fg='blue',
                            font=button_font, command=NormalLevelMiniMax)
        button2.pack(side=tk.TOP, padx=5, pady=5)
        button3 = tk.Button(frame, text='Hard', width=15, fg='red',
                            font=button_font, command=HardLevelMiniMax)
        button3.pack(side=tk.TOP, padx=5, pady=5)
    else:
        button2 = tk.Button(frame, text='Normal', width=15, fg='blue',
                            font=button_font, command=NormalLevelAlphaBeta)
        button2.pack(side=tk.TOP, padx=5, pady=5)
        button3 = tk.Button(frame, text='Hard', width=15, fg='red',
                            font=button_font, command=HardLevelAlphaBeta)
        button3.pack(side=tk.TOP, padx=5, pady=5)
    # Calculate the x and y positions to center the window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_pos = int(screen_width / 2 - 250)
    y_pos = int(screen_height / 2 - 125)
    # Set the geometry of the window to center it on the screen
    root.geometry("450x250+{}+{}".format(x_pos, y_pos))
    # Start the main event loop
    root.mainloop()

def Input_Gui_Algorithm():
    def MiniMaxAlgorithm():
        global MiniMaxNormal, AlgorithmChoice
        input_text = MiniMaxNormal
        AlgorithmChoice = int(input_text)
        root.destroy()

    def MiniMaxUsingAlphaBetaAlgorithm():
        global MiniMaxAlphaBeta, AlgorithmChoice
        input_text = MiniMaxAlphaBeta
        AlgorithmChoice = int(input_text)
        root.destroy()
    # Create the GUI window
    root = tk.Tk()
    root.title("Connect-4 Game")
    root.geometry("450x250")
    button_font = ('Arial', 12, 'bold')
    label = tk.Label(root, text="Select Algorithm Type",
                     font=button_font, padx=10, pady=10)
    label.pack()
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)
    frame.config(bg="black")
    root.configure(bg='black')
    # Create the buttons and add them to the frame
    button1 = tk.Button(frame, text='Mini Max', width=20, fg='red',
                        font=button_font, command=MiniMaxAlgorithm)
    button1.pack(side=tk.TOP, padx=10,pady=10)
    button2 = tk.Button(frame, text='Alpha Beta Prunning', width=20, fg='blue',
                        font=button_font, command=MiniMaxUsingAlphaBetaAlgorithm)
    button2.pack(side=tk.TOP, padx=10,pady=10)
    # Calculate the x and y positions to center the window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_pos = int(screen_width / 2 - 250)
    y_pos = int(screen_height / 2 - 125)
    # Set the geometry of the window to center it on the screen
    root.geometry("450x250+{}+{}".format(x_pos, y_pos))
    root.mainloop()

def PlayGameMiniMax():
    board = CreateBoard()
    PrintBoard(board)
    game_over = False
    Draw = True
    pygame.init()
    DrawBoard(board)
    pygame.display.update()
    pygame.display.set_caption("Connect-4 Game")
    myfont = pygame.font.SysFont("monospace", 75)
    turn = random.randint(COMPUTER, AGENT)
    while not game_over:
        # AGENT TURN
        if turn == AGENT and not game_over:
            col, minimax_score = MiniMax(board, Difficulty, True)
            if ValidColumn(board, col):
                pygame.time.wait(200)
                row = Next_Available_Row(board, col)
                PutPiece(board, row, col, AGENT_PIECE)
                if winMove(board, AGENT_PIECE):
                    label = myfont.render("Agent wins!!", 1, yellow)
                    print("Agent wins!!\n")
                    screen.blit(label, (40, 10))
                    game_over = True
                    Draw = False
                turn = 0
                PrintBoard(board)
                DrawBoard(board)
        # COMPUTER TRUN
        elif turn == COMPUTER and not game_over:
            col, minimax_score = MiniMax(board, Difficulty, True)
            if ValidColumn(board, col):
                pygame.time.wait(200)
                row = Next_Available_Row(board, col)
                PutPiece(board, row, col, COMPUTER_PIECE)
                if winMove(board, COMPUTER_PIECE):
                    label = myfont.render("Computer wins!!", 1, red)
                    print("Computer wins!!\n")
                    screen.blit(label, (40, 10))
                    game_over = True
                    Draw = False
                turn = 1
                PrintBoard(board)
                DrawBoard(board)
        # Check if the game is over close the screen after 3 seconds
        if game_over and not Draw:
            pygame.time.wait(3000)

def PlayGameAlphaBetaPrunning():
    board = CreateBoard()
    PrintBoard(board)
    game_over = False
    Draw = True
    pygame.init()
    DrawBoard(board)
    pygame.display.update()
    pygame.display.set_caption("Connect-4 Game")
    myfont = pygame.font.SysFont("monospace", 75)
    turn = random.randint(COMPUTER, AGENT)
    while not game_over:
        # AGENT TURN
        if turn == AGENT and not game_over:
            col, minimax_score = MiniMaxUsingAlphaBeta(board, Difficulty,
                                                       -math.inf, math.inf, True)
            if ValidColumn(board, col):
                pygame.time.wait(200)
                row = Next_Available_Row(board, col)
                PutPiece(board, row, col, AGENT_PIECE)
                if winMove(board, AGENT_PIECE):
                    label = myfont.render("Agent wins!!", 1, yellow)
                    print("Agent wins!!\n")
                    screen.blit(label, (40, 10))
                    game_over = True
                    Draw = False
                turn = 0
                PrintBoard(board)
                DrawBoard(board)
        # COMPUTER TRUN
        elif turn == COMPUTER and not game_over:
            col, minimax_score = MiniMaxUsingAlphaBeta(board, Difficulty,
                                                       -math.inf, math.inf, True)
            if ValidColumn(board, col):
                pygame.time.wait(200)
                row = Next_Available_Row(board, col)
                PutPiece(board, row, col, COMPUTER_PIECE)
                if winMove(board, COMPUTER_PIECE):
                    label = myfont.render("Computer wins!!", 1, red)
                    print("Computer wins!!\n")
                    screen.blit(label, (40, 10))
                    game_over = True
                    Draw = False
                turn = 1
                PrintBoard(board)
                DrawBoard(board)
        # Check if the game is over close the screen after 3 seconds
        if game_over and not Draw:
            pygame.time.wait(6000)

def PrintConsole(diff, algorithmChoice):
    if diff == 1:
        print("Difficulty : Easy")
    elif diff == 2:
        print("Difficulty : Normal")
    elif diff == 3:
        print("Difficulty : Hard")
    if algorithmChoice == 1:
        print("AlgorithmChoice : MiniMax Algorithm")
    elif algorithmChoice == 2:
        print("AlgorithmChoice : MiniMax Alpha Beta")

#  ------------------------- Main -------------------------
PrintConsole(Difficulty, AlgorithmChoice)
Input_Gui_Algorithm()
Input_Gui_Level(AlgorithmChoice)
# Play The Game by MiniMax Algorithm
if AlgorithmChoice == 1:
    PlayGameMiniMax()
# Play The Game by MiniMax Algorithm Refined by Alpha Beta Prunning Algorithm
elif AlgorithmChoice == 2:
    PlayGameAlphaBetaPrunning()
