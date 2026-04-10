"""
Fact Base Module for BetaRoot
Stores observations, inferred facts, and belief states with temporal tracking.
"""
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime
import logging
import copy

logger = logging.getLogger(__name__)


class TruthValue(Enum):
    """قيم الحقيقة المدعومة مع توسيع للمنطق غير الرتيب"""
    TRUE = auto()           # صحيح مؤكد
    FALSE = auto()          # خاطئ مؤكد
    UNKNOWN = auto()        # غير معروف / غير محدد
    CONTRADICTED = auto()   # متناقض (للمراجعة غير الرتيبة)


@dataclass
class Fact:
    """
    تمثيل حقيقة مع سياق زمني ودرجة يقين ومصدر
    
    يدعم:
    - التحديث غير الرتيب (مراجعة الحقائق المتناقضة)
    - تتبع التبريرات (لشرح الاستنتاجات)
    - النسخ التاريخية (للتراجع عند الحاجة)
    """
    variable: str
    value: Any
    truth: TruthValue
    confidence: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "user"  # user, observation, inference, revision, external
    justification: Optional[str] = None  # rule_id, evidence_ref, or explanation
    version: int = 1  # لتتبع التحديثات على نفس المتغير
    
    def __post_init__(self):
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"Confidence must be in [0.0, 1.0], got {self.confidence}")
    
    def contradicts(self, other: 'Fact') -> bool:
        """تحقق مما إذا كانت هذه الحقيقة تناقض حقيقة أخرى"""
        if self.variable != other.variable:
            return False
        if self.truth == TruthValue.UNKNOWN or other.truth == TruthValue.UNKNOWN:
            return False
        if self.truth == TruthValue.CONTRADICTED or other.truth == TruthValue.CONTRADICTED:
            return True
        # تناقض إذا كانت القيم مختلفة وكلاهما مؤكد بدرجة معقولة
        return (self.truth != other.truth or 
                (self.value != other.value and 
                 self.confidence > 0.5 and other.confidence > 0.5))
    
    def merge_with(self, other: 'Fact', strategy: str = 'higher_confidence') -> 'Fact':
        """
        دمج حقيقتين لنفس المتغير وفق استراتيجية محددة
        
        استراتيجيات الدمج:
        - 'higher_confidence': نحتفظ بالأعلى يقيناً
        - 'weighted_average': متوسط مرجح للقيم العددية
        - 'newer_timestamp': نحتفظ بالأحدث زمنياً
        """
        if self.variable != other.variable:
            raise ValueError("Cannot merge facts about different variables")
        
        if strategy == 'higher_confidence':
            return self if self.confidence >= other.confidence else other
        
        elif strategy == 'newer_timestamp':
            return self if self.timestamp >= other.timestamp else other
        
        elif strategy == 'weighted_average' and isinstance(self.value, (int, float)):
            total_conf = self.confidence + other.confidence
            if total_conf == 0:
                return self
            merged_value = (
                self.value * self.confidence + other.value * other.confidence
            ) / total_conf
            return Fact(
                variable=self.variable,
                value=merged_value,
                truth=TruthValue.TRUE,
                confidence=min(total_conf / 2, 1.0),
                source="merged",
                justification=f"merged:{self.justification},{other.justification}"
            )
        
        #fallback
        return self
    
    def __repr__(self):
        return (f"Fact({self.variable}={self.value}, truth={self.truth.name}, "
                f"conf={self.confidence:.2f}, src={self.source})")


@dataclass
class FactHistoryEntry:
    """سجل تغيير لحقيقة ما (للتتبع والتراجع)"""
    variable: str
    action: str  # 'add', 'update', 'revise', 'remove'
    old_fact: Optional[Fact]
    new_fact: Optional[Fact]
    timestamp: datetime = field(default_factory=datetime.now)
    reason: Optional[str] = None
    
    def __repr__(self):
        return f"HistoryEntry({self.variable}:{self.action} @ {self.timestamp.strftime('%H:%M:%S')})"


