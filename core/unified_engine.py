"""
BetaRoot: UnifiedEngine
يربط فعلياً:
  KnowledgeBase → قواعد الاستدلال
  FactBase      → الحقائق الديناميكية
  ForwardChainer → استنتاج أمامي
  BackwardChainer → استنتاج خلفي
  BetaNode      → fallback احتمالي
  PhysicalDomains → معادلات فيزيائية (resonance etc.)
"""

from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import time


# ──────────────────────────────────────────────
# استراتيجيات الاستدلال
# ──────────────────────────────────────────────

class EngineStrategy(Enum):
    SYMBOLIC_FIRST   = "symbolic_first"    # رمزي → بايزي عند الفشل
    BAYESIAN_FIRST   = "bayesian_first"    # بايزي → رمزي عند عدم اليقين
    PARALLEL_HYBRID  = "parallel_hybrid"   # الاثنان معاً → اختيار الأفضل
    BACKWARD_ONLY    = "backward_only"     # تحقق من فرضية محددة


# ──────────────────────────────────────────────
# نتيجة الاستدلال
# ──────────────────────────────────────────────

@dataclass
class InferenceResult:
    variable:      str
    value:         Any
    certainty:     float          # 0.0 → 1.0
    method:        str            # forward_chain | backward_chain | bayesian | physical
    reasoning:     List[str]      = field(default_factory=list)
    success:       bool           = True

    def to_dict(self) -> Dict:
        return {
            "success":   self.success,
            "answer":    self.value,
            "certainty": self.certainty,
            "method":    self.method,
            "reasoning": self.reasoning,
        }


# ──────────────────────────────────────────────
# BetaNode داخلي (fallback احتمالي)
# ──────────────────────────────────────────────

class _BetaNode:
    def __init__(self, name: str, prior: float = 0.5):
        self.name  = name
        self.alpha = prior * 2
        self.beta  = (1 - prior) * 2

    def update(self, confirmed: bool):
        if confirmed:
            self.alpha += 1
        else:
            self.beta  += 1

    def certainty(self) -> float:
        return self.alpha / (self.alpha + self.beta)


# ──────────────────────────────────────────────
# المحرك الموحد
# ──────────────────────────────────────────────

