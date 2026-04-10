"""
Knowledge Base Module for BetaRoot
Stores rules, causal relationships, and logical dependencies.
"""
from typing import Dict, List, Optional, Set, Callable, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime
import networkx as nx
import logging

logger = logging.getLogger(__name__)


class RuleType(Enum):
    """أنواع القواعد المنطقية المدعومة"""
    IMPLICATION = auto()        # A → B (إذا A فإن B)
    BICONDITIONAL = auto()      # A ↔ B (A إذا وفقط إذا B)
    CAUSAL = auto()             # A causes B (علاقة سببية احتمالية)
    CONSTRAINT = auto()         # ¬(A ∧ B) (قيود عدم التوافق)
    DISJUNCTION = auto()        # A ∨ B → C (أو منطقي)


@dataclass
class Rule:
    """
    تمثيل قاعدة معرفية قابلة للاستدلال
    
    مثال:
        Rule(
            id="R1",
            antecedents=["Fever", "Cough"],
            consequent="PossibleInfection",
            rule_type=RuleType.IMPLICATION,
            confidence=0.9,
            meta={"domain": "medical", "source": "expert"}
        )
    """
    id: str
    antecedents: List[str]           # المقدمات/الشروط
    consequent: str                  # النتيجة/الاستنتاج
    rule_type: RuleType
    confidence: float = 1.0          # درجة اليقين [0.0, 1.0]
    meta: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    enabled: bool = True             # لإيقاف القاعدة مؤقتاً دون حذفها
    
    def __post_init__(self):
        """تحقق من صحة البيانات عند الإنشاء"""
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"Confidence must be in [0.0, 1.0], got {self.confidence}")
        if not self.id or not self.consequent:
            raise ValueError("Rule ID and consequent are required")
    
    def is_satisfied(self, facts: 'FactBase', threshold: float = 0.5) -> bool:
        """
        تحقق مما إذا كانت كل المقدمات مُحققة في قاعدة الحقائق
        
        Args:
            facts: قاعدة الحقائق للتحقق منها
            threshold: الحد الأدنى لدرجة اليقين لاعتبار الحقيقة "صحيحة"
        
        Returns:
            True إذا كانت كل المقدمات مُحققة بدرجة يقين كافية
        """
        if not self.enabled:
            return False
            
        for ant in self.antecedents:
            fact = facts.get(ant)
            if fact is None:
                return False  # مقدمة غير معروفة
            if fact.truth != TruthValue.TRUE or fact.confidence < threshold:
                return False  # مقدمة غير صحيحة أو غير مؤكدة بما يكفي
        return True
    
    def apply(self, facts: 'FactBase') -> Optional['Fact']:
        """
        تطبيق القاعدة لإنتاج حقيقة جديدة
        
        Returns:
            Fact جديدة تمثل النتيجة، أو None إذا لم تُطبَّق
        """
        if not self.is_satisfied(facts):
            return None
            
        # حساب درجة اليقين للنتيجة: حاصل ضرب يقين المقدمات × يقين القاعدة
        confidence = self.confidence
        for ant in self.antecedents:
            fact = facts.get(ant)
            if fact:
                confidence *= fact.confidence
        
        return Fact(
            variable=self.consequent,
            value=True,  # يمكن تعميم هذا لاحقاً لقيم غير بوليانية
            truth=TruthValue.TRUE,
            confidence=min(confidence, 1.0),
            source="inference",
            justification=self.id
        )
    
    def __repr__(self):
        ant_str = " ∧ ".join(self.antecedents) if self.antecedents else "TRUE"
        return f"Rule({self.id}): {ant_str} → {self.consequent} [conf={self.confidence}]"


