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
rho_conc = 2400  # kg/m3
cp_conc = 880    # J/kgK
k_conc = 1.8  # W/mK

# Propriétés des cellules
isbout_vec = [True, False, False, False, False, True]

# Propriétés de l'isolant
k_insul = 0.02  # W/mK
thickness_insul = 0.1  # m

# Propriétés de l'air
cp_air = 1005  # J/kgK

m_a12_on = 0.2381
m_a21_on = 0.4438
m_a23_on = 0.3268
m_a32_on = 0.7042
m_a34_on = 0.2646
m_a43_on = 0.5915
m_a45_on = 0.1988
m_a54_on = 0.2915
m_a56_on = 0.4694
m_a65_on = 0.4070

m_a12_off = 0.04113
m_a21_off = 0.06844
m_a23_off = 0.05290
m_a32_off = 0.09304
m_a34_off = 0.05121
m_a43_off = 0.10386
m_a45_off = 0.04163
m_a54_off = 0.08528
m_a56_off = 0.03718
m_a65_off = 0.05788
