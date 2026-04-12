import numpy as np


class WorldModel:
    def __init__(self, state_dim=16, lr=0.05):
        self.state_dim = state_dim
        self.lr = lr

        # internal world state representation
        self.world_state = np.zeros(state_dim)

        # transition matrix (how world evolves)
        self.transition = np.eye(state_dim)

        # uncertainty tracker
        self.uncertainty = np.ones(state_dim)

    # -------------------------
    # encode input signal
    # -------------------------
    def encode(self, signal):
        signal = np.array(signal)

        if len(signal) < self.state_dim:
            padded = np.zeros(self.state_dim)
            padded[:len(signal)] = signal
            signal = padded

        return signal[:self.state_dim]

    # -------------------------
    # update world state
    # -------------------------
    def observe(self, signal):
        obs = self.encode(signal)

        prediction = self.transition @ self.world_state

        error = obs - prediction

        # update world state
        self.world_state += self.lr * error

        # update uncertainty
        self.uncertainty = 0.9 * self.uncertainty + 0.1 * np.abs(error)

        return error

    # -------------------------
    # learn dynamics (key part)
    # -------------------------
    def learn_dynamics(self, prev_state, next_state):
        prev = self.encode(prev_state)
        next_ = self.encode(next_state)

        # simple linear dynamics learning
        delta = np.outer((next_ - prev), prev)

        self.transition += self.lr * delta

    # -------------------------
    # predict next world state
    # -------------------------
    def predict(self):
        return self.transition @ self.world_state

    # -------------------------
    # stability of world model
    # -------------------------
    def stability(self):
        return float(1.0 / (1.0 + np.mean(self.uncertainty)))
