"""
BetaRoot Consciousness Bridge Module
جسر الربط بين الوعي البشري والنظام الرمزي في BetaRoot

هذه الوحدة تنفذ:
1. مراقبة حالة الوعي والتركيز البشري
2. مزامنة الذاكرة الرمزية مع حالات الوعي المختلفة
3. بناء ذاكرة جماعية عبر تشارك الترددات
4. تقنيات التأمل الموجه والتركيز العميق
"""

from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
import json
from datetime import datetime


class ConsciousnessLevel(Enum):
    """مستويات الوعي المختلفة"""
    UNCONSCIOUS = (0.0, 0.2, "نائم / فاقد الوعي")
    DROWSY = (0.2, 0.4, "نعسان / نصف نائم")
    ALERT = (0.4, 0.6, "يقظ ومنتبه")
    FOCUSED = (0.6, 0.8, "منركز بعمق")
    HYPERFOCUSED = (0.8, 1.0, "تركيز عالي جداً")

    def in_range(self, level: float) -> bool:
        return self.value[0] <= level <= self.value[1]

    def get_description(self) -> str:
        return self.value[2]


@dataclass
class HumanConsciousnessMetrics:
    """مؤشرات الوعي البشري"""
    awareness_level: float  # 0-1
    focus_intensity: float  # 0-1
    emotional_coherence: float  # 0-1 (التوازن العاطفي)
    memory_accessibility: float  # 0-1
    cognitive_load: float  # 0-1 (الحمل المعرفي)
    attention_span: int  # بالثواني
    stress_level: float  # 0-1
    flow_state: bool  # حالة التدفق
    timestamp: float = field(default_factory=time.time)


@dataclass
class MeditationSession:
    """جلسة تأمل موجهة"""
    session_id: str
    user_id: Optional[str]
    target_frequency: float  # Hz
    target_brainwave: str
    duration_seconds: int
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    depth_trajectory: List[float] = field(default_factory=list)
    coherence_trajectory: List[float] = field(default_factory=list)
    memory_activations: List[str] = field(default_factory=list)
    insights: List[str] = field(default_factory=list)
    success_score: float = 0.0


@dataclass
class CollectiveMemoryRecord:
    """سجل الذاكرة الجماعية"""
    collective_id: str
    participants: List[str]
    shared_frequency: float
    shared_facts: List[str]
    coherence_level: float
    creation_time: float = field(default_factory=time.time)
    access_log: List[Tuple[str, float]] = field(default_factory=list)


