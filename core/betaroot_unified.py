"""
BetaRoot — الكلاس الموحد النهائي
يحل مشكلة الكلاسين المتكررين ويربط كل الطبقات عبر unified_engine
"""

from typing import Any, Dict, List, Optional
import re
import time
import datetime

from .unified_engine import UnifiedEngine, EngineStrategy
from .knowledge.knowledge_base import KnowledgeBase, Rule, RuleType
from .knowledge.fact_base import FactBase, TruthValue
from .memory import BetaRootMemory, create_memory_system
from .consistency_checker import ConsistencyChecker
from .explainability_engine import ExplainabilityEngine
from .symbolic_patterns_extended import SymbolicPatternsExtended


class BetaRoot:
    """
    الواجهة الموحدة لإطار BetaRoot
    
    المبدأ: Only 1, Never 0
    البنية: NLP → Classify → UnifiedEngine → KnowledgeBase + FactBase → Explain
    """

    VERSION = "0.2.0"

    def __init__(self, strategy: EngineStrategy = EngineStrategy.SYMBOLIC_FIRST):

        # قاعدة المعرفة الحقيقية
        self.kb = KnowledgeBase()
        self.fb = FactBase()

        # المحرك الموحد (يربط KB + FB + Chainers + BetaNode)
        self.engine = UnifiedEngine(self.kb, self.fb, strategy=strategy)

        # الطبقات الأخرى
        self.memory    = create_memory_system()
        self.patterns  = SymbolicPatternsExtended()
        self.explain   = ExplainabilityEngine()
        self.checker   = ConsistencyChecker()

        # تصنيف السؤال
        self._classifier = {
            "logical":      [r"هل .* فان", r"استنتج", r"هل .* صحيح", r"كل .* .*"],
            "mathematical": [r"\d+\s*[\+\-\*/\^]\s*\d+", r"احسب", r"ما ناتج"],
            "causal":       [r"لماذا", r"ما سبب", r"كيف يحدث", r"ما آلية"],
            "physical":     [r"تردد", r"كتلة", r"قطر", r"رنين", r"موجة"],
        }

        self.session_id = f"br_{int(time.time())}"

    # ══════════════════════════════════════════
    # الواجهة الرئيسية
    # ══════════════════════════════════════════

    def process(self, query: str,
                context: Optional[Dict] = None) -> Dict[str, Any]:
        """نقطة الدخول الموحدة لكل الاستعلامات"""

        if not query.strip():
            return self._error("استعلام فارغ")

        if context:
            self.memory.update_context(context)

        # 1. تحقق الاتساق
        consistency = self.checker.verify(query, context)
        if not consistency.is_consistent:
            return {
                "success":    False,
                "error":      "تناقض في الادعاء",
                "conflicts":  consistency.conflicts,
                "certainty":  0.0
            }

        # 2. تصنيف
        qtype = self._classify(query)

        # 3. توجيه للمحرك المناسب
        if qtype == "physical":
            result = self.engine.infer_physical(query)
        elif qtype in ("logical", "causal"):
            result = self.engine.infer(query)
        elif qtype == "mathematical":
            result = self._math(query)
        else:
            result = self.engine.infer(query)

        # 4. إضافة الشرح إذا غاب
        if "reasoning" not in result:
            result["reasoning"] = []

        result.update({
            "question_type": qtype,
            "session_id":    self.session_id,
            "timestamp":     datetime.datetime.now().isoformat(),
            "patterns_used": self.patterns.stats()["total"]
        })

        return result

    # ══════════════════════════════════════════
    # إضافة معرفة
    # ══════════════════════════════════════════

    def add_fact(self, variable: str, value: Any,
                 truth: TruthValue = TruthValue.TRUE,
                 source: str = "user") -> bool:
        """إضافة حقيقة إلى FactBase"""
        return self.fb.add(variable, value, truth, source=source)

    def add_rule(self, rule_id: str,
                 antecedents: List[str],
                 consequent: str,
                 rule_type: RuleType = RuleType.IMPLICATION,
                 confidence: float = 1.0) -> None:
        """إضافة قاعدة إلى KnowledgeBase"""
        rule = Rule(rule_id, antecedents, consequent, rule_type, confidence)
        self.kb.add_rule(rule)

    def inject_domain(self, domain_module) -> Dict:
        """حقن نطاق معرفي كامل (مثل resonance_law) في KB + FB"""
        return domain_module.inject_into_betaroot(self)

    # ══════════════════════════════════════════
    # استعلام مباشر
    # ══════════════════════════════════════════

    def query_fact(self, variable: str) -> Optional[Any]:
        fact = self.fb.facts.get(variable)
        return fact.value if fact else None

    def apply_pattern(self, data: Any, pattern_name: str):
        from .unary_logic import create_engine
        engine = create_engine()
        state  = engine.encode(data)
        return self.patterns.apply(state, pattern_name)

    # ══════════════════════════════════════════
    # معلومات النظام
    # ══════════════════════════════════════════

    def system_info(self) -> Dict[str, Any]:
        return {
            "version":      self.VERSION,
            "philosophy":   "Only 1, Never 0",
            "session_id":   self.session_id,
            "engine":       self.engine.status(),
            "patterns":     self.patterns.stats(),
            "facts":        len(self.fb.facts),
            "rules":        len(self.kb.rules),
        }

    def __repr__(self):
        return (f"BetaRoot(v{self.VERSION}, "
                f"facts={len(self.fb.facts)}, rules={len(self.kb.rules)}, "
                f"patterns={self.patterns.stats()['total']})")

    # ══════════════════════════════════════════
    # داخلي
    # ══════════════════════════════════════════

    def _classify(self, query: str) -> str:
        q = query.lower()
        for qtype, patterns in self._classifier.items():
            for p in patterns:
                if re.search(p, q):
                    return qtype
        return "general"

    def _math(self, query: str) -> Dict:
        try:
            expr = re.search(r"[\d\s\+\-\*\/\^\(\)\.]+", query)
            if expr:
                result = eval(expr.group().replace("^", "**"),
                              {"__builtins__": {}})
                return {
                    "success":   True,
                    "answer":    result,
                    "certainty": 1.0,
                    "method":    "safe_eval"
                }
        except Exception:
            pass
        return self._error("تعذر تقييم العملية الحسابية")

    def _error(self, msg: str) -> Dict:
        return {"success": False, "error": msg, "certainty": 0.0}


def create_betaroot(strategy: EngineStrategy = EngineStrategy.SYMBOLIC_FIRST) -> BetaRoot:
    return BetaRoot(strategy=strategy)
