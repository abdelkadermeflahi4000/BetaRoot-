# betaroot/core/cycle_engine.py
import time
import asyncio
from datetime import datetime
from typing import Dict, Any
from .unary_logic import create_engine as create_unary_engine
from .causal_graph import create_causal_builder
from .memory import create_memory_system
from .frequency_resonance import FrequencyResonance

class CycleEngine:
    """
    محرك الدورة الحياتية لـ BetaRoot
    observe → plan → act → evaluate → learn
    """
    
    def __init__(self):
        self.unary = create_unary_engine()
        self.causal = create_causal_builder()
        self.memory = create_memory_system()
        self.resonance = FrequencyResonance()  # ربط بالـ Schumann
        
        self.cycle_count = 0
        self.last_state = None
        self.running = False

    async def observe(self) -> Dict:
        """مرحلة الملاحظة (Environment + Internal State)"""
        # 1. قراءة الترددات (Schumann / biophoton / local sensors)
        freq_status = self.resonance.calculate_wrong_pressure(
            f_current=7.83 + 0.2 * (self.cycle_count % 10),  # محاكاة
            tech_intensity=0.4,
            contamination=0.3
        )
        
        # 2. حالة الذاكرة
        memory_stats = self.memory.get_stats()
        
        # 3. حالة النظام
        return {
            "timestamp": datetime.now().isoformat(),
            "cycle": self.cycle_count,
            "frequency_status": freq_status,
            "memory_stats": memory_stats,
            "internal_state": self.last_state or "initial"
        }

    async def plan(self, observation: Dict) -> Dict:
        """مرحلة التخطيط (Unary Logic + Causal Graph)"""
        # تحويل الملاحظة إلى تمثيل آحادي
        state = self.unary.encode(observation)
        
        # بناء أو تحديث الـ causal graph
        if observation["frequency_status"]["status"] == "CONTAMINATED":
            self.causal.add_causal_relation(
                cause="frequency_contamination",
                effect="consciousness_pressure",
                relation_type="direct"
            )
        
        # خطة بسيطة في V1
        plan = {
            "action": "correct_frequency" if observation["frequency_status"]["correction_needed"] else "learn_from_memory",
            "priority": 0.9 if observation["frequency_status"]["correction_needed"] else 0.4,
            "reason": "ضغط خاطئ مكتشف" if observation["frequency_status"]["correction_needed"] else "تعلم روتيني"
        }
        return plan

    async def act(self, plan: Dict) -> Dict:
        """تنفيذ الخطة"""
        if plan["action"] == "correct_frequency":
            result = {"success": True, "corrected": True, "message": "تم تفعيل Unary Correction Pattern"}
        else:
            result = {"success": True, "message": "تم استرجاع ذاكرة وتعلم جديد"}
        
        return result

    async def evaluate(self, observation: Dict, action_result: Dict) -> Dict:
        """تقييم النتيجة"""
        score = 0.85 if action_result.get("success") else 0.3
        return {
            "cycle_score": score,
            "feedback": "جيد" if score > 0.7 else "يحتاج تحسين",
            "learned": f"تم اكتشاف ضغط ترددي في الدورة {self.cycle_count}"
        }

    async def learn(self, evaluation: Dict):
        """التعلم والحفظ في الذاكرة الدائمة"""
        self.memory.store_fact(
            content=evaluation,
            priority=0.8,
            source="cycle_engine"
        )
        self.cycle_count += 1

    async def run_cycle(self):
        """دورة كاملة واحدة"""
        obs = await self.observe()
        plan = await self.plan(obs)
        action = await self.act(plan)
        eval_result = await self.evaluate(obs, action)
        await self.learn(eval_result)
        
        self.last_state = eval_result
        print(f"✅ Cycle {self.cycle_count} completed | Score: {eval_result['cycle_score']:.2f}")

    async def start(self, interval_seconds: int = 60):
        """تشغيل الدورة الدائمة"""
        self.running = True
        print("🌍 BetaRoot Living Core بدأ العمل...")
        
        while self.running:
            await self.run_cycle()
            await asyncio.sleep(interval_seconds)

    def stop(self):
        self.running = False
        print("⏹️ تم إيقاف Cycle Engine")


# ====================== تشغيل سريع ======================
if __name__ == "__main__":
    engine = CycleEngine()
    asyncio.run(engine.start(interval_seconds=30))   # كل 30 ثانية دورة
