# signal/biophoton_decoder.py

import numpy as np
from PyEMD import EMD
from scipy.signal import hilbert

class BiophotonDecoder:
    def __init__(self, sampling_rate=1000):
        self.fs = sampling_rate

    def decompose_signal(self, signal):
        """
        EMD decomposition (part of HHT)
        """
        emd = EMD()
        imfs = emd(signal)
        return imfs

    def hilbert_transform(self, imfs):
        """
        Compute instantaneous frequency & amplitude
        """
        features = []

        for imf in imfs:
            analytic_signal = hilbert(imf)
            amplitude = np.abs(analytic_signal)
            phase = np.unwrap(np.angle(analytic_signal))

            # instantaneous frequency
            inst_freq = np.diff(phase) * self.fs / (2 * np.pi)

            features.append({
                "amplitude": amplitude[:-1],
                "phase": phase[:-1],
                "frequency": inst_freq
            })

        return features

    def extract_tokens(self, features, freq_bins=10):
        """
        Convert features → frequency tokens
        """
        tokens = []

        for f in features:
            freq = f["frequency"]
            amp = f["amplitude"]

            # Normalize frequency
            freq_norm = (freq - np.min(freq)) / (np.max(freq) - np.min(freq) + 1e-9)

            # Quantize into bins
            freq_quant = np.floor(freq_norm * freq_bins)

            for i in range(len(freq_quant)):
                token = {
                    "freq_bin": int(freq_quant[i]),
                    "amplitude": float(amp[i]),
                }
                tokens.append(token)

        return tokens

    def process(self, signal):
        imfs = self.decompose_signal(signal)
        features = self.hilbert_transform(imfs)
        tokens = self.extract_tokens(features)
        return tokens
