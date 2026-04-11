# betaroot/memory/prioritization.py
"""
Memory Prioritization & Trust Management Engine
Decides: What to keep? What to forget? What to trust?
"""
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from .types import MemoryItem, Priority, TrustLevel, MemoryType
import logging

logger = logging.getLogger(__name__)

@dataclass
class RetentionPolicy:
    """سياسة الاحتفاظ: متى نحذف؟ متى نرفع الأولوية؟"""
    max_stm_size: int = 20
    max_wm_items: int = 50
    max_ltm_size: int = 10000
    min_trust_for_ltm: TrustLevel = TrustLevel.LOW_CONFIDENCE
    critical_tags: List[str] = None  # عناصر بهذه الوسوم لا تُحذف أبدًا
    auto_promote_after_access: int = 5  # بعد ن وصولات، ارفع الأولوية

    def __post_init__(self):
        if self.critical_tags is None:
            self.critical_tags = ["core", "axiom", "safety"]

class PrioritizationEngine:
    """
    المحرك الذكي لإدارة أولويات الذاكرة والثقة
    
    المسؤول عن:
    - حساب درجة الأهمية لكل عنصر
    - اتخاذ قرار الحفظ/النسيان عند امتلاء الذاكرة
    - ترقية/خفض الثقة بناءً على التكرار والتوافق
    - كشف التناقضات واقتراح المراجعة
    """
    
    def __init__(self, policy: Optional[RetentionPolicy] = None):
        self.policy = policy or RetentionPolicy()
        self.trust_history: Dict[str, List[float]] = {}  # لتتبع تطور الثقة
        
    def should_store_in_ltm(self, item: MemoryItem) -> bool:
        """هل يستحق هذا العنصر الحفظ طويل الأمد؟"""
        # شروط الرفض الفوري
        if item.trust == TrustLevel.CONTRADICTED:
            return False
        if item.priority == Priority.TEMPORARY:
            return False
        if item.trust.value < self.policy.min_trust_for_ltm.value:
            logger.debug(f"Item {item.id} rejected: trust too low ({item.trust.value})")
            return False
        
        # شروط القبول
        if item.priority in (Priority.CRITICAL, Priority.HIGH):
            return True
        if item.access_count >= self.policy.auto_promote_after_access:
            return True
        if any(tag in self.policy.critical_tags for tag in item.tags):
            return True
            
        # قرار مرن بناءً على درجة الأهمية
        return item.importance_score() >= 0.6
    
    def select_forget_candidates(self, items: List[MemoryItem], 
                               target_count: int) -> List[MemoryItem]:
        """
        اختيار العناصر المرشحة للنسيان عند امتلاء الذاكرة
        
        الخوارزمية:
        1. استبعاد العناصر الحرجة والمحمية
        2. ترتيب البقية حسب درجة الأهمية (تصاعديًا)
        3. إرجاع الأقل أهمية حتى نصل للعدد المطلوب
        """
        # 1. تصفية العناصر المحمية
        protected = [
            item for item in items
            if item.priority == Priority.CRITICAL
            or any(tag in self.policy.critical_tags for tag in item.tags)
            or item.trust == TrustLevel.VERIFIED
        ]
        
        # 2. العناصر القابلة للحذف
        candidates = [item for item in items if item not in protected]
        
        # 3. ترتيب حسب الأهمية (الأقل أولاً) + عامل الزمن (الأقدم أولاً عند التساوي)
        candidates.sort(key=lambda x: (x.importance_score(), x.created_at))
        
        return candidates[:target_count]
    
    def update_trust(self, item: MemoryItem, 
                    new_evidence: Dict[str, Any]) -> TrustLevel:
        """
        تحديث درجة الثقة بناءً على أدلة جديدة
        
        يدعم:
        - التعزيز: تكرار التأكيد يرفع الثقة
        - التناقض: دليل معاكس يخفض الثقة
        - المصدر: ثقة المصدر تؤثر في التحديث
        """
        old_trust = item.trust.value
        source_trust = self._source_trust_factor(item.source)
        
        # حساب تأثير الدليل الجديد
        evidence_strength = new_evidence.get("strength", 0.5)  # [0,1]
        evidence_direction = new_evidence.get("supports", True)  # True=يدعم، False=يناقض
        
        # معادلة تحديث الثقة (مبسطة من نموذج بايزي)
        if evidence_direction:
            # تعزيز: ثقة جديدة = ثقة قديمة + (1-قديمة) × قوة_الدليل × ثقة_المصدر
            new_trust = old_trust + (1 - old_trust) * evidence_strength * source_trust
        else:
            # تناقض: ثقة جديدة = ثقة قديمة × (1 - قوة_الدليل × ثقة_المصدر)
            new_trust = old_trust * (1 - evidence_strength * source_trust)
        
        # حدود [0, 1]
        new_trust = max(0.0, min(1.0, new_trust))
        
        # تعيين مستوى ثقة منفصل
        trust_levels = [
            (0.95, TrustLevel.VERIFIED),
            (0.85, TrustLevel.HIGH_CONFIDENCE),
            (0.65, TrustLevel.MEDIUM_CONFIDENCE),
            (0.45, TrustLevel.LOW_CONFIDENCE),
            (0.0, TrustLevel.UNTRUSTED)
        ]
        for threshold, level in trust_levels:
            if new_trust >= threshold:
                updated_trust = level
                break
        
        # تسجيل التاريخ
        self.trust_history.setdefault(item.id, []).append(new_trust)
        
        logger.info(f"Trust updated for {item.id}: {old_trust:.2f} → {new_trust:.2f} ({updated_trust.name})")
        return updated_trust
    
    def detect_contradictions(self, new_item: MemoryItem, 
                            existing_items: List[MemoryItem]) -> List[Dict]:
        """كشف التناقضات المحتملة مع المعرفة الحالية"""
        contradictions = []
        new_key = self._item_key(new_item)
        
        for existing in existing_items:
            if self._items_conflict(new_item, existing):
                contradictions.append({
                    "new_item": new_item.to_dict(),
                    "conflicting_item": existing.to_dict(),
                    "conflict_type": self._classify_conflict(new_item, existing),
                    "suggestion": self._suggest_resolution(new_item, existing)
                })
        
        return contradictions
    
    def _item_key(self, item: MemoryItem) -> str:
        """مفتاح دلالي للمقارنة: نوع + موضوع + مسند"""
        content = item.content
        return f"{item.memory_type.value}:{content.get('subject')}:{content.get('predicate')}"
    
    def _items_conflict(self, a: MemoryItem, b: MemoryItem) -> bool:
        """تحديد ما إذا كان عنصران متناقضين"""
        if self._item_key(a) != self._item_key(b):
            return False
        # تناقض في القيمة
        if a.content.get("value") != b.content.get("value"):
            return True
        # تناقض في الثقة الشديدة
        if {a.trust, b.trust} == {TrustLevel.VERIFIED, TrustLevel.CONTRADICTED}:
            return True
        return False
    
    def _classify_conflict(self, a: MemoryItem, b: MemoryItem) -> str:
        if a.content.get("value") != b.content.get("value"):
            return "value_mismatch"
        if a.trust != b.trust:
            return "trust_mismatch"
        return "unknown"
    
    def _suggest_resolution(self, a: MemoryItem, b: MemoryItem) -> str:
        # قاعدة بسيطة: الأعلى ثقة + الأحدث زمنياً يفوز
        if a.trust.value > b.trust.value:
            return f"Prefer item {a.id} (higher trust: {a.trust.name})"
        elif b.trust.value > a.trust.value:
            return f"Prefer item {b.id} (higher trust: {b.trust.name})"
        elif a.last_accessed > b.last_accessed:
            return f"Prefer item {a.id} (more recent)"
        return "Manual review recommended"
    
    def _source_trust_factor(self, source: str) -> float:
        """عامل ثقة المصدر: بعض المصادر أكثر موثوقية من غيرها"""
        trust_map = {
            "logical_inference": 0.95,
            "verified_observation": 0.9,
            "user_expert": 0.85,
            "user": 0.7,
            "external_api": 0.6,
            "unverified": 0.4,
            "contradicted_source": 0.2
        }
        return trust_map.get(source, 0.5)
