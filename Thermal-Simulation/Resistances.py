from ProprietesMats import *

r_mur_insul = thickness_insul / (k_insul * (tot_height * tot_width))
r_sixth_wall_insul = thickness_insul / (k_insul * (tot_height * p_len))
r_sixth_floor_insul = thickness_insul / (k_insul * (tot_width * p_len))

def get_insul_resistance(is_bou:bool):
    return 1/(1/r_sixth_floor_insul + 2/(r_sixth_wall_insul) + (1 if is_bou else 0)/r_mur_insul)

R_insuls = [get_insul_resistance(i) for i in isbout_vec]

print(R_insuls)
