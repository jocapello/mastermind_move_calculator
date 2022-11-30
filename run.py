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
        self.vars = {}
        for v in self.flatten([self.C, self.G, self.Rl, self.Wl, self.Rn, self.Wn]):
            self.vars[v.__repr__()] = v
        self.hypothetical = []
        
        

    def flatten(self, lsts):
        flat = []
        for lst in lsts:
            if type(lst) != type([]):
                flat.append(lst)
            else:
                flat = flat + self.flatten(lst)
        return flat
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
        self.hypothetical.append([[v.__repr__() for v in self.flatten(self.C)] ,guess_con & peg_con])
        #self.constraints.append(iff(guess_con, peg_con))
    def compile(self):
        self.E.add_constraint(self.rules)
        self.E.add_constraint_list(self.constraints)
        self.T = self.E.compile()
        return self.T
    def filter(self, solution, return_true_only = False, variables = None):
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
    def solve(self, return_true_only = False, variables = None):
        self.T = self.compile()
        solution = self.T.solve()
        return filter(solution, return_true_only = return_true_only, variables = variables)
    def models(self):
        return self.compile().models()
    def model_count(self):
        return self.compile().model_count()

    def model_iter(self, models, names):
        for model in models:
            yield {
                name: value
                for name, value in model.items()
                if name in names
            }
    def hyp_constraints(self):
        new_constraints = []
        T = self.compile()
        

        for hyp in self.hypothetical:
            T_temp = And([T, hyp[1], And(new_constraints)])
            

            names = frozenset(hyp[0])
            models = T_temp.to_CNF().models()
            f = false
            for model in self.model_iter(models, names):
                fa = true
                for name, value in model.items():
                    if value:
                        fa &= self.vars[name]
                    else:
                        fa &= self.vars[name].negate()
                f |= fa
            new_constraints.append(f)
        # T_temp = And([T, And(new_constraints)])
        # names = frozenset(T_temp.vars())
        # models = T_temp.to_CNF().models()
        # return self.model_iter(models, names)
        self.constraints = self.constraints + new_constraints
        return new_constraints
            
        #return self.compile().to_CNF().models()

            
                




# construct game rules




if __name__ == "__main__":
    game = Game()
    print("Available colours are: ", [colour.capitalize() for colour in COLORS], "\n")
    # code = get_code_input("code")
    num_g = int(input("number of past guesses: "))
    for n in range(num_g): 
        guess = get_code_input("guess")
        rn = int(input("enter num reds here: "))
        wn =  int(input("enter num whites here: "))
        # game.set_code(code)
        # game.set_guess(guess)
        game.set_guess_pegs(guess, rn, wn)
    hyp_constraints = game.hyp_constraints()
    models = And(hyp_constraints).models()
    for m in models:
        print(game.filter(m, return_true_only = True))
    #game.set_game_state()
    #print(game.compile().to_CNF())
    
    #dsharp.compile(T.to_CNF(), smooth=True).model_count()
    
    # for m in game.model_hyp():
    #     #print(m)
    #     print(game.filter(m, return_true_only = True))
    #     print(game.filter(m, return_true_only = True, variables=[v.__repr__() for v in game.flatten(game.C)]))
    #print(game.solve())