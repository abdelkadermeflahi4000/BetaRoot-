# signal/global_field/noosphere_engine.py

import numpy as np
from PyEMD import EMD
from scipy.signal import hilbert, welch

class NoosphereEngine:
    def __init__(self, sampling_rate=100):
        self.fs = sampling_rate

    # ----------------------------
    # 1. Decomposition (HHT)
    # ----------------------------
    def decompose(self, signal):
        emd = EMD()
        imfs = emd(signal)
        return imfs

    # ----------------------------
    # 2. Instantaneous Features
    # ----------------------------
    def extract_features(self, imfs):
        features = []

        for imf in imfs:
            analytic = hilbert(imf)
            amplitude = np.abs(analytic)
            phase = np.unwrap(np.angle(analytic))
            freq = np.diff(phase) * self.fs / (2 * np.pi)

            features.append({
                "frequency": freq,
                "amplitude": amplitude[:-1],
                "phase": phase[:-1]
            })

        return features

    # ----------------------------
    # 3. Spectrum (Welch)
    # ----------------------------
    def spectrum(self, signal):
        freqs, power = welch(signal, fs=self.fs, nperseg=256)
        return freqs, power

    # ----------------------------
    # 4. Tokenization
    # ----------------------------
    def tokenize(self, features, bins=8):
        tokens = []

        for f in features:
            freq = f["frequency"]
            amp = f["amplitude"]

            if len(freq) == 0:
                continue

            norm = (freq - np.min(freq)) / (np.max(freq) - np.min(freq) + 1e-9)
            quant = np.floor(norm * bins)

            for i in range(len(quant)):
                tokens.append({
                    "freq_bin": int(quant[i]),
                    "amplitude": float(amp[i]),
                    "type": "global_field"
                })

        return tokens

    # ----------------------------
    # 5. Full Pipeline
    # ----------------------------
    def process(self, signal):
        imfs = self.decompose(signal)
        features = self.extract_features(imfs)
        tokens = self.tokenize(features)

        return tokens
