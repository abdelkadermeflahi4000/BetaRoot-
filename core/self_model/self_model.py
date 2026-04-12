import numpy as np


class SelfModel:
    def __init__(self, n_bins=16):
        self.n_bins = n_bins

        # model of "self state evolution"
        self.self_state = np.zeros(n_bins)

        # drift tracking
        self.drift_history = []

    # -------------------------
    # update internal model
    # -------------------------
    def update(self, state):
        state = np.array(state)

        drift = state - self.self_state

        self.self_state += 0.1 * drift

        self.drift_history.append(np.linalg.norm(drift))

    # -------------------------
    # detect self-change rate
    # -------------------------
    def change_rate(self):
        if len(self.drift_history) < 5:
            return 0.0

        return float(np.mean(self.drift_history[-5:]))

    # -------------------------
    # predict next self state
    # -------------------------
    def predict_next(self):
        return self.self_state * 1.05
