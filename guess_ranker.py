import game
import possibility_eliminator
import random

def get_guess_elim(poss, N_COLORS, POSITIONS):
    poss_list = list(poss)
    new_poss_list = {}
    for guess in poss_list:
        new_poss = []
        for code in poss_list:
            r, w, R, W = game.apply_guess(code, guess, N_COLORS, POSITIONS)
            new_poss.append(len(possibility_eliminator.elim_poss(poss, guess, w, r, N_COLORS, POSITIONS)))
        new_poss_list[guess] = (sum(new_poss)/len(poss_list), max(new_poss))


    return new_poss_list
def rank_guesses(guess_stats):
    guesses = list(guess_stats.keys())
    ranked = sorted(guesses, key = lambda g, guess_stats = guess_stats: guess_stats[g][1])
    return ranked

if __name__ == "__main__":
    colors = {0:'red', 1:'green', 2:'blue', 3:'purple', 4:'yellow', 5:'white'}
    N_COLORS = 6
    POSITIONS = 4
    possible = set(map(tuple, possibility_eliminator.possible_list(N_COLORS, POSITIONS)))
    code = [random.randrange(5) for _ in range(POSITIONS)]
    code = [0, 1, 0, 2]
    # print(code)


    guess = list(map(int, list(input("Put guess here(eg. 0102): "))))



    while guess != code:
        
        r, w, R, W = game.apply_guess(code, guess, N_COLORS, POSITIONS)
        print("incorrect guess, you got {} red pegs and {} white pegs.\n".format(str(r), str(w)))
        possible = possibility_eliminator.elim_poss(possible, guess, w, r, N_COLORS, POSITIONS)
        guess_stats = get_guess_elim(possible, N_COLORS, POSITIONS)
        ranked = rank_guesses(guess_stats)
        print(ranked[0])
        print(guess_stats[ranked[0]], guess_stats[ranked[-1]])
        
        guess = list(map(int, list(input("Put guess here(eg. 0102): "))))

    print("guess is correct!")