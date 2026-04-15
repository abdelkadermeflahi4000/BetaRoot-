# core/frequency/consciousness.py
import numpy as np

class ConsciousnessLayer:
    def __init__(self):
        self.history = []

    def compute_consciousness(self, sync: float, diversity: float, memory_coupling: float) -> float:
        """مقياس الوعي العلمي (مبني على IIT + Dynamical Systems)"""
        S = 1 / (1 + (1 - sync))          # التزامن
        D = np.clip(diversity, 0.1, 2.0)  # التنوع
        M = np.clip(memory_coupling, 0.0, 1.0)

        # صيغة مرجحة علمياً
        C = 0.45 * S + 0.30 * D + 0.25 * M
        
        self.history.append(C)
        return float(C)
