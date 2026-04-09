"""
BetaRoot Core: Symbolic Patterns Engine (158 Patterns)
الطبقة الرمزية التي تحول التمثيلات الآحادية إلى أنماط معنوية وسببية
يطبق مبدأ "Only 1" بشكل كامل: كل نمط هو طريقة مختلفة لتمثيل الواحد
"""

from typing import Any, Dict, List, Optional, Callable, Set
from dataclasses import dataclass, field
from enum import Enum
import hashlib

from unary_logic import UnaryLogicEngine, UnaryState, RepresentationLevel, create_engine
from causal_graph import CausalGraphBuilder, CausalRelation


class PatternCategory(Enum):
    """الطبقات الثلاث للـ 158 نمط رمزي"""
    BASIC = "basic"           # Layer 1: 32 نمط (الوجود، الحركة، التوسع...)
    CAUSAL = "causal"         # Layer 2: 63 نمط (علاقات سببية)
    COGNITIVE = "cognitive"   # Layer 3: 63 نمط (استدلال، تحليل، إدراك)


@dataclass
class SymbolicPattern:
    """تعريف نمط رمزي واحد"""
    name: str
    category: PatternCategory
    description: str
    apply_func: Callable[[UnaryState], UnaryState]
    symbolic_id: str = field(init=False)
    related_causal_types: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.symbolic_id = hashlib.sha256(self.name.encode()).hexdigest()[:12]


