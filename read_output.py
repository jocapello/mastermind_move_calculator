dic = {'Wl_0': False, 'Rn_4': True, 'Rn_3': False, 'Rl_0': True, 'Rl_1': True, 'Wn_3': False, 'Wn_4': True, 'Rn_2': False, 'Rl_2': True, 'Rn_1': False, 'Wl_1': False, 'Wl_2': False, 'Wn_1': False, 'Wn_2': False, 'Rl_3': True, 'Rn_0': False, 'G_2_r': False, 'C_2_p': False, 'G_1_b': False, 'G_0_r': True, 'G_1_w': False, 'G_3_y': False, 'C_3_g': False, 'C_1_p': False, 'C_2_y': False, 'G_2_y': False, 'C_2_w': False, 'G_0_y': False, 'C_1_r': False, 'Wn_0': False, 'C_0_p': False, 'Wl_3': False, 'C_0_b': False, 'G_1_p': False, 'G_1_r': False, 'G_3_b': False, 'G_1_g': True, 'C_3_p': False, 'G_2_w': False, 'C_1_g': False, 'C_2_b': False, 'C_0_g': False, 'C_3_w': True, 'G_2_b': True, 'G_3_p': True, 'G_0_g': False, 'C_2_g': True, 'G_0_w': False, 'G_3_g': False, 'C_3_y': False, 'C_3_b': False, 'C_0_r': True, 'C_1_w': False, 'C_0_w': False, 'C_3_r': False, 'G_3_r': False, 'C_1_b': True, 'C_1_y': False, 'G_2_g': False, 'C_0_y': False, 'C_2_r': False, 'G_1_y': False, 'G_0_p': False, 'G_2_p': False, 'G_0_b': False, 'G_3_w': False}









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


print(Rl)
print(Wl)
for s in Rl:
    print(s+": "+str(dic[s]))

for s in Wl:
    print(s+": "+str(dic[s]))

for s in Rn:
    print(s+": "+str(dic[s]))

for s in Wn:
    print(s+": "+str(dic[s]))