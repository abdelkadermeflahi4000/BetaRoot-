import numpy as np


class CausalExtractor:
    def __init__(self, threshold=0.3):
        self.threshold = threshold

    # -------------------------
    # convert tokens → state vector
    # -------------------------
    def vectorize(self, tokens, size=16):
        vec = np.zeros(size)

        for t in tokens:
            idx = t["f_bin"] % size
            vec[idx] += t.get("amp", 1.0)

        return vec / (np.linalg.norm(vec) + 1e-9)

    # -------------------------
    # detect causal change
    # -------------------------
    def extract(self, prev_tokens, curr_tokens):
        if prev_tokens is None:
            return []

        prev = self.vectorize(prev_tokens)
        curr = self.vectorize(curr_tokens)

        diff = curr - prev

        causal_links = []

        for i in range(len(diff)):
            if abs(diff[i]) > self.threshold:
                causal_links.append((i, float(diff[i])))

        return causal_links