class FactBase:
    """
    قاعدة الحقائق الديناميكية لـ BetaRoot
    
    المسؤولة عن:
    - تخزين الحقائق المرصودة والمستنتجة
    - كشف التناقضات وإدارتها
    - تتبع تاريخ التغييرات لدعم المراجعة غير الرتيبة
    - توفير واجهات استعلام فعالة للمحركات
    """
    
    def __init__(self, name: str = "default", max_history: int = 1000):
        self.name = name
        self.facts: Dict[str, Fact] = {}
        self.history: List[FactHistoryEntry] = []
        self.max_history = max_history  # للحد من استهلاك الذاكرة
        
        # فهرس بالمصدر لتتبع أصل الحقائق
        self._source_index: Dict[str, Set[str]] = {}
        
        logger.info(f"FactBase '{name}' initialized with max_history={max_history}")
    
    # ========== إدارة الحقائق ==========
    
    def add(self, variable: str, value: Any, truth: TruthValue,
            confidence: float = 1.0, source: str = "user",
            justification: str = None,
            on_conflict: str = 'reject') -> tuple[bool, Optional[str]]:
        """
        إضافة أو تحديث حقيقة في قاعدة الحقائق
        
        Args:
            variable: اسم المتغير/الحقيقة
            value: القيمة المراد تخزينها
            truth: قيمة الحقيقة (TRUE/FALSE/UNKNOWN/CONTRADICTED)
            confidence: درجة اليقين [0.0, 1.0]
            source: مصدر الحقيقة (user, observation, inference, etc.)
            justification: مرجع يبرر هذه الحقيقة (rule_id, evidence, etc.)
            on_conflict: استراتيجية التعامل مع التناقضات:
                - 'reject': رفض الإضافة وإرجاع خطأ
                - 'replace': استبدال الحقيقة القديمة
                - 'merge': محاولة دمج القيم
                - 'flag': وضع الحقيقة في حالة CONTRADICTED
        
        Returns:
            (success: bool, message: Optional[str])
        """
        old_fact = self.facts.get(variable)
        new_fact = Fact(
            variable=variable, value=value, truth=truth,
            confidence=confidence, source=source, justification=justification,
            version=(old_fact.version + 1) if old_fact else 1
        )
        
        # كشف التناقض
        if old_fact and old_fact.contradicts(new_fact):
            if on_conflict == 'reject':
                msg = f"Conflict: '{variable}' contradicts existing fact {old_fact}"
                logger.warning(msg)
                return False, msg
            
            elif on_conflict == 'replace':
                self._record_history(variable, 'update', old_fact, new_fact, 
                                   reason="conflict_resolution:replace")
                self.facts[variable] = new_fact
                self._update_source_index(variable, source, add=True)
                return True, "replaced"
            
            elif on_conflict == 'merge':
                merged = old_fact.merge_with(new_fact)
                self._record_history(variable, 'merge', old_fact, merged,
                                   reason="conflict_resolution:merge")
                self.facts[variable] = merged
                return True, "merged"
            
            elif on_conflict == 'flag':
                # نحتفظ بالقيمة الجديدة لكن نعلّمها كمتناقضة
                new_fact.truth = TruthValue.CONTRADICTED
                self._record_history(variable, 'flag', old_fact, new_fact,
                                   reason="conflict_flagged")
                self.facts[variable] = new_fact
                return True, "flagged_as_contradicted"
        
        # لا تناقض → إضافة/تحديث عادي
        action = 'add' if not old_fact else 'update'
        self._record_history(variable, action, old_fact, new_fact)
        self.facts[variable] = new_fact
        self._update_source_index(variable, source, add=True)
        
        logger.debug(f"{action.capitalize()} fact: {new_fact}")
        return True, action
    
    def _record_history(self, variable: str, action: str, 
                       old_fact: Optional[Fact], new_fact: Optional[Fact],
                       reason: str = None):
        """تسجيل تغيير في سجل التاريخ"""
        entry = FactHistoryEntry(
            variable=variable, action=action,
            old_fact=copy.deepcopy(old_fact) if old_fact else None,
            new_fact=copy.deepcopy(new_fact) if new_fact else None,
            reason=reason
        )
        self.history.append(entry)
        
        # تدوير السجل إذا تجاوز الحد
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def _update_source_index(self, variable: str, source: str, add: bool):
        """تحديث فهرس المصادر"""
        if add:
            self._source_index.setdefault(source, set()).add(variable)
        else:
            if source in self._source_index:
                self._source_index[source].discard(variable)
                if not self._source_index[source]:
                    del self._source_index[source]
    
    # ========== استعلامات الحقائق ==========
    
    def get(self, variable: str) -> Optional[Fact]:
        """الحصول على حقيقة بمتغيرها"""
        return self.facts.get(variable)
    
    def is_true(self, variable: str, threshold: float = 0.5) -> bool:
        """تحقق مما إذا كان المتغير صحيحاً بدرجة يقين كافية"""
        fact = self.facts.get(variable)
        return (fact is not None and 
                fact.truth == TruthValue.TRUE and 
                fact.confidence >= threshold)
    
    def is_false(self, variable: str, threshold: float = 0.5) -> bool:
        """تحقق مما إذا كان المتغير خاطئاً بدرجة يقين كافية"""
        fact = self.facts.get(variable)
        return (fact is not None and 
                fact.truth == TruthValue.FALSE and 
                fact.confidence >= threshold)
    
    def get_value(self, variable: str, default: Any = None) -> Any:
        """الحصول على قيمة المتغير إذا كان صحيحاً"""
        fact = self.facts.get(variable)
        return fact.value if fact and fact.truth == TruthValue.TRUE else default
    
    def get_all(self, truth_filter: Optional[TruthValue] = None,
                source_filter: Optional[str] = None,
                min_confidence: float = 0.0) -> Dict[str, Fact]:
        """
        إرجاع كل الحقائق مع خيارات التصفية
        
        مفيد لتصدير الحالة أو للعرض
        """
        results = {}
        for var, fact in self.facts.items():
            if truth_filter and fact.truth != truth_filter:
                continue
            if source_filter and fact.source != source_filter:
                continue
            if fact.confidence < min_confidence:
                continue
            results[var] = fact
        return results
    
    def get_by_source(self, source: str) -> List[str]:
        """إرجاع كل المتغيرات التي أتت من مصدر معين"""
        return list(self._source_index.get(source, set()))
    
    # ========== إدارة التناقضات والمراجعة ==========
    
    def detect_conflicts(self, candidate_facts: Dict[str, Fact]) -> List[Dict]:
        """
        كشف التناقضات بين حقائق مرشحة للإضافة والحقائق الحالية
        
        Returns:
            قائمة بالتناقضات المكتشفة مع التفاصيل
        """
        conflicts = []
        for var, new_fact in candidate_facts.items():
            old_fact = self.facts.get(var)
            if old_fact and old_fact.contradicts(new_fact):
                conflicts.append({
                    'variable': var,
                    'old_fact': old_fact,
                    'new_fact': new_fact,
                    'conflict_type': 'value_mismatch' if old_fact.value != new_fact.value else 'truth_mismatch'
                })
        return conflicts
    
    def retract(self, variable: str, reason: str = None) -> bool:
        """
        سحب/إزالة حقيقة (للمراجعة غير الرتيبة)
        
        Returns:
            True إذا وُجدت الحقيقة وأزيلت
        """
        if variable not in self.facts:
            return False
        
        old_fact = self.facts.pop(variable)
        self._record_history(variable, 'remove', old_fact, None, reason=reason)
        self._update_source_index(variable, old_fact.source, add=False)
        
        logger.info(f"Retracted fact: {variable} (reason: {reason})")
        return True
    
    def get_history(self, variable: Optional[str] = None, 
                   limit: int = 50) -> List[FactHistoryEntry]:
        """
        استرجاع سجل التغييرات
        
        Args:
            variable: لتصفية التاريخ لمتغير معين (أو None للكل)
            limit: أقصى عدد من السجلات للإرجاع
        """
        entries = self.history
        if variable:
            entries = [e for e in entries if e.variable == variable]
        return entries[-limit:]  # الأحدث أولاً
    
    def snapshot(self) -> Dict[str, Fact]:
        """إنشاء لقطة حالية من كل الحقائق (للتراجع أو المقارنة)"""
        return {k: copy.deepcopy(v) for k, v in self.facts.items()}
    
    def restore_snapshot(self, snapshot: Dict[str, Fact], reason: str = "restore"):
        """استعادة حالة سابقة من لقطة"""
        old_vars = set(self.facts.keys())
        new_vars = set(snapshot.keys())
        
        # إزالة المتغيرات غير الموجودة في اللقطة
        for var in old_vars - new_vars:
            self.retract(var, reason=f"{reason}:removed")
        
        # استعادة/تحديث المتغيرات في اللقطة
        for var, fact in snapshot.items():
            self.facts[var] = copy.deepcopy(fact)
            self._record_history(var, 'restore', self.facts.get(var), fact, reason=reason)
            self._update_source_index(var, fact.source, add=True)
        
        logger.info(f"Restored snapshot: {len(snapshot)} facts (reason: {reason})")
    
    # ========== أدوات مساعدة ==========
    
    def clear(self, source_filter: Optional[str] = None):
        """مسح الحقائق، مع خيار تصفية حسب المصدر"""
        if source_filter:
            vars_to_remove = self.get_by_source(source_filter)
            for var in vars_to_remove:
                self.retract(var, reason=f"clear_source:{source_filter}")
        else:
            self.facts.clear()
            self.history.clear()
            self._source_index.clear()
            logger.info("FactBase cleared")
    
    def export_to_dict(self) -> Dict[str, Any]:
        """تصدير الحقائق كقاموس"""
        return {
            'name': self.name,
            'facts': {
                k: {
                    'value': v.value,
                    'truth': v.truth.name,
                    'confidence': v.confidence,
                    'source': v.source,
                    'justification': v.justification,
                    'timestamp': v.timestamp.isoformat(),
                    'version': v.version
                }
                for k, v in self.facts.items()
            },
            'fact_count': len(self.facts)
        }
    
    @classmethod
    def import_from_dict(cls, data: Dict[str, Any]) -> 'FactBase':
        """استيراد حقائق من قاموس"""
        fb = cls(name=data.get('name', 'imported'))
        for var, fact_data in data.get('facts', {}).items():
            fb.add(
                variable=var,
                value=fact_data['value'],
                truth=TruthValue[fact_data['truth']],
                confidence=fact_data['confidence'],
                source=fact_data.get('source', 'imported'),
                justification=fact_data.get('justification'),
                on_conflict='replace'
            )
        return fb
    
    def __len__(self):
        return len(self.facts)
    
    def __contains__(self, variable: str):
        return variable in self.facts
    
    def __repr__(self):
        return f"FactBase('{self.name}', facts={len(self.facts)}, history={len(self.history)})"
