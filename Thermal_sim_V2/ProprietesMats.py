import numpy as np

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
# Sources : https://www.engineeringtoolbox.com/concrete-properties-d_1223.html
rho_conc = 2300  # kg/m3
cp_conc = 850    # J/kgK
k_conc = 1.1  # W/mK

# Propriétés des cellules
isbout_vec = [True, False, False, False, False, True]

# Propriétés de l'isolant
k_insul = 0.02  # W/mK
thickness_insul = 0.1  # m

# Propriétés de l'acier
k_acier = 45  # W/mK
thickness_acier = 1E-2  # m

# Propriétés de l'asphalte
k_asphalte = 1.2  # W/mK
thickness_asphalte = 8E-3

# Propriétés de l'air
cp_air = 1005  # J/kgK
rho_air = 1.225  # kg/m3

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

m_on_going_right = [m_a12_on, m_a23_on, m_a34_on, m_a45_on, m_a56_on]
m_on_going_left = [m_a21_on, m_a32_on, m_a43_on, m_a54_on, m_a65_on]

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

m_off_going_right = [m_a12_off, m_a23_off, m_a34_off, m_a45_off, m_a56_off]
m_off_going_left = [m_a21_off, m_a32_off, m_a43_off, m_a54_off, m_a65_off]

m_infiltr = np.abs([0.04107/2 + 0.04483, #1
             (0.04107 + 0.01930)/2,#2
             (0.01930 - 0.06402)/2,#3
             (-0.06402 - 0.05980)/2,#4
             (-0.05980 - 0.03247)/2,#5
             -0.03247/2 + 0.02567])#6

# Propriétés des cellules
heater_power = [10e3, 15e3, 10e3, 7.5e3, 7.5e3, 10e3]
# heater_off = [0, 0, 0, 0, 0, 0]
