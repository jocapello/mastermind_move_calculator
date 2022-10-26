import game
import random
def possible_list(N_COLORS, p):
    p_list = []
    if p > 0:
        for c in range(N_COLORS):
            for comb in possible_list(N_COLORS, p-1):
                p_list.append([c]+comb)
    else:
        p_list.append([])
    return p_list



def elim_poss(poss, guess, w, r, N_COLORS, POSITIONS):
    poss_list = list(poss)
    new_poss = []
    for code in poss_list:
        r2, w2, R2, W2 = game.apply_guess(code, guess, N_COLORS, POSITIONS)
        if (r, w) == (r2, w2):
            new_poss.append(code)
    return set(new_poss)
    
if __name__ == "__main__":
    colors = {0:'red', 1:'green', 2:'blue', 3:'purple', 4:'yellow', 5:'white'}
    N_COLORS = 6
    POSITIONS = 4
    possible = set(map(tuple, possible_list(N_COLORS, POSITIONS)))
    code = [random.randrange(5) for _ in range(POSITIONS)]

    # print(code)


    guess = list(map(int, list(input("Put guess here(eg. 0102): "))))



    while guess != code:
        
        r, w, R, W = game.apply_guess(code, guess, N_COLORS, POSITIONS)
        print("incorrect guess, you got {} red pegs and {} white pegs.\n".format(str(r), str(w)))
        possible = elim_poss(possible, guess, w, r, N_COLORS, POSITIONS)
        print(possible)
        
        guess = list(map(int, list(input("Put guess here(eg. 0102): "))))

    print("guess is correct!")

