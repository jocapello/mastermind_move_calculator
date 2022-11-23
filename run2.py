from nnf import Var, And, Or
from nnf import true, false
#from nnf import dsharp
# Encoding that will store all of your constraints


COLORS = ["red", "green", "blue", "purple", "yellow", "white"]
COLORS_LENGTH = len(COLORS)
CODE_LENGTH = 4

T = Encoding()
#creating new encoding class
class Encoding():
    def __init__(self):
        self.constraints = []

    
    def add_constraint(self, constraint):
        self.constraints.append(constraint)
    def add_constraint_list(self, constraints):
        self.constraints = self.constraints + constraints
    def compile(self):
        return And(self.constraints)
    def solve(self, variables = None):
        return self.constraints.solve()





def iff(A, B):
    return (A|B.negate()) & (B|A.negate())

def init_code(type_of):
    pos_grid = []
    for loc in range(CODE_LENGTH):
        col_grid = []
        for col in COLORS:
            col_grid.append(Var(f'{type_of}_{loc}_{col[0]}'))
        pos_grid.append(col_grid)
    return pos_grid

def init_loc_peg(type_of):
    grid = []
    for loc in range(CODE_LENGTH):
        grid.append(Var(f'{type_of}_{loc}'))
    return grid

def init_peg(type_of):
    grid = []
    for num in range(CODE_LENGTH+1):
        grid.append(Var(f'{type_of}_{num}'))
    return grid


def equiv_label(labels, lst):
    grid = []
    for i in range(len(labels)):
        grid.append(iff(labels[i], lst[i]))
    return grid


def set_code_constraints(grid):
    constraints = []
    
    for loc in grid:
        
        for y, col in enumerate(loc):
            f = true
            for y2, col2 in enumerate(loc):
                if y != y2:
                    f &= col2.negate()
            constraints.append(iff(col, f))
        
    return constraints

def set_num_constraints(grid):
    constraints = []
    
    for n, num in enumerate(grid):
        f = true
        for n2, num2 in enumerate(grid):
            if n != n2:
                f &= num2.negate()
        constraints.append(iff(num, f))
        
    return constraints
    

def set_num_state(num, grid):
    f = true
    
    for n, numc in enumerate(grid):
        if n == num:

        
            f &= numc
        
    return f



def set_code_state(code, grid):
    f = true
    for x, color in enumerate(code):
        for y, col in enumerate(COLORS):
            if color == col:
                f &= grid[x][y]
    return f

def set_peg_state(pegs, grid):
    f = true
    for x, truth in enumerate(pegs):
        grid[x] == truth
    return f


def get_red(C, G):
    grid = []
    for loc in range(CODE_LENGTH):
        f = false
        for col in range(COLORS_LENGTH):
            f |= C[loc][col] & G[loc][col]
        grid.append(f)
    return grid


def get_white(C, G, R):
    grid = []
    for loc in range(CODE_LENGTH):
        f = false
        for col in range(COLORS_LENGTH):
            for loc2 in range(CODE_LENGTH):
                f |= R[loc].negate() & R[loc2].negate() & G[loc][col] & C[loc2][col]
        grid.append(f)
    return grid


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
        
        for higher_num in range(num+1, CODE_LENGTH+1):
            f1 &= lst2[higher_num].negate()
            f2 &= lst1[higher_num].negate()
        grid.append(f1 | f2)
    return grid
def equiv_lists(lst1, lst2):
    f = true
    for num in range(CODE_LENGTH+1):
        f &= iff(lst1[num], lst2[num])
    return f

def equiv_count_lists(lst1, lst2):
    f = false
    for num in range(CODE_LENGTH+1):
        f |= (lst1[num] & lst2[num])
    return f
            
def count_list(lst):
    grid = []
    for num in range(CODE_LENGTH+1):
        grid.append(count_num(lst, num))
    return grid



def list_total(R, W, C, G):
    R_count = count_list(R)
    W_true = [false for i in range(CODE_LENGTH)]
    for col in range(COLORS_LENGTH):
        code_can_be_white = [C[loc][col] & R[loc].negate() for loc in range(CODE_LENGTH)]
        W_this_col = [G[loc][col] & W[loc] for loc in range(CODE_LENGTH)]
        for loc in range(CODE_LENGTH):
            count_can_be_white = count_list(code_can_be_white)
            count_prev_W = count_list(W_this_col[:loc])
            W_true[loc] |= equiv_count_lists(count_prev_W, max_count(count_can_be_white, count_prev_W)).negate() & W_this_col[loc]
    W_count = count_list(W_true)
    return R_count, W_count




#this is the code proposition
C = init_code("C")
T.add_constraint_list(set_code_constraints(C))
#this is the guess proposition
G = init_code("G")
T.add_constraint_list(set_code_constraints(G))

Rl = init_loc_peg("Rl")

Wl = init_loc_peg("Wl")

#number of red pegs
Rn = init_peg("Rn")
T.add_constraint_list(set_num_constraints(Rn))
#number of white pegs
Wn = init_peg("Wn")
T.add_constraint_list(set_num_constraints(Wn))



Rc = get_red(C, G)
T.add_constraint_list(equiv_label(Rl, Rc))
# print(R.__repr__())


Wc = get_white(C, G, Rl)
# print(W.__repr__())



T.add_constraint_list(equiv_label(Wl, Wc))






R_count, W_count = list_total(Rl, Wl, C, G)


R_e = equiv_label(Rn, R_count)
W_e = equiv_label(Wn, W_count)

T.add_constraint_list(R_e)
T.add_constraint_list(W_e)


if __name__ == "__main__":
    code = input("enter colors here: ").split(",")
    T.add_constraint(set_code_state(code, C))

    guess = input("enter guess here: ").split(",")
    T.add_constraint(set_code_state(guess, G))
    # T.add_constraint(set_num_state(int(input("enter num reds here: ")), Rn))
    # T.add_constraint(set_num_state(int(input("enter num whites here: ")), Wn))
    
    T = T.compile()
    #dsharp.compile(T.to_CNF(), smooth=True).model_count()
    print(T.solve())