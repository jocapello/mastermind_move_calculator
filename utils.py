from nnf import Var, And, Or
from nnf import true, false
from nnf import dsharp
from config import *
import re
from bauhaus import Encoding as Enc
import nnf


# Utils file, all proposition reating functions are here


# gets the color sequence from the user and makes sure that it is compatible with other functions
def get_code_input(tp):
    
    iswrong = True
    while iswrong:
        iswrong = False
        code = input(f'Enter {tp} here: ').lower()
        pattern = ".*?(\w+)"*CODE_LENGTH + '.*?'
        code = re.match(pattern, code)
        code = [code[i] for i in range(1, CODE_LENGTH+1)]
        for i in range(len(code)):
            if code[i][0] not in [c[0] for c in COLORS]:
                print(f'You have entered an invalid colour at {i+1}, try again')
                iswrong = True
    return code

#creating new encoding class
class Encoding():
    def __init__(self):
        self.constraints = []
        self.theory = None

    
    def add_constraint(self, constraint):
        self.constraints.append(constraint)
    def add_constraint_list(self, constraints):
        self.constraints = self.constraints + constraints
    def compile(self):
        return And(self.constraints)
    def solve(self, variables = None):
        self.theory = self.compile()
        return self.theory.solve()
    # pretty print function migrated from the bauhaus source code
    def pprint(self, formula, solution = None, var_level=False):
        """Pretty print an NNF formula

        Arguments
        ---------
        formula : NNF
            Formula to be displayed.
        solution : dictionary
            Optional; A solution to use to highlight output.
        var_level : boolean
            Defaults to False; If True, output coloring will be based on the
            variable instead of the literal.
        """

        def _process(f):
            if isinstance(f, nnf.Var):
                if solution:
                    if var_level:
                        color = {True: "\u001b[32m", False: "\u001b[31m"}[
                            solution[f.name]
                        ]
                        return (
                            {True: "", False: "¬"}[f.true]
                            + color
                            + str(f.name)
                            + "\u001b[0m"
                        )
                    else:
                        val = solution[f.name]
                        if not f.true:
                            val = not val
                        color = {True: "\u001b[32m", False: "\u001b[31m"}[val]
                        return (
                            color
                            + {True: "", False: "¬"}[f.true]
                            + str(f.name)
                            + "\u001b[0m"
                        )
                else:
                    return {True: "", False: "¬"}[f.true] + str(f.name)
            elif isinstance(f, nnf.And):
                return "(" + " ∧ ".join([_process(i) for i in f]) + ")"
            elif isinstance(f, nnf.Or):
                return "(" + " ∨ ".join([_process(i) for i in f]) + ")"
            else:
                raise TypeError("Can only pprint an NNF object. Given %s" % type(f))

        print(_process(formula))



# simplifies the creation of equivalence relations
def iff(A, B):
    return (A|B.negate()) & (B|A.negate())

# initializes the atoms for either guess or code var
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
            if color[0] == col[0]:
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
            f |= l & count_num(lst[:i], 0) & count_num(lst[i+1:], isnum-1)
        return f


def count_list(lst):
    grid = []
    for num in range(CODE_LENGTH+1):
        grid.append(count_num(lst, num))
    return grid

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

def get_game_constraints(C, G, Rn, Wn):
    T = Encoding()


    #this is the code proposition
    T.add_constraint_list(set_code_constraints(C))
    #this is the guess proposition
    T.add_constraint_list(set_code_constraints(G))



    #number of red pegs

    T.add_constraint_list(set_num_constraints(Rn))
    #number of white pegs

    T.add_constraint_list(set_num_constraints(Wn))



    Rc = get_red(C, G)
    # T.add_constraint_list(equiv_label(Rl, Rc))
    #Rl = Rc
    # print(R.__repr__())


    Wc = get_white(C, G, Rc)
    # print(W.__repr__())



    # T.add_constraint_list(equiv_label(Wl, Wc))
    #Wl = Wc





    R_count, W_count = list_total(Rc, Wc, C, G)


    R_e = equiv_label(Rn, R_count)
    W_e = equiv_label(Wn, W_count)

    T.add_constraint_list(R_e)
    T.add_constraint_list(W_e)

    

    return T.compile()