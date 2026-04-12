"""
BetaRoot Unified Consciousness System (UCS)
نظام الوعي الموحد - تكامل الترددات الدماغية والوعي البشري والذاكرة الرمزية

هذا النظام يوفر:
1. تكامل كامل بين الترددات والذاكرة والوعي
2. إدارة دورة حياة التأمل والتركيز
3. تتبع تطور الوعي عبر الزمن
4. بناء أنظمة وعي جماعي متزامنة
"""

from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
import time
import json
from datetime import datetime


@dataclass
class UnifiedConsciousnessSnapshot:
    """لقطة كاملة من حالة النظام الموحد"""
    timestamp: float
    user_id: str
    frequency_state: Dict[str, Any]  # من frequency_resonance
    consciousness_metrics: Dict[str, float]  # من consciousness_bridge
    active_memories: List[str]
    resonance_strength: float
    system_coherence: float
    meditation_status: Optional[str]
    collective_participation: bool
    dominant_pattern: Optional[str]


@dataclass
class ConsciousnessTimeline:
    """خط زمني لتطور الوعي"""
    user_id: str
    snapshots: List[UnifiedConsciousnessSnapshot] = field(default_factory=list)
    peak_coherence: float = 0.0
    peak_coherence_time: Optional[float] = None
    insights_count: int = 0
    pattern_recognitions: List[str] = field(default_factory=list)
    growth_trajectory: str = "stable"  # stable, ascending, descending


