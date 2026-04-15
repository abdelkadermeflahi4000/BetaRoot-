# betaroot/core/frequency/bit.py
import numpy as np
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional

@dataclass
class FrequencyBit:
    """Bit ترددي آحادي — أصغر وحدة معنى في BetaRoot"""
    id: str
    phase: float                    # 0 → 2π
    amplitude: float
    frequency: float                # حول 7.83 Hz
    resonance_score: float = 0.0
    causal_link: Optional[str] = None
    consciousness_contribution: float = 0.0
    timestamp: str = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.metadata is None:
            self.metadata = {}

    def to_unary(self) -> Dict:
        """تحويل إلى تمثيل آحادي"""
        return {
            "type": "frequency_bit",
            "value": self.phase,                    # Only 1 Principle
            "strength": self.amplitude * self.resonance_score,
            "id": self.id,
            "consciousness": round(self.consciousness_contribution, 4)
        }

    def distance_to(self, other: 'FrequencyBit') -> float:
        phase_diff = np.abs(self.phase - other.phase)
        phase_diff = min(phase_diff, 2*np.pi - phase_diff)
        return phase_diff / np.pi + (1.0 - self.resonance_score * other.resonance_score)
