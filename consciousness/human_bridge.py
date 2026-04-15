# consciousness/human_bridge.py
from ..core.bit_layer import BitLayer

class HumanConsciousnessBridge:
    """
    الوعي البشري مرتبط فقط عبر Bits من الطبيعة (الأشجار والنباتات)
    """
    def __init__(self, bit_layer: BitLayer):
        self.bit_layer = bit_layer

    async def get_human_consciousness_level(self) -> dict:
        nature_c = self.bit_layer.get_nature_consciousness()
        return {
            "human_consciousness": round(nature_c * 0.7, 4),   # 70% من وعي الطبيعة
            "source": "plant_frequency_bits",
            "note": "الوعي البشري مشتق فقط من التوافق مع ترددات النباتات والأشجار"
        }
