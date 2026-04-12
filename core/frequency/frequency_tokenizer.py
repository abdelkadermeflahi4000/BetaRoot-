import numpy as np

class FrequencyTokenizer:
    def __init__(self, n_bins=16):
        self.n_bins = n_bins

    def normalize(self, x):
        x = np.array(x)
        return (x - np.min(x)) / (np.max(x) - np.min(x) + 1e-9)

    def encode(self, frequency, amplitude, phase=None):
        """
        Convert oscillatory signal → structured tokens
        """

        freq_norm = self.normalize(frequency)
        bins = np.floor(freq_norm * self.n_bins).astype(int)

        tokens = []

        for i in range(len(bins)):
            token = {
                "f_bin": int(bins[i]),
                "amp": float(amplitude[i]) if i < len(amplitude) else 0.0,
                "phase": float(phase[i]) if phase is not None and i < len(phase) else 0.0
            }
            tokens.append(token)

        return tokens
