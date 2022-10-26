import random
colors = {1:'red', 2:'blue', 3:'purple', 4:'orange', 5:'white', 6:'green'}

code = []
code = [random.randint(1,6) for i in range(4)]
def c_to_s(code):
    return [colors[i] for i in code]

def check_c(i, c, code):
    #global code
    return code[i] == c

def check(i, code):
    #global code
    return code[i]
# def G(i, c):
#     global guess
#     return guess[i] == c
# print(code)

guess = list(map(int, input("Put guess here: ").split(", ")))
G = [lambda c, guess = guess, i = i: check_c(i, c, guess) for i in range(4)]
C = [lambda c, code = code, i = i: check_c(i, c, code) for i in range(4)]
red_pegs = [False, False, False, False]
white_pegs = [False, False, False, False]
R = red_pegs
W = white_pegs

def list_total(code, guess, R, W):
    r = sum(list(map(int, R)))
    w = 0

    pos = [True for i in range(4)]
    #pos = [False,False,False,False]

    for c in range(1, 7):
        tot_p = sum(list(map(lambda code, c = c: int(code==c), code)))
        tot_p -= sum([int(R[i] and guess[i] == c) for i in range(4)])
        tot_p_temp = tot_p
        
        #print(c, tot_p_temp)
        for i in range(4):
            tot_p_temp -= int(W[i] and guess[i] == c)
            #print(c, int(W[i] and guess[i] == c), i, tot_p_temp, pos)
            if tot_p_temp < 0:
                pos[i] = False
                tot_p_temp = 0
            #print(pos)
        w += min(tot_p, sum([int(W[i] and guess[i] == c) for i in range(4)]))
    return r, w, pos


while guess != code:


    # print(guess)
    red_pegs = [True in [C[t](c) and G[t](c) for c in range(1,7)] for t in range(4)]   
    R = red_pegs
    # print(red_pegs)

    
    white_pegs = [True in [not R[t] and G[t](c) and C[x](c) and not R[x] for x in range(4) for c in range(1, 7)] for t in range(4)]
    W = white_pegs
    # print(white_pegs)
    r, w, cor = list_total(code, guess, R, W)
    # print([W[i] and cor[i] for i in range(4)])
    # print(r, w)
    guess = list(map(int, input("Put guess here: ").split(", ")))
    G = [lambda c, guess = guess, i = i: check_c(i, c, guess) for i in range(4)]
    C = [lambda c, code = code, i = i: check_c(i, c, code) for i in range(4)]
