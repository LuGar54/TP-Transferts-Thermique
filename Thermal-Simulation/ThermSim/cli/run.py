import argparse

from ThermSim import LcmModel, animate


def main():
    model = LcmModel()
    animate()
    print('Run was successful')


if __name__ == "__main__":
    main()