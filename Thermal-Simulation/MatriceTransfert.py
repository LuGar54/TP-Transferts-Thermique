import numpy as np
import sympy as sp


class Lcm:
    def __init__(self, elements):
        self.elements = elements
        n = len(elements)
        
        self._adjacency = sp.zeros(n, n)

    def _add_conductance(self, a, b, G):
        # diagonal terms
        self._adjacency[a, a] -= G
        self._adjacency[b, b] -= G
        # off-diagonal symmetric terms
        self._adjacency[a, b] += G
        self._adjacency[b, a] += G

    def series(self, idx, resistances):
        idx = list(idx)

        if len(idx) < 2:
            raise ValueError("Series must contain at least 2 connected nodes")
        if len(resistances) != len(idx) - 1:
            raise ValueError("Need exactly len(idx)-1 resistances")

        resistances = [sp.sympify(R) for R in resistances]
        conductances = [1 / R for R in resistances]

        
        for a, b, G in zip(idx[:-1], idx[1:], conductances):
            self._add_conductance(a, b, G)

    def parallel(self, idx, resistances, node):
        if len(idx) == 0:
            raise ValueError("idx must include at least one node")
        if len(idx) != len(resistances):
            raise ValueError("Need one resistance per parallel branch")

        resistances = [sp.sympify(R) for R in resistances]
        Gs = [1 / R for R in resistances]

        for i, G in zip(idx, Gs):
            self._add_conductance(i, node, G)

    @property
    def matrix(self):
        return self._adjacency