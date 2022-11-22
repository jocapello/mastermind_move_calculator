dic = {}









COLORS = ["red", "green", "blue", "purple", "yellow", "white"]
COLORS_LENGTH = len(COLORS)
CODE_LENGTH = 4

def init_code(type_of):
    pos_grid = []
    for loc in range(CODE_LENGTH):
        col_grid = []
        for col in COLORS:
            col_grid.append(f'{type_of}_{loc}_{col[0]}')
        pos_grid.append(col_grid)
    return pos_grid

def init_loc_peg(type_of):
    grid = []
    for loc in range(CODE_LENGTH):
        grid.append(f'{type_of}_{loc}')
    return grid

def init_peg(type_of):
    grid = []
    for num in range(CODE_LENGTH+1):
        grid.append(f'{type_of}_{num}')
    return grid

#this is the code proposition
C = init_code("C")
#this is the guess proposition
G = init_code("G")

Rl = init_loc_peg("Rl")

Wl = init_loc_peg("Wl")

#number of red pegs
Rn = init_peg("Rn")
#number of white pegs
Wn = init_peg("Wn")

for s in C:
    print(s+": "+str(dic[s]))

for s in C:
    print(s+": "+str(dic[s]))

for s in Rl:
    print(s+": "+str(dic[s]))

for s in Wl:
    print(s+": "+str(dic[s]))

for s in Rn:
    print(s+": "+str(dic[s]))

for s in Wn:
    print(s+": "+str(dic[s]))