from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# Encoding that will store all of your constraints
E = Encoding()

COLOURS = ["red", "green", "blue", "purple", "yellow", "white"]
COLOURS_LENGTH = len(COLOURS)
GUESS_LOCATIONS = 4

PEGS = ["red", "white", "blank"]
PEGS_LENGTH = len(PEGS)
PEG_LOCATIONS = 4

PROPOSITIONS = []


class Unique(object):
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return str(self)

    def __str__(self):
        assert False, "You need to define the __str__ function on a proposition class"


# An item must have a location and a colour => it will also be a part of a row
@proposition(E)
class Item(Unique):
    def __init__(self, colour, location):
        self.colour = colour
        self.location = location

    def __str__(self):
        return f"I-{self.location}.{self.colour}"


# A peg must have a location, a colour (could be blank) and be a part of a row
@proposition(E)
class Peg(Unique):
    def __init__(self, colour, location):
        self.colour = colour
        self.location = location

    def __str__(self):
        return f"P-{self.location}.{self.colour}"


# A row must have 4 items in it, and 0-4 pegs
# @proposition(E)
# class Row(Unique):
#     def __init__(self, items: list, pegs: list):
#         self.items = [Item(items[i], i) for i in range(len(items))]
#         self.pegs = [Peg(pegs[i], i) for i in range(len(pegs))]

#     def __str__(self):
#         return f"ROWS-{[it for it in self.items]}"


# A board is defined as having at least 1 row
# @proposition(E)
# class Board(Unique):
#     def __init__(self, rows: list):
#         self.rows = rows

#     def __str__(self):
#         return f"B:{[row for row in self.rows]}"


# Define the 4 locations to be iterated over
# loc1, loc2, loc3, loc4 = 0, 0, 0, 0

# Create all of the possible row colour combinations
# item_colours = []
# for i in range(COLOURS_LENGTH):
#     for j in range(COLOURS_LENGTH):
#         for k in range(COLOURS_LENGTH):
#             for l in range(COLOURS_LENGTH):
#                 item_colours.append(
#                     [COLOURS[loc1], COLOURS[loc2], COLOURS[loc3], COLOURS[loc4]]
#                 )
#                 loc4 += 1
#             loc3 += 1
#             loc4 = 0
#         loc2 += 1
#         loc3 = 0
#     loc1 += 1
#     loc2 = 0


# Define the 4 locations to be iterated over
# loc1, loc2, loc3, loc4 = 0, 0, 0, 0

# Create all of the possible peg combinations
# pegs_colours = []
# for i in range(PEGS_LENGTH):
#     for j in range(PEGS_LENGTH):
#         for k in range(PEGS_LENGTH):
#             for l in range(PEGS_LENGTH):
#                 pegs_colours.append([PEGS[loc1], PEGS[loc2], PEGS[loc3], PEGS[loc4]])
#                 loc4 += 1
#             loc3 += 1
#             loc4 = 0
#         loc2 += 1
#         loc3 = 0
#     loc1 += 1
#     loc2 = 0

# print(pegs_colours)

# Create all of the possible row states by combining the boards and the pegs
# all_rows = []
# for item_row in item_colours:
#     for peg_row in pegs_colours:
#         all_rows.append(Row(item_row, peg_row))

# We define our items, and then a dictionary containing our pegs
A = [
    Item("red", 0),
    Item("green", 1),
    Item("blue", 2),
    Item("orange", 3),
    {"blank": 1, "white": 1, "red": 2},
]

# Constraint to ensure there is 1 location per colour
for location in range(GUESS_LOCATIONS):
    constraint.add_exactly_one(E, [Item(colour, location) for colour in COLOURS])

# Remove the specific guess that we've provided


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarifyw
#  what the expectations are.
def example_theory():
    # our answer can't be the original guess
    E.add_constraint(~(A[0] & A[1] & A[2] & A[3]))
    pegs = A[4]

    if pegs["white"] == 1:
        # we need to ensure there is at least 1 of the colours in the final solution
        colours = [A[item].colour for item in range(len(A) - 1)]
        con = []
        for colour in colours:
            con.append(
                Item(colour, 0) | Item(colour, 1) | Item(colour, 2) | Item(colour, 3)
            )
        E.add_constraint(con[0] | con[1] | con[2] | con[3])

    if pegs["red"] == 1:
        E.add_constraint(A[0] | A[1] | A[2] | A[3])
    elif pegs["red"] == 2:
        x = ""
        for i in range(len(A) - 1):
            for j in range(len(A) - 1):
                x = (A[i] & A[j]) if x == "" else x | (A[i] & A[j])
        # possible = [[x = x | A[i] & A[j] for j in range(len(A) - 1)] for i in range(len(A) - 1)]
        print("possible", x)
        E.add_constraint(x)

    return E


if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v, vn in zip([], "abcxyz"):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
