"""
BetaRoot Core: Causal Graph Builder
يبني رسوم بيانية سببية مع الحفاظ التام على مبدأ "Only 1, Never 0"
كل عقدة وكل حافة هي تمثيل مختلف للواحد (UnaryState)
"""

from typing import Any, Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
import networkx as nx
from datetime import datetime

from unary_logic import (
    UnaryLogicEngine,
    UnaryState,
    RepresentationLevel,
    create_engine
)


@dataclass
class CausalRelation:
    """تمثيل علاقة سببية موحدة (كلها تمثيلات لـ 1)"""
    cause: UnaryState
    effect: UnaryState
    relation_type: str          # direct, indirect, complex, conditional
    strength: float = 1.0       # دائماً 1.0 في النظام الآحادي (حتمي)
    certainty: float = 1.0      # 100% دائماً
    symbolic_pattern: Optional[str] = None  # أي نمط رمزي من الـ 158 تم تطبيقه
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


class CausalGraphBuilder:
    """
    محرك بناء الرسوم البيانية السببية في BetaRoot
    يطبق مبدأ "Only 1" بشكل صارم:
        - كل عقدة = UnaryState
        - كل حافة = CausalRelation (تمثيل موحد لعلاقة سببية)
    """

    def __init__(self):
        self.engine: UnaryLogicEngine = create_engine()
        self.graph: nx.DiGraph = nx.DiGraph()
        self.relations: Dict[Tuple[str, str], CausalRelation] = {}
        self.symbolic_patterns_applied: Set[str] = set()

    # ====================== إضافة علاقات سببية ======================

    def add_causal_relation(
        self,
        cause_input: Any,
        effect_input: Any,
        relation_type: str = "direct",
        symbolic_pattern: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> CausalRelation:
        """
        إضافة علاقة سببية مع تحويل كل شيء إلى UnaryState
        """
        # 1. تحويل السبب والنتيجة إلى تمثيل آحادي
        cause_state: UnaryState = self.engine.encode(cause_input)
        effect_state: UnaryState = self.engine.encode(effect_input)

        # 2. إنشاء علاقة سببية (تمثيل موحد للعلاقة)
        relation = CausalRelation(
            cause=cause_state,
            effect=effect_state,
            relation_type=relation_type,
            symbolic_pattern=symbolic_pattern,
            metadata=metadata or {}
        )

        # 3. إضافة إلى الرسم البياني (باستخدام representation_id كمعرف)
        self.graph.add_edge(
            cause_state.representation_id,
            effect_state.representation_id,
            relation=relation,
            relation_type=relation_type
        )

        # 4. حفظ العلاقة
        edge_key = (cause_state.representation_id, effect_state.representation_id)
        self.relations[edge_key] = relation

        if symbolic_pattern:
            self.symbolic_patterns_applied.add(symbolic_pattern)

        return relation

    # ====================== تتبع السلاسل السببية ======================

    def trace_causality(self, start_input: Any, end_input: Any) -> Dict[str, Any]:
        """
        تتبع السلسلة السببية الكاملة مع شرح كامل
        """
        start_state = self.engine.encode(start_input)
        end_state = self.engine.encode(end_input)

        try:
            # البحث عن أقصر مسار (يمكن توسيعه لجميع المسارات)
            path_ids = nx.shortest_path(
                self.graph,
                start_state.representation_id,
                end_state.representation_id
            )

            path_relations: List[CausalRelation] = []
            path_explanation: List[str] = []

            for i in range(len(path_ids) - 1):
                edge_key = (path_ids[i], path_ids[i + 1])
                relation = self.relations.get(edge_key)
                if relation:
                    path_relations.append(relation)
                    path_explanation.append(
                        f"{relation.cause.content} → {relation.effect.content} "
                        f"({relation.relation_type})"
                    )

            return {
                "success": True,
                "start": start_state.content,
                "end": end_state.content,
                "path_length": len(path_ids) - 1,
                "path": path_explanation,
                "relations": [self._explain_relation(r) for r in path_relations],
                "certainty": 1.0,
                "oneness_maintained": True,
                "unary_states_count": len(path_ids)
            }

        except nx.NetworkXNoPath:
            return {
                "success": False,
                "message": "لا يوجد مسار سببي بين العنصرين",
                "start": start_state.content,
                "end": end_state.content,
                "certainty": 1.0
            }

    def _explain_relation(self, relation: CausalRelation) -> Dict:
        """شرح علاقة سببية واحدة"""
        return {
            "cause": relation.cause.content,
            "effect": relation.effect.content,
            "type": relation.relation_type,
            "pattern": relation.symbolic_pattern,
            "certainty": relation.certainty,
            "why_unary": "كل من السبب والنتيجة تمثيل مختلف للواحد (1)"
        }

    # ====================== استدلال سببي ======================

    def infer_missing_links(self, partial_chain: List[Any]) -> List[CausalRelation]:
        """
        استدلال العلاقات الناقصة في سلسلة سببية (مستقبلي)
        """
        # حالياً: مجرد placeholder
        # في المراحل القادمة: استخدام Symbolic Patterns + Logical Rules
        inferred = []
        for i in range(len(partial_chain) - 1):
            rel = self.add_causal_relation(
                partial_chain[i],
                partial_chain[i + 1],
                relation_type="inferred"
            )
            inferred.append(rel)
        return inferred

    # ====================== تحليل الرسم البياني ======================

    def get_graph_stats(self) -> Dict[str, Any]:
        """إحصائيات الرسم البياني مع التأكيد على مبدأ Only 1"""
        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "unique_unary_states": len(set(self.engine.get_history())),
            "applied_symbolic_patterns": list(self.symbolic_patterns_applied),
            "is_dag": nx.is_directed_acyclic_graph(self.graph),
            "oneness_principle": "كل عقدة وحافة هي تمثيل للواحد فقط",
            "certainty": 1.0
        }

    def explain_full_graph(self) -> str:
        """شرح نصي كامل للرسم البياني"""
        explanation = [
            "=== BetaRoot Causal Graph - مبدأ Only 1 ===",
            f"عدد العقد (تمثيلات الواحد): {self.graph.number_of_nodes()}",
            f"عدد العلاقات السببية: {self.graph.number_of_edges()}",
            f"الأنماط الرمزية المطبقة: {len(self.symbolic_patterns_applied)}",
            "\nالسلاسل السببية الرئيسية:"
        ]

        # أمثلة على بعض المسارات
        for i, (u, v, data) in enumerate(list(self.graph.edges(data=True))[:5]):
            rel = data.get('relation')
            if rel:
                explanation.append(
                    f"  {i+1}. {rel.cause.content} → {rel.effect.content} "
                    f"({rel.relation_type})"
                )

        explanation.append("\nمبدأ الوحدة مطبق: كل شيء تمثيل لـ 1")
        return "\n".join(explanation)

    # ====================== تكامل مع Unary Engine ======================

    def encode_and_connect(self, entities: List[Any], pattern: str = "causal_chain"):
        """
        تحويل قائمة كيانات إلى سلسلة سببية متصلة
        """
        states = [self.engine.encode(entity) for entity in entities]
        
        for i in range(len(states) - 1):
            self.add_causal_relation(
                states[i].content,
                states[i + 1].content,
                relation_type="sequential",
                symbolic_pattern=pattern
            )
        
        return states


