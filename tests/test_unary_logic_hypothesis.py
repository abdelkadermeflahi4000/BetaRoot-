"""
اختبارات متقدمة لـ UnaryLogicEngine باستخدام Hypothesis
Property-Based Testing + pytest
"""

import pytest
from hypothesis import given, settings, strategies as st, HealthCheck
from hypothesis.stateful import RuleBasedStateMachine, rule, initialize

from betaroot.core.unary_logic import (
    create_engine,
    UnaryLogicEngine,
    UnaryState,
    RepresentationLevel
)


# ====================== استراتيجيات Hypothesis مخصصة لـ BetaRoot ======================

# أي بيانات يمكن أن تكون مدخلاً للنظام
unary_input_strategy = st.one_of(
    st.integers(min_value=-10**9, max_value=10**9),      # أرقام كبيرة
    st.floats(allow_nan=False, allow_infinity=False),    # أرقام عشرية
    st.text(min_size=1, max_size=200),                   # نصوص (عربي/إنجليزي)
    st.booleans(),                                       # True/False
    st.none(),                                           # None (يجب أن يكون تمثيلاً صالحاً)
    st.lists(st.integers(), max_size=15),                # قوائم
    st.dictionaries(st.text(min_size=1, max_size=30), st.integers(), max_size=10),
)


# ====================== Property-Based Tests ======================

class TestUnaryLogicProperties:

    @given(data=unary_input_strategy)
    @settings(max_examples=500, deadline=None, suppress_health_check=[HealthCheck.too_slow])
    def test_encode_produces_valid_unary_state(self, data):
        """كل مدخل → يجب أن ينتج UnaryState صالح يحافظ على Only 1"""
        engine = create_engine()
        state: UnaryState = engine.encode(data)

        # الخصائص الأساسية
        assert isinstance(state, UnaryState)
        assert state.representation_id and len(state.representation_id) >= 8
        assert state.level in list(RepresentationLevel)
        assert state.content is not None or isinstance(data, (type(None), bool))

    @given(data=unary_input_strategy)
    @settings(max_examples=300)
    def test_oneness_and_consistency_always_hold(self, data):
        """مبدأ Only 1: كل حالة يجب أن تكون متسقة 100%"""
        engine = create_engine()
        state = engine.encode(data)
        consistency = engine.verify_consistency(state)

        assert consistency["is_consistent"] is True
        assert consistency["certainty"] == 1.0
        assert "violations" in consistency and len(consistency["violations"]) == 0

    @given(data=unary_input_strategy)
    @settings(max_examples=200)
    def test_identity_transformation_preserves_oneness(self, data):
        """التحويل Identity يجب أن يحافظ على الوحدة تماماً"""
        engine = create_engine()
        original = engine.encode(data)
        transformed = engine.transform(original, "identity")

        assert transformed.representation_id != original.representation_id  # ID جديد
        assert transformed.parent_states[-1] == original                 # يحتفظ بالأصل
        assert transformed.level == original.level


# ====================== Stateful Testing (State Machine) ======================

class UnaryEngineStateMachine(RuleBasedStateMachine):
    """
    اختبار حالات معقد: تسلسل عمليات على UnaryLogicEngine
    """

    def __init__(self):
        super().__init__()
        self.engine = create_engine()
        self.states_created = 0

    @initialize()
    def start_with_empty_engine(self):
        """ابدأ بمحرك فارغ"""
        self.states_created = 0

    @rule(data=unary_input_strategy)
    def encode_new_data(self, data):
        """قاعدة: تشفير بيانات جديدة"""
        state = self.engine.encode(data)
        self.states_created += 1

        assert isinstance(state, UnaryState)
        assert state.representation_id

    @rule()
    @precondition(lambda self: self.states_created >= 2)
    def compose_two_previous_states(self):
        """قاعدة: دمج حالتين سابقاً (Composition)"""
        history = self.engine.get_history()
        if len(history) >= 2:
            state_a = history[-2]
            state_b = history[-1]
            composed = self.engine.compose([state_a, state_b], rule="test_composition")

            assert composed.level == RepresentationLevel.SYMBOLIC
            assert len(composed.parent_states) == 2

    @rule()
    def verify_all_states_consistent(self):
        """فحص اتساق كل الحالات الموجودة"""
        for state in self.engine.get_history():
            consistency = self.engine.verify_consistency(state)
            assert consistency["is_consistent"] is True


# تسجيل State Machine كاختبار pytest
TestUnaryStateMachine = UnaryEngineStateMachine.TestCase


# ====================== اختبار أداء + Hypothesis ======================

@pytest.mark.slow
@given(data=st.lists(unary_input_strategy, min_size=100, max_size=300))
@settings(max_examples=5, deadline=None)
def test_large_batch_encoding_performance(data):
    """اختبار أداء على دفعات كبيرة"""
    engine = create_engine()
    start = time.time()

    states = [engine.encode(item) for item in data]

    duration = time.time() - start
    assert duration < 3.0, f"معالجة {len(data)} مدخل استغرقت {duration:.2f} ثانية (بطيء جداً)"
    assert len(states) == len(data)
    assert all(isinstance(s, UnaryState) for s in states)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--hypothesis-show-statistics", "--tb=short"])
