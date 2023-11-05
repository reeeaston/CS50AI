import pygame
import sys
import time

from minesweeper import Minesweeper, Sentence
class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        # Sentences are of the class type
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # (1) Cell is marked as one of the moves made in the game
        self.moves_made.add(cell)

        # (2) Mark the cell as a safe cell
        self.mark_safe(cell)

        # (3) Add a new sentence with all undetermined cells and count
        neighboringCells = set()
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Update neighboringCells if cell in bounds and unmarked
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) not in self.moves_made:
                        neighboringCells.add((i, j))
        newSentence = Sentence(neighboringCells, count)
        self.knowledge.append(newSentence)


        # (4) Any sentences that have the safe cell should update
        mineList = set()
        safeList = set()

        # Get a list of mines and safes
        for sentence in self.knowledge:
            if sentence.known_mines() is not None:
                for mine in sentence.known_mines():
                    mineList.add(mine)
            if sentence.known_safes() is not None:
                for safe in sentence.known_safes():
                    safeList.add(safe)
        if mineList != None:
            for mine in mineList:
                self.mark_mine(mine)
        if safeList != None:
            for safe in safeList:
                self.safes.add(safe)
        
        # (5) Iterate through all sentences, copy since we update the existing list
        for sentence in self.knowledge.copy():
            # If the new sentence is a subset of any of the subsets
            if newSentence.cells.issubset(sentence.cells) and (newSentence != sentence):
                # Find the new count and cells
                newCount = sentence.count - newSentence.count
                newCells = sentence.cells.difference(newSentence.cells)
                self.knowledge.append(Sentence(newCells, newCount))
                pass

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Iterate through each sentence in knowledge
        for sentence in self.knowledge:
            # Get a list of safe cells
            safeCells = sentence.known_safes()
            # If the list isn't none
            if safeCells is not None:
                # Return the first cell in the list that isn't a move made
                for cell in safeCells:
                    if cell not in self.moves_made:
                        return cell
        # No safe cell, return none
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # Iterate through all possible cell values
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                # Cell value shouldn't have been moved and shouldn't be a mine
                if (cell not in self.moves_made) and (cell not in self.mines):
                    return cell
                 
        # No possible cell, return none
        return None

HEIGHT = 8
WIDTH = 8
MINES = 8

# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
lost = False

while True:
    move = ai.make_safe_move()
    if move is None:
        move = ai.make_random_move()
        if move is None:
            flags = ai.mines.copy()
            print("No moves left to make.")
        else:
            print("No known safe moves, AI making random move.")
    else:
        print("AI making safe move.")


    if game.is_mine(move):
        lost = True
        break
    else:
        nearby = game.nearby_mines(move)
        revealed.add(move)
        ai.add_knowledge(move, nearby)


