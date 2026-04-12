import numpy as np
import matplotlib.pyplot as plt
from signal.biophoton_decoder import BiophotonDecoder

# Generate synthetic "biophoton-like" signal
fs = 1000
t = np.linspace(0, 1, fs)

signal = (
    0.5 * np.sin(2 * np.pi * 10 * t) +
    0.3 * np.sin(2 * np.pi * 40 * t) +
    0.2 * np.random.randn(fs)
)

# Add bursts
signal[200:220] += 2
signal[600:620] += 1.5

decoder = BiophotonDecoder(fs)
tokens = decoder.process(signal)

print("Sample Tokens:")
print(tokens[:10])

plt.plot(signal)
plt.title("Simulated Biophoton Signal")
plt.show()
