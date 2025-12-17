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