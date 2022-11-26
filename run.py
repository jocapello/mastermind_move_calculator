from nnf import Var, And, Or
from nnf import true, false
from nnf import dsharp, kissat
from utils import *
from config import *
# Encoding that will store all of your constraints


class Game():
    def __init__(self, code = None, guess = None, num_red = None, num_white = None):
        
        self.C = init_code("C")
        self.G = init_code("G")
        self.Rl = init_loc_peg("Rl")
        self.Wl = init_loc_peg("Wl")
        self.Rn = init_peg("Rn")
        self.Wn = init_peg("Wn")
        self.rules = get_game_constraints(self.C, self.G, self.Rl, self.Wl, self.Rn, self.Wn)
        self.code = code
        self.guess = guess
        self.num_red = num_red
        self.num_white = num_white
        self.constraints = []
        self.E = Encoding()
        self.T = None
        


    def set_code(self, code):
        self.code = code
    def set_guess(self, guess):
        self.guess = guess
    def set_red(self, num_red):
        self.num_red = num_red
    def set_white(self, num_white):
        self.num_white = num_white
    def set_game_state(self):
        if self.code:
            self.constraints.append(set_code_state(self.code, self.C))
        if self.guess:
            self.constraints.append(set_code_state(self.guess, self.G))
        if self.num_red:
            self.constraints.append(set_num_state(self.num_red, self.Rn))
        if self.num_white:
            self.constraints.append(set_num_state(self.num_white, self.Wn))
    def wipe_game_state(self):
        self.constraints = []
        self.set_code(None)
        self.set_guess(None)
        self.set_red(None)
        self.set_white(None)
    def set_guess_pegs(self, guess, nred, nwhite):
        guess_con = set_code_state(guess, self.G)
        peg_con = set_num_state(nred, self.Rn) & set_num_state(nwhite, self.Wn)
        self.constraints.append(iff(guess_con, peg_con))
    def compile(self):
        self.E.add_constraint(self.rules)
        self.E.add_constraint_list(self.constraints)
        self.T = self.E.compile()
        return self.T
    def solve(self, return_true_only = False, variables = None):
        self.T = self.compile()
        solution = self.T.solve()
        if return_true_only:
            truths = []
            for key in solution:
                if solution[key]:
                    if variables:
                        if key in variables:
                            truths.append(key)
                    else:
                        truths.append(key)
            return truths
        else:
            if variables:
                filtered_sol = {}
                for key in solution:
                    if key in variables:
                        filtered_sol[key] = solution[key]
                return filtered_sol
            else:
                return solution
    

            
                




# construct game rules





if __name__ == "__main__":
    game = Game()
    code = input("enter colors here: ").split(",")

    guess = input("enter guess here: ").split(",")
    # int(input("enter num reds here: "))
    # int(input("enter num whites here: "))
    game.set_code(code)
    game.set_guess(guess)
    game.set_game_state()
    
    
    #dsharp.compile(T.to_CNF(), smooth=True).model_count()
    print(game.solve(return_true_only = False))