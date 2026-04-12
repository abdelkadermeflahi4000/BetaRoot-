import numpy as np


class SelfCuriosityEngine:
    def __init__(self, n_bins=16, lr=0.05, novelty_threshold=0.3):
        self.n_bins = n_bins
        self.lr = lr
        self.novelty_threshold = novelty_threshold

        # internal predictive model (simple expectation map)
        self.expectation = np.zeros(n_bins)

        # curiosity memory
        self.curiosity_trace = []

    # -------------------------
    # Encode tokens
    # -------------------------
    def encode(self, tokens):
        vec = np.zeros(self.n_bins)

        for t in tokens:
            idx = t["f_bin"] % self.n_bins
            vec[idx] += t.get("amp", 1.0)

        return vec / (np.linalg.norm(vec) + 1e-9)

    # -------------------------
    # Compute prediction error
    # -------------------------
    def prediction_error(self, state):
        return np.abs(state - self.expectation)

    # -------------------------
    # Curiosity signal (no reward!)
    # -------------------------
    def curiosity(self, tokens):
        state = self.encode(tokens)
        error = self.prediction_error(state)

        curiosity_score = np.mean(error)

        return state, error, curiosity_score

    # -------------------------
    # Learning rule (pure curiosity)
    # -------------------------
    def update(self, tokens):
        state, error, curiosity_score = self.curiosity(tokens)

        # update expectation (predictive memory)
        self.expectation += self.lr * (state - self.expectation)

        # store curiosity trace
        self.curiosity_trace.append(curiosity_score)

        return {
            "state": state,
            "error": error,
            "curiosity": curiosity_score
        }

    # -------------------------
    # Detect novelty bursts
    # -------------------------
    def is_novel(self):
        if len(self.curiosity_trace) < 10:
            return True

        recent = np.mean(self.curiosity_trace[-10:])
        return recent > self.novelty_threshold
