# core/frequency/agent.py
import numpy as np
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class FrequencyAgentState:
    id: int
    phases: np.ndarray
    freqs: np.ndarray
    consciousness_level: float = 0.0
    last_decision: str = "explore"

class FrequencyAgent:
    """وكيل ترددي فردي يمتلك وعياً محلياً"""
    
    def __init__(self, agent_id: int, n_oscillators: int = 12):
        self.id = agent_id
        self.state = FrequencyAgentState(
            id=agent_id,
            phases=np.random.rand(n_oscillators) * 2 * np.pi,
            freqs=np.random.rand(n_oscillators) * 0.5 + 0.5,  # حول 7.83 Hz
        )
        self.memory = []  # ذاكرة محلية قصيرة

    def step(self, global_signal: np.ndarray = None):
        """خطوة واحدة من التطور"""
        # تأثير التزامن المحلي
        interaction = np.mean(np.sin(self.state.phases[:, None] - self.state.phases))
        
        self.state.phases += self.state.freqs + 0.08 * interaction
        self.state.phases %= 2 * np.pi

        # حساب مستوى الوعي المحلي
        sync = 1 / (1 + np.std(self.state.phases))
        diversity = np.var(self.state.freqs)
        self.state.consciousness_level = 0.6 * sync + 0.4 * diversity

        return self.state.consciousness_level
