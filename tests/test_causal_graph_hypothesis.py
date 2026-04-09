"""
اختبارات متقدمة لـ CausalGraphBuilder باستخدام Hypothesis
Property-Based + Stateful Testing
"""

import pytest
from hypothesis import given, settings, strategies as st, HealthCheck
from hypothesis.stateful import RuleBasedStateMachine, rule, initialize, precondition
import networkx as nx

from betaroot.core.causal_graph import CausalGraphBuilder, create_causal_builder
from betaroot.core.unary_logic import create_engine


# ====================== استراتيجيات Hypothesis مخصصة ======================

# استراتيجية لتوليد كيانات سببية (أسماء، مفاهيم، ظواهر)
entity_strategy = st.one_of(
    st.text(min_size=3, max_size=50, alphabet=st.characters(whitelist_categories=["L", "N", "S"])),  # نصوص عربية/إنجليزية
    st.sampled_from([
        "الشمس", "الضوء", "الغلاف_الجوي", "تشتت_ريليه", "اللون_الأزرق",
        "المطر", "الأرض", "الانزلاق", "الجليد", "الماء", "الروابط_الهيدروجينية",
        "أرسطو", "البشر", "الفناء"
    ])
)

relation_type_strategy = st.sampled_from(["direct", "indirect", "complex", "sequential", "conditional"])


# ====================== Property-Based Tests ======================

class TestCausalGraphProperties:

    @given(
        cause=entity_strategy,
        effect=entity_strategy,
        rel_type=relation_type_strategy
    )
    @settings(max_examples=400, deadline=None)
    def test_add_causal_relation_always_valid(self, cause, effect, rel_type):
        """كل علاقة سببية مضافة يجب أن تكون صالحة وتحافظ على certainty=1.0"""
        builder = create_causal_builder()
        
        relation = builder.add_causal_relation(cause, effect, relation_type=rel_type)

        assert relation is not None
        assert relation.cause.content == cause
        assert relation.effect.content == effect
        assert relation.relation_type == rel_type
        assert relation.certainty == 1.0
        assert relation.strength == 1.0

    @given(
        entities=st.lists(entity_strategy, min_size=3, max_size=12, unique=True)
    )
    @settings(max_examples=150)
    def test_build_and_trace_causal_chain(self, entities):
        """بناء سلسلة سببية ثم تتبعها يجب أن ينجح"""
        builder = create_causal_builder()

        # بناء سلسلة سببية متصلة
        for i in range(len(entities) - 1):
            builder.add_causal_relation(
                entities[i], 
                entities[i + 1], 
                relation_type="sequential"
            )

        # تتبع السلسلة من البداية إلى النهاية
        result = builder.trace_causality(entities[0], entities[-1])

        assert result["success"] is True
        assert result["path_length"] == len(entities) - 1
        assert result["certainty"] == 1.0
        assert len(result["path"]) > 0

    @given(entities=st.lists(entity_strategy, min_size=4, max_size=10))
    @settings(max_examples=100)
    def test_graph_is_directed_acyclic_after_sequential_add(self, entities):
        """الرسم البياني بعد إضافة علاقات تسلسلية يجب أن يكون DAG"""
        builder = create_causal_builder()

        for i in range(len(entities) - 1):
            builder.add_causal_relation(entities[i], entities[i + 1])

        stats = builder.get_graph_stats()
        assert stats["is_dag"] is True


# ====================== Stateful Testing (State Machine) ======================

class CausalGraphStateMachine(RuleBasedStateMachine):
    """
    اختبار حالات معقد لـ CausalGraphBuilder
    يحاكي سيناريوهات استخدام حقيقية
    """

    def __init__(self):
        super().__init__()
        self.builder = create_causal_builder()
        self.entities = []
        self.relations_added = 0

    @initialize()
    def setup_empty_graph(self):
        """ابدأ برسوم بيانية فارغة"""
        self.entities = []
        self.relations_added = 0

    @rule(entity=entity_strategy)
    def add_new_entity(self, entity):
        """إضافة كيان جديد (يتم تخزينه لاستخدامه لاحقاً)"""
        if entity not in self.entities:
            self.entities.append(entity)

    @rule()
    @precondition(lambda self: len(self.entities) >= 2)
    def add_random_causal_relation(self):
        """إضافة علاقة سببية عشوائية بين كيانين موجودين"""
        if len(self.entities) < 2:
            return

        # اختيار كيانين مختلفين
        idx1, idx2 = st.integers(min_value=0, max_value=len(self.entities)-1).example(), \
                     st.integers(min_value=0, max_value=len(self.entities)-1).example()
        
        while idx1 == idx2:
            idx2 = st.integers(min_value=0, max_value=len(self.entities)-1).example()

        cause = self.entities[idx1]
        effect = self.entities[idx2]

        rel_type = st.sampled_from(["direct", "indirect", "complex"]).example()

        self.builder.add_causal_relation(cause, effect, relation_type=rel_type)
        self.relations_added += 1

    @rule()
    @precondition(lambda self: len(self.entities) >= 3 and self.relations_added >= 2)
    def trace_random_path(self):
        """تتبع مسار سببي عشوائي"""
        if len(self.entities) < 3:
            return

        start = st.sampled_from(self.entities).example()
        end = st.sampled_from(self.entities).example()

        if start == end:
            return

        result = self.builder.trace_causality(start, end)

        # إما أن يكون هناك مسار أو لا (كلا الحالتين مقبولتان)
        assert isinstance(result, dict)
        assert "success" in result
        assert "certainty" in result and result["certainty"] == 1.0

    @rule()
    def graph_must_be_valid(self):
        """الرسم البياني يجب أن يكون دائماً صالحاً"""
        stats = self.builder.get_graph_stats()
        assert stats["is_dag"] is True
        assert stats["total_nodes"] == len(self.builder.graph.nodes)
        assert stats["oneness_principle"] is not None


# تسجيل State Machine كاختبار
TestCausalGraphStateMachine = CausalGraphStateMachine.TestCase


# ====================== اختبارات أداء وحدود ======================

@pytest.mark.slow
@given(entities=st.lists(entity_strategy, min_size=50, max_size=150, unique=True))
@settings(max_examples=8, deadline=None)
def test_large_causal_graph_performance(entities):
    """اختبار أداء على رسوم بيانية كبيرة"""
    builder = create_causal_builder()
    start_time = time.time()

    # بناء شبكة كبيرة
    for i in range(len(entities) - 1):
        builder.add_causal_relation(entities[i], entities[i + 1], "sequential")

    duration = time.time() - start_time

    stats = builder.get_graph_stats()
    
    assert stats["total_nodes"] == len(entities)
    assert stats["is_dag"] is True
    assert duration < 4.0, f"بناء رسم بياني يحتوي على {len(entities)} عقدة استغرق {duration:.2f} ثانية"


if __name__ == "__main__":
    pytest.main([
        __file__, 
        "-v", 
        "--hypothesis-show-statistics", 
        "--tb=short"
    ])
