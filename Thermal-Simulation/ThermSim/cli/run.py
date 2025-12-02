import argparse

import numpy as np

from ThermSim import Lcm, animate


def main():
    # list of element capacities
    elements = [1, 1, 1, 1, 1, 1]
    model = Lcm(elements)
    model.series([0, 1, 2, 3, 4, 5], [1, 1, 1, 1, 1])
#    model.parallel([0, 1, 2, 3, 4, 5], [1, 1, 1, 1, 1, 1], node=7)
#    model.parallel([0, 1, 2, 3, 4, 5], [1, 1, 1, 1, 1, 1], node=9)

    np.set_printoptions(precision=2)
    print(repr(model._adjacency))
    




if __name__ == "__main__":
    main()