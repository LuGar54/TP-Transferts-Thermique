from ProprietesMats import *

_r_mur_insul = thickness_insul / (k_insul * a_mur)
_r_p_mur_insul = thickness_insul / (k_insul * a_p_mur)
_r_p_sol_insul = thickness_insul / (k_insul * a_p_sol)

def get_insul_resistance(is_bou:bool):
    return 1/(1/_r_p_sol_insul + 2/(_r_p_mur_insul) + (1 if is_bou else 0)/_r_mur_insul)

_r_insuls = [get_insul_resistance(i) for i in isbout_vec]

_r_mur_beton = thickness_conc / (k_conc * a_mur)
_r_p_mur_beton = thickness_conc / (k_conc * a_p_mur)
_r_p_sol_beton = thickness_conc / (k_conc * a_p_sol)

def get_beton_resistance(is_bou:bool):
    return 1/(1/(_r_p_sol_beton) + 2/(_r_p_mur_beton) + (1 if is_bou else 0)/_r_mur_beton)

_r_betons = [get_beton_resistance(i) for i in isbout_vec]

_r_conv_f_mur = 1/(h_forcee_murs * a_mur)
_r_conv_f_p_mur = 1/(h_forcee_murs * a_p_mur)
_r_conv_f_sol = 1/(h_forcee_sol * a_p_sol)

_r_convs_forcee = [1/(1/_r_conv_f_sol + 2/(_r_conv_f_p_mur) + (1 if is_bou else 0)/_r_conv_f_mur) for is_bou in isbout_vec]

_r_conv_n_mur = 1/(h_naturelle_murs * a_mur)
_r_conv_n_p_mur = 1/(h_naturelle_murs * a_p_mur)
_r_conv_n_sol = 1/(h_naturelle_sol * a_p_sol)
_r_conv_n_plaf = 1/(h_plafond * a_p_sol)

_r_convs_naturelles = [1/(1/_r_conv_n_sol + 2/(_r_conv_n_p_mur) + (1 if is_bou else 0)/_r_conv_n_mur) for is_bou in isbout_vec]

R_Tbet_Tsol_nat = [_r_convs_naturelles[i] + _r_betons[i] + _r_insuls[i] for i in range(len(isbout_vec))]

R_Tbet_Tsol_force = [_r_convs_forcee[i] + _r_betons[i] + _r_insuls[i] for i in range(len(isbout_vec))]

R_plafond_ext = _r_conv_n_plaf + thickness_acier/(k_acier*a_p_sol) + thickness_asphalte/(a_p_sol*k_asphalte) + 1/(h_exterieure_sol * a_p_sol)