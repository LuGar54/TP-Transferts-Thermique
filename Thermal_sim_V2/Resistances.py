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

def get_beton_resistance(is_bou:bool):
    return 1/(1/(r_p_sol_beton) + 2/(r_p_mur_beton) + (1 if is_bou else 0)/r_mur_beton)

R_betons = [get_beton_resistance(i) for i in isbout_vec]

h_forcee_murs = 8.33  # W/m2K
h_forcee_sol = 6.25    # W/m2K

h_naturelle_murs = 2.6  # W/m2K
h_naturelle_sol = 3.7   # W/m2K
h_exterieure_sol = 30  # W/m2K
h_plafond = 5         # W/m2K

R_conv_f_mur = 1/(h_forcee_murs * a_mur)
R_conv_f_p_mur = 1/(h_forcee_murs * a_p_mur)
R_conv_f_sol = 1/(h_forcee_sol * a_p_sol)

R_convs_forcee = [1/(1/R_conv_f_sol + 2/(R_conv_f_p_mur) + (1 if is_bou else 0)/R_conv_f_mur) for is_bou in isbout_vec]

R_conv_n_mur = 1/(h_naturelle_murs * a_mur)
R_conv_n_p_mur = 1/(h_naturelle_murs * a_p_mur)
R_conv_n_sol = 1/(h_naturelle_sol * a_p_sol)
R_conv_n_plaf = 1/(h_plafond * a_p_sol)

R_convs_naturelles = [1/(1/R_conv_n_sol + 2/(R_conv_n_p_mur) + (1 if is_bou else 0)/R_conv_n_mur) for is_bou in isbout_vec]

R_Tbet_Tsol_nat = [R_convs_naturelles[i] + R_betons[i] + R_insuls[i] for i in range(len(isbout_vec))]

R_Tbet_Tsol_force = [R_convs_forcee[i] + R_betons[i] + R_insuls[i] for i in range(len(isbout_vec))]

#R_plafond_ext = (1/(1/R_conv_n_sol + k_acier/(a_p_sol*thickness_acier) + k_asphalte/(a_p_sol*thickness_asphalte) + 1/(h_exterieure_sol * a_p_sol)))
R_plafond_ext = R_conv_n_plaf + thickness_acier/(k_acier*a_p_sol) + thickness_asphalte/(a_p_sol*k_asphalte) + 1/(h_exterieure_sol * a_p_sol)

R_12_on = 1/(m_a12_on*cp_air)
R_21_on = 1/(m_a21_on*cp_air)
R_23_on = 1/(m_a23_on*cp_air)
R_32_on = 1/(m_a32_on*cp_air)
R_34_on = 1/(m_a34_on*cp_air)
R_43_on = 1/(m_a43_on*cp_air)
R_45_on = 1/(m_a45_on*cp_air)
R_54_on = 1/(m_a54_on*cp_air)
R_56_on = 1/(m_a56_on*cp_air)
R_65_on = 1/(m_a65_on*cp_air)

R_to_cell_on = [R_12_on, R_23_on, R_34_on, R_45_on, R_65_on]
R_from_cell_on = [R_21_on, R_32_on, R_43_on, R_54_on, R_56_on]

R_12_off = 1/(m_a12_off*cp_air)
R_21_off = 1/(m_a21_off*cp_air)
R_23_off = 1/(m_a23_off*cp_air)
R_32_off = 1/(m_a32_off*cp_air)
R_34_off = 1/(m_a34_off*cp_air)
R_43_off = 1/(m_a43_off*cp_air)
R_45_off = 1/(m_a45_off*cp_air)
R_54_off = 1/(m_a54_off*cp_air)
R_56_off = 1/(m_a56_off*cp_air)
R_65_off = 1/(m_a65_off*cp_air)

R_to_cell_off = [R_12_off, R_23_off, R_34_off, R_45_off, R_65_off]
R_from_cell_off = [R_21_off, R_32_off, R_43_off, R_54_off, R_56_off]