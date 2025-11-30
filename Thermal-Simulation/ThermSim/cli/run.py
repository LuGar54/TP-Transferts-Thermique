import argparse

from ThermSim import Lcm, animate


def main():
    # list of element capacities
    elements = [1, 1, 1, 1, 1]
    model = Lcm(elements)
    print(model.series([0,1,2,4], [10, 20, 30]))



if __name__ == "__main__":
    main()