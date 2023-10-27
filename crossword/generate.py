import sys

from crossword import Variable, Crossword
#from crossword.crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # self.domains of type { Variable : set(all words in vocabulary) }
        # Iterate through all variables, and all words that variable can be
        for var in self.domains:
            for word in self.domains[var].copy():
                # If a word is not the same length as the variable's length
                if len(word) != var.length:
                    # Remove it
                    self.domains[var].remove(word)
            
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        # overlap is a tuple for the i'th character of x and y, respectively
        overlap = self.crossword.overlaps[x, y]
        # If the two variables don't overlap, no need to make changes
        if overlap == None:
            return revised
        # For every word in x (copy since we remove values)
        for xWord in self.domains[x].copy():
            satisfactionCheck = False
            # For every word in y
            for yWord in self.domains[y].copy():
                # If there is a possible y-value to satisfy the x-value
                if xWord[overlap[0]] == yWord[overlap[1]]:
                    # We're satisfied
                    satisfactionCheck = True
            # If there's no y-value that has a corresponding x-value
            if satisfactionCheck == False:
                # Remove the word from X and mark that we've changed X's domain
                self.domains[x].remove(xWord)
                revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Initial queue of all arcs in the queue
        queue = []
        if arcs == None:
            for overlap in self.crossword.overlaps.copy():
                if self.crossword.overlaps[overlap] is not None:
                    queue.append(overlap)
        else:
            queue = arcs
        # Until everything in the queue is gone
        while len(queue) > 0:
            # Revise the last arc on the queue and remove it
            arc = queue.pop()
            # If any changes are made
            if self.revise(arc[0], arc[1]):
                # If the first arc has all domain values removed, return false 
                # since there's no possible x value to be consistent with the y value
                if len(self.domains[arc[0]]) == 0:
                    return False
                # For every possible list of neighbors
                for neighborArc in self.crossword.overlaps:
                    # If the neighbor has X, and doesn't have Y, add it
                    if (arc[0] in neighborArc) and (arc[1] not in neighborArc):
                        queue.append(neighborArc)
        return True
        

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Go through every variable in the crossword puzzle 
        for var in self.crossword.variables:
            # If it's not in assignment, return false
            if var not in assignment:
                return False
            # If it doesn't have a value, return false
            if (assignment[var] == None):
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        distinctVals = []
        for var in assignment:
            # Check if value is distinct
            value = assignment[var]
            if value in distinctVals:
                return False
            # If it hasn't been used, it is a distinct value
            distinctVals.append(value)
            # Check if value has the proper amount of characters
            if len(value) != var.length:
                return False
            # For any neighboring variable
            for otherVar in self.crossword.neighbors(var):
                overlap = self.crossword.overlaps[var, otherVar]
                # If overlap is a tuple and the other variable has already been assigned
                if overlap and (otherVar in assignment):
                    # If the overlapping cell values don't match
                    if value[overlap[0]] != assignment[otherVar][overlap[1]]:
                        return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
    
        # A dictionary that maps each value in var to the number of values it removes
        valToScore = {}
        # Neighbors with the variable : overlap tuple
        neighbors = {
            neighbor : self.crossword.overlaps[var, neighbor]
            for neighbor in self.crossword.neighbors(var)
        }
        
        # For each value in the variable
        for value in self.domains[var]:
            # Initialize the value in the list with a score of 0
            valToScore[value] = 0
            # For each neighbor variable in neighbors
            for neighbor in neighbors:
                # Save the overlap, which is the value in neighbors
                overlap = neighbors[neighbor]
                # For each value in the neighboring variable
                for neighboringVal in self.domains[neighbor]:
                    # If the overlap is not the same, they're not compatible, 
                    # and we add 1 to the val to score
                    if value[overlap[0]] != neighboringVal[overlap[1]]:
                        valToScore[value] += 1
        sortedVals = [key for key, value in sorted(valToScore.items(), key=lambda x: x[1])]
        return sortedVals

        
        # Doing without the heuristic for now
        # Return list of values in var's domain
        values = self.domains[var]
        return values
        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # var is a variable mapped to its domain length
        currentVar = None
        domainLength = 9999
        # Get a list of all variables
        variables = self.crossword.variables
        # If the variable isn't already assigned
        for variable in variables:
            otherDomainLength = len(self.domains[variable])
            # If the amount of values the variable has is less than the current smallest
            if (variable not in assignment) and (otherDomainLength < domainLength):
                currentVar = variable
                domainLength = otherDomainLength
            # If the lengths are equal:
            if otherDomainLength == domainLength:
                # If the new variable has more neighbors
                if len(self.crossword.neighbors(currentVar)) < len(self.crossword.neighbors(variable)):
                    currentVar = variable
        return currentVar
                
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # If the assignment is complete, return it
        if self.assignment_complete(assignment):
            return assignment
        # Select an unassigned variable
        var = self.select_unassigned_variable(assignment)
        # For each value in that variable's domain
        for value in self.order_domain_values(var, assignment):
            tempAssignment = assignment
            tempAssignment[var] = value
            # If the new value is consistent:
            if self.consistent(tempAssignment):
                # Add the variable value pair
                assignment[var] = value
                # get the result of backtracking
                result = self.backtrack(assignment=assignment)
                # If this result does not fail, return it
                if result != None:
                    return result
            # If it did fail, remove the variable pair from assignment and try another one (loop back)
            del assignment[var]
        # If no value in any variable satisfies the problem, return failure
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
