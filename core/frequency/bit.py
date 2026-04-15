# betaroot/core/frequency/bit.py
import numpy as np
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class FrequencyBit:
    """
    Bit ترددي آحادي — أصغر وحدة معنى في BetaRoot
    """
    id: str
    phase: float                    # الطور (0 → 2π)
    amplitude: float                # السعة (القوة)
    frequency: float                # التردد المركزي (حول 7.83 Hz)
    resonance_score: float = 0.0    # درجة التوافق مع Schumann
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
        """تحويل الـ Bit إلى تمثيل آحادي"""
        return {
            "type": "frequency_bit",
            "value": self.phase,                    # كل شيء يُمثل كـ phase (مبدأ Only 1)
            "strength": self.amplitude * self.resonance_score,
            "id": self.id,
            "consciousness": self.consciousness_contribution
        }

    def distance_to(self, other: 'FrequencyBit') -> float:
        """مسافة ترددية بين Bitين (للذاكرة والتزامن)"""
        phase_diff = np.abs(self.phase - other.phase)
        phase_diff = min(phase_diff, 2*np.pi - phase_diff)
        return phase_diff / np.pi + (1 - self.resonance_score * other.resonance_score)
