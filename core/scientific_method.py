import numpy as np
from prob_engine import BetaAtom # نفترض وجود كلاس الاحتمالات
from logic import LogicRules    # نفترض وجود قواعد المنطق

class ScientificInference:
    def __init__(self):
        self.knowledge_base = {} # وعاء لتخزين "الذرات المنطقية"
        self.threshold = 0.95    # حد اليقين العلمي

    def research_cycle(self, hypothesis_name, evidence_stream):
        """
        دورة البحث العلمي: ملاحظة -> استنتاج -> تحديث
        """
        if hypothesis_name not in self.knowledge_base:
            self.knowledge_base[hypothesis_name] = BetaAtom(hypothesis_name)
        
        node = self.knowledge_base[hypothesis_name]
        
        print(f"--- بدء دورة البحث على: {hypothesis_name} ---")
        
        for i, data_point in enumerate(evidence_stream):
            # 1. التوقع المنطقي (Deduction)
            prediction = LogicRules.get_prediction(hypothesis_name)
            
            # 2. المقارنة بالدليل (Empirical Testing)
            is_consistent = (data_point == prediction)
            
            # 3. تحديث الوعاء الموحد (Bayesian Update)
            node.update(evidence_strength=1, is_consistent=is_consistent)
            
            # 4. إدارة التناقض
            if not is_consistent:
                print(f"ملاحظة {i}: تناقض مكتشف! تحديث الشك في الفرضية.")
            
            # عرض الحالة الراهنة لليقين
            print(f"خطوة {i}: درجة اليقين الحالية = {node.certainty():.4f}")

        # النتيجة النهائية للدورة
        self.evaluate_final_status(node)

    def evaluate_final_status(self, node):
        if node.certainty() > self.threshold:
            print(f"✅ النتيجة: تم تأكيد الفرضية كقانون منطقي (P ~ 1)")
        elif node.certainty() < (1 - self.threshold):
            print(f"❌ النتيجة: تم تفنيد الفرضية منطقياً (P ~ 0)")
        else:
            print(f"⚠️ النتيجة: البيانات غير كافية، اليقين متوسط.")
