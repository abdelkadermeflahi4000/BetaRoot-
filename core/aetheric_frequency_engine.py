# core/aetheric_frequency_engine.py
import numpy as np
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Any
from .frequency.bit import GeneticFrequencyBit
from .bit_layer import BitLayer
from .reality_engine import RealityEngine

@dataclass
class AethericBit:
    """Bit أثيري — ما وراء الكهرومغناطيسية"""
    id: str
    phase: float                    # طور أثيري (غير مرتبط بمجال مغناطيسي)
    amplitude: float                # قوة الهالة / الوعي
    frequency: float                # تردد نقي (مرتبط بالأصل 7.83 Hz)
    aura_resonance: float           # توافق مع هالة الإنسان
    collective_impact: float        # أثر على الوعي الجماعي
    programmable_matter_code: str   # كود مادة قابلة للبرمجة
    reality_layer: str              # "time", "nature", "pollution", "pure"
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

    def to_pure_frequency(self) -> Dict:
        """تمثيل نقي ما وراء EM"""
        return {
            "type": "aetheric_bit",
            "phase_value": self.phase,
            "strength": self.amplitude * self.aura_resonance,
            "collective_consciousness_impact": self.collective_impact,
            "reality_layer": self.reality_layer
        }

class AethericFrequencyEngine:
    """
    محرك الحوسبة ما وراء الكهرومغناطيسية
    يقيس كل شيء من خلال الترددات فقط (الهالة + الوعي + الأثر الأثيري)
    """

    def __init__(self):
        self.bit_layer = BitLayer()
        self.reality = RealityEngine()
        self.aether_bits: List[AethericBit] = []

    async def create_aetheric_bit(self, plant_name: str, human_aura_signal: np.ndarray) -> AethericBit:
        """إنشاء Bit أثيري من نبات + هالة إنسان"""
        # استخراج Bit نباتي
        plant_bit = await self.bit_layer.ingest_plant_signal(plant_name, human_aura_signal)

        # حساب توافق الهالة
        aura_resonance = np.exp(-np.std(human_aura_signal) / 0.3)  # كلما كانت الهالة أكثر استقراراً = أعلى

        bit = AethericBit(
            id=str(uuid.uuid4())[:12],
            phase=plant_bit.phase,
            amplitude=plant_bit.amplitude,
            frequency=plant_bit.frequency,
            aura_resonance=aura_resonance,
            collective_impact=plant_bit.consciousness_contribution * aura_resonance,
            programmable_matter_code=f"freq_{plant_bit.frequency:.3f}_phase_{plant_bit.phase:.3f}",
            reality_layer="pure_nature" if aura_resonance > 0.85 else "polluted"
        )
        self.aether_bits.append(bit)
        return bit

    def measure_human_consciousness(self, aura_signal: np.ndarray) -> Dict:
        """قياس الوعي البشري من خلال الهالة والتردد فقط"""
        # مقاييس داخلية
        stability = 1 / (1 + np.std(aura_signal))
        coherence = np.mean(np.abs(np.fft.fft(aura_signal)[:10])) / np.max(np.abs(np.fft.fft(aura_signal)))
        purity = np.exp(-np.mean(np.abs(aura_signal - 7.83)))  # قرب من التردد الأصلي

        total_consciousness = 0.4 * stability + 0.35 * coherence + 0.25 * purity

        return {
            "total_consciousness_level": round(total_consciousness, 4),
            "stability": round(stability, 4),
            "coherence": round(coherence, 4),
            "purity_from_earth": round(purity, 4),
            "status": "سليم وناضج" if total_consciousness > 0.75 else "متأثر بالتلوث",
            "recommendation": "زيادة التواصل مع الأشجار" if total_consciousness < 0.6 else "الحفاظ على التوازن"
        }

    async def program_reversed_reality(self, target_reality: str = "pure_nature"):
        """برمجة واقع معكوس نقي"""
        patches = []
        for bit in self.aether_bits[-5:]:  # آخر 5 Bits
            patch = await self.reality.generate_pure_patch(bit.plant_source if hasattr(bit, 'plant_source') else "banyan")
            if patch:
                patches.append(patch)

        return {
            "programmed_patches": len(patches),
            "reality_layer": target_reality,
            "message": "تم إدخال واقع معكوس نقي — الوعي الجماعي يعود إلى توازنه الأصلي عبر ترددات النباتات"
        }

    def get_multi_reality_state(self) -> Dict:
        """حالة الواقع المتعدد"""
        return {
            "time_layer": "ترددي (غير خطي)",
            "nature_layer": "متوازنة عندما تكون الكثافة النباتية عالية",
            "pollution_layer": "مرتفعة حالياً بسبب التصرفات السلبية",
            "human_consciousness_tied_to": "الهالة + التردد الأصلي للأرض",
            "programmable_matter": "مادة قابلة للبرمجة عبر Genetic Frequency Bits"
        }