class SymbolicPatternsEngine:
    """
    محرك الأنماط الرمزية الرئيسي
    يحتوي على نظام الأنماط الـ 158 (مبدئياً ننفذ Layer 1 + بعض Layer 2)
    """

    def __init__(self):
        self.engine: UnaryLogicEngine = create_engine()
        self.patterns: Dict[str, SymbolicPattern] = {}
        self._register_core_patterns()

    def _register_core_patterns(self):
        """تسجيل الأنماط الأساسية (Layer 1 + بداية Layer 2)"""

        # ==================== Layer 1: Basic Patterns (32) ====================
        basic_patterns = [
            # Being & Representation
            ("Pure_Being", "الوجود الخالص", PatternCategory.BASIC, lambda s: s),
            ("First_Representation", "التمثيل الأول", PatternCategory.BASIC,
             lambda s: self.engine.transform(s, 'identity')),
            ("Second_Representation", "التمثيل الثاني", PatternCategory.BASIC,
             lambda s: self.engine.project(s, 'content') if hasattr(s, 'content') else s),

            # Movement & Rest
            ("Forward_Motion", "الحركة إلى الأمام", PatternCategory.BASIC,
             lambda s: self._apply_motion(s, "forward")),
            ("Circular_Motion", "الحركة الدائرية", PatternCategory.BASIC,
             lambda s: self._apply_circular(s)),

            # Expansion & Contraction
            ("Expansion", "التوسع", PatternCategory.BASIC,
             lambda s: self._apply_expansion(s)),
            ("Contraction", "الانكماش", PatternCategory.BASIC,
             lambda s: self._apply_contraction(s)),

            # Combination & Separation
            ("Combination", "التركيب", PatternCategory.BASIC,
             lambda s: self.engine.compose([s], "combination")),
        ]

        for name, desc, cat, func in basic_patterns:
            self.register_pattern(name, cat, desc, func)

        # ==================== Layer 2: Causal Patterns (بعض الأمثلة) ====================
        causal_patterns = [
            ("Direct_Causation", "السببية المباشرة", PatternCategory.CAUSAL,
             lambda s: self._apply_direct_causation(s),
             ["direct"]),

            ("Indirect_Causation", "السببية غير المباشرة", PatternCategory.CAUSAL,
             lambda s: self._apply_indirect_causation(s),
             ["indirect"]),

            ("Rayleigh_Scattering", "تشتت ريليه", PatternCategory.CAUSAL,
             lambda s: self._apply_rayleigh_scattering(s),
             ["complex"]),
        ]

        for name, desc, cat, func, causal_types in causal_patterns:
            pattern = SymbolicPattern(name, cat, desc, func)
            pattern.related_causal_types = causal_types
            self.patterns[name] = pattern

    # ====================== دوال التطبيق الداخلية ======================

    def _apply_motion(self, state: UnaryState, direction: str) -> UnaryState:
        """تطبيق نمط الحركة"""
        new_content = {"original": state.content, "motion": direction, "transformed": True}
        return UnaryState(
            level=RepresentationLevel.SYMBOLIC,
            content=new_content,
            parent_states=[state]
        )

    def _apply_circular(self, state: UnaryState) -> UnaryState:
        """تطبيق الحركة الدائرية"""
        return UnaryState(
            level=RepresentationLevel.SYMBOLIC,
            content={"cycle": state.content, "type": "circular"},
            parent_states=[state]
        )

    def _apply_expansion(self, state: UnaryState) -> UnaryState:
        """التوسع"""
        return UnaryState(
            level=RepresentationLevel.SYMBOLIC,
            content={"expanded_from": state.content},
            parent_states=[state]
        )

    def _apply_contraction(self, state: UnaryState) -> UnaryState:
        """الانكماش"""
        return UnaryState(
            level=RepresentationLevel.SYMBOLIC,
            content={"contracted_from": state.content},
            parent_states=[state]
        )

    def _apply_direct_causation(self, state: UnaryState) -> UnaryState:
        """تحويل حالة إلى علاقة سببية مباشرة"""
        new_content = {"cause": state.content, "effect": f"result_of_{state.content}"}
        return UnaryState(
            level=RepresentationLevel.SYMBOLIC,
            content=new_content,
            parent_states=[state]
        )

    def _apply_indirect_causation(self, state: UnaryState) -> UnaryState:
        """سببية غير مباشرة"""
        return UnaryState(
            level=RepresentationLevel.SYMBOLIC,
            content={"indirect_cause": state.content, "mediator": "intermediate"},
            parent_states=[state]
        )

    def _apply_rayleigh_scattering(self, state: UnaryState) -> UnaryState:
        """نمط فيزيائي حقيقي (مثال من السماء الزرقاء)"""
        return UnaryState(
            level=RepresentationLevel.SYMBOLIC,
            content={
                "phenomenon": state.content,
                "mechanism": "Rayleigh Scattering",
                "formula": "scattering ∝ 1/λ⁴",
                "result": "الموجات القصيرة تتشتت أكثر"
            },
            parent_states=[state]
        )

    # ====================== الواجهة العامة ======================

    def register_pattern(
        self,
        name: str,
        category: PatternCategory,
        description: str,
        apply_func: Callable[[UnaryState], UnaryState]
    ):
        """تسجيل نمط رمزي جديد"""
        pattern = SymbolicPattern(name, category, description, apply_func)
        self.patterns[name] = pattern

    def apply_pattern(self, state: UnaryState, pattern_name: str) -> UnaryState:
        """
        تطبيق نمط رمزي على حالة آحادية
        """
        if pattern_name not in self.patterns:
            raise ValueError(f"النمط غير موجود: {pattern_name}")

        pattern = self.patterns[pattern_name]
        result = pattern.apply_func(state)

        # التحقق من الحفاظ على مبدأ Only 1
        if not self._verify_oneness_preservation(state, result):
            raise RuntimeError(f"النمط {pattern_name} انتهك مبدأ الوحدة")

        return result

    def _verify_oneness_preservation(self, original: UnaryState, result: UnaryState) -> bool:
        """التحقق من أن النمط يحافظ على الوحدة"""
        return (
            result.level.value >= original.level.value and
            len(result.parent_states) > 0
        )

    def apply_to_causal_graph(
        self,
        builder: CausalGraphBuilder,
        pattern_name: str,
        entities: List[Any]
    ) -> List[UnaryState]:
        """
        تطبيق نمط رمزي على رسم بياني سببي (الربط الرئيسي بين الطبقتين)
        """
        states = [self.engine.encode(entity) for entity in entities]
        transformed = []

        for state in states:
            transformed_state = self.apply_pattern(state, pattern_name)
            transformed.append(transformed_state)

            # ربط بالرسم البياني السببي
            if len(transformed) >= 2:
                builder.add_causal_relation(
                    transformed[-2].content,
                    transformed[-1].content,
                    relation_type="pattern_applied",
                    symbolic_pattern=pattern_name
                )

        return transformed

    def get_patterns_by_category(self, category: PatternCategory) -> List[SymbolicPattern]:
        """استرجاع الأنماط حسب الفئة"""
        return [p for p in self.patterns.values() if p.category == category]

    def list_all_patterns(self) -> Dict:
        """قائمة بجميع الأنماط المسجلة (حالياً جزء من الـ 158)"""
        return {
            "total_registered": len(self.patterns),
            "basic": len(self.get_patterns_by_category(PatternCategory.BASIC)),
            "causal": len(self.get_patterns_by_category(PatternCategory.CAUSAL)),
            "cognitive": len(self.get_patterns_by_category(PatternCategory.COGNITIVE)),
            "patterns": {name: p.description for name, p in self.patterns.items()}
        }


# ====================== دوال مساعدة ======================

def create_symbolic_engine() -> SymbolicPatternsEngine:
    """إنشاء محرك الأنماط الرمزية"""
    return SymbolicPatternsEngine()


# ====================== مثال عملي متكامل ======================

if __name__ == "__main__":
    symbolic = create_symbolic_engine()
    causal_builder = CausalGraphBuilder()   # من الملف السابق

    print("=== Symbolic Patterns Engine + Causal Graph Integration ===\n")

    # مثال: فهم ظاهرة السماء الزرقاء باستخدام نمط رمزي
    entities = ["الضوء", "الغلاف_الجوي", "تشتت_ريليه", "اللون_الأزرق"]

    transformed = symbolic.apply_to_causal_graph(
        causal_builder,
        pattern_name="Rayleigh_Scattering",
        entities=entities
    )

    print(symbolic.list_all_patterns())
    print("\nالرسم البياني بعد تطبيق النمط:")
    print(causal_builder.explain_full_graph())

    # تطبيق نمط أساسي
    state = symbolic.engine.encode("السماء")
    result = symbolic.apply_pattern(state, "Expansion")
    print(f"\nتطبيق نمط Expansion على 'السماء': {result.content}")