class KnowledgeBase:
    """
    قاعدة المعرفة المركزية لـ BetaRoot
    
    المسؤولة عن:
    - تخزين القواعد المنطقية والسببية
    - إدارة الرسم البياني السببي (Causal DAG)
    - تتبع تبعيات القواعد لتسهيل المراجعة
    - دعم الاستعلامات الفعالة للاستدلال
    """
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.rules: Dict[str, Rule] = {}
        self.causal_graph: nx.DiGraph = nx.DiGraph()
        
        # فهرس عكسي: consequent → [rule_ids] لتسريع السلسلة الخلفية
        self._consequent_index: Dict[str, Set[str]] = {}
        
        # فهرس للمقدمات: antecedent → [rule_ids] لتسريع السلسلة الأمامية
        self._antecedent_index: Dict[str, Set[str]] = {}
        
        # تتبع التبعيات بين القواعد (للمراجعة غير الرتيبة)
        self._rule_dependencies: Dict[str, Set[str]] = {}
        
        logger.info(f"KnowledgeBase '{name}' initialized")
    
    # ========== إدارة القواعد ==========
    
    def add_rule(self, rule: Rule, update_indices: bool = True) -> bool:
        """
        إضافة قاعدة جديدة إلى قاعدة المعرفة
        
        Args:
            rule: الكائن Rule المراد إضافته
            update_indices: هل نحدّث الفهارس الداخلية تلقائياً؟
        
        Returns:
            True إذا أضيفت بنجاح، False إذا كانت موجودة مسبقاً
        """
        if rule.id in self.rules:
            logger.warning(f"Rule '{rule.id}' already exists, skipping")
            return False
        
        # تحقق من أن الرسم السببي يبقى DAG عند إضافة قواعد سببية
        if rule.rule_type == RuleType.CAUSAL:
            temp_graph = self.causal_graph.copy()
            for ant in rule.antecedents:
                temp_graph.add_edge(ant, rule.consequent)
            if not nx.is_directed_acyclic_graph(temp_graph):
                raise ValueError(
                    f"Adding causal rule '{rule.id}' would create a cycle in the causal graph"
                )
            # تحديث الرسم السببي الفعلي
            for ant in rule.antecedents:
                self.causal_graph.add_edge(ant, rule.consequent, rule_id=rule.id)
        
        self.rules[rule.id] = rule
        
        if update_indices:
            self._update_indices_for_rule(rule, add=True)
        
        logger.debug(f"Added rule: {rule}")
        return True
    
    def remove_rule(self, rule_id: str, update_indices: bool = True) -> bool:
        """إزالة قاعدة من قاعدة المعرفة"""
        if rule_id not in self.rules:
            return False
        
        rule = self.rules[rule_id]
        
        # إزالة الحواف السببية المرتبطة
        if rule.rule_type == RuleType.CAUSAL:
            for ant in rule.antecedents:
                if self.causal_graph.has_edge(ant, rule.consequent):
                    edge_data = self.causal_graph[ant][rule.consequent]
                    if edge_data.get('rule_id') == rule_id:
                        self.causal_graph.remove_edge(ant, rule.consequent)
        
        del self.rules[rule_id]
        
        if update_indices:
            self._update_indices_for_rule(rule, add=False)
        
        logger.debug(f"Removed rule: {rule_id}")
        return True
    
    def enable_rule(self, rule_id: str, enabled: bool) -> bool:
        """تفعيل أو تعطيل قاعدة دون حذفها"""
        if rule_id not in self.rules:
            return False
        self.rules[rule_id].enabled = enabled
        return True
    
    def _update_indices_for_rule(self, rule: Rule, add: bool):
        """تحديث الفهارس الداخلية عند إضافة/إزالة قاعدة"""
        operation = (lambda s, x: s.add(x)) if add else (lambda s, x: s.discard(x))
        
        # فهرس النتائج
        operation(self._consequent_index.setdefault(rule.consequent, set()), rule.id)
        
        # فهرس المقدمات
        for ant in rule.antecedents:
            operation(self._antecedent_index.setdefault(ant, set()), rule.id)
    
    # ========== استعلامات القواعد ==========
    
    def get_applicable_rules(self, facts: 'FactBase', threshold: float = 0.5) -> List[Rule]:
        """
        إرجاع كل القواعد التي يمكن تطبيقها حالياً بناءً على الحقائق المتاحة
        
        يستخدم للسلسلة الأمامية (Forward Chaining)
        """
        applicable = []
        for rule in self.rules.values():
            if rule.is_satisfied(facts, threshold):
                applicable.append(rule)
        return applicable
    
    def get_rules_for_conclusion(self, conclusion: str) -> List[Rule]:
        """
        إرجاع كل القواعد التي تنتج نتيجة معينة
        
        يستخدم للسلسلة الخلفية (Backward Chaining)
        """
        rule_ids = self._consequent_index.get(conclusion, set())
        return [self.rules[rid] for rid in rule_ids if rid in self.rules]
    
    def get_rules_triggered_by(self, variable: str) -> List[Rule]:
        """
        إرجاع كل القواعد التي قد تتأثر بتحديث متغير معين
        
        مفيد لتحديد المعتقدات التي تحتاج مراجعة عند تغيير حقيقة
        """
        rule_ids = self._antecedent_index.get(variable, set())
        return [self.rules[rid] for rid in rule_ids if rid in self.rules]
    
    def find_affected_variables(self, variable: str, max_depth: int = -1) -> Set[str]:
        """
        العثور على كل المتغيرات التي تعتمد سببياً على متغير معين
        
        يستخدم لتحديد نطاق تأثير مراجعة المعتقدات
        """
        if variable not in self.causal_graph:
            return set()
        
        if max_depth == -1:
            # كل الأبناء في الرسم السببي
            return nx.descendants(self.causal_graph, variable)
        else:
            # الأبناء حتى عمق معين
            return nx.descendants_at_distance(self.causal_graph, variable, max_depth)
    
    # ========== أدوات مساعدة ==========
    
    def get_rule(self, rule_id: str) -> Optional[Rule]:
        """الحصول على قاعدة بمعرفها"""
        return self.rules.get(rule_id)
    
    def list_rules(self, filter_type: Optional[RuleType] = None) -> List[Rule]:
        """سرد القواعد مع خيار التصفية حسب النوع"""
        rules = list(self.rules.values())
        if filter_type:
            rules = [r for r in rules if r.rule_type == filter_type]
        return rules
    
    def export_to_dict(self) -> Dict[str, Any]:
        """تصدير قاعدة المعرفة كقاموس (للتخزين أو النقل)"""
        return {
            'name': self.name,
            'rules': [
                {
                    'id': r.id,
                    'antecedents': r.antecedents,
                    'consequent': r.consequent,
                    'rule_type': r.rule_type.name,
                    'confidence': r.confidence,
                    'meta': r.meta,
                    'enabled': r.enabled
                }
                for r in self.rules.values()
            ],
            'causal_edges': list(self.causal_graph.edges(data=True))
        }
    
    @classmethod
    def import_from_dict(cls, data: Dict[str, Any]) -> 'KnowledgeBase':
        """استيراد قاعدة معرفة من قاموس"""
        kb = cls(name=data.get('name', 'imported'))
        
        for rule_data in data.get('rules', []):
            rule = Rule(
                id=rule_data['id'],
                antecedents=rule_data['antecedents'],
                consequent=rule_data['consequent'],
                rule_type=RuleType[rule_data['rule_type']],
                confidence=rule_data['confidence'],
                meta=rule_data.get('meta', {}),
                enabled=rule_data.get('enabled', True)
            )
            kb.add_rule(rule, update_indices=False)
        
        # إعادة بناء الفهارس والرسم السببي
        for rule in kb.rules.values():
            kb._update_indices_for_rule(rule, add=True)
            if rule.rule_type == RuleType.CAUSAL:
                for ant in rule.antecedents:
                    kb.causal_graph.add_edge(ant, rule.consequent)
        
        return kb
    
    def __len__(self):
        return len(self.rules)
    
    def __repr__(self):
        return f"KnowledgeBase('{self.name}', rules={len(self.rules)}, causal_edges={self.causal_graph.number_of_edges()})"