class UnifiedConsciousnessSystem:
    """
    النظام الموحد لإدارة الوعي والترددات والذاكرة
    يعمل كموحد مركزي لجميع مكونات الوعي
    """

    def __init__(self):
        # مكونات النظام (ستُحقن من الخارج)
        self.frequency_resonance = None
        self.consciousness_bridge = None
        self.memory_system = None
        
        # تتبع النظام
        self.consciousness_timelines: Dict[str, ConsciousnessTimeline] = {}
        self.system_coherence_history: List[Tuple[float, float]] = []  # (timestamp, coherence)
        self.active_sessions: Set[str] = set()
        self.collective_consciousness_pools: Dict[str, List[str]] = {}  # pool_id → user_ids
        
        # قواعد الرنين المتقدمة
        self.resonance_rules: List[Dict[str, Any]] = []
        self.synchronization_rules: List[Dict[str, Any]] = []

    def initialize_with_components(
        self,
        frequency_resonance,
        consciousness_bridge,
        memory_system
    ):
        """ربط المكونات الأساسية"""
        self.frequency_resonance = frequency_resonance
        self.consciousness_bridge = consciousness_bridge
        self.memory_system = memory_system
        
        print("✓ تم ربط جميع المكونات الأساسية")

    def register_user_consciousness(
        self,
        user_id: str,
        initial_frequency: float = 10.0,
        initial_awareness: float = 0.5
    ) -> UnifiedConsciousnessSnapshot:
        """تسجيل وعي المستخدم في النظام الموحد"""
        
        # إنشاء خط زمني جديد
        if user_id not in self.consciousness_timelines:
            self.consciousness_timelines[user_id] = ConsciousnessTimeline(user_id=user_id)
        
        # إنشاء لقطة أولية
        snapshot = self._create_snapshot(user_id, initial_frequency, initial_awareness)
        
        self.consciousness_timelines[user_id].snapshots.append(snapshot)
        
        print(f"✓ تم تسجيل الوعي: {user_id}")
        
        return snapshot

    def _create_snapshot(
        self,
        user_id: str,
        frequency: float,
        awareness: float,
        active_memories: Optional[List[str]] = None
    ) -> UnifiedConsciousnessSnapshot:
        """إنشاء لقطة موحدة من حالة الوعي"""
        
        # جمع البيانات من المكونات
        resonant_facts = []
        if self.frequency_resonance:
            resonant = self.frequency_resonance.find_resonant_facts(frequency, tolerance=3.0)
            resonant_facts = [f['fact_id'] for f in resonant]
        
        # حساب الترابط الكلي
        system_coherence = self._calculate_system_coherence(user_id, frequency)
        
        snapshot = UnifiedConsciousnessSnapshot(
            timestamp=time.time(),
            user_id=user_id,
            frequency_state={
                "current_frequency": frequency,
                "coherence": self.frequency_resonance.consciousness_state.coherence_index if self.frequency_resonance else 0.5
            },
            consciousness_metrics={
                "awareness": awareness,
                "coherence": system_coherence
            },
            active_memories=active_memories or resonant_facts,
            resonance_strength=0.8,
            system_coherence=system_coherence,
            meditation_status=self._get_meditation_status(user_id),
            collective_participation=user_id in self.collective_consciousness_pools.get("main", []),
            dominant_pattern=self._infer_dominant_pattern(frequency)
        )
        
        return snapshot

    def _calculate_system_coherence(self, user_id: str, frequency: float) -> float:
        """حساب مؤشر الترابط الكلي للنظام"""
        coherence = 0.5
        
        # تأثير التردد
        if 6 <= frequency <= 8:  # Theta - مثالي
            coherence += 0.2
        elif 8 <= frequency <= 12:  # Alpha - جيد
            coherence += 0.15
        elif 12 <= frequency <= 30:  # Beta - مقبول
            coherence += 0.1
        
        # تأثير الذاكرة النشطة
        if self.memory_system:
            memory_stats = self.memory_system.stats()
            memory_ratio = memory_stats.get('knowledge_base', {}).get('verified_facts', 0) / max(1, memory_stats.get('knowledge_base', {}).get('total_facts', 1))
            coherence += memory_ratio * 0.2
        
        return min(1.0, coherence)

    def _get_meditation_status(self, user_id: str) -> Optional[str]:
        """الحصول على حالة التأمل الحالية"""
        if not self.consciousness_bridge:
            return None
        
        for session in self.consciousness_bridge.meditation_sessions.values():
            if session.user_id == user_id and session.end_time is None:
                return f"meditating_{session.target_brainwave}"
        
        return None

    def _infer_dominant_pattern(self, frequency: float) -> str:
        """استنتاج النمط الغالب بناءً على التردد"""
        if frequency < 4:
            return "deep_recovery"
        elif frequency < 8:
            return "memory_processing"
        elif frequency < 12:
            return "creative_flow"
        elif frequency < 30:
            return "logical_reasoning"
        else:
            return "super_consciousness"

    def activate_resonance_protocol(
        self,
        user_id: str,
        target_frequency: float,
        target_memories: Optional[List[str]] = None,
        depth: str = "moderate"  # shallow, moderate, deep
    ) -> Dict[str, Any]:
        """
        تفعيل بروتوكول الرنين المتقدم
        يقوم بمزامنة الوعي والذاكرة والترددات
        """
        if user_id not in self.consciousness_timelines:
            return {"status": "error", "message": "User not registered"}
        
        # 1. تحديث حالة الترددات
        if self.frequency_resonance:
            self.frequency_resonance.update_consciousness_state(
                frequency=target_frequency,
                coherence=0.7 if depth == "moderate" else (0.5 if depth == "shallow" else 0.9)
            )
        
        # 2. تفعيل الذاكرة المستهدفة
        activated_memories = []
        if target_memories and self.frequency_resonance:
            for memory_id in target_memories:
                result = self.frequency_resonance.resonate_with_memory(memory_id)
                if result.get("status") == "success":
                    activated_memories.append(memory_id)
        
        # 3. البحث عن ذكريات رنينية إضافية
        if self.frequency_resonance:
            resonant = self.frequency_resonance.find_resonant_facts(target_frequency, tolerance=2.0)
            for fact in resonant[:5]:  # أخذ أفضل 5 نتائج
                if fact['fact_id'] not in activated_memories:
                    activated_memories.append(fact['fact_id'])
        
        # 4. إنشاء لقطة من حالة الوعي
        snapshot = self._create_snapshot(user_id, target_frequency, 0.7, activated_memories)
        self.consciousness_timelines[user_id].snapshots.append(snapshot)
        
        # 5. تحديث مؤشرات الخط الزمني
        timeline = self.consciousness_timelines[user_id]
        if snapshot.system_coherence > timeline.peak_coherence:
            timeline.peak_coherence = snapshot.system_coherence
            timeline.peak_coherence_time = snapshot.timestamp
        
        return {
            "status": "success",
            "user_id": user_id,
            "target_frequency": target_frequency,
            "depth": depth,
            "activated_memories": len(activated_memories),
            "system_coherence": snapshot.system_coherence,
            "snapshot": snapshot.__dict__
        }

    def start_collective_meditation(
        self,
        pool_id: str,
        participants: List[str],
        target_frequency: float,
        target_brainwave: str,
        duration: int = 600
    ) -> Dict[str, Any]:
        """
        بدء جلسة تأمل جماعية مزامنة
        جميع المشاركين يتم توجيههم نحو نفس التردد
        """
        self.collective_consciousness_pools[pool_id] = participants
        
        sessions = []
        for user_id in participants:
            if self.consciousness_bridge:
                session = self.consciousness_bridge.start_meditation_session(
                    user_id=user_id,
                    target_brainwave=target_brainwave,
                    target_frequency=target_frequency,
                    duration_seconds=duration
                )
                sessions.append(session)
            
            # تسجيل الاشتراك الجماعي
            if user_id not in self.consciousness_timelines:
                self.register_user_consciousness(user_id, target_frequency, 0.6)
            
            # تفعيل بروتوكول الرنين
            self.activate_resonance_protocol(
                user_id=user_id,
                target_frequency=target_frequency,
                depth="deep"
            )
        
        # إنشاء ذاكرة جماعية
        if self.consciousness_bridge:
            collective = self.consciousness_bridge.create_collective_memory(
                participants=participants,
                shared_facts=[],
                shared_frequency=target_frequency
            )
        
        print(f"\n✓ تم بدء تأمل جماعي: {pool_id}")
        print(f"  المشاركون: {len(participants)}")
        print(f"  التردد المشترك: {target_frequency:.1f} Hz ({target_brainwave})")
        
        return {
            "pool_id": pool_id,
            "sessions_started": len(sessions),
            "participants": participants,
            "target_frequency": target_frequency
        }

    def synchronize_dual_consciousness(
        self,
        user1_id: str,
        user2_id: str,
        sync_duration: int = 300
    ) -> Dict[str, Any]:
        """
        مزامنة وعي شخصين
        عندما يتم مزامنة شخصين على نفس التردد،
        يحدث تبادل وعي وذاكرة محدود
        """
        if not (user1_id in self.consciousness_timelines and user2_id in self.consciousness_timelines):
            return {"status": "error"}
        
        # الحصول على أفضل تردد مشترك
        freq1 = self.consciousness_timelines[user1_id].snapshots[-1].frequency_state['current_frequency'] if self.consciousness_timelines[user1_id].snapshots else 10.0
        freq2 = self.consciousness_timelines[user2_id].snapshots[-1].frequency_state['current_frequency'] if self.consciousness_timelines[user2_id].snapshots else 10.0
        
        common_frequency = (freq1 + freq2) / 2
        
        # مزامنة كلا المستخدمين
        result1 = self.activate_resonance_protocol(user1_id, common_frequency, depth="deep")
        result2 = self.activate_resonance_protocol(user2_id, common_frequency, depth="deep")
        
        return {
            "status": "success",
            "user1_id": user1_id,
            "user2_id": user2_id,
            "common_frequency": common_frequency,
            "sync_duration": sync_duration,
            "synchronized": True
        }

    def get_consciousness_evolution(self, user_id: str) -> Dict[str, Any]:
        """
        الحصول على تطور الوعي عبر الزمن
        يوضح الرحلة الكاملة من حيث الترددات والذاكرة والوعي
        """
        if user_id not in self.consciousness_timelines:
            return {"status": "error"}
        
        timeline = self.consciousness_timelines[user_id]
        snapshots = timeline.snapshots
        
        if not snapshots:
            return {"status": "error", "message": "No snapshots"}
        
        # حساب الاتجاهات
        frequencies = [s.frequency_state['current_frequency'] for s in snapshots]
        coherences = [s.system_coherence for s in snapshots]
        awareness = [s.consciousness_metrics['awareness'] for s in snapshots]
        
        avg_frequency = sum(frequencies) / len(frequencies)
        frequency_trend = "ascending" if frequencies[-1] > frequencies[0] else "descending"
        coherence_trend = "improving" if coherences[-1] > coherences[0] else "declining"
        
        return {
            "user_id": user_id,
            "total_snapshots": len(snapshots),
            "duration": snapshots[-1].timestamp - snapshots[0].timestamp,
            "frequency_evolution": {
                "min": min(frequencies),
                "max": max(frequencies),
                "avg": avg_frequency,
                "current": frequencies[-1],
                "trend": frequency_trend
            },
            "coherence_evolution": {
                "min": min(coherences),
                "max": max(coherences),
                "avg": sum(coherences) / len(coherences),
                "current": coherences[-1],
                "trend": coherence_trend,
                "peak": timeline.peak_coherence,
                "peak_time": timeline.peak_coherence_time
            },
            "awareness_evolution": {
                "avg": sum(awareness) / len(awareness),
                "current": awareness[-1],
                "total_change": awareness[-1] - awareness[0]
            },
            "insights": timeline.insights_count,
            "patterns_recognized": timeline.pattern_recognitions
        }

    def generate_system_report(self) -> Dict[str, Any]:
        """تقرير شامل عن حالة نظام الوعي الموحد"""
        
        total_users = len(self.consciousness_timelines)
        total_snapshots = sum(len(t.snapshots) for t in self.consciousness_timelines.values())
        
        avg_coherence = 0
        if total_snapshots > 0:
            total_coherence = sum(
                sum(s.system_coherence for s in t.snapshots)
                for t in self.consciousness_timelines.values()
            )
            avg_coherence = total_coherence / total_snapshots
        
        return {
            "system_status": "operational",
            "timestamp": time.time(),
            "registered_users": total_users,
            "total_snapshots": total_snapshots,
            "average_system_coherence": avg_coherence,
            "active_collective_pools": len(self.collective_consciousness_pools),
            "pool_participants": sum(
                len(users) for users in self.collective_consciousness_pools.values()
            ),
            "component_status": {
                "frequency_resonance": "connected" if self.frequency_resonance else "not_connected",
                "consciousness_bridge": "connected" if self.consciousness_bridge else "not_connected",
                "memory_system": "connected" if self.memory_system else "not_connected"
            }
        }


