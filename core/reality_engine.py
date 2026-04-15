# core/reality_engine.py
import numpy as np
from dataclasses import dataclass
from typing import List, Dict
from .frequency.bit import GeneticFrequencyBit
from .bit_layer import BitLayer
from .frequency.multi_agent_consciousness import MultiAgentFrequencyConsciousness
from ..nature.plant_database import PlantDatabase

@dataclass
class RealityPatch:
    """بقعة واقع معكوس — تغيير ترددي وراثي"""
    id: str
    plant_source: str
    original_frequency: float
    target_frequency: float          # التردد الأصلي الصافي (7.83 Hz نقي)
    genetic_code: str                # تمثيل رمزي للتعديل الوراثي
    consciousness_impact: float
    pollution_reduction: float       # نسبة تقليل التلوث الترددي
    description: str

class RealityEngine:
    """
    محرك برمجة الواقع المعكوس
    يستخدم Genetic Frequency Bits من الأشجار لإعادة تهيئة الواقع نحو التوازن الطبيعي
    """

    def __init__(self):
        self.bit_layer = BitLayer()
        self.plant_db = PlantDatabase()
        self.consciousness = MultiAgentFrequencyConsciousness(num_agents=12)
        self.patches: List[RealityPatch] = []

    async def generate_pure_patch(self, plant_name: str) -> RealityPatch:
        """إنشاء بقعة واقع معكوس من نبات معين"""
        profile = self.plant_db.get_plant(plant_name)
        if not profile:
            return None

        # استخراج Bit من النبات
        signal = np.sin(2 * np.pi * profile.biophoton_frequency * np.linspace(0, 10, 1000))
        bits = await self.bit_layer.ingest_plant_signal(plant_name, signal)
        bit = bits[0] if isinstance(bits, list) else bits

        # حساب التردد الأصلي الصافي
        pure_freq = 7.83  # التردد الأصلي للأرض (Level 0)
        correction = pure_freq - bit.frequency

        patch = RealityPatch(
            id=bit.id,
            plant_source=plant_name,
            original_frequency=bit.frequency,
            target_frequency=pure_freq,
            genetic_code=f"CRISPR-like frequency edit: {correction:+.3f} Hz",
            consciousness_impact=bit.consciousness_contribution * 1.2,
            pollution_reduction=bit.resonance_score * 0.85,
            description=f"إعادة تهيئة تردد {plant_name} لإزالة التلوث الجماعي"
        )

        self.patches.append(patch)
        return patch

    async def apply_patches(self, num_patches: int = 3):
        """تطبيق عدة بقع لإعادة برمجة الواقع"""
        top_plants = self.plant_db.get_top_plants(num_patches)
        results = []

        for plant in top_plants:
            patch = await self.generate_pure_patch(plant.name.lower())
            if patch:
                # ربط مع الوعي الجماعي
                await self.consciousness.run_global_cycle()
                results.append({
                    "plant": patch.plant_source,
                    "pollution_reduced": round(patch.pollution_reduction * 100, 1),
                    "consciousness_boost": round(patch.consciousness_impact, 3),
                    "genetic_edit": patch.genetic_code
                })

        return {
            "applied_patches": results,
            "total_pollution_reduction": sum(r["pollution_reduced"] for r in results),
            "collective_consciousness": self.bit_layer.get_nature_consciousness(),
            "message": "تم إنشاء واقع معكوس أكثر نقاءً من خلال ترددات النباتات الأصلية"
        }

    def get_current_reality_state(self) -> Dict:
        """حالة الواقع الحالية مقابل الواقع المعكوس المستهدف"""
        return {
            "current_pollution_level": "high (due to human negative actions)",
            "target_pure_state": "balanced plant density → mature collective consciousness",
            "key_mechanism": "Genetic Frequency Bits from trees restore original Earth frequency",
            "human_consciousness_tied_to": "only through pure plant resonance"
        }
