import numpy as np


class EarthSignalAdapter:
    def __init__(self):
        self.base_freq = 7.83

    # -------------------------
    # simulate / ingest Schumann signal
    # -------------------------
    def process(self, t):
        signal = (
            np.sin(2 * np.pi * 7.83 * t) +
            0.5 * np.sin(2 * np.pi * 14.3 * t) +
            0.2 * np.sin(2 * np.pi * 20.8 * t)
        )

        noise = np.random.randn(len(t)) * 0.05

        return signal + noise

    # -------------------------
    # extract world features
    # -------------------------
    def extract_features(self, signal):
        return {
            "energy": float(np.mean(signal ** 2)),
            "mean": float(np.mean(signal)),
            "variance": float(np.var(signal))
        }
