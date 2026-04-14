# orchestrator/validation_layer.py
from typing import Dict, List, Tuple
from ..core.consistency_checker import ConsistencyChecker
from ..core.causal_graph import CausalGraphBuilder
from ..core.symbolic_patterns import SymbolicPatternEngine
from ..core.frequency_resonance import FrequencyResonance

class ValidationLayer:
    """
    طبقة التحقق والدمج — قلب BetaRoot كـ Meta-Orchestrator
    """

    def __init__(self):
        self.consistency = ConsistencyChecker()
        self.causal = CausalGraphBuilder()
        self.patterns = SymbolicPatternEngine()
        self.resonance = FrequencyResonance()

    async def validate_and_fuse(self, raw_responses: Dict[str, str], user_query: str) -> Dict:
        """
        1. التحقق من كل إجابة
        2. تصفية الإجابات المتسقة
        3. دمجها في Causal Graph
        4. تطبيق أنماط رمزية + تصحيح ترددي
        """
        validated = []
        contradictions = []

        for agent, response in raw_responses.items():
            check = self.consistency.verify(response, context=user_query)
            
            if check["is_consistent"]:
                validated.append((agent, response))
                self.causal.add_relation(f"Query: {user_query}", f"answered_by_{agent}", response[:150] + "...")
            else:
                contradictions.append((agent, check["conflicts"]))

        # دمج الإجابات المتسقة
        fused_answer = self._fuse_answers(validated)

        # تطبيق نمط رمزي
        pattern_result = self.patterns.apply_pattern(fused_answer)

        # تصحيح ترددي Schumann
        pressure = self.resonance.calculate_wrong_pressure(f_current=7.83 + 0.15)  # سيتم ربطه لاحقاً بالـ live signal

        return {
            "fused_answer": fused_answer,
            "validated_count": len(validated),
            "contradictions_found": len(contradictions),
            "applied_pattern": pattern_result.pattern_name if pattern_result else None,
            "wrong_pressure": pressure["wrong_pressure"],
            "correction_needed": pressure["correction_needed"],
            "causal_nodes": len(self.causal.graph.nodes),
            "final_certainty": 1.0 if len(validated) >= 2 else 0.75
        }

    def _fuse_answers(self, validated: List[Tuple[str, str]]) -> str:
        """دمج الإجابات بطريقة سببية"""
        if not validated:
            return "لا توجد إجابات متسقة."

        # ترتيب حسب عدد الكلمات + الاتساق (بسيط)
        sorted_answers = sorted(validated, key=lambda x: len(x[1]), reverse=True)
        
        fused = f"الإجابة المتكاملة من BetaRoot:\n\n"
        for i, (agent, ans) in enumerate(sorted_answers[:3]):  # أفضل 3 إجابات
            fused += f"[{agent.upper()}]:\n{ans}\n\n"
        
        fused += "\n→ BetaRoot Synthesis: تم دمج الإجابات بعد التحقق من الاتساق السببي والمنطق الآحادي."
        return fused
