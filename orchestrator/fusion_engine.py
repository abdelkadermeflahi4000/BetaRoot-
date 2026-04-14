# orchestrator/fusion_engine.py
from typing import Dict, Any
from ..core.core_engine import BetaRootCoreEngine

class FusionEngine:
    """
    محرك الدمج النهائي + Self-Evolution
    """

    def __init__(self):
        self.core = BetaRootCoreEngine()

    async def fuse_and_evolve(self, validation_result: Dict, user_query: str) -> Dict:
        """
        الدمج النهائي + التطور الذاتي
        """
        # 1. حفظ في الذاكرة
        self.core.memory.store({
            "query": user_query,
            "fused_answer": validation_result["fused_answer"],
            "validated_count": validation_result["validated_count"],
            "pressure": validation_result["wrong_pressure"]
        }, memory_type="EPISODIC", priority="HIGH", source="FusionEngine")

        # 2. Self-Evolution
        if validation_result["correction_needed"]:
            # تعلم ذاتي: خفض معامل التلوث
            self.core.resonance.k_conscious = max(0.05, self.core.resonance.k_conscious - 0.02)
            evolution_type = "frequency_correction"
        else:
            evolution_type = "stable_fusion"

        # 3. إنشاء تقرير التطور
        evolution_report = {
            "cycle": self.core.cycle_count,
            "evolution_type": evolution_type,
            "improvement": "reduced_conscious_contamination" if validation_result["correction_needed"] else "maintained_stability",
            "new_k_conscious": round(self.core.resonance.k_conscious, 3),
            "timestamp": datetime.now().isoformat()
        }

        return {
            "final_answer": validation_result["fused_answer"],
            "meta": validation_result,
            "evolution": evolution_report,
            "recommendation": "استخدم الإجابة بثقة عالية" if validation_result["final_certainty"] > 0.9 else "تحقق يدوياً من المصادر"
        }
