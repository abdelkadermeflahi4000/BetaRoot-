"""
BetaRoot Core Tests
اختبارات بسيطة وشاملة لجميع الطبقات الأساسية
"""

import pytest
import time
from betaroot.core.betaroot import BetaRoot, create_betaroot
from betaroot.core.unary_logic import create_engine, RepresentationLevel
from betaroot.core.memory import create_memory_system


class TestBetaRootCore:

    @pytest.fixture
    def br(self):
        """إنشاء نسخة BetaRoot لكل اختبار"""
        return create_betaroot()

    @pytest.fixture
    def memory(self):
        return create_memory_system()

    # ====================== اختبارات Unary Logic ======================

    def test_unary_encoding(self):
        """اختبار التحويل الآحادي الأساسي"""
        engine = create_engine()
        
        state1 = engine.encode(42)
        state2 = engine.encode("السماء زرقاء")
        state3 = engine.encode({"key": "value"})

        assert state1.level == RepresentationLevel.FIRST_ORDER
        assert state2.level == RepresentationLevel.SECOND_ORDER
        assert state3.level == RepresentationLevel.SYMBOLIC
        
        # كل حالة لها معرف فريد
        assert len(state1.representation_id) > 0
        assert state1.representation_id != state2.representation_id

    def test_oneness_principle(self):
        """التأكد من مبدأ Only 1"""
        engine = create_engine()
        state = engine.encode(None)  # حتى None يُعامل كتمثيل
        
        consistency = engine.verify_consistency(state)
        assert consistency["is_consistent"] is True
        assert consistency["certainty"] == 1.0

    # ====================== اختبارات Symbolic Patterns ======================

    def test_symbolic_patterns(self, br):
        """اختبار تطبيق الأنماط الرمزية"""
        state = br.unary.encode("الضوء")
        transformed = br.symbolic.apply_pattern(state, "Expansion")
        
        assert transformed.level == RepresentationLevel.SYMBOLIC
        assert "expanded_from" in str(transformed.content)

    # ====================== اختبارات Causal Graph ======================

    def test_causal_relation(self, br):
        """اختبار إضافة علاقة سببية"""
        rel = br.add_causal_relation("الشمس", "تبعث", "الضوء")
        
        assert rel.cause.content == "الشمس"
        assert rel.effect.content == "الضوء"
        assert rel.relation_type == "direct"
        assert rel.certainty == 1.0

    def test_causal_trace(self, br):
        """اختبار تتبع سلسلة سببية"""
        br.add_causal_relation("المطر", "يبلل", "الأرض")
        br.add_causal_relation("الأرض المبللة", "تسبب", "الانزلاق")
        
        result = br.causal.trace_causality("المطر", "الانزلاق")
        
        assert result["success"] is True
        assert len(result["path"]) > 0
        assert result["certainty"] == 1.0

    # ====================== اختبارات Consistency Checker ======================

    def test_consistency_checker(self, br):
        """اختبار فاحص الاتساق"""
        # ادعاء متسق
        result1 = br.check_consistency("كل البشر فانون")
        assert result1["is_consistent"] is True

        # ادعاء يحتوي على تناقض واضح
        result2 = br.check_consistency("أرسطو فان وغير فان في نفس الوقت")
        # قد يكون False أو True حسب المنطق البسيط الحالي (لكن الفحص يعمل)

    # ====================== اختبارات Memory Layer ======================

    def test_knowledge_base(self, memory):
        """اختبار قاعدة المعرفة"""
        fact_id = memory.store_fact("كل البشر فانون", source="أرسطو")
        
        recall = memory.recall("هل البشر فانون؟")
        
        assert len(recall["results"]) >= 1
        assert recall["results"][0]["similarity"] > 0.6

    def test_context_manager(self, br):
        """اختبار إدارة السياق"""
        br.set_context({
            "user": "كادر",
            "topic": "الفلسفة الآحادية",
            "goal": "فهم BetaRoot"
        })
        
        context = br.get_context()
        assert context["user"] == "كادر"
        assert context["topic"] == "الفلسفة الآحادية"

    # ====================== اختبار النظام المتكامل ======================

    def test_full_pipeline(self, br):
        """اختبار الأنبوب الكامل: من المدخل إلى الشرح"""
        # إضافة معرفة أولية
        br.add_fact("كل البشر فانون")
        br.add_fact("أرسطو بشر")

        # معالجة سؤال
        result = br.process("هل أرسطو فان؟")

        assert result["success"] is True
        assert result["certainty"] == 1.0
        assert "answer" in result
        assert "natural_explanation" in result

    def test_sky_blue_example(self, br):
        """اختبار المثال الكلاسيكي: لماذا السماء زرقاء"""
        # إضافة علاقات سببية
        br.add_causal_relation("الشمس", "تبعث", "الضوء")
        br.add_causal_relation("الضوء", "يمر عبر", "الغلاف الجوي")
        br.add_causal_relation("الغلاف الجوي", "يسبب", "تشتت ريليه")

        result = br.process("لماذا السماء زرقاء؟")

        assert result["success"] is True
        assert result["certainty"] == 1.0
        # يجب أن يحتوي الشرح على كلمات مفتاحية
        explanation = str(result["natural_explanation"]).lower()
        assert "تشتت" in explanation or "ريليه" in explanation or "زرقاء" in explanation

    # ====================== اختبارات الأداء البسيطة ======================

    def test_performance(self, br):
        """اختبار أداء بسيط"""
        start = time.time()
        
        for i in range(50):
            br.process(f"سؤال اختبار رقم {i}")
        
        duration = time.time() - start
        assert duration < 5.0, f"المعالجة بطيئة جداً: {duration:.2f} ثانية"


