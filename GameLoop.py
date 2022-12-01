from nnf import Var, And, Or
from nnf import true, false
from nnf import dsharp, kissat
from utils import *
from config import *
from run import Game
import random
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
        
        hyp_codes = And(self.game.get_hyp_constraints()).models()
        for codem in hyp_codes:
            yield self.game.filter(codem, return_true_only = True)
        
    def restart(self):
        self.game.wipe_game_state()
        self.set_code_random()
    
    def text_game_loop(self):
        running = True
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
                if rn == 4:
                    print("congradulations, you got the correct guess!")
                else:
                    print(f'incorrect guess, you got {rn} red pegs and {wn} white pegs')
            elif command == "assist":
                for codem in self.get_possible_codes():
                    code = ["n/a" for _ in range(4)]
                    for var in codem:
                        code[int(var[2])] = var[4]
                    print(" ".join(code))
            elif command == "exit":
                running = False
        return self.game
    def text_game_loop_debug(self, inputs):
        running = True
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
                if rn == 4:
                    print("congradulations, you got the correct guess!")
                else:
                    print(f'incorrect guess, you got {rn} red pegs and {wn} white pegs')
            elif command == "assist":
                for codem in self.get_possible_codes():
                    code = ["n/a" for _ in range(4)]
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
            