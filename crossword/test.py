from generate import CrosswordCreator
from crossword import Variable, Crossword

#crossword = Crossword("crossword/data/structure0.txt", "crossword/data/words0.txt")
crossword = Crossword("data/structure1.txt", "data/words1.txt")

creator = CrosswordCreator(crossword=crossword)

"""
print(creator.crossword)
print(creator.domains)
"""

creator.enforce_node_consistency()



varList = []
for variable in creator.domains:
    varList.append(variable)
x = Variable(0, 1, 'down', 5)
y = Variable(0, 1, 'across', 3)

creator.ac3()
# Variable(0, 1, 'down', 5): {'SEVEN'}, Variable(0, 1, 'across', 3): {'TWO', 'TEN', 'SIX'}}

# All variables with one value in their domain remaining, they've been assigned
assignment = {}
for variable in creator.domains:
    if len(creator.domains[variable]) == 1:
        assignment[variable] = creator.domains[variable] 

#print(creator.order_domain_values(varList[0], assignment))
#print(creator.domains)
print(assignment)



print(creator.backtrack(dict()))

print(creator.domains)
                                                                                                                                                            


