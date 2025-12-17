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
    C1, C2 = 4, np.inf
    R12, R21 = 100, 7
    mat = np.array([[-1/(R12*C1), 1/(R21*C1)],
                    [1/(R12*C2), -1/(R21*C1)]])
    return mat

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
    temperatures = np.full((2), -10)
    historique_temperature = np.zeros((duree, 2))

    # chauffage = False
    # source = [np.zeros((13,)), np.array([10e3, 15e3, 10e3, 7.5e3, 7.5e3, 10e3, 0, 0, 0, 0, 0, 0, 0])*120]

    for i in range(duree):
        temperatures[1] = temp_sol(i)
        historique_temperature[i] = temperatures
        
        #chauffage = controle(*temperatures[[0, 5]], chauffage) # on sonde les températures aux bouts (cellules d'airs)
        temperatures =  mats @ temperatures + temperatures# + source[chauffage]

    return historique_temperature
    
        
def main():
    mats = generer_matrices()

    hist = simulate(31, mats)
    # animate_thermal_system(hist)
    
    plt.plot(np.linspace(0, 1, 31*24*30), hist[:,0])
    plt.ylim(-20, 50)
    plt.show()
    



if __name__ == '__main__':
    main()