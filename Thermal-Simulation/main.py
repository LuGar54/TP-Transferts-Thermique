import numpy as np
import sympy as sp

from MatriceTransfert import Lcm

def main():
     # list of element capacities
    # elements = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # model = Lcm(elements)
    # model.series([0, 1, 2, 3, 4, 5], [12, 23, 34, 45, 56])
    # for i in range(6):
    #     model.series([i, i+6], [int(f'{i}{i+6}')])
    #     print(f'{i}{i+6}')

    # print(repr(model._adjacency))

    R12, R23, R34, R45, R56, R17, R28, R39, R410, R511, R612 = sp.symbols('R_{1\,2} R_{2\,3} R_{3\,4} R_{4\,5} R_{5\,6} R_{1\,7} R_{2\,8} R_{3\,9} R_{4\,10} R_{5\,11} R_{6\,12}')

    # R12, R23, R34, R45, R56, R17, R28, R39, R410, R511, R612 = sp.symbols('R12 R23 R34 R45 R56 R17 R28 R39 R410 R511 R612')


    model = Lcm([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    model.series([0, 1, 2, 3, 4, 5], [R12, R23, R34, R45, R56])
    for i in range(6):
        model.series([i, i+6], [locals()[f'R{i+1}{i+7}']])

    print(sp.simplify(model.matrix))
    # sp.pprint(model.matrix)
    # print(sp.latex(sp.simplify(model.matrix)))


if __name__ == '__main__':
    main()