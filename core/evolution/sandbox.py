# core/evolution/sandbox.py

import copy

class Sandbox:

    def test(self, engine, mutation):
        test_engine = copy.deepcopy(engine)

        try:
            # تطبيق التعديل مؤقتاً
            self.apply_mutation(test_engine, mutation)

            # تشغيل دورات اختبار
            for _ in range(5):
                test_engine.cycle()

            return True

        except Exception:
            return False

    def apply_mutation(self, engine, mutation):
        if mutation["type"] == "threshold_change":
            engine.state.metrics["stability"] *= mutation["value"]
