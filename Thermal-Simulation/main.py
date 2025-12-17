import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

from MatriceTransfert import Lcm
from Capacitances import (vol_conc_cells,
C_conc_cells,
vol_air_cells,
C_air_cells)
from Resistances import *
from animation_vis import animate_thermal_system

def generer_matrices():
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


    ##### test values #####

    # subs_cap = dict(zip(C, np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, np.inf])))
    # subs_res_cell_on = dict(zip(R_horiz, 5*np.ones(6)))
    # subs_res_cell_off = dict(zip(R_horiz, 5*np.ones(6)))
    # subs_res_conc_on = dict(zip(R_vert, 5*np.ones(6)))
    # subs_res_conc_off = dict(zip(R_vert, 5*np.ones(6)))
    # subs_res_ext = dict(zip(R_ext, 5*np.ones(6)))

    #########

    transfer_mat = transfer_mat.subs(subs_cap).subs(subs_res_ext)

    # corrige les constantes de temps pour être selon 2 minutes
    transfert_mat_on = transfer_mat.subs(subs_res_cell_on).subs(subs_res_conc_on)
    transfert_mat_off = transfer_mat.subs(subs_res_cell_off).subs(subs_res_conc_off)

    return np.array(transfert_mat_on).astype(np.float64), np.array(transfert_mat_off).astype(np.float64)

def controle(T1, T6, is_on) -> bool:
    if T1 < -15 or T6 < -15:
        return True
    elif T1 < 50 and T6 < 50 and is_on:
        return True
    else:
        return False
        

def temp_sol(t):
    # la température du sol oscille entre -15 et -5 l'hivers au cours d'une journée
    return -5*np.cos(t/(24*60)) - 10

def simulate(duree, mats):
    # duree de la simulation en jours
    # timestep est de 2 minutes
    duree = duree * 24 * 30 # 24 * 30 * 2 minutes dans une journee
    
    # on initialise à -10 degree partout
    temperatures = np.full((13), -10)
    historique_temperature = np.zeros((duree, 13))

    chauffage = False
    source = [np.zeros((13,)), np.array([10e3, 15e3, 10e3, 7.5e3, 7.5e3, 10e3, 0, 0, 0, 0, 0, 0, 0])*120]

    for i in range(duree):
        temperatures[12] = temp_sol(i)
        historique_temperature[i] = temperatures
        
        #chauffage = controle(*temperatures[[0, 5]], chauffage) # on sonde les températures aux bouts (cellules d'airs)
        temperatures =  mats[chauffage] @ temperatures + temperatures# + source[chauffage]

    return historique_temperature
    
        
def main():
    mats = generer_matrices()

    hist = simulate(31, mats)
    # animate_thermal_system(hist)
    
    plt.plot(np.linspace(0, 1, 31*24*30), hist[:,3])
    plt.ylim(-20, 50)
    plt.show()
    



if __name__ == '__main__':
    main()