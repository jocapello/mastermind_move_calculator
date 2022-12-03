from nnf import Var, And, Or
from nnf import true, false
from nnf import dsharp, kissat
from utils import *
from config import *
import random



# game class that will automatically create all the rule constraints and set game state constraints accordingly
class Game():
    def __init__(self, code = None, guess = None, num_red = None, num_white = None):
        # initialize all atom variables
        self.C = init_code("C")
        self.G = init_code("G")
        self.Rn = init_peg("Rn")
        self.Wn = init_peg("Wn")

        # initialize the rule constraints
        self.rules = get_game_constraints(self.C, self.G, self.Rn, self.Wn)

        # set variables
        self.code = code
        self.guess = guess
        self.num_red = num_red
        self.num_white = num_white
        self.constraints = []
        self.E = Encoding()
        self.T = None
        self.hypothetical = []
        self.hyp_constraints = []

        # creake a dictionary that maps from variable name to variable object
        self.vars = {}
        for v in self.flatten([self.C, self.G, self.Rn, self.Wn]):
            self.vars[v.__repr__()] = v
        
        

    # flattens a list
    def flatten(self, lsts):
        flat = []
        for lst in lsts:
            if type(lst) != type([]):
                flat.append(lst)
            else:
                flat = flat + self.flatten(lst)
        return flat

    # there are self explainatory
    def set_code(self, code):
        self.code = code

    def set_guess(self, guess):
        self.guess = guess

    def set_red(self, num_red):
        self.num_red = num_red

    def set_white(self, num_white):
        self.num_white = num_white

    # retrieves the constraints that correspond to each part of the gamestate if it is known
    def set_game_state(self):
        if self.code:
            self.constraints.append(set_code_state(self.code, self.C))
        if self.guess:
            self.constraints.append(set_code_state(self.guess, self.G))
        if self.num_red:
            self.constraints.append(set_num_state(self.num_red, self.Rn))
        if self.num_white:
            self.constraints.append(set_num_state(self.num_white, self.Wn))

    # wipes the entire game state and resets constraints
    def wipe_game_state(self):
        self.constraints = []
        self.hyp_constraints = []
        self.hypothetical = []
        self.set_code(None)
        self.set_guess(None)
        self.set_red(None)
        self.set_white(None)

    # only wipes guesses, and constraints related to guesses
    def wipe_guess(self):
        self.constraints = []
        self.set_guess(None)
        self.set_red(None)
        self.set_white(None)

    # creates a hypothetical constraint where given some unknown code, the specified guess must return the specified pegs
    def set_guess_pegs(self, guess, nred, nwhite):
        guess_con = set_code_state(guess, self.G)
        peg_con = set_num_state(nred, self.Rn) & set_num_state(nwhite, self.Wn)
        self.hypothetical.append([[v.__repr__() for v in self.flatten(self.C)] ,guess_con & peg_con])

    # compiles game rule constraints and game state constraints into a theory
    def compile(self):
        self.E.add_constraint(self.rules)
        self.E.add_constraint_list(self.constraints)
        self.T = self.E.compile()
        self.E = Encoding()
        return self.T

    # when given a model, filters the model
    # returns a list of dictionary keys corresponding to the value True if return_true_only=true
    # returns only specified dictionary keys if variables are given
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
    
    # solves the theory given by combining all the constraints to return a satasfactory model.
    # in general, this should return the only model that is satasfactory, which contains the previously known truth value of red and white pegs
    def solve(self, return_true_only = False, variables = None):
        self.T = self.compile()
        solution = dsharp.compile(self.T.to_CNF()).solve()
        return self.filter(solution, return_true_only = return_true_only, variables = variables)

    # returns all models that satasfies the constraints of the game, mostly used for debugging
    def models(self):
        return self.compile().models()

    # returns the number of satasfactory models
    def model_count(self):
        return self.compile().model_count()

    # iterates through a list of models and filters each model to only return variables included in the names list
    def model_iter(self, models, names):
        for model in models:
            yield {
                name: value
                for name, value in model.items()
                if name in names
            }

    # adds a list of constraints to the game's existing constraints, mostly for debugging
    def add_constraints(self, constraints):
        self.constraints = self.constraints + constraints

    # loops through hypothetical constraints and creates a theory combining it with the game rules to generate hypothetical models
    # then, based on the variable list included with the hypothetical constraint, generates a new constraint that implies at least one of the models to be true
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



# a class that defines the game loop and all the main functions of a game loop
class GameLoop():
    def __init__(self):
        self.game = Game()
        self.guess_history = []

    # sets a random code
    def set_code_random(self):
        global COLORS, COLORS_LENGTH, CODE_LENGTH
        code = []
        for _ in range(CODE_LENGTH):
            code.append(random.choice(COLORS))
        self.game.set_code(code)
        return code

    # sets a specific code
    def set_code(self, code):
        self.game.wipe_game_state()
        self.game.set_code(code)
        return code

    # a guess is made, the constraints are compiled and solved, then the number of pegs are generated
    # then, the guess/peg combination are saved such that they can be later used to assist the player in generating all possible codes
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

    # gets all the possible codes given the hypothetical constraints representing the information available to the user
    def get_possible_codes(self):
        hyp_codes = And(self.game.get_hyp_constraints()+set_code_constraints(self.game.C)).models()
        for codem in hyp_codes:
            yield self.game.filter(codem, return_true_only = True)
        
    # restarts the game
    def restart(self):
        self.game.wipe_game_state()
        self.set_code_random()
    
    # a game loop utilizing text inputs
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

    # a game loop that runs off of a predefined list of player actions, used for debugging
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
    gl.text_game_loop()
    # gl.text_game_loop_debug(test_input_1)
