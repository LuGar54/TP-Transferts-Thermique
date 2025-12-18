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

def get_capacitance_concrete(rho, cp, vol_conc):
    C_concrete = rho * cp * vol_conc
    return C_concrete

vol_conc_cells = [volume_concrete(i) for i in isbout_vec]
C_conc_cells = [get_capacitance_concrete(rho_conc, cp_conc, i) for i in vol_conc_cells]

vol_air_cells = [tot_width * tot_height * p_len for _ in isbout_vec]
C_air_cells = [rho_air * cp_air * vol for vol in vol_air_cells]

C_air_ajuste = C_air_cells + (np.array(C_conc_cells)/8)
