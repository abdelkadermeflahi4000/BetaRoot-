"""
BetaRoot Core: Consistency Checker
فاحص الاتساق الشامل الذي يتحقق من:
- الاتساق الآحادي (Oneness)
- الاتساق السببي
- الاتساق الرمزي
- الاتساق المنطقي العام
ويعيد نتيجة حتمية (certainty = 1.0 أو 0.0)
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from unary_logic import UnaryLogicEngine, UnaryState, RepresentationLevel
from causal_graph import CausalGraphBuilder
from symbolic_patterns import SymbolicPatternsEngine, PatternCategory
from explainability_engine import ExplainabilityEngine, Explanation


@dataclass
class ConsistencyResult:
    """نتيجة فحص الاتساق الكامل"""
    is_consistent: bool
    certainty: float = 1.0
    conflicts: List[Dict[str, Any]] = field(default_factory=list)
    checks_performed: List[str] = field(default_factory=list)
    violated_principles: List[str] = field(default_factory=list)
    recommendation: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    explanation: Optional[Explanation] = None


class ConsistencyChecker:
    """
    فاحص الاتساق الرئيسي في BetaRoot
    يطبق مبدأ "Only 1" على مستوى النظام ككل
    """

    def __init__(self):
        self.unary_engine: UnaryLogicEngine = UnaryLogicEngine()
        self.symbolic_engine: SymbolicPatternsEngine = SymbolicPatternsEngine()
        self.causal_builder: CausalGraphBuilder = CausalGraphBuilder()
        self.explain_engine: ExplainabilityEngine = ExplainabilityEngine()

    def verify(self, claim: Any, context: Optional[Dict[str, Any]] = None) -> ConsistencyResult:
        """
        الدالة الرئيسية: التحقق من اتساق أي ادعاء أو مدخل
        """
        conflicts = []
        checks = []

        # 1. فحص الاتساق الآحادي (Oneness Check)
        unary_result = self._check_unary_consistency(claim)
        checks.append("unary_oneness")
        if not unary_result["consistent"]:
            conflicts.append({
                "type": "unary_violation",
                "description": "انتهاك مبدأ Only 1",
                "details": unary_result["details"]
            })

        # 2. فحص الاتساق السببي (Causal Consistency)
        causal_result = self._check_causal_consistency(claim, context)
        checks.append("causal_consistency")
        if not causal_result["consistent"]:
            conflicts.extend(causal_result["conflicts"])

        # 3. فحص الاتساق الرمزي (Symbolic Pattern Consistency)
        symbolic_result = self._check_symbolic_consistency(claim, context)
        checks.append("symbolic_consistency")
        if not symbolic_result["consistent"]:
            conflicts.extend(symbolic_result["conflicts"])

        # 4. فحص الاتساق المنطقي العام (Logical Consistency)
        logical_result = self._check_logical_consistency(claim, context)
        checks.append("logical_consistency")
        if not logical_result["consistent"]:
            conflicts.extend(logical_result["conflicts"])

        # 5. توليد النتيجة النهائية
        is_consistent = len(conflicts) == 0
        certainty = 1.0 if is_consistent else 0.0

        recommendation = None
        if not is_consistent:
            recommendation = self._generate_recommendation(conflicts)

        # إنشاء شرح تفسيري (اختياري)
        explanation = None
        if context and context.get("generate_explanation", False):
            explanation = self.explain_engine.explain(
                question=f"التحقق من اتساق: {claim}",
                input_data=claim,
                target_pattern=context.get("pattern"),
                causal_entities=context.get("entities")
            )

        result = ConsistencyResult(
            is_consistent=is_consistent,
            certainty=certainty,
            conflicts=conflicts,
            checks_performed=checks,
            violated_principles=[c["type"] for c in conflicts],
            recommendation=recommendation,
            explanation=explanation
        )

        return result

    # ====================== الفحوصات الداخلية ======================

    def _check_unary_consistency(self, claim: Any) -> Dict:
        """فحص الاتساق مع مبدأ Only 1"""
        try:
            state: UnaryState = self.unary_engine.encode(claim)
            consistency = self.unary_engine.verify_consistency(state)

            return {
                "consistent": consistency["is_consistent"],
                "details": {
                    "representation_id": state.representation_id,
                    "level": state.level.name,
                    "violations": consistency.get("violations", [])
                }
            }
        except Exception as e:
            return {
                "consistent": False,
                "details": {"error": str(e)}
            }

    def _check_causal_consistency(self, claim: Any, context: Optional[Dict] = None) -> Dict:
        """فحص الاتساق السببي"""
        conflicts = []
        if not context or "entities" not in context:
            return {"consistent": True, "conflicts": []}

        entities = context["entities"]
        if len(entities) < 2:
            return {"consistent": True, "conflicts": []}

        try:
            # محاولة بناء سلسلة سببية
            for i in range(len(entities) - 1):
                self.causal_builder.add_causal_relation(
                    entities[i], entities[i + 1], relation_type="sequential"
                )

            trace = self.causal_builder.trace_causality(entities[0], entities[-1])
            if not trace.get("success"):
                conflicts.append({
                    "type": "causal_disconnection",
                    "description": "انقطاع في السلسلة السببية",
                    "entities": entities
                })

            # فحص وجود دورات (يجب أن يكون DAG في معظم الحالات)
            if not self.causal_builder.graph.number_of_nodes() == 0:
                if not nx.is_directed_acyclic_graph(self.causal_builder.graph):
                    conflicts.append({
                        "type": "causal_cycle",
                        "description": "وجود دورة سببية غير منطقية"
                    })

        except Exception as e:
            conflicts.append({"type": "causal_error", "details": str(e)})

        return {"consistent": len(conflicts) == 0, "conflicts": conflicts}

    def _check_symbolic_consistency(self, claim: Any, context: Optional[Dict] = None) -> Dict:
        """فحص الاتساق مع الأنماط الرمزية"""
        conflicts = []
        if not context or "pattern" not in context:
            return {"consistent": True, "conflicts": []}

        pattern_name = context["pattern"]
        try:
            state = self.unary_engine.encode(claim)
            transformed = self.symbolic_engine.apply_pattern(state, pattern_name)

            # التحقق من أن التحويل حافظ على مستوى أعلى أو مساوٍ
            if transformed.level.value < state.level.value:
                conflicts.append({
                    "type": "symbolic_downgrade",
                    "description": f"النمط {pattern_name} خفض مستوى التمثيل"
                })

        except ValueError as e:
            conflicts.append({
                "type": "unknown_pattern",
                "description": str(e)
            })
        except Exception as e:
            conflicts.append({"type": "symbolic_error", "details": str(e)})

        return {"consistent": len(conflicts) == 0, "conflicts": conflicts}

    def _check_logical_consistency(self, claim: Any, context: Optional[Dict] = None) -> Dict:
        """فحص الاتساق المنطقي العام (مثال بسيط حالياً)"""
        conflicts = []

        # مثال: التحقق من تناقضات واضحة (يمكن توسيعها)
        if isinstance(claim, str):
            if "كل" in claim and "لا شيء" in claim and "فان" in claim:
                conflicts.append({
                    "type": "logical_contradiction",
                    "description": "تناقض منطقي محتمل في الصياغة"
                })

        return {"consistent": len(conflicts) == 0, "conflicts": conflicts}

    def _generate_recommendation(self, conflicts: List[Dict]) -> str:
        """توليد توصية لإصلاح التناقضات"""
        if any(c["type"] == "unary_violation" for c in conflicts):
            return "أعد صياغة الادعاء كتمثيل آحادي موحد (تجنب الثنائيات المطلقة)"
        if any(c["type"] == "causal_disconnection" for c in conflicts):
            return "أضف روابط سببية وسيطة لربط السلسلة"
        if any(c["type"] == "causal_cycle" for c in conflicts):
            return "أزل الدورات السببية غير المنطقية"
        return "راجع الادعاء وأعد التحقق باستخدام أنماط رمزية واضحة"

    # ====================== واجهات إضافية ======================

    def verify_with_explanation(self, claim: Any, context: Optional[Dict] = None) -> Dict[str, Any]:
        """فحص الاتساق + إنتاج شرح كامل"""
        result = self.verify(claim, context)
        
        full_response = {
            "is_consistent": result.is_consistent,
            "certainty": result.certainty,
            "conflicts_count": len(result.conflicts),
            "conflicts": result.conflicts,
            "recommendation": result.recommendation,
            "checks_performed": result.checks_performed
        }

        if result.explanation:
            full_response["natural_explanation"] = self.explain_engine.explain_in_natural_language(
                result.explanation
            )

        return full_response

    def batch_verify(self, claims: List[Any]) -> List[ConsistencyResult]:
        """التحقق من مجموعة من الادعاءات"""
        return [self.verify(claim) for claim in claims]


# ====================== دالة مساعدة ======================

def create_consistency_checker() -> ConsistencyChecker:
    """إنشاء فاحص الاتساق"""
    return ConsistencyChecker()


# ====================== مثال تشغيلي كامل ======================

if __name__ == "__main__":
    checker = create_consistency_checker()

    print("=== اختبار ConsistencyChecker مع الطبقات الأربع ===\n")

    # مثال 1: ادعاء متسق (السماء الزرقاء)
    context1 = {
        "entities": ["الشمس", "الضوء", "الغلاف_الجوي", "تشتت_ريليه", "اللون_الأزرق"],
        "pattern": "Rayleigh_Scattering",
        "generate_explanation": True
    }

    result1 = checker.verify_with_explanation("السماء زرقاء بسبب تشتت ريليه", context1)
    print("نتيجة فحص السماء الزرقاء:")
    print(f"متسق: {result1['is_consistent']}")
    print(f"الثقة: {result1['certainty']}")
    print(f"عدد التناقضات: {result1['conflicts_count']}")

    print("\n" + "="*70 + "\n")

    # مثال 2: ادعاء يحتوي على تناقض محتمل
    context2 = {
        "entities": ["كل البشر فانون", "أرسطو خالد"],
        "pattern": "Direct_Causation"
    }

    result2 = checker.verify("أرسطو فان وغير فان في نفس الوقت", context2)
    print("نتيجة فحص ادعاء متناقض:")
    print(f"متسق: {result2.is_consistent}")
    print(f"التناقضات: {[c['type'] for c in result2.conflicts]}")
    if result2.recommendation:
        print(f"التوصية: {result2.recommendation}")
