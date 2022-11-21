from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from nnf import Var
from nnf import true
# Encoding that will store all of your constraints
E = Encoding()

COLORS = ["red", "green", "blue", "purple", "yellow", "white"]
COLORS_LENGTH = len(COLORS)
CODE_LENGTH = 4




def init_code(type_of):
    pos_grid = []
    for loc in range(CODE_LENGTH):
        col_grid = []
        for col in COLORS:
            col_grid.append(Var(f'{type_of}_{loc}_{col[0]}'))
        pos_grid.append(col_grid)
    return pos_grid

def init_peg(type_of):
    grid = []
    for loc in range(CODE_LENGTH):
        grid.append(Var(f'{type_of}_{loc}'))
    return grid

#this is the code proposition
C = init_code("C")
#this is the guess proposition
G = init_code("G")
#localized red pegs
R = init_peg("R")
#localized white pegs
W = init_peg("W")

code = input("enter colors here: ").split(",")
guess = input("enter guess here: ").split(",")


def set_code_state(code, grid):
    f = true
    for x, color in enumerate(code):
        for y, col in enumerate(COLORS):
            if color == col:
                f &= grid[x][y]
            else:
                f &= ~grid[x][y]
    return f

print(set_code_state(code, C).__repr__())
print(set_code_state(guess, G).__repr__())


