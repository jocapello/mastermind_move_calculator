dic = {'Wl_1': True, 'Wl_0': True, 'C_0_y': False, 'C_0_w': False, 'C_1_p': False, 'C_0_g': True, 'C_0_p': False, 'C_0_b': False, 'C_1_r': True, 'C_1_w': False, 'C_1_b': False, 'C_1_y': False, 'C_0_r': False, 'C_1_g': False, 'Rl_1': False, 'Rl_0': False, 'C_2_b': True, 'C_2_g': False, 'Rl_2': True, 'C_2_p': False, 'C_2_w': False, 'C_2_r': False, 'C_2_y': False, 'Wl_2': False, 'C_3_y': False, 'Wl_3': False, 'C_3_p': True, 'C_3_b': False, 'C_3_g': False, 'C_3_w': False, 'Rl_3': True, 'C_3_r': False, 'Wn_1': False, 'G_3_g': False, 'G_0_y': False, 'G_0_g': False, 'G_3_r': False, 'Rn_0': False, 'G_2_r': False, 'Rn_3': False, 'G_1_w': False, 'G_1_g': True, 'G_1_p': False, 'G_1_b': False, 'G_0_r': True, 'G_1_y': False, 'G_1_r': False, 'G_2_w': False, 'G_2_y': False, 'Wn_3': False, 'Wn_0': False, 'G_3_p': True, 'Wn_4': False, 'G_3_b': False, 'Rn_1': False, 'G_3_y': False, 'G_0_p': False, 'G_2_g': False, 'Rn_4': False, 'G_2_p': False, 'Wn_2': True, 'G_0_b': False, 'G_3_w': False, 'Rn_2': True, 'G_2_b': True, 'G_0_w': False}












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


# print(Rl)
# print(Wl)
# for s in Rl:
#     if dic[s]:
#         print(s)

# for s in Wl:
#     if dic[s]:
#         print(s)

# for s in Rn:
#     if dic[s]:
#         print(s)

# for s in Wn:
#     if dic[s]:
#         print(s)

for key in dic:
    if dic[key]:
        print(key)