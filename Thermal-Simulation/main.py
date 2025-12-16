import numpy as np
import sympy as sp

from MatriceTransfert import Lcm
from Capacitances import vol_cells as vols
from Capacitances import C_cells as C

def main():
    R12, R23, R34, R45, R56, R17, R28, R39, R410, R511, R612 = sp.symbols('R12 R23 R34 R45 R56 R17 R28 R39 R410 R511 R612')

    C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12 = sp.symbols('C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12')

    cmat = sp.diag(C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12).inv()
    
    model = Lcm([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    model.series([0, 1, 2, 3, 4, 5], [R12, R23, R34, R45, R56])
    for i in range(6):
        model.series([i, i+6], [locals()[f'R{i+1}{i+7}']])

    # matrice 
    transfer_mat = cmat @ model.matrix
    transfer_mat.simplify()
    # sp.pprint(cmat)
    # sp.pprint(model.matrix)

    # watch out c'est vrm laid!
    sp.pprint(transfer_mat)
    

if __name__ == '__main__':
    main()