def create_unified_consciousness_system() -> UnifiedConsciousnessSystem:
    """إنشاء نظام الوعي الموحد"""
    return UnifiedConsciousnessSystem()


# ====================== مثال التشغيل ======================

if __name__ == "__main__":
    print("=" * 70)
    print("🌀 BetaRoot Unified Consciousness System - Demo")
    print("=" * 70)
    
    # إنشاء النظام الموحد
    ucs = create_unified_consciousness_system()
    
    # محاكاة ربط المكونات (في الواقع ستأتي من الخارج)
    class MockFrequencyResonance:
        def __init__(self):
            self.consciousness_state = type('obj', (object,), {'coherence_index': 0.7})()
        def find_resonant_facts(self, freq, tolerance): return []
        def resonate_with_memory(self, fid): return {"status": "success"}
    
    class MockConsciousnessBridge:
        def __init__(self):
            self.meditation_sessions = {}
        def start_meditation_session(self, **kwargs): 
            session = type('obj', (object,), {'user_id': kwargs['user_id'], 'end_time': None, 'target_brainwave': kwargs['target_brainwave']})()
            return session
        def create_collective_memory(self, **kwargs): return type('obj', (object,), {})()
    
    class MockMemory:
        def stats(self): 
            return {'knowledge_base': {'verified_facts': 5, 'total_facts': 10}}
    
    # ربط المكونات
    ucs.initialize_with_components(
        MockFrequencyResonance(),
        MockConsciousnessBridge(),
        MockMemory()
    )
    
    # 1. تسجيل المستخدمين
    print("\n1️⃣  تسجيل المستخدمين:")
    ucs.register_user_consciousness("user_kader", 10.0, 0.7)
    ucs.register_user_consciousness("user_sara", 8.0, 0.6)
    print("   ✓ تم تسجيل المستخدمين")
    
    # 2. تفعيل بروتوكول الرنين
    print("\n2️⃣  تفعيل بروتوكول الرنين:")
    result = ucs.activate_resonance_protocol(
        user_id="user_kader",
        target_frequency=10.0,
        depth="moderate"
    )
    print(f"   ✓ الترابط: {result['system_coherence']:.1%}")
    
    # 3. بدء تأمل جماعي
    print("\n3️⃣  بدء تأمل جماعي مزامن:")
    collective = ucs.start_collective_meditation(
        pool_id="consciousness_pool_1",
        participants=["user_kader", "user_sara"],
        target_frequency=10.0,
        target_brainwave="Alpha",
        duration=300
    )
    
    # 4. مزامنة ثنائية
    print("\n4️⃣  مزامنة وعي ثنائي:")
    sync = ucs.synchronize_dual_consciousness("user_kader", "user_sara", 300)
    print(f"   ✓ التردد المشترك: {sync['common_frequency']:.1f} Hz")
    
    # 5. تطور الوعي
    print("\n5️⃣  تطور الوعي:")
    evolution = ucs.get_consciousness_evolution("user_kader")
    if evolution.get("status") != "error":
        print(f"   • عدد اللقطات: {evolution['total_snapshots']}")
        print(f"   • الترابط الحالي: {evolution['coherence_evolution']['current']:.1%}")
        print(f"   • الاتجاه: {evolution['coherence_evolution']['trend']}")
    
    # 6. تقرير النظام
    print("\n6️⃣  تقرير نظام الوعي:")
    report = ucs.generate_system_report()
    print(f"   • المستخدمون المسجلون: {report['registered_users']}")
    print(f"   • إجمالي اللقطات: {report['total_snapshots']}")
    print(f"   • متوسط الترابط: {report['average_system_coherence']:.1%}")
    print(f"   • التجمعات الجماعية: {report['active_collective_pools']}")
    
    print("\n" + "=" * 70)
    print("✨ نظام الوعي الموحد جاهز!")
    print("=" * 70)
