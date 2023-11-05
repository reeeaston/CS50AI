import tictactoe as t

EMPTY = None
board1 = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
board = [[EMPTY, "O", EMPTY],
            [EMPTY, "X", "X"],
            ["O", "X", "O"]]

# Get all possible actions
currentScore = -2
currentAction = ()
actionList = t.actions(board)
