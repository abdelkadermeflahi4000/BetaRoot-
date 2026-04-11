# betaroot/memory/types.py
"""
Unified type definitions for BetaRoot Memory System
"""
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime
import hashlib

class MemoryType(Enum):
    FACT = "fact"
    RULE = "rule"
    EXPERIENCE = "experience"
    CONTEXT = "context"
    GOAL = "goal"

class Priority(Enum):
    """أولوية العنصر في الذاكرة: ما الذي نحتفظ به عند الامتلاء؟"""
    CRITICAL = 10    # أساسي للنظام، لا يُحذف أبدًا
    HIGH = 7         # مهم جدًا، يُحفظ طويلًا
    MEDIUM = 4       # عادي، يُحفظ مع مراجعة دورية
    LOW = 2          # ثانوي، يُحذف أولًا عند الحاجة
    TEMPORARY = 1    # مؤقت، يُحذف تلقائيًا بعد وقت قصير

class TrustLevel(Enum):
    """درجة الثقة في مصدر العنصر: ما الذي نثق به في الاستدلال؟"""
    VERIFIED = 1.0      # مثبت تجريبيًا أو منطقيًا
    HIGH_CONFIDENCE = 0.9
    MEDIUM_CONFIDENCE = 0.7
    LOW_CONFIDENCE = 0.5
    UNTRUSTED = 0.3     # مصدر غير موثوق، يحتاج تحقق
    CONTRADICTED = 0.0  # تم دحضه، يُستخدم فقط للتتبع

@dataclass
class MemoryItem:
    """عنصر ذاكرة موحد لجميع الطبقات"""
    content: Dict[str, Any]          # المحتوى الفعلي (fact, rule, etc.)
    memory_type: MemoryType
    priority: Priority = Priority.MEDIUM
    trust: TrustLevel = TrustLevel.MEDIUM_CONFIDENCE
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0            # كم مرة تم الوصول لهذا العنصر؟
    source: str = "system"           # من أين أتى؟ (user, inference, observation...)
    tags: List[str] = field(default_factory=list)  # للفهرسة الدلالية
    meta: Dict[str, Any] = field(default_factory=dict)
    id: str = field(init=False)      # معرف فريد

    def __post_init__(self):
        # توليد معرف فريد بناءً على المحتوى والمصدر
        raw = f"{self.content}{self.source}{self.created_at.isoformat()}"
        self.id = hashlib.sha256(raw.encode()).hexdigest()[:16]

    def touch(self):
        """تحديث وقت آخر وصول وزيادة العداد"""
        self.last_accessed = datetime.now()
        self.access_count += 1

    def importance_score(self) -> float:
        """
        حساب درجة الأهمية الكلية للعنصر
        تستخدم لقرار: ما الذي نحفظ؟ ما الذي نحذف؟
        """
        # وزن الأولوية (40%) + الثقة (30%) + التكرار (20%) + الحداثة (10%)
        priority_weight = {
            Priority.CRITICAL: 1.0, Priority.HIGH: 0.8,
            Priority.MEDIUM: 0.5, Priority.LOW: 0.3, Priority.TEMPORARY: 0.1
        }
        time_decay = max(0.1, 1.0 - (datetime.now() - self.created_at).total_seconds() / 86400)  # اضمحلال يومي
        
        score = (
            priority_weight[self.priority] * 0.4 +
            self.trust.value * 0.3 +
            min(1.0, self.access_count / 10) * 0.2 +  # تشبع بعد 10 وصولات
            time_decay * 0.1
        )
        return round(score, 3)

    def to_dict(self) -> dict:
        return {
            "id": self.id, "content": self.content, "type": self.memory_type.value,
            "priority": self.priority.name, "trust": self.trust.name,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "access_count": self.access_count, "source": self.source,
            "tags": self.tags, "meta": self.meta,
            "importance": self.importance_score()
        }

    @classmethod
    def from_dict(cls,  'MemoryItem':
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["last_accessed"] = datetime.fromisoformat(data["last_accessed"])
        data["memory_type"] = MemoryType[data["type"]]
        data["priority"] = Priority[data["priority"]]
        data["trust"] = TrustLevel[data["trust"]]
        return cls(**data)
