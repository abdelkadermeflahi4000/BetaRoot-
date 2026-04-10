# betaroot/core/knowledge/knowledge_base.py
from typing import Dict, List, Optional, Set, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
import networkx as nx

class RuleType(Enum):
    IMPLICATION = "if_then"          # A → B
    BICONDITIONAL = "iff"            # A ↔ B
    CAUSAL = "causes"                # A causes B (probabilistic)
    CONSTRAINT = "constraint"        # ¬(A ∧ B)

@dataclass
class Rule:
    """تمثيل قاعدة معرفية قابلة للاستدلال"""
    id: str
    antecedents: List[str]           # المقدمات [A, B]
    consequent: str                  # النتيجة C
    rule_type: RuleType
    confidence: float = 1.0          # درجة اليقين (1.0 للمنطق الصارم)
    metadata: Dict = field(default_factory=dict)
    
    def is_satisfied(self, facts: 'FactBase') -> bool:
        """تحقق مما إذا كانت المقدمات مُحققة في قاعدة الحقائق"""
        if self.rule_type == RuleType.IMPLICATION:
            return all(facts.is_true(ant) for ant in self.antecedents)
        # ... أنواع أخرى
        return False

class KnowledgeBase:
    """
    قاعدة المعرفة: تحتوي على القواعد والعلاقات السببية
    - منفصلة عن الحقائق لتسهيل المراجعة والتحديث
    """
    def __init__(self):
        self.rules: Dict[str, Rule] = {}
        self.causal_graph: nx.DiGraph = nx.DiGraph()
        self.rule_dependencies: Dict[str, Set[str]] = {}  # تتبع تبعيات القواعد
        
    def add_rule(self, rule: Rule) -> None:
        """إضافة قاعدة مع تحديث تبعياتها"""
        self.rules[rule.id] = rule
        # تحديث الرسم السببي إذا كانت القاعدة سببية
        if rule.rule_type == RuleType.CAUSAL:
            for ant in rule.antecedents:
                self.causal_graph.add_edge(ant, rule.consequent)
                
    def get_applicable_rules(self, facts: 'FactBase') -> List[Rule]:
        """إرجاع القواعد التي يمكن تطبيقها حالياً"""
        return [r for r in self.rules.values() if r.is_satisfied(facts)]
    
    def find_rules_for_conclusion(self, conclusion: str) -> List[Rule]:
        """البحث عن كل القواعد التي تنتج نتيجة معينة (للسلسلة الخلفية)"""
        return [r for r in self.rules.values() if r.consequent == conclusion]
