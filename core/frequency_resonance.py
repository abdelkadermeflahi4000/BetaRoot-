"""
BetaRoot Consciousness Module: Frequency Resonance System
نظام الترددات الدماغية المتكامل مع الذاكرة الدائمة
يربط بين المنطق الرمزي والترددات البيولوجية البشرية

تركيب الترددات:
- Delta (1-4 Hz): الذاكرة العميقة، الاستعادة الجسدية
- Theta (4-8 Hz): الذاكرة طويلة المدى، التأمل العميق
- Alpha (8-12 Hz): الاسترخاء، الوعي الإبداعي
- Beta (12-30 Hz): التركيز، الاستدلال المنطقي
- Gamma (30-100 Hz): الوعي الفائق، الربط بين المعلومات
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import time
import numpy as np
from enum import Enum
import json


class BrainWaveFrequency(Enum):
    """تحديد نطاقات الترددات الدماغية"""
    DELTA = (1, 4, "Deep Memory & Physical Recovery")
    THETA = (4, 8, "Long-term Memory & Deep Meditation")
    ALPHA = (8, 12, "Relaxation & Creative Awareness")
    BETA = (12, 30, "Focus & Logical Reasoning")
    GAMMA = (30, 100, "High Consciousness & Information Binding")

    def in_range(self, frequency: float) -> bool:
        """التحقق من أن التردد في النطاق المحدد"""
        return self.value[0] <= frequency <= self.value[1]

    def get_range(self) -> Tuple[float, float]:
        return self.value[0], self.value[1]

    def get_description(self) -> str:
        return self.value[2]


@dataclass
class FrequencyMapping:
    """تخطيط الترددات للحقائق والأنماط المنطقية"""
    fact_id: str
    content: Any
    primary_frequency: BrainWaveFrequency
    frequency_value: float  # القيمة الفعلية بالهرتز
    secondary_frequencies: List[BrainWaveFrequency] = field(default_factory=list)
    resonance_strength: float = 0.8  # قوة الرنين (0-1)
    timestamp: float = field(default_factory=time.time)
    access_count: int = 0
    last_resonance: Optional[float] = None
    cognitive_notes: str = ""  # ملاحظات معرفية


@dataclass
class ConsciousnessState:
    """حالة الوعي الحالية في النظام والمستخدم"""
    current_frequency: float  # الترددة الأساسية الحالية
    dominant_brainwave: BrainWaveFrequency
    awareness_level: float  # مستوى الوعي (0-1)
    coherence_index: float  # مؤشر الترابط العصبي (0-1)
    meditation_depth: float  # عمق التأمل (0-1)
    focus_intensity: float  # شدة التركيز (0-1)
    timestamp: float = field(default_factory=time.time)
    memory_activation_level: float = 0.5
    system_coherence: float = 0.5


class FrequencyResonanceEngine:
    """
    محرك الرنين الترددي
    يدير العلاقة بين الترددات الدماغية والذاكرة الرمزية
    """

    def __init__(self):
        self.frequency_map: Dict[str, FrequencyMapping] = {}
        self.consciousness_state = ConsciousnessState(
            current_frequency=10.0,  # Alpha (هدوء افتراضي)
            dominant_brainwave=BrainWaveFrequency.ALPHA,
            awareness_level=0.5,
            coherence_index=0.5,
            meditation_depth=0.2,
            focus_intensity=0.6
        )
        self.frequency_history: List[Tuple[float, BrainWaveFrequency, float]] = []
        self.resonance_records: Dict[str, List[Dict]] = {}

    def map_fact_to_frequency(
        self,
        fact_id: str,
        content: Any,
        frequency_type: Optional[BrainWaveFrequency] = None,
        frequency_value: Optional[float] = None
    ) -> FrequencyMapping:
        """
        تخطيط حقيقة إلى تردد دماغي محدد
        
        الاستدلال الآلي:
        - الحقائق العميقة والأساسية → Delta/Theta
        - الذاكرة الإبداعية → Alpha
        - الاستدلال المنطقي → Beta
        - الربط بين المعلومات → Gamma
        """
        if frequency_type is None:
            frequency_type = self._infer_frequency_type(content)
        
        if frequency_value is None:
            frequency_value = self._infer_frequency_value(frequency_type, content)
        
        mapping = FrequencyMapping(
            fact_id=fact_id,
            content=content,
            primary_frequency=frequency_type,
            frequency_value=frequency_value,
            resonance_strength=0.8
        )
        
        self.frequency_map[fact_id] = mapping
        print(f"✓ تم تخطيط الحقيقة '{fact_id}' → {frequency_type.name} ({frequency_value:.1f} Hz)")
        
        return mapping

    def _infer_frequency_type(self, content: Any) -> BrainWaveFrequency:
        """
        استنتاج نوع التردد المناسب للمحتوى
        """
        content_str = str(content).lower()
        
        # مؤشرات الذاكرة العميقة
        if any(word in content_str for word in ["أساسي", "جذري", "بدائي", "fundamental", "core"]):
            return BrainWaveFrequency.DELTA
        
        # مؤشرات الذاكرة طويلة المدى
        if any(word in content_str for word in ["يومي", "طويل", "مستمر", "persistent", "long-term"]):
            return BrainWaveFrequency.THETA
        
        # مؤشرات الإبداع
        if any(word in content_str for word in ["إبداعي", "خيال", "تصور", "creative", "imagine"]):
            return BrainWaveFrequency.ALPHA
        
        # مؤشرات الاستدلال المنطقي
        if any(word in content_str for word in ["لأن", "لذا", "إذا", "لكن", "logic", "reason"]):
            return BrainWaveFrequency.BETA
        
        # مؤشرات الوعي الفائق والربط
        if any(word in content_str for word in ["شامل", "متكامل", "كلي", "integration", "holistic"]):
            return BrainWaveFrequency.GAMMA
        
        # الافتراضي
        return BrainWaveFrequency.ALPHA

    def _infer_frequency_value(self, freq_type: BrainWaveFrequency, content: Any) -> float:
        """استنتاج القيمة الدقيقة للتردد"""
        min_freq, max_freq = freq_type.get_range()
        
        # حساب بسيط بناءً على طول المحتوى والتعقيد
        content_complexity = len(str(content)) / 100  # تطبيع
        frequency_value = min_freq + (max_freq - min_freq) * min(content_complexity, 1.0)
        
        return frequency_value

    def update_consciousness_state(
        self,
        frequency: Optional[float] = None,
        awareness_level: Optional[float] = None,
        coherence: Optional[float] = None,
        meditation_depth: Optional[float] = None
    ) -> ConsciousnessState:
        """تحديث حالة الوعي الحالية"""
        if frequency is not None:
            self.consciousness_state.current_frequency = frequency
            # تحديد الموجة الدماغية المسيطرة
            for wave in BrainWaveFrequency:
                if wave.in_range(frequency):
                    self.consciousness_state.dominant_brainwave = wave
                    break
        
        if awareness_level is not None:
            self.consciousness_state.awareness_level = max(0, min(1, awareness_level))
        
        if coherence is not None:
            self.consciousness_state.coherence_index = max(0, min(1, coherence))
        
        if meditation_depth is not None:
            self.consciousness_state.meditation_depth = max(0, min(1, meditation_depth))
        
        self.consciousness_state.timestamp = time.time()
        self.frequency_history.append((
            frequency or self.consciousness_state.current_frequency,
            self.consciousness_state.dominant_brainwave,
            awareness_level or self.consciousness_state.awareness_level
        ))
        
        return self.consciousness_state

    def resonate_with_memory(self, fact_id: str) -> Dict[str, Any]:
        """
        تفعيل رنين مع حقيقة محفوظة
        عندما يتم استدعاء حقيقة، يتم تعديل حالة الوعي للتناسب مع تردد الحقيقة
        """
        if fact_id not in self.frequency_map:
            return {"status": "error", "message": "Fact not found"}
        
        mapping = self.frequency_map[fact_id]
        
        # تحديث حالة الوعي لمطابقة التردد
        self.update_consciousness_state(
            frequency=mapping.frequency_value,
            coherence=mapping.resonance_strength
        )
        
        # تسجيل الرنين
        if fact_id not in self.resonance_records:
            self.resonance_records[fact_id] = []
        
        self.resonance_records[fact_id].append({
            "timestamp": time.time(),
            "frequency": mapping.frequency_value,
            "brainwave": mapping.primary_frequency.name,
            "coherence": mapping.resonance_strength,
            "awareness_level": self.consciousness_state.awareness_level
        })
        
        mapping.access_count += 1
        mapping.last_resonance = time.time()
        
        return {
            "status": "success",
            "fact_id": fact_id,
            "frequency": mapping.frequency_value,
            "brainwave_type": mapping.primary_frequency.name,
            "resonance_strength": mapping.resonance_strength,
            "access_count": mapping.access_count,
            "consciousness_update": {
                "current_frequency": self.consciousness_state.current_frequency,
                "dominant_brainwave": self.consciousness_state.dominant_brainwave.name,
                "coherence": self.consciousness_state.coherence_index
            }
        }

    def find_resonant_facts(
        self,
        target_frequency: Optional[float] = None,
        brainwave_type: Optional[BrainWaveFrequency] = None,
        tolerance: float = 2.0
    ) -> List[Dict[str, Any]]:
        """
        البحث عن الحقائق التي تتوافق مع تردد معين
        يستخدم هذا عندما يصل الدماغ إلى حالة تردد معينة
        """
        target_freq = target_frequency or self.consciousness_state.current_frequency
        
        resonant_facts = []
        for fact_id, mapping in self.frequency_map.items():
            frequency_diff = abs(mapping.frequency_value - target_freq)
            
            # التحقق من المطابقة
            if frequency_diff <= tolerance:
                resonant_facts.append({
                    "fact_id": fact_id,
                    "content": mapping.content,
                    "frequency": mapping.frequency_value,
                    "brainwave": mapping.primary_frequency.name,
                    "frequency_difference": frequency_diff,
                    "resonance_strength": mapping.resonance_strength,
                    "cognitive_relevance": 1.0 - (frequency_diff / tolerance)
                })
        
        # ترتيب حسب أفضل توافق
        resonant_facts.sort(key=lambda x: x["cognitive_relevance"], reverse=True)
        return resonant_facts

    def get_consciousness_report(self) -> Dict[str, Any]:
        """تقرير شامل عن حالة الوعي الحالية"""
        return {
            "current_frequency": self.consciousness_state.current_frequency,
            "dominant_brainwave": self.consciousness_state.dominant_brainwave.name,
            "awareness_level": self.consciousness_state.awareness_level,
            "coherence_index": self.consciousness_state.coherence_index,
            "meditation_depth": self.consciousness_state.meditation_depth,
            "focus_intensity": self.consciousness_state.focus_intensity,
            "total_frequency_mappings": len(self.frequency_map),
            "frequency_history_size": len(self.frequency_history),
            "resonance_activations": sum(len(records) for records in self.resonance_records.values()),
            "brainwave_distribution": self._get_brainwave_distribution()
        }

    def _get_brainwave_distribution(self) -> Dict[str, int]:
        """توزيع الحقائق عبر أنواع الموجات الدماغية"""
        distribution = {wave.name: 0 for wave in BrainWaveFrequency}
        for mapping in self.frequency_map.values():
            distribution[mapping.primary_frequency.name] += 1
        return distribution


class BinauralBeatsGenerator:
    """
    محرر توليد نبضات ثنائية بتردد معين
    تُستخدم لمزامنة الدماغ مع التردد المطلوب
    """

    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.generated_beats = []

    def generate_beats(
        self,
        carrier_frequency: float = 440.0,  # A4 note
        beat_frequency: float = 10.0,  # Target brainwave frequency
        duration_seconds: float = 5.0
    ) -> Tuple[np.ndarray, int]:
        """
        توليد نبضات ثنائية
        
        المبدأ:
        - قناة يسار: carrier_frequency Hz
        - قناة يمين: carrier_frequency + beat_frequency Hz
        - الفرق ينتج "نبضة" بتردد = beat_frequency
        """
        t = np.linspace(0, duration_seconds, int(self.sample_rate * duration_seconds))
        
        # القناة اليسرى
        left = np.sin(2 * np.pi * carrier_frequency * t)
        
        # القناة اليمنى (بتردد أعلى)
        right = np.sin(2 * np.pi * (carrier_frequency + beat_frequency) * t)
        
        # الجمع
        stereo = np.vstack([left, right])
        
        return stereo, self.sample_rate

    def save_beats_to_file(
        self,
        output_path: str,
        carrier_frequency: float = 440.0,
        beat_frequency: float = 10.0,
        duration_seconds: float = 60.0
    ):
        """حفظ النبضات كملف صوتي"""
        try:
            import scipy.io.wavfile as wavfile
            
            stereo, sr = self.generate_beats(carrier_frequency, beat_frequency, duration_seconds)
            
            # تطبيع
            stereo = (stereo / np.max(np.abs(stereo)) * 32767).astype(np.int16)
            
            # حفظ
            wavfile.write(output_path, sr, stereo.T)
            print(f"✓ تم حفظ النبضات في: {output_path}")
            
        except ImportError:
            print("⚠️ scipy غير مثبت. استخدم: pip install scipy")


def create_frequency_resonance_engine() -> FrequencyResonanceEngine:
    """إنشاء محرك الرنين الترددي"""
    return FrequencyResonanceEngine()


# ====================== مثال التشغيل ======================

if __name__ == "__main__":
    print("=" * 70)
    print("🧠 BetaRoot Frequency Resonance System - Demo")
    print("=" * 70)
    
    # إنشاء المحرك
    resonance = create_frequency_resonance_engine()
    
    # 1. تخطيط الحقائق إلى ترددات
    print("\n1️⃣  تخطيط الحقائق إلى الترددات الدماغية:")
    
    facts = [
        ("f1", "كل البشر فانون - حقيقة أساسية", BrainWaveFrequency.DELTA),
        ("f2", "الحب يستمر في القلب - ذاكرة طويلة المدى", BrainWaveFrequency.THETA),
        ("f3", "التخيل يخلق واقع جديد - إبداع", BrainWaveFrequency.ALPHA),
        ("f4", "إذا A ثم B - استدلال منطقي", BrainWaveFrequency.BETA),
        ("f5", "تكامل الوعي والمادة - وعي فائق", BrainWaveFrequency.GAMMA),
    ]
    
    for fact_id, content, freq_type in facts:
        mapping = resonance.map_fact_to_frequency(fact_id, content, freq_type)
        print(f"   • {fact_id}: {content[:50]}...")
        print(f"     → {mapping.primary_frequency.name} ({mapping.frequency_value:.2f} Hz)")
    
    # 2. تحديث حالة الوعي
    print("\n2️⃣  تحديث حالة الوعي:")
    
    # سيناريو: الدخول في حالة تأمل عميق
    consciousness = resonance.update_consciousness_state(
        frequency=6.0,  # Theta
        awareness_level=0.7,
        coherence=0.8,
        meditation_depth=0.6
    )
    print(f"   • التردد الحالي: {consciousness.current_frequency:.2f} Hz")
    print(f"   • موجة الدماغ: {consciousness.dominant_brainwave.name}")
    print(f"   • مستوى الوعي: {consciousness.awareness_level:.1%}")
    print(f"   • عمق التأمل: {consciousness.meditation_depth:.1%}")
    
    # 3. البحث عن الحقائق الرنينية
    print("\n3️⃣  الحقائق الرنينية عند التردد الحالي:")
    
    resonant = resonance.find_resonant_facts(tolerance=3.0)
    for fact in resonant:
        print(f"   • {fact['fact_id']}: {fact['content'][:40]}...")
        print(f"     → توافق: {fact['cognitive_relevance']:.1%} | تردد: {fact['frequency']:.2f} Hz")
    
    # 4. تفعيل الرنين مع حقيقة
    print("\n4️⃣  تفعيل الرنين مع حقيقة محفوظة:")
    
    resonance_result = resonance.resonate_with_memory("f2")
    print(f"   • الحقيقة: f2")
    print(f"   • التردد الجديد: {resonance_result['frequency']:.2f} Hz")
    print(f"   • قوة الرنين: {resonance_result['resonance_strength']:.1%}")
    print(f"   • عدد الاستدعاءات: {resonance_result['access_count']}")
    
    # 5. تقرير شامل
    print("\n5️⃣  تقرير حالة الوعي:")
    report = resonance.get_consciousness_report()
    print(f"   • توزيع الحقائق عبر الموجات:")
    for wave, count in report['brainwave_distribution'].items():
        print(f"     - {wave}: {count} حقيقة")
    print(f"   • إجمالي التنشيطات الرنينية: {report['resonance_activations']}")
    
    # 6. توليد نبضات ثنائية
    print("\n6️⃣  توليد نبضات ثنائية:")
    
    generator = BinauralBeatsGenerator()
    print("   • جاري توليد نبضات Theta (للتأمل العميق)...")
    # generator.save_beats_to_file(
    #     "/home/claude/theta_meditation.wav",
    #     carrier_frequency=440.0,
    #     beat_frequency=6.0,
    #     duration_seconds=10.0
    # )
    print("   ✓ يمكن توليد ملفات صوتية للتأمل الموجه")
    
    print("\n" + "=" * 70)
    print("✨ نظام الرنين الترددي متكامل ومستعد!")
    print("=" * 70)

def assess_coherence(self, current_freq: float = 7.83, amplitude: float = 1.0):
    deviation = abs(current_freq - self.BASE_FREQUENCY)
    coherence_score = max(0.0, 1.0 - (deviation / 2.0))  # مثال بسيط
    
    if coherence_score < 0.7:
        return {
            "status": "CONTAMINATED",
            "deviation": deviation,
            "suggested_action": "Activate Unary Correction + 7.83 Hz Entrainment Pattern",
            "coherence": coherence_score
        }
    return {"status": "COHERENT", "coherence": coherence_score}