class UnifiedEngine:
    """
    المحرك المركزي الذي ينسق كل طبقات الاستدلال.
    يُنشأ مع KnowledgeBase + FactBase من BetaRoot.
    """

    def __init__(self, kb, fb,
                 strategy: EngineStrategy = EngineStrategy.SYMBOLIC_FIRST):
        self.kb        = kb
        self.fb        = fb
        self.strategy  = strategy
        self._bayesian_nodes: Dict[str, _BetaNode] = {}
        self._call_log: List[Dict]  = []
        self._physical_domains: Dict[str, Any] = {}

    # ══════════════════════════════════════════
    # نقطة الدخول الرئيسية
    # ══════════════════════════════════════════

    def infer(self, query: Union[str, List[str]],
              evidence: Optional[Dict] = None,
              max_depth: int = 10) -> Dict:
        """
        استدلال موحد حسب الاستراتيجية المختارة.
        """
        t0 = time.time()

        # حقن أدلة خارجية في FactBase
        if evidence:
            self._inject_evidence(evidence)

        queries = [query] if isinstance(query, str) else query

        if self.strategy == EngineStrategy.SYMBOLIC_FIRST:
            result = self._symbolic_first(queries, max_depth)

        elif self.strategy == EngineStrategy.BAYESIAN_FIRST:
            result = self._bayesian_first(queries)

        elif self.strategy == EngineStrategy.PARALLEL_HYBRID:
            result = self._parallel_hybrid(queries, max_depth)

        elif self.strategy == EngineStrategy.BACKWARD_ONLY:
            result = self._backward_only(queries[0], max_depth)

        else:
            result = self._symbolic_first(queries, max_depth)

        # سجل الاستدعاء
        self._call_log.append({
            "query":    query,
            "method":   self.strategy.value,
            "elapsed":  round(time.time() - t0, 4),
            "success":  result.get("success", False)
        })

        return result

    def infer_physical(self, query: str) -> Dict:
        """
        استدلال في النطاقات الفيزيائية المحقونة.
        مثال: تردد، كتلة، رنين
        """
        for domain_name, domain in self._physical_domains.items():
            if hasattr(domain, "answer_query"):
                result = domain.answer_query(query)
                if result.get("success"):
                    result["method"] = f"physical:{domain_name}"
                    return result

        # fallback للاستدلال العام
        return self.infer(query)

    # ══════════════════════════════════════════
    # الاستراتيجيات الداخلية
    # ══════════════════════════════════════════

    def _symbolic_first(self, queries: List[str], max_depth: int) -> Dict:
        """١. رمزي أمامي → ٢. رمزي خلفي → ٣. بايزي fallback"""

        # ── Forward Chaining ──
        forward_results = self._run_forward()

        resolved   = {}
        unresolved = []

        for q in queries:
            if self.fb.is_true(q):
                resolved[q] = InferenceResult(
                    variable  = q,
                    value     = True,
                    certainty = 1.0,
                    method    = "forward_chain",
                    reasoning = [f"✓ {q} ثابتة بالسلسلة الأمامية"]
                )
            else:
                unresolved.append(q)

        # ── Backward Chaining لما لم يُحسم ──
        for q in unresolved:
            proof = self._run_backward(q, max_depth)
            if proof["proven"]:
                resolved[q] = InferenceResult(
                    variable  = q,
                    value     = proof["value"],
                    certainty = proof["confidence"],
                    method    = "backward_chain",
                    reasoning = proof["chain"]
                )
            else:
                unresolved_still = q

        # ── BetaNode fallback لما بقي غير محسوم ──
        still_unresolved = [q for q in queries if q not in resolved]
        for q in still_unresolved:
            node = self._get_or_create_node(q)
            resolved[q] = InferenceResult(
                variable  = q,
                value     = node.certainty() > 0.5,
                certainty = node.certainty(),
                method    = "bayesian_fallback",
                reasoning = [f"⚡ استدلال بايزي: يقين={node.certainty():.2f}"]
            )

        return self._aggregate(resolved, queries)

    def _bayesian_first(self, queries: List[str]) -> Dict:
        """بايزي أولاً → رمزي لما يقين > 0.9"""
        resolved = {}
        for q in queries:
            node = self._get_or_create_node(q)
            cert = node.certainty()
            if cert >= 0.9:
                resolved[q] = InferenceResult(
                    variable  = q,
                    value     = True,
                    certainty = cert,
                    method    = "bayesian_high_confidence",
                    reasoning = [f"يقين بايزي عالٍ: {cert:.2f}"]
                )
            else:
                # رمزي للتأكيد
                proof = self._run_backward(q, 5)
                if proof["proven"]:
                    resolved[q] = InferenceResult(
                        variable  = q,
                        value     = proof["value"],
                        certainty = 1.0,
                        method    = "bayesian+symbolic",
                        reasoning = proof["chain"]
                    )
                else:
                    resolved[q] = InferenceResult(
                        variable  = q,
                        value     = cert > 0.5,
                        certainty = cert,
                        method    = "bayesian_uncertain",
                        reasoning = [f"يقين منخفض: {cert:.2f} — يُنصح بإضافة قواعد"]
                    )
        return self._aggregate(resolved, queries)

    def _parallel_hybrid(self, queries: List[str], max_depth: int) -> Dict:
        """الرمزي والبايزي معاً → الأفضل يقيناً يفوز"""
        sym_result  = self._symbolic_first(queries, max_depth)
        bayes_result = self._bayesian_first(queries)

        # اختر الأعلى يقيناً
        if sym_result.get("certainty", 0) >= bayes_result.get("certainty", 0):
            sym_result["method"] = "parallel_hybrid:symbolic_won"
            return sym_result
        else:
            bayes_result["method"] = "parallel_hybrid:bayesian_won"
            return bayes_result

    def _backward_only(self, query: str, max_depth: int) -> Dict:
        """تحقق مباشر من فرضية واحدة"""
        proof = self._run_backward(query, max_depth)
        result = InferenceResult(
            variable  = query,
            value     = proof.get("value", False),
            certainty = proof.get("confidence", 0.0),
            method    = "backward_only",
            reasoning = proof.get("chain", []),
            success   = proof.get("proven", False)
        )
        return result.to_dict()

    # ══════════════════════════════════════════
    # تشغيل الـ Chainers الفعليين
    # ══════════════════════════════════════════

    def _run_forward(self) -> List:
        """تشغيل ForwardChainer الحقيقي"""
        try:
            try:
                from .inference.forward_chainer import ForwardChainer
            except ImportError:
                from inference.forward_chainer import ForwardChainer
            fc = ForwardChainer(self.kb, self.fb)
            return fc.run()
        except Exception:
            # fallback بسيط
            new_facts = []
            for rule in self.kb.rules.values():
                if rule.is_satisfied(self.fb):
                    if not self.fb.is_true(rule.consequent):
                        try:
                            try:
                                from .knowledge.fact_base import TruthValue
                            except ImportError:
                                from knowledge.fact_base import TruthValue
                            self.fb.add(rule.consequent, True,
                                        TruthValue.TRUE, source="forward_chain")
                        except Exception:
                            pass
                        new_facts.append(rule.consequent)
            return new_facts

    def _run_backward(self, hypothesis: str, max_depth: int) -> Dict:
        """تشغيل BackwardChainer الحقيقي"""
        try:
            try:
                from .inference.backward_chainer import BackwardChainer, ProofStatus
            except ImportError:
                from inference.backward_chainer import BackwardChainer, ProofStatus
            bc = BackwardChainer(self.kb, self.fb, max_depth)
            node = bc.prove(hypothesis)
            chain = [bc.explain_proof(node)]
            return {
                "proven":     node.status == ProofStatus.PROVEN,
                "value":      node.status == ProofStatus.PROVEN,
                "confidence": node.confidence,
                "chain":      chain
            }
        except Exception:
            # fallback بسيط
            rules = self.kb.find_rules_for_conclusion(hypothesis)
            for rule in rules:
                if all(self.fb.is_true(ant) for ant in rule.antecedents):
                    chain = (
                        [f"✓ {ant} ← موجودة" for ant in rule.antecedents] +
                        [f"→ القاعدة [{rule.id}] تنتج: {hypothesis}"]
                    )
                    return {
                        "proven":     True,
                        "value":      True,
                        "confidence": rule.confidence,
                        "chain":      chain
                    }
            return {"proven": False, "value": False, "confidence": 0.0, "chain": []}

    # ══════════════════════════════════════════
    # إدارة النطاقات الفيزيائية
    # ══════════════════════════════════════════

    def register_domain(self, name: str, domain_obj: Any):
        """تسجيل نطاق فيزيائي (مثل ResonanceLaw)"""
        self._physical_domains[name] = domain_obj

    # ══════════════════════════════════════════
    # أدوات داخلية
    # ══════════════════════════════════════════

    def _inject_evidence(self, evidence: Dict):
        from .knowledge.fact_base import TruthValue
        for var, val in evidence.items():
            self.fb.add(var, val, TruthValue.TRUE, source="evidence")

    def _get_or_create_node(self, name: str) -> _BetaNode:
        if name not in self._bayesian_nodes:
            self._bayesian_nodes[name] = _BetaNode(name)
        return self._bayesian_nodes[name]

    def update_bayesian(self, variable: str, confirmed: bool):
        """تحديث مؤشر بايزي لمتغير معين من قياس خارجي"""
        self._get_or_create_node(variable).update(confirmed)

    def _aggregate(self, resolved: Dict, queries: List[str]) -> Dict:
        """تجميع نتائج استعلامات متعددة"""
        if len(queries) == 1:
            q = queries[0]
            r = resolved.get(q, InferenceResult(q, None, 0.0, "unknown", success=False))
            return r.to_dict()

        return {
            "success":   all(r.success for r in resolved.values()),
            "results":   {q: r.to_dict() for q, r in resolved.items()},
            "certainty": min((r.certainty for r in resolved.values()), default=0.0),
            "method":    self.strategy.value
        }

    def status(self) -> Dict:
        return {
            "strategy":        self.strategy.value,
            "rules":           len(self.kb.rules),
            "facts":           len(self.fb.facts),
            "bayesian_nodes":  len(self._bayesian_nodes),
            "physical_domains": list(self._physical_domains.keys()),
            "calls":           len(self._call_log)
        }
