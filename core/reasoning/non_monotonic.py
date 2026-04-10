# betaroot/core/reasoning/non_monotonic.py
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import copy

class RevisionType(Enum):
    EXPANSION = "add_new"      # إضافة معلومة جديدة دون تناقض
    CONTRACTION = "remove"     # إزالة معتقد لتجنب التناقض
    REVISION = "replace"       # استبدال معتقد قديم بجديد

@dataclass
class BeliefRevisionReport:
    """تقرير مفصل عن عملية مراجعة المعتقدات"""
    original_facts: Dict
    new_evidence: Dict
    conflicts_detected: List[Dict]
    actions_taken: List[Dict]
    final_state: Dict
    confidence_changes: Dict[str, float]

class NonMonotonicReasoner:
    """
    تنفيذ للمنطق غير الرتيب باستخدام نظرية AGM (Alchourrón–Gärdenfors–Makinson)
    يدعم:
    - كشف التناقضات
    - مراجعة المعتقدات بأقل تغيير ممكن
    - تتبع التبريرات (TMS-style)
    """
    def __init__(self, kb: KnowledgeBase, fb: FactBase):
        self.kb = kb
        self.fb = fb
        self.justification_db: Dict[str, Set[str]] = {}  # fact → {rule_ids that support it}
        
    def register_justification(self, fact_var: str, rule_id: str):
        """تسجيل أن قاعدة معينة تدعم حقيقة معينة"""
        if fact_var not in self.justification_db:
            self.justification_db[fact_var] = set()
        self.justification_db[fact_var].add(rule_id)
        
    def detect_conflicts(self, new_evidence: Dict) -> List[Dict]:
        """كشف التناقضات بين الأدلة الجديدة والحقائق الحالية"""
        conflicts = []
        for var, new_val in new_evidence.items():
            old_fact = self.fb.facts.get(var)
            if old_fact and old_fact.value != new_val:
                conflicts.append({
                    'variable': var,
                    'old_value': old_fact.value,
                    'new_value': new_val,
                    'old_confidence': old_fact.confidence,
                    'justification': old_fact.justification
                })
        return conflicts
    
    def revise_beliefs(self, new_evidence: Dict, 
                      strategy: str = "minimal_change") -> BeliefRevisionReport:
        """
        تنفيذ مراجعة المعتقدات وفق استراتيجية محددة
        
        استراتيجيات مدعومة:
        - "minimal_change": غيّر أقل عدد ممكن من المعتقدات
        - "recency_priority": فضّل الأدلة الأحدث زمنياً
        - "confidence_priority": فضّل المعتقدات الأعلى يقيناً
        """
        report = BeliefRevisionReport(
            original_facts=copy.deepcopy({k: v.value for k, v in self.fb.facts.items()}),
            new_evidence=new_evidence,
            conflicts_detected=[],
            actions_taken=[],
            final_state={},
            confidence_changes={}
        )
        
        # 1. كشف التناقضات
        report.conflicts_detected = self.detect_conflicts(new_evidence)
        
        if not report.conflicts_detected:
            # لا تناقض → مجرد توسعة
            for var, val in new_evidence.items():
                self.fb.add(var, val, TruthValue.TRUE, source="revision")
                report.actions_taken.append({'action': 'add', 'variable': var})
            report.final_state = {k: v.value for k, v in self.fb.facts.items()}
            return report
        
        # 2. معالجة التناقضات حسب الاستراتيجية
        for conflict in report.conflicts_detected:
            var = conflict['variable']
            
            if strategy == "recency_priority":
                # الأدلة الجديدة تُفضّل دائماً
                self._replace_fact(var, new_evidence[var], 
                                 source="revision:recency")
                report.actions_taken.append({
                    'action': 'replace', 'variable': var,
                    'reason': 'recency_priority'
                })
                
            elif strategy == "confidence_priority":
                # قارن درجات اليقين
                old_conf = conflict['old_confidence']
                new_conf = 1.0  # نفترض أن الأدلة المباشرة عالية اليقين
                if new_conf > old_conf:
                    self._replace_fact(var, new_evidence[var],
                                     source="revision:confidence")
                    report.actions_taken.append({
                        'action': 'replace', 'variable': var,
                        'reason': 'higher_confidence'
                    })
                    
            elif strategy == "minimal_change":
                # استخدم خوارزمية تعتمد على تبعيات القواعد
                # لتقليل عدد المعتقدات المتأثرة
                affected = self._find_affected_beliefs(var)
                if len(affected) <= 1:
                    self._replace_fact(var, new_evidence[var],
                                     source="revision:minimal")
                    report.actions_taken.append({
                        'action': 'replace', 'variable': var,
                        'reason': 'minimal_ripple'
                    })
                else:
                    # تناقض معقد → استخدم بايز لاتخاذ القرار
                    report.actions_taken.append({
                        'action': 'defer_to_bayesian', 'variable': var,
                        'reason': 'complex_dependency'
                    })
        
        # 3. تحديث التقرير النهائي
        report.final_state = {k: v.value for k, v in self.fb.facts.items()}
        report.confidence_changes = self._compute_confidence_deltas()
        
        return report
    
    def _replace_fact(self, var: str, new_value: Any, source: str):
        """استبدال حقيقة مع تسجيل العملية"""
        old = self.fb.facts.get(var)
        if old:
            report.confidence_changes[var] = new_value - old.value
        self.fb.add(var, new_value, TruthValue.TRUE, source=source)
    
    def _find_affected_beliefs(self, variable: str) -> Set[str]:
        """العثور على كل المعتقدات التي تعتمد على متغير معين"""
        affected = set()
        # استخدم الرسم السببي للعثور على المتغيرات المتأثرة
        if variable in self.kb.causal_graph:
            # كل الأبناء يتأثرون
            affected.update(nx.descendants(self.kb.causal_graph, variable))
        return affected
    
    def _compute_confidence_deltas(self) -> Dict[str, float]:
        """حساب التغيرات في درجات اليقين بعد المراجعة"""
        # يمكن توسيع هذا لحساب تأثير الدومينو على المعتقدات المرتبطة
        return {}
