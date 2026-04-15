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

import numpy as np
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional

@dataclass
class GeneticFrequencyBit:
    """
    Bit وراثي-ترددي — الوحدة الأساسية في BetaRoot الجديد
    يربط DNA → تردد → وعي (عبر النباتات)
    """
    id: str
    phase: float                    # طور DNA vibration
    amplitude: float                # كثافة Biophoton / تعبير جيني
    frequency: float                # تردد DNA (مستمد من Schumann + plant resonance)
    resonance_score: float          # توافق مع Schumann 7.83 Hz
    genetic_expression: float       # درجة التعبير الجيني (من النباتات)
    plant_source: str               # نوع الشجرة/النبات
    consciousness_bridge: float = 0.0  # مساهمة في الوعي البشري
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

    def to_unary(self) -> Dict:
        """تحويل إلى تمثيل آحادي (Only 1)"""
        return {
            "type": "genetic_frequency_bit",
            "value": self.phase,                                 # القيمة الآحادية
            "strength": self.amplitude * self.resonance_score * self.genetic_expression,
            "id": self.id,
            "source": self.plant_source,
            "consciousness": round(self.consciousness_bridge, 4)
        }

    def distance_to(self, other: 'GeneticFrequencyBit') -> float:
        """مسافة وراثية-ترددية"""
        phase_diff = min(abs(self.phase - other.phase), 2*np.pi - abs(self.phase - other.phase))
        genetic_diff = abs(self.genetic_expression - other.genetic_expression)
        return (phase_diff / np.pi) + genetic_diff + (1 - self.resonance_score * other.resonance_score)
