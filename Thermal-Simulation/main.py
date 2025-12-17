import numpy as np
import sympy as sp

from MatriceTransfert import Lcm
from Capacitances import (vol_conc_cells,
C_conc_cells,
vol_air_cells,
C_air_cells)
from Resistances import *

def controle(T1, T6) -> bool:
    pass

def main():
    # résistances inter cellules d'air
    R_horiz = [sp.Symbol(f'R{i}{i+1}') for i in range(1, 6)]
    
    # résistances cellules d'air vers béton
    R_vert = [sp.Symbol(f'R{i}{i+6}') for i in range(1, 7)]
    
    # résistances béton vers sol extérieur
    R_ext = [sp.Symbol(f"R_{i}ext") for i in range(7, 13)]

    C = sp.symbols('C1:14')
    cmat = sp.diag(*[1/c for c in C])

    # cellules d'air 1 à 6
    # béton 7 à 12
    # extérieur 13
    model = Lcm(list(range(1, 14)))
    
    # connexion inter celllule d'air
    # 1<->2<->3<->4<->5<->6
    model.series(list(range(6)), R_horiz)

    # connexion celllule d'air vers béton
    for i, r_symbol in zip(range(6), R_vert):
        model.series([i, i+6], [r_symbol])

    # béton vers extérieur
    model.parallel(list(range(6, 12)), R_ext, 12)

    transfer_mat = cmat @ model.matrix

    # extérieur = réservoir thermique donc C_ext = inf
    subs_cap = dict(zip(C, C_air_cells + C_conc_cells + [np.inf]))

    # faudrait modifier la facon de generer la matrice car elle ne support pas des résistances différent de chaque coté
    subs_res_cell_on = dict(zip(R_horiz, R_to_cell_on))
    subs_res_cell_off = dict(zip(R_horiz, R_to_cell_off))
    subs_res_conc_on = dict(zip(R_vert, R_convs_forcee))
    subs_res_conc_off = dict(zip(R_vert, R_convs_naturelles))
    subs_res_ext = dict(zip(R_ext, R_Tbet_Text))

    transfer_mat = transfer_mat.subs(subs_cap).subs(subs_res_ext)
    
    transfert_mat_on = transfer_mat.subs(subs_res_cell_on).subs(subs_res_conc_on)
    transfert_mat_off = transfer_mat.subs(subs_res_cell_off).subs(subs_res_conc_off)

    print(sp.latex(transfert_mat_on))
    # print(sp.latex(transfert_mat_off))

if __name__ == '__main__':
    main()