# Dimension totale
tot_len = 26.1 
tot_width = 3.7
tot_height = 1.7
thickness_conc = 0.4
p_len = tot_len/6

a_mur = tot_height * tot_width
a_p_mur = tot_height * p_len
a_p_sol = tot_width * p_len

# Propriétés du béton
rho = 2400  # kg/m3
cp = 880    # J/kgK
k_conc = 1.8  # W/mK

# Propriétés des cellules
isbout_vec = [True, False, False, False, False, True]

# Propriétés de l'isolant
k_insul = 0.02  # W/mK
thickness_insul = 0.1  # m