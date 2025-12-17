import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

from MatriceTransfert import Lcm
from ProprietesMats import cp_air, rho_air
from Capacitances import (vol_conc_cells,
C_conc_cells,
vol_air_cells,
C_air_cells)
from Resistances import *
from animation_vis import animate_thermal_system
    

    # faudrait modifier la facon de generer la matrice car elle ne support pas des résistances différent de chaque coté
    # subs_res_cell_on = dict(zip(R_horiz, R_to_cell_on))
    # subs_res_cell_off = dict(zip(R_horiz, R_to_cell_off))
    # subs_res_conc_on = dict(zip(R_vert, R_convs_forcee))
    # subs_res_conc_off = dict(zip(R_vert, R_convs_naturelles))
    # subs_res_ext = dict(zip(R_ext, R_Tbet_Text))

# def controle(T1, T6, is_on) -> bool:
#     if T1 < -15 or T6 < -15:
#         return True
#     elif T1 < 50 and T6 < 50 and is_on:
#         return True
#     else:
#         return False
        

def temp_sol(t):
    # la température du sol oscille entre -15 et -5 l'hivers au cours d'une journée
    return -5*np.cos(t*np.pi/(24*15)) - 10

def simulate(duree):
    # duree de la simulation en jours
    # timestep est de 2 minutes
    duree = (int)(duree * 24 * 60/2) # il y a 24 * 30 de 2 minutes dans une journee
    
    # on initialise à -10 degree partout
    temperatures = np.full((13), -10.01)
    historique_temperature = np.zeros((duree, 13))

    chauffage = False
    source = [np.array([10e3, 15e3, 10e3, 7.5e3, 7.5e3, 10e3, 0, 0, 0, 0, 0, 0, 0])*120]
    # heating = source * 

    dt = 120  # timestep en secondes

    for i in range(duree):
        temperatures[0] = temp_sol(i)
        historique_temperature[i] = temperatures
        newTemps = temperatures.copy()
        # dQ = ((temperatures[0]-temperatures[1])/(R_convs_naturelles[0]*C_conc_cells[0]))

        correction = 1

        for j in range(1, 7):
            # print(j)
            newTemps[j] = temperatures[j] + dt * ((temperatures[j+1]-temperatures[j])/(R_12_off) * 1/(C_air_cells[0])
                                                    + (temperatures[j+6] - temperatures[j])/(R_convs_naturelles[0])*1/C_conc_cells[0])
            
        for j in range(7, 13):
            newTemps[j] = temperatures[j] + dt * ((temperatures[j-6]-temperatures[j])/(R_convs_naturelles[0]) * 1/C_conc_cells[0]
                                                      + (temperatures[0]-temperatures[j])/(R_Tbet_Text[0]) * 1/C_conc_cells[0])
            
        temperatures = newTemps
        # print((temperatures[0]-temperatures[j])/(R_Tbet_Text[0]*C_conc_cells[0]))
        # return historique_temperature
        #chauffage = controle(*temperatures[[0, 5]], chauffage) # on sonde les températures aux bouts (cellules d'airs)
        # temperatures =  mats[chauffage] @ temperatures + temperatures# + source[chauffage]

        # temperatures[2] = temperatures[2]/R_23_off + temperatures[1]/R_32_off

    return historique_temperature
    
        
def main():
    hist = simulate(31)
    # animate_thermal_system(hist)
    x = np.linspace(0, 31, 31*24*30)
    plt.plot(x, hist[:, 1], label='Cellule 1')
    plt.ylim(-20, 50)
    plt.show()
    



if __name__ == '__main__':
    main()