# betaroot/core/memory_system.py
import time
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

from .unary_logic import create_engine
from .causal_graph import create_causal_builder
from .frequency_resonance import FrequencyResonance


class MemoryType(Enum):
    EPISODIC = "episodic"      # أحداث وتجارب
    SEMANTIC = "semantic"      # حقائق وأنماط
    PROCEDURAL = "procedural"  # مهارات وقواعد


class Priority(Enum):
    CRITICAL = 0.95
    HIGH = 0.80
    MEDIUM = 0.60
    LOW = 0.30


@dataclass
class MemoryItem:
    id: str
    content: Any
    memory_type: MemoryType
    priority: float
    trust: float          # 0.0 - 1.0
    timestamp: str
    source: str
    tags: List[str]
    causal_links: List[str] = None  # روابط في الـ Causal Graph
    decay_factor: float = 1.0       # لآلية النسيان

    def to_dict(self):
        return asdict(self)


class BetaRootMemorySystem:
    """
    نظام الذاكرة الذكي لـ BetaRoot
    يجمع بين Episodic + Semantic + Prioritization + Decay + Unary Consistency
    """

    def __init__(self, storage_path: str = "data/memory"):
        self.storage_path = storage_path
        self.unary = create_engine()
        self.causal = create_causal_builder()
        self.resonance = FrequencyResonance()
        
        # الطبقات
        self.working_memory: List[MemoryItem] = []      # قصيرة الأمد
        self.episodic: Dict[str, MemoryItem] = {}       # حدثية
        self.semantic: Dict[str, MemoryItem] = {}       # دلالية (الحقائق المستقرة)

    def store(self, content: Any, 
              memory_type: MemoryType = MemoryType.EPISODIC,
              priority: Priority = Priority.MEDIUM,
              trust: float = 0.8,
              source: str = "cycle_engine",
              tags: List[str] = None) -> str:
        
        item_id = str(uuid.uuid4())
        
        # تحويل إلى تمثيل آحادي + فحص الاتساق
        unary_state = self.unary.encode(content)
        consistency = self.unary.verify_consistency(unary_state)
        
        if not consistency["is_consistent"]:
            trust = min(trust, 0.4)  # خفض الثقة عند وجود تناقض

        item = MemoryItem(
            id=item_id,
            content=content,
            memory_type=memory_type,
            priority=priority.value,
            trust=trust,
            timestamp=datetime.now().isoformat(),
            source=source,
            tags=tags or [],
            causal_links=[],
            decay_factor=1.0
        )

        if memory_type == MemoryType.EPISODIC:
            self.episodic[item_id] = item
            # ربط بالـ Causal Graph
            self.causal.add_causal_relation(
                cause=f"event_{item_id[:8]}",
                effect="knowledge_update",
                relation_type="episodic"
            )
        elif memory_type == MemoryType.SEMANTIC:
            self.semantic[item_id] = item

        # نقل إلى Working Memory مؤقتًا
        self.working_memory.append(item)
        if len(self.working_memory) > 50:  # حد أقصى
            self._consolidate()

        return item_id

    def retrieve(self, query: str, top_k: int = 5, min_trust: float = 0.6) -> List[Dict]:
        """استرجاع ذكي (semantic search + priority + recency)"""
        results = []
        
        # بحث في Semantic أولاً
        for item in self.semantic.values():
            if item.trust >= min_trust:
                # محاكاة similarity بسيطة (يمكن تطويرها بـ embeddings)
                score = self._simple_similarity(query, str(item.content))
                results.append({"item": item, "score": score * item.priority * item.trust})

        # بحث في Episodic
        for item in self.episodic.values():
            if item.trust >= min_trust:
                score = self._simple_similarity(query, str(item.content))
                results.append({"item": item, "score": score * item.priority * item.decay_factor})

        # ترتيب حسب الدرجة
        results.sort(key=lambda x: x["score"], reverse=True)
        return [r["item"].to_dict() for r in results[:top_k]]

    def _simple_similarity(self, query: str, text: str) -> float:
        """محاكاة بسيطة — يمكن استبدالها بـ sentence-transformers"""
        q_words = set(query.lower().split())
        t_words = set(text.lower().split())
        return len(q_words & t_words) / max(len(q_words), 1)

    def _consolidate(self):
        """دمج episodic → semantic (Consolidation)"""
        for item in self.working_memory[:]:
            if item.memory_type == MemoryType.EPISODIC and item.priority > 0.7:
                # استخراج حقيقة دلالية
                semantic_content = {"fact": str(item.content), "derived_from": item.id}
                self.store(semantic_content, MemoryType.SEMANTIC, Priority.HIGH, item.trust * 0.9)
        
        self.working_memory.clear()

    def get_stats(self) -> Dict:
        """إحصائيات الذاكرة"""
        return {
            "episodic_count": len(self.episodic),
            "semantic_count": len(self.semantic),
            "working_count": len(self.working_memory),
            "total_trust_avg": sum(i.trust for i in list(self.semantic.values()) + list(self.episodic.values())) / 
                              max(1, len(self.semantic) + len(self.episodic))
        }

    def apply_decay(self):
        """آلية النسيان التدريجي"""
        for item in list(self.episodic.values()):
            item.decay_factor *= 0.98  # تناقص بطيء
            if item.decay_factor < 0.3 and item.priority < 0.5:
                del self.episodic[item.id]  # نسيان


# ====================== مثال استخدام ======================
if __name__ == "__main__":
    memory = BetaRootMemorySystem()
    
    # تخزين حدث
    memory.store(
        content="اكتشف ضغط ترددي خاطئ عند 8.2 هرتز",
        memory_type=MemoryType.EPISODIC,
        priority=Priority.CRITICAL,
        source="frequency_resonance"
    )
    
    # استرجاع
    results = memory.retrieve("ضغط ترددي خاطئ", top_k=3)
    for r in results:
        print(f"✓ {r['content']} | Trust: {r['trust']} | Priority: {r['priority']}")
    
    print("\n📊 Stats:", memory.get_stats())