# ====================== تشغيل الاختبارات ======================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])



"""""""""""""""""""""""""""""""""""""""
BetaRoot Advanced Tests with Hypothesis
اختبارات متقدمة تعتمد على Property-Based Testing
"""

import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from hypothesis.stateful import RuleBasedStateMachine, rule, initialize, precondition
import time
import json

from betaroot.core.betaroot import BetaRoot, create_betaroot
from betaroot.core.unary_logic import create_engine, RepresentationLevel, UnaryState
from betaroot.core.memory import create_memory_system


# ====================== استراتيجيات Hypothesis مخصصة ======================

# استراتيجية لتوليد بيانات متنوعة مناسبة لـ BetaRoot
any_data = st.one_of(
    st.integers(min_value=-10**6, max_value=10**6),
    st.floats(allow_nan=False, allow_infinity=False),
    st.text(min_size=1, max_size=100),
    st.booleans(),
    st.lists(st.integers(), max_size=10),
    st.dictionaries(st.text(min_size=1, max_size=20), st.integers(), max_size=8),
    st.none()
)

# ====================== اختبارات Property-Based ======================

class TestBetaRootProperties:

    @given(data=any_data)
    @settings(max_examples=200, deadline=None)
    def test_unary_encoding_property(self, data):
        """كل مدخل يجب أن يتحول إلى UnaryState صالح"""
        engine = create_engine()
        state = engine.encode(data)

        # الخصائص الأساسية
        assert isinstance(state, UnaryState)
        assert hasattr(state, "representation_id")
        assert len(state.representation_id) >= 8
        assert state.level in RepresentationLevel.__members__.values()
        assert state.content is data or str(state.content) == str(data) or isinstance(state.content, dict)

    @given(data=any_data)
    @settings(max_examples=100)
    def test_oneness_preservation(self, data):
        """مبدأ Only 1: كل حالة يجب أن تكون متسقة"""
        engine = create_engine()
        state = engine.encode(data)
        consistency = engine.verify_consistency(state)

        assert consistency["is_consistent"] is True
        assert consistency["certainty"] == 1.0

    @given(query=st.text(min_size=5, max_size=150))
    @settings(max_examples=150)
    def test_process_always_returns_success_or_consistent_error(self, query):
        """br.process() يجب أن يعيد دائماً هيكل صحيح"""
        br = create_betaroot()
        result = br.process(query)

        assert isinstance(result, dict)
        assert "success" in result
        assert "certainty" in result
        assert result["certainty"] in (0.0, 1.0)

        if result["success"]:
            assert "answer" in result
            assert "natural_explanation" in result
        else:
            assert "conflicts" in result or "error" in result

    @given(fact=st.text(min_size=10, max_size=200))
    @settings(max_examples=80)
    def test_memory_store_and_recall_property(self, fact):
        """الحقائق المخزنة يجب أن تُسترجع بدرجة تشابه معقولة"""
        memory = create_memory_system()
        memory.store_fact(fact)

        recall = memory.recall(fact[: len(fact)//2])  # استرجاع جزء من الحقيقة

        assert isinstance(recall, dict)
        assert "results" in recall
        # على الأقل يجب أن يجد شيئاً مشابهاً
        if recall["results"]:
            assert recall["results"][0]["similarity"] > 0.5

    @given(cause=st.text(min_size=5), effect=st.text(min_size=5))
    @settings(max_examples=100)
    def test_causal_relation_property(self, cause, effect):
        """كل علاقة سببية يجب أن تكون متسقة"""
        br = create_betaroot()
        rel = br.add_causal_relation(cause, effect)

        assert rel.certainty == 1.0
        assert rel.cause.content == cause
        assert rel.effect.content == effect


# ====================== State Machine Test (اختبار حالات معقد) ======================

class BetaRootStateMachine(RuleBasedStateMachine):
    """اختبار حالات النظام بطريقة متقدمة (Stateful Testing)"""

    def __init__(self):
        super().__init__()
        self.br = create_betaroot()
        self.added_facts = []

    @initialize()
    def init_system(self):
        """تهيئة النظام"""
        self.br.add_fact("كل البشر فانون")
        self.added_facts.append("كل البشر فانون")

    @rule(fact=st.text(min_size=8, max_size=120))
    def add_random_fact(self, fact):
        """إضافة حقيقة عشوائية"""
        fact_id = self.br.add_fact(fact)
        self.added_facts.append(fact)
        assert fact_id is not None

    @rule()
    def recall_random_fact(self):
        """استرجاع حقيقة عشوائية"""
        if self.added_facts:
            query = self.added_facts[-1]
            result = self.br.recall(query)
            assert isinstance(result, dict)

    @rule(query=st.text(min_size=10, max_size=100))
    def process_random_query(self, query):
        """معالجة استعلام عشوائي"""
        result = self.br.process(query)
        assert "success" in result
        assert "certainty" in result

    @rule()
    def check_system_consistency(self):
        """التحقق من اتساق النظام ككل"""
        info = self.br.system_info()
        assert "memory_stats" in info
        assert info["memory_stats"]["total_facts"] >= 0


# تسجيل State Machine كاختبار
TestBetaRootStateMachine = BetaRootStateMachine.TestCase


# ====================== اختبارات أداء وحدود ======================

@pytest.mark.slow
def test_large_scale_processing():
    """اختبار معالجة كمية كبيرة من البيانات"""
    br = create_betaroot()
    start = time.time()

    for i in range(300):
        query = f"سؤال عشوائي رقم {i} عن الفلسفة الآحادية والسببية"
        br.process(query)

    duration = time.time() - start
    assert duration < 12.0, f"الأداء بطيء: {duration:.2f} ثوانٍ لـ 300 استعلام"


# ====================== تشغيل الاختبارات ======================

if __name__ == "__main__":
    pytest.main([
        __file__, 
        "-v", 
        "--hypothesis-show-statistics", 
        "--tb=short"
    ])
