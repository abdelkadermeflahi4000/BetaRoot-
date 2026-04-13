# betaroot/core/consolidation_engine.py
import time
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

from .unary_logic import create_engine
from .causal_graph import create_causal_builder
from .memory_system import BetaRootMemorySystem, MemoryType, Priority
from .frequency_resonance import FrequencyResonance


@dataclass
class ConsolidationResult:
    success: bool
    new_semantic_facts: int
    patterns_applied: List[str]
    message: str
    timestamp: str


class ConsolidationEngine:
    """
    محرك الدمج (Consolidation): 
    يحول الذاكرة الحدثية (Episodic) إلى ذاكرة دلالية (Semantic) 
    باستخدام Unary Logic + Symbolic Patterns + Causal Reasoning
    """

    def __init__(self, memory: BetaRootMemorySystem):
        self.memory = memory
        self.unary = create_engine("ConsolidationEngine")
        self.causal = create_causal_builder()
        self.resonance = FrequencyResonance()
        
        self.consolidation_count = 0
        self.last_consolidation = datetime.now()

    def should_consolidate(self) -> bool:
        """يقرر متى يجب الدمج"""
        # شروط الدمج:
        # 1. عدد كبير من الأحداث الجديدة
        # 2. ضغط ترددي مرتفع
        # 3. مرور وقت كافٍ
        
        freq_status = self.resonance.calculate_wrong_pressure(f_current=7.83 + 0.15)
        high_pressure = freq_status["correction_needed"]
        
        many_events = len(self.memory.episodic) > 8
        
        time_passed = (datetime.now() - self.last_consolidation).total_seconds() > 300  # كل 5 دقائق
        
        return high_pressure or many_events or time_passed

    def consolidate(self) -> ConsolidationResult:
        """الدمج الرئيسي"""
        if not self.should_consolidate():
            return ConsolidationResult(
                success=False,
                new_semantic_facts=0,
                patterns_applied=[],
                message="لا حاجة للدمج حالياً",
                timestamp=datetime.now().isoformat()
            )

        new_facts = 0
        patterns_used = []

        # معالجة كل حدث في Episodic Memory
        for item_id, item in list(self.memory.episodic.items()):
            if item.priority < 0.5:
                continue  # تجاهل الأحداث الضعيفة

            # 1. تحويل الحدث إلى تمثيل آحادي
            unary_state = self.unary.encode(item.content)

            # 2. تطبيق أنماط رمزية (من الـ 158)
            # في V1 نستخدم نمطين أساسيين
            pattern_result = self._apply_symbolic_patterns(unary_state, item.content)
            if pattern_result:
                patterns_used.append(pattern_result["pattern_name"])

                # 3. استخراج حقيقة دلالية
                semantic_fact = {
                    "derived_from": item_id,
                    "fact": pattern_result["extracted_fact"],
                    "causal_chain": pattern_result["causal_summary"],
                    "confidence": pattern_result["confidence"]
                }

                # 4. تخزين في Semantic Memory
                self.memory.store(
                    content=semantic_fact,
                    memory_type=MemoryType.SEMANTIC,
                    priority=Priority.HIGH,
                    trust=pattern_result["confidence"],
                    source="consolidation_engine",
                    tags=["consolidated", "semantic"]
                )
                new_facts += 1

                # 5. ربط بالـ Causal Graph
                self.causal.add_causal_relation(
                    cause=f"event_{item_id[:8]}",
                    effect=pattern_result["extracted_fact"],
                    relation_type="consolidation"
                )

            # 6. نقل الحدث إلى أرشيف (أو حذفه بعد الدمج)
            # في النسخة الحالية نحتفظ به لكن نضعف أولويته
            item.priority *= 0.6

        self.consolidation_count += 1
        self.last_consolidation = datetime.now()

        return ConsolidationResult(
            success=True,
            new_semantic_facts=new_facts,
            patterns_applied=patterns_used,
            message=f"تم دمج {new_facts} حقيقة دلالية جديدة",
            timestamp=datetime.now().isoformat()
        )

    def _apply_symbolic_patterns(self, unary_state, original_content) -> Dict | None:
        """تطبيق أنماط رمزية بسيطة (Layer 1 & 2 من الـ 158)"""
        content_str = str(original_content).lower()

        # نمط 1: Cause-Effect Detection (من Layer 2)
        if any(word in content_str for word in ["يسبب", "causes", "leads to", "نتج عنه"]):
            return {
                "pattern_name": "Direct_Causation",
                "extracted_fact": f"علاقة سببية: {content_str[:80]}...",
                "causal_summary": "سبب → نتيجة مباشرة",
                "confidence": 0.92
            }

        # نمط 2: Pattern Recognition (من Layer 1)
        if any(word in content_str for word in ["تكرار", "repeated", "cycle", "دورة"]):
            return {
                "pattern_name": "Repetition_Recognition",
                "extracted_fact": f"نمط تكراري مكتشف: {content_str[:60]}...",
                "causal_summary": "دورة متكررة → استقرار",
                "confidence": 0.85
            }

        # نمط 3: Frequency / Resonance Link
        if any(word in content_str for word in ["هرتز", "hz", "تردد", "resonance", "schumann"]):
            return {
                "pattern_name": "Frequency_Resonance",
                "extracted_fact": f"ارتباط ترددي: {content_str[:70]}...",
                "causal_summary": "تردد → تأثير على الوعي",
                "confidence": 0.88
            }

        return None  # لا يوجد نمط مناسب حالياً

    def get_consolidation_stats(self) -> Dict:
        return {
            "total_consolidations": self.consolidation_count,
            "last_consolidation": self.last_consolidation.isoformat(),
            "semantic_facts_count": len(self.memory.semantic),
            "episodic_facts_count": len(self.memory.episodic)
        }


# ====================== مثال استخدام (للاختبار) ======================
if __name__ == "__main__":
    from .memory_system import BetaRootMemorySystem
    
    memory = BetaRootMemorySystem()
    consolidator = ConsolidationEngine(memory)

    # إضافة بعض الأحداث
    memory.store("اكتشفت ضغط ترددي عند 8.4 هرتز أثناء الدورة 12", MemoryType.EPISODIC, Priority.HIGH)
    memory.store("المريض يشعر بتحسن بعد التعرض لتردد 7.83 هرتز", MemoryType.EPISODIC, Priority.MEDIUM)

    print("🔄 بدء عملية الدمج...")
    result = consolidator.consolidate()
    
    print(f"✅ {result.message}")
    print(f"   • تم إنشاء {result.new_semantic_facts} حقيقة دلالية")
    print(f"   • الأنماط المستخدمة: {result.patterns_applied}")
    
    print("\n📊 الإحصائيات بعد الدمج:")
    print(consolidator.get_consolidation_stats())
