import numpy as np
from ProprietesMats import *


def volume_concrete(is_bou:bool):
    # plancher
    vol_floor = tot_width * p_len * thickness_conc
    # murs
    vol_walls = 2 * (tot_height * p_len * thickness_conc) 
    if is_bou:
        vol_walls += (tot_height * tot_width * thickness_conc)
    return vol_floor + vol_walls

def get_capacitance_concrete(rho, cp, is_bou:bool):
    vol_concrete = volume_concrete(is_bou)
    C_concrete = rho * cp * vol_concrete
    return C_concrete

vol_cells = [volume_concrete(i) for i in isbout_vec]
C_cells = [get_capacitance_concrete(rho, cp, i) for i in isbout_vec]

print(C_cells)