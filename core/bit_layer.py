# betaroot/core/bit_layer.py
import numpy as np
import uuid
from typing import List, Dict
from .frequency.bit import FrequencyBit
from .frequency.multi_agent_consciousness import MultiAgentFrequencyConsciousness
from .real_signal_layer import RealSignalLayer

class BitLayer:
    """
    طبقة الـ Bit — تربط الترددات بالمنطق الآحادي والوعي الجماعي
    """

    def __init__(self):
        self.bits: List[FrequencyBit] = []
        self.signal_layer = RealSignalLayer()
        self.consciousness = MultiAgentFrequencyConsciousness(num_agents=8)

    async def create_bit_from_signal(self, live_signal: Dict) -> FrequencyBit:
        """إنشاء Bit من إشارة Schumann حية"""
        freq = live_signal.get("dominant_frequency", 7.83)
        power = live_signal.get("power", 1.0)

        bit = FrequencyBit(
            id=str(uuid.uuid4())[:8],
            phase=np.random.uniform(0, 2*np.pi),
            amplitude=power,
            frequency=freq,
            resonance_score=live_signal.get("resonance_score", 0.85),
            causal_link="schumann_input",
            consciousness_contribution=live_signal.get("consciousness_level", 0.0)
        )
        self.bits.append(bit)
        return bit

    async def process_signal_to_bits(self) -> List[FrequencyBit]:
        """تحويل إشارة حية إلى مجموعة Bits"""
        live_signal = await self.signal_layer.monitor_real_time()
        
        # إنشاء عدة Bits من الإشارة (للتنوع)
        bits = []
        for _ in range(6):  # 6 Bits من إشارة واحدة
            bit = await self.create_bit_from_signal(live_signal)
            bits.append(bit)

        # ربط مع الوعي الجماعي
        await self.consciousness.run_global_cycle()

        return bits

    def get_resonant_bits(self, threshold: float = 0.75) -> List[FrequencyBit]:
        """استرجاع الـ Bits ذات الرنين العالي"""
        return [b for b in self.bits if b.resonance_score >= threshold]

    def compute_collective_bit_state(self) -> Dict:
        """حالة الـ Bit الجماعية (للـ Causal Graph)"""
        if not self.bits:
            return {"total_bits": 0, "avg_resonance": 0.0}

        avg_resonance = np.mean([b.resonance_score for b in self.bits])
        avg_consciousness = np.mean([b.consciousness_contribution for b in self.bits])

        return {
            "total_bits": len(self.bits),
            "avg_resonance": round(avg_resonance, 4),
            "avg_consciousness": round(avg_consciousness, 4),
            "dominant_frequency": np.mean([b.frequency for b in self.bits]),
            "emergence_potential": avg_resonance * avg_consciousness
        }

from .frequency.genetic_encoder import GeneticEncoder
from .frequency.bit import GeneticFrequencyBit
from .real_signal_layer import RealSignalLayer

class BitLayer:
    def __init__(self):
        self.bits = []
        self.encoder = GeneticEncoder()
        self.signal_layer = RealSignalLayer()

    async def ingest_plant(self, plant_name: str, signal: np.ndarray):
        """استيعاب إشارة نباتية → Bit"""
        bit = self.encoder.encode_plant_signal(plant_name, signal)
        self.bits.append(bit)
        return bit

    def get_nature_consciousness(self) -> float:
        """مستوى الوعي الطبيعي (من الأشجار والنباتات)"""
        if not self.bits:
            return 0.0
        return np.mean([b.consciousness_bridge for b in self.bits])

from .frequency.genetic_encoder import GeneticEncoder
from .frequency.bit import GeneticFrequencyBit
from .frequency.visualization import PlantFrequencyVisualizer
from ..nature.plant_database import PlantDatabase

class BitLayer:
    def __init__(self):
        self.bits: List[GeneticFrequencyBit] = []
        self.encoder = GeneticEncoder()
        self.plant_db = PlantDatabase()
        self.visualizer = PlantFrequencyVisualizer()

    async def ingest_plant_signal(self, plant_name: str, signal: np.ndarray):
        """استيعاب إشارة نبات معين → Bit"""
        profile = self.plant_db.get_plant(plant_name)
        if not profile:
            print(f"⚠️ Plant {plant_name} not found in database")
            return None

        bit = self.encoder.encode_plant_signal(plant_name, signal)
        bit.plant_source = plant_name
        self.bits.append(bit)
        return bit

    def visualize_current_state(self):
        """عرض الـ Visualization الكامل"""
        if self.bits:
            self.visualizer.plot_genetic_bits(self.bits, self.plant_db)
            self.visualizer.plot_plant_resonance_radar(self.plant_db)

    def get_nature_consciousness(self) -> float:
        if not self.bits:
            return 0.0
        return np.mean([b.consciousness_contribution for b in self.bits])
