import numpy as np
from PyEMD import EMD
from scipy.signal import hilbert, welch


class NoosphereEngine:
    def __init__(self, sampling_rate=1000):
        self.fs = sampling_rate

    # ----------------------------
    # EMD decomposition
    # ----------------------------
    def decompose(self, signal):
        emd = EMD()
        return emd(signal)

    # ----------------------------
    # Hilbert features
    # ----------------------------
    def extract_features(self, imfs):
        all_features = []

        for imf in imfs:
            analytic = hilbert(imf)

            amplitude = np.abs(analytic)
            phase = np.unwrap(np.angle(analytic))

            if len(phase) < 2:
                continue

            frequency = np.diff(phase) * self.fs / (2 * np.pi)

            all_features.append({
                "freq": frequency,
                "amp": amplitude[:-1],
                "phase": phase[:-1]
            })

        return all_features

    # ----------------------------
    # Spectral stability (important upgrade)
    # ----------------------------
    def spectral_stability(self, signal):
        freqs, power = welch(signal, fs=self.fs, nperseg=512)

        stability = np.std(power) / (np.mean(power) + 1e-9)

        return {
            "freqs": freqs,
            "power": power,
            "stability": float(stability)
        }

    # ----------------------------
    # Token generation (enhanced)
    # ----------------------------
    def tokenize(self, features):
        tokens = []

        for f in features:
            freq = f["freq"]
            amp = f["amp"]

            if len(freq) == 0:
                continue

            f_min, f_max = np.min(freq), np.max(freq)

            norm = (freq - f_min) / (f_max - f_min + 1e-9)
            bins = (norm * 12).astype(int)

            for i in range(len(bins)):
                tokens.append({
                    "type": "global_field",
                    "freq_bin": int(bins[i]),
                    "amplitude": float(amp[i]),
                    "stability_weight": float(np.mean(amp))
                })

        return tokens

    # ----------------------------
    # FULL PIPELINE
    # ----------------------------
    def process(self, signal):
        imfs = self.decompose(signal)
        features = self.extract_features(imfs)
        tokens = self.tokenize(features)
        spectral = self.spectral_stability(signal)

        return {
            "tokens": tokens,
            "spectral": spectral
        }
