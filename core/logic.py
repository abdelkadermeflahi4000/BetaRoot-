class LogicRules:
    """
    محرك القواعد المنطقية: يمثل الاستنتاج (Deduction)
    """
    
    # قاعدة البيانات المنطقية (القواعد الثابتة)
    RULES = {
        "water_boiling": 1,  # نتوقع منطقياً أن الماء يغلي عند 100 درجة
        "gravity_acceleration": 1, # نتوقع أن الأجسام تسقط للأسفل
        "electronic_signal": 0 # نتوقع عدم وجود إشارة في حالة السكون
    }

    @staticmethod
    def get_prediction(hypothesis_name):
        """
        يقدم التنبؤ المنطقي الصرف (0 أو 1)
        إذا كانت الفرضية غير موجودة، يفترض النظام الجهل (None)
        """
        return LogicRules.RULES.get(hypothesis_name, None)

    @staticmethod
    def add_rule(name, expected_outcome):
        """إضافة قاعدة منطقية جديدة للنظام"""
        if expected_outcome in [0, 1]:
            LogicRules.RULES[name] = expected_outcome
