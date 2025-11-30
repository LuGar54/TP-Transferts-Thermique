import numpy as np
import sympy as sp


class Lcm():
    def __init__(self, elements):
        self.elements = elements
        self._adjacency = np.zeros((len(elements),)*2)

    def series(self, idx, resistances):
        idx = list(idx)
        resistances = np.array(resistances, dtype=float)

        if len(idx) < 2:
            raise ValueError("Series must contain at least 2 connected nodes")
        if len(resistances) != len(idx) - 1:
            raise ValueError("Need exactly len(idx)-1 resistances for a series chain")

        conductances = 1.0 / resistances  # G = 1/R

        # diagonal terms
        self._adjacency[idx[0], idx[0]] -= conductances[0]
        self._adjacency[idx[-1], idx[-1]] -= conductances[-1]

        mid = idx[1:-1]
        self._adjacency[mid, mid] -= (conductances[:-1] + conductances[1:])

        # off-diagonal neighbor couplings
        for (a, b, G) in zip(idx[:-1], idx[1:], conductances):
            self._adjacency[a, b] += G
            self._adjacency[b, a] += G  # remove if directed

        return self._adjacency
                

    def parallel(resistances):
        pass
    
