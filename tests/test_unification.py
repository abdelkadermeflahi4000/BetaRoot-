import unittest
from core.scientific_method import ScientificInference
from core.prob_engine import BetaAtom # نفترض وجود هذا الكلاس في محركك

class TestBetaRootInference(unittest.TestCase):
    
    def setUp(self):
        self.ai = ScientificInference()

    def test_absolute_confirmation(self):
        """ اختبار: هل يصل النظام لليقين الكامل عند تطابق البيانات مع المنطق؟ """
        data = [1, 1, 1, 1, 1]
        self.ai.research_cycle("gravity_acceleration", data)
        node = self.ai.knowledge_base["gravity_acceleration"]
        # نتوقع يقين عالي جداً (أكبر من 0.8)
        self.assertGreater(node.certainty(), 0.8)

    def test_logical_contradiction(self):
        """ اختبار: هل ينهار اليقين عند حدوث تناقض مستمر؟ """
        # المنطق يتوقع 1، لكننا سنعطيه أصفاراً
        contradictory_data = [0, 0, 0, 0, 0]
        self.ai.research_cycle("water_boiling", contradictory_data)
        node = self.ai.knowledge_base["water_boiling"]
        # نتوقع يقين منخفض جداً (أقل من 0.2)
        self.assertLess(node.certainty(), 0.2)

    def test_noise_resilience(self):
        """ اختبار: هل النظام مرن أمام خطأ واحد وسط سلسلة نجاحات؟ """
        data = [1, 1, 0, 1, 1] # صفر واحد (ضجيج) وسط الواحدات
        self.ai.research_cycle("electronic_signal", data)
        node = self.ai.knowledge_base["electronic_signal"]
        # يجب أن يظل اليقين مرتفعاً رغم الخطأ البسيط
        self.assertGreater(node.certainty(), 0.6)

if __name__ == '__main__':
    unittest.main()
