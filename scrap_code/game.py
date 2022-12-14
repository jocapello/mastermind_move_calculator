import random


def c_to_s(code):
    return [colors[i] for i in code]

def check_c(i, c, code):
    return code[i] == c

def list_total(code, guess, R, W, N_COLORS, POSITIONS):
    r = sum(list(map(int, R)))
    w = 0

    #pos = [True for _ in range(POSITIONS)]


    for c in range(N_COLORS):
        tot_p = sum(list(map(lambda code, c = c: int(code==c), code)))
        tot_p -= sum([int(R[i] and guess[i] == c) for i in range(POSITIONS)])
        # tot_p_temp = tot_p
        
        # #print(c, tot_p_temp)
        # for i in range(POSITIONS):
        #     tot_p_temp -= int(W[i] and guess[i] == c)
        #     #print(c, int(W[i] and guess[i] == c), i, tot_p_temp, pos)
        #     if tot_p_temp < 0:
        #         pos[i] = False
        #         tot_p_temp = 0
        #     #print(pos)
        w += min(tot_p, sum([int(W[i] and guess[i] == c) for i in range(POSITIONS)]))
    return r, w#, pos

def apply_guess(code, guess, N_COLORS, POSITIONS):
    G = [lambda c, guess = guess, i = i: check_c(i, c, guess) for i in range(POSITIONS)]
    C = [lambda c, code = code, i = i: check_c(i, c, code) for i in range(POSITIONS)]
    red_pegs = [True in [C[t](c) and G[t](c) for c in range(N_COLORS)] for t in range(POSITIONS)]   
    R = red_pegs
    # print(red_pegs)

    
    white_pegs = [True in [not R[t] and G[t](c) and C[x](c) and not R[x] for x in range(POSITIONS) for c in range(N_COLORS)] for t in range(POSITIONS)]
    W = white_pegs
    # print(white_pegs)
    r, w = list_total(code, guess, R, W, N_COLORS, POSITIONS)
    # print(r, w, [W[i] and cor[i] for i in range(POSITIONS)])
    return r, w#, R, [W[i] and cor[i] for i in range(POSITIONS)]

if __name__ == "__main__":
    colors = {0:'red', 1:'green', 2:'blue', 3:'purple', 4:'yellow', 5:'white'}
    N_COLORS = 6
    POSITIONS = 4

    code = []
    code = [random.randrange(5) for _ in range(POSITIONS)]

    # print(code)


    guess = list(map(int, list(input("Put guess here(eg. 0102): "))))



    while guess != code:
        
        r, w = apply_guess(code, guess, N_COLORS, POSITIONS)
        print("incorrect guess, you got {} red pegs and {} white pegs.\n".format(str(r), str(w)))
        
        guess = list(map(int, list(input("Put guess here(eg. 0102): "))))

    print("guess is correct!")