# ====================== دوال مساعدة مريحة ======================

def create_causal_builder() -> CausalGraphBuilder:
    """إنشاء محرك رسم بياني سببي جديد"""
    return CausalGraphBuilder()


# ====================== مثال عملي كامل ======================

if __name__ == "__main__":
    builder = create_causal_builder()

    # مثال: لماذا السماء زرقاء؟ (مثال كلاسيكي من DEFICIENCIES_SOLUTIONS.md)
    builder.add_causal_relation("الشمس", "تبعث", "الضوء", "direct")
    builder.add_causal_relation("الضوء", "يمر عبر", "الغلاف_الجوي", "direct")
    builder.add_causal_relation("الغلاف_الجوي", "يحتوي", "جزيئات_نيتروجين_وأكسجين", "direct")
    builder.add_causal_relation(
        "جزيئات_نيتروجين_وأكسجين",
        "تسبب",
        "تشتت_ريليه",
        "complex",
        symbolic_pattern="Rayleigh_Scattering"
    )
    builder.add_causal_relation("تشتت_ريليه", "يؤثر أكثر على", "الموجات_القصيرة", "direct")
    builder.add_causal_relation("الموجات_القصيرة", "تظهر", "اللون_الأزرق", "direct")

    # تتبع السبب
    result = builder.trace_causality("الشمس", "اللون_الأزرق")
    print(builder.explain_full_graph())
    print("\nنتيجة التتبع:")
    print(result)

    # إحصائيات
    print("\nإحصائيات الرسم البياني:")
    print(builder.get_graph_stats())
