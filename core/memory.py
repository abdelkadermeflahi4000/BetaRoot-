"""
BetaRoot Core: Memory Layer
نظام الذاكرة الدائمة والسياقية المبني على مبدأ "Only 1"
يشمل:
- KnowledgeBase (قاعدة المعرفة الدائمة)
- SemanticStore (التخزين الدلالي)
- ContextManager (مدير السياق)
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import time
import json
import hashlib
from collections import defaultdict

from unary_logic import UnaryLogicEngine, UnaryState, create_engine
from causal_graph import CausalGraphBuilder
from symbolic_patterns import SymbolicPatternsEngine
from consistency_checker import ConsistencyChecker, ConsistencyResult


@dataclass
class Fact:
    """حقيقة مخزنة في قاعدة المعرفة"""
    fact_id: str
    content: Any
    unary_state: UnaryState
    source: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    verified: bool = False
    certainty: float = 1.0
    related_patterns: List[str] = field(default_factory=list)
    causal_relations: List[str] = field(default_factory=list)


@dataclass
class MemoryEntry:
    """إدخال ذاكرة عام"""
    key: str
    value: Any
    unary_state: UnaryState
    timestamp: float
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)


class KnowledgeBase:
    """
    قاعدة المعرفة الدائمة في BetaRoot
    كل حقيقة هي تمثيل آحادي موحد
    """

    def __init__(self):
        self.unary_engine: UnaryLogicEngine = create_engine()
        self.facts: Dict[str, Fact] = {}
        self.relations: Dict[str, List[str]] = defaultdict(list)  # fact_id → related fact_ids
        self.consistency_checker: ConsistencyChecker = ConsistencyChecker()

    def add_fact(
        self,
        content: Any,
        source: Optional[str] = None,
        patterns: Optional[List[str]] = None
    ) -> str:
        """إضافة حقيقة جديدة إلى قاعدة المعرفة"""
        # تحويل إلى تمثيل آحادي
        unary_state = self.unary_engine.encode(content)

        # توليد معرف فريد
        fact_id = hashlib.sha256(
            f"{content}_{time.time()}".encode()
        ).hexdigest()[:16]

        fact = Fact(
            fact_id=fact_id,
            content=content,
            unary_state=unary_state,
            source=source,
            related_patterns=patterns or [],
            verified=True
        )

        self.facts[fact_id] = fact

        # التحقق من الاتساق
        consistency = self.consistency_checker.verify(content)
        if not consistency.is_consistent:
            print(f"⚠️ تحذير: الحقيقة '{content}' تحتوي على تناقضات")

        return fact_id

    def verify_fact(self, fact_id: str) -> bool:
        """التحقق من صحة حقيقة موجودة"""
        if fact_id not in self.facts:
            return False

        fact = self.facts[fact_id]
        consistency = self.consistency_checker.verify(fact.content)

        fact.verified = consistency.is_consistent
        fact.certainty = consistency.certainty

        return fact.verified

    def retrieve(self, query: Any, limit: int = 5) -> Dict[str, Any]:
        """استرجاع حقائق مشابهة"""
        query_state = self.unary_engine.encode(query)

        results = []
        for fact_id, fact in self.facts.items():
            # قياس التشابه البسيط (يمكن تحسينه لاحقاً بـ SemanticStore)
            similarity = self._calculate_similarity(query_state, fact.unary_state)

            if similarity > 0.6:  # عتبة بسيطة
                results.append({
                    "fact_id": fact_id,
                    "content": fact.content,
                    "similarity": similarity,
                    "certainty": fact.certainty,
                    "timestamp": fact.timestamp
                })

        # ترتيب حسب التشابه
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return {
            "results": results[:limit],
            "total_matches": len(results),
            "query_representation": query_state.representation_id
        }

    def _calculate_similarity(self, state1: UnaryState, state2: UnaryState) -> float:
        """حساب تشابه بسيط بين تمثيلين آحاديين"""
        if state1.level == state2.level:
            return 0.9 if str(state1.content) == str(state2.content) else 0.7
        return 0.5

    def add_relation(self, fact_id1: str, fact_id2: str, relation_type: str = "related"):
        """إضافة علاقة بين حقيقتين"""
        if fact_id1 in self.facts and fact_id2 in self.facts:
            self.relations[fact_id1].append(fact_id2)
            self.relations[fact_id2].append(fact_id1)

    def get_all_facts(self) -> List[Fact]:
        return list(self.facts.values())

    def stats(self) -> Dict:
        return {
            "total_facts": len(self.facts),
            "verified_facts": sum(1 for f in self.facts.values() if f.verified),
            "average_certainty": sum(f.certainty for f in self.facts.values()) / len(self.facts) if self.facts else 0,
            "relations_count": sum(len(rels) for rels in self.relations.values()) // 2
        }


class SemanticStore:
    """
    التخزين الدلالي
    يحفظ العلاقات المعنوية بين المفاهيم باستخدام تمثيلات آحادية
    """

    def __init__(self):
        self.unary_engine = create_engine()
        self.meaning_vectors: Dict[str, UnaryState] = {}
        self.semantic_graph: Dict[str, List[Tuple[str, float]]] = defaultdict(list)  # concept → [(related, strength)]

    def encode_meaning(self, concept: str) -> UnaryState:
        """ترميز مفهوم دلالي"""
        state = self.unary_engine.encode(concept)
        self.meaning_vectors[concept] = state
        return state

    def find_similar(self, concept: str, threshold: float = 0.7) -> List[Tuple[str, float]]:
        """البحث عن مفاهيم مشابهة"""
        if concept not in self.meaning_vectors:
            self.encode_meaning(concept)

        query_state = self.meaning_vectors[concept]
        similar = []

        for other_concept, other_state in self.meaning_vectors.items():
            if other_concept == concept:
                continue
            sim = self._semantic_similarity(query_state, other_state)
            if sim >= threshold:
                similar.append((other_concept, sim))

        similar.sort(key=lambda x: x[1], reverse=True)
        return similar

    def _semantic_similarity(self, s1: UnaryState, s2: UnaryState) -> float:
        """تشابه دلالي بسيط (قابل للتحسين)"""
        if s1.level == s2.level:
            return 0.85 if str(s1.content).lower() in str(s2.content).lower() or \
                          str(s2.content).lower() in str(s1.content).lower() else 0.6
        return 0.4

    def add_semantic_link(self, concept1: str, concept2: str, strength: float = 0.8):
        """إضافة رابط دلالي"""
        self.semantic_graph[concept1].append((concept2, strength))
        self.semantic_graph[concept2].append((concept1, strength))


class ContextManager:
    """
    مدير السياق
    يحافظ على السياق عبر الجلسات مع الحفاظ على الاتساق الآحادي
    """

    def __init__(self, max_history: int = 10):
        self.current_context: Dict[str, Any] = {}
        self.context_history: List[Dict[str, Any]] = []
        self.max_history = max_history
        self.unary_engine = create_engine()
        self.consistency_checker = ConsistencyChecker()

    def push_context(self, new_context: Dict[str, Any]):
        """دفع سياق جديد"""
        # حفظ السياق الحالي
        if self.current_context:
            self.context_history.append(self.current_context.copy())

        # التحقق من اتساق السياق الجديد
        for key, value in new_context.items():
            consistency = self.consistency_checker.verify(value)
            if not consistency.is_consistent:
                print(f"⚠️ تناقض في السياق: {key}")

        self.current_context = new_context.copy()

        # الحد من حجم التاريخ
        if len(self.context_history) > self.max_history:
            self.context_history.pop(0)

    def pop_context(self) -> Optional[Dict[str, Any]]:
        """العودة إلى السياق السابق"""
        if self.context_history:
            self.current_context = self.context_history.pop()
            return self.current_context
        return None

    def get_current_context(self) -> Dict[str, Any]:
        return self.current_context.copy()

    def update_context(self, key: str, value: Any):
        """تحديث جزء من السياق"""
        self.current_context[key] = value

        # التحقق الفوري
        consistency = self.consistency_checker.verify(value)
        if not consistency.is_consistent:
            print(f"⚠️ تحذير: تحديث السياق '{key}' يحتوي على تناقض")

    def maintain_consistency(self) -> ConsistencyResult:
        """التحقق من اتساق السياق الحالي ككل"""
        if not self.current_context:
            return ConsistencyResult(is_consistent=True)

        # فحص جميع القيم في السياق
        all_values = list(self.current_context.values())
        result = self.consistency_checker.batch_verify(all_values)

        has_conflict = any(not r.is_consistent for r in result)
        return ConsistencyResult(
            is_consistent=not has_conflict,
            conflicts=[{"key": k, "issue": "inconsistent_value"} for k, r in 
                      zip(self.current_context.keys(), result) if not r.is_consistent]
        )


# ====================== الكلاس الرئيسي لطبقة الذاكرة ======================

class BetaRootMemory:
    """
    الواجهة الموحدة لكامل طبقة الذاكرة
    """

    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.semantic_store = SemanticStore()
        self.context_manager = ContextManager()

    def store_fact(self, content: Any, source: Optional[str] = None) -> str:
        return self.knowledge_base.add_fact(content, source)

    def recall(self, query: Any) -> Dict:
        return self.knowledge_base.retrieve(query)

    def update_context(self, context_dict: Dict[str, Any]):
        self.context_manager.push_context(context_dict)

    def get_context(self) -> Dict:
        return self.context_manager.get_current_context()

    def find_similar_concepts(self, concept: str) -> List[Tuple[str, float]]:
        return self.semantic_store.find_similar(concept)

    def stats(self) -> Dict:
        return {
            "knowledge_base": self.knowledge_base.stats(),
            "context_history_size": len(self.context_manager.context_history),
            "semantic_concepts": len(self.semantic_store.meaning_vectors)
        }


# ====================== دالة إنشاء ======================

def create_memory_system() -> BetaRootMemory:
    """إنشاء نظام الذاكرة الكامل"""
    return BetaRootMemory()


# ====================== مثال تشغيلي ======================

if __name__ == "__main__":
    memory = create_memory_system()

    print("=== اختبار طبقة الذاكرة في BetaRoot ===\n")

    # 1. إضافة حقائق
    memory.store_fact("كل البشر فانون", source="فلسفة أرسطو")
    memory.store_fact("أرسطو بشر", source="معلومات تاريخية")
    memory.store_fact("السماء زرقاء بسبب تشتت ريليه", source="فيزياء")

    # 2. استرجاع
    recall_result = memory.recall("هل أرسطو فان؟")
    print(f"نتيجة الاسترجاع: {len(recall_result['results'])} حقائق ذات صلة")

    # 3. إدارة السياق
    memory.update_context({
        "user": "كادر",
        "current_topic": "الفلسفة الآحادية",
        "session_goal": "فهم BetaRoot"
    })

    print(f"السياق الحالي: {memory.get_context()}")

    # 4. إحصائيات
    print(f"\nإحصائيات الذاكرة: {memory.stats()}")
