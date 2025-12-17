from ProprietesMats import *

r_mur_insul = thickness_insul / (k_insul * a_mur)
r_p_mur_insul = thickness_insul / (k_insul * a_p_mur)
r_p_sol_insul = thickness_insul / (k_insul * a_p_sol)

def get_insul_resistance(is_bou:bool):
    return 1/(1/r_p_sol_insul + 2/(r_p_mur_insul) + (1 if is_bou else 0)/r_mur_insul)

R_insuls = [get_insul_resistance(i) for i in isbout_vec]

r_mur_beton = thickness_conc / (k_conc * a_mur)
r_p_mur_beton = thickness_conc / (k_conc * a_p_mur)
r_p_sol_beton = thickness_conc / (k_conc * a_p_sol)

print(r_mur_beton, r_p_mur_beton, r_p_sol_beton)

def get_beton_resistance(is_bou:bool):
    return 1/(1/(r_p_sol_beton) + 2/(r_p_mur_beton) + (1 if is_bou else 0)/r_mur_beton)

R_betons = [get_beton_resistance(i) for i in isbout_vec]

print(R_betons)