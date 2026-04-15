# core/frequency/agent.py
import numpy as np
from numba import njit
from dataclasses import dataclass
from typing import Dict

@njit(fastmath=True)
def kuramoto_step(phases, freqs, K):
    n = len(phases)
    new_phases = np.zeros(n)
    for i in range(n):
        interaction = 0.0
        for j in range(n):
            interaction += np.sin(phases[j] - phases[i])
        dtheta = freqs[i] + (K / n) * interaction
        new_phases[i] = phases[i] + dtheta
    return new_phases % (2 * np.pi)

@dataclass
class FrequencyAgentState:
    id: int
    phases: np.ndarray
    freqs: np.ndarray
    consciousness_level: float = 0.0

class FrequencyAgent:
    def __init__(self, agent_id: int, n_oscillators: int = 24):
        self.id = agent_id
        self.state = FrequencyAgentState(
            id=agent_id,
            phases=np.random.uniform(0, 2*np.pi, n_oscillators),
            freqs=np.random.uniform(0.6, 1.2, n_oscillators),  # حول Schumann
        )

    def step(self, global_coupling: float = 0.1):
        """خطوة واحدة محسنة بـ Numba"""
        self.state.phases = kuramoto_step(
            self.state.phases, 
            self.state.freqs, 
            global_coupling * (1 + self.state.consciousness_level)
        )
        
        # حساب الوعي المحلي
        sync = 1 / (1 + np.std(self.state.phases))
        diversity = np.var(self.state.freqs)
        self.state.consciousness_level = 0.65 * sync + 0.35 * diversity
        
        return self.state.consciousness_level
