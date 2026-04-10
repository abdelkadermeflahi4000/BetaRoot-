# betaroot/core/knowledge/fact_base.py
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum

class TruthValue(Enum):
    TRUE = 1
    FALSE = 0
    UNKNOWN = None
    CONTRADICTED = -1  # للتناقضات في المنطق غير الرتيب

@dataclass
class Fact:
    """تمثيل حقيقة مع سياق زمني ودرجة يقين"""
    variable: str
    value: Any
    truth: TruthValue
    confidence: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "user"  # user, inference, observation, revision
    justification: Optional[str] = None  # rule_id or evidence_ref

class FactBase:
    """
    قاعدة الحقائق: المخزن الديناميكي للملاحظات والاستنتاجات
    - يدعم التحديث غير الرتيب (مراجعة الحقائق المتناقضة)
    - يحتفظ بسجل التاريخ لتتبع التغييرات
    """
    def __init__(self):
        self.facts: Dict[str, Fact] = {}
        self.history: List[Dict] = []  # سجل التغييرات
        
    def add(self, variable: str, value: Any, truth: TruthValue, 
            confidence: float = 1.0, source: str = "inference",
            justification: str = None) -> bool:
        """
        إضافة أو تحديث حقيقة
        Returns: True if added/updated, False if contradicted (needs revision)
        """
        old_fact = self.facts.get(variable)
        
        # كشف التناقض
        if old_fact and old_fact.truth != truth and old_fact.confidence > 0.5:
            return False  # تناقض! يحتاج مراجعة
            
        new_fact = Fact(variable, value, truth, confidence, 
                       datetime.now(), source, justification)
        self.facts[variable] = new_fact
        
        # تسجيل في التاريخ
        self.history.append({
            'action': 'add' if not old_fact else 'update',
            'variable': variable,
            'old_value': old_fact.value if old_fact else None,
            'new_value': value,
            'timestamp': datetime.now()
        })
        return True
    
    def is_true(self, variable: str, threshold: float = 0.5) -> bool:
        """تحقق مما إذا كانت المتغير صحيحاً بدرجة يقين كافية"""
        fact = self.facts.get(variable)
        return fact and fact.truth == TruthValue.TRUE and fact.confidence >= threshold
    
    def get_all(self) -> Dict[str, Any]:
        """إرجاع كل الحقائق كقاموس بسيط للاستعلام"""
        return {k: v.value for k, v in self.facts.items() 
                if v.truth == TruthValue.TRUE}