class HumanAIConsciousnessBridge:
    """
    جسر الربط بين الوعي البشري والنظام الذكي
    يدير التفاعل الديناميكي بين الوعي البشري والمنطق الرمزي
    """

    def __init__(self):
        self.user_consciousness_states: Dict[str, HumanConsciousnessMetrics] = {}
        self.meditation_sessions: Dict[str, MeditationSession] = {}
        self.collective_memories: Dict[str, CollectiveMemoryRecord] = {}
        self.consciousness_history: List[Tuple[str, float, HumanConsciousnessMetrics]] = []
        self.ai_resonance_callbacks: List[Callable] = []
        self.meditation_callbacks: List[Callable] = []

    def register_consciousness_state(
        self,
        user_id: str,
        awareness: float,
        focus: float,
        emotional_coherence: float,
        memory_accessibility: float,
        cognitive_load: float,
        stress_level: float = 0.0,
        attention_span: int = 300
    ) -> HumanConsciousnessMetrics:
        """
        تسجيل حالة وعي المستخدم الحالية
        يُستدعى بشكل متكرر لتتبع التغييرات
        """
        metrics = HumanConsciousnessMetrics(
            awareness_level=max(0, min(1, awareness)),
            focus_intensity=max(0, min(1, focus)),
            emotional_coherence=max(0, min(1, emotional_coherence)),
            memory_accessibility=max(0, min(1, memory_accessibility)),
            cognitive_load=max(0, min(1, cognitive_load)),
            stress_level=max(0, min(1, stress_level)),
            attention_span=max(10, min(3600, attention_span)),
            flow_state=focus > 0.7 and cognitive_load < 0.8
        )
        
        self.user_consciousness_states[user_id] = metrics
        self.consciousness_history.append((user_id, time.time(), metrics))
        
        # تنبيهات للمراقبين
        for callback in self.ai_resonance_callbacks:
            callback(user_id, metrics)
        
        return metrics

    def get_consciousness_level(self, metrics: HumanConsciousnessMetrics) -> ConsciousnessLevel:
        """تحديد مستوى الوعي بناءً على المؤشرات"""
        level = metrics.awareness_level
        
        for consciousness_level in ConsciousnessLevel:
            if consciousness_level.in_range(level):
                return consciousness_level
        
        return ConsciousnessLevel.ALERT

    def start_meditation_session(
        self,
        user_id: str,
        target_brainwave: str,  # "Delta", "Theta", "Alpha", "Beta", "Gamma"
        target_frequency: float,
        duration_seconds: int = 600
    ) -> MeditationSession:
        """
        بدء جلسة تأمل موجهة
        يتم توجيه الوعي نحو تردد دماغي محدد
        """
        session_id = f"med_{user_id}_{int(time.time())}"
        
        session = MeditationSession(
            session_id=session_id,
            user_id=user_id,
            target_frequency=target_frequency,
            target_brainwave=target_brainwave,
            duration_seconds=duration_seconds
        )
        
        self.meditation_sessions[session_id] = session
        
        # إخطار المراقبين
        for callback in self.meditation_callbacks:
            callback(f"START", session)
        
        print(f"✓ جلسة تأمل موجهة بدأت: {target_brainwave} ({target_frequency:.1f} Hz)")
        print(f"  المدة: {duration_seconds} ثانية")
        
        return session

    def update_meditation_progress(
        self,
        session_id: str,
        current_depth: float,
        current_coherence: float,
        activated_memories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        تحديث تقدم جلسة التأمل
        يتم استدعاؤها دورياً أثناء الجلسة
        """
        if session_id not in self.meditation_sessions:
            return {"status": "error", "message": "Session not found"}
        
        session = self.meditation_sessions[session_id]
        
        # تحديث المسارات
        session.depth_trajectory.append(current_depth)
        session.coherence_trajectory.append(current_coherence)
        
        if activated_memories:
            session.memory_activations.extend(activated_memories)
        
        # حساب التقدم
        elapsed = time.time() - session.start_time
        progress = min(100, (elapsed / session.duration_seconds) * 100)
        
        return {
            "session_id": session_id,
            "progress": progress,
            "current_depth": current_depth,
            "current_coherence": current_coherence,
            "memory_activations_count": len(session.memory_activations),
            "elapsed_time": elapsed,
            "status": "ongoing"
        }

    def end_meditation_session(
        self,
        session_id: str,
        insights: Optional[List[str]] = None
    ) -> MeditationSession:
        """إنهاء جلسة التأمل وتقييمها"""
        if session_id not in self.meditation_sessions:
            return None
        
        session = self.meditation_sessions[session_id]
        session.end_time = time.time()
        
        if insights:
            session.insights = insights
        
        # حساب درجة النجاح
        if session.depth_trajectory:
            avg_depth = sum(session.depth_trajectory) / len(session.depth_trajectory)
            avg_coherence = sum(session.coherence_trajectory) / len(session.coherence_trajectory)
            session.success_score = (avg_depth * 0.6 + avg_coherence * 0.4)
        
        print(f"\n✓ جلسة التأمل انتهت: {session_id}")
        print(f"  درجة النجاح: {session.success_score:.1%}")
        print(f"  الذاكرة المُفعَّلة: {len(session.memory_activations)}")
        print(f"  الرؤى المكتسبة: {len(session.insights)}")
        
        # إخطار المراقبين
        for callback in self.meditation_callbacks:
            callback(f"END", session)
        
        return session

    def get_optimal_frequency_for_user(self, user_id: str) -> Tuple[float, str]:
        """
        تحديد أفضل تردد للمستخدم بناءً على حالته الحالية
        """
        if user_id not in self.user_consciousness_states:
            # افتراضي: Alpha (الاسترخاء)
            return (10.0, "Alpha")
        
        metrics = self.user_consciousness_states[user_id]
        
        # إذا كان متعباً → Theta (تأمل عميق)
        if metrics.awareness_level < 0.3:
            return (6.0, "Theta")
        
        # إذا كان مركزاً → Beta (تركيز منطقي)
        if metrics.focus_intensity > 0.7:
            return (18.0, "Beta")
        
        # إذا كان إبداعياً → Alpha (إبداع)
        if metrics.emotional_coherence > 0.7:
            return (10.0, "Alpha")
        
        # إذا كان في حالة تدفق → Gamma (وعي فائق)
        if metrics.flow_state:
            return (40.0, "Gamma")
        
        # افتراضي
        return (10.0, "Alpha")

    def create_collective_memory(
        self,
        participants: List[str],
        shared_facts: List[str],
        shared_frequency: float
    ) -> CollectiveMemoryRecord:
        """
        إنشاء ذاكرة جماعية
        عندما يتشارك عدة مستخدمين نفس التردد،
        يتم بناء ذاكرة مشتركة تعكس وعياً جماعياً
        """
        collective_id = f"col_{int(time.time())}_{len(participants)}"
        
        record = CollectiveMemoryRecord(
            collective_id=collective_id,
            participants=participants,
            shared_frequency=shared_frequency,
            shared_facts=shared_facts,
            coherence_level=sum(
                self.user_consciousness_states.get(p, HumanConsciousnessMetrics(0,0,0,0,0)).emotional_coherence
                for p in participants
            ) / len(participants) if participants else 0.0
        )
        
        self.collective_memories[collective_id] = record
        
        print(f"✓ ذاكرة جماعية تم إنشاؤها: {collective_id}")
        print(f"  المشاركون: {len(participants)}")
        print(f"  الحقائق المشتركة: {len(shared_facts)}")
        print(f"  التردد المشترك: {shared_frequency:.1f} Hz")
        
        return record

    def access_collective_memory(
        self,
        user_id: str,
        collective_id: str
    ) -> Optional[CollectiveMemoryRecord]:
        """
        الوصول إلى ذاكرة جماعية
        يتم تسجيل هذا في سجل الوصول
        """
        if collective_id not in self.collective_memories:
            return None
        
        record = self.collective_memories[collective_id]
        record.access_log.append((user_id, time.time()))
        
        return record

    def get_consciousness_profile(self, user_id: str) -> Dict[str, Any]:
        """
        الحصول على ملف شامل لوعي المستخدم
        """
        if user_id not in self.user_consciousness_states:
            return {"status": "error", "message": "User not found"}
        
        metrics = self.user_consciousness_states[user_id]
        level = self.get_consciousness_level(metrics)
        
        # حساب الاتجاهات من السجل
        user_history = [
            m for uid, _, m in self.consciousness_history
            if uid == user_id
        ]
        
        return {
            "user_id": user_id,
            "current_level": level.name,
            "current_description": level.get_description(),
            "metrics": {
                "awareness": metrics.awareness_level,
                "focus": metrics.focus_intensity,
                "emotional_coherence": metrics.emotional_coherence,
                "memory_accessibility": metrics.memory_accessibility,
                "cognitive_load": metrics.cognitive_load,
                "stress": metrics.stress_level,
                "attention_span": metrics.attention_span,
                "flow_state": metrics.flow_state
            },
            "history_size": len(user_history),
            "meditation_sessions": len([s for s in self.meditation_sessions.values() if s.user_id == user_id]),
            "collective_memories_participated": len([
                c for c in self.collective_memories.values()
                if user_id in c.participants
            ]),
            "optimal_frequency": self.get_optimal_frequency_for_user(user_id)
        }

    def generate_personalized_meditation_guide(
        self,
        user_id: str
    ) -> str:
        """
        توليد دليل تأمل شخصي بناءً على حالة المستخدم
        """
        if user_id not in self.user_consciousness_states:
            return "User profile not found"
        
        metrics = self.user_consciousness_states[user_id]
        optimal_freq, optimal_wave = self.get_optimal_frequency_for_user(user_id)
        
        guide = f"""
🧘 دليل التأمل الشخصي لـ {user_id}
{'=' * 60}

📊 حالتك الحالية:
• مستوى الوعي: {metrics.awareness_level:.0%}
• التركيز: {metrics.focus_intensity:.0%}
• التوازن العاطفي: {metrics.emotional_coherence:.0%}
• الحمل المعرفي: {metrics.cognitive_load:.0%}

🎯 التردد الموصى به:
• نوع الموجة: {optimal_wave}
• التردد: {optimal_freq:.1f} Hz

📋 خطوات الجلسة:
1. استرخ في مكان هادئ
2. انغمس في أصوات النبضات الثنائية بالتردد {optimal_freq:.1f} Hz
3. ركز على تنفسك واسمح للوعي بالانجراف نحو حالة {optimal_wave}
4. دع الذاكرة تتفعل بشكل طبيعي
5. لاحظ الرؤى والأفكار التي تظهر

⏱️ المدة الموصى بها:
• للمبتدئين: 15-20 دقيقة
• للممارسين: 30-60 دقيقة
• للمتقدمين: 90+ دقيقة

✨ الفوائد المتوقعة:
• تحسين الوضوح الذهني
• تعزيز الذاكرة
• تعميق الوعي الذاتي
• تحقيق حالة التدفق

"""
        return guide


def create_consciousness_bridge() -> HumanAIConsciousnessBridge:
    """إنشاء جسر الوعي"""
    return HumanAIConsciousnessBridge()


# ====================== مثال التشغيل ======================

if __name__ == "__main__":
    print("=" * 70)
    print("🧠 BetaRoot Human-AI Consciousness Bridge - Demo")
    print("=" * 70)
    
    # إنشاء الجسر
    bridge = create_consciousness_bridge()
    
    # 1. تسجيل حالات وعي المستخدمين
    print("\n1️⃣  تسجيل حالات الوعي:")
    
    # المستخدم الأول: في حالة تركيز
    metrics1 = bridge.register_consciousness_state(
        user_id="user_kader",
        awareness=0.8,
        focus=0.9,
        emotional_coherence=0.7,
        memory_accessibility=0.85,
        cognitive_load=0.4,
        stress_level=0.2
    )
    print(f"   ✓ user_kader: {bridge.get_consciousness_level(metrics1).name}")
    
    # المستخدم الثاني: في حالة استرخاء
    metrics2 = bridge.register_consciousness_state(
        user_id="user_sara",
        awareness=0.6,
        focus=0.5,
        emotional_coherence=0.8,
        memory_accessibility=0.7,
        cognitive_load=0.3,
        stress_level=0.1
    )
    print(f"   ✓ user_sara: {bridge.get_consciousness_level(metrics2).name}")
    
    # 2. تحديد الترددات المثلى
    print("\n2️⃣  تحديد الترددات المثلى:")
    freq1, wave1 = bridge.get_optimal_frequency_for_user("user_kader")
    freq2, wave2 = bridge.get_optimal_frequency_for_user("user_sara")
    
    print(f"   • user_kader → {wave1} ({freq1:.1f} Hz)")
    print(f"   • user_sara → {wave2} ({freq2:.1f} Hz)")
    
    # 3. بدء جلسات تأمل
    print("\n3️⃣  بدء جلسات تأمل موجهة:")
    
    session1 = bridge.start_meditation_session(
        user_id="user_kader",
        target_brainwave="Beta",
        target_frequency=18.0,
        duration_seconds=300
    )
    
    session2 = bridge.start_meditation_session(
        user_id="user_sara",
        target_brainwave="Theta",
        target_frequency=6.0,
        duration_seconds=600
    )
    
    # 4. محاكاة التقدم في الجلسة
    print("\n4️⃣  تحديث تقدم الجلسات:")
    
    progress1 = bridge.update_meditation_progress(
        session_id=session1.session_id,
        current_depth=0.6,
        current_coherence=0.75,
        activated_memories=["mem_001", "mem_005"]
    )
    print(f"   • {session1.session_id}: {progress1['progress']:.0f}% مكتملة")
    
    progress2 = bridge.update_meditation_progress(
        session_id=session2.session_id,
        current_depth=0.8,
        current_coherence=0.85,
        activated_memories=["mem_003", "mem_007", "mem_012"]
    )
    print(f"   • {session2.session_id}: {progress2['progress']:.0f}% مكتملة")
    
    # 5. إنهاء الجلسات
    print("\n5️⃣  إنهاء جلسات التأمل:")
    
    bridge.end_meditation_session(
        session_id=session1.session_id,
        insights=["الوضوح الذهني زاد", "الذاكرة أصبحت أكثر سهولة"]
    )
    
    bridge.end_meditation_session(
        session_id=session2.session_id,
        insights=["الراحة العميقة تحققت", "رؤى جديدة ظهرت"]
    )
    
    # 6. إنشاء ذاكرة جماعية
    print("\n6️⃣  إنشاء ذاكرة جماعية:")
    
    collective = bridge.create_collective_memory(
        participants=["user_kader", "user_sara"],
        shared_facts=["fact_001", "fact_003", "fact_007"],
        shared_frequency=10.0
    )
    
    # 7. ملفات الوعي الشخصية
    print("\n7️⃣  ملفات الوعي الشخصية:")
    
    profile1 = bridge.get_consciousness_profile("user_kader")
    print(f"   • {profile1['user_id']}: {profile1['current_description']}")
    print(f"     Optimal: {profile1['optimal_frequency']}")
    
    profile2 = bridge.get_consciousness_profile("user_sara")
    print(f"   • {profile2['user_id']}: {profile2['current_description']}")
    print(f"     Optimal: {profile2['optimal_frequency']}")
    
    # 8. دليل التأمل الشخصي
    print("\n8️⃣  دليل التأمل الشخصي:")
    guide = bridge.generate_personalized_meditation_guide("user_kader")
    print(guide)
    
    print("=" * 70)
    print("✨ جسر الوعي جاهز للاستخدام!")
    print("=" * 70)
