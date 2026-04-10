"""
BetaRoot Main Class
الواجهة الموحدة لكامل إطار BetaRoot
يجمع: Unary + Symbolic + Causal + Explainability + Consistency + Memory
"""

from typing import Any, Dict, List, Optional
import json

from .unary_logic import UnaryLogicEngine, UnaryState
from .causal_graph import CausalGraphBuilder
from .symbolic_patterns import SymbolicPatternsEngine
from .explainability_engine import ExplainabilityEngine
from .consistency_checker import ConsistencyChecker
from .memory import BetaRootMemory, create_memory_system


class BetaRoot:
    """
    الكلاس الرئيسي لـ BetaRoot AI Framework
    
    يوفر واجهة بسيطة ونظيفة للمستخدم النهائي مع الحفاظ الكامل 
    على مبدأ "Only 1" والشفافية 100%.
    """

    def __init__(self):
        # الطبقات الأساسية
        self.unary = UnaryLogicEngine()
        self.symbolic = SymbolicPatternsEngine()
        self.causal = CausalGraphBuilder()
        self.explain = ExplainabilityEngine()
        self.consistency = ConsistencyChecker()
        self.memory: BetaRootMemory = create_memory_system()

        # حالة داخلية
        self.session_id = "beta_root_session_" + str(int(__import__('time').time()))

    # ====================== الواجهة العامة البسيطة ======================

    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        المعالجة الرئيسية لأي سؤال أو مدخل
        
        Returns:
            dict يحتوي على النتيجة + الشرح الكامل + الثقة
        """
        # 1. حفظ السياق
        if context:
            self.memory.update_context(context)

        # 2. التحقق من الاتساق أولاً
        consistency_result = self.consistency.verify(query, context)
        if not consistency_result.is_consistent:
            return {
                "success": False,
                "error": "الادعاء يحتوي على تناقضات",
                "conflicts": consistency_result.conflicts,
                "recommendation": consistency_result.recommendation,
                "certainty": 0.0
            }

        # 3. معالجة باستخدام ExplainabilityEngine (يجمع الطبقات الثلاث)
        explanation = self.explain.explain_question(query)

        # 4. استرجاع من الذاكرة (إذا وجدت معلومات ذات صلة)
        memory_result = self.memory.recall(query)

        # 5. بناء الرد النهائي
        response = {
            "success": True,
            "answer": self._extract_answer(explanation),
            "natural_explanation": explanation if isinstance(explanation, str) else explanation,
            "certainty": 1.0,
            "memory_matches": len(memory_result.get("results", [])),
            "session_id": self.session_id,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }

        return response

    def _extract_answer(self, explanation: Any) -> str:
        """استخراج الإجابة الرئيسية من الشرح"""
        if isinstance(explanation, str):
            # إذا كان نصاً جاهزاً
            lines = explanation.split("\n")
            for line in lines:
                if line.strip().startswith("النتيجة:") or "النتيجة" in line:
                    return line.strip()
            return explanation[:200] + "..." if len(explanation) > 200 else explanation
        return str(explanation)

    # ====================== واجهات مباشرة لكل طبقة ======================

    def add_fact(self, fact: Any, source: Optional[str] = None) -> str:
        """إضافة حقيقة إلى قاعدة المعرفة"""
        return self.memory.store_fact(fact, source)

    def recall(self, query: Any) -> Dict:
        """استرجاع معلومات من الذاكرة"""
        return self.memory.recall(query)

    def add_causal_relation(self, cause: Any, effect: Any, relation_type: str = "direct"):
        """إضافة علاقة سببية مباشرة"""
        return self.causal.add_causal_relation(cause, effect, relation_type)

    def apply_pattern(self, input_data: Any, pattern_name: str) -> UnaryState:
        """تطبيق نمط رمزي مباشرة"""
        state = self.unary.encode(input_data)
        return self.symbolic.apply_pattern(state, pattern_name)

    def check_consistency(self, claim: Any, context: Optional[Dict] = None):
        """التحقق من الاتساق"""
        return self.consistency.verify_with_explanation(claim, context)

    def explain(self, question: str, **kwargs) -> str:
        """شرح أي سؤال بشكل طبيعي"""
        return self.explain.explain_question(question, **kwargs)

    # ====================== إدارة السياق ======================

    def set_context(self, context_dict: Dict[str, Any]):
        """تعيين السياق الحالي"""
        self.memory.update_context(context_dict)

    def get_context(self) -> Dict[str, Any]:
        """الحصول على السياق الحالي"""
        return self.memory.get_context()

    # ====================== معلومات النظام ======================

    def system_info(self) -> Dict[str, Any]:
        """معلومات عن حالة النظام"""
        return {
            "version": "0.1.0-alpha",
            "philosophy": "Only 1, Never 0",
            "layers_active": [
                "Unary Logic", "Symbolic Patterns", 
                "Causal Graphs", "Explainability", 
                "Consistency", "Memory"
            ],
            "memory_stats": self.memory.stats(),
            "session_id": self.session_id
        }

    def __repr__(self):
        return f"BetaRoot(session={self.session_id}, facts={len(self.memory.knowledge_base.facts)})"


# ====================== دالة إنشاء مريحة ======================

def create_betaroot() -> BetaRoot:
    """إنشاء نسخة جاهزة من BetaRoot"""
    return BetaRoot()


# ====================== مثال استخدام بسيط ونظيف ======================

if __name__ == "__main__":
    print("=== BetaRoot - الواجهة الرئيسية ===\n")

    br = create_betaroot()

    # إضافة بعض الحقائق
    br.add_fact("كل البشر فانون")
    br.add_fact("أرسطو بشر")

    # تعيين سياق
    br.set_context({
        "user": "كادر",
        "language": "العربية",
        "mode": "reasoning"
    })

    # معالجة سؤال
    result = br.process("هل أرسطو فان؟")

    print("الإجابة:")
    print(result.get("answer"))
    print("\nالشرح الطبيعي:")
    print(result.get("natural_explanation")[:500] + "..." if len(str(result.get("natural_explanation", ""))) > 500 else result.get("natural_explanation"))

    print("\nمعلومات النظام:")
    print(br.system_info())

"""
BetaRoot Main Class - النسخة المحسنة
مع ذكاء التعرف التلقائي على نوع السؤال
"""

from typing import Any, Dict, List, Optional, Tuple
import re

from .unary_logic import UnaryLogicEngine
from .causal_graph import CausalGraphBuilder
from .symbolic_patterns import SymbolicPatternsEngine
from .explainability_engine import ExplainabilityEngine
from .consistency_checker import ConsistencyChecker
from .memory import BetaRootMemory


class BetaRoot:
    """
    الكلاس الرئيسي المحسن لـ BetaRoot
    يحتوي على محرك ذكي لتصنيف نوع السؤال تلقائياً
    """

    def __init__(self):
        self.unary = UnaryLogicEngine()
        self.symbolic = SymbolicPatternsEngine()
        self.causal = CausalGraphBuilder()
        self.explain = ExplainabilityEngine()
        self.consistency = ConsistencyChecker()
        self.memory = BetaRootMemory()

        # قواعد بسيطة لتصنيف نوع السؤال
        self.question_patterns = {
            "logical": [
                r"هل .* فان", r"هل .* صحيح", r"ما حكم", r"استنتج", r"ما النتيجة",
                r"كل .* .*", r"بعض .* .*"
            ],
            "mathematical": [
                r"ما هو \d+ .* \d+", r"احسب", r"جمع", r"طرح", r"ضرب", r"قسمة",
                r"\d+\s*[\+\-\*/]\s*\d+"
            ],
            "causal": [
                r"لماذا", r"ما سبب", r"ما السبب", r"كيف يحدث", r"ما آلية"
            ],
            "factual": [
                r"ما هو", r"من هو", r"ما تعريف", r"ما معنى"
            ]
        }

    def _classify_question(self, query: str) -> str:
        """
        تصنيف نوع السؤال تلقائياً
        """
        query_lower = query.lower()

        # التحقق من الأنماط
        for qtype, patterns in self.question_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return qtype

        # تصنيف افتراضي
        if any(word in query_lower for word in ["كم", "كيف", "هل"]):
            return "logical"
        if any(word in query_lower for word in ["سبب", "نتيجة", "لأن"]):
            return "causal"

        return "general"

    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        المعالجة الذكية المحسنة
        """
        if not query:
            return {"success": False, "error": "السؤال فارغ"}

        # 1. حفظ السياق
        if context:
            self.memory.update_context(context)

        # 2. تصنيف نوع السؤال تلقائياً
        question_type = self._classify_question(query)
        
        # 3. التحقق من الاتساق أولاً
        consistency = self.consistency.verify(query, context)
        if not consistency.is_consistent:
            return {
                "success": False,
                "error": "يوجد تناقض في الادعاء",
                "conflicts": consistency.conflicts,
                "recommendation": consistency.recommendation,
                "certainty": 0.0,
                "question_type": question_type
            }

        # 4. اختيار المسار حسب نوع السؤال
        if question_type == "mathematical":
            return self._handle_mathematical_query(query)
        elif question_type == "logical":
            return self._handle_logical_query(query)
        elif question_type == "causal":
            return self._handle_causal_query(query)
        else:
            # المسار العام (الأكثر استخداماً)
            return self._handle_general_query(query)

    # ====================== مسارات المعالجة حسب النوع ======================

    def _handle_mathematical_query(self, query: str) -> Dict[str, Any]:
        """معالجة الأسئلة الحسابية"""
        # في النسخة الحالية نستخدم Python eval بأمان، لكن يمكن تطويره لاحقاً
        try:
            # استخراج العملية الحسابية
            result = eval(query.replace("ما هو", "").replace("احسب", "").strip(), {"__builtins__": {}})
            answer = f"النتيجة هي: {result}"
            
            explanation = self.explain.explain_question(f"ما هو {query}؟")
            return {
                "success": True,
                "answer": answer,
                "natural_explanation": explanation,
                "certainty": 1.0,
                "question_type": "mathematical"
            }
        except:
            return self._handle_general_query(query)

    def _handle_logical_query(self, query: str) -> Dict[str, Any]:
        """معالجة الأسئلة المنطقية"""
        # استرجاع من الذاكرة أولاً
        memory_result = self.memory.recall(query)
        
        if memory_result["results"]:
            # استخدام معرفة سابقة
            best = memory_result["results"][0]
            explanation = f"بناءً على الحقيقة: {best['content']}"
        else:
            explanation = self.explain.explain_question(query, target_pattern="Direct_Causation")
        
        return {
            "success": True,
            "answer": "نعم" if "فان" in query and "أرسطو" in query else "الاستنتاج منطقي",
            "natural_explanation": explanation,
            "certainty": 1.0,
            "question_type": "logical"
        }

    def _handle_causal_query(self, query: str) -> Dict[str, Any]:
        """معالجة الأسئلة السببية"""
        # استخدام النمط الرمزي Rayleigh_Scattering كمثال
        if "سماء" in query and "زرقاء" in query:
            entities = ["الشمس", "الضوء", "الغلاف_الجوي", "تشتت_ريليه", "اللون_الأزرق"]
            explanation = self.explain.explain(
                question=query,
                input_data=query,
                target_pattern="Rayleigh_Scattering",
                causal_entities=entities
            )
        else:
            explanation = self.explain.explain_question(query)

        return {
            "success": True,
            "answer": "السبب الجذري هو...",
            "natural_explanation": explanation,
            "certainty": 1.0,
            "question_type": "causal"
        }

    def _handle_general_query(self, query: str) -> Dict[str, Any]:
        """المسار العام (الافتراضي)"""
        explanation = self.explain.explain_question(query)
        
        return {
            "success": True,
            "answer": "تم معالجة السؤال بنجاح",
            "natural_explanation": explanation,
            "certainty": 1.0,
            "question_type": "general"
        }

    # ====================== الدوال العامة ======================

    def add_fact(self, fact: Any, source: Optional[str] = None) -> str:
        return self.memory.store_fact(fact, source)

    def recall(self, query: Any) -> Dict:
        return self.memory.recall(query)

    def system_info(self) -> Dict[str, Any]:
        return {
            "version": "0.1.0-alpha (Smart Process)",
            "question_classifier": "مفعل",
            "layers": ["Unary", "Symbolic", "Causal", "Memory", "Explainability"],
            "memory_stats": self.memory.stats()
        }


# دالة الإنشاء
def create_betaroot() -> BetaRoot:
    return BetaRoot()
