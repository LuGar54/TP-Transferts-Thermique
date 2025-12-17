import numpy as np
import sympy as sp

from MatriceTransfert import Lcm
from Capacitances import vol_cells as vols
from Capacitances import C_cells as C


def main():
    R_horiz = [sp.Symbol(f'R{i}{i+1}') for i in range(1, 6)]
    R_vert = [sp.Symbol(f'R{i}{i+6}') for i in range(1, 7)]

    C = sp.symbols('C1:13')
    cmat = sp.diag(*[1/c for c in C])
    
    model = Lcm(list(range(1, 13)))
    model.series(list(range(6)), R_horiz)
    for i, r_symbol in zip(range(6), R_vert):
        model.series([i, i+6], [r_symbol])

     
    transfer_mat = cmat @ model.matrix
    transfer_mat.simplify()
    # sp.pprint(cmat)
    # sp.pprint(model.matrix)

    # watch out c'est vrm laid!
    sp.pprint(transfer_mat)
    

if __name__ == '__main__':
    main()