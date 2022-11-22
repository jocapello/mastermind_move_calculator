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

# print(set_code_state(code, C).__repr__())
# print(set_code_state(guess, G).__repr__())

def get_red(C, G):
    grid = []
    for loc in range(CODE_LENGTH):
        f = false
        for col in range(COLORS_LENGTH):
            f |= C[loc][col] & G[loc][col]
        grid.append(f)
    return grid

R = get_red(C, G)
# print(R.__repr__())
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
# print(W.__repr__())

def count_num(lst, isnum):
    if isnum == 0:
        f = true
        for l in lst:
            f &= l.negate()
        return f
    else:
        f = false
        for i, l in enumerate(lst):
            f |= l & count_num(lst[:i]+lst[i+1:], isnum-1)
        return f
def min_count(lst1, lst2):
    grid = []
    for num in range(CODE_LENGTH+1):
        f1 = lst1[num]
        f2 = lst2[num]
        
        for lower_num in range(num):
            f1 &= lst2[lower_num].negate()
            f2 &= lst1[lower_num].negate()
        grid.append(f1 | f2)
    return grid

def max_count(lst1, lst2):
    grid = []
    for num in range(CODE_LENGTH+1):
        f1 = lst1[num]
        f2 = lst2[num]
        
        for higher_num in range(num, CODE_LENGTH+1):
            f1 &= lst2[higher_num].negate()
            f2 &= lst1[higher_num].negate()
        grid.append(f1 | f2)
    return grid
def equiv_lists(lst1, lst2):
    f = true
    for num in range(CODE_LENGTH+1):
        f &= lst1[num] & lst2[num]
    return f
            
def count_list(lst):
    grid = []
    for num in range(CODE_LENGTH+1):
        grid.append(count_num(lst, num))
    return grid

#for count in count_list(R):
    # print(count.__repr__())

def list_total(R, W, C, G):
    R_count = count_list(R)
    W_true = [false for i in range(CODE_LENGTH)]
    for col in range(COLORS_LENGTH):
        code_can_be_white = [C[loc][col] | (R[loc] & G[loc][col]).negate() for loc in range(CODE_LENGTH)]
        W_this_col = [G[loc][col] | W[loc] for loc in range(CODE_LENGTH)]
        for loc in range(CODE_LENGTH):
            count_can_be_white = count_list(code_can_be_white)
            count_prev_W = count_list(W_this_col[:loc])
            W_true[loc] |= equiv_lists(count_prev_W, max_count(count_can_be_white, count_prev_W)).negate() & W_this_col[loc]
    W_count = count_list(W_true)
    return R_count, W_count

R_count, W_count = list_total(R, W, C, G)

def equiv_label(labels, lst):
    grid = []
    for i in range(len(labels)):
        grid.append((labels[i].negate() & lst[i].negate()) | (labels[i] & lst[i]))
    return grid
R_e = equiv_label(Rg, R_count)
W_e = equiv_label(Wg, W_count)

E.add_constraint(R_e)
E.add_constraint(W_e)

if __name__ == "__main__":
    code = input("enter colors here: ").split(",")
    guess = input("enter guess here: ").split(",")

    E.add_constraint(set_code_state(code, C))

    E.add_constraint(set_code_state(guess, G))

    E = E.compile()

    print(E.solve())