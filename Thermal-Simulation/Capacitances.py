import numpy as np


def volume_concrete(is_bou:bool):
    # plancher
    vol_floor = tot_width * p_len * thickness
    # murs
    vol_walls = 2 * (tot_height * p_len * thickness) 
    if is_bou:
        vol_walls += (tot_height * tot_width * thickness)
    return vol_floor + vol_walls

def get_capacitance(rho, cp, is_bou:bool):
    vol_concrete = volume_concrete(is_bou)
    C_concrete = rho * cp * vol_concrete
    return C_concrete

    
# Dimension totale
tot_len = 26.1 
tot_width = 3.7
tot_height = 1.7
thickness = 0.4
p_len = tot_len/6

# Propriétés du béton
rho = 2400  # kg/m3
cp = 880    # J/kgK

isbout_vec = [True, False, False, False, False, True]
vol_cells = [volume_concrete(i) for i in isbout_vec]
C_cells = [get_capacitance(rho, cp, i) for i in isbout_vec]

