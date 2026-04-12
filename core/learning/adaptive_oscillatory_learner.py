import numpy as np


class AdaptiveOscillatoryLearner:
    def __init__(self, n_bins=16, lr=0.05):
        self.n_bins = n_bins
        self.lr = lr

        # weight memory (what system "learns")
        self.weights = np.ones(n_bins)

    # -------------------------
    # Encode tokens into vector
    # -------------------------
    def encode(self, tokens):
        vec = np.zeros(self.n_bins)

        for t in tokens:
            idx = t["f_bin"] % self.n_bins
            vec[idx] += t.get("amp", 1.0)

        return vec

    # -------------------------
    # Forward state
    # -------------------------
    def forward(self, tokens):
        vec = self.encode(tokens)
        weighted = vec * self.weights

        return weighted / (np.linalg.norm(weighted) + 1e-9)

    # -------------------------
    # Learning step (core idea)
    # -------------------------
    def update(self, tokens, reward_signal):
        """
        reward_signal:
        +1 → useful pattern
        -1 → noisy / irrelevant
        """

        vec = self.encode(tokens)

        # normalize
        vec = vec / (np.linalg.norm(vec) + 1e-9)

        # update rule
        self.weights += self.lr * reward_signal * vec

        # stability clamp
        self.weights = np.clip(self.weights, 0.01, 10.0)

    # -------------------------
    # Forgetting mechanism
    # -------------------------
    def decay(self, factor=0.995):
        self.weights *= factor
