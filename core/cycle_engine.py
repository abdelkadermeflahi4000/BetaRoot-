# core/cycle_engine.py

from typing import Callable, Dict, List, Any, Optional
import time


# ========================
# 🧬 State Definition
# ========================

class CycleState:
    def __init__(
        self,
        name: str,
        action: Callable[[Dict], Dict],
        duration: float = 0.0,
        metadata: Optional[Dict] = None
    ):
        self.name = name
        self.action = action
        self.duration = duration
        self.metadata = metadata or {}

    def execute(self, system_state: Dict) -> Dict:
        return self.action(system_state)


# ========================
# 🔁 Transition Controller
# ========================

class TransitionController:
    def __init__(self, states: List[CycleState]):
        self.states = {s.name: s for s in states}
        self.order = [s.name for s in states]

    def next(self, current_name: str) -> str:
        idx = self.order.index(current_name)
        return self.order[(idx + 1) % len(self.order)]

    def get(self, name: str) -> CycleState:
        return self.states[name]


# ========================
# 🧠 Feedback System
# ========================

class FeedbackSystem:
    def evaluate(self, prev_state: Dict, new_state: Dict) -> Dict:
        return {
            "delta": {
                k: new_state.get(k, 0) - prev_state.get(k, 0)
                for k in new_state
            }
        }


# ========================
# 🧠 Memory Interface (plug-in)
# ========================

class CycleMemory:
    def __init__(self):
        self.history = []

    def store(self, entry: Dict):
        self.history.append(entry)

    def get_last(self):
        return self.history[-1] if self.history else None


# ========================
# 🤖 Agent Interface (optional)
# ========================

class CycleAgent:
    def decide(self, system_state: Dict, feedback: Dict) -> Optional[str]:
        """
        Return next state name or None for default transition
        """
        return None


# ========================
# 🌍 World Adapter (optional)
# ========================

class WorldAdapter:
    def observe(self) -> Dict:
        return {}

    def apply(self, state: Dict):
        pass


# ========================
# 🚀 Core Cycle Engine
# ========================

class CycleEngine:
    def __init__(
        self,
        states: List[CycleState],
        agent: Optional[CycleAgent] = None,
        memory: Optional[CycleMemory] = None,
        feedback_system: Optional[FeedbackSystem] = None,
        world: Optional[WorldAdapter] = None,
        sleep: float = 0.0
    ):
        self.controller = TransitionController(states)
        self.agent = agent or CycleAgent()
        self.memory = memory or CycleMemory()
        self.feedback = feedback_system or FeedbackSystem()
        self.world = world or WorldAdapter()

        self.current_state_name = states[0].name
        self.sleep = sleep

    def step(self, system_state: Dict) -> Dict:
        state_obj = self.controller.get(self.current_state_name)

        prev_state = dict(system_state)

        # 🔧 Execute state logic
        new_state = state_obj.execute(system_state)

        # 🧠 Feedback
        feedback = self.feedback.evaluate(prev_state, new_state)

        # 🤖 Agent decision
        decision = self.agent.decide(new_state, feedback)

        if decision and decision in self.controller.states:
            next_state = decision
        else:
            next_state = self.controller.next(self.current_state_name)

        # 🧠 Memory store
        self.memory.store({
            "state": self.current_state_name,
            "next": next_state,
            "data": new_state,
            "feedback": feedback
        })

        # 🌍 Apply to world
        self.world.apply(new_state)

        # 🔁 Transition
        self.current_state_name = next_state

        if state_obj.duration > 0 or self.sleep > 0:
            time.sleep(max(state_obj.duration, self.sleep))

        return new_state

    def run(self, initial_state: Dict, steps: int = 10) -> Dict:
        state = initial_state
        for _ in range(steps):
            observed = self.world.observe()
            state.update(observed)

            state = self.step(state)

        return state


# ========================
# 🧪 Example Use (can remove in production)
# ========================

if __name__ == "__main__":

    def fill(s):
        s["water"] = s.get("water", 0) + 10
        return s

    def wash(s):
        s["dirt"] = s.get("dirt", 1.0) * 0.5
        return s

    def spin(s):
        s["water"] = s.get("water", 0) * 0.2
        return s

    states = [
        CycleState("Fill", fill),
        CycleState("Wash", wash),
        CycleState("Spin", spin),
    ]

    engine = CycleEngine(states)

    final = engine.run({"water": 0, "dirt": 1.0}, steps=6)

    print(final)

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
