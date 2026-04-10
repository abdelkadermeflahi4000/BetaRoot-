# betaroot/core/learning/delta_updater.py
from ..knowledge.knowledge_base import KnowledgeBase
from ..knowledge.fact_base import FactBase, TruthValue
from typing import Dict

class DeltaUpdater:
    @staticmethod
    def update_cpd_from_observations(bayesian_engine, variable: str, 
                                     new_observations: list[bool], alpha: float = 0.1):
        """
        تحديث تدريجي لجدول الاحتمالات الشرطية باستخدام قاعدة التعلم البايزي البسيط
        P_new = (1-α) * P_old + α * P_empirical
        """
        # ملاحظة: في التطبيق الحقيقي، يُعدّل CPD داخل pgmpy مباشرة
        # هذا نموذج مبسط يوضح الفكرة دون كسر واجهة engine
        emp_prob = sum(new_observations) / len(new_observations)
        old_cpd = bayesian_engine.cpds.get(variable)
        if not old_cpd: raise ValueError(f"CPD for {variable} not found")
        
        # تحديث الوزن التجريبي تدريجياً
        updated_values = []
        for row in old_cpd.values:
            updated_row = [(1-alpha)*p + alpha*emp_prob for p in row]
            updated_values.append(updated_row)
            
        # هنا يمكن استبدال CPD في النموذج إذا لزم الأمر
        print(f"🔄 Updated CPD for '{variable}': empirical weight {alpha} applied.")
        return updated_values
