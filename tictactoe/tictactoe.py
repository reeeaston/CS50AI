"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count number of X's and O's
    x = 0
    o = 0
    for row in board:
        for item in row:
            if item == "X":
                x += 1
            elif item == "O":
                o += 1
    # If X and O is 9, it's no player's turn
    if x + o == 9:
        return None
    # If X and O are equal, it's X's turn
    if x == o:
        return "X"
    # Else, it's O's turn
    else:
        return "O"

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Define a list of actions
    actions = set()
    # For every square, return (row, cell) if it's empty
    
    for row_index, row in enumerate(board):
        for col_index, cell in enumerate(row):
            if cell == EMPTY:
                actions.add((row_index, col_index))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Copy board
    new_board = copy.deepcopy(board)
    # If the action is invalid, raise an exception
    validActions = actions(board)
    if action not in validActions:
        raise Exception("Invalid action")
    # Return the new board (determine player based on current board)
    else:
        new_board[action[0]][action[1]] = player(board)
        return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and (row[0] is not EMPTY):
            return row[0]
    # Check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and (board[0][i] is not EMPTY):
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and (board[0][0] is not EMPTY):
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and (board[0][2] is not EMPTY):
        return board[0][2]
    return EMPTY

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If there is a winner, the game is over
    if winner(board) != EMPTY:
        return True
    # If any squares aren't filled, the game isn't over
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Check state of winner(board)
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Determine if we're X or O
    currentPlayer = player(board)
    print("Playing as " + currentPlayer)
    # If AI is playing as X
    if currentPlayer == "X":
        # Get all possible actions
        currentScore = -2
        currentAction = ()
        actionList = actions(board)
        # For each action, generate the new state
        for action in actionList:
            # Find the min value generated by that state
            value = minValue(result(board, action), currentScore)
            # Else, if it's higher than the current, make it the new action
            if value == 1:
                return action
            if value > currentScore:
                currentScore = value
                currentAction = action
        return currentAction
    else:
        # Get all possible actions
        actionList = actions(board)
        currentScore = 2
        currentAction = ()
        # For each action, generate the new state
        for action in actionList:
        # Find the max value generated by that state
            value = maxValue(result(board, action), currentScore)
        # Else, if it's lower than the current, make it the new action and change score
            if value == -1:
                return action
            if value < currentScore:
                currentScore = value
                currentAction = action
        return currentAction
    
def maxValue(board, lowest):
   # If the game is over, return the value of the winner
   if terminal(board):
       return utility(board)
   v = -2
   # For each possible action, V is the maximum of what V currently is and the 
   # minimum of the result of that action
   actionList = actions(board)
   for action in actionList:
       v = max(v, minValue(result(board, action), v))
       # If this set doesn't have the potential to be lower than what we already
       # have, I don't even wanna calculate the rest.
       if v > lowest:
           return 0
       # Already reached the best move 
       if v == 1:
        return v
   return v    

def minValue(board, highest):
   # If the game is over, return the value of the winner
   if terminal(board):
       return utility(board)
   v = 2
   # For each possible action, V is the minimum of what V currently is and the 
   # maximum of the result of that action
   actionList = actions(board)
   for action in actionList:
       v = min(v, maxValue(result(board, action), v))
       # If this set doesn't have the potential to be higher than what we already
       # have, I don't even wanna calculate the rest.
       if v < highest:
           return 0
       # Already reached the best move 
       if v == -1:
        return v
   return v
