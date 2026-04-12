import numpy as np
from collections import deque


class TemporalMemory:
    def __init__(self, max_size=100):
        self.buffer = deque(maxlen=max_size)

    # -------------------------
    # store time-stamped state
    # -------------------------
    def add(self, state, timestamp):
        self.buffer.append({
            "state": np.array(state),
            "time": timestamp
        })

    # -------------------------
    # temporal difference
    # -------------------------
    def temporal_diff(self):
        if len(self.buffer) < 2:
            return None

        prev = self.buffer[-2]["state"]
        curr = self.buffer[-1]["state"]

        return curr - prev

    # -------------------------
    # trend detection
    # -------------------------
    def trend(self):
        if len(self.buffer) < 5:
            return None

        states = np.array([b["state"] for b in self.buffer])
        return np.mean(states[-1] - states[0])
