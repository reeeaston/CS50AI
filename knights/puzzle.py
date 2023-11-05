from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    # Either a knight or a knave, not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # A is a knight if his sentence is true
    Implication(AKnight, And(AKnight, AKnave)),
    # A is a knave if his sentence is false
    Implication(AKnave, Not(And(AKnight, AKnave))),   
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    # Either a knight or a knave, not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # If they are both knaves, A is a knight
    Implication(AKnight, And(AKnave, BKnave)),
    # If they are both knave, A is a knave
    Implication(AKnave, Not(And(AKnave, BKnave))),   
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    # Either an knight or a knave, not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # A is a knight if they are both knights or both knaves
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # B is a knight if one is a knight and the other is a knave
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight)))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    # Either an knight or a knave, not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    # A being a knight implies he's a knight or a knave
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),

    # B being a knight implies A said he's a knave, vice versa
    Implication(BKnight, Implication(AKnight, AKnave)),
    Implication(BKnave, Not(Implication(AKnight, AKnave))),

    # B being a knight implies C is a knave, vice versa
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    # C being a knight implies A is a knight, vice versa
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
