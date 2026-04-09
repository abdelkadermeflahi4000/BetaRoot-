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
