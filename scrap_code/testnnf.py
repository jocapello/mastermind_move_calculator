from nnf import Var, And, Or
from nnf import true, false
from nnf import dsharp, kissat
from utils import *
from config import *
#from prettyprint import prettyprint as pprint
from run import *

game = Game()
game.set_code(['red', 'blue', 'green', 'green'])
game.set_guess(['red', 'green', 'white', 'blue'])
game.set_game_state()

def simp(thing):
    return thing.simplify()

print(list(map(simp, game.constraints)))
print(list(map(simp, set_code_constraints(game.C))))
print(list(map(simp, set_code_constraints(game.G))))
#print(get_red(game.C, game.G))
print(list(map(simp, equiv_label(game.Rl, get_red(game.C, game.G)))))