import numpy as np
import sympy as sp


class Lcm():
    def __init__(self, elements):
        self.elements = elements
        self._adjacency = np.zeros((len(elements),)*2)

    """j'ai fait une methode de base ensuite j'ai demande a chatgpt de l'optimiser"""
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
                
    """meme chose que la methode series"""
    def parallel(self, idx, resistances, node):
        idx = np.asarray(idx, dtype=int)
        resistances = np.asarray(resistances, dtype=float)

        if len(idx) == 0:
            raise ValueError("idx must contain at least one node")
        if resistances.shape[0] != idx.shape[0]:
            raise ValueError("Need one resistance per node in idx")

        G = 1.0 / resistances  # conductances

        # update diagonal for nodes in parallel group
        diag_updates = np.bincount(idx, weights=-G, minlength=self._adjacency.shape[0])
        self._adjacency[np.diag_indices_from(self._adjacency)] += diag_updates

        # update diagonal for target node
        self._adjacency[node, node] -= G.sum()

        # off-diagonal couplings to node
        self._adjacency[idx, node] += G
        self._adjacency[node, idx] += G  # remove this line if directed

