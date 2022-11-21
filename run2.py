from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from nnf import Var
from nnf import true, false
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
    for num in range(CODE_LENGTH+1):
        grid.append(Var(f'{type_of}_{num}'))
    return grid

#this is the code proposition
C = init_code("C")
#this is the guess proposition
G = init_code("G")
#number of red pegs
Rg = init_peg("R")
#number of white pegs
Wg = init_peg("W")

code = input("enter colors here: ").split(",")
guess = input("enter guess here: ").split(",")


def set_code_state(code, grid):
    f = true
    for x, color in enumerate(code):
        for y, col in enumerate(COLORS):
            if color == col:
                f &= grid[x][y]
            else:
                f &= grid[x][y].negate()
    return f

def set_peg_state(pegs, grid):
    f = true
    for x, truth in enumerate(pegs):
        grid[x] == truth
    return f

print(set_code_state(code, C).__repr__())
print(set_code_state(guess, G).__repr__())

def get_red(C, G):
    grid = []
    for loc in range(CODE_LENGTH):
        f = false
        for col in range(COLORS_LENGTH):
            f |= C[loc][col] & G[loc][col]
        grid.append(f)
    return grid

R = get_red(C, G)
print(R.__repr__())
def get_white(C, G):
    grid = []
    for loc in range(CODE_LENGTH):
        f = false
        for col in range(COLORS_LENGTH):
            for loc2 in range(CODE_LENGTH):
                f |= R[loc].negate() & R[loc2].negate() & G[loc][col] & C[loc2][col]
        grid.append(f)
    return grid

W = get_white(C, G)
for i, w in enumerate(W):
    print(i, w.__repr__())

def count_list(lst, isnum):
    if isnum == 0:
        f = true
        for l in lst:
            f &= l.negate()
        return f
    else:
        f = false
        for i, l in enumerate(lst):
            f |= l & count_list(lst[:i]+lst[i+1:], isnum-1)
        return f
            
def count_red(R):
    grid = []
    for num in range(CODE_LENGTH+1):
        grid.append(count_list(R, num))
    return grid

for i, count in enumerate(count_red(R)):
    print(i, count.__repr__())

def list_total(R, C, G):
    R_count = count_red(R)
    W_true = []
    for col in range(COLORS_LENGTH):
        code_is_col = [loc[col] for loc in C]
        loc_col_is_red = [R[loc] & G[loc][col] for loc in range(CODE_LENGTH)]
