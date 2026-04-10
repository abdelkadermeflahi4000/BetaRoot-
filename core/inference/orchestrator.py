# betaroot/core/inference/orchestrator.py
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

class InferenceStrategy(Enum):
    SYMBOLIC_FIRST = "symbolic_first"      # جرب المنطق أولاً
    PROBABILISTIC_FIRST = "probabilistic_first"
    PARALLEL_HYBRID = "parallel_hybrid"    # شغّل الاثنين وادمج النتائج
    BACKWARD_ONLY = "backward_only"        # للتحقيق في فرضية محددة

@dataclass
class InferenceResult:
    variable: str
    value: Any
    confidence: float
    method: str  # "forward_chain", "backward_chain", "bayesian", "hybrid"
    justification: List[str]  # rule_ids or evidence chain
    timestamp: float

class InferenceOrchestrator:
    """
    المحرك الرئيسي الذي ينسق بين:
    - السلسلة الأمامية/الخلفية
    - الاستدلال البيزي
    - مراجعة المعتقدات
    """
    def __init__(self, kb: KnowledgeBase, fb: FactBase, 
                 bayesian_engine: 'BayesianEngine' = None):
        self.kb = kb
        self.fb = fb
        self.bayesian = bayesian_engine
        self.strategies = {}
        
    def register_strategy(self, name: str, strategy: Callable):
        """تسجيل استراتيجية استدلال مخصصة"""
        self.strategies[name] = strategy
        
    def infer(self, query: Union[str, List[str]], 
              strategy: InferenceStrategy = InferenceStrategy.SYMBOLIC_FIRST,
              evidence: Optional[Dict] = None,
              max_depth: int = 10) -> Dict[str, InferenceResult]:
        """
        النقطة المركزية للاستدلال
        """
        if evidence:
            # دمج الأدلة الجديدة في قاعدة الحقائق
            for var, val in evidence.items():
                self.fb.add(var, val, TruthValue.TRUE, source="evidence")
        
        results = {}
        
        if strategy == InferenceStrategy.SYMBOLIC_FIRST:
            # 1. جرب الاستدلال الرمزي أولاً
            results = self._symbolic_inference(query, max_depth)
            
            # 2. للمتغيرات التي لم تُحسم، استخدم بايز
            unresolved = [q for q in (query if isinstance(query, list) else [query]) 
                         if q not in results or results[q].confidence < 1.0]
            if unresolved and self.bayesian:
                bayes_results = self._probabilistic_inference(unresolved)
                results.update(bayes_results)
                
        elif strategy == InferenceStrategy.BACKWARD_ONLY:
            results = self._backward_chain_query(query)
            
        elif strategy == InferenceStrategy.PARALLEL_HYBRID:
            # شغّل الرمزي والاحتمالي بالتوازي وادمج
            sym_results = self._symbolic_inference(query, max_depth)
            prob_results = self._probabilistic_inference(query) if self.bayesian else {}
            results = self._merge_results(sym_results, prob_results)
            
        return results
    
    def _symbolic_inference(self, query, max_depth: int) -> Dict:
        """تنفيذ السلسلة الأمامية والخلفية رمزياً"""
        from .symbolic.forward_chainer import ForwardChainer
        from .symbolic.backward_chainer import BackwardChainer
        
        results = {}
        
        # Forward chaining: استنتج كل ما يمكن من الحقائق الحالية
        forward = ForwardChainer(self.kb, self.fb)
        new_facts = forward.run(max_iterations=max_depth)
        
        # تحقق مما إذا كانت الاستعلامات موجودة في النتائج
        queries = query if isinstance(query, list) else [query]
        for q in queries:
            if self.fb.is_true(q):
                results[q] = InferenceResult(
                    variable=q, value=True, confidence=1.0,
                    method="forward_chain", justification=["derived"]
                )
            elif self.fb.facts.get(q) and self.fb.facts[q].truth == TruthValue.FALSE:
                results[q] = InferenceResult(
                    variable=q, value=False, confidence=1.0,
                    method="forward_chain", justification=["derived"]
                )
        
        # Backward chaining للفرضيات غير المحسومة
        if len(results) < len(queries):
            backward = BackwardChainer(self.kb, self.fb)
            for q in queries:
                if q not in results:
                    proof = backward.prove(q, max_depth=max_depth)
                    if proof.success:
                        results[q] = InferenceResult(
                            variable=q, value=proof.value, confidence=1.0,
                            method="backward_chain", justification=proof.chain
                        )
        
        return results
    
    def _probabilistic_inference(self, query) -> Dict:
        """تنفيذ الاستدلال البيزي"""
        if not self.bayesian:
            return {}
            
        results = {}
        queries = query if isinstance(query, list) else [query]
        
        # تحويل الحقائق إلى أدلة للاستدلال البيزي
        evidence = {k: v.value for k, v in self.fb.facts.items() 
                   if v.truth == TruthValue.TRUE}
        
        for q in queries:
            prob_result = self.bayesian.query([q], evidence=evidence)
            # استخراج الحالة الأكثر احتمالاً
            best_state = max(prob_result, key=prob_result.get)
            value = best_state.split('=')[1] if '=' in best_state else best_state
            confidence = prob_result[best_state]
            
            results[q] = InferenceResult(
                variable=q, value=value, confidence=confidence,
                method="bayesian", justification=["probabilistic_inference"]
            )
            
        return results
    
    def _merge_results(self, sym: Dict, prob: Dict) -> Dict:
        """دمج نتائج المنطق الرمزي والاحتمالي"""
        merged = {}
        all_vars = set(sym.keys()) | set(prob.keys())
        
        for var in all_vars:
            if var in sym and sym[var].confidence == 1.0:
                # المنطق الرمزي حاسم → نفضّله
                merged[var] = sym[var]
            elif var in prob:
                # نستخدم النتيجة الاحتمالية
                merged[var] = prob[var]
            elif var in sym:
                # نتيجة رمزية غير حاسمة → نستخدمها مع تعديل اليقين
                merged[var] = sym[var]
                
        return merged
