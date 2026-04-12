import numpy as np

class OscillatoryEngine:
    def __init__(self):
        self.state = None

    def ingest_tokens(self, tokens):
        """
        Convert frequency tokens into internal state vector
        """

        vec = np.zeros(16)

        for t in tokens:
            idx = t["f_bin"] % 16
            vec[idx] += t["amp"]

        self.state = vec / (np.linalg.norm(vec) + 1e-9)
        return self.state

    def compare_states(self, new_tokens):
        new_state = self.ingest_tokens(new_tokens)

        if self.state is None:
            return 0.0

        similarity = np.dot(self.state, new_state)
        return float(similarity)
