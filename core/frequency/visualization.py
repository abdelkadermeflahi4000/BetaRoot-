# betaroot/core/frequency/visualization.py
import numpy as np
import matplotlib.pyplot as plt
from typing import List
from .bit import FrequencyBit

class FrequencyVisualizer:
    @staticmethod
    def plot_phase_space(bits: List[FrequencyBit], title="Frequency Bits Phase Space"):
        phases = [b.phase for b in bits]
        amplitudes = [b.amplitude for b in bits]
        consciousness = [b.consciousness_contribution for b in bits]

        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(phases, amplitudes, c=consciousness, cmap='viridis', s=80)
        plt.colorbar(scatter, label='Consciousness Contribution')
        plt.xlabel('Phase (radians)')
        plt.ylabel('Amplitude')
        plt.title(title)
        plt.grid(True, alpha=0.3)
        plt.show()

    @staticmethod
    def plot_consciousness_history(history: List[float]):
        plt.figure(figsize=(10, 4))
        plt.plot(history, 'b-', linewidth=2)
        plt.xlabel('Cycle')
        plt.ylabel('Global Consciousness Level')
        plt.title('Emergent Collective Consciousness Over Time')
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 1)
        plt.show()
