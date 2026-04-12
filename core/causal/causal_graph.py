import numpy as np
from collections import defaultdict


class CausalGraph:
    def __init__(self, decay=0.99):
        # adjacency: cause -> effect weights
        self.graph = defaultdict(lambda: defaultdict(float))
        self.decay = decay

    # -------------------------
    # Add causal observation
    # -------------------------
    def observe(self, cause, effect, strength=1.0):
        self.graph[cause][effect] += strength

    # -------------------------
    # Normalize / stabilize graph
    # -------------------------
    def normalize(self):
        for c in self.graph:
            total = sum(self.graph[c].values()) + 1e-9
            for e in self.graph[c]:
                self.graph[c][e] /= total

    # -------------------------
    # Decay weak relations
    # -------------------------
    def decay_graph(self):
        for c in list(self.graph.keys()):
            for e in list(self.graph[c].keys()):
                self.graph[c][e] *= self.decay

                if self.graph[c][e] < 0.01:
                    del self.graph[c][e]

    # -------------------------
    # Query causal influence
    # -------------------------
    def get_effects(self, cause):
        return dict(self.graph.get(cause, {}))
