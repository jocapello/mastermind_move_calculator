from nnf import Var, And, Or
from nnf import true, false
from nnf import dsharp, kissat
from utils import *
from config import *
import random
# Encoding that will store all of your constraints


class Game():
    def __init__(self, code = None, guess = None, num_red = None, num_white = None):
        
        self.C = init_code("C")
        self.G = init_code("G")
        self.Rn = init_peg("Rn")
        self.Wn = init_peg("Wn")
        self.rules = get_game_constraints(self.C, self.G, self.Rn, self.Wn)
        self.code = code
        self.guess = guess
        self.num_red = num_red
        self.num_white = num_white
        self.constraints = []
        self.E = Encoding()
        self.T = None
        self.vars = {}
        for v in self.flatten([self.C, self.G, self.Rn, self.Wn]):
            self.vars[v.__repr__()] = v
        self.hypothetical = []
        self.hyp_constraints = []
        
        


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
        self.hyp_constraints = []
        self.hypothetical = []
        self.set_code(None)
        self.set_guess(None)
        self.set_red(None)
        self.set_white(None)
    def wipe_guess(self):
        self.constraints = []
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
        self.E = Encoding()
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
        return self.filter(solution, return_true_only = return_true_only, variables = variables)
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

    def add_constraints(self, constraints):
        self.constraints = self.constraints + constraints
    def get_hyp_constraints(self):
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
                    # else:
                    #     fa &= self.vars[name].negate()
                f |= fa
            new_constraints.append(f)
        # T_temp = And([T, And(new_constraints)])
        # names = frozenset(T_temp.vars())
        # models = T_temp.to_CNF().models()
        # return self.model_iter(models, names)
        self.hyp_constraints = new_constraints
        return new_constraints
            
        #return self.compile().to_CNF().models()

            
                




# construct game rules




class GameLoop():
    def __init__(self):
        self.game = Game()
        self.guess_history = []
    def set_code_random(self):
        global COLORS, COLORS_LENGTH, CODE_LENGTH
        code = []
        for _ in range(CODE_LENGTH):
            code.append(random.choice(COLORS))
        self.game.set_code(code)
        return code

    def set_code(self, code):
        self.game.wipe_game_state()
        self.game.set_code(code)
        return code

    def make_guess(self, guess):
        self.game.set_guess(guess)
        self.game.set_game_state()
        results = self.game.solve(return_true_only=True, variables = [v.__repr__() for v in self.game.flatten([self.game.Rn, self.game.Wn])])
        
        for result in results:
            if result[0:2] == "Rn":
                rn = int(result[3])
            if result[0:2] == "Wn":
                wn = int(result[3])
        self.guess_history.append([guess, rn, wn])
        self.game.set_guess_pegs(guess, rn, wn)
        self.game.wipe_guess()
        return rn, wn

    def get_possible_codes(self):
        
        hyp_codes = And(self.game.get_hyp_constraints()+set_code_constraints(self.game.C)).models()
        for codem in hyp_codes:
            yield self.game.filter(codem, return_true_only = True)
        
    def restart(self):
        self.game.wipe_game_state()
        self.set_code_random()
    
    def text_game_loop(self):
        running = True
        self.restart()
        this_code = self.set_code_random()

        while running:
            command = input("choose your next action(restart/setcode/getcode/makeguess/assist/exit): ").lower()
            if command == "restart":
                self.restart()
            elif command == "setcode":
                this_code = self.set_code(get_code_input("code"))
            elif command == "getcode":
                print(" ".join(this_code))
            elif command == "makeguess":
                rn, wn = self.make_guess(get_code_input("guess"))
                if rn == CODE_LENGTH:
                    print("congradulations, you got the correct guess!")
                else:
                    print(f'incorrect guess, you got {rn} red pegs and {wn} white pegs')
            elif command == "assist":
                for codem in self.get_possible_codes():
                    code = ["n/a" for _ in range(CODE_LENGTH)]
                    for var in codem:
                        code[int(var[2])] = var[4]
                    print(" ".join(code))
            elif command == "exit":
                running = False
        return self.game
    def text_game_loop_debug(self, inputs):
        running = True
        self.restart()
        this_code = self.set_code_random()
        n = 0
        while running:
            command = inputs[n][0].lower()
            print(command)
            if command == "restart":
                self.restart()
            elif command == "setcode":
                print(", ".join(inputs[n][1]))
                this_code = self.set_code(inputs[n][1])
            elif command == "getcode":
                print(" ".join(this_code))
            elif command == "makeguess":
                print(", ".join(inputs[n][1]))
                rn, wn = self.make_guess(inputs[n][1])
                if rn == CODE_LENGTH:
                    print("congradulations, you got the correct guess!")
                else:
                    print(f'incorrect guess, you got {rn} red pegs and {wn} white pegs')
            elif command == "assist":
                for codem in self.get_possible_codes():
                    code = ["n/a" for _ in range(CODE_LENGTH)]
                    for var in codem:
                        code[int(var[2])] = var[4]
                    print(" ".join(code))
            elif command == "exit":
                running = False
            n += 1
        return self.game


test_input_1 = [
    ["getcode"],
    ["makeguess", ['r', 'r', 'g', 'g']],
    ["makeguess", ['b', 'b', 'p', 'p']],
    ["makeguess", ['y', 'y', 'w', 'w']],
    ["assist"],
    ["exit"]
]


if __name__ == "__main__":
    gl = GameLoop()
    gl.text_game_loop_debug(test_input_1)
    gl.text_game_loop_debug(test_input_1)
    gl.text_game_loop_debug(test_input_